# Spring-2026
CSCI 3340-04

Samuel Gonzalez, Andres Cazares, Pablo Magana

Project Desc:

The goal of our application is to create a social matchmaking website that is based on / out of the UTRGV Game Room. Users will be able to create their own profile and interact with others who share interests in certain games. Aditionally, they'll be able to schedule / view meeting times corresponding to the time of day, genre of game, etc. (Will update the description as we progress further in development.)

Agile Planning:

1.
Considering that we have an overall understanding of how we want the application to function, and the purpose it serves, our first goal is to get a basic webpage going as we learn more about Django. To prevent us from being overwhelmed and "biting off more than what we can chew", we decided to structure our application off of the UTRGV Game Room. Seeing as that area has specific games / stations, and is only open for certain hours, it ensures we can focus on the communication aspect without being bogged down by the open-ended possibilites of the assignment. Granted, we do have a lot of ideas, but it's best to take a practical approach as we start out and learn more about developing a webpage, and eventually add things such as profile customizations, live chatting, guest accounts, etc.


4 / 14 / 2026 Second Preliminary Note:

The application when ran, directs users to the homescreen. From there they are able to create an account, log into an existing one, and even browse the calendar to see if there are any events on certain days. If there is an ongoing event, it will show up on the homepage, allowing users to not have to check the calendar. Additionally, users who create an account are now able to customize their own profile. At the moment, users are only able to update their bios, however we plan on expanding it to allow more personalization. We also plan on improving the visibility of who is online and who is interested in certain events to promote an easier way of communicating.

If an admin wants to create / schedule an event, then they're able to do so by using Django's built in system. By going to http://localhost:8000/admin/ and navigating under the mycalendar tab, Admins can schedule events, while also being able to check user data by navigating under the Authentication and Authorization tab.


5 / 11 / 2026 Final Presentation

The finalized application is similar to the 2nd preliminary but with a lot more quality of life changes alongside more visual feedback and customizability. There's now an easy accessible toggle to switch between a darker presentation or a light version (dark / light mode.) Additionally, superusers / admins can now directly create and manage events from the home page if they are logged in (in comparison to the previous build where it was only through http://localhost:8000/admin/). This feature is only accessible to those in the "Tornament Organizer" group. (You can create groups with access to various features from http://localhost:8000/admin/) Regardless, everyone who has an account can customize their "loadout" (profile) even more now. Since the application is structured based off a competitive gaming audience, there's now options to display your available days, times, comp. game interests, etc. Users are also able to upload their own profile picture as well. 

Events are now more streamlined and easier to create and customize. Users can now set a specific start time, on top of adding a link to a Twitch stream that'll be livestreaming said event. The application calls upon the Twitch API to show users in real time the status of the event host. It shows their twitch profile, if they're online, and their overall status. 