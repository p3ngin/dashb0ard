#!/usr/bin/python3
from tkinter import *
import sys
import os
import MySQLdb
import datetime

''' TABLE chores (chore TEXT, inputdate DATE, duedate DATE, completed BOOL '''

db = MySQLdb.connect("192.168.1.8", "DBUSER", "PASSWORD", "dashboard")
curs = db.cursor()

sqlA = "INSERT INTO chores values('"

class Dashboard:
	def __init__(self, master):
		self.master = master
		self.master.configure(bg='#EBEBEB')
		self.frame = Frame(self.master, bg='#EBEBEB')

		self.master.title("Dashboard")
		self.master.minsize(width=250, height=225)

		date1 = ("Date:  " + str(datetime.date.today()))

		self.labelDate = Label(self.frame, relief=RIDGE, bg='#E0E0E0', text=date1)
		self.labelDate.grid(column=0, row=0, sticky=W)

		self.labeltd = Label(self.frame, bg='#EBEBEB', text='----------------To-Do----------------')
		self.labeltd.grid(column=0, row=1, columnspan=4, pady=7)

		self.labelR = Label(self.frame, bg='#EBEBEB', text='Chore assigned for today: ')
		self.labelR.grid(column=0, row=2, sticky=E)

		self.randChore = self.randChore()

		self.labelRchore = Label(self.frame, relief=RIDGE, text=self.randChore, bg='red', fg='white')
		self.labelRchore.grid(column=1, row=2, columnspan=3, stick=W)

		self.button1 = Button(self.frame, text='Edit Chores', width=10, command=self.new_window)
		self.button1.grid(column=0, row=3, sticky=W, pady=75)

		self.frame.pack()

	def randChore(self):
		curs.execute("SELECT chore FROM chores ORDER BY RAND() LIMIT 1")
		db.commit()

		curs.fetchone
		rChore = str(curs.fetchone()[0])
		return rChore

	def new_window(self):
		self.newWindow = Toplevel(self.master)
		self.app = Chore(self.newWindow)

class Chore:
	def __init__(self, master):
		self.master = master
		self.frame = Frame(self.master)

		self.master.title("Chore Input")
		self.master.minsize(width=350, height=250)

		self.label1 = Label(self.frame, text="Input chore: ")
		self.label1.grid(row=0, column=0, sticky=E)

		self.label2 = Label(self.frame, text="Total list of chores: ")
		self.label2.grid(row=1, column=0, sticky=NE)

		self.c1 = Entry(self.frame)
		self.c1.grid(row=0, column=1, sticky=W)

		self.buttonAdd = Button(self.frame, text="add", command=self.add)
		self.buttonAdd.grid(row=0, column=2)

		self.listbox = Listbox(self.frame)
		self.listbox.grid(row=1, column=1, columnspan=3, sticky=W, pady=5)

		self.buttonShowAll = Button(self.frame, text="Show All", command=self.showAll)
		self.buttonShowAll.grid(row=2, column=1, sticky=W)

		self.buttonDelete = Button(self.frame, text="Delete Selected", command=self.deleteChore)
		self.buttonDelete.grid(row=2, column=2, sticky=E)
		self.frame.pack()
		self.showAll()

	def add(self):
		self.chore1 = self.c1.get()

		sqlAdd = (sqlA + self.chore1 + "', NOW(), CURRENT_DATE() + INTERVAL 1 DAY, 0)")

		if len(self.chore1) == 0:
			self.labelEmpty = Label(self.frame, text="*", fg="red")
			self.labelEmpty.grid(row=0, column=4)
			return 0
		else:
			print(self.c1.get())
			curs.execute(sqlAdd)
			db.commit()

			self.showAll()

	def showAll(self):
		self.c1.delete(0, 'end')
		self.c1.focus()
		
		self.listbox.delete(0, END)

		curs.execute("SELECT * FROM chores")
		db.commit()

		for reading in curs.fetchall():
			line = str(reading[0])
			self.listbox.insert(END, line)

	def deleteChore(self):
		selection = self.listbox.curselection()
		value = self.listbox.get(selection[0])
		print(value)

		sqlDelete = ("DELETE from chores where chore ='" + value + "'")
		
		curs.execute(sqlDelete)
		db.commit()

		self.showAll()

	def close_windows(self):
		self.master.destroy()

def main():
	root = Tk()
	app = Dashboard(root)
	root.mainloop()

if __name__ == '__main__':
	main()
