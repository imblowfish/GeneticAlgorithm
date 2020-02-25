#from graphics import *
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
	FigureCanvasTkAgg, 
	NavigationToolbar2Tk
)
from matplotlib.figure import Figure
from random import *

class Interface:
	root = None
	buttons = []
	textboxes = []
	radiobuttons = []
	labels = []
	
	def __init__(self, size):
		self.root = tk.Tk()
		self.root.wm_title("Лабораторная 1")
		self.root.geometry(size)
	def start(self):
		tk.mainloop()
	#-------------------------------------------------
	def add_graphic(self,width, height, pos_x, pos_y):				#добавление графика
		fig = Figure(figsize=(width,height),dpi=100)
		ax = fig.add_subplot(111, projection='3d')
		canvas = FigureCanvasTkAgg(fig, master=self.root)
		canvas.get_tk_widget().place(x=pos_x, y=pos_y)
		canvas.draw()
		return canvas
	#-----------------------------------------------------------
	def draw_graphic(self, canvas, title, xlabel, ylabel, zlabel, x, y, z):	#рисование значений на графике
		ax = canvas.figure.axes[0]
		ax.clear()
		ax.plot(x, y, z, alpha=0.5)
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)
		ax.set_zlabel(zlabel)
		ax.set_title(title)
		for item in ([ax.title, ax.xaxis.label, ax.yaxis.label, ax.zaxis.label] + ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()):
			item.set_fontsize(6)
		canvas.draw()
	#---------------------------------
	def draw_dots(self, canvas, dots):										#рисование точек на графике
		ax = canvas.figure.axes[0]
		if(len(dots) == 1):
			ax.scatter(dots[0][0], dots[0][1], dots[0][2], c="#00FF00", s=20)
			
		else:
			for i in dots:
				ax.scatter(i[0], i[1], i[2], c="#FF0000", s=10)
		canvas.draw()
	#------------------------------------------------------
	def add_button(self, text, pos_x, pos_y, command=None):
		b = tk.Button(self.root, text=text, font=("Helvetica","8"), command=command)
		b.place(x=pos_x, y=pos_y)
		self.buttons.append(b)
		return b
	#---------------------------------------
	def add_label(self, text, pos_x, pos_y):	
		l = tk.Label(self.root, text=text, font=("Helvetica","8"))
		l.place(x=pos_x, y=pos_y)
		self.labels.append(l)
		return l
	#--------------------------------------------------------
	def add_textbox(self, width, height, text, pos_x, pos_y):
		tb = tk.Text(self.root, width=width, height=height, font=("Helvetica","8"))
		tb.insert(tk.END, text)
		tb.place(x=pos_x, y=pos_y)
		self.textboxes.append(tb)
		return tb
	#-----------------------------------
	def add_radiobutton(self, elements):
		rbuttons = []
		for i in elements:
			r = tk.Radiobutton(text=i["text"])
			r.place(x=i["x"], y=i["y"])
			rbuttons.append(r)
			self.radiobuttons.append(r)
		return rbuttons
	#----------------------------------	
	def update_textbox(self, tb, text):
		tb.insert(tk.END, text)
		tb.see(tk.END)
	#---------------------------
	def clear_textbox(self, tb):
		tb.delete(1.0, tk.END)
	#-----------------------------------
	def get_text_from_textbox(self, tb):
		return tb.get(1.0, tk.END)
#---Interface END---
			
	
		
	