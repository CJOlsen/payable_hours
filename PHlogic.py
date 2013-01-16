# Payable Hours
# Author: Christopher Olsen

## *** THIS FILE HOLDS THE DISPLAY CODE, FOR MYSQL INTERFACE SEE 
##     PHdbOperations.py and for display code see PHmain.py ***


import sys
if '/home/james/Documents/programs/python/payablehours/' not in sys.path:
    print 'adding to sys path'
    sys.path.append('/home/james/Documents/programs/python/payablehours/')

    #import PHdisplay

import PHdbOperations as PHdb

### Clear tab function

def clear_frame(tab_frame):
    fields = tab_frame.winfo_children()
    [field.delete(0,'end') for field in fields\
     if field.winfo_class() == "Entry"]

### Company tab logic-------------------------------------------------------

def company_save():
    """called when the save button is pressed on the company tab"""
    company = PHdb.Company()
    company.name = company_name_field.get()
    company.address = company_address_field.get()
    company.city = company_city_field.get()
    company.state = company_state_field.get()
    company.phone = company_phone_field.get()
    company.write()

def company_selected(name,frame):

    #for field in company_fields:
    #    field.delete(0,'end')

    clear_frame(frame)
        
    company = PHdb.getCompanyByName(name)
    print 'company type', type(company)
    company_name_field.insert(0,name)
    company_address_field.insert(0,company.address)
    company_city_field.insert(0,company.city)
    company_state_field.insert(0,company.state)
    company_phone_field.insert(0,company.phone)
    company_notes_field.insert(0,company.notes)
    

    
### Contact tab logic-------------------------------------------------------

def contact_selected(name):
    #get contact company, update company tab
    pass


def save_contact():
    pass

    
def update_contact_tab(**kwargs):
    #if kwargs['clear?'] == True:
    pass   
        


### Project tab logic-------------------------------------------------------

def update_project_tab(**kwargs):
    pass

def project_selected(name):
    #update company and contact tabs
    pass

def save_project():
    pass



### Session tab logic-------------------------------------------------------

def update_session_tab(**kwaargs):
    pass

def session_selected(datetime):
    pass

def new_session():
    pass

def save_session():
    pass


### Observer


