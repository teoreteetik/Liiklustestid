from dbobject import *
from questionsGUI import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class OverviewGUI(Toplevel):
    '''Kuvab kõik küsimused treeviews'''
    
    def __init__(self):
        Toplevel.__init__(self)
        self.title('Ülevaade')

       
        questions = Question.findAll('ORDER BY correct/tries')
        
        #Raam, kus on nupud "Nulli statistika" ja "Sulge"
        buttonFrame = Frame(self)
        buttonFrame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = N+E+S+W)
        
        ttk.Button(buttonFrame, text = 'Nulli statistika', command = self.nullStats).grid(column = 0, row = 0, sticky = N+E+W)
        ttk.Button(buttonFrame, text = 'Sulge', command = self.destroy).grid(column = 0, row = 1, pady = 10, sticky = N+E+W)

        #Raam, kus on treeview ja selle scrollbar
        tableFrame = Frame(self)
        tableFrame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = N+E+S+W)

        #Treeview
        columns = ('id', 'question', 'tries', 'correct','percentage')
        columnHeadings = ('ID', 'Küsimus', 'Vastatud' ,'Õigesti', 'Edukus')

        self.tree = ttk.Treeview(tableFrame, columns=columns, show = 'headings')
        
        for i, column in enumerate(columns):
            self.tree.heading(column, text=columnHeadings[i], command=lambda column = column: self.treeSort(column, False))

        #Arvud joonda paremale
        self.tree.column('tries', anchor = 'e')
        self.tree.column('correct', anchor = 'e')
        self.tree.column('percentage', anchor = 'e')

        #Lisa küsimused treeviewsse
        for question in questions:
            self.tree.insert('', 'end', question.id, values=(question.id, question.question, question.tries, question.correct, question.percentage), tags = ('popUp'))
        #Iga küsimuse peal topeltkliki tehes kuvatakase valitud küsimus
        self.tree.tag_bind('popUp', '<Double-1>', self.displayQuestion)    
        self.tree.grid(row = 0, column = 0, sticky = N+E+S+W)


        #Scrollbar treeviews navigeerimiseks   
        scroller = ttk.Scrollbar(tableFrame, orient = VERTICAL, command = self.tree.yview)
        scroller.grid(row = 0, column = 1, sticky = N+S)
        self.tree.configure(yscrollcommand = scroller.set)


        #Et akna suuruse muutmisel muutuks ka treeview suurus
        self.rowconfigure(0,weight = 1)
        self.columnconfigure(1,weight = 1)
        tableFrame.rowconfigure(0,weight = 1)
        tableFrame.columnconfigure(0,weight = 1)

        self.mainloop()

    def nullStats(self):
        """ küsib kasutajalt üle kas ta ikka soovib nullida"""
        if messagebox.askyesno(message='Kas soovite nullida statistika?', title='Olete kindel?'):
            Question.nullStats()
            self.destroy()
            OverviewGUI()
        #muidu fookus kaob
        else: self.focus()
        
        
    def displayQuestion(self,_):
        '''Kuvab küsimuse kui kasutaja teeb topeltklõpsu küsimuse peal'''
        QuestionsGUI([Question.findByID(self.tree.focus())])

    def treeSort(self,column, reverse):
        '''Sorteerib treeview tulba päisele klõpsates, kasutatud koodijuppe siit: http://stackoverflow.com/questions/1966929/tk-treeview-column-sort'''
        l = [(self.tree.set(k, column), k) for k in self.tree.get_children('')]
        l = sorted(l, key = lambda a: a[0] if column=='question' else float(a[0]), reverse = reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        # reverse sort next time
        self.tree.heading(column, command = lambda: self.treeSort(column, not reverse))  
