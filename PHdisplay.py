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


#connect to database
connection,cursor = PHdb.connectDB()

###############################################################################
#### LOGIC (the Controller in MVC)
###############################################################################



################################################################################
#### BUILD THE DISPLAY (the V in MVC)
################################################################################


class NotebookPanel(wx.Panel):
    """ This is the Class for notebook tabs.

        """
    def __init__(self, parent, name):
        wx.Panel.__init__(self, parent=parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        #label = wx.StaticText(self, label="this is a label")
        #sizer.Add(label)



class CompanyPanel(NotebookPanel):
    """ The company tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent, name= "Company")

        self.current_selected = 0
        #self.SetBackgroundColour('#4f5049')
        
        self.BuildUI()
        self.Show()



    def BuildUI(self):
        """ panels are nested to create layout

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
        left_sizer.Add(lbl_name, 0, wx.ALL, 10)
        left_sizer.Add(lbl_address, 0, wx.ALL, 10)
        left_sizer.Add(lbl_city, 0, wx.ALL, 10)
        left_sizer.Add(lbl_state, 0, wx.ALL, 10)
        left_sizer.Add(lbl_phone, 0, wx.ALL, 10)
        left_sizer.Add(lbl_notes, 0, wx.ALL, 10)
        left_sizer.Add(btn_field_save, 0, wx.ALL, 10)
        left_sizer.Layout()
        
        # middle panel: text fields and clear button
        txt_name = wx.TextCtrl(middle_panel, wx.ID_ANY, "")
        txt_address = wx.TextCtrl(middle_panel, wx.ID_ANY, "")
        txt_city = wx.TextCtrl(middle_panel, wx.ID_ANY, "")        
        txt_state = wx.TextCtrl(middle_panel, wx.ID_ANY, "")
        txt_phone = wx.TextCtrl(middle_panel, wx.ID_ANY, "")
        txt_notes = wx.TextCtrl(middle_panel, wx.ID_ANY, "")
        btn_field_clear = wx.Button(middle_panel, 2, "Clear", (13, 200))

        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        middle_sizer.Add(txt_name, 0, wx.ALL, 5)
        middle_sizer.Add(txt_address, 0, wx.ALL, 5)
        middle_sizer.Add(txt_city, 0, wx.ALL, 5)
        middle_sizer.Add(txt_state, 0, wx.ALL, 5)
        middle_sizer.Add(txt_phone, 0, wx.ALL, 5)
        middle_sizer.Add(txt_notes, 0, wx.ALL, 5)
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
                                     (175, 200), the_list, wx.LB_SINGLE)
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
        main_sizer.Add(right_panel)
        
        self.SetSizerAndFit(main_sizer)

    def OnSave(self, event):
        """ Saves the current fields into a new company or updates a current
            company if the name already exists.

            """
        pass

    def OnClear(self, event):
        """ Just clears the fields.  Doesn't delete the company.

            """
        pass

    def OnSelect(self, event):
        """ Bound to the select button.  populates the fields with the
            current selection's info.

            """
        print self.lstbx_companies.GetString(self.current_selected)

    def OnCompanySelected(self, event):
        """ Bound to the company listbox.  Updates the internal variable
            current_selected

            """
        self.current_selected = event.GetSelection()
        print self.current_selected

    def OnDelete(self, event):
        """ Deletes the current selection *from the database*

            """
        pass
    
 
        

class ContactPanel(NotebookPanel):
    """ The contact tab for the notebook.

        """
    def __init__(self, parent):
        NotebookPanel.__init__(self, parent= parent, name= "Contact")

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
        
    



