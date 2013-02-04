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
import sys

# globals 
connection = None
cursor = None

# general database operations
# these methods are the interface for the database and database objects

def connectDB():
    """ Takes: nothing
        Tries to create a connection to the MySQL database.
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
    """ Takes: nothing
        Disconnects from the database.
        Returns: nothing
        """
    if connection:
        connection.commit()
        connection.close()


def create_table_structure():
    """ Needs a connection with an empty database and sufficient privileges.
        Creates the table structure for the program (subject to change.)
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
                   "id INT(11),"\
                   "company_name VARCHAR(50),"\
                   "project_name VARCHAR(50),"\
                   "start_time DATETIME,"\
                   "stop_time DATETIME,"\
                   "time TIME,"\
                   "notes VARCHAR(400),"\
                   "PRIMARY KEY (id));")
    connection.commit()
                   





def get_all_companies():
    """ Takes: nothing
        Selects all names from the company table
        Returns: all company names
        """
    cursor.execute("SELECT name FROM company")
    return [x[0] for x in cursor.fetchall()]
    
def get_company_by_name(name):
    """ Takes: a name string
        Returns: a company object corresponding to the name
        """
    company = Company()
    return company.get_by_name(name)

def delete_company_by_name(name):
    """ Takes: a name string
        Deletes the corresponding company from the database
        Returns: nothing
        """
    company=Company()
    company.delete_by_name(name)

def get_contact_by_name(name):
    """ Takes: a name string
        Returns: a contact object corresponding to the name
        """
    contact = Contact()
    return contact.get_by_name(name)

def delete_contact_by_name(name):
    """ Takes: a name string
        Deletes the corresponding contact from the database
        Returns: nothing
        """
    contact=Contact()
    contact.delete_by_name(name)
    

def get_all_projects():
    """ Takes: nothing
        Returns: all names from the project table
        """
    cursor.execute("SELECT name FROM project")
    return cursor.fetchall()

def get_active_projects():
    """ Takes: nothing
        Returns: all names from the project table if the project is active
        """
    cursor.execute("SELECT name FROM project WHERE projectActive = True")
    return cursor.fetchall()

def get_all_contacts():
    """ Takes: nothing
        Returns: all names from the contact table
        """
    cursor.execute("SELECT name FROM contact")
    return cursor.fetchall()

def get_contacts_for_company(name):
    # to do
    pass

def get_contact_by_ID():
    # to do
    pass
    


    
# objects correspond to relations (this is a simple ORM system)
class Company(object):
    def __init__(self, companyID =None, name=None, address=None, city=None,
                 state=None, phone=None, notes=None):
        self.companyID = companyID
        self.name      = name
        self.address   = address
        self.city      = city
        self.state     = state
        self.phone     = phone
        self.notes     = notes

    # because Python doesn't allow multiple init's it's easier to initialize
    # a new object in two steps than mangle(?) __init__, but getByName really
    # is part of the initialization process (conceptually)
    def get_by_name(self,name):
        """ Takes: a name string
            Queries the database for the company corresponding to the name
            string, and maps attributes ot local variables.
            Returns: self
            """
        global cursor
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM company WHERE name=%s",(name))
        record_dict = cursor.fetchall()[0]
        
        if record_dict:
            self.name      = record_dict['name']
            self.address   = record_dict['address']
            self.city      = record_dict['city']
            self.state     = record_dict['state']
            self.phone     = record_dict['phone']
            self.notes     = record_dict['notes']
        else:
            print 'there was an error'
            
        cursor = connection.cursor()
        return self

    def delete_by_name(self, name):
        """ Takes a name string
            Removes the corresponding company entry, if any, from the database
            Returns nothing
            """
        global cursor, connection
        cursor.execute("DELETE FROM company WHERE name=%s", (name))
        connection.commit()
   
    def write(self):
        """ Takes: nothing (implied self)
            Writes all data in the company object to the database, and commits
            Returns: Nothing
            """
        global cursor
        cursor.execute("REPLACE INTO company "\
                       "(name, address, city, state, phone, notes)"\
                        " VALUES (%s,%s,%s,%s,%s,%s)",\
                        (self.name,self.address,self.city,\
                        self.state,self.phone,self.notes))
        connection.commit()

class Contact(object):
    def __init__(self, name=None, company_name=None, phone=None,
                 email=None, notes=None):
        self.name = name
        self.company_name = company_name
        self.phone = phone
        self.email = email
        self.notes = notes

    def write(self):
        cursor.execute("REPLACE INTO contact "\
                       "(company_name, name, phone, email, notes)"\
                       " VALUES (%s,%s,%s,%s,%s)",\
                        (self.company_name,self.name,self.phone,\
                        self.email,self.notes))
        connection.commit()

    def get_by_name(self,name):
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM contact WHERE name=%s",(name))
        record_dict = cursor.fetchall()[0]
        
        if record_dict:
            self.company_name = record_dict['company_name']
            self.name = record_dict['name']
            self.email = record_dict['email']
            self.notes = record_dict['notes']
            self.phone = record_dict['phone']
            return self
        else:
            print 'there was an error'

    def delete_by_name(self, name):
        """ Takes a name string
            Removes the corresponding company entry, if any, from the database
            Returns nothing
            """
        global cursor, connection
        cursor.execute("DELETE FROM contact WHERE name=%s", (name))
        connection.commit()
    
        


class Project(object):
    def __init__(self, 
                 name =None, company_name =None, hourly_pay =None,
                 quoted_hours =None, worked_hours =None, billed_hours =None,
                 total_invoiced =None, total_paid =None, money_owed =None,
                 project_active =None, contact_name =None, contact_phone =None,
                 notes =None):
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
        self.contact_phone = contact_phone
        self.notes = notes



    def write(self):
        cursor.execute("REPLACE INTO project "\
                       "(name, company_name, contact_name, hourly_pay, "\
                       "quoted_hours, worked_hours, billed_hours, "\
                       "total_invoiced, total_paid, money_owed, "\
                       "project_active, notes)"\
                       " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                        (self.name,self.company_name,self.contact_name,
                         self.hourly_pay, self.quoted_hours, self.total_invoiced,
                         self.total_paid, self.money_owed, self.project_active,
                         self.notes))
        connection.commit()

    def getRecordByName(self,name):
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM project WHERE name=%s",(name))
        record_dict = cursor.fetchall()[0]
        
        if recordDict:\
            # to do: fix order
            self.name           = record_dict['name']
            self.company_name   = record_dict['company_name']
            self.hourly_pay     = record_dict['hourly_pay']
            self.quoted_hours   = record_dict['quoted_hours']
            self.worked_hours   = record_dict['worked_hours']
            self.billed_hours   = record_dict['billed_hours']
            self.total_invoiced = record_dict['total_invoiced']
            self.total_paid     = record_dict['total_paid']
            self.money_owed     = record_dict['money_owed']
            self.project_active = record_dict['project_active']
            self.contact_name   = record_dict['contact_name']
            self.notes          = record_dict['notes']
        else:
            print 'there was an error'
            
        cursor = connection.cursor()
        return self

    
class Session(object):
    def __init__(self, 
                 sessionID =None, company_name =None, project_name =None,
                 start_time =None, stop_time =None, time =None, notes =None):
        self.sessionID = sessionID
        self.company_name = company_name
        self.project_name = project_name
        self.start_time = start_time
        self.stop_time = stop_time
        self.time = time
        self.notes = notes

    def write(self):
        cursor.execute("REPLACE INTO session "\
                       "(id, company_name, project_name, start_time,"\
                       "stop_time, time, notes)"\
                       " VALUES (%s,%s,%s,%s,%s,%s,%s)",\
                        (self.sessionID, self.company_name, self.project_name,\
                       self.start_time, self.stop_time, self.time,\
                       self.notes))
        connection.commit()

    def getRecordByName(self,name):
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM session WHERE name=%s",(name))
        recordDict = cursor.fetchall()[0]
        
        if recordDict:
            self.sessionID = recordDict['id']
            self.company_name = recordDict['company_name']
            self.project_name = recordDict['project_name']
            self.start_time = recordDict['start_time']
            self.stop_time = recordDict['stop_time']
            self.time = recordDict['time']
            self.notes = recordDict['notes']

        else:
            print 'there was an error'
        cursor = connection.cursor()

