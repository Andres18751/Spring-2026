import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone


TWITCH_TOKEN_URL = 'https://id.twitch.tv/oauth2/token'
TWITCH_API_BASE_URL = 'https://api.twitch.tv/helix'
TWITCH_TOKEN_CACHE_KEY = 'twitch_app_access_token'


class TwitchAPIError(Exception):
    pass


def is_configured():
    return bool(settings.TWITCH_CLIENT_ID and settings.TWITCH_CLIENT_SECRET)


def extract_twitch_login(twitch_url):
    parsed_url = urlparse(twitch_url)
    hostname = parsed_url.netloc.lower().removeprefix('www.')

    if hostname != 'twitch.tv':
        return ''

    return parsed_url.path.strip('/').split('/')[0].lower()


def get_app_access_token():
    cached_token = cache.get(TWITCH_TOKEN_CACHE_KEY)
    if cached_token:
        return cached_token

    if not is_configured():
        raise TwitchAPIError('Twitch API credentials are not configured.')

    payload = urlencode({
        'client_id': settings.TWITCH_CLIENT_ID,
        'client_secret': settings.TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }).encode('utf-8')

    request = Request(
        TWITCH_TOKEN_URL,
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )

    data = _send_json_request(request)
    access_token = data.get('access_token')
    expires_in = data.get('expires_in', 3600)

    if not access_token:
        raise TwitchAPIError('Twitch did not return an access token.')

    cache.set(TWITCH_TOKEN_CACHE_KEY, access_token, max(expires_in - 60, 60))
    return access_token


def get_channel_profile(login):
    response = _helix_get('/users', {'login': login})
    users = response.get('data', [])
    return users[0] if users else None


def get_stream_status(login):
    response = _helix_get('/streams', {'user_login': login})
    streams = response.get('data', [])
    return streams[0] if streams else None


def hydrate_event_twitch_data(event):
    if not event.twitch_url:
        return event

    login = extract_twitch_login(event.twitch_url)
    if not login:
        return event

    event.twitch_login = login

    profile = get_channel_profile(login)
    if profile:
        event.twitch_display_name = profile.get('display_name', '')
        event.twitch_profile_image_url = profile.get('profile_image_url', '')
        event.twitch_broadcaster_type = profile.get('broadcaster_type', '')

    refresh_event_live_status(event)
    return event


def refresh_event_live_status(event):
    if not event.twitch_login:
        return event

    stream = get_stream_status(event.twitch_login)
    event.twitch_live_status = bool(stream)
    event.twitch_last_checked_at = timezone.now()

    if stream:
        event.twitch_stream_title = stream.get('title', '')
        event.twitch_stream_game_name = stream.get('game_name', '')
        event.twitch_viewer_count = stream.get('viewer_count')
    else:
        event.twitch_stream_title = ''
        event.twitch_stream_game_name = ''
        event.twitch_viewer_count = None

    return event


def _helix_get(path, params):
    access_token = get_app_access_token()
    query_string = urlencode(params)
    request = Request(
        f'{TWITCH_API_BASE_URL}{path}?{query_string}',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Client-Id': settings.TWITCH_CLIENT_ID,
        },
        method='GET',
    )
    return _send_json_request(request)


def _send_json_request(request):
    try:
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as error:
        raise TwitchAPIError(f'Twitch API request failed with status {error.code}.') from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise TwitchAPIError('Unable to reach Twitch API right now.') from error
