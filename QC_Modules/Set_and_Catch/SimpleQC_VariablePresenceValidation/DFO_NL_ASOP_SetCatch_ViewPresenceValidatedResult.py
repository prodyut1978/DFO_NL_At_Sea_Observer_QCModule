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
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_SetCatch_RunPresenceValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_SetCatch_ViewPresenceMust_FailedVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_SetCatch_ViewPresenceConditional_FailedVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_ViewQC_MiscPresence_RTGD
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_Misc_Support


def SetCatch_ViewPresenceValidatedResult():
    root=tk.Toplevel()
    root.title ("DFO-NL-ASOP Variable Presence Validation QC - ID-C-03")
    root.geometry('1055x890+400+100')
    root.config(bg="aliceblue")
    Topframe = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    lbl_Total_QCEntries = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Entries For QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCEntries.grid(row =0, column = 0, padx=4, pady =2)
    Set_Catch_TotalEntries =DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumberOf_Entries()
    Total_QC_Entries = IntVar(Topframe, value=Set_Catch_TotalEntries)
    entry_Total_QCEntries = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Entries, width = 8, bd=2)
    entry_Total_QCEntries.grid(row =1, column = 0, padx=2, pady =1)

    ## Get File Name Imported File
    ImportedFileName = DFO_NL_ASOP_Misc_Support.GetPickledImportedFileName()
    ImportedFileName = ImportedFileName.split(",")
    ImportedFileName =(ImportedFileName[0])
    TextString =  '( File Name : ' + ImportedFileName + ' )'
    lblHeader = Label(Topframe, font=('aerial', 12, 'bold'), 
                text=("  ** Simple QC & Validation Summary- ID-C-03 : Variable Presence QC  **  ") + '\n' + TextString, 
                bg="aliceblue")
    lblHeader.grid(row =1, column = 1, padx=40, pady =2, sticky =W, columnspan =2)
    ## TopFrame
    Topframe.pack(side = TOP)
    TableMargin1 = Frame(root, bd = 2, padx= 2, pady= 2, relief = RIDGE, bg="aliceblue")
    TableMargin1.pack(side=TOP)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", 
                                               "column3", "column4", 
                                               "column5"), height=0,
                                                show='headings')
    tree1.heading("#1", text="ID-C-03", anchor=CENTER)
    tree1.heading("#2", text="QC Variables Name", anchor=CENTER)
    tree1.heading("#3", text="Total QC Failed", anchor=CENTER)
    tree1.heading("#4", text="View Failed Results & Update Set & Catch DB", anchor=CENTER)
    tree1.heading("#5", text="QC Variables Presence Details", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=55)       
    tree1.column('#2', stretch=NO, minwidth=0, width=160)            
    tree1.column('#3', stretch=NO, minwidth=0, width=160)
    tree1.column('#4', stretch=NO, minwidth=0, width=350)
    tree1.column('#5', stretch=NO, minwidth=0, width=290)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'),background ="aliceblue", foreground='black')
    tree1.pack()
    QCFrame = Frame(TableMargin1, bd = 2, padx= 0, pady= 5, relief = RIDGE, bg="white")
    QCFrame.pack(side = LEFT)

    QCFailed_PresenceMust = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumberOf_PresenceMust_Failed()
    QCFailed_PresenceConditional = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumberOf_PresenceConditional_Failed()
    QCFailed_PreCondlMisc = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumOf_PreCondlMisc_Fail()
    
    def SimpleQC_PresenceMust_FailedVariables():
        def QCFailed_PresenceMustResultViewer():
            QCFailed_PresenceMust = ( DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumberOf_PresenceMust_Failed())
            QCFailed_PresenceMust =int(QCFailed_PresenceMust)
            if QCFailed_PresenceMust>0:
                    DFO_NL_ASOP_SetCatch_ViewPresenceMust_FailedVariables.ViewPresenceMustValidatedResult()
            else:
                tkinter.messagebox.showinfo("Presence Must Type Variables Table Range Validation Message",
                "Presence Must Type Variables Table Range Validation All Passed. *** All Presence Must Type Variables Table Range \
                in The Set & Catch Import are Validated Against Presence Must Type Variables Table Range Table ****")
        PresenceMust_FailedVariables = IntVar(QCFrame, value=0)
        entry_PresenceMust_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = PresenceMust_FailedVariables, width = 3, bd=2)
        entry_PresenceMust_FailedVariables.grid(row =0, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        List_PresenceMust_FailedVariables = Listbox(QCFrame, font=('aerial', 8, 'bold'), height =10, width =22)
        List_PresenceMust_FailedVariables.insert( 1," ASOC/ObsN/SetN")
        List_PresenceMust_FailedVariables.insert( 2," DepN/SubTripN")
        List_PresenceMust_FailedVariables.insert( 3," Country/Quota/SetType")
        List_PresenceMust_FailedVariables.insert( 4," VesSideN/VesClass")
        List_PresenceMust_FailedVariables.insert( 5," GType/RType/NAFO")
        List_PresenceMust_FailedVariables.insert( 6," Yr/D/M/DataSource/AvgD")
        List_PresenceMust_FailedVariables.insert( 7," HD/HM/StTime/Duration")
        List_PresenceMust_FailedVariables.insert( 8," PosPrec/InOut200")
        List_PresenceMust_FailedVariables.insert( 9," Lat/Lon (Start/End)")
        List_PresenceMust_FailedVariables.insert( 10," DirSpecies/DetailCatchSCCode   ")
        List_PresenceMust_FailedVariables.grid(row =0, column = 1, padx=20, pady =2, ipady = 5, sticky =W)
        
        QCFailed_PresenceMust = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumberOf_PresenceMust_Failed()
        QCFailed_PresenceMust = IntVar(QCFrame, value=QCFailed_PresenceMust)
        entry_QCFailed_PresenceMust = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_PresenceMust, width = 10, bd=2)
        entry_QCFailed_PresenceMust.grid(row =0, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedPresenceMust = Button(QCFrame, text="QC View & Update DB \n (ID-C-03-0)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="c", padx=10,
                                    command = QCFailed_PresenceMustResultViewer)
        btnViewQCFailedPresenceMust.grid(row =0, column = 3, padx=90, pady =2, sticky =W)
        PresenceMustVariables = Listbox(QCFrame, font=('aerial', 9), height =11, width =45)
        PresenceMustVariables.insert( 1,"           **** Variables Must Not Be Blank **** ")
        PresenceMustVariables.insert( 2," - ASOC/Depl#/Set#")
        PresenceMustVariables.insert( 3," - Obs#(>2006)/SubTrip# (>2012)")
        PresenceMustVariables.insert( 4," - Country/Quota/SetType")
        PresenceMustVariables.insert( 5," - VesselSide#/VesselClass/DirectedSpecies")
        PresenceMustVariables.insert( 6," - GearType/RecordType/NAFODivision")
        PresenceMustVariables.insert( 7," - Year/Day/Month/DataSource/AverageDepth")
        PresenceMustVariables.insert( 8," - HaulDay(>2012)/HaulMonth(>2012)")
        PresenceMustVariables.insert( 9," - PositionPrecision/InOut200MileLimit/StartTime/Duration")
        PresenceMustVariables.insert( 10," - StartLatitude/StartLongitude/EndLatitude/EndLongitude")
        PresenceMustVariables.insert( 11," - DetailedCatchSpeciesCompCode(>2012)")
        
        PresenceMustVariables.grid(row =0, column = 4, padx=1, pady =2, ipady = 5, sticky =W)
        
    def SimpleQC_PresenceConditional_FailedVariables():
        def QCFailed_PresenceConditionalResultViewer():
            QCFailed_PresenceConditional = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumberOf_PresenceConditional_Failed()
            QCFailed_PresenceConditional =int(QCFailed_PresenceConditional)
            if QCFailed_PresenceConditional>0:
                DFO_NL_ASOP_SetCatch_ViewPresenceConditional_FailedVariables.ViewPresenceConditionalValidatedResult()
            else:
                tkinter.messagebox.showinfo("Presence Conditional Type Variables Table Range Validation Message",
                "Presence Conditional Type Variables Table Range Validation All Passed. *** All Presence Conditional Type Variables Table Range \
                in The Set & Catch Import are Validated Against Presence Conditional Type Variables Table Range****")
        
        PresenceConditional_FailedVariables = IntVar(QCFrame, value=1)
        entry_PresenceConditional_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = PresenceConditional_FailedVariables, width = 3, bd=2)
        entry_PresenceConditional_FailedVariables.grid(row =2, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        List_PresenceConditional_FailedVariables = Listbox(QCFrame, font=('aerial', 8, 'bold'), height =8, width =22)
        List_PresenceConditional_FailedVariables.insert(1, " AverageTowSpeed   ")
        List_PresenceConditional_FailedVariables.insert(2, " CodendMeshSize   ")
        List_PresenceConditional_FailedVariables.insert(3, " MeshSize_MG   ")
        List_PresenceConditional_FailedVariables.insert(4, " NumberGillnets   ")
        List_PresenceConditional_FailedVariables.insert(5, " AverageGillnetLength  ")
        List_PresenceConditional_FailedVariables.insert(6, " NumberHooks  ")
        List_PresenceConditional_FailedVariables.insert(7, " NumberWindows  ")
        List_PresenceConditional_FailedVariables.insert(8, " NumberPots  ")
        List_PresenceConditional_FailedVariables.grid(row =2, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_PresenceConditional = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumberOf_PresenceConditional_Failed()
        QCFailed_PresenceConditional = IntVar(QCFrame, value=QCFailed_PresenceConditional)
        entry_QCFailed_PresenceConditional = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_PresenceConditional, width = 10, bd=2)
        entry_QCFailed_PresenceConditional.grid(row =2, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedPresenceConditional = Button(QCFrame, text="QC View & Update DB \n (ID-C-03-1)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="c", padx=10,
                                    command = QCFailed_PresenceConditionalResultViewer)
        btnViewQCFailedPresenceConditional.grid(row =2, column = 3, padx=90, pady =2, sticky =W)
        
        PresenceConditionalVariables = Listbox(QCFrame, font=('aerial', 9), height =22, width =45)
        PresenceConditionalVariables.insert(1, " If GearType (Fixed Gear)==[ 4,5,7,8,10,13,14,15,20,22,64,65]")
        PresenceConditionalVariables.insert(2, " Then > AverageTowSpeed Value == 0.0 or Blank")
        PresenceConditionalVariables.insert(3, " Else > AverageTowSpeed Value > 0.0 ")

        PresenceConditionalVariables.insert(4, " ***************************************************** ")
        
        PresenceConditionalVariables.insert(5, " If GearType ==[ 1,2,3,9,16,17,18,21,24,66,67,97 ] ")
        PresenceConditionalVariables.insert(6, " Then > CodendMeshSize == Not Blank Else Blank ")

        PresenceConditionalVariables.insert(7, " ***************************************************** ")

        PresenceConditionalVariables.insert(8, " If GearType ==[ 1,2,3,6,9,16,17,18,21,23,24,66,67,97 ] ")
        PresenceConditionalVariables.insert(9, " Then > MeshSizeMG == Not Blank Else Blank")

        PresenceConditionalVariables.insert(10, " ***************************************************** ")

        PresenceConditionalVariables.insert(11, " If GearType ==[ 5,15 ] ")
        PresenceConditionalVariables.insert(12, " Then > NumberGillnets == Not Blank Else Blank ")
        PresenceConditionalVariables.insert(12, " & AverageGillnetLength == Not Blank Else Blank ")

        PresenceConditionalVariables.insert(13, " ***************************************************** ")
        
        PresenceConditionalVariables.insert(14, " If GearType ==[ 7,8,22 ] ")
        PresenceConditionalVariables.insert(15, " Then > NumberHooks == Not Blank Else Blank ")

        PresenceConditionalVariables.insert(16, " ***************************************************** ")
        
        PresenceConditionalVariables.insert(17, " If GearType ==[ 1,2,16,17,18,21,66,67 ] ")
        PresenceConditionalVariables.insert(18, " Then > NumberWindows == Not Blank Else Blank ")

        PresenceConditionalVariables.insert(19, " ***************************************************** ")
        
        PresenceConditionalVariables.insert(20, " If GearType ==[ 64 ] ")
        PresenceConditionalVariables.insert(21, " Then > NumberPots == Not Blank Else Blank")
        
        PresenceConditionalVariables.grid(row =2, column = 4, padx=1, pady =20, ipady = 5, sticky =W)

    def SimpleQC_PreCondlMisc_FailedVariables():
        def QCFailed_PreCondlMiscResultViewer():
            QCFailed_PreCondlMisc = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumOf_PreCondlMisc_Fail()
            QCFailed_PreCondlMisc =int(QCFailed_PreCondlMisc)
            if QCFailed_PreCondlMisc>0:
                DFO_NL_ASOP_ViewQC_MiscPresence_RTGD.ViewQCFailed_MiscPresence_RTGD()
            else:
                tkinter.messagebox.showinfo("Presence Conditional Type Variables Table Range Validation Message",
                "Presence Conditional Type Variables Table Range Validation All Passed. *** All Presence Conditional Type Variables Table Range \
                in The Set & Catch Import are Validated Against Presence Conditional Type Variables Table Range****")
        
        PreCondlMisc_FailedVariables = IntVar(QCFrame, value=2)
        entry_PreCondlMisc_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = PreCondlMisc_FailedVariables, width = 3, bd=2)
        entry_PreCondlMisc_FailedVariables.grid(row =6, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        List_PreCondlMisc_FailedVariables = Listbox(QCFrame, font=('aerial', 8, 'bold'), height =2, width =22)
        List_PreCondlMisc_FailedVariables.insert(1, " RecordType   ")
        List_PreCondlMisc_FailedVariables.insert(2, " GearDamage   ")
        List_PreCondlMisc_FailedVariables.grid(row =6, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_PresenceCondlMisc = DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult_DBCount.SetCatch_NumOf_PreCondlMisc_Fail()
        QCFailed_PreCondlMisc = IntVar(QCFrame, value=QCFailed_PresenceCondlMisc)
        entry_QCFailed_PreCondlMisc = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_PreCondlMisc, width = 10, bd=2)
        entry_QCFailed_PreCondlMisc.grid(row =6, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedPreCondlMisc = Button(QCFrame, text="QC View & Update DB \n (ID-C-03-2)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="c", padx=10,
                                    command = QCFailed_PreCondlMiscResultViewer)
        btnViewQCFailedPreCondlMisc.grid(row =6, column = 3, padx=90, pady =2, sticky =W)
        
        PreCondlMiscVariables = Listbox(QCFrame, font=('aerial', 9), height =2, width =45)
        PreCondlMiscVariables.insert(1, " If No RecType 2 Present For A Set")
        PreCondlMiscVariables.insert(2, " Then > GearDamage Should Not Equal To 1")

        PreCondlMiscVariables.grid(row =6, column = 4, padx=1, pady =20, ipady = 5, sticky =W)

    SimpleQC_PresenceMust_FailedVariables()
    SimpleQC_PresenceConditional_FailedVariables()
    SimpleQC_PreCondlMisc_FailedVariables()

    lbl_Total_QCFailed = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Failed In QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCFailed.grid(row =0, column = 3, padx=4, pady =2)
    Set_Catch_TotalFailed = int(QCFailed_PresenceMust) + \
                            int(QCFailed_PresenceConditional) + \
                            int(QCFailed_PreCondlMisc)
    Total_QC_Failed = IntVar(Topframe, value=Set_Catch_TotalFailed)
    entry_Total_QCFailed = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Failed, width = 8, bd=2)
    entry_Total_QCFailed.grid(row =1, column = 3, padx=1, pady =5)

    ## Defining Reload Functions
    def ReloadQCFailedSummary():
        entry_Total_QCFailed.delete(0,END)
        Reload_SetCatch_RunRunRangeValidation = DFO_NL_ASOP_SetCatch_RunPresenceValidation.SetCatch_VariablePresenceValidation()
        TotalFailedQC_RangeValidation = Reload_SetCatch_RunRunRangeValidation[1]
        entry_Total_QCFailed.insert(tk.END,TotalFailedQC_RangeValidation)
        SimpleQC_PresenceMust_FailedVariables()
        SimpleQC_PresenceConditional_FailedVariables()
        SimpleQC_PreCondlMisc_FailedVariables()
    
    ## Defining Bottom Frame
    BottomFrame = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    BottomFrame.pack(side = BOTTOM)
    btnRefreashReload = Button(BottomFrame, text="Reload QC Failed Summary", font=('aerial', 12, 'bold'), 
                                        bg ="aliceblue", height =2, width=22, bd=2, anchor=tk.CENTER, padx=5,
                                        command = ReloadQCFailedSummary)
    btnRefreashReload.grid(row =0, column = 0, padx=1, pady =4, sticky =W)

    root.mainloop()
