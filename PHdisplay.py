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
import wx

##from wx.lib.pubsub import setupkwargs
##from wx.lib.pubsub import pub


#connect to database
connection,cursor = PHdb.connectDB()

#################################################################################
###### wxpython publish-subscribe broker (PubSub)
#################################################################################
##
##class SomeReceiver(object):
##    def __init__(self):
##        pub.subscribe(self.__onObjectAdded, 'object.added')
##
##    def __onObjectAdded(self, data, extra1, extra2=None):
##        print 'Object', repr(data), 'is added'
##        print extra1
##        if extra2:
##            print extra2




################################################################################
#### wxpython code
################################################################################


class NotebookPanel(wx.Panel):
    """ This is the Class for notebook tabs.

        """
    def __init__(self, parent, name):
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.observers = []

    ## Set up message passing between the tabs
    def add_observer(self, observer):
        assert type(observer) is NotebookPanel
        self.observers.append(observer)

    def remove_observer(self, observer):
        assert type(observer) is NotebookPanel
        self.observers.remove(observer)
        
    def send_message(self, message):
        """ Must be overridden by instance.
            
            """
        return NotImplementedError

    def receive_message(self, message):
        """ Must be overridden by instance.

            """
        return NotImplementedError



class CompanyPanel(NotebookPanel):
    """ The company tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent, name= "Company")
        
        self.current_selected = 0 #keeps track of selected listbox item
        self.current_company = None
        
        self.BuildUI()
        self.Show()

    def BuildUI(self):
        """ Panels are nested to create layout.  Logic is handled in the
            On*** definitions which recieve and handle events.  Elements that
            need to be accessible outside of this definition are prepended
            self.<element>

            """
        left_panel = wx.Panel(self)
        middle_panel = wx.Panel(self)
        right_panel = wx.Panel(self)
        
        # left panel: labels and save button
        lbl_name = wx.StaticText(left_panel, wx.ID_ANY, "Name:")
        lbl_address = wx.StaticText(left_panel, wx.ID_ANY, "Address:")
        lbl_city = wx.StaticText(left_panel, wx.ID_ANY, "City:")
        lbl_state = wx.StaticText(left_panel, wx.ID_ANY, "State:")
        lbl_phone = wx.StaticText(left_panel, wx.ID_ANY, "Phone:")
        lbl_notes = wx.StaticText(left_panel, wx.ID_ANY, "Notes:")
        btn_field_save = wx.Button(left_panel, 1, "Save", (50, 13))

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(item= lbl_name,
                       proportion= 0, # use ratios between elements
                       flag= wx.ALL, # border, alignment and sizing changes
                       border= 10,
                       userData= None) # generally not used
        left_sizer.Add(lbl_address, 0, wx.ALL, 10)
        left_sizer.Add(lbl_city, 0, wx.ALL, 10)
        left_sizer.Add(lbl_state, 0, wx.ALL, 10)
        left_sizer.Add(lbl_phone, 0, wx.ALL, 10)
        left_sizer.Add(lbl_notes, 0, wx.ALL, 10)
        left_sizer.Add(btn_field_save, 0, wx.ALL, 10)
        left_sizer.Layout()
        
        # middle panel: text fields and clear button
        self.txt_name = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        self.txt_address = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        self.txt_city = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))        
        self.txt_state = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        self.txt_phone = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        self.txt_notes = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        btn_field_clear = wx.Button(middle_panel, 2, "Clear", (13, 200))

        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        middle_sizer.Add(self.txt_name, 0, wx.ALL | wx.EXPAND, 5)
        middle_sizer.Add(self.txt_address, 0, wx.ALL, 5)
        middle_sizer.Add(self.txt_city, 0, wx.ALL, 5)
        middle_sizer.Add(self.txt_state, 0, wx.ALL, 5)
        middle_sizer.Add(self.txt_phone, 0, wx.ALL, 5)
        middle_sizer.Add(self.txt_notes, 0, wx.ALL, 5)
        middle_sizer.Add(btn_field_clear, 0, wx.ALL, 10)
        middle_sizer.Layout()

        # right panel:
            # listbox buttons
        listbox_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_lstbx_select = wx.Button(right_panel, 3, "Select", (22, 22))
        btn_lstbx_delete = wx.Button(right_panel, 4, "Delete", (22, 22))

        listbox_buttons_sizer.Add(btn_lstbx_select, 0,wx.ALL, 5)
        listbox_buttons_sizer.Add(btn_lstbx_delete, 0, wx.ALL, 5)
        listbox_buttons_sizer.Layout()

            # label and listbox
        lbl_listbox = wx.StaticText(right_panel, wx.ID_ANY, "Companies:")
        the_list = PHdb.Company.get_all_companies()
                # listbox's self.foo because it's needed elsewhere
        self.lstbx_companies = wx.ListBox(right_panel,  26, wx.DefaultPosition,
                                     (175, 175), the_list, wx.LB_SINGLE)
        self.lstbx_companies.SetSelection(0)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(lbl_listbox, 0, wx.ALL, 5)
        right_sizer.Add(self.lstbx_companies, 0, wx.ALL, 5)
        right_sizer.Add(listbox_buttons_sizer, 0, wx.ALL, 5)
        right_sizer.Layout()

        # bind buttons and events

        self.Bind(wx.EVT_BUTTON, self.OnSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=4)
        self.Bind(wx.EVT_LISTBOX, self.OnCompanySelected, id=26)
        
        # add the columns to the main tab frame
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_panel)
        main_sizer.Add(middle_panel) # add a ,2 for spacing
        main_sizer.Add(right_panel, flag=wx.LEFT, border=45)
        
        self.SetSizerAndFit(main_sizer)
        main_sizer.Layout()

    def update_listbox(self):
        self.lstbx_companies.Set(PHdb.Company.get_all_companies())
        
    
    ####################
    ## Event Handling ##
    ####################    
    def OnSave(self, event):
        """ Saves the current fields into a new company or updates a current
            company if the name already exists.

            """

        # don't save companies without names (make a dialog?)
        if len(self.txt_name.GetValue()) == 0:
            print 'error, no name'
            pass
        
        # modify/create Company object for PHdbOperations.py
        if not self.current_company:
            self.current_company = PHdb.Company()
        self.current_company.name = self.txt_name.GetValue()
        self.current_company.address = self.txt_address.GetValue()
        self.current_company.city = self.txt_city.GetValue()
        self.current_company.state = self.txt_state.GetValue()
        self.current_company.phone = self.txt_phone.GetValue()
        self.current_company.notes = self.txt_notes.GetValue()

        # saving is handled by PHdbOperations.py
        self.current_company.write()
        self.update_listbox()
        

    def OnClear(self, event):
        """ Just clears the fields.  Doesn't delete the company.

            """
        # just clear everything out
        self.txt_name.SetValue("")
        self.txt_address.SetValue("")
        self.txt_city.SetValue("")
        self.txt_state.SetValue("")
        self.txt_phone.SetValue("")
        self.txt_notes.SetValue("")
        

    def OnSelect(self, event):
        """ Bound to the select button.  populates the fields with the
            current selection's info.

            """
        # get new Company object from PHdbOperations.py
        name = self.lstbx_companies.GetString(self.current_selected)
        self.current_company = PHdb.Company.get_by_name(name)

        # update listbox values with new company
        self.txt_name.SetValue(self.current_company.name)
        self.txt_address.SetValue(self.current_company.address)
        self.txt_city.SetValue(self.current_company.city)
        self.txt_state.SetValue(self.current_company.state)
        self.txt_phone.SetValue(self.current_company.phone)
        self.txt_notes.SetValue(self.current_company.notes)

    def OnCompanySelected(self, event):
        """ Bound to the company listbox.  Updates the internal variable
            current_selected (doesn't update the locally stored company object)

            """
        self.current_selected = event.GetSelection()
        

    def OnDelete(self, event):
        """ Deletes the current selection *from the database*

            """
        # could use an "are you sure?" dialog
        # deletion handled by PHdbOperations.py
        name = self.lstbx_companies.GetString(self.current_selected)
        PHdb.Company.delete_by_name(name)
        self.update_listbox()
    
 
        

class ContactPanel(NotebookPanel):
    """ The contact tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent, name= "Contact")

        self.current_selected = 0 #keeps track of selected listbox item
        self.current_company = None
        
        self.BuildUI()
        self.Show()


    def BuildUI(self):
        """ Panels are nested to create layout.  Logic is handled in the
            On*** definitions which recieve and handle events.  Elements that
            need to be accessible outside of this definition are prepended
            self.<element>

            """
        left_panel = wx.Panel(self)
        middle_panel = wx.Panel(self)
        right_panel = wx.Panel(self)
        
        # left panel: labels and save button
        lbl_name = wx.StaticText(left_panel, wx.ID_ANY, "Name:")
        lbl_company = wx.StaticText(left_panel, wx.ID_ANY, "Company:")
        lbl_phone = wx.StaticText(left_panel, wx.ID_ANY, "Phone:")
        lbl_email = wx.StaticText(left_panel, wx.ID_ANY, "Email:")
        lbl_notes = wx.StaticText(left_panel, wx.ID_ANY, "Notes:")
        btn_field_save = wx.Button(left_panel, 1, "Save", (50, 13))

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(item= lbl_name,
                       proportion= 0, # use ratios between elements
                       flag= wx.ALL, # border, alignment and sizing changes
                       border= 10,
                       userData= None) # generally not used
        left_sizer.Add(lbl_company, 0, wx.ALL, 10)
        left_sizer.Add(lbl_phone, 0, wx.ALL, 10)
        left_sizer.Add(lbl_email, 0, wx.ALL, 10)
        left_sizer.Add(lbl_notes, 0, wx.ALL, 10)
        left_sizer.Add(btn_field_save, 0, wx.ALL, 10)
        left_sizer.Layout()
        
        # middle panel: text fields and clear button
        self.txt_name = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        self.txt_company = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        self.txt_phone = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))        
        self.txt_email = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        self.txt_notes = wx.TextCtrl(middle_panel, wx.ID_ANY, "", size=(200,25))
        btn_field_clear = wx.Button(middle_panel, 2, "Clear", (13, 200))

        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        middle_sizer.Add(self.txt_name, 0, wx.ALL | wx.EXPAND, 5)
        middle_sizer.Add(self.txt_company, 0, wx.ALL, 5)
        middle_sizer.Add(self.txt_phone, 0, wx.ALL, 5)
        middle_sizer.Add(self.txt_email, 0, wx.ALL, 5)
        middle_sizer.Add(self.txt_notes, 0, wx.ALL, 5)
        middle_sizer.Add(btn_field_clear, 0, wx.ALL, 10)
        middle_sizer.Layout()

        # right panel:
            # listbox buttons
        listbox_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_listbox_showall = wx.Button(right_panel, 5, "Show All", (22,22))
        btn_lstbx_select = wx.Button(right_panel, 3, "Select", (22, 22))
        btn_lstbx_delete = wx.Button(right_panel, 4, "Delete", (22, 22))

        #listbox_buttons_sizer.Add(btn_listbox_showall, 0, wx.ALL, 5)
        listbox_buttons_sizer.Add(btn_lstbx_select, 0,wx.ALL, 5)
        listbox_buttons_sizer.Add(btn_lstbx_delete, 0, wx.ALL, 5)
        listbox_buttons_sizer.Layout()

            # label and listbox
        lbl_listbox = wx.StaticText(right_panel, wx.ID_ANY, "Contacts:")
        the_list = PHdb.Contact.get_all_contacts()
                # listbox's self.foo because it's needed elsewhere
        self.lstbx_contacts = wx.ListBox(right_panel,  26, wx.DefaultPosition,
                                     (175, 175), the_list, wx.LB_SINGLE)
        self.lstbx_contacts.SetSelection(0)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add(lbl_listbox, 0, wx.ALL, 5)
        right_sizer.Add(self.lstbx_contacts, 0, wx.ALL, 5)
        right_sizer.Add(btn_listbox_showall, 0, wx.LEFT, 50)
        right_sizer.Add(listbox_buttons_sizer, 0, wx.ALL, 5)
        right_sizer.Layout()

        # bind buttons and events

        self.Bind(wx.EVT_BUTTON, self.OnSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=4)
        self.Bind(wx.EVT_BUTTON, self.OnShowAll, id=5)
        self.Bind(wx.EVT_LISTBOX, self.OnContactSelected, id=26)
        
        # add the columns to the main tab frame
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_panel)
        main_sizer.Add(middle_panel) # add a ,2 for spacing
        main_sizer.Add(right_panel, flag=wx.LEFT, border=45)
        
        self.SetSizerAndFit(main_sizer)
        main_sizer.Layout()

    def update_listbox(self):
        self.lstbx_contacts.Set(PHdb.Contact.get_all_contacts())
        
    
    ####################
    ## Event Handling ##
    ####################    
    def OnSave(self, event):
        """ Saves the current fields into a new company or updates a current
            company if the name already exists.

            """

        # don't save contacts without names (make a dialog?)
        if len(self.txt_name.GetValue()) == 0:
            print 'error, no name'
            pass
        
        # modify/create Company object for PHdbOperations.py
        if not self.current_contact:
            self.current_contact = PHdb.Contact()
        self.current_contact.name = self.txt_name.GetValue()
        self.current_contact.company = self.txt_company.GetValue()
        self.current_contact.phone = self.txt_phone.GetValue()
        self.current_contact.email = self.txt_email.GetValue()
        self.current_contact.notes = self.txt_notes.GetValue()

        # saving is handled by PHdbOperations.py
        self.current_contact.write()
        self.update_listbox()
        

    def OnClear(self, event):
        """ Just clears the fields.  Doesn't delete the company.

            """
        # just clear everything out
        self.txt_name.SetValue("")
        self.txt_company.SetValue("")
        self.txt_phone.SetValue("")
        self.txt_email.SetValue("")
        self.txt_notes.SetValue("")
        
    def OnSelect(self, event):
        """ Bound to the select button.  populates the fields with the
            current selection's info.

            """
        # get new Company object from PHdbOperations.py
        name = self.lstbx_contacts.GetString(self.current_selected)
        self.current_contact = PHdb.Contact.get_by_name(name)

        # update listbox values with new company
        self.txt_name.SetValue(self.current_contact.name)
        self.txt_company.SetValue(self.current_contact.company)
        self.txt_phone.SetValue(self.current_contact.phone)
        self.txt_email.SetValue(self.current_contact.email)
        self.txt_notes.SetValue(self.current_contact.notes)

    def OnContactSelected(self, event):
        """ Bound to the company listbox.  Updates the internal variable
            current_selected (doesn't update the locally stored company object)

            """
        self.current_selected = event.GetSelection()
        

    def OnDelete(self, event):
        """ Deletes the current selection *from the database*

            """
        # could use an "are you sure?" dialog
        # deletion handled by PHdbOperations.py
        name = self.lstbx_contacts.GetString(self.current_selected)
        PHdb.Contact.delete_by_name(name)
        self.update_listbox()

    def OnShowAll(self, event):
        """ Show all contacts regardless of the comany chosen in the company tab

            """
        pass
        

class ProjectPanel(NotebookPanel):
    """ The project tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent, name= "Project")

class SessionPanel(NotebookPanel):
    """ The session tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent, name= "Session")

class MysqlPanel(NotebookPanel):
    """ The MySQL tab for the notebook.  Allows the user to directly interact
        with the backend database.  Dangerous.

        """

    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent, name= "MySQL")
        


class MainNotebook(wx.Notebook):
    """ This is the main Notebook

        """
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)

        # add the 5 tabs
        self.AddPage(CompanyPanel(self), "Company")
        self.AddPage(ContactPanel(self), "Contact")
        self.AddPage(ProjectPanel(self), "Project")
        self.AddPage(SessionPanel(self), "Session")
        self.AddPage(MysqlPanel(self), "MySQL")
        

class MainFrame(wx.Frame):
    """ Main Payable Hours frame.

        """
    def __init__(self,  parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,400))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # add the notebook
        self.Notebook = MainNotebook(self)
        
        # setting up the file menu
        filemenu = wx.Menu()

        #wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxwidgets
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", " Terminate the program.")

        # Creating the Menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        self.Show(True)

        # create event bindings
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        # display the notebook
        sizer = wx.BoxSizer()
        sizer.Add(self.Notebook, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)
        self.Layout()

    def OnAbout(self, e):
        """ Bound to the 'About' menu item.  Displays a dialog box with an OK
            button.

            """
        text = "Payable Hours is a time tracking application by Christopher "\
               "Olsen.\n\ngithub.com/cjolsen"
        dialog = wx.MessageDialog(self,
                                  text,
                                  "About Payable Hours",
                                  wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, e):
        self.Close(True)

app = wx.App(False)
frame = MainFrame(None,  'Payable Horses')
app.MainLoop()
        
    



