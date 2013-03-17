## Tkinter Notebook Maker
##
##
##


import Tkinter as tk
import ttk


class Element(object):
    """ A wrapper for tkinter elements.  This helps to create elements
        dynamically at runtime - they may not be known until then.

        name = name of the object, created internally.  Must be nothing or None.
        master = the notebook tab the element belongs to.  Notebook tab object.
        the_type = the element type (field, label, listbox or button). String.
        text = the short name of the element.  String.
        command = lambda function to execute when the button is pressed.
                must be a function existing elsewhere AND arguments for it!
                or nothing/None
        row, width, column, rowspan, sticky = display instructions
                must be int's except sticky must be 'e','w','n', or 's'.
                optional depending on element type
        tkel = the tkinter element being wrapped
                must be nothing or None.

        """
    def __init__(self, name=None, master=None, the_type=None,
                 text=None, command=None, row=None, width=None, rowspan=None,
                 sticky=None, tkel=None):
        assert name is None
        self.name = name
        
        # assert master in tabs_list #(need to create tabs_list)
        #assert type(master) is Tab
        self.master = master
        
        assert the_type in ['entry', 'label', 'button', 'listbox']
        self.the_type = the_type

        assert type(text) is str or text is None
        self.text = text
        
        assert type(command) is str or command is None
        #assert "lambda" in command
        #self.command = command
        
        assert type(row) is int or row is None
        self.row = row
        
        assert type(width) is int or width is None
        self.width = width
        
        assert type(rowspan) is int or rowspan is None
        self.rowspan = rowspan
        
        assert sticky in ['n','s','e','w'] or sticky is None
        self.sticky = sticky

        if self.the_type == "entry":
            self.text='test text'
            self.name = '_'.join((self.master.name,self.the_type,self.text))
            self.tkel = tk.Entry(self.master.tktab, width=self.width)

        elif self.the_type == "label":
            self.name = '_'.join((self.master,self.the_type,self.text))
            self.tkel = tk.Label(self.master, self.text)

        elif self.the_type == "button":
            pass

        elif self.the_type == "listbox":
            pass
        
    def display(self, the_row=None, the_column=None, sticky=None, rowspan=None):
        """ execute the grid command on self.tkel
        """
        self.row = the_row
        self.column = the_column
        if sticky is not None and rowspan is not None:
            self.tkel.grid(row=self.row, column=self.column,
                           rowspan=self.rowspan, sticky=self.sticky)
        elif sticky is None and rowspan is not None:
            self.tkel.grid(row=self.row, column=self.column,
                           rowspan=self.rowspan)
        elif sticky is None and rowspan is None:
            self.tkel.grid(row=self.row, column=self.column)
        else:
            print "maybe there's been an error"

    def clear(self):
        """ Only for entry fields and lisboxes
        """
        pass
    
    def update(self):
        """ Only for listboxes
        """
        pass


class Tab(object):
    """ This is a wrapper for the tkinter notebook tab that keeps track of
        all of the elements in the tab and decides how to display them
        when it is time.  It contains (for now) a list of field elements.

        """
    def __init__(self, master=None, name=None):
        assert type(name) is str
        self.name = name
        self.tktab = tk.Frame()
        self.master = master
        self.master.notebook.add(self.tktab, text=self.name)

    def update(self):
        pass

    def display(self):
        for i in range(len(self.elements)):
            self.element[i].display(i, 0)

    def add(self, element):
        assert type(element) is Element
        self.elements.add(element)

    def remove(self):
        """ currently removes the last object added
        """
        self.elements.pop()

    def add_field():
        pass

    def add_listbox():
        pass

    def add_field_button():
        pass

    def add_listbox_button():
        pass
        
        

class Notebook(object):
    """ This is a wrapper for the tkinter Notebook object, just in case
        it's needed later.

        """
    def __init__(self, master=None):
        self.notebook = ttk.Notebook(master)

    def display(self):
        
        self.notebook.grid(row=0, column=0)

    def add_tab(self, tab=None):
        assert type(tab) is Tab
        self.notebook.add(tab.tktab, text=tab.name)


##def test():
##
##    """ create tab
##        create fields
##        create notebook, add tab
##
##        """
##    root = tk.Tk()
##    root.title("Testing Horse")
##    root.geometry("300x300")
##
##    nbook = Notebook(root)
##    the_tab = Tab(nbook, 'test tab')
##    the_tab = Tab(nbook, 'another test tab')    
##    a = Element(master=the_tab, the_type = 'entry')
##    b = Element(master=the_tab, the_type = 'entry')
##    
##
##    nbook.display()
##    
##    root.mainloop()
        
        


## Create A Field
    ## create a name to reference the field by (challenge)
    ## field_name = tk.Entry(master, width=xx)
    ## create a name to reference the field label by (challenge)
    ## label_name = tk.Entry(master, "name")
    ## field_name.grid(row=x, column=y, sticky="w")
    ## field_label.grid(""                       "")

## Create A Listbox
    ## create a listbox name to reference the lisbox by
    ## listbox_name = tk.Listbox(master)
    ## listbox_name.grid(row=x, column=y, rowspan=z)

## Create A Button
    ## create a name to reference the Button by
    ## button_name = tk.Button(master,
    ##                         name = "name",
    ##                         command = lambda: method(*args)
    ## button_name.grid(....)
    ##
    ## Create The Button Command
        ## create method name and method
        ## create lambda function and argument
        ##
        ## Classes Of Button Events
            ## listbox select & delete, clear & refresh
            ## tab save & clear

## Create Main Window

## Create Notebook

## Create Tabs

## Create Tab Elements For A Tab

## Repeat For Each Tab

## Display Each Tab's Elements

