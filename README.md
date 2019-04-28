# hiv-alliance-sheltercare-quack-for-a-cause-2019
Please ignore the work in the Shelter Care directory -- we started working on that project just in case we had time to get around to it, but we did not.

We created a web application which you can see live at https://hiv-alliance.herokuapp.com/.

The purpose of this application is to provide the staff and volunteers at HIV Alliance a tool that they can use to keep track of the interactions they have with their clients.

A "client" represents a unique individual who uses HIV Alliance's services.  An "encounter" is an event where a client visits a HIV Alliance location for services.  You can save many different pieces of information in the "client" and the "encounter" views.  You can add, view, and edit any of the things mentioned in addition to using the search tools to find existing clients and log new encounters for them.

Finally, there's a report tool which you can use to analyze and look for pieces of information using more detailed queries.

Run the app localy with (using python 3.6.8)
* pip install -r requirements.txt
* preflight.sh HIVA

This will launch app server at `localhost:5000`.

Participants:
* Sam Oberg
* Jeff Knees
* Brandon Sov
* Alex Geoffrey
* Daniel su
