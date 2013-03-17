## Tkinter Test
##
##

from tkinter_automaker import *

def test():

    """ create tab
        create fields
        create notebook, add tab

        """
    root = tk.Tk()
    root.title("Testing Horse")
    root.geometry("300x300")

    notebook = Notebook(root)
    the_tab = Tab(notebook, 'test tab')
    new_tab = Tab(notebook, 'new tab')
    a = Element(master=the_tab, the_type = 'entry')
    b = Element(master=the_tab, the_type = 'entry')
    a.display()
    b.display()
    #notebook.add_tab(the_tab)
    #notebook.add_tab(new_tab)

    print 'notebook children: ', notebook.notebook.children
    notebook.display()

    
    
    root.mainloop()
