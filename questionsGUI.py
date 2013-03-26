from dbobject import *
from tkinter import *
from tkinter import ttk

class QuestionsGUI(Toplevel):
    '''Aken, kus kuvatakse etteantud küsimused, kui küsimusi ei anta, leiab ise'''

    def __init__(self, questions = []):
        Toplevel.__init__(self)
        self.title('Küsimused')
        
        
        self.focus()
        #et akna suuruse muutmisel elemendid kaasa tuleksid
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


        #scrollbar küsimuste scrollimiseks
        self.vscrollbar = Scrollbar(self)
        self.vscrollbar.grid(row=0, column=1, sticky=N+S)
        #kõik küsimused canvasesse, sest frame'i ei saa kerida
        self.canvas = Canvas(self, yscrollcommand = self.vscrollbar.set, height = 730)
        self.canvas.grid(row = 0, column = 0, sticky = N+E+S+W)
        self.vscrollbar.config(command = self.canvas.yview)


        #sellesse frame'i tulevad nupud ja spinbox küsimuste arvu muutmiseks
        self.sideFrame = Frame(self)
        self.sideFrame.grid(row = 0, column = 2, sticky = N+E+S+W)
        self.sideFrame.rowconfigure(3, weight = 1)
        #Vastuste kontrollimise nupp
        self.checkBtn = ttk.Button(self.sideFrame, text= "Vasta", command=self.checkAnswers)
        self.checkBtn.grid(row=0,column = 0, sticky = N+E+W, padx=10, pady=10)
        #küsimuste arvu valimise spinbox
        Label(self.sideFrame, text = 'Küsimuste arv(1-100):').grid(row = 1, column = 0, sticky = W, padx = 10)
        self.spinbox = Spinbox(self.sideFrame, from_ = 1, to = 100, validate = 'focus')
        self.spinbox.grid(row = 2, column = 0, padx = 10)
        #spinboxi defaultiks 10
        self.spinbox.delete(0, "end")
        self.spinbox.insert(0, 5)
        #akna sulgemise nupp
        ttk.Button(self.sideFrame, text= "Sulge", command=self.destroy).grid(row=3,column = 0, sticky = E+S+W, padx=10, pady=10)
        
        self.questions = questions
        
        #Kuvab etteantud küsimused
        self.displayQuestions()

        #et küsimuste kerimine töötaks hiire scroll wheeliga
        self.bind("<MouseWheel>", lambda e: self.canvas.yview("scroll",int(-e.delta/100),"units"))
        
        self.mainloop()

    def displayQuestions(self):
        '''Kuvab etteantud küsimused'''

        #Kui pole küsimusi, siis otsib ise nii mitu tükki, kui on arv spinboxis
        if not self.questions: self.questions = Question.getNextN(int(self.spinbox.get()))
        #Vastamise nupu ülesanne vaheldub "Vasta"<->"Järgmised küsimused"
        self.checkBtn['text'] = 'Vasta'
        self.checkBtn['command'] = self.checkAnswers

        #sellesse frame'i tulevad kõik küsimused, iga kord loob uue, et eelmised küsimused kaoksid
        self.questionsContainer = Frame(self.canvas)
        #self.questionFrames - list, mille elementideks QuestionFrame klassist objektid. Iga element esindab ühte küsimust.
        self.questionFrames = []
        
        #Käi küsimused läbi ja kuva igaüks omaette Frame'is
        for qNum, q in enumerate(self.questions):
            self.questionFrames.append(QuestionFrame(q, self.questionsContainer))
            self.questionFrames[qNum].grid(row = qNum + 1, column = 0, columnspan=2, sticky = N+E+W, padx = 10)

        #seab uued canvase mõõtmed uute küsimuste jaoks
        self.canvas.delete(ALL)
        self.canvas.create_window(0, 0, anchor=NW, window=self.questionsContainer)
        self.questionsContainer.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview('moveto', 0)
        self.canvas['width'] = self.questionsContainer.winfo_width()
        
    def checkAnswers(self):
        '''Kontrollib kõik kuvatud küsimuste vastused ja uuendab statistikat andmebaasis'''
        
        wrong = []
        n = 0
        #Vaatab üle kas on kõigile küsimustele vastatud       
        for questionFrame in self.questionFrames:
            n += 1
            if not questionFrame.Answer_given():
                wrong.append(n)
            
        if len(wrong) == 0:            
            
            self.checkBtn['text'] = 'Järgmised'
            self.checkBtn['command'] = lambda: self.displayQuestions()            

            for questionFrame in self.questionFrames:
                q = questionFrame.q
                q.tries+=1
                q.correct+=questionFrame.checkAnswers()
                #Uuendab andmebaasis küsimuse vastamiste ja õigesti vastamiste arvu
                q.update()
            #Hävitab praegused küsimused, displayQuestions nende asemel uued leiaks
            self.questions=[]
        else:
            #Annab kasutajale tead millistel küsimustele pole vastatud
            messagebox.showinfo(message = 'Vastus pole esitatud küsimustele {}'.format(wrong))
            self.focus()
            
class QuestionFrame(Frame):
    '''Kuvab ühe etteantud küsimuse omaette Frame's'''
    
    def __init__(self, q, master = None):
        Frame.__init__(self, master, bd = 2, relief="groove")
        self.q=q
      
        #Küsimuse tekst
        Label(self, text = q.question, font = "Helvetica 14 bold", wraplength = 800, justify = 'left').grid(row = 0,column = 0, columnspan = 2, sticky = W)

        ##Vastusevariandid
        self.checkBoxVals = []
        self.checkBoxes = []
        self.answers = q.getAnswers()
    
        for i, answer in enumerate(self.answers):
            self.checkBoxVals.append(IntVar())
            self.checkBoxes.append(
                Checkbutton(self,
                            variable = self.checkBoxVals[i],
                            text = answer.answer,
                            font = "Times 12",
                            wraplength = 400,
                            justify='left'))
            
            self.checkBoxes[i].grid(row=i+1, column=0, padx=(10,0), sticky = N+W)
            
        #Pilt
        if q.pic_name:
            self.path = 'images/' + q.pic_name
            self.photo = PhotoImage(file = self.path)
            Label(self, image = self.photo).grid(row = 1, column = 1, rowspan = len(self.answers), padx = 10, sticky = E)
            
        self.rowconfigure(len(self.answers), weight = 1)
        self.rowconfigure(0, pad = 20)
        
    def Answer_given(self):
        '''Vaatab üht küsimust, kas selle on vastatud või mitte, väljastav True/False'''
        answered = False
        for i, checkBoxVal in enumerate(self.checkBoxVals):            
            if checkBoxVal.get()==1:
                answered = True
                
        #tagastab, kas vastusele vastati või mitte
        return answered
    
    def checkAnswers(self):
        '''Kontrollib ühe küsimuse vaastused ja tagastab 0 või 1 vastavalt sellele, kas küsimuse vastamisel esines vigu või mitte'''
        correct = 1
        for i, checkBoxVal in enumerate(self.checkBoxVals):
            #punane, kui kasutaja valis vastuse, mis on vale
            if checkBoxVal.get()==1 and self.answers[i].value==0:
                self.checkBoxes[i]['bg']='red'
                correct = 0
            #kollane, kui kasutaja jättis valimata vastuse, mis on õige
            if checkBoxVal.get()==0 and self.answers[i].value==1:
                self.checkBoxes[i]['bg']='yellow'
                correct = 0
            #roheline kui kasutaja valis vastuse, mis on õige
            if checkBoxVal.get()==1 and self.answers[i].value==1:
                self.checkBoxes[i]['bg']='green'
                
        #tagastab, kas vastusele vastati õigesti või mitte, et andmebaasis statistikat uuendada
        return correct
