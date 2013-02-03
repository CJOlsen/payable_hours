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


def getAllCompanies():
    """ Takes: nothing
        Selects all names from the company table
        Returns: all company names
        """
    cursor.execute("SELECT name FROM company")
    return [x[0] for x in cursor.fetchall()]
    
def getCompanyByName(name):
    """ Takes: a name string
        Returns: a company object corresponding to the name
        """
    company = Company()
    return company.getByName(name)

def deleteCompanyByName(name):
    """ Takes: a name string
        Deletes the corresponding company from the database
        Returns: nothing
        """
    company=Company()
    company.deleteByName(name)

def getContactByName(name):
    """ Takes: a name string
        Returns: a contact object corresponding to the name
        """
    contact = Contact()
    return contact.getByName(name)

def deleteContactByName(name):
    """ Takes: a name string
        Deletes the corresponding contact from the database
        Returns: nothing
        """
    contact=Contact()
    contact.deleteByName(name)
    

def getAllProjects():
    """ Takes: nothing
        Returns: all names from the project table
        """
    cursor.execute("SELECT name FROM project")
    return cursor.fetchall()

def getActiveProjects():
    """ Takes: nothing
        Returns: all names from the project table if the project is active
        """
    cursor.execute("SELECT name FROM project WHERE projectActive = True")
    return cursor.fetchall()

def getAllContacts():
    """ Takes: nothing
        Returns: all names from the contact table
        """
    cursor.execute("SELECT name FROM contact")
    return cursor.fetchall()

def getContactsForCompany(name):
    # to do
    pass

def getContactByID():
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
    def getByName(self,name):
        """ Takes: a name string
            Queries the database for the company corresponding to the name
            string, and maps attributes ot local variables.
            Returns: self
            """
        global cursor
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM company WHERE name=%s",(name))
        recordDict = cursor.fetchall()[0]
        
        if recordDict:
            self.name      = recordDict['name']
            self.address   = recordDict['address']
            self.city      = recordDict['city']
            self.state     = recordDict['state']
            self.phone     = recordDict['phone']
            self.notes     = recordDict['notes']
        else:
            print 'there was an error'
            
        cursor = connection.cursor()
        return self

    def deleteByName(self, name):
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

    def getByName(self,name):
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM contact WHERE name=%s",(name))
        recordDict = cursor.fetchall()[0]
        
        if recordDict:
            self.company_name = recordDict['company_name']
            self.name = recordDict['name']
            self.email = recordDict['email']
            self.notes = recordDict['notes']
            self.phone = recordDict['phone']
            return self
        else:
            print 'there was an error'

    def deleteByName(self, name):
        """ Takes a name string
            Removes the corresponding company entry, if any, from the database
            Returns nothing
            """
        global cursor, connection
        cursor.execute("DELETE FROM contact WHERE name=%s", (name))
        connection.commit()
    
        


class Project(object):
    def __init__(self, 
                 name          =None,
                 companyTab    =None,
                 hourlyPay     =None,
                 quotedHours   =None,
                 workedHours   =None,
                 billedHours   =None,
                 totalInvoiced =None,
                 totalPaid     =None,
                 moneyOwed     =None,
                 projectActive =None,
                 contactName   =None,
                 contactPhone  =None,
                 notes         =None):
        self.name          = name
        self.companyID     = companyID
        self.hourlyPay     = hourlyPay
        self.quotedHours   = quotedHours
        self.workedHours   = workedHours
        self.billedHours   = billedHours
        self.totalInvoiced = totalInvoiced
        self.totalPaid     = totalPaid
        self.moneyOwed     = moneyOwed
        self.projectActive = projectActive
        self.contactName   = contactName
        self.contactPhone  = contactPhone
        self.notes         = notes
            
    def write():
        # query to write to DB
        if self.companyID:
            # companyID should only be assigned by MySQl, so if an object
            # has one, it already exists and needs to be overwritten
            # REPLACE will overwrite or add new, INSERT adds new only
            cursor.execute("REPLACE INTO project\
                           (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                           (self.name,self.companyID,self.hourlyPay,\
                            self.quotedHours,self.workedHours,self.billedHours,\
                            self.totalInvoiced,self.totalPaid,self.moneyOwed,\
                            self.projectActive,self.contactName,\
                            self.contactPhone,self.notes))
        else:
            cursor.execute("INSERT INTO project\
                           (name, address, city, state, phone, notes)\
                           (%s,%s,%s,%s,%s,%s)",\
                           (self.name,self.address,self.city,self.state,\
                            self.phone,self.notes))

        # nothing is final until committed    
        connection.commit()


    def getRecordByName(self,name):
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM project WHERE name=%s",(name))
        recordDict = cursor.fetchall()[0]
        
        if recordDict:
            self.name          = recordDict['name']
            self.companyID     = recordDict['companyID']
            self.hourlyPay     = recordDict['hourlyPay']
            self.quotedHours   = recordDict['quotedHours']
            self.workedHours   = recordDict['workedHours']
            self.billedHours   = recordDict['billedHours']
            self.totalInvoiced = recordDict['totalInvoiced']
            self.totalPaid     = recordDict['totalPaid']
            self.moneyOwed     = recordDict['moneyOwed']
            self.projectActive = recordDict['projectActive']
            self.contactName   = recordDict['contactName']
            self.contactPhone  = recordDict['contactPhone']
            self.notes         = recordDict['notes']
        else:
            print 'there was an error'
            
        cursor = connection.cursor()
        return self

    
class Session(object):
    def __init__(self, 
                 sessionid =None,
                 companyID =None,
                 projectID =None,
                 startTime =None,
                 stopTime  =None,
                 time      =None,
                 notes     =None):
        self.sessionID = sessionID
        self.companyID = companyID
        self.projectID = projectID
        self.startTime = startTime
        self.stopTime  = stopTime
        self.time      = time
        self.notes     = notes


    def write():
        # query to write to DB
        if self.sessionid:
            #sessionID should only be assigned by MySQl, so if an object
            #has one, it already exists and needs to be overwritten
            cursor.execute("REPLACE INTO session\
                           (%s,%s,%s,%s,%s,%s,%s)",\
                           (self.sessionID,self.companyID,self.projectID,\
                            self.startTime,self.stopTime,self.time,self.notes))
        else:
            cursor.execute("INSERT INTO session\
                           (companyID, projectID, startTime, stopTime,\
                           time,notes)(%s,%s,%s,%s,%s,%s)",\
                           (self.companyID,self.projectID,\
                            self.startTime,self.stopTime,self.time,self.notes))
            
        connection.commit()

    def getRecordByName(self,name):
        cursor = connection.cursor(mdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM session WHERE name=%s",(name))
        recordDict = cursor.fetchall()[0]
        
        if recordDict:
            self.name      = recordDict['name']
            self.sessionID = recordDict['sessionID']
            self.companyID = recordDict['companyID']
            self.projectID = recordDict['projectID']
            self.startTime = recordDict['startTime']
            self.stopTime  = recordDict['stopTime']
            self.time      = recordDict['time']
            self.notes     = recordDict['notes']

        else:
            print 'there was an error'
        cursor = connection.cursor()

