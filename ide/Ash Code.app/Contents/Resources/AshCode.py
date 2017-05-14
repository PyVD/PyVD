from Tkinter import *
import tkFileDialog as fd
import tkMessageBox
import sys
import os
import glob
import platform
import urllib
import getpass

class MainApplication():
	def __init__(self, baseTitle, sw, sh):
		if sw < 200:
			print("Window too small!")
			exit()
		self.highlights = 0
		self.prev = ""
		self.ft = []
		self.root = Tk()
		self.filename = "Untitled"
		if platform.system() != "Windows":
			self.dirname = "/Users/"+getpass.getuser()+"/Desktop"
		elif platform.system() == "Windows":			
			self.dirname = "\\Users\\"+getpass.getuser()+"\\Desktop"
		self.baseTitle = baseTitle
		self.updateTitle()
		self.root.config(bg="#000000")
		self.root.minsize(sw, sh)
		self.root.maxsize(sw, sh)
		self.root.resizable(False, False)

		self.filetree = Frame(self.root, width=200)
		self.filetree.config(background="#ffffff")

		self.files = Frame(self.filetree, width=200)

		self.textframe = Frame(self.root)
		self.text = Text(self.textframe, width=sw-200, height=sh)
		self.textframe.config(highlightthickness=0, bg="#34495e")
		self.text.config(padx=5, tabs="32", highlightthickness=0, bg="#34495e", fg="white", insertbackground="white", font=("Consolas", 12))

		self.text.bind("<KeyRelease>", self.check)
		self.root.bind("<Configure>", self.__screen)

		# The "File" Menu

		self.menu = Menu(self.root)
		self.filemenu = Menu(self.menu)
		self.filemenu.add_command(label="Open", command=self.open_folder)
		self.filemenu.add_command(label="Save", command=self.save_file)
		self.filemenu.add_command(label="Save As", command=self.save_As)
		self.filemenu.add_command(label="New", command=self.new_file)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Run with Python 2", command=self.run2)
		self.filemenu.add_command(label="Run with Python 3", command=self.run3)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Close", command=sys.exit)

		# The "Edit" Menu

		self.editmenu = Menu(self.root)
		self.editmenu.add_command(label="Add Ash Import Definitions", command=self.add_defs)
		self.editmenu.add_command(label="Use Default Project", command=self.use_default)
		self.editmenu.add_separator()
		self.editmenu.add_command(label="Copy")
		self.editmenu.add_command(label="Cut")
		self.editmenu.add_command(label="Paste")
		self.editmenu.add_separator()
		self.editmenu.add_command(label="Install CofeePy", command=self.installcofee)

		# The "Help" Menu

		self.helpmenu = Menu(self.root)
		self.helpmenu.add_command(label="How To")
		self.helpmenu.add_separator()		
		self.helpmenu.add_command(label="About")

		# Adding Menu Items
		self.menu.add_cascade(label="File", menu=self.filemenu)
		self.menu.add_cascade(label="Edit", menu=self.editmenu)
		self.menu.add_cascade(label="Help", menu=self.helpmenu)

		# Setting The Root Window Menu
		self.root.config(menu=self.menu)
	def updateTitle(self):
		self.root.title(self.filename+" - "+self.baseTitle)
	def exec_(self):
		self.filetree.pack(side=LEFT, fill=Y)
		self.files.pack(side=TOP, fill=Y)
		self.textframe.pack(side=RIGHT, fill=Y)
		self.text.pack(fill=Y)
		self.root.mainloop()
	def __screen(self, event):
		return
	def add_defs(self):
		self.text.insert(0.0, "from ash.gui import Gui\nfrom ash.core import AshApplication\n")
	def use_default(self):
		self.text.delete(0.0, END)
		self.add_defs()
		self.text.insert(END, "\ngui = Gui()\napp = AshApplication(\"Hello, World!\")\nitem = gui.label()")
	def open_folder(self):
		fn = fd.askdirectory(title="Open Folder")
		self.files = Frame(self.filetree, width=200)

		self.dirname = fn
		self.ft = []
		cwd = os.getcwd()
		os.chdir(self.dirname)
		self.lbls = []
		for f in glob.glob("*"):
			self.ft.append(f)
			self.lbls.append(Label(self.files, text=f))
			self.lbls[len(self.lbls)-1].config(foreground="#000000")
			num = len(self.ft)-1
			self.lbls[len(self.lbls)-1].bind("<Button-1>", self.makeClosure(f, self.lbls[len(self.lbls)-1]))
			self.lbls[len(self.lbls)-1].pack()
		os.chdir(cwd)
		self.files.pack(side=TOP, fill=Y)
	def run2(self):
		try:
			direct = os.path.join(self.dirname, self.filename)
			if platform.system() == "Windows":
				os.system("C:\\Python27\\python.exe "+direct)
			else:
				os.system("python2.7 "+direct)
		except Exception, e:
			tkMessageBox.showwarning(
            	"Error 007",
            	"Cannot run this file!"
        	)
	def run3(self):
		try:
			direct = os.path.join(self.dirname, self.filename)
			if platform.system() == "Windows":
				os.system("C:\\Python35\\python.exe "+direct)
			else:
				os.system("python3 "+direct)
		except Exception, e:
			tkMessageBox.showwarning(
            	"Error 007",
            	"Cannot run this file!"
        	)
	def makeClosure(self, f, lbl):
		return lambda event: self.open_high(f, lbl)
	def open_file(self, fn):
		self.filename = fn
		path = os.path.join(self.dirname, fn)
		f = open(path, "r")
		self.text.delete(0.0, END)
		self.text.insert(0.0, f.read(), END)
		f.close()
		self.updateTitle()
	def open_high(self, f, lbl):
		if self.prev != "":
			self.prev.config(background="#ffffff")
		self.open_file(f)
		lbl.config(background="#dddddd")
		self.prev = lbl
	def installcofee(self):
		if os.path.exists(os.path.join(self.dirname, "Cofee")) == False:
			cwd = os.getcwd()
			os.chdir(self.dirname)
			os.system("git clone https://github.com/CofeePy/Cofee.git")
			os.chdir(cwd)
	def save_file(self):
		if self.filename != "Untitled":
			try:
				direct = os.path.join(self.dirname, self.filename)
				f = open(direct, "w")
				f.write(self.text.get(0.0, END).rstrip())
				f.close()
			except Exception, e:
				tkMessageBox.showwarning(
	            	"Error 009",
	            	"Cannot save this file!"
	        	)
		else:
			self.save_As()
	def save_As(self):
		self.filename = fd.asksaveasfilename(filetypes=(("Python Files", "*.*"), ("Python Files", "*.pyw"), ("All Files", "*.*")))
		self.save_file()
		self.updateTitle()
		self.updateFileTree()
	def new_file(self):
		self.text.delete(0.0, END)
		self.filename = "Untitled"
		self.updateTitle()
		if self.prev != "":
			self.prev.config(background="#ffffff")
	def highlight(self, seq, bg, fg, font):
		self.highlights += 1
		if "highlight" in self.text.tag_names():
			content = self.text
			self.text.tag_delete(content,"highlight"+str(self.highlights))
		i = len(seq)
		index = "1.0"
		while True:
			index = self.text.search(seq, index, nocase=1, stopindex='end')
			if index:
				index2 = self.text.index("%s+%dc" % (index, i))
				self.text.tag_add('highlight'+str(self.highlights), index, index2)
				if font == "":
					self.text.tag_configure('highlight'+str(self.highlights), background=bg, foreground=fg)
				else:
					self.text.tag_configure('highlight'+str(self.highlights), font=font, background=bg, foreground=fg)
				index = index2
			else:
				return
	def check(self, event):
		if self.text.get(0.0, END).rstrip() != "":
			self.highlight("import", "#34495e", "red", "")
			self.highlight("if", "#34495e", "red", "")
			self.highlight("elif", "#34495e", "red", "")
			self.highlight("else", "#34495e", "red", "")
			self.highlight("for", "#34495e", "red", "")
			self.highlight("return", "#34495e", "red", "")
			self.highlight("print", "#34495e", "red", "")
			self.highlight("in", "#34495e", "red", "")
			ftxt = self.text.get(0.0, END).rstrip().split("\n")
			txt = []
			for item in ftxt:
				for ite in item.split(" "):
					for it in ite.split("\t"):
						if it != "":
							txt.append(it)

			for word in txt:
				if word != "import" and word != "if" and word != "elif" and word != "else" and word != "for" and word != "while" and word != "in" and word != "print" and word != "return":
					self.highlight(word, "#34495e", "#ffffff", "")
	def updateFileTree(self):
		self.files = Frame(self.filetree, width=200)
		self.ft = []
		cwd = os.getcwd()
		os.chdir(self.dirname)
		self.lbls = []
		for f in glob.glob("*"):
			self.ft.append(f)
			self.lbls.append(Label(self.files, text=f))
			self.lbls[len(self.lbls)-1].config(foreground="#000000")
			num = len(self.ft)-1
			self.lbls[len(self.lbls)-1].bind("<Button-1>", self.makeClosure(f, self.lbls[len(self.lbls)-1]))
			self.lbls[len(self.lbls)-1].pack()
		os.chdir(cwd)
		self.files.pack(side=TOP, fill=Y)
app = MainApplication("Ash Code", 800, 600)
app.exec_()