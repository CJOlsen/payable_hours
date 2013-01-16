Project: Payable Hours
Author: Christopher Olsen
License: GNU GPL (see LICENSE.txt)
Version: 0.01 (in development)

About:
	Payable Hours is a program for the tracking of clients, projects,
and hours worked.  It is written in Python using TKinter for the GUI and
MySQL for the backend.  It has a simple ORM (object-relational mapping)
system for communicating with the database, which may not be necessary but
makes for a clear layer of abstraction.  

Payable Hours follows the Model-View-Controller (MVC) design paradigm of 
which the the Model and the View are much farther along than the Controller.
The current plan is to scrap what little is there for the Controller and
rebuild using the GOF's Observer pattern so changes in one tab will be 
reflected in the other tabs as well.

TODO: * Design the controller logic
      * Possibly change the naming convention from CamelCasing to 
        underscores_for_new_words

Requires:
	Python 2.7, MySQL and TKinter


It would be appreciated if the project isn't forked until it's functional,
though the GPL license makes it legal to do so.


As always questions, ideas and help are appreciated.
