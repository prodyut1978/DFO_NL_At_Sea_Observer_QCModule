import sys
from tkinter import *
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
import numpy as np
import pandas as pd
import sqlite3
import time

from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_RunRangeValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_CalenderVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_PositionalVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_GearVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_CatchVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_Misc_Support


def SetCatch_ViewRangeVariablesValidatedResult():
    root=tk.Toplevel()
    root.title ("DFO-NL-ASOP Variable Range Validation QC - ID-C-02")
    root.geometry('1085x690+400+100')
    root.config(bg="aliceblue")
    Topframe = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")

    lbl_Total_QCEntries = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Entries For QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCEntries.grid(row =0, column = 0, padx=4, pady =2)
    Set_Catch_TotalEntries =DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_Entries()  
    Total_QC_Entries = IntVar(Topframe, value=Set_Catch_TotalEntries)
    entry_Total_QCEntries = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Entries, width = 8, bd=2)
    entry_Total_QCEntries.grid(row =0, column = 1, padx=1, pady =5)

    Topframe.pack(side = TOP)
    Midframe = Frame(root, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
    Midframe.pack(side = TOP)

    ## Get File Name Imported File
    ImportedFileName = DFO_NL_ASOP_Misc_Support.GetPickledImportedFileName()
    ImportedFileName = ImportedFileName.split(",")
    ImportedFileName =(ImportedFileName[0])
    TextString =  '( File Name : ' + ImportedFileName + ' )'
    lblHeader = Label(Midframe, font=('aerial', 12, 'bold'), 
                text=("  ** Simple QC & Validation Summary- ID-C-02 : Variable Range QC  **  ") + '\n' + TextString,
                bg="aliceblue")
    lblHeader.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
    
    TableMargin1 = Frame(root, bd = 2, padx= 2, pady= 2, relief = RIDGE, bg="aliceblue")
    TableMargin1.pack(side=TOP)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4", "column5"), height=0, show='headings')
    tree1.heading("#1", text="ID-C-02", anchor=CENTER)
    tree1.heading("#2", text="QC Variables Name", anchor=CENTER)
    tree1.heading("#3", text="Total QC Failed", anchor=CENTER)
    tree1.heading("#4", text="View Failed Results & Update Set & Catch DB", anchor=CENTER)
    tree1.heading("#5", text="QC Variables Range Details", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=55)       
    tree1.column('#2', stretch=NO, minwidth=0, width=180)            
    tree1.column('#3', stretch=NO, minwidth=0, width=160)
    tree1.column('#4', stretch=NO, minwidth=0, width=370)
    tree1.column('#5', stretch=NO, minwidth=0, width=300)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'),background ="aliceblue", foreground='black')
    tree1.pack()
    QCFrame = Frame(TableMargin1, bd = 2, padx= 0, pady= 5, relief = RIDGE, bg="white")
    QCFrame.pack(side = LEFT)

    QCFailed_CalenderVariables = DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_CalenderVariables()
    QCFailed_PositionalVariables = DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_PositionalVariables()
    QCFailed_GearVariables = DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearVariables()
    QCFailed_CatchVariables = DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_CatchVariables()
    
    def SimpleQC_RangeValidation_CalenderVariables():

        def QCFailed_CalenderVariablesResultViewer():
            QCFailed_CalenderVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_CalenderVariables())
            QCFailed_CalenderVariables =int(QCFailed_CalenderVariables)
            if QCFailed_CalenderVariables>0:
                    DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_CalenderVariables.ViewRangeValidatedResult_CalenderVariables()
            else:
                tkinter.messagebox.showinfo("Calender Variables Table Range Validation Message",
                "Calender Variables Table Range Validation All Passed. *** All Calender Variables Table Range \
                in The Set & Catch Import are Validated Against Calender Variables Table Range Table ****")

        entryID_CalenderVariables = IntVar(QCFrame, value=0)
        entry_entryID_CalenderVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_CalenderVariables, width = 3, bd=2)
        entry_entryID_CalenderVariables.grid(row =0, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_CalenderVariables = Listbox(QCFrame, font=('aerial', 10, 'bold'), height =5, width =22)
        List_entryID_CalenderVariables.insert(1, " Year")
        List_entryID_CalenderVariables.insert(2, " Day")
        List_entryID_CalenderVariables.insert(3, " Month")
        List_entryID_CalenderVariables.insert(4, " HaulDay")
        List_entryID_CalenderVariables.insert(5, " HaulMonth")
        List_entryID_CalenderVariables.grid(row =0, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_CalenderVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_CalenderVariables())
        QCFailed_CalenderVariables =int(QCFailed_CalenderVariables)
        entryQCFailed_Calender = IntVar(QCFrame, value=QCFailed_CalenderVariables)
        entry_QCFailed_CalenderVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_Calender, width = 10, bd=2)
        entry_QCFailed_CalenderVariables.grid(row =0, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedCalenderVariables = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-C-02-0)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_CalenderVariablesResultViewer)
        btnViewQCFailedCalenderVariables.grid(row =0, column = 3, padx=60, pady =2, sticky =W)

        RangeDetails_CalenderVariables = Listbox(QCFrame, font=('aerial', 9), height =5, width =40)
        RangeDetails_CalenderVariables.insert(1, " Year : 1984 To Current - No Blank")
        RangeDetails_CalenderVariables.insert(2, " Day : 1 - 31 - No Blank")
        RangeDetails_CalenderVariables.insert(3, " Month : 1 - 12 - No Blank")
        RangeDetails_CalenderVariables.insert(4, " HaulDay : 1 - 31 - No Blank")
        RangeDetails_CalenderVariables.insert(5, " HaulMonth : 1 - 12 - No Blank")
        RangeDetails_CalenderVariables.grid(row =0, column = 4, padx=1, pady =2, ipady = 5, sticky =W)
            
    def SimpleQC_RangeValidation_PositionalVariables():
        
        def QCFailed_PositionalVariablesResultViewer():
            QCFailed_PositionalVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_PositionalVariables())
            QCFailed_PositionalVariables =int(QCFailed_PositionalVariables)
            if QCFailed_PositionalVariables>0:
                    DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_PositionalVariables.ViewRangeValidatedResult_PositionalVariables()
            else:
                tkinter.messagebox.showinfo("Positional Variables Table Range Validation Message",
                "Positional Variables Table Range Validation All Passed. *** All Positional Variables Table Range \
                in The Set & Catch Import are Validated Against Positional Variables Table Range Table ****")

        entryID_PositionalVariables = IntVar(QCFrame, value=1)
        entry_entryID_PositionalVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_PositionalVariables, width = 3, bd=2)
        entry_entryID_PositionalVariables.grid(row =2, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_PositionalVariables = Listbox(QCFrame, font=('aerial', 10, 'bold'), height =6, width =22)
        List_entryID_PositionalVariables.insert(1, " PositionPrecision")
        List_entryID_PositionalVariables.insert(2, " StartLatitude")
        List_entryID_PositionalVariables.insert(3, " StartLongitude")
        List_entryID_PositionalVariables.insert(4, " EndLatitude")
        List_entryID_PositionalVariables.insert(5, " EndLongitude")
        List_entryID_PositionalVariables.insert(6, " InOut200MileLimit")
        List_entryID_PositionalVariables.grid(row =2, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_PositionalVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_PositionalVariables())
        QCFailed_PositionalVariables =int(QCFailed_PositionalVariables)
        entryQCFailed_Positional = IntVar(QCFrame, value=QCFailed_PositionalVariables)
        entry_QCFailed_PositionalVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_Positional, width = 10, bd=2)
        entry_QCFailed_PositionalVariables.grid(row =2, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedPositionalVariables = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-C-02-1)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_PositionalVariablesResultViewer)
        btnViewQCFailedPositionalVariables.grid(row =2, column = 3, padx=60, pady =2, sticky =W)

        RangeDetails_PositionalVariables = Listbox(QCFrame, font=('aerial', 9), height =6, width =40)
        RangeDetails_PositionalVariables.insert(1, " PositionPrecision : 1 or 2 - No Blank")
        RangeDetails_PositionalVariables.insert(2, " StartLatitude : 3900 To 7500 - No Blank")
        RangeDetails_PositionalVariables.insert(3, " StartLongitude : 4200 To 7500 - No Blank")
        RangeDetails_PositionalVariables.insert(4, " EndLatitude : 3900 To 7500 - No Blank")
        RangeDetails_PositionalVariables.insert(5, " EndLongitude : 4200 To 7500 - No Blank")
        RangeDetails_PositionalVariables.insert(6, " InOut200MileLimit : 1 or 2 - No Blank")
        RangeDetails_PositionalVariables.grid(row =2, column = 4, padx=1, pady =2, ipady = 5, sticky =W)

    def SimpleQC_RangeValidation_GearVariables():

        def QCFailed_GearVariablesResultViewer():
            QCFailed_GearVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearVariables())
            QCFailed_GearVariables =int(QCFailed_GearVariables)
            if QCFailed_GearVariables>0:
                    DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_GearVariables.ViewRangeValidatedResult_GearVariables()
            else:
                tkinter.messagebox.showinfo("Gear Variables Table Range Validation Message",
                "Gear Variables Table Range Validation All Passed. *** All Gear Variables Table Range \
                in The Set & Catch Import are Validated Against Gear Variables Table Range Table ****")
        
        entryID_GearVariables = IntVar(QCFrame, value=2)
        entry_entryID_GearVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_GearVariables, width = 3, bd=2)
        entry_entryID_GearVariables.grid(row =4, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_GearVariables = Listbox(QCFrame, font=('aerial', 10, 'bold'), height =6, width =22)
        List_entryID_GearVariables.insert(1, " RollerBobbbinDiameter")
        List_entryID_GearVariables.insert(2, " NumberGillnets")
        List_entryID_GearVariables.insert(3, " AverageGillnetLength")
        List_entryID_GearVariables.insert(4, " GrateBarSpacing")
        List_entryID_GearVariables.insert(5, " NumberPots")
        List_entryID_GearVariables.insert(6, " NumberPotReleasedCrab")
        List_entryID_GearVariables.grid(row =4, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_GearVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearVariables())
        QCFailed_GearVariables =int(QCFailed_GearVariables)
        QCFailed_Gear = IntVar(QCFrame, value=QCFailed_GearVariables)
        entry_QCFailed_GearVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_Gear, width = 10, bd=2)
        entry_QCFailed_GearVariables.grid(row =4, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedGearVariables = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-C-02-2)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_GearVariablesResultViewer)
        btnViewQCFailedGearVariables.grid(row =4, column = 3, padx=60, pady =2, sticky =W)

        RangeDetails_GearVariables = Listbox(QCFrame, font=('aerial', 9), height =6, width =40)
        RangeDetails_GearVariables.insert(1, " RollerBobbbinDiameter : 20 To 95 - If Not Blank")
        RangeDetails_GearVariables.insert(2, " NumberGillnets : 0 To 650 - If Not Blank")
        RangeDetails_GearVariables.insert(3, " AverageGillnetLength : 30 To 100 - If Not Blank")
        RangeDetails_GearVariables.insert(4, " GrateBarSpacing : 17 To 50 - If Not Blank")
        RangeDetails_GearVariables.insert(5, " NumberPots : 0 To 350 - If Not Blank")
        RangeDetails_GearVariables.insert(6, " NumberPotReleasedCrab : 0 To 350 - If Not Blank")
        RangeDetails_GearVariables.grid(row =4, column = 4, padx=1, pady =2, ipady = 5, sticky =W)

    def SimpleQC_RangeValidation_CatchVariables():

        def QCFailed_CatchVariablesResultViewer():
            QCFailed_CatchVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_CatchVariables())
            QCFailed_CatchVariables =int(QCFailed_CatchVariables)
            if QCFailed_CatchVariables>0:
                DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_CatchVariables.ViewRangeValidatedResult_CatchVariables()
            else:
                tkinter.messagebox.showinfo("Catch Variables Table Range Validation Message",
                "Catch Variables Table Range Validation All Passed. *** All Catch Variables Table Range \
                in The Set & Catch Import are Validated Against Catch Variables Table Range Table ****")
        
        entryID_CatchVariables = IntVar(QCFrame, value=3)
        entry_entryID_CatchVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_CatchVariables, width = 3, bd=2)
        entry_entryID_CatchVariables.grid(row =6, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_CatchVariables = Listbox(QCFrame, font=('aerial', 10, 'bold'), height =6, width =22)
        List_entryID_CatchVariables.insert(1, " RecordType")
        List_entryID_CatchVariables.insert(2, " AverageTowSpeed")
        List_entryID_CatchVariables.insert(3, " KeptWeight")
        List_entryID_CatchVariables.insert(4, " DiscardWeight")
        List_entryID_CatchVariables.insert(5, " NumberIndividuals")
        List_entryID_CatchVariables.insert(6, " NumberWindows")
        List_entryID_CatchVariables.grid(row =6, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_CatchVariables = (DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_CatchVariables())
        QCFailed_CatchVariables =int(QCFailed_CatchVariables)
        QCFailed_Catch = IntVar(QCFrame, value=QCFailed_CatchVariables)
        entry_QCFailed_CatchVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_Catch, width = 10, bd=2)
        entry_QCFailed_CatchVariables.grid(row =6, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedCatchVariables = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-C-02-3)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_CatchVariablesResultViewer)
        btnViewQCFailedCatchVariables.grid(row =6, column = 3, padx=60, pady =2, sticky =W)

        RangeDetails_CatchVariables = Listbox(QCFrame, font=('aerial', 9), height =6, width =40)
        RangeDetails_CatchVariables.insert(1, " RecordType : 1 or 2 - No Blank")
        RangeDetails_CatchVariables.insert(2, " AverageTowSpeed : 0 To 5 - If Not Blank")
        RangeDetails_CatchVariables.insert(3, " KeptWeight : 0 To 150,000 - If Not Blank")
        RangeDetails_CatchVariables.insert(4, " DiscardWeight : 0 To 15,000 - If Not Blank")
        RangeDetails_CatchVariables.insert(5, " NumberIndividuals : 0 To 100 - If Not Blank")
        RangeDetails_CatchVariables.insert(6, " NumberWindows : 0 To 1 - If Not Blank")
        RangeDetails_CatchVariables.grid(row =6, column = 4, padx=1, pady =2, ipady = 5, sticky =W)

    SimpleQC_RangeValidation_CalenderVariables()
    SimpleQC_RangeValidation_PositionalVariables()
    SimpleQC_RangeValidation_GearVariables()
    SimpleQC_RangeValidation_CatchVariables()

    lbl_Total_QCFailed = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Failed In QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCFailed.grid(row =0, column = 2, padx=4, pady =2)
    Set_Catch_TotalFailed = (int(QCFailed_CalenderVariables) + int(QCFailed_PositionalVariables)
                             + int(QCFailed_GearVariables) + int(QCFailed_CatchVariables))
    Total_QC_Failed = IntVar(Topframe, value=Set_Catch_TotalFailed)
    entry_Total_QCFailed = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Failed, width = 8, bd=2)
    entry_Total_QCFailed.grid(row =0, column = 3, padx=1, pady =5)

    ## Defining Reload Functions
    def ReloadQCFailedSummary():
        entry_Total_QCFailed.delete(0,END)
        Reload_SetCatch_RunRunRangeValidation = DFO_NL_ASOP_SetCatch_RunRangeValidation.SetCatch_VariableRangeValidation()
        TotalFailedQC_RangeValidation = Reload_SetCatch_RunRunRangeValidation[1]
        entry_Total_QCFailed.insert(tk.END,TotalFailedQC_RangeValidation)
        SimpleQC_RangeValidation_CalenderVariables()
        SimpleQC_RangeValidation_PositionalVariables()
        SimpleQC_RangeValidation_GearVariables()
        SimpleQC_RangeValidation_CatchVariables()
    ## Defining Bottom Frame
    BottomFrame = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    BottomFrame.pack(side = BOTTOM)
    btnRefreashReload = Button(BottomFrame, text="Reload QC Failed Summary", font=('aerial', 12, 'bold'), 
                                        bg ="aliceblue", height =2, width=22, bd=2, anchor=tk.CENTER, padx=5,
                                        command = ReloadQCFailedSummary)
    btnRefreashReload.grid(row =0, column = 0, padx=1, pady =4, sticky =W)

    root.mainloop()

