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
        
    



