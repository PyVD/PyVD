from Tkinter import *
import tkFileDialog as fd
import sys
import os
import glob
import platform
import urllib

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
		self.dirname = ""
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

		self.root.bind("<Configure>", self.__screen)

		# The "File" Menu

		self.menu = Menu(self.root)
		self.filemenu = Menu(self.menu)
		self.filemenu.add_command(label="Open", command=self.open_folder)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Run")
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
		self.text.delete(0.0)
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
			print(f)
			self.ft.append(f)
			self.lbls.append(Label(self.files, text=f))
			self.lbls[len(self.lbls)-1].config(foreground="#000000")
			num = len(self.ft)-1
			self.lbls[len(self.lbls)-1].bind("<Button-1>", self.makeClosure(f, self.lbls[len(self.lbls)-1]))
			self.lbls[len(self.lbls)-1].pack()
		os.chdir(cwd)
		self.files.pack(side=TOP, fill=Y)
	def run(self):
		for f in self.ft:
			os.chdir("ash")
			os.system("./ash "+self.dirname)
	def makeClosure(self, f, lbl):
		return lambda event: self.open_high(f, lbl)
	def open_file(self, fn):
		self.filename = fn
		path = os.path.join(self.dirname, fn)
		f = open(path, "r")
		self.text.delete(0.0, END)
		self.text.insert(0.0, f.read(), END)
		f.close()
	def open_high(self, f, lbl):
		if self.prev != "":
			self.prev.config(background="#ffffff")
		self.open_file(f)
		lbl.config(background="#dddddd")
		self.prev = lbl
	def installcofee(self):
		cwd = os.getcwd()
		os.chdir(self.dirname)
		os.system("git clone https://github.com/CofeePy/Cofee.git")
		os.chdir(cwd)
app = MainApplication("Ash Code", 800, 600)
app.exec_()