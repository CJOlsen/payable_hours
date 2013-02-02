# Payable Hours
# Author: Christopher Olsen
#
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

## *** THIS FILE HOLDS THE DISPLAY AND LOGIC CODE, FOR MYSQL INTERFACE SEE 
##     PHdbOperations.py ***


## ******** TODO
## ******** company list box on company tab needs to update



import sys
import PHdbOperations as PHdb
import Tkinter as tk
import ttk

#connect to database
connection,cursor = PHdb.connectDB()

################################################################################
#### LOGIC (the Controller in MVC)
################################################################################

### Clear tab function

def clear_frame(tab_frame):
    fields = tab_frame.winfo_children()
    [field.delete(0,'end') for field in fields\
     if field.winfo_class() == "Entry"]

### Company tab logic-------------------------------------------------------

def company_save(frame):
    """ called when the save button is pressed on the company tab
        """
    company = PHdb.Company()
    company.name = company_name_field.get()
    company.address = company_address_field.get()
    company.city = company_city_field.get()
    company.state = company_state_field.get()
    company.phone = company_phone_field.get()
    company.write()

    clear_frame(frame)

    # need to check to see if this works on empty list box
    company_listbox.delete(0,'end')
    populate_company_listbox()
    update_contact_tab(company_name=company.name, clear=False)

def company_selected(name,frame):
    """ called by the select button on the company tab
        """
    clear_frame(frame)
    company = PHdb.getCompanyByName(name)

    company_name_field.insert(0,company.name)
    if company.address:
        company_address_field.insert(0,company.address)
    if company.city:
        company_city_field.insert(0,company.city)
    if company.state:
        company_state_field.insert(0,company.state)
    if company.phone:
        company_phone_field.insert(0,company.phone)
    if company.notes:
        company_notes_field.insert(0,company.notes)

    update_contact_tab(company_name=company.name, clear=False)

def populate_company_listbox():
    for item in PHdb.getAllCompanies():
        company_listbox.insert('end',item)
    

    
### Contact tab logic-------------------------------------------------------

def contact_selected(name, frame):
    """ called by the select button on the contact tab
        """
    clear_frame(frame)
    #get contact company, update company tab
    contact = PHdb.getContactByName(name)
    contact_company_field.insert(0, contact.companyID)
    contact_name_field.insert(0, contact.name)
    contact_phone_field.insert(0, contact.phone)
    contact_email_field.insert(0, contact.email)
    contact_notes_field.insert(0, contact.notes)

    update_project_tab(contact_name=contact.name, clear=False)

def contact_save():
    # create a new contact object and write it to the db
    contact = PHdb.Contact()
    contact.company_name = contact_company_field.get()
    contact.name = contact_name_field.get()
    contact.phone = contact_phone_field.get()
    contact.email = contact_email_field.get()
    contact.notes = contact_notes_field.get()
    contact.write()

    update_project_tab(contact_name=contact.name, clear=False)

def clear_contact_listbox():
    contact_listbox.delete(0)

def populate_contact_listbox(**kwargs):
    """ Populates the contact tab listbox.
        All calls to this function must supply: a "show_all" key designating
        whether or not the call is to show all contacts, and if that is false
        a "company" key to designate which company contacts to load.
        Returns: Nothing

        """
    clear_contact_listbox()
    if kwargs["show_all"] == True:
        contacts = PHdb.getAllContacts()
        for contact in PHdb.getAllContacts():
            contact_listbox.insert('end', contact)
    else:
        for contact in PHdb.getContactsForCompany(company):
            contact_listbox.insert('end', contact)
        
        
        

def update_contact_tab(**kwargs):
    if kwargs['clear'] == True:
        clear_frame(contactTab)
    elif kwargs['company_name']:
        pass
    elif kwargs['contact_name']:
        # update project lists for company name
        pass
    update_project_tab(clear=True)

def contact_show_all():
    pass
        

### Project tab logic-------------------------------------------------------

def project_selected(name):
    #update company and contact tabs
    project = PHdb.getProjectByName(name)
    project_name_field.insert(0, project.name)
    project_hourlyPay_field.insert(0, project.hourlyPay)
    project_workedHours_field.insert(0, project.workedHours)
    project_billedHours_field.insert(0, project.billedHours)
    project_totalInvoiced_field.insert(0, project.totalInvoiced)
    project_totalPaid_field.insert(0, project.totalPaid)
    project_moneyOwed_field.insert(0, project.moneyOwed)
    project_projectActive_field(0, project.projectActive)
    project_contactName_field(0, project.contactName)
    project_contactPhone_field(0, project.contactPhone)

    update_session_tab(project_name=project.name, clear=False)
    
def save_project():
    project = PHdb.Project()
    project.name = project_name_field.get()
    project.hourlyPay = project_hourlyPay_field.get()
    project.workedHours = project_workedHours_field.get()
    project.billedHours = project_billedHours_field.get()
    project.totalInvoiced = project_totalInvoiced_field.get()
    project.totalPaid = project_totalPaid_field.get()
    project.moneyOwed = project_moneyOwed_field.get()
    project.projectActive = project_projectActive_field.get()
    project.contactName = project_contactName_field.get()
    project.contactPhone = project_contactPhone_field.get()
    project.write()

    update_session_tab(project_name=project.name, clear=False)

def update_project_tab(**kwargs):
    pass


### Session tab logic-------------------------------------------------------

def session_selected(datetime):
    session = PHdb.getSessionBySessionID(sessionID)
    session_sessionID_field.insert(0, session.sessionID)
    session_companyID_field.insert(0, session.companyID)
    session_projectID_field.insert(0, session.projectID)
    session_startTime_field.insert(0, session.startTime)
    session_stopTime_field.insert(0, session.stopTime)
    session_time_field.insert(0, session.time)
    session_notes_field.insert(0, session.notes)


def save_session():
    session = PHdb.Session()
    session.sessionID = session_sessionID_field.get()
    session.companyID = session_companyID_field.get()
    session.projectID = session_projectID_field.get()
    session.startTime = session_startTime_field.get()
    session.stopTime = session_stopTime_field.get()
    session.time = session_time_field.get()
    session.notes = session_notes_field.get()
    session.write()

def new_session():
    pass

def update_session_tab(**kwaargs):
    pass



################################################################################
#### BUILD THE DISPLAY (the V in MVC)
################################################################################


#create main window 
root = tk.Tk()
root.title("Payable Horse")
root.geometry("600x600+100+50")

#create notebook
nbook = ttk.Notebook(root)
nbook.grid(row=0,column=0)

#make tabs and add them
companyTab = tk.Frame()
contactTab = tk.Frame()
projectTab = tk.Frame()
sessionTab = tk.Frame()
mysqlTab   = tk.Frame()

nbook.add(companyTab,text='Company')
nbook.add(contactTab,text='Contact')
nbook.add(projectTab,text='Project')
nbook.add(sessionTab,text='Session')
nbook.add(mysqlTab,text='MySQL')


#### company page content------------------------------------------------------
  ## set up the fields and labels
company_name_field    = tk.Entry(companyTab,width=25)
company_address_field = tk.Entry(companyTab,width=25)
company_city_field    = tk.Entry(companyTab,width=25)
company_state_field   = tk.Entry(companyTab,width=5)
company_phone_field   = tk.Entry(companyTab,width=25)
company_notes_field   = tk.Entry(companyTab,width=25)

company_name_label    = tk.Label(companyTab,text="Name")
company_address_label = tk.Label(companyTab,text="Address")
company_city_label    = tk.Label(companyTab,text="City")
company_state_label   = tk.Label(companyTab,text="State")
company_phone_label   = tk.Label(companyTab,text="Phone")
company_notes_label   = tk.Label(companyTab,text="Notes")

company_listbox = tk.Listbox(companyTab)

# create a button to select from the listbox
# this needs a lambda function because it stores the result of the command
company_listbox_button = tk.Button(companyTab, text="Select",
                                   command = lambda: company_selected(
                                       company_listbox.get(
                                           company_listbox.curselection()[0])
                                           ,companyTab))

company_save_button = tk.Button(companyTab,text='Save',
                                command = lambda: company_save(companyTab))

company_clear_button = tk.Button(companyTab,text='Clear',
                                 command = lambda: \
                                 [field.delete(0,'end') for field in\
                                  companyTab.winfo_children() \
                                  if field.winfo_class() == 'Entry'])


#### contact page content -----------------------------------------------------

contact_name_field  = tk.Entry(contactTab,width=20)
contact_company_field = tk.Entry(contactTab,width=20)
contact_phone_field = tk.Entry(contactTab,width=20)
contact_email_field = tk.Entry(contactTab,width=20)
contact_notes_field = tk.Entry(contactTab,width=20)

contact_name_label  = tk.Label(contactTab,text="Name")
contact_company_label = tk.Label(contactTab,text="Company")
contact_phone_label = tk.Label(contactTab,text="Phone")
contact_email_label = tk.Label(contactTab,text="Email")
contact_notes_label = tk.Label(contactTab,text="Notes")

# contact list box
contact_listbox = tk.Listbox(contactTab)


for item in PHdb.getAllContacts():
    contact_listbox.insert('end',item)



# this needs a lambda function because it stores the result of the command
contact_listbox_button = tk.Button(contactTab, text="Select",
                                   command = lambda: contact_selected(
                                       contact_listbox.get(
                                           contact_listbox.curselection()[0])
                                           ,contactTab))

contact_show_all_button = tk.Button(contactTab, text='Show All',
                                   command = lambda: contact_show_all())

contact_save_button = tk.Button(contactTab,text='Save',
                                command = lambda: contact_save())

contact_clear_button = tk.Button(contactTab,text='Clear',
                                 command = lambda: \
                                 [field.delete(0,'end') for field in\
                                  contactTab.winfo_children() \
                                  if field.winfo_class() == 'Entry'])



#### project page content -----------------------------------------------------

project_hourlyPay_field     = tk.Entry(projectTab,width=25)
project_quotedHours_field   = tk.Entry(projectTab,width=25)
project_workedHours_field   = tk.Entry(projectTab,width=25)
project_billedHours_field   = tk.Entry(projectTab,width=25)
project_totalInvoiced_field = tk.Entry(projectTab,width=25)
project_totalPaid_field     = tk.Entry(projectTab,width=25)
project_moneyOwed_field     = tk.Entry(projectTab,width=25)
project_projectActive_field = tk.Entry(projectTab,width=5)
project_contactName_field   = tk.Entry(projectTab,width=25)
project_contactPhone_field  = tk.Entry(projectTab,width=25)
#project_notes_field         = tk.Entry(projectTab,width=200)\
#                              .grid(row=11,column=1)

project_hourlyPay_label     = tk.Label(projectTab,text="Hourly Pay")
project_quotedHours_label   = tk.Label(projectTab,text="Quoted Hours")
project_workedHours_label   = tk.Label(projectTab,text="Worked Hours")
project_billedHours_label   = tk.Label(projectTab,text="Billed Hours")
project_totalInvoiced_label = tk.Label(projectTab,text="Total Invoiced")
project_totalPaid_label     = tk.Label(projectTab,text="Total Paid")
project_moneyOwed_label     = tk.Label(projectTab,text="Money Owed")
project_projectActive_label = tk.Label(projectTab,text="Project Active")
project_contactName_label   = tk.Label(projectTab,text="Contact Name")
project_contactPhone_label  = tk.Label(projectTab,text="Contact Phone")
project_notes_label         = tk.Label(projectTab,text="Notes Label")

#company list box

#contact list box
 ## create the listboxes
project_company_listbox = tk.Listbox(projectTab)
project_contact_listbox = tk.Listbox(projectTab)

for item in PHdb.getAllCompanies():
    project_company_listbox.insert('end',item)

def update_project_company_listbox(name):
    for item in PHdb.getContactsForCompany(name):
        project_contact_listbox.insert('end',item)

        
    ## create a button to select from the company listbox
    ## ...



                              
#### session page content -----------------------------------------------------

session_startTime_field    = tk.Entry(sessionTab,width=15)
session_stopTime_field     = tk.Entry(sessionTab,width=15)
session_time_field         = tk.Entry(sessionTab,width=15)
#session_notes_field        = tk.Entry(sessionTab,width=200).grid(row=3,column=1)

session_startTime_label    = tk.Label(sessionTab,text="Start time")
session_stopTime_label     = tk.Label(sessionTab,text="Stop time")
session_time_label         = tk.Label(sessionTab,text="Time")
session_notes_label        = tk.Label(sessionTab,text="Notes")

#company list box

#contact list box

#project list box



#### MySQL prompt
# just a window to pull up a sql command line prompt
# not sure if this is even possible.....



################################################################################
#### DISPLAY THE DISPLAY
################################################################################


  ## display the company widgets
company_name_field.grid(row=0,column=1)
company_address_field.grid(row=1,column=1)
company_city_field.grid(row=2,column=1)
company_state_field.grid(row=3,column=1,sticky='w')
company_phone_field.grid(row=4,column=1)
company_notes_field.grid(row=5,column=1,rowspan=4)

company_name_label.grid(row=0,column=0)
company_address_label.grid(row=1,column=0)
company_city_label.grid(row=2,column=0)
company_state_label.grid(row=3,column=0)
company_phone_label.grid(row=4,column=0)
company_notes_label.grid(row=5,column=0)

company_listbox.grid(column=4,row=0,rowspan=5)
company_listbox_button.grid(row=5,column=4)
company_save_button.grid(row=10,column=1)
company_clear_button.grid(row=10,column=2)

populate_company_listbox()

  ## display the contact widgets
contact_name_field.grid(row=0,column=1)
contact_company_field.grid(row=1,column=1)
contact_phone_field.grid(row=2,column=1)
contact_email_field.grid(row=3,column=1)
contact_notes_field.grid(row=4,column=1)

contact_name_label.grid(row=0,column=0)
contact_company_label.grid(row=1, column=0)
contact_phone_label.grid(row=2,column=0)
contact_email_label.grid(row=3,column=0)
contact_notes_label.grid(row=4,column=0)

contact_listbox.grid(column=4,row=0,rowspan=5)
contact_listbox_button.grid(row=5,column=4)
contact_show_all_button.grid(row=6, column=4)
contact_save_button.grid(row=5,column=1)
contact_clear_button.grid(row=6,column=1)

populate_contact_listbox(show_all=True)

  ## display the project widgets
project_hourlyPay_field.grid(row=0,column=1)
project_quotedHours_field.grid(row=2,column=1)
project_workedHours_field.grid(row=3,column=1)
project_billedHours_field.grid(row=4,column=1)
project_totalInvoiced_field.grid(row=5,column=1)
project_totalPaid_field.grid(row=6,column=1)
project_moneyOwed_field.grid(row=7,column=1)
project_projectActive_field.grid(row=8,column=1)
project_contactName_field.grid(row=9,column=1)
project_contactPhone_field.grid(row=10,column=1)

project_hourlyPay_label.grid(row=0,column=0)
project_quotedHours_label.grid(row=2,column=0)
project_workedHours_label.grid(row=3,column=0)
project_billedHours_label.grid(row=4,column=0)
project_totalInvoiced_label.grid(row=5,column=0)
project_totalPaid_label.grid(row=6,column=0)
project_moneyOwed_label.grid(row=7,column=0)
project_projectActive_label.grid(row=8,column=0)
project_contactName_label.grid(row=9,column=0)
project_contactPhone_label.grid(row=10,column=0)
project_notes_label.grid(row=11,column=0)

  ## display the session widgets
session_startTime_field.grid(row=0,column=1)
session_stopTime_field.grid(row=1,column=1)
session_time_field.grid(row=2,column=1)

session_startTime_label.grid(row=0,column=0)
session_stopTime_label.grid(row=1,column=0)
session_time_label.grid(row=2,column=0)
session_notes_label.grid(row=3,column=0)


## 
## This line is so necessary.  Don't remove it.
##
root.mainloop()



"""
    WHAT WILL THE GUI NEED?
        -five tabs:
            -Company
                - show all data
                - select company dropdown
                - save changes button
            -Contact
                - show all data
                - select contact dropdown
                - save changes button
            -Project
                - show all data
                - select project
                - save changes button
                - start/stop project session
            -Session
                - session search feature
                - show all data
                - save changes button
                - start/stop button
                - combine sessions
            -MySQL prompt
                - Open a window with a MySQL command line interface
"""

    





