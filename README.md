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
