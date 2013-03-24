# Payable Hours
# Author: Christopher Olsen
#
# Copyright Notice: Copyright 2012, 2013 Christopher Olsen
# License: None.  All rights reserved.
#
# Once this project reaches maturity it will likely be released into the
# wild but for now I'm removing the license to relieve myself from the fears
# of being prematurely forked.


# This is the testing file


import PHdbOperations as PHdbOps
#import PHdisplay



def populate_database():
    """ This function populates the database with test information.

        """
    # create Company objects and write them
    companies = []
    companies.append(PHdbOps.Company('company_name-1', 'company_address-1',
                                 'company_city-1', 'AA', 'company_phone-1',
                                 'company_notes-1'))
    companies.append(PHdbOps.Company('company_name-2', 'company_address-2',
                                 'company_city-2', 'BB', 'company_phone-2',
                                 'company_notes-2'))
    companies.append(PHdbOps.Company('company_name-3', 'company_address-3',
                                 'company_city-3', 'CC', 'company_phone-3',
                                 'company_notes-3'))
    companies.append(PHdbOps.Company('company_name-4', 'company_address-4',
                                 'company_city-4', 'AA', 'company_phone-4',
                                 'company_notes-4'))
    companies.append(PHdbOps.Company('company_name-5', 'company_address-5',
                                 'company_city-5', 'BB', 'company_phone-5',
                                 'company_notes-5'))
    for company in companies:
        company.write()

    # create Contact objects and write them
    contacts = []
    contacts.append(PHdbOps.Contact('contact_name-1', 'company_name-1',
                                    'contact_phone-1', 'contact_email-1',
                                    'contact_notes-1'))
    contacts.append(PHdbOps.Contact('contact_name-2', 'company_name-2',
                                    'contact_phone-2', 'contact_email-2',
                                    'contact_notes-2'))
    contacts.append(PHdbOps.Contact('contact_name-3', 'company_name-3',
                                    'contact_phone-3', 'contact_email-3',
                                    'contact_notes-3'))
    contacts.append(PHdbOps.Contact('contact_name-4', 'company_name-4',
                                    'contact_phone-4', 'contact_email-4',
                                    'contact_notes-4'))
    contacts.append(PHdbOps.Contact('contact_name-5', 'company_name-5',
                                    'contact_phone-5', 'contact_email-5',
                                    'contact_notes-5'))
    for contact in contacts:
        contact.write()

    projects = []
    projects.append(PHdbOps.Project('project_name-1', 'company_name-1',
                                    'hourly_pay-1', 'quoted_hours-1',
                                    'worked_hours-1', 'billed_hours-1',
                                    'total_invoiced-1', 'total_paid-1',
                                    'money_owed-1', 'project_active-1',
                                    'contact_name-1',
                                    'project_notes-1'))
    projects.append(PHdbOps.Project('project_name-2', 'company_name-2',
                                    'hourly_pay-2', 'quoted_hours-2',
                                    'worked_hours-2', 'billed_hours-2',
                                    'total_invoiced-2', 'total_paid-2',
                                    'money_owed-2', 'project_active-2',
                                    'contact_name-2',
                                    'project_notes-2'))
    projects.append(PHdbOps.Project('project_name-3', 'company_name-3',
                                    'hourly_pay-3', 'quoted_hours-3',
                                    'worked_hours-3', 'billed_hours-3',
                                    'total_invoiced-3', 'total_paid-3',
                                    'money_owed-3', 'project_active-3',
                                    'contact_name-3',
                                    'project_notes-3'))
    projects.append(PHdbOps.Project('project_name-4', 'company_name-4',
                                    'hourly_pay-4', 'quoted_hours-4',
                                    'worked_hours-4', 'billed_hours-4',
                                    'total_invoiced-4', 'total_paid-4',
                                    'money_owed-4', 'project_active-4',
                                    'contact_name-4',
                                    'project_notes-4'))
    projects.append(PHdbOps.Project('project_name-5', 'company_name-5',
                                    'hourly_pay-5', 'quoted_hours-5',
                                    'worked_hours-5', 'billed_hours-5',
                                    'total_invoiced-5', 'total_paid-5',
                                    'money_owed-5', 'project_active-5',
                                    'contact_name-5',
                                    'project_notes-5'))
    for project in projects:
        project.write()


    sessions = []
    sessions.append(PHdbOps.Session('company_name-1', 'proj_name-1',
                                    'proj_sesh-1', 'start_time-1',
                                    'stop_time-1', 'session_time-1',
                                    'session_notes-1', 'git_commit-1'))
    sessions.append(PHdbOps.Session('company_name-2', 'proj_name-2',
                                    'proj_sesh-2', 'start_time-2',
                                    'stop_time-2', 'session_time-2',
                                    'session_notes-2', 'git_commit-2'))
    sessions.append(PHdbOps.Session('company_name-3', 'proj_name-3',
                                    'proj_sesh-3', 'start_time-3',
                                    'stop_time-3', 'session_time-3',
                                    'session_notes-3', 'git_commit-3'))
    sessions.append(PHdbOps.Session('company_name-4', 'proj_name-4',
                                    'proj_sesh-4', 'start_time-4',
                                    'stop_time-4', 'session_time-4',
                                    'session_notes-4', 'git_commit-4'))
    sessions.append(PHdbOps.Session('company_name-5', 'proj_name-5',
                                    'proj_sesh-5', 'start_time-5',
                                    'stop_time-5', 'session_time-5',
                                    'session_notes-5', 'git_commit-5'))
    for session in sessions:
        print 'writing session: ', session.__dict__
        session.write()



def clear_database():
    """ drops all data in the database but leaves the table structure

        """
    connection, cursor = PHdbOps.connectDB()

    cursor.execute("DELETE FROM company")
    cursor.execute("DELETE FROM contact")
    cursor.execute("DELETE FROM project")
    cursor.execute("DELETE FROM session")
    connection.commit()

def reset_database():
    clear_database()
    populate_database()
    

        
    
    

        
    


        
    
    

    
