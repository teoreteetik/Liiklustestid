##Innar Hallik ja Lembit Gerz
##inf1

from tkinter import *
from tkinter import ttk
from tkinter.tix import *
from questionsGUI import *
from overviewGUI import *

app = Tk()
app.title('Liiklusteooria')

Label(text = 'Liiklusteooria testid').grid(row=0, column = 0, padx=50, pady=30)

testBtn = ttk.Button(app, text = 'Alusta testi', command = QuestionsGUI)
testBtn.grid(row = 1, column = 0, sticky = N+E+S+W, padx = 10)

resultsBtn = ttk.Button(app, text = 'Tulemused', command = OverviewGUI)
resultsBtn.grid(row = 2, column = 0, sticky = N+E+S+W, padx=10)

quitBtn = ttk.Button(app, text = 'Sulge', command = app.destroy)
quitBtn.grid(row = 3, column = 0, sticky = N+E+S+W, padx = 10, pady = (0,10))

app.mainloop()
