#!/usr/bin/env python
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import messagebox
import sys
import os
from resume_parser import parse_resumes
from package_parser import parse_promotion_packages

class GUIFramework(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.master.title('Resume Ranker')
        top=self.winfo_toplevel()
        self.grid(padx=15, pady=15, sticky=N+S+E+W)
        self.InitResizing()
        self.CreateWidgets()

    def InitResizing(self):
        top= self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(6, weight=1)

    def CreateWidgets(self):
        self.lbText= Label(self, text='Enter PDF Filename')
        self.lbText.pack()

        self.enText= Entry(self)
        self.enText.pack(side=TOP)

        ##TODO: add entry for keyowrds file name. The Run ranker should set the keyword list to this file


        self.btnParsePackage = Button(self,text = 'Parse Packages', command=self.ParsePackagePDF)
        self.btnParsePackage.pack(side=RIGHT, padx=10, pady=10)

        self.btnParseResume = Button(self, text = 'Parse Resumes', command=self.ParseResumePDF)
        self.btnParseResume.pack(side=LEFT, padx =10, pady=10)

        self.btnRanker = Button(self, text ='Run Ranker', command=self.CallResumeRank)
        self.btnRanker.pack(side=BOTTOM)

    def CallResumeRank(self):
        try:
            os.system('python resume_ranker.py')
            messagebox.showinfo('Status', 'Ranking Complete')
        except:
            messagebox.showinfo('Status', 'Something Went Wrong')

    def ParseResumePDF(self):
        try:
            file =self.enText.get()
            parse_resumes(file)
            messagebox.showinfo('Status', 'Parsing Complete')
        except:
            messagebox.showinfo('Status', 'Something went wrong')

    def ParsePackagePDF(self):
        try:
            file =self.enText.get()
            parse_promotion_packages(file)
            messagebox.showinfo('Status', 'Parsing Complete')
        except:
            messagebox.showinfo('Status', 'Something went wring')




if __name__ == "__main__":
    guiFrame = GUIFramework()
    guiFrame.mainloop()
