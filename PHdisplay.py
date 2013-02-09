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

import sys
import PHdbOperations as PHdb
import Tkinter as tk
import ttk

#connect to database
connection,cursor = PHdb.connectDB()

###############################################################################
#### LOGIC (the Controller in MVC)
###############################################################################

### Clear tab function

def clear_frame(tab_frame):
    """ Clears the fields of any given tab

        """
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
    company = PHdb.Company.get_by_name(name)

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

def company_delete_selected(name, frame):
    """ called by the 'delete' button on the company tab
        """
    # needs an 'are you sure' prompt
    PHdb.Company.delete_by_name(name)
    company_listbox.delete(0, 'end')
    populate_company_listbox()
    

def populate_company_listbox():
    for item in PHdb.Company.get_all_companies():
        company_listbox.insert('end',item)
    

    
### Contact tab logic-------------------------------------------------------

def contact_selected(name, frame):
    """ called by the select button on the contact tab
        """
    clear_frame(frame)
    #get contact company, update company tab
    contact = PHdb.Contact.get_by_name(name)
    contact_company_field.insert(0, contact.company_name)
    contact_name_field.insert(0, contact.name)
    contact_phone_field.insert(0, contact.phone)
    contact_email_field.insert(0, contact.email)
    contact_notes_field.insert(0, contact.notes)

    update_project_tab(contact_name=contact.name, clear=False)

def contact_save():
    """ called by the save button on the contact tab
        """
    # create a new contact object and write it to the db
    contact = PHdb.Contact()
    contact.company_name = contact_company_field.get()
    contact.name = contact_name_field.get()
    contact.phone = contact_phone_field.get()
    contact.email = contact_email_field.get()
    contact.notes = contact_notes_field.get()
    contact.write()

    populate_contact_listbox(show_all=True)
    update_project_tab(contact_name=contact.name, clear=False)


    

def contact_delete_selected(name, frame):
    """ called by the 'delete' button on the company tab
        """
    # needs an 'are you sure' prompt
    PHdb.Contact.delete_by_name(name)
    contact_listbox.delete(0, 'end')
    populate_contact_listbox(show_all=True)


def clear_contact_listbox():
    contact_listbox.delete(0, 'end')

def populate_contact_listbox(**kwargs):
    """ Populates the contact tab listbox.
        All calls to this function must supply: a "show_all" key designating
        whether or not the call is to show all contacts, and if that is false
        a "company" key to designate which company contacts to load.
        Returns: Nothing

        """
    clear_contact_listbox()
    if kwargs['show_all'] == True:
        for contact in PHdb.Contact.get_all_contacts():
            # the [0] after contact removes curly braces
            contact_listbox.insert('end', contact[0])
    else:
        for contact in PHdb.Contact.get_contacts_for_company(company):
            contact_listbox.insert('end', contact[0])
        
        
        

def update_contact_tab(**kwargs):
    if kwargs['clear'] == True:
        clear_frame(contact_tab)
    elif kwargs['company_name']:
        pass
    elif kwargs['contact_name']:
        # update project lists for company name
        pass
    update_project_tab(clear=True)

def contact_show_all():
    pass
        

### Project tab logic-------------------------------------------------------

def project_selected(name, frame):

    clear_frame(frame)
    #update company and contact tabs
    project = PHdb.Project.get_by_name(name)
    project_name_field.insert(0, project.name)
    project_hourlyPay_field.insert(0, project.hourly_pay)
    project_quotedHours_field.insert(0, project.quoted_hours)
    project_workedHours_field.insert(0, project.worked_hours)
    project_billedHours_field.insert(0, project.billed_hours)
    project_totalInvoiced_field.insert(0, project.total_invoiced)
    project_totalPaid_field.insert(0, project.total_paid)
    project_moneyOwed_field.insert(0, project.money_owed)
    project_projectActive_field.insert(0, project.project_active)
    project_contactName_field.insert(0, project.contact_name)
    project_companyName_field.insert(0, project.company_name)
    project_notes_field.insert(0, project.notes)

    update_session_tab(project_name=project.name, clear=False)
    
def project_save():
    project = PHdb.Project()
    project.name = project_name_field.get()
    project.hourly_pay = project_hourlyPay_field.get()
    project.quoted_hours = project_quotedHours_field.get()
    project.worked_hours = project_workedHours_field.get()
    project.billed_hours = project_billedHours_field.get()
    project.total_invoiced = project_totalInvoiced_field.get()
    project.total_paid = project_totalPaid_field.get()
    project.money_owed = project_moneyOwed_field.get()
    project.project_active = project_projectActive_field.get()
    project.contact_name = project_contactName_field.get()
    project.company_name = project_companyName_field.get()
    project.notes = project_notes_field.get()
    
    project.write()

    update_session_tab(project_name=project.name, clear=False)

def update_project_tab(**kwargs):
    pass


def project_delete_selected(name, frame):
    """ called by the 'delete' button on the company tab
        """
    # needs an 'are you sure' prompt
    PHdb.Project.delete_by_name(name)
    project_listbox.delete(0, 'end')
    populate_project_listbox(show_all=True)


def clear_project_listbox():
    project_listbox.delete(0, 'end')

def populate_project_listbox(**kwargs):
    """ Populates the project tab listbox.
        All calls to this function must supply: a "show_all" key designating
        whether or not the call is to show all projects, and if that is false
        a "company" key to designate which company contacts to load. ???
        Returns: Nothing

        """
    clear_project_listbox()
    if kwargs['show_all'] == True:
        for project in PHdb.Project.get_all_projects():
            # project[0] removes curly braces
            project_listbox.insert('end', project[0])
    else:
        for project in PHdb.Contact.get_contacts_for_company(company):
            project_listbox.insert('end', project[0])


### Session tab logic-------------------------------------------------------

def session_selected(datetime):
    session = PHdb.Session.get_session_by_sessionID(sessionID)
    session_sessionID_field.insert(0, session.sessionID)
    session_companyName_field.insert(0, session.company_name)
    session_projectName_field.insert(0, session.project_name)
    session_startTime_field.insert(0, session.start_time)
    session_stopTime_field.insert(0, session.stop_time)
    session_time_field.insert(0, session.time)
    session_notes_field.insert(0, session.notes)
    session_gitCommit_field.insert(0, session.git_commit)


def save_session():
    session = PHdb.Session()
    
    session.companyID = session_companyName_field.get()
    session.projectID = session_projectName_field.get()
    session.startTime = session_startTime_field.get()
    session.stopTime = session_stopTime_field.get()
    session.time = session_time_field.get()
    session.notes = session_notes_field.get()
    session.gitCommit = session_gitCommit_field.get()

    try:
        session.sessionID = session_sessionID_field.get()
        if len(session.sessionID) < 1:
            raise Exception
    except:
        PHdb.session.get_session_number
        session.sessionID = PHdb.session.make_sessionID(session)
    session.write()

def new_session():
    pass

def update_session_tab(**kwaargs):
    pass

## need: session save, session clear, session listbox, delete from listbox,
##       select from listbox, project listbox, select project from listbox,
##       start session, stop session!!!

## session_session_listbox
## session_project_listbox


# session tab session listbox
def session_session_delete_selected(name, frame):
    """ called by the 'delete' button on the session tab
        """
    # needs an 'are you sure' prompt
    PHdb.Session.delete_by_name(name)
    session_session_listbox.delete(0, 'end')
    populate_session_session_listbox(show_all=True)


def clear_session_session_listbox():
    session_session_listbox.delete(0, 'end')

def populate_session_session_listbox(**kwargs):
    """ Populates the session tab's sesssion listbox.
        All calls to this function must supply: a "show_all" key designating
        whether or not the call is to show all contacts, and if that is false
        a "project" key to designate which sessions to load.
        Returns: Nothing

        """
    clear_contact_listbox()
    if kwargs['show_all'] == True:
        for session in PHdb.Session.get_all_sessions():
            # the [0] after contact removes curly braces
            contact_listbox.insert('end', contact[0])
    else:
        for session in PHdb.Session.get_sessions_for_project(project):
            session_session_listbox.insert('end', session[0])


# session tab project listbox
# projects can only be selected on the session tab
def clear_session_session_listbox():
    session_project_listbox.delete(0, 'end')

def populate_session_session_listbox(**kwargs):
    """ Populates the session tab's sesssion listbox.
        All calls to this function must supply: a "show_all" key designating
        whether or not the call is to show all contacts, and if that is false
        a "project" key to designate which sessions to load.
        Returns: Nothing

        """
    clear_contact_listbox()
    if kwargs['show_all'] == True:
        for session in PHdb.Session.get_all_sessions():
            # the [0] after contact removes curly braces
            contact_listbox.insert('end', contact[0])
    else:
        for session in PHdb.Session.get_sessions_for_project(project):
            session_session_listbox.insert('end', session[0])

def session_project_selected(name, frame):
    """ Called by the 'Select' button for the project listbox on the session
        tab.

        """
    print "session_project_selected()"

def session_session_selected(name, frame):
    """ Called by the "Select' button for the session listbox on the session
        tab.

        """
    print "session_session_selected()"

def session_session_deleted(name, frame):
    """ Called by the "Delete' button for the session listbox on the session
        tab.

        """
    print "session_session_deleted()"

def session_session_show_all(frame):
    """ Called by the "Show All" button for the session listbox on the session
        tab.

        """
    print "session_session_show_all()"

def session_session_save(frame):
    """ Called by the "Save" button for the session listbox on the session
        tab.

        """
    print "session_session_save()"




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
company_tab = tk.Frame()
contact_tab = tk.Frame()
project_tab = tk.Frame()
session_tab = tk.Frame()
mysql_tab   = tk.Frame()

nbook.add(company_tab,text='Company')
nbook.add(contact_tab,text='Contact')
nbook.add(project_tab,text='Project')
nbook.add(session_tab,text='Session')
nbook.add(mysql_tab,text='MySQL')


#### company page content------------------------------------------------------
  ## set up the fields and labels
company_name_field    = tk.Entry(company_tab,width=25)
company_address_field = tk.Entry(company_tab,width=25)
company_city_field    = tk.Entry(company_tab,width=25)
company_state_field   = tk.Entry(company_tab,width=5)
company_phone_field   = tk.Entry(company_tab,width=25)
company_notes_field   = tk.Entry(company_tab,width=25)

company_name_label    = tk.Label(company_tab,text="Name")
company_address_label = tk.Label(company_tab,text="Address")
company_city_label    = tk.Label(company_tab,text="City")
company_state_label   = tk.Label(company_tab,text="State")
company_phone_label   = tk.Label(company_tab,text="Phone")
company_notes_label   = tk.Label(company_tab,text="Notes")

company_listbox = tk.Listbox(company_tab)

# create a button to select from the listbox
# this needs a lambda function because it stores the result of the command
company_listbox_button = tk.Button(company_tab, text="Select",
                                   command = lambda: company_selected(
                                       company_listbox.get(
                                           company_listbox.curselection()[0])
                                           ,company_tab))

company_delete_selected_button = tk.Button(
    company_tab, text="Delete", command = lambda: company_delete_selected(
        company_listbox.get(company_listbox.curselection()[0])
        ,company_tab))

company_save_button = tk.Button(company_tab,text='Save',
                                command = lambda: company_save(company_tab))

company_clear_button = tk.Button(company_tab,text='Clear',
                                 command = lambda: \
                                 [field.delete(0,'end') for field in\
                                  company_tab.winfo_children() \
                                  if field.winfo_class() == 'Entry'])


#### contact page content -----------------------------------------------------

contact_name_field  = tk.Entry(contact_tab,width=20)
contact_company_field = tk.Entry(contact_tab,width=20)
contact_phone_field = tk.Entry(contact_tab,width=20)
contact_email_field = tk.Entry(contact_tab,width=20)
contact_notes_field = tk.Entry(contact_tab,width=20)

contact_name_label  = tk.Label(contact_tab,text="Name")
contact_company_label = tk.Label(contact_tab,text="Company")
contact_phone_label = tk.Label(contact_tab,text="Phone")
contact_email_label = tk.Label(contact_tab,text="Email")
contact_notes_label = tk.Label(contact_tab,text="Notes")

# contact list box
contact_listbox = tk.Listbox(contact_tab)


for item in PHdb.Contact.get_all_contacts():
    contact_listbox.insert('end',item)



# this needs a lambda function because it stores the result of the command
contact_listbox_button = tk.Button(contact_tab, text="Select",
                                   command = lambda: contact_selected(
                                       contact_listbox.get(
                                           contact_listbox.curselection()[0])
                                           ,contact_tab))


contact_delete_selected_button = tk.Button(
    contact_tab, text="Delete", command = lambda: contact_delete_selected(
        contact_listbox.get(contact_listbox.curselection()[0])
        ,contact_tab))


contact_show_all_button = tk.Button(contact_tab, text='Show All',
                                   command = lambda: contact_show_all())

contact_save_button = tk.Button(contact_tab,text='Save',
                                command = lambda: contact_save())

contact_clear_button = tk.Button(contact_tab,text='Clear',
                                 command = lambda: \
                                 [field.delete(0,'end') for field in\
                                  contact_tab.winfo_children() \
                                  if field.winfo_class() == 'Entry'])



#### project page content -----------------------------------------------------

project_name_field          = tk.Entry(project_tab,width=25)
project_hourlyPay_field     = tk.Entry(project_tab,width=25)
project_quotedHours_field   = tk.Entry(project_tab,width=25)
project_workedHours_field   = tk.Entry(project_tab,width=25)
project_billedHours_field   = tk.Entry(project_tab,width=25)
project_totalInvoiced_field = tk.Entry(project_tab,width=25)
project_totalPaid_field     = tk.Entry(project_tab,width=25)
project_moneyOwed_field     = tk.Entry(project_tab,width=25)
project_projectActive_field = tk.Entry(project_tab,width=5)
project_contactName_field   = tk.Entry(project_tab,width=25)
project_companyName_field   = tk.Entry(project_tab,width=25)
project_notes_field         = tk.Entry(project_tab,width=25)

project_name_label          = tk.Label(project_tab,text="Project Name")
project_hourlyPay_label     = tk.Label(project_tab,text="Hourly Pay")
project_quotedHours_label   = tk.Label(project_tab,text="Quoted Hours")
project_workedHours_label   = tk.Label(project_tab,text="Worked Hours")
project_billedHours_label   = tk.Label(project_tab,text="Billed Hours")
project_totalInvoiced_label = tk.Label(project_tab,text="Total Invoiced")
project_totalPaid_label     = tk.Label(project_tab,text="Total Paid")
project_moneyOwed_label     = tk.Label(project_tab,text="Money Owed")
project_projectActive_label = tk.Label(project_tab,text="Project Active")
project_contactName_label   = tk.Label(project_tab,text="Contact Name")
project_companyName_label   = tk.Label(project_tab,text="Company Name")
project_notes_label         = tk.Label(project_tab,text="Notes")


# contact list box
project_listbox = tk.Listbox(project_tab)


for item in PHdb.Project.get_all_projects():
    project_listbox.insert('end',item)



# this needs a lambda function because it stores the result of the command
project_listbox_button = tk.Button(project_tab, text="Select",
                                   command = lambda: project_selected(
                                       project_listbox.get(
                                           project_listbox.curselection()[0])
                                           ,project_tab))


project_delete_selected_button = tk.Button(
    project_tab, text="Delete", command = lambda: project_delete_selected(
        project_listbox.get(project_listbox.curselection()[0])
        ,project_tab))


project_show_all_button = tk.Button(project_tab, text='Show All',
                                   command = lambda: project_show_all())

project_save_button = tk.Button(project_tab,text='Save',
                                command = lambda: project_save())

project_clear_button = tk.Button(project_tab,text='Clear',
                                 command = lambda: \
                                 [field.delete(0,'end') for field in\
                                  project_tab.winfo_children() \
                                  if field.winfo_class() == 'Entry'])

                              
#### session page content -----------------------------------------------------

session_startTime_field = tk.Entry(session_tab,width=15)
session_stopTime_field = tk.Entry(session_tab,width=15)
session_time_field = tk.Entry(session_tab,width=15)
session_notes_field = tk.Entry(session_tab,width=15)
session_companyName_field = tk.Entry(session_tab,width=15)
session_projectName_field = tk.Entry(session_tab,width=15)
session_gitCommit_field = tk.Entry(session_tab,width=15)

session_startTime_label    = tk.Label(session_tab,text="Start time")
session_stopTime_label     = tk.Label(session_tab,text="Stop time")
session_time_label         = tk.Label(session_tab,text="Time")
session_notes_label        = tk.Label(session_tab,text="Notes")
session_companyName_label = tk.Label(session_tab,text="Company Name")
session_projectName_label = tk.Label(session_tab,text="Project Name")
session_gitCommit_label = tk.Label(session_tab,text="Git Commit")

# session tab project list box
session_project_listbox = tk.Listbox(session_tab)
session_project_listbox_label = tk.Label(session_tab, text="Project:")

# create a button to select from the listbox
# this needs a lambda function because it stores the result of the command
session_project_listbox_button = tk.Button(session_tab, text="Select",
                                   command = lambda: session_project_selected(
                                       session_project_listbox.get(
                                           session_project_listbox.curselection()[0])
                                           ,session_tab))
# populate the session tab project listbox
for item in PHdb.Project.get_all_projects():
    session_project_listbox.insert('end',item[0])


# session tab session list box
session_session_listbox_label = tk.Label(session_tab, text="Session:")
session_session_listbox = tk.Listbox(session_tab)

# this needs a lambda function because it stores the result of the command
session_session_listbox_button = tk.Button(session_tab, text="Select",
                                   command = lambda: session_session_selected(
                                       session_session_listbox.get(
                                           session_session_listbox.curselection()[0])
                                           ,session_tab))


session_session_delete_selected_button = tk.Button(
    session_tab, text="Delete",
    command = lambda: session_session_delete_selected(
        session_session_listbox.get(session_session_listbox.curselection()[0])
        ,session_tab))


session_session_show_all_button = tk.Button(session_tab, text='Show All',
                                   command = lambda: session_session_show_all())

session_session_save_button = tk.Button(contact_tab,text='Save',
                                command = lambda: session_session_save())

##session_session_clear_button = tk.Button(session_tab,text='Clear',
##                                 command = lambda: \
##                                 [field.delete(0,'end') for field in\
##                                  contact_tab.winfo_children() \
##                                  if field.winfo_class() == 'Entry'])





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
company_listbox_button.grid(row=6,column=4)
company_delete_selected_button.grid(row=7,column=4)
company_save_button.grid(row=7,column=1)
company_clear_button.grid(row=7,column=2)

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
contact_delete_selected_button.grid(row=6, column=4)
contact_show_all_button.grid(row=7, column=4)
contact_save_button.grid(row=5,column=1)
contact_clear_button.grid(row=6,column=1)

populate_contact_listbox(show_all=True)

  ## display the project widgets
project_name_field.grid(row=0,column=1)
project_hourlyPay_field.grid(row=1,column=1)
project_quotedHours_field.grid(row=2,column=1)
project_workedHours_field.grid(row=3,column=1)
project_billedHours_field.grid(row=4,column=1)
project_totalInvoiced_field.grid(row=5,column=1)
project_totalPaid_field.grid(row=6,column=1)
project_moneyOwed_field.grid(row=7,column=1)
project_projectActive_field.grid(row=8,column=1)
project_contactName_field.grid(row=9,column=1)
project_companyName_field.grid(row=10,column=1)
project_notes_field.grid(row=11,column=1)

project_name_label.grid(row=0,column=0)
project_hourlyPay_label.grid(row=1,column=0)
project_quotedHours_label.grid(row=2,column=0)
project_workedHours_label.grid(row=3,column=0)
project_billedHours_label.grid(row=4,column=0)
project_totalInvoiced_label.grid(row=5,column=0)
project_totalPaid_label.grid(row=6,column=0)
project_moneyOwed_label.grid(row=7,column=0)
project_projectActive_label.grid(row=8,column=0)
project_contactName_label.grid(row=9,column=0)
project_companyName_label.grid(row=10,column=0)
project_notes_label.grid(row=11,column=0)

project_listbox.grid(column=4, row=0, rowspan=5)
project_listbox_button.grid(row=5,column=4)
project_delete_selected_button.grid(row=6, column=4)
project_show_all_button.grid(row=7, column=4)
project_save_button.grid(row=12,column=1)
project_clear_button.grid(row=13,column=1)

populate_project_listbox(show_all=True)


  ## display the session widgets
session_startTime_field.grid(row=0,column=1)
session_stopTime_field.grid(row=1,column=1)
session_time_field.grid(row=2,column=1)
session_notes_field.grid(row=3,column=1)
session_companyName_field.grid(row=4,column=1)
session_projectName_field.grid(row=5,column=1)
session_gitCommit_field.grid(row=6,column=1)

session_startTime_label.grid(row=0,column=0)
session_stopTime_label.grid(row=1,column=0)
session_time_label.grid(row=2,column=0)
session_notes_label.grid(row=3,column=0)
session_companyName_label.grid(row=4,column=0)
session_projectName_label.grid(row=5,column=0)
session_gitCommit_label.grid(row=6,column=0)

session_project_listbox_label.grid(column=4, row=0, sticky='w')
session_project_listbox.grid(column=4, row=1, rowspan=4)
session_project_listbox_button.grid(column=4, row=5)

session_session_listbox_label.grid(column=4, row=6, sticky='w')
session_session_listbox.grid(column=4, row=7, rowspan=4)
session_session_listbox_button.grid(column=4, row=11)
session_session_delete_selected_button.grid(column=4, row=12)
session_session_show_all_button.grid(column=4, row=13)
session_session_save_button.grid(column=4, row=14)


## 
## This line is so necessary.  Don't remove it.
##
root.mainloop()





