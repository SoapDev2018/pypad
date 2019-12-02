import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class MyPad:
	__root = Tk()
	
	__thisWidth = 300
	__thisHeight = 300
	__thisTextArea = Text(__root)
	__thisMenuBar = Menu(__root)
	__thisFileMenu = Menu(__thisMenuBar, tearoff=0) 
	__thisEditMenu = Menu(__thisMenuBar, tearoff=0) 
	__thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
	__thisSearchMenu = Menu(__thisMenuBar, tearoff=0)
	
	__thisScrollBar = Scrollbar(__thisTextArea)
	__file = None
	
	def __init__(self,**kwargs):
		try:
			self.__root.wm_iconbitmap("MyPad.ico")
		except:
			pass
		
		try:
			self.__thisWidth = kwargs['width']
		except KeyError:
			pass

		try:
			self.__thisHeight = kwargs['height']
		except KeyError:
			pass
			
		self.__root.title("Untitled - MyPad")
		
		screenWidth = self.__root.winfo_screenwidth()
		screenHeight = self.__root.winfo_screenheight()
		
		left = (screenWidth / 2) - (self.__thisWidth / 2)
		top = (screenHeight / 2) - (self.__thisHeight / 2)
		
		self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))
		
		self.__root.grid_rowconfigure(0, weight = 1)
		self.__root.grid_columnconfigure(0, weight = 1)
		
		self.__thisTextArea.grid(sticky = N + E + S + W) 
		self.__thisFileMenu.add_command(label = "New", command = self.__newFile, accelerator="Ctrl+N")
		self.__thisFileMenu.add_command(label = "Open", command = self.__openFile, accelerator="Ctrl+O")
		self.__thisFileMenu.add_command(label = "Save", command = self.__saveFile, accelerator="Ctrl+S")
		self.__thisFileMenu.add_separator()
		self.__thisFileMenu.add_command(label = "Exit", command = self.__quitApplication, accelerator="Ctrl+Z")
		self.__thisMenuBar.add_cascade(label = "File", menu = self.__thisFileMenu)
		self.__root.bind_all("<Control-n>", self.__newFile)
		self.__root.bind_all("<Control-o>", self.__openFile)
		self.__root.bind_all("<Control-s>", self.__saveFile)
		self.__root.bind_all("<Control-z>", self.__quitApplication)

		self.__thisEditMenu.add_command(label = "Undo", command = None)
		self.__thisEditMenu.add_command(label = "Redo", command = None)
		self.__thisEditMenu.add_separator()
		self.__thisEditMenu.add_command(label = "Cut", command = self.__cut, accelerator="Ctrl+X")
		self.__thisEditMenu.add_command(label = "Copy", command = self.__copy, accelerator="Ctrl+C")
		self.__thisEditMenu.add_command(label = "Paste", command = self.__paste, accelerator="Ctrl+V")
		self.__thisEditMenu.add_command(label = "Select All", command = None)
		self.__thisMenuBar.add_cascade(label = "Edit", menu = self.__thisEditMenu)
		self.__root.bind_all("<Control-x>", self.__cut)
		self.__root.bind_all("<Control-c>", self.__copy)
		self.__root.bind_all("<Control-v>", self.__paste)
		
		self.__thisSearchMenu.add_command(label = "Search", command = None)
		self.__thisSearchMenu.add_command(label = "Search & Replace", command = None)
		self.__thisMenuBar.add_cascade(label = "Search", menu = self.__thisSearchMenu)

		self.__thisHelpMenu.add_command(label = "About MyPad", command = self.__showAbout)
		self.__thisMenuBar.add_cascade(label = "?", menu = self.__thisHelpMenu)

		self.__root.config(menu=self.__thisMenuBar)

		self.__thisScrollBar.pack(side = RIGHT, fill = Y)

		self.__thisScrollBar.config(command = self.__thisTextArea.yview)
		self.__thisTextArea.config(yscrollcommand = self.__thisScrollBar.set)
		

	def __quitApplication(self,*args):
		self.__root.destroy()

	def __showAbout(self):
		showinfo("Notepad", "Original Author: Mrinal Verma, Modified By: Sayantan Chaudhuri")
		
	def __openFile(self,*args):
		self.__file = askopenfilename(defaultextension = ".txt", filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		if self.__file == "":
			self.__file = None
		else:
			self.__root.title(os.path.basename(self.__file) + " - MyPad")
			self.__thisTextArea.delete(1.0,END)
			file = open(self.__file,"r")
			self.__thisTextArea.insert(1.0,file.read())
			file.close()
			
	def __newFile(self,*args): 
		self.__root.title("Untitled - MyPad") 
		self.__file = None
		self.__thisTextArea.delete(1.0,END) 
		
	def __saveFile(self,*args):
		if self.__file == None:
			self.__file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension = ".txt", filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
			
			if self.__file == "":
				self.__file = None
			else:
				file = open(self.__file,"w")
				file.write(self.__thisTextArea.get(1.0,END))
				file.close()
				self.__root.title(os.path.basename(self.__file) + " - MyPad")
		else:
			file = open(self.__file,"w")
			file.write(self.__thisTextArea.get(1.0,END))
			file.close()
			
	def __cut(self,*args):
		self.__thisTextArea.event_generate("<<Cut>>")
		
	def __copy(self,*args):
		self.__thisTextArea.event_generate("<<Copy>>")
		
	def __paste(self,*args):
		self.__thisTextArea.event_generate("<<Paste>>")
		
	def run(self):
		self.__root.mainloop()


mypad = MyPad(width=600,height=400)
mypad.run()