from tkinter import filedialog
from tkinter import *
from helper import *
import re

window = Tk()
window.title("Database Migrator")
window.geometry("800x800")

var = IntVar()
filename1 =""
def browse():
	global filename1
	filename1 = filedialog.askopenfilename()
	e.delete(0,END)
	e.insert(0,filename1)

def convert():
	global filename1
	print(filename1)
	f = open(filename1,"r")
	if var.get() == 2:
		pg = pgsql2mysql(f)
	else:
		pg = mysql2pgsql(f)
	text.delete('1.0',END)
	text.insert(INSERT, pg)	
 
def save():
	 f = filedialog.asksaveasfilename(filetypes=(("sql file","*.sql"),("backup file","*.bak")))
	 if f is None:
	 	return
	 text2save = str(text.get(1.0, END))
	 fp = open(f,"w")
	 fp.write(text2save)
	 fp.close()
                
Label(text="Welcome to Database Migrator.\n",font=("Times New Roman", 20)).place(x=50,y=4)

Radiobutton(window, text="MySQL to PgSQL", variable=var, value=1).place(x=50,y=50)
Radiobutton(window, text="PgSQL to MySQL", variable=var, value=2).place(x=200,y=50)
e = Entry(window, bd=5)
e.place(x=60,y=100)
Button(text="Browse", command=browse).place(x=230,y=100)
Button(text="Convert", command=convert,bg="red").place(x=130,y=130)
text = Text(master=window, height=35, width=100)
text.place(x=5,y=180)
Button(text="Save As", command=save).place(x=5,y=675)

window.mainloop()
