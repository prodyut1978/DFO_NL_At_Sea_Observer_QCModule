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
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_ViewLogical_Catch_FailedVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_ViewLogical_RTypeNSpecies_FailedVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_ViewLogical_RTypeSetN_FailedVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_ViewLogical_RT_SC_NS_FailedVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_ViewLogical_RT_KW_DW_NI_FailedVariables
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_RunLogicalValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_Misc_Support

def SetCatch_ViewLogicalValidatedResult():
    root=tk.Toplevel()
    root.title ("DFO-NL-ASOP Variable Logical Validation QC")
    root.geometry('1140x880+200+20')
    root.config(bg="aliceblue")
    Topframe = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    lbl_Total_QCEntries = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Entries For QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCEntries.grid(row =0, column = 0, padx=4, pady =2)
    Set_Catch_TotalEntries =DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_Entries()
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
                text=("  ** Simple QC & Validation Summary- ID-C-04 : Variable Logical QC  **  ") + '\n' + TextString, 
                bg="aliceblue")
    lblHeader.grid(row =1, column = 1, padx=40, pady =2, sticky =W, columnspan =2)
    ## Topframe
    Topframe.pack(side = TOP)
    TableMargin1 = Frame(root, bd = 2, padx= 2, pady= 2, relief = RIDGE, bg="aliceblue")
    TableMargin1.pack(side=TOP)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", 
                                               "column3", "column4", 
                                               "column5"), height=0,
                                                show='headings')
    tree1.heading("#1", text="ID-C-04", anchor=CENTER)
    tree1.heading("#2", text="QC Variables Name", anchor=CENTER)
    tree1.heading("#3", text="Total QC Failed", anchor=CENTER)
    tree1.heading("#4", text="View Failed Results & Update Set & Catch DB", anchor=CENTER)
    tree1.heading("#5", text="QC Variables Logical Details", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=55)       
    tree1.column('#2', stretch=NO, minwidth=0, width=160)            
    tree1.column('#3', stretch=NO, minwidth=0, width=160)
    tree1.column('#4', stretch=NO, minwidth=0, width=320)
    tree1.column('#5', stretch=NO, minwidth=0, width=440)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'),background ="aliceblue", foreground='black')
    tree1.pack()
    QCFrame = Frame(TableMargin1, bd = 2, padx= 0, pady= 5, relief = RIDGE, bg="white")
    QCFrame.pack(side = LEFT)
    QCFailed_CatchVariables = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalCatch_Failed()
    QCFailed_RS = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRS_Failed()
    QCFailed_RN = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRN_Failed()
    QCFailed_RT_SpCode = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRT_SpCode_Failed()
    QCFailed_RT_KW_DW_NI = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_RecType_KW_DW_NI_Failed()

    def SimpleQC_LogicalFailed_CatchVariables():

        def QCFailed_CatchVariablesResultViewer():
            QCFailed_CatchVariables = (DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalCatch_Failed())
            QCFailed_CatchVariables =int(QCFailed_CatchVariables)
            if QCFailed_CatchVariables>0:
                    DFO_NL_ASOP_SetCatch_ViewLogical_Catch_FailedVariables.ViewLogicalSetCatchlValidatedResult()
            else:
                tkinter.messagebox.showinfo("Catch Type Variables Table Logical Validation Message",
                "Catch Type Variables Table Logical Validation All Passed. *** All Catch Variables Table Logical \
                in The Set & Catch Import are Validated Against Catch Variables Table Logical Table ****")

        LogicalCatch_FailedVariables = IntVar(QCFrame, value=0)
        entry_LogicalCatch_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = LogicalCatch_FailedVariables, width = 3, bd=2)
        entry_LogicalCatch_FailedVariables.grid(row =0, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        List_LogicalCatch_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =5, width =22, borderwidth =4)
        List_LogicalCatch_FailedVariables.insert( 1," 1: CodendMeshSize   ")
        List_LogicalCatch_FailedVariables.insert( 2," 2: NumberPotReleasedCrab   ")
        List_LogicalCatch_FailedVariables.insert( 3," 3: EstimatedWeightReleasedCrab   ")
        List_LogicalCatch_FailedVariables.insert( 4," 4: KeptWeight   ")
        List_LogicalCatch_FailedVariables.insert( 5," 5: DiscardWeight   ")
        
        List_LogicalCatch_FailedVariables.grid(row =0, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_LogicalCatch = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalCatch_Failed()
        QCFailed_LogicalCatch =int(QCFailed_LogicalCatch)
        entryQCFailed_Catch = IntVar(QCFrame, value=QCFailed_LogicalCatch)
        
        entry_QCFailed_LogicalCatch = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_Catch, width = 10, bd=2)
        entry_QCFailed_LogicalCatch.grid(row =0, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedLogicalCatch = Button(QCFrame, text="QC View & Update DB \n (ID-C-04-0)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_CatchVariablesResultViewer)
        btnViewQCFailedLogicalCatch.grid(row =0, column = 3, padx=90, pady =2, sticky =W)
        LogicalCatchVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =6, width =60, borderwidth =4)
       
        LogicalCatchVariables.insert( 1," 1. CodendMeshSize =< MeshSize_MG ")
        LogicalCatchVariables.insert( 2," 2. If NumberPotsReleasedCrab Non-Blank Then : ")
        LogicalCatchVariables.insert( 3,"     >>> DirectedSpecies Must Be 8213")
        
        LogicalCatchVariables.insert( 4," 3. If EstimatedWeightReleasedCrab Non-Blank Then :")
        LogicalCatchVariables.insert( 5,"     >>> NumberPotsReleasedCrab Must Be > 0 & Non-Blank")
       
        LogicalCatchVariables.insert( 6," 4. KeptWeight + DiscardWeight => 1 ")

        LogicalCatchVariables.grid(row =0, column = 4, padx=1, pady =20, ipady = 5, sticky =W)

    def SimpleQC_LogicalFailed_RecordType_SetNumber():
        
        def QCFailed_RecordtypeSetNumberResultViewer():
            QCFailed_RS = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRS_Failed()
            QCFailed_RS =int(QCFailed_RS)
            if QCFailed_RS>0:
                    DFO_NL_ASOP_SetCatch_ViewLogical_RTypeSetN_FailedVariables.ViewLogicalRT_SNValidatedResult()
            else:
                tkinter.messagebox.showinfo("RecordType-SetNumber Variables Logical Validation Message",
                "RecordType - SetNumber Logical Validation All Passed. *** All RecordType - SetNumber Logical \
                in The Set & Catch Import are Validated Against RecordType - SetNumber Logical Table ****")
        
        LogicalRS_FailedVariables = IntVar(QCFrame, value=1)
        entry_LogicalRS_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), 
                                state=DISABLED, justify='center',
                                textvariable = LogicalRS_FailedVariables, width = 3, bd=2)
        entry_LogicalRS_FailedVariables.grid(row =2, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        List_LogicalRS_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =2, width =22, borderwidth =4)
       
        List_LogicalRS_FailedVariables.insert(1, "1: RecordType   ")
        List_LogicalRS_FailedVariables.insert(2, "2: SetNumber   ")
        List_LogicalRS_FailedVariables.grid(row =2, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_RS_Variable = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRS_Failed()
        QCFailed_RS_Variable =int(QCFailed_RS_Variable)
        QCFailed_RecordTypeSetN = IntVar(QCFrame, value=QCFailed_RS_Variable)
        entry_QCFailed_RS = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_RecordTypeSetN, width = 10, bd=2)
        entry_QCFailed_RS.grid(row =2, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedRS = Button(QCFrame, text="QC View & Update DB \n (ID-C-04-1)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="c", padx=10,
                                    command = QCFailed_RecordtypeSetNumberResultViewer)
        btnViewQCFailedRS.grid(row =2, column = 3, padx=90, pady =2, sticky =W)
        
        LogicalRSVariables = Listbox(QCFrame, font=('aerial', 9,'bold'), height =2, width =60, borderwidth =4)
        LogicalRSVariables.insert(1, " Logical RecordType-SetNumber Relation : ")
        LogicalRSVariables.insert(2, " Only (No Multiple) & Atleast One (No Empty) RecordType1 Per SetNumber")
        LogicalRSVariables.grid(row =2, column = 4, padx=1, pady =20, ipady = 5, sticky =W)

    def SimpleQC_LogicalFailed_NumberSpeciesVariables():

        def QCFailed_RecordtypeNumberSpeciesResultViewer():
            QCFailed_RN = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRN_Failed()
            QCFailed_RN =int(QCFailed_RN)
            if QCFailed_RN>0:
                    DFO_NL_ASOP_SetCatch_ViewLogical_RTypeNSpecies_FailedVariables.ViewLogicalNSpeciesValidatedResult()
            else:
                tkinter.messagebox.showinfo("RecordType-NumberSpecies Variables Logical Validation Message",
                "RecordType - NumberSpecies Logical Validation All Passed. *** All RecordType - NumberSpecies Logical \
                in The Set & Catch Import are Validated Against RecordType - NumberSpecies Logical Table ****")
        
        LogicalNumberSpecies_FailedVariables = IntVar(QCFrame, value=2)
        entry_LogicalNumberSpecies_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = LogicalNumberSpecies_FailedVariables, width = 3, bd=2)
        entry_LogicalNumberSpecies_FailedVariables.grid(row =4, column = 0, padx=10, pady =2, ipady = 2, sticky =W)
        List_LogicalNumberSpecies_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =4, width =22, borderwidth =4)
       
        List_LogicalNumberSpecies_FailedVariables.insert(1, "1: RecordType   ")
        List_LogicalNumberSpecies_FailedVariables.insert(2, "2: SetNumber   ")
        List_LogicalNumberSpecies_FailedVariables.insert(3, "3: NumberSpecies   ")
        List_LogicalNumberSpecies_FailedVariables.grid(row =4, column = 1, padx=20, pady =2, ipady = 2, sticky =W)

        QCFailed_RN_Variable = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRN_Failed()
        QCFailed_RN_Variable =int(QCFailed_RN_Variable)
        QCFailed_RecordTypeNS = IntVar(QCFrame, value=QCFailed_RN_Variable)
        entry_QCFailed_NS = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_RecordTypeNS, width = 10, bd=2)
        entry_QCFailed_NS.grid(row =4, column = 2, padx=2, pady =2, ipady = 2, sticky =W)

        btnViewQCFailedNS = Button(QCFrame, text="QC View & Update DB \n (ID-C-04-2)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_RecordtypeNumberSpeciesResultViewer)
        btnViewQCFailedNS.grid(row =4, column = 3, padx=90, pady =2, sticky =W)
        
        LogicalNumberSpeciesVariables = Listbox(QCFrame, font=('aerial', 9,'bold'), height =7, width =60, borderwidth =4)
        LogicalNumberSpeciesVariables.insert(1, " Logical RecordType - SetNumber - NumberSpecies Relation :  ")
        LogicalNumberSpeciesVariables.insert(2, " A. Case - A ")
        LogicalNumberSpeciesVariables.insert(3, " In A Set With Only RecordType1 =>> ")
        LogicalNumberSpeciesVariables.insert(4, " NumberSpecies Must Be == 0 or Blank ")
        LogicalNumberSpeciesVariables.insert(5, " B. Case - B ")
        LogicalNumberSpeciesVariables.insert(6, " In A Set With Recordtype 1 & 2 =>> ")
        LogicalNumberSpeciesVariables.insert(7, " NumberSpecies In RecordType 1 == NumberSpecies In RecordType 2 ")
        LogicalNumberSpeciesVariables.grid(row =4, column = 4, padx=1, pady =20, ipady = 2, sticky =W)
    
    def SimpleQC_LogicalFailed_RecordType_SpeciesCode():
        
        def QCFailed_RecordType_SpeciesCodeViewer():
            QCFailed_RN = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRT_SpCode_Failed()
            QCFailed_RN = int(QCFailed_RN)
            if QCFailed_RN > 0:
                 DFO_NL_ASOP_SetCatch_ViewLogical_RT_SC_NS_FailedVariables.ViewLogical_RT_NS_SpCode_ValidatedResult()
            else:
                tkinter.messagebox.showinfo("RecordType-SpeciesCode Variables Logical Validation Message",
                "RecordType - SpeciesCode Logical Validation All Passed. *** All RecordType - SpeciesCode Logical \
                in The Set & Catch Import are Validated Against RecordType - SpeciesCode Logical Table ****")
        
        LogicalRecTypSpecCode_FailedVariables = IntVar(QCFrame, value=3)
        entry_LogicalRecTypSpecCode_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), 
                                state=DISABLED, justify='center',
                                textvariable = LogicalRecTypSpecCode_FailedVariables, width = 3, bd=2)
        entry_LogicalRecTypSpecCode_FailedVariables.grid(row =6, column = 0, padx=10, pady =2, ipady = 2, sticky =W)
        List_LogicalRecTypSpecCode_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =4, width =22, borderwidth =4)
    
        List_LogicalRecTypSpecCode_FailedVariables.insert(1, "1: RecordType   ")
        List_LogicalRecTypSpecCode_FailedVariables.insert(2, "2: SetNumber   ")
        List_LogicalRecTypSpecCode_FailedVariables.insert(3, "3: NumberSpecies   ")
        List_LogicalRecTypSpecCode_FailedVariables.insert(4, "4: SpeciesCode   ")
        List_LogicalRecTypSpecCode_FailedVariables.grid(row =6, column = 1, padx=20, pady =2, ipady = 2, sticky =W)

        QCFailed_RTSC_Variable = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_LogicalRT_SpCode_Failed()
        QCFailed_RTSC_Variable =int(QCFailed_RTSC_Variable)
        QCFailed_RecTypSpecCode = IntVar(QCFrame, value=QCFailed_RTSC_Variable)
        entry_QCFailed_RecTypSpecCode = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_RecTypSpecCode, width = 10, bd=2)
        entry_QCFailed_RecTypSpecCode.grid(row =6, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedRecTypSpecCode = Button(QCFrame, text="QC View & Update DB \n (ID-C-04-3)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_RecordType_SpeciesCodeViewer)
        btnViewQCFailedRecTypSpecCode.grid(row =6, column = 3, padx=90, pady =2, sticky =W)

        LogicalRecTypSpecCode_IdentityVariables = Listbox(QCFrame, font=('aerial', 9,'bold'), height =6, width =60, borderwidth =4)
        LogicalRecTypSpecCode_IdentityVariables.insert(1, " Case - A : For RecordType1 @ Each Set")
        LogicalRecTypSpecCode_IdentityVariables.insert(2, " SpeciesCode Must Be Blank")
       
        LogicalRecTypSpecCode_IdentityVariables.insert(4, " Case -B : For RecordType2 @ Each Set")
        LogicalRecTypSpecCode_IdentityVariables.insert(5, " Count Sum Of SpeciesCode Must Equal To NumberSpecies")
        LogicalRecTypSpecCode_IdentityVariables.insert(6, " & NumberSpecies Must Be Same")
       
        LogicalRecTypSpecCode_IdentityVariables.grid(row =6, column = 4, padx=1, pady =20, ipady = 2, sticky =W)

    def SimpleQC_LogicalFailed_RecType_KW_DW_NI():
        
        def QCFailed_RecType_KW_DW_NIViewer():
            QCFailed_RT_KW_DW_NI = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_RecType_KW_DW_NI_Failed()
            QCFailed_RT_KW_DW_NI = int(QCFailed_RT_KW_DW_NI)
            if QCFailed_RT_KW_DW_NI > 0:
                 DFO_NL_ASOP_SetCatch_ViewLogical_RT_KW_DW_NI_FailedVariables.ViewLogical_RecType_KW_DW_NI_Result()
            else:
                tkinter.messagebox.showinfo("RecordType-SpeciesCode Variables Logical Validation Message",
                "Logical Validation All Passed. *** All Logical \
                in The Set & Catch Import are Validated Against Logical Table ****")
        
        LogicalRT_KW_DW_NI_FailedVariables = IntVar(QCFrame, value=4)
        entry_LogicalRT_KW_DW_NI_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = LogicalRT_KW_DW_NI_FailedVariables, width = 3, bd=2)
        entry_LogicalRT_KW_DW_NI_FailedVariables.grid(row =8, column = 0, padx=10, pady =1, ipady = 2, sticky =W)
        List_LogicalRT_KW_DW_NI_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =4, width =22, borderwidth =4)
    
        List_LogicalRT_KW_DW_NI_FailedVariables.insert(1, "1: RecordType 1   ")
        List_LogicalRT_KW_DW_NI_FailedVariables.insert(2, "2: DiscardWeight   ")
        List_LogicalRT_KW_DW_NI_FailedVariables.insert(3, "3: KeptWeight   ")
        List_LogicalRT_KW_DW_NI_FailedVariables.insert(4, "4: NumberIndividuals   ")
        List_LogicalRT_KW_DW_NI_FailedVariables.grid(row =8, column = 1, padx=20, pady =1, ipady = 2, sticky =W)

        QCFailed_RT_KW_DW_NI_Variable = DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult_DBCount.SetCatch_NumberOf_RecType_KW_DW_NI_Failed()
        QCFailed_RT_KW_DW_NI_Variable =int(QCFailed_RT_KW_DW_NI_Variable)
        QCFailed_RT_KW_DW_NICode = IntVar(QCFrame, value=QCFailed_RT_KW_DW_NI_Variable)
        entry_QCFailed_RT_KW_DW_NICode = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = QCFailed_RT_KW_DW_NICode, width = 10, bd=2)
        entry_QCFailed_RT_KW_DW_NICode.grid(row =8, column = 2, padx=2, pady =1, ipady = 5, sticky =W)

        btnViewQCFailedRT_KW_DW_NICode = Button(QCFrame, text="QC View & Update DB \n (ID-C-04-4)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_RecType_KW_DW_NIViewer)
        btnViewQCFailedRT_KW_DW_NICode.grid(row =8, column = 3, padx=90, pady =1, sticky =W)

        LogicalRT_KW_DW_NICode_IdentityVariables = Listbox(QCFrame, font=('aerial', 9,'bold'), height =3, width =60, borderwidth =4)
        LogicalRT_KW_DW_NICode_IdentityVariables.insert(1, " For RecordType1 @ Each Set")
        LogicalRT_KW_DW_NICode_IdentityVariables.insert(2, " KeptWeight/DiscardWeight/NumberIndividuals Must Be Blank")
    
        LogicalRT_KW_DW_NICode_IdentityVariables.grid(row =8, column = 4, padx=1, pady =20, ipady = 2, sticky =W)

    SimpleQC_LogicalFailed_CatchVariables()
    SimpleQC_LogicalFailed_RecordType_SetNumber()
    SimpleQC_LogicalFailed_NumberSpeciesVariables()
    SimpleQC_LogicalFailed_RecordType_SpeciesCode()
    SimpleQC_LogicalFailed_RecType_KW_DW_NI()
    
    lbl_Total_QCFailed = Label(Topframe, font=('aerial', 12, 'bold'), 
                        text="Total Failed In QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCFailed.grid(row =0, column = 3, padx=4, pady =2)
    Set_Catch_TotalFailed = (int(QCFailed_CatchVariables)+\
                             int(QCFailed_RS) + int(QCFailed_RN)+\
                             int(QCFailed_RT_SpCode)+ int(QCFailed_RT_KW_DW_NI)
                             )
    Total_QC_Failed = IntVar(Topframe, value=Set_Catch_TotalFailed)
    entry_Total_QCFailed = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Failed, width = 8, bd=2)
    entry_Total_QCFailed.grid(row =1, column = 3, padx=1, pady =5)
    
    ## Defining Reload Functions
    def ReloadQCFailedSummary():
        entry_Total_QCFailed.delete(0,END)
        Reload_SetCatch_RunRunRangeValidation = DFO_NL_ASOP_SetCatch_RunLogicalValidation.SetCatch_VariableLogicalValidation()
        TotalFailedQC_RangeValidation = Reload_SetCatch_RunRunRangeValidation[1]
        entry_Total_QCFailed.insert(tk.END,TotalFailedQC_RangeValidation)
        SimpleQC_LogicalFailed_CatchVariables()
        SimpleQC_LogicalFailed_RecordType_SetNumber()
        SimpleQC_LogicalFailed_NumberSpeciesVariables()
        SimpleQC_LogicalFailed_RecordType_SpeciesCode()
        SimpleQC_LogicalFailed_RecType_KW_DW_NI()
    
    ## Defining Bottom Frame
    BottomFrame = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    BottomFrame.pack(side = BOTTOM)
    btnRefreashReload = Button(BottomFrame, text="Reload QC Failed Summary", font=('aerial', 12, 'bold'), 
                                        bg ="aliceblue", height =2, width=22, bd=2, anchor=tk.CENTER, padx=5,
                                        command = ReloadQCFailedSummary)
    btnRefreashReload.grid(row =0, column = 0, padx=1, pady =4, sticky =W)

    root.mainloop()

