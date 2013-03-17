## Payable Hours
## Python 2.7
## Christopher Olsen

# Copyright Notice: Copyright 2012 Christopher Olsen
# License: GNU General Public License, v3 (see LICENSE.txt)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import MySQLdb as mdb
import datetime
import time
import sys

# globals 
connection = None
cursor = None

# general database operations
# these methods are the interface for the database and database objects

def connectDB():
    """ Tries to create a connection to the MySQL database.
        Returns: connection, cursor (which are None if the con fails)
        
        """
    global connection, cursor
    try:
        connection = mdb.connect('localhost',
                                 'james',
                                 'password',
                                 'PayableHours');

        cursor = connection.cursor()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    return connection, cursor

def disconnectDB():
    """ Disconnects from the database.
        Returns: nothing
        
        """
    if connection:
        connection.commit()
        connection.close()


def create_table_structure():
    """ Needs a connection with an empty database and sufficient privileges.
        Creates the table structure for the program (subject to change.)
        Returns: nothing
        
        """
    global connection, cursor
    cursor.execute("CREATE TABLE company ("\
                   "name VARCHAR(50),"\
                   "address VARCHAR(50),"\
                   "city VARCHAR(20),"\
                   "state VARCHAR(2),"\
                   "phone VARCHAR(15),"\
                   "notes VARCHAR(200),"\
                   "PRIMARY KEY (name));")
    connection.commit()
    cursor.execute("CREATE TABLE contact ("\
                   "name VARCHAR(50),"\
                   "phone VARCHAR(15),"\
                   "email VARCHAR(30),"\
                   "notes VARCHAR(200),"\
                   "company_name VARCHAR(50),"\
                   "PRIMARY KEY (name));")
    connection.commit()
    cursor.execute("CREATE TABLE project ("\
                   "name VARCHAR(50),"\
                   "company_name VARCHAR(50),"\
                   "contact_name VARCHAR(50),"\
                   "hourly_pay DECIMAL(5,2),"\
                   "quoted_hours INT(11),"\
                   "worked_hours DECIMAL(6,2),"\
                   "billed_hours DECIMAL(6,2),"\
                   "total_invoiced DECIMAL(7,2),"\
                   "total_paid DECIMAL(7,2),"\
                   "money_owed DECIMAL(7,2),"\
                   "project_active TINYINT(1),"\
                   "notes VARCHAR(400),"\
                   "PRIMARY KEY (name));")
    connection.commit()
    cursor.execute("CREATE TABLE session ("\
                   "sessionID VARCHAR(20),"\
                   "company_name VARCHAR(50),"\
                   "project_name VARCHAR(50),"\
                   "project_session_number INT(4),"\
                   "start_time DATETIME,"\
                   "stop_time DATETIME,"\
                   "time TIME,"\
                   "notes VARCHAR(400),"\
                   "git_commit VARCHAR(12),"\
                   "PRIMARY KEY (project_name, project_session_number));")
    connection.commit()



    
# objects correspond to relations (this is a simple ORM system)
class Company(object):
    """ ORM Company class.  Interface for the "company" table of the database

        """
    def __init__(self, companyID =None, name=None, address=None, city=None,
                 state=None, phone=None, notes=None):
        self.companyID = companyID
        self.name      = name
        self.address   = address
        self.city      = city
        self.state     = state
        self.phone     = phone
        self.notes     = notes

    @classmethod
    def get_by_name(cls,name):
        ## these get_by_name methods might need to be reworked?
        ## the if/else statements especially
        """ Takes a name string
            Returns: a new Company instance populated from the database
            
            """
        global cursor
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM company WHERE name=%s",(name))
        record_dict = cursor.fetchall()[0]

        new_object = Company()
        
        if record_dict:
            new_object.name = record_dict['name']
            new_object.address = record_dict['address']
            new_object.city = record_dict['city']
            new_object.state = record_dict['state']
            new_object.phone = record_dict['phone']
            new_object.notes = record_dict['notes']
        else:
            print 'there was an error'
            
        cursor = connection.cursor()
        return new_object

    @classmethod
    def delete_by_name(cls, name):
        """ Takes a name string
            Removes the corresponding company entry, if any, from the database
            Returns: nothing
            
            """
        global cursor, connection
        cursor.execute("DELETE FROM company WHERE name=%s", (name))
        connection.commit()
   
    def write(self):
        """ Writes the Company instance's values to the database
            Returns: nothing
            
            """
        global cursor
        cursor.execute("REPLACE INTO company "\
                       "(name, address, city, state, phone, notes)"\
                        " VALUES (%s,%s,%s,%s,%s,%s)",\
                        (self.name,self.address,self.city,\
                        self.state,self.phone,self.notes))
        connection.commit()

    @staticmethod
    def get_all_companies():
        """ Returns: a list of all company names

            """
        cursor.execute("SELECT name FROM company")
        return [x[0] for x in cursor.fetchall()]

    @staticmethod
    def delete_company_by_name(name):
        """ Takes a name string
            Deletes the corresponding company from the database
            Returns: nothing
            
            """
        company=Company()
        company.delete_by_name(name)
        

class Contact(object):
    """ ORM Contact class.  Interface for the "contact" table of the database
    
        """
    def __init__(self, name=None, company_name=None, phone=None,
                 email=None, notes=None):
        self.name = name
        self.company_name = company_name
        self.phone = phone
        self.email = email
        self.notes = notes

    def write(self):
        """ Writes the Contact instance's values to the database
            Returns: nothing
            
            """
        cursor.execute("REPLACE INTO contact "\
                       "(company_name, name, phone, email, notes)"\
                       " VALUES (%s,%s,%s,%s,%s)",\
                        (self.company_name,self.name,self.phone,\
                        self.email,self.notes))
        connection.commit()

    @classmethod
    def get_by_name(cls,name):
        """ Takes a name
            Returns: a new Contact instance populated from the database
            
            """
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM contact WHERE name=%s",(name))
        record_dict = cursor.fetchall()[0]

        new_contact_obj = Contact()
        if record_dict:
            new_contact_obj.company_name = record_dict['company_name']
            new_contact_obj.name = record_dict['name']
            new_contact_obj.email = record_dict['email']
            new_contact_obj.notes = record_dict['notes']
            new_contact_obj.phone = record_dict['phone']
        else:
            print 'there was an error'

        cursor = connection.cursor()
        return new_contact_obj

    @staticmethod
    def get_all_contacts():
        """ Returns: all names from the contact table
    
            """
        cursor.execute("SELECT name FROM contact")
        return cursor.fetchall()

    @staticmethod
    def delete_by_name(name):
        """ Takes a name string
            Removes the corresponding company entry, if any, from the database
            Returns: nothing
            
            """
        global cursor, connection
        cursor.execute("DELETE FROM contact WHERE name=%s", (name))
        connection.commit()



class Project(object):
    """ ORM Project class.  Interface for the "project" table of the database

        """
    # todo: fix order
    def __init__(self, 
                 name =None, company_name =None, hourly_pay =None,
                 quoted_hours =None, worked_hours =None, billed_hours =None,
                 total_invoiced =None, total_paid =None, money_owed =None,
                 project_active =None, contact_name =None, notes =None):
        self.name = name
        self.company_name = company_name
        self.hourly_pay = hourly_pay
        self.quoted_hours = quoted_hours
        self.worked_hours = worked_hours
        self.billed_hours = billed_hours
        self.total_invoiced = total_invoiced
        self.total_paid = total_paid
        self.money_owed = money_owed
        self.project_active = project_active
        self.contact_name = contact_name
        self.company_name = company_name
        self.notes = notes

    def write(self):
        """ Writes the Project instance's values to the database
            Returns: nothing
            
            """
        cursor.execute("REPLACE INTO project "\
                       "(name, company_name, contact_name, hourly_pay, "\
                       "quoted_hours, worked_hours, billed_hours, "\
                       "total_invoiced, total_paid, money_owed, "\
                       "project_active, notes)"\
                       " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                        (self.name,self.company_name,self.contact_name,
                         self.hourly_pay, self.quoted_hours, self.worked_hours,
                         self.billed_hours,self.total_invoiced,
                         self.total_paid,self.money_owed, self.project_active,
                         self.notes))
        
        connection.commit()

    @classmethod
    def get_by_name(cls,name):
        """ Takes a project name
            Returns: a new Project instance populated from the database
            
            """
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM project WHERE name=%s",(name))
        record_dict = cursor.fetchall()[0]

        new_project_obj = Project()
        if record_dict:
            new_project_obj.name = record_dict['name']
            new_project_obj.company_name = record_dict['company_name']
            new_project_obj.hourly_pay = record_dict['hourly_pay']
            new_project_obj.quoted_hours = record_dict['quoted_hours']
            new_project_obj.worked_hours = record_dict['worked_hours']
            new_project_obj.billed_hours = record_dict['billed_hours']
            new_project_obj.total_invoiced = record_dict['total_invoiced']
            new_project_obj.total_paid = record_dict['total_paid']
            new_project_obj.money_owed = record_dict['money_owed']
            new_project_obj.project_active = record_dict['project_active']
            new_project_obj.contact_name = record_dict['contact_name']
            new_project_obj.notes = record_dict['notes']
        else:
            print 'there was an error'

        cursor = connection.cursor()
        return new_project_obj

    @staticmethod
    def get_all_projects():
        """ Returns: all names from the project table
            
            """
        cursor.execute("SELECT name FROM project")
        return cursor.fetchall()

    @staticmethod
    def get_active_projects():
        """ Returns: all names from the project table if the project is active
            
            """
        cursor.execute("SELECT name FROM project WHERE projectActive = True")
        return cursor.fetchall()

    @staticmethod
    def delete_by_name(name):
        """ Takes a name string
            Removes the corresponding project entry, if any, from the database
            Returns: nothing
            
            """
        global cursor, connection
        cursor.execute("DELETE FROM project WHERE name=%s", (name))
        connection.commit()

    
class Session(object):
    """ ORM Session class.  Interface for the "session" table of the database
        
        """
    def __init__(self, sessionID=None, company_name =None, project_name =None,
                 project_session_number=None, start_time =None, stop_time =None,
                 time =None, notes =None, git_commit =None):
        self.sessionID = sessionID
        self.company_name = company_name
        self.project_name = project_name
        self.project_session_number = project_session_number
        self.start_time = start_time
        self.stop_time = stop_time
        self.time = time
        self.notes = notes
        self.git_commit = git_commit

    def write(self):
        """ Writes the values of the Session instance to the database
            Returns: nothing
            
            """
        self.sessionID = self.make_sessionID()
        
        cursor.execute("REPLACE INTO session "\
                       "(sessionID, company_name, project_name,"\
                       "project_session_number, start_time, stop_time, time, "\
                       "notes, git_commit)"\
                       " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                        (self.sessionID, self.company_name, self.project_name,
                         self.project_session_number, self.start_time,
                         self.stop_time, self.time, self.notes,
                         self.git_commit))
        connection.commit()

    @classmethod
    def get_session_by_sessionID(cls,sessionID):
        """ Takes a sessionID
            Returns: a new Session object populated from the database
            
            """
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM session WHERE sessionID=%s",(sessionID))
        record_dict = cursor.fetchall()[0]

        new_session_obj = Session()
        if record_dict:
            new_session_obj.sessionID = record_dict['sessionID']
            new_session_obj.company_name = record_dict['company_name']
            new_session_obj.project_name = record_dict['project_name']
            new_session_obj.project_session_number = record_dict[
                'project_session_number']
            new_session_obj.start_time = record_dict['start_time']
            new_session_obj.stop_time = record_dict['stop_time']
            new_session_obj.time = record_dict['time']
            new_session_obj.notes = record_dict['notes']
            new_session_obj.git_commit = record_dict['git_commit']

        else:
            print 'there was an error'
            
        cursor = connection.cursor()
        return new_session_obj

    def make_sessionID(self):
        """ Returns: a string in the form "project_name.4" where 4 would
                     designate the 4th project session
            
            """
        cursor.execute("SELECT MAX(project_session_number) FROM session WHERE "\
                       "project_name=%s", (self.project_name))
        max_number = cursor.fetchone()[0] + 1
        self.project_session_number = max_number
        return '.'.join([self.project_name, str(max_number)])

