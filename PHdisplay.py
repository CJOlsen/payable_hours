# Payable Hours
# Author: Christopher Olsen
#
# Copyright Notice: Copyright 2012, 2013 Christopher Olsen
# License: None.  All rights reserved.
#
# Once this project reaches maturity it will likely be released into the
# wild but for now I'm removing the license to relieve myself from the fears
# of being prematurely forked.


## *** THIS FILE HOLDS THE DISPLAY AND LOGIC CODE, FOR MYSQL INTERFACE SEE 
##     PHdbOperations.py ***

import sys
import PHdbOperations as PHdb
import wx

# connect to database
connection,cursor = PHdb.connectDB()

debugging = True

################################################################################
#### wxpython code
################################################################################


class EntrySubPanel(wx.Panel):
    """ This is a subpanel that handles the creation and management of
        multiple text fields and their labels, and their buttons.
        Fields can be accessed through their names - but not directly.

        The dictionary of dictionaries may not be the optimal data structure.
        Should be a list of dictionaries using the list index for ordering.

        """

    def __init__(self, parent, names=None):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        # create some containers for the new labels and text boxes
        assert type(names) is list
        self.names = names
        self.fields = {}
        self.buttons = {}

        count = 0
        for name in names:
            assert type(name) is str
            if debugging: print "EntrySubPanel __init__, name:", name
            self.fields[name] = {'label':None, 'txt_field':None,'index':count}
            count += 1

        self.BuildUI()

    def BuildUI(self):
        """ This creates a column of labels corresponding to the list of names
            as well as a column of TextCtrl fields and save/clear buttons at the
            bottom.

            """

        ########################################################################
        ######## ****** artifact showing up on upper left of screen****#########
        ########################################################################
        main_sub_sizer = wx.BoxSizer(wx.VERTICAL)
        
        labels_panel = wx.Panel(self)
        textctrls_panel = wx.Panel(self)
        buttons_panel = wx.Panel(self)

        # make the sizers
        labels_sizer = wx.BoxSizer(wx.VERTICAL)
        textctrls_sizer = wx.BoxSizer(wx.VERTICAL)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # make the labels and text entry fields
        for name in self.names:
            self.fields[name]['label'] = wx.StaticText(self,
                                                       wx.ID_ANY,
                                                       ''.join([name, ':']))
            
            self.fields[name]['txt_field'] = wx.TextCtrl(self,
                                                         wx.ID_ANY,
                                                         "",
                                                         size=(200,25))
        
        # make the buttons
        self.buttons['save'] = wx.Button(self, 1, "Save", size=(100,25))
        self.buttons['clear'] = wx.Button(self, 2, "Clear", size=(100,25))

        # let the parent class handle the button events
        self.Bind(wx.EVT_BUTTON, self.parent.OnSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.parent.OnClear, id=2)

        # populate the sizers
        for name in self.names:
            labels_sizer.Add(self.fields[name]['label'],
                             1,
                             wx.ALL | wx.ALIGN_LEFT,
                             3)
            
            textctrls_sizer.Add(self.fields[name]['txt_field'],
                                1,
                                wx.ALL | wx.ALIGN_LEFT,
                                3)

        buttons_sizer.Add(self.buttons['save'], 0, wx.ALL, 5)
        buttons_sizer.Add(self.buttons['clear'], 0, wx.ALL, 5)

        not_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        not_buttons_sizer.Add(labels_sizer, 1, wx.EXPAND, 1)
        not_buttons_sizer.Add(textctrls_sizer, 0, wx.EXPAND, 0)

        main_sub_sizer.Add(not_buttons_sizer, 1, wx.EXPAND | wx.ALIGN_LEFT, 1)
        main_sub_sizer.Add(buttons_sizer, 1, wx.ALIGN_CENTER, 1)
        
        self.SetSizer(main_sub_sizer)

    def SetField(self, field_name, value):
        """ Takes a field_name and a value and sets that value in the UI
            Returns: nothing

            """
        # self.fields have a dictionary of 'label', 'txt_field', and 'index'
        if debugging: print 'EntrySubPanel SetField'
        self.fields[field_name]['txt_field'].SetValue(value)

    def GetField(self, field_name):
        """ Takes a field_name and
            Returns: a string retrieved from the UI

            """
        if debugging: print 'EntrySubPanel GetField, field_name:', field_name
        return self.fields[field_name]['txt_field'].GetValue()
        

class ListboxSubPanel(wx.Panel):
    """ Subpanel that handles the creation of a listbox and its corresponding
        buttons.

        """
    def __init__(self, parent, list_type=None):
        """ takes a parent object (a wxwidget parent) and a list_type that
            must be 'companies', 'contacts', 'projects', or 'sessions'

            """
        assert list_type in ['companies', 'contacts', 'projects', 'sessions',
                             None]
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.list_type = list_type

        self.BuildUI()

    def BuildUI(self):
        """ Attempts to build the user interface, called by self during init
            Returns: nothing (even in the event of error)

            """

        listbox_subpanel = wx.Panel(self.Parent)
        listbox_sizer = wx.BoxSizer(wx.VERTICAL)

        buttons_panel = wx.Panel(self.parent)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn_lstbx_select = wx.Button(self, 3, "Select", (22, 22))
        btn_lstbx_delete = wx.Button(self, 4, "Delete", (22, 22))

        buttons_sizer.Add(btn_lstbx_select, 0,wx.ALL, 5)
        buttons_sizer.Add(btn_lstbx_delete, 0, wx.ALL, 5)

            # label and listbox
        lbl_listbox = wx.StaticText(self,
                                    wx.ID_ANY,
                                    ''.join([self.list_type, ':']))

        # get the list depending on type of listbox
        if self.list_type == 'companies':
            the_list = PHdb.Company.get_all_names()
            listbox_height = 150
        elif self.list_type == 'contacts':
            the_list = PHdb.Contact.get_all_names()
            listbox_height = 125
        elif self.list_type == 'projects':
            the_list = PHdb.Project.get_all_projects()
            listbox_height = 300
        elif self.list_type == 'sessions':
            the_list = PHdb.Session.get_all_names()
            listbox_height = 200
            
        else:
            return Exception # could be more specific

        print 'the_list', the_list
        
        self.Bind(wx.EVT_LISTBOX, self.parent.OnListboxSelected, id=26)
        
        self.listbox = wx.ListBox(self,
                                  26,
                                  wx.DefaultPosition,
                                  (175, listbox_height),
                                  the_list,
                                  wx.LB_SINGLE)
        self.listbox.SetSelection(0)

        listbox_sizer.Add(lbl_listbox, 0, wx.ALL, 5)
        listbox_sizer.Add(self.listbox, 0, wx.ALL, 5)
        listbox_sizer.Add(buttons_sizer, 0, wx.ALL, 5)

        self.SetSizer(listbox_sizer)
        
        # bind buttons and events
        self.Bind(wx.EVT_BUTTON, self.parent.OnSelect, id=3)
        self.Bind(wx.EVT_BUTTON, self.parent.OnDelete, id=4)
        #self.Bind(wx.EVT_LISTBOX, self.parent.OnCompanySelected, id=26)

    def UpdateListbox(self):
        """ Reaches out to PHdbOperations and collects information of the
            current listbox type, updates the UI
            Returns: nothing

            """
        self.listbox.Set(self.current_orm_object.get_all_names())



class NotebookPanel(wx.Panel):
    """ This is the Class for notebook tabs.

        """
    def __init__(self, parent):
        """ Returns: nothing """
        wx.Panel.__init__(self, parent=parent)

        self.parent = parent
        self.current_orm_object = Exception
        self.current_selected = 0
        self.fields = Exception
        self.colleagues = []

    def update_listbox(self):
        """ Strange.  May conflict with ListboxSubpanel.UpdateListbox()
            One should be deprecated """
        ######## marked for deprecation ########
        new_list = self.current_orm_object.get_all_names()
        self.listbox_subpanel.listbox.Set(new_list)

    def BuildUI(self,panel_type):
        """ Panels are nested to create layout.  Logic is handled in the
            On*** definitions which recieve and handle events.  Elements that
            need to be accessible outside of this definition are prepended
            self.<element>
            Returns: nothing

            """
        assert panel_type in ['companies', 'contacts', 'projects', 'sessions']
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.entry_subpanel = EntrySubPanel(self, self.fields)
        self.listbox_subpanel = ListboxSubPanel(self, panel_type)
        
        main_sizer.Add(self.entry_subpanel)
        main_sizer.Add(self.listbox_subpanel)

        self.SetSizer(main_sizer)
    
    ####################
    ## Event Handling ##
    ####################
    def OnSelect(self, event):
        """ Bound to the Select button in the listbox subpanel.
            Gets the currently selected name from the UI listbox, calls
            upon PHdbOperations to get the corresponding info and updates
            the entry fields.
            Returns: nothing (event handling)
            
            """
        # get the selected text from the listbox (which is buried)
        name = self.listbox_subpanel.listbox.GetString(self.current_selected)

        # get a new ORM object from PHdb*.py by calling a @classmethod
        self.current_orm_object = self.current_orm_object.get_by_name(name)

        # step through the text boxes and update them
        for field in self.fields:
            new_value = self.current_orm_object.__dict__[field]
            if new_value is not None:
                self.entry_subpanel.SetField(field, new_value)
            else:
                self.entry_subpanel.SetField(field, '')


    def OnClear(self, event):
        """ Bound to the Clear button in the entry subpanel.
            Clears the entry fields of the UI.
            Returns: nothing (event handling)

            """
        # step through the fields, clearing them along the way
        for field in self.fields:
            self.entry_subpanel.SetField(field, '')

    def OnSave(self, event):
        """ Bound to the Save button in the entry subpanel.
            Collects data from entry fields and calls upon PHdbOperations to
            save them, then updates the UI listbox.
            Returns: nothing (event handling)

            """
        # don't save companies without names (make a dialog?)
        ####if len(self.entry_subpanel.txt_name.GetValue()) == 0:
        if len(self.entry_subpanel.GetField("txt_name")) == 0:
            print 'error, no name'
            return error
        
        for field in self.fields:
            value = self.entry_subpanel.GetField(field)
            self.current_orm_object.set_attr(field, value)

        # saving is handled by PHdbOperations.py
        self.current_company.write()
        self.update_listbox()

    def OnDelete(self, event):
        """ Bound to the Delete button in the listbox subpanel
            Gets the name of the currently selected item in the UI listbox
            and calls upon PHdbOperations to delete its corresponding record.
            Returns: nothing (event handling)

            """
        # get the selected text from the listbox (which is buried)
        name = self.listbox_subpanel.listbox.GetString(self.current_selected)        
        self.current_orm_object.delete_by_name(name)
        self.update_listbox()

    def OnListboxSelected(self, event):
        """ Bound to the listbox, called when a new member of the listbox
            is selected.  Only called for a mouseclick inside the listbox.
            Updates the internal "current_selected" variable.
            Returns: nothing

            """
        self.current_selected = event.GetSelection()

    ###################
    #### Messaging ####
    ###################

    def add_colleague(self, tab):
        """ Takes a notebook tab and adds it to the list of colleagues.

            """
        self.colleagues.append(tab)

    def remove_colleague(self, tab):
        """ Takes a notebook tab and attempts to remove it from the current
            list of colleagues.

            """
        self.colleagues = [x for x in self.colleagues if x is not tab]
        
    
    def receive_message(self, **kwargs):
        """ Takes incoming messages and performs necessary actions.

            """
        return NotImplementedError

    def send_message(self, **kwargs):
        """ Sends messages to all colleagues and performs necessary actions.

            """
        return NotImplementedError



class CompanyPanel(NotebookPanel):
    """ The company tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        self.current_orm_object = PHdb.Company(None)
        self.fields = ['name', 'address', 'city', 'state', 'phone', 'notes']
        self.BuildUI('companies')


    def receive_message(self, **kwargs):
        """ Takes incoming messages and performs necessary actions.

            """
        ## company panel doesn't need any messages
        pass

    def send_message(self, **kwargs):
        """ Sends messages to all colleagues and performs necessary actions.

            """
        ## sends message to contact, project and session tabs
        pass
        
 
class ContactPanel(NotebookPanel):
    """ The contact tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)

        self.current_selected = 0 #keeps track of selected listbox item
        self.current_orm_object = PHdb.Contact(None)
        self.fields = ['name', 'company', 'phone', 'email', 'notes']
        self.BuildUI('contacts')
        #self.Show()

    def receive_message(self, **kwargs):
        """ Takes incoming messages and performs necessary actions.

            """
        ## receives messages from company tab
        pass

    def send_message(self, **kwargs):
        """ Sends messages to all colleagues and performs necessary actions.

            """
        ## sends message to project and session tabs
        pass



class ProjectPanel(NotebookPanel):
    """ The project tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        self.fields = ['name', 'company', 'contact', 'hourly_pay',
                       'quoted_hours', 'worked_hours', 'billed_hours',
                       'total_invoiced', 'total_paid', 'money_owed',
                       'project_active', 'notes']
        self.current_ORM_object = PHdb.Project(None)
        self.BuildUI('projects')

    def receive_message(self, **kwargs):
        """ Takes incoming messages and performs necessary actions.

            """
        ## receives messages from company and contact tabs
        pass

    def send_message(self, **kwargs):
        """ Sends messages to all colleagues and performs necessary actions.

            """
        ## sends message to session tab
        pass



class SessionPanel(NotebookPanel):
    """ The session tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        self.current_orm_object = PHdb.Company(None)
        self.fields = ['sessionID', 'company_name',  'project_name',
                       'project_session_number', 'start_time', 'stop_time',
                       'time', 'notes', 'git_commit']
        self.BuildUI('sessions')


    def receive_message(self, **kwargs):
        """ Takes incoming messages and performs necessary actions.

            """
        ## receives messages from company, contact and project tabs
        pass

    def send_message(self, **kwargs):
        """ Sends messages to all colleagues and performs necessary actions.

            """
        ## sends message to session tab
        pass



class MysqlPanel(NotebookPanel):
    """ The MySQL tab for the notebook.  Allows the user to directly interact
        with the backend database.  Dangerous.

        """

    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        


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

app = wx.App(True)
frame = MainFrame(None,  'Payable Horses')
app.MainLoop()
        
    



