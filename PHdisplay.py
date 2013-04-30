# Payable Hours
# Author: Christopher Olsen
#
# Copyright Notice: Copyright 2012, 2013 Christopher Olsen
# License: None. All rights reserved.
#
# Once this project reaches maturity it will likely be released into the
# wild but for now I'm removing the license to relieve myself from the fears
# of being prematurely forked.


## *** THIS FILE HOLDS THE DISPLAY AND LOGIC CODE, FOR MYSQL INTERFACE SEE
## PHdbOperations.py ***


import wx
import PHdbOperations as PHdb

connection, cursor = PHdb.connectDB()

class Observable(object):
    """ An observer class to facilitate tab synchronization.  ie when a comapny
        is active in the Company tab only projects and contacts from that
        company will show in the other tabs (showall button is still there)

        """
    def __init__(self):
        self.observers = []
    def subscribe(self, observer):
        self.observers.append(observer)
    def inbox(self, event):
        # each tab needs to handle the messages differently, so this must be
        # implemented in the child class
        return NotImplementedError
    def fire(self, **kwargs):
        for o in self.observers:
            o.inbox(kwargs)

class NotebookPanel(wx.Panel, Observable):
    """ This is the Class for notebook tabs.

        """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        Observable.__init__(self)
        self.parent = parent
        self.buttons = {}
        self.current_orm_object = None
        self.current_selected = 0
        #self.fields = Exception
        #self.colleagues = []

    def AddEntryFields(self):
        """ Adds the entry fields and their labels based on the self.fields list
            defined in the child class.

            """
        assert self.fields
        
        self.labels = {}
        self.entry_fields = {}
        i = 0
        for member in self.fields:
            self.labels[member] = wx.StaticText(self.panel,
                                                label=member)
            self.sizer.Add(self.labels[member],
                           pos=(i,0),
                           flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                           border=5)
            self.entry_fields[member] = wx.TextCtrl(self.panel,
                                                    size=(200,25))
            self.sizer.Add(self.entry_fields[member],
                           pos=(i,1),
                           flag=wx.TOP|wx.LEFT,
                           border=1)
            i += 1



    
    def BuildUI(self, panel_type):
        """ Panels are nested to create layout.  Logic is handled in the
            On*** definitions which recieve and handle events.  Elements that
            need to be accessible outside of this definition are prepended
            self.<element>
            Returns: nothing

            """
        assert panel_type in ['companies', 'contacts', 'projects', 'sessions']
        self.list_type = panel_type
        
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(5, 5) # (vgap, hgap)

        self.AddEntryFields()

        # add entry buttons
        save_button = wx.Button(self.panel, 1, "Save")
        clear_button = wx.Button(self.panel, 2, "Clear")
        self.sizer.Add(save_button,             # item
                       (len(self.fields), 0),   # position
                       (1,1),                   # span=DefaultSpan
                       wx.ALIGN_RIGHT,          # flag=0
                       5)                       # border=0, userData=None
        self.sizer.Add(clear_button,
                       (len(self.fields), 1),
                       (1,1),
                       wx.ALIGN_LEFT,
                       5)

        # add listbox
        ## get the list and height depending on type of listbox
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
            return Exception # should be more specific

        self.listbox_label = wx.StaticText(self.panel,
                                           wx.ID_ANY,
                                           self.list_type)
        self.sizer.Add(self.listbox_label,
                       (0,3),
                       (1,1),
                       wx.ALIGN_LEFT|wx.ALIGN_BOTTOM,
                       5)
        
        self.listbox = wx.ListBox(self.panel,           # parent
                                  26,                   # id
                                  (1,2),                # pos
                                  (275, 28.5*(len(self.fields)-1)),# size
                                  the_list,             # choces
                                  wx.LB_SINGLE)         # style
        self.sizer.Add(self.listbox,
                       (1,3),
                       (len(self.fields)-1,1),
                       wx.ALIGN_LEFT,
                       5)
        self.panel.SetSizerAndFit(self.sizer)

        self.sizer.text = "what the who"

        # add listbox buttons
        select_button = wx.Button(self.panel, 3, "Select")
        delete_button = wx.Button(self.panel, 4, "Delete")
        showall_button = wx.Button(self.panel, 5, "Show All")
        listbox_button_sizer =wx.BoxSizer()
        listbox_button_sizer.Add(select_button)
        listbox_button_sizer.Add(delete_button)
        listbox_button_sizer.Add(showall_button)
        self.sizer.Add(listbox_button_sizer,
                       (len(self.fields), 3),
                       (1,2),
                       wx.ALIGN_CENTER,
                       5)

        # bind buttons to events
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=4)
        self.Bind(wx.EVT_BUTTON, self.OnShowAll, id=5)

        self.Bind(wx.EVT_LISTBOX, self.OnListboxSelected, id=26)

    # Event Handling (button event methods are CapitalizedCamelCase)
    
    def OnClear(self, event):
        """ Clears the text fields.

            """
        for field in self.fields:
            # entry_fields is a dictionary connecting field names to their
            # text boxes
            self.entry_fields[field].SetValue('')
    
    # the following event handling to be handled by children classes
    def OnSave(self, event):
        """

            """
        # still needs to be overridden for the session tab 
        if len(self.entry_fields["name"].GetValue()) == 0:
            print 'Error, no name'
            return
        for field in self.fields:
            value = self.entry_fields[field].GetValue()
            self.current_orm_object.set_attr(field, value)
            
        self.current_orm_object.write()
        self.update_listbox()
        
    def OnSelect(self, event):
        """

            """
        # get a new ORM object from PHdb***.py by calling a @classmethod
        self.current_name = name = self.listbox.GetString(self.current_selected)
        self.current_orm_object = self.current_orm_object.get_by_name(name)

        # step through the text boxes and update them
        for field in self.fields:
            new_value = self.current_orm_object.__dict__[field]
            if new_value is not None:
                self.entry_fields[field].SetValue(str(new_value))
            else:
                self.entry_fields[field].SetValue('')

        self.fire_message()
                
    def OnDelete(self, event):
        name = self.listbox.GetString(self.current_selected)
        self.current_orm_object.delete_by_name(name)
        self.update_listbox()

    def OnShowAll(self, event):
        self.update_listbox()

    def OnListboxSelected(self, event):
        self.current_selected = event.GetSelection()

    def update_listbox(self):
        new_list = self.current_orm_object.get_all_names()
        self.listbox.Set(new_list)

    def fire_message(self):
        if self.list_type == 'companies':
            self.fire(company=self.current_name)
        elif self.list_type == 'contacts':
            self.fire(contact=self.current_name)
        elif self.list_type == 'projects':
            self.fire(project=self.current_name)
        else:
            pass
        
        
        


class CompanyPanel(NotebookPanel):
    """ The company tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        self.current_orm_object = PHdb.Company(None)
        self.fields = ['name', 'address', 'city', 'state', 'phone', 'notes']
        self.BuildUI('companies')

    def inbox(self, event):
        for key in event.keys():
            if key[0] == 'contact':
                name = PHdb.Contact().get_by_name(event[key]).company
                self.current_orm_object = self.current_orm_object.get_by_name(name)
                # get company for the contact
                pass
            elif key[0] == 'project':
                # get company for the project, if none just clear the fields
                pass
            elif key[0] == 'session':
                # get company for the session, if none just clear the fields
                pass
            else:
                pass
        # update fields
        
        # get a new ORM object from PHdb***.py by calling a @classmethod
        #self.current_name = name = self.listbox.GetString(self.current_selected)
        #self.current_orm_object = self.current_orm_object.get_by_name(name)

        # step through the text boxes and update them
        for field in self.fields:
            new_value = self.current_orm_object.__dict__[field]
            if new_value is not None:
                self.entry_fields[field].SetValue(str(new_value))
            else:
                self.entry_fields[field].SetValue('')
            
        


class ContactPanel(NotebookPanel):
    """ The contact tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        self.current_orm_object = PHdb.Contact(None)
        self.fields = ['name', 'company', 'phone', 'email', 'notes']
        self.current_state = {'company':None}
        self.BuildUI('contacts')
        

    def inbox(self, event):
        print 'contact recieved event', event
        filtered_list = self.current_orm_object.get_filtered_names(event)
        self.listbox.Set(filtered_list)


class ProjectPanel(NotebookPanel):
    """ The project tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        self.current_orm_object = PHdb.Project(None)
        self.fields = ['name', 'company', 'contact', 'hourly_pay',
                       'quoted_hours', 'worked_hours', 'billed_hours',
                       'total_invoiced', 'total_paid', 'money_owed',
                       'project_active', 'notes']
        self.current_state = {'company':None, 'contact':None}
        self.BuildUI('projects')

    def inbox(self, event):
        ## cases:
        ## *company selected
        ## *contact selected
        print 'project recieved event', event
        for k in event:
            print k,event[k]

class SessionPanel(NotebookPanel):
    """ The session tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent)
        self.current_orm_object = PHdb.Company(None)
        self.fields = ['sessionID', 'company',  'project',
                       'project_session_number', 'start_time', 'stop_time',
                       'time', 'notes', 'git_commit']
        self.current_state = {'company':None, 'contact':None, 'project':None}
        self.BuildUI('sessions')

    def inbox(self, event):
        print 'session recieved event', event
        for k in event:
            print k,event[k]

        
        

class MainNotebook(wx.Notebook):
    """ This is the main Notebook

        """
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent=parent)

        # make the noteboox tabs
        self.company_panel = CompanyPanel(self)
        self.contact_panel = ContactPanel(self)
        self.project_panel = ProjectPanel(self)
        self.session_panel = SessionPanel(self)

        # sign up for message passing
        self.company_panel.subscribe(self.contact_panel)
        self.company_panel.subscribe(self.project_panel)
        self.company_panel.subscribe(self.session_panel)
        self.contact_panel.subscribe(self.project_panel)
        self.contact_panel.subscribe(self.session_panel)
        self.project_panel.subscribe(self.session_panel)
        
        # add the notebook tabs
        self.AddPage(self.company_panel, "Company")
        self.AddPage(self.contact_panel, "Contact")
        self.AddPage(self.project_panel, "Project")
        self.AddPage(self.session_panel, "Session")
        #self.AddPage(MysqlPanel(self), "MySQL")


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
        sizer.Add(self.Notebook, 1, wx.EXPAND, border =15)
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



app = wx.App()
MainFrame(None, title="what the what?")
app.MainLoop()
