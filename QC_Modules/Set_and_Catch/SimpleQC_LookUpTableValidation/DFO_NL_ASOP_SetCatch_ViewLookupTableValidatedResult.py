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
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_RunLookUpTableValidation
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_ASOCCode
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_Country
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DataSource
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_GearDamage
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_GearType
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_NAFODivision
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_Quota
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_SetType
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_VesselClass
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_SpeciesCode
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DirectedSpecies
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_UnitArea
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_Misc_Support

def SetCatch_ViewLookupTableValidatedResult():
    root=tk.Toplevel()
    root.title ("DFO-NL-ASOP Lookup Tables Validation QC - ID-C-01")
    root.geometry('1000x790+400+100')
    root.config(bg="aliceblue")
    Topframe = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    
    lbl_Total_QCEntries = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Entries For QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCEntries.grid(row =0, column = 0, padx=4, pady =2)
    Set_Catch_TotalEntries = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_Entries()
    Total_QC_Entries = IntVar(Topframe, value=Set_Catch_TotalEntries)
    entry_Total_QCEntries = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Entries, width = 8, bd=2)
    entry_Total_QCEntries.grid(row =1, column = 0, padx=2, pady =1)

    Topframe.pack(side = TOP)
    Midframe = Frame(root, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
    Midframe.pack(side = TOP)

    ## Get File Name Imported File
    ImportedFileName = DFO_NL_ASOP_Misc_Support.GetPickledImportedFileName()
    ImportedFileName = ImportedFileName.split(",")
    ImportedFileName =(ImportedFileName[0])
    TextString =  '( File Name : ' + ImportedFileName + ' )'
    lblHeader = Label(Topframe, font=('aerial', 12, 'bold'), 
                text=("  ** Simple QC & Validation Summary- ID-C-01 : Variable Lookup QC  **  ") + '\n' + TextString, 
                bg="aliceblue")
    lblHeader.grid(row =1, column = 1, padx=40, pady =2, sticky =W, columnspan =2)
    
    TableMargin1 = Frame(root, bd = 2, padx= 2, pady= 2, relief = RIDGE, bg="aliceblue")
    TableMargin1.pack(side=TOP)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4", "column5"), height=0, show='headings')
    tree1.heading("#1", text="ID-C-01", anchor=CENTER)
    tree1.heading("#2", text="DFO-NL-ASOP Lookup Table", anchor=CENTER)
    tree1.heading("#3", text="Total QC Failed", anchor=CENTER)
    tree1.heading("#4", text="View Failed Results & Update Set & Catch DB", anchor=CENTER)
    tree1.heading("#5", text="Lookup Codes Stat Report", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=60)       
    tree1.column('#2', stretch=NO, minwidth=0, width=240)            
    tree1.column('#3', stretch=NO, minwidth=0, width=140)
    tree1.column('#4', stretch=NO, minwidth=0, width=340)
    tree1.column('#5', stretch=NO, minwidth=0, width=215)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'),background ="aliceblue", foreground='black')
    tree1.pack()
    QCFrame = Frame(TableMargin1, bd = 2, padx= 0, pady= 5, relief = RIDGE, bg="white")
    QCFrame.pack(side = LEFT)

    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")

    QCFailed_ASOCCode = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_ASOCCode()
    QCFailed_Country = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_Country()
    QCFailed_DataSource = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_DataSource()
    QCFailed_GearDamage = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearDamage()
    QCFailed_GearType = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearType()
    QCFailed_NAFODivision = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_NAFODivision()
    QCFailed_UnitArea = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_UnitArea()
    QCFailed_Quota = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_Quota()
    QCFailed_SetType = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_SetType()
    QCFailed_SpeciesCode = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_SpeciesCode()
    QCFailed_DirectedSpecies = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_DirectedSpecies()
    QCFailed_VesselClass = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_VesselClass()

    def SimpleQC_TableLookUp_ASOCCode():
        ## Defining Functions For ASOCCode
        def QCFailed_ASOCCodeResultViewer():
            QCFailed_ASOCCode = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_ASOCCode()
            QCFailed_ASOCCodeCount = int(QCFailed_ASOCCode)
            if QCFailed_ASOCCodeCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_ASOCCode.SetCatch_ViewLookupValidatedResult_ASOCCode()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "ASOCCode Codes Validation All Passed. *** All ASOCCode Codes \
                in The Set & Catch Import are Validated Against ASOCCode Codes LookUp Table ****")
       
        def Generate_ASOCCodeStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'ASOCCode'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['ASOCCode'] = (InvDB_Set_Catch_Analysis.loc[:,['ASOCCode']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['ASOCCode'] = (InvDB_Set_Catch_Analysis.loc[:,['ASOCCode']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()
            
            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_ASOCCodeProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()

            time.sleep(1)
            
            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['ASOCCode'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'ASOCCode':'ASOCCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                                                  how='left', on ='ASOCCode')
            Inv_DB_Set_Catch_Analysis1['ASOCCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['ASOCCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['ASOCCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['ASOCCode']]).replace(99999999, '')
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['ASOCCode','ASOCName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['ASOCName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['ASOCName']]).replace(np.nan, 'None')
            
            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['ASOCCode', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'ASOCCode':'ASOCCode',
                                                       'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                       'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['ASOCCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['ASOCCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['ASOCCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['ASOCCode']]).replace(99999999, '')   
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            
            window = Tk()
            window.title("ASOCCode Statistics Report - ID-C-01-0")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - ASOCCode  **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="ASOCCode", anchor=CENTER)
            tree1.heading("#2", text="ASOCCode Name", anchor=CENTER)
            tree1.heading("#3", text="Count By ASOCCode", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="ASOCCode", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
            
            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()

        ## LookUp ASOCCode Validation
        QCFailed_ASOCCode = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_ASOCCode()
        entryIDASOCCode = IntVar(QCFrame, value=0)
        entryTable_ASOCCode = StringVar(QCFrame, value="ASOCCode Table")
        entryQCFailed_ASOCCode = IntVar(QCFrame, value=QCFailed_ASOCCode)

        entry_ID_ASOCCode = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDASOCCode, width = 3, bd=2)
        entry_ID_ASOCCode.grid(row =0, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_ASOCCode = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                textvariable = entryTable_ASOCCode, width = 30, bd=2)
        entry_Table_ASOCCode.grid(row =0, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_ASOCCode = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_ASOCCode, width = 10, bd=2)
        entry_QCFailed_ASOCCode.grid(row =0, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewASOCProfile = Button(QCFrame, text="ASOCCode QC Failed Results \n (ID-C-01-0)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                    command = QCFailed_ASOCCodeResultViewer)
        btnViewASOCProfile.grid(row =0, column = 3, padx=50, pady =2, sticky =W)

        btnASOCCodeReport = Button(QCFrame, text="ASOCCode Statistics \n (ID-C-01-0)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_ASOCCodeStat_Report)
        btnASOCCodeReport.grid(row =0, column = 4, padx=15, pady =2, sticky =W)
        
    def SimpleQC_TableLookUp_Country():
        ## Defining Functions For Country
        def QCFailed_CountryResultViewer():
            QCFailed_Country = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_Country()
            QCFailed_CountryCount = int(QCFailed_Country)
            if QCFailed_CountryCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_Country.SetCatch_ViewLookupValidatedResult_Country()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "Country Codes Validation All Passed. *** All Country Codes \
                in The Set & Catch Import are Validated Against Country Codes LookUp Table ****")
            
        def Generate_CountryStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'Country'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['Country'] = (InvDB_Set_Catch_Analysis.loc[:,['Country']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['Country'] = (InvDB_Set_Catch_Analysis.loc[:,['Country']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_CountryProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()

            time.sleep(1)
            
            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['Country'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'Country':'CountryCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                                                  how='left', on ='CountryCode')
            Inv_DB_Set_Catch_Analysis1['CountryCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['CountryCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['CountryCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['CountryCode']]).replace(99999999, '')       
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['CountryCode','CountryName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['CountryName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['CountryName']]).replace(np.nan, 'None')

            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['Country', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'Country':'CountryCode',
                                                       'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                       'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['CountryCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['CountryCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['CountryCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['CountryCode']]).replace(99999999, '')       
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            
            window = Tk()
            window.title("Country Code Statistics Report - ID-C-01-2")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - Country Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="Country Codes", anchor=CENTER)
            tree1.heading("#2", text="Country Name", anchor=CENTER)
            tree1.heading("#3", text="Count By Country", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="Country Codes", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
            
            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()
            
        ## LookUp Table_Country Code Validation
        QCFailed_Country = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_Country()
        entryIDCountry = IntVar(QCFrame, value=1)
        entryTable_Country = StringVar(QCFrame, value="Country Codes Table")
        entryQCFailed_Country = IntVar(QCFrame, value=QCFailed_Country)

        entry_IDCountry = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDCountry, width = 3, bd=2)
        entry_IDCountry.grid(row =2, column = 0, padx=4, pady =2, ipady = 3, sticky =W)

        entry_Table_Country = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_Country, width = 30, bd=2)
        entry_Table_Country.grid(row =2, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_Country = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                    textvariable = entryQCFailed_Country, width = 10, bd=2)
        entry_QCFailed_Country.grid(row =2, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnQCFailed_CountryResultViewer = Button(QCFrame, text="Country QC Failed Results \n (ID-C-01-1)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_CountryResultViewer)
        btnQCFailed_CountryResultViewer.grid(row =2, column = 3, padx=50, pady =2, sticky =W)


        btnCountryCodeReport = Button(QCFrame, text="Country Code Statistics \n (ID-C-01-1)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_CountryStat_Report)
        btnCountryCodeReport.grid(row =2, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_DataSource():
        ## Defining Functions For DataSource
        def QCFailed_DataSourceResultViewer():
            QCFailed_DataSource = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_DataSource()
            QCFailed_DataSourceCount = int(QCFailed_DataSource)
            if QCFailed_DataSourceCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DataSource.SetCatch_ViewLookupValidatedResult_DataSource()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "DataSource Codes Validation All Passed. *** All DataSource Codes \
                in The Set & Catch Import are Validated Against DataSource Codes LookUp Table ****")
        
        def Generate_DataSourceStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'DataSource'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['DataSource'] = (InvDB_Set_Catch_Analysis.loc[:,['DataSource']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['DataSource'] = (InvDB_Set_Catch_Analysis.loc[:,['DataSource']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_DataSourceProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()
            
            time.sleep(1)
            
            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['DataSource'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'DataSource':'DataSourceCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                                                  how='left', on ='DataSourceCode')
            Inv_DB_Set_Catch_Analysis1['DataSourceCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['DataSourceCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['DataSourceCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['DataSourceCode']]).replace(99999999, '')
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['DataSourceCode','DataSourceName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['DataSourceName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['DataSourceName']]).replace(np.nan, 'None')
            
            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['DataSource', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'DataSource':'DataSourceCode',
                                                       'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                       'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['DataSourceCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['DataSourceCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['DataSourceCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['DataSourceCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            
            window = Tk()
            window.title("DataSource Code Statistics Report - ID-C-01-3")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - DataSource Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="DataSource Codes", anchor=CENTER)
            tree1.heading("#2", text="DataSource Name", anchor=CENTER)
            tree1.heading("#3", text="Count By DataSource", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="DataSource Codes", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
            
            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()
        
        ## LookUp DataSource Code Validation
        QCFailed_DataSource = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_DataSource()
        entryIDDataSource = IntVar(QCFrame, value=2)
        entryTable_DataSource = StringVar(QCFrame, value="DataSource Codes Table")
        entryQCFailed_DataSource = IntVar(QCFrame, value=QCFailed_DataSource)

        entry_ID_DataSource = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDDataSource, width = 3, bd=2)
        entry_ID_DataSource.grid(row =4, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_DataSource = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                textvariable = entryTable_DataSource, width = 30, bd=2)
        entry_Table_DataSource.grid(row =4, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_DataSource = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_DataSource, width = 10, bd=2)
        entry_QCFailed_DataSource.grid(row =4, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewDataSourceProfile = Button(QCFrame, text="DataSource QC Failed Results \n (ID-C-01-2)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                    command = QCFailed_DataSourceResultViewer)
        btnViewDataSourceProfile.grid(row =4, column = 3, padx=50, pady =2, sticky =W)

        btnDataSourceCodeReport = Button(QCFrame, text="DataSource Code Statistics \n (ID-C-01-2)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_DataSourceStat_Report)
        btnDataSourceCodeReport.grid(row =4, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_GearDamage():
        ## Defining Functions For GearDamage
        def QCFailed_GearDamageResultViewer():
            QCFailed_GearDamage = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearDamage()
            QCFailed_GearDamageCount = int(QCFailed_GearDamage)
            if QCFailed_GearDamageCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_GearDamage.SetCatch_ViewLookupValidatedResult_GearDamage()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "GearDamage Codes Validation All Passed. *** All GearDamage Codes \
                in The Set & Catch Import are Validated Against GearDamage Codes LookUp Table ****")

        def Generate_GearDamageStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'GearDamage'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['GearDamage'] = (InvDB_Set_Catch_Analysis.loc[:,['GearDamage']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['GearDamage'] = (InvDB_Set_Catch_Analysis.loc[:,['GearDamage']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_GearDamageProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()
            
            time.sleep(1)
            
            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['GearDamage'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'GearDamage':'GearDamageCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                            how='left', on ='GearDamageCode')
            Inv_DB_Set_Catch_Analysis1['GearDamageCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['GearDamageCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['GearDamageCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['GearDamageCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['GearDamageCode','GearDamageName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['GearDamageName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['GearDamageName']]).replace(np.nan, 'None')
            
            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['GearDamage', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'GearDamage':'GearDamageCode',
                                                        'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                        'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['GearDamageCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['GearDamageCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['GearDamageCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['GearDamageCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            window = Tk()
            window.title("GearDamage Code Statistics Report - ID-C-01-3")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - GearDamage Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="GearDamage Codes", anchor=CENTER)
            tree1.heading("#2", text="GearDamage Name", anchor=CENTER)
            tree1.heading("#3", text="Count By GearDamage", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="GearDamage Codes", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
            
            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()
        
        ## LookUp Gear Damage Code Validation
        QCFailed_GearDamage = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearDamage()
        entryIDGearDamage = IntVar(QCFrame, value=3)
        entryTable_GearDamage = StringVar(QCFrame, value="GearDamage Codes Table")
        entryQCFailed_GearDamage = IntVar(QCFrame, value=QCFailed_GearDamage)

        entry_ID_GearDamage = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                            textvariable = entryIDGearDamage, width = 3, bd=2)
        entry_ID_GearDamage.grid(row =6, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_GearDamage = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_GearDamage, width = 30, bd=2)
        entry_Table_GearDamage.grid(row =6, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_GearDamage = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                    textvariable = entryQCFailed_GearDamage, width = 10, bd=2)
        entry_QCFailed_GearDamage.grid(row =6, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewGearDamageProfile = Button(QCFrame, text="GearDamage QC Failed Results \n (ID-C-01-3)", font=('aerial', 10, 'bold'),
                                            bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                            command = QCFailed_GearDamageResultViewer)
        btnViewGearDamageProfile.grid(row =6, column = 3, padx=50, pady =2, sticky =W)
        btnGearDamageCodeReport = Button(QCFrame, text="GearDamage Code Statistics \n (ID-C-01-3)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_GearDamageStat_Report)
        btnGearDamageCodeReport.grid(row =6, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_GearType():
        ## Defining Functions For GearType
        def QCFailed_GearTypeResultViewer():
            QCFailed_GearType = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearType()
            QCFailed_GearTypeCount = int(QCFailed_GearType)
            if QCFailed_GearTypeCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_GearType.SetCatch_ViewLookupValidatedResult_GearType()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "GearType Codes Validation All Passed. *** All GearType Codes \
                in The Set & Catch Import are Validated Against GearType Codes LookUp Table ****")
        
        def Generate_GearTypeStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'GearType'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['GearType'] = (InvDB_Set_Catch_Analysis.loc[:,['GearType']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['GearType'] = (InvDB_Set_Catch_Analysis.loc[:,['GearType']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_GearTypeProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()
            
            time.sleep(1)
            
            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['GearType'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'GearType':'GearTypeCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                            how='left', on ='GearTypeCode')
            Inv_DB_Set_Catch_Analysis1['GearTypeCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['GearTypeCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['GearTypeCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['GearTypeCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['GearTypeCode','GearTypeName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['GearTypeName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['GearTypeName']]).replace(np.nan, 'None')
            
            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['GearType', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'GearType':'GearTypeCode',
                                                        'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                        'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['GearTypeCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['GearTypeCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['GearTypeCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['GearTypeCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            window = Tk()
            window.title("GearType Code Statistics Report - ID-C-01-4")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - GearType Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="GearType Codes", anchor=CENTER)
            tree1.heading("#2", text="GearType Name", anchor=CENTER)
            tree1.heading("#3", text="Count By GearType", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="GearType Codes", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
            
            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()

        ## LookUp GearType Code Validation
        QCFailed_GearType = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_GearType()
        entryIDGearType = IntVar(QCFrame, value=4)
        entryTable_GearType = StringVar(QCFrame, value="GearType Codes Table")
        entryQCFailed_GearType = IntVar(QCFrame, value=QCFailed_GearType)

        entry_ID_GearType = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                            textvariable = entryIDGearType, width = 3, bd=2)
        entry_ID_GearType.grid(row =8, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_GearType = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_GearType, width = 30, bd=2)
        entry_Table_GearType.grid(row =8, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_GearType = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                    textvariable = entryQCFailed_GearType, width = 10, bd=2)
        entry_QCFailed_GearType.grid(row =8, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewGearTypeProfile = Button(QCFrame, text="GearType QC Failed Results \n (ID-C-01-4)", font=('aerial', 10, 'bold'),
                                            bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                            command = QCFailed_GearTypeResultViewer)
        btnViewGearTypeProfile.grid(row =8, column = 3, padx=50, pady =2, sticky =W)
        btnGearTypeCodeReport = Button(QCFrame, text="GearType Code Statistics \n (ID-C-01-4)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_GearTypeStat_Report)
        btnGearTypeCodeReport.grid(row =8, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_NAFODivision():
        ## Defining Functions For NAFODivision
        def QCFailed_NAFODivisionResultViewer():
            QCFailed_NAFODivision = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_NAFODivision()
            QCFailed_NAFODivisionCount = int(QCFailed_NAFODivision)
            if QCFailed_NAFODivisionCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_NAFODivision.SetCatch_ViewLookupValidatedResult_NAFODivision()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "NAFODivision Codes Validation All Passed. *** All NAFODivision Codes \
                in The Set & Catch Import are Validated Against NAFODivision Codes LookUp Table ****")

        def Generate_NAFODivisionStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'NAFODivision', 'Country'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['NAFODivision'] = (InvDB_Set_Catch_Analysis.loc[:,['NAFODivision']]).replace('', '99999999')
            InvDB_Set_Catch_Analysis['NAFODivision'] = (InvDB_Set_Catch_Analysis.loc[:,['NAFODivision']]).astype(str, errors='ignore')
            InvDB_Set_Catch_Analysis['NAFODivision'] = InvDB_Set_Catch_Analysis['NAFODivision'].str.strip()
            InvDB_Set_Catch_Analysis['NAFODivision'] = InvDB_Set_Catch_Analysis['NAFODivision'].str.replace(" ", "")
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            time.sleep(1)
            
            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['NAFODivision', 'Country'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'NAFODivision':'NAFODivisionCode', 'Country': 'CountryCode','DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)

            Inv_DB_Set_Catch_Analysis1['NAFODivisionCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['NAFODivisionCode']]).astype(str, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['NAFODivisionCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['NAFODivisionCode']]).replace('99999999', '')
            Inv_DB_Set_Catch_Analysis1= Inv_DB_Set_Catch_Analysis1.drop_duplicates(['NAFODivisionCode','CountryCode', 'TotalCount'],keep='last')          
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['NAFODivisionCode','CountryCode', 'TotalCount']]
            
            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['NAFODivision', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'NAFODivision':'NAFODivisionCode',
                                                       'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                       'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['NAFODivisionCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['NAFODivisionCode']]).astype(str, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['NAFODivisionCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['NAFODivisionCode']]).replace('99999999', '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            
            window = Tk()
            window.title("NAFODivision Code Statistics Report - ID-C-01-5")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - NAFODivision Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="NAFODivision Code", anchor=CENTER)
            tree1.heading("#2", text="Country Code", anchor=CENTER)
            tree1.heading("#3", text="Count By NAFODivision", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="NAFODivision Code", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
            
            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()

        ## LookUp NAFODivision Code Validation
        QCFailed_NAFODivision = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_NAFODivision()
        entryIDNAFODivision = IntVar(QCFrame, value=5)
        entryTable_NAFODivision = StringVar(QCFrame, value="NAFODivision Codes Table")
        entryQCFailed_NAFODivision = IntVar(QCFrame, value=QCFailed_NAFODivision)

        entry_ID_NAFODivision = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDNAFODivision, width = 3, bd=2)
        entry_ID_NAFODivision.grid(row =10, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_NAFODivision = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_NAFODivision, width = 30, bd=2)
        entry_Table_NAFODivision.grid(row =10, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_NAFODivision = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_NAFODivision, width = 10, bd=2)
        entry_QCFailed_NAFODivision.grid(row =10, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewNAFODivisionProfile = Button(QCFrame, text="NAFODivision QC Failed Results \n (ID-C-01-5)", font=('aerial', 10, 'bold'),
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_NAFODivisionResultViewer)
        btnViewNAFODivisionProfile.grid(row =10, column = 3, padx=50, pady =2, sticky =W)
        btnNAFODivisionCodeReport = Button(QCFrame, text="NAFODivision Code Statistics \n (ID-C-01-5)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_NAFODivisionStat_Report)
        btnNAFODivisionCodeReport.grid(row =10, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_UnitArea():
        ## Defining Functions For UnitArea
        def QCFailed_UnitAreaResultViewer():
            QCFailed_UnitArea = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_UnitArea()
            QCFailed_UnitAreaCount = int(QCFailed_UnitArea)
            if QCFailed_UnitAreaCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_UnitArea.SetCatch_ViewLookupValidatedResult_UnitArea()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "UnitArea Codes Validation All Passed. *** All UnitArea Codes \
                in The Set & Catch Import are Validated Against UnitArea Codes LookUp Table ****")

        def Generate_UnitAreaStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'NAFODivision', 'UnitArea'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['UnitArea'] = (InvDB_Set_Catch_Analysis.loc[:,['UnitArea']]).replace('', '99999999')
            InvDB_Set_Catch_Analysis['UnitArea'] = (InvDB_Set_Catch_Analysis.loc[:,['UnitArea']]).astype(str, errors='ignore')
            InvDB_Set_Catch_Analysis['UnitArea'] = InvDB_Set_Catch_Analysis['UnitArea'].str.strip()
            InvDB_Set_Catch_Analysis['UnitArea'] = InvDB_Set_Catch_Analysis['UnitArea'].str.replace(" ", "")
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            time.sleep(1)
            
            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['UnitArea', 'NAFODivision'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'UnitArea':'UnitAreaCode','NAFODivision':'NAFODivisionCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1['UnitAreaCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['UnitAreaCode']]).astype(str, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['UnitAreaCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['UnitAreaCode']]).replace('99999999', '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            
            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['UnitArea', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'UnitArea':'UnitAreaCode',
                                                       'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                       'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['UnitAreaCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['UnitAreaCode']]).astype(str, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['UnitAreaCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['UnitAreaCode']]).replace('99999999', '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            
            window = Tk()
            window.title("UnitArea Code Statistics Report - ID-C-01-6")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - UnitArea Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="UnitArea Code", anchor=CENTER)
            tree1.heading("#2", text="NAFODivision Code", anchor=CENTER)
            tree1.heading("#3", text="Count By UnitArea", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="UnitArea Code", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
            
            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()
                 
        ## LookUp UnitArea Code Validation
        QCFailed_UnitArea = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_UnitArea()
        entryIDUnitArea = IntVar(QCFrame, value=6)
        entryTable_UnitArea = StringVar(QCFrame, value="UnitArea Codes Table")
        entryQCFailed_UnitArea = IntVar(QCFrame, value=QCFailed_UnitArea)

        entry_ID_UnitArea = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDUnitArea, width = 3, bd=2)
        entry_ID_UnitArea.grid(row =12, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_UnitArea = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_UnitArea, width = 30, bd=2)
        entry_Table_UnitArea.grid(row =12, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_UnitArea = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_UnitArea, width = 10, bd=2)
        entry_QCFailed_UnitArea.grid(row =12, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewUnitAreaProfile = Button(QCFrame, text="UnitArea QC Failed Results \n (ID-C-01-6)", font=('aerial', 10, 'bold'),
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_UnitAreaResultViewer)
        btnViewUnitAreaProfile.grid(row =12, column = 3, padx=50, pady =2, sticky =W)
        btnUnitAreaCodeReport = Button(QCFrame, text="UnitArea Code Statistics \n (ID-C-01-6)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_UnitAreaStat_Report)
        btnUnitAreaCodeReport.grid(row =12, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_Quota():
        ## Defining Functions For Quota
        def QCFailed_QuotaResultViewer():
            QCFailed_Quota = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_Quota()
            QCFailed_QuotaCount = int(QCFailed_Quota)
            if QCFailed_QuotaCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_Quota.SetCatch_ViewLookupValidatedResult_Quota()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "Quota Codes Validation All Passed. *** All Quota Codes \
                in The Set & Catch Import are Validated Against Quota Codes LookUp Table ****")
        
        def Generate_QuotaStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'Quota'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['Quota'] = (InvDB_Set_Catch_Analysis.loc[:,['Quota']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['Quota'] = (InvDB_Set_Catch_Analysis.loc[:,['Quota']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_QuotaProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()

            time.sleep(1)

            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['Quota'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'Quota':'QuotaCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                            how='left', on ='QuotaCode')
            Inv_DB_Set_Catch_Analysis1['QuotaCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['QuotaCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['QuotaCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['QuotaCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['QuotaCode','QuotaName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['QuotaName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['QuotaName']]).replace(np.nan, 'None')

            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['Quota', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'Quota':'QuotaCode',
                                                        'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                        'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['QuotaCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['QuotaCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['QuotaCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['QuotaCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            window = Tk()
            window.title("Quota Code Statistics Report - ID-C-01-7")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - Quota Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="Quota Codes", anchor=CENTER)
            tree1.heading("#2", text="Quota Name", anchor=CENTER)
            tree1.heading("#3", text="Count By Quota", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="Quota Codes", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')

            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()
        
        ## LookUp Quota Code Validation
        QCFailed_Quota = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_Quota()
        entryIDQuota = IntVar(QCFrame, value=7)
        entryTable_Quota = StringVar(QCFrame, value="Quota Codes Table")
        entryQCFailed_Quota = IntVar(QCFrame, value=QCFailed_Quota)

        entry_ID_Quota = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDQuota, width = 3, bd=2)
        entry_ID_Quota.grid(row =14, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_Quota = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_Quota, width = 30, bd=2)
        entry_Table_Quota.grid(row =14, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_Quota = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_Quota, width = 10, bd=2)
        entry_QCFailed_Quota.grid(row =14, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewQuotaProfile = Button(QCFrame, text="Quota QC Failed Results \n (ID-C-01-7)", font=('aerial', 10, 'bold'),
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_QuotaResultViewer)
        btnViewQuotaProfile.grid(row =14, column = 3, padx=50, pady =2, sticky =W)
        btnQuotaCodeReport = Button(QCFrame, text="Quota Code Statistics \n (ID-C-01-7)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_QuotaStat_Report)
        btnQuotaCodeReport.grid(row =14, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_SetType():
        ## Defining Functions For SetType
        def QCFailed_SetTypeResultViewer():
            QCFailed_SetType = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_SetType()
            QCFailed_SetTypeCount = int(QCFailed_SetType)
            if QCFailed_SetTypeCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_SetType.SetCatch_ViewLookupValidatedResult_SetType()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "SetType Codes Validation All Passed. *** All SetType Codes \
                in The Set & Catch Import are Validated Against SetType Codes LookUp Table ****")

        def Generate_SetTypeStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'SetType'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['SetType'] = (InvDB_Set_Catch_Analysis.loc[:,['SetType']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['SetType'] = (InvDB_Set_Catch_Analysis.loc[:,['SetType']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_SetTypeProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()

            time.sleep(1)

            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['SetType'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'SetType':'SetTypeCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                            how='left', on ='SetTypeCode')
            Inv_DB_Set_Catch_Analysis1['SetTypeCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['SetTypeCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['SetTypeCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['SetTypeCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['SetTypeCode','SetTypeName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['SetTypeName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['SetTypeName']]).replace(np.nan, 'None')

            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['SetType', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'SetType':'SetTypeCode',
                                                        'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                        'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['SetTypeCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['SetTypeCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['SetTypeCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['SetTypeCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            window = Tk()
            window.title("SetType Code Statistics Report - ID-C-01-8")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - SetType Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="SetType Codes", anchor=CENTER)
            tree1.heading("#2", text="SetType Name", anchor=CENTER)
            tree1.heading("#3", text="Count By SetType", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="SetType Codes", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')

            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()

        ## LookUp SetType Code Validation
        QCFailed_SetType = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_SetType()
        entryIDSetType = IntVar(QCFrame, value=8)
        entryTable_SetType = StringVar(QCFrame, value="SetType Codes Table")
        entryQCFailed_SetType = IntVar(QCFrame, value=QCFailed_SetType)

        entry_ID_SetType = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDSetType, width = 3, bd=2)
        entry_ID_SetType.grid(row =16, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_SetType = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_SetType, width = 30, bd=2)
        entry_Table_SetType.grid(row =16, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_SetType = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_SetType, width = 10, bd=2)
        entry_QCFailed_SetType.grid(row =16, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewSetTypeProfile = Button(QCFrame, text="SetType QC Failed Results \n (ID-C-01-8)", font=('aerial', 10, 'bold'),
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_SetTypeResultViewer)
        btnViewSetTypeProfile.grid(row =16, column = 3, padx=50, pady =2, sticky =W)
        btnSetTypeCodeReport = Button(QCFrame, text="SetType Code Statistics \n (ID-C-01-8)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_SetTypeStat_Report)
        btnSetTypeCodeReport.grid(row =16, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_SpeciesCode():
        ## Defining Functions For SpeciesCode
        def QCFailed_SpeciesCodeResultViewer():
            QCFailed_SpeciesCode = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_SpeciesCode()
            QCFailed_SpeciesCodeCount = int(QCFailed_SpeciesCode)
            if QCFailed_SpeciesCodeCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_SpeciesCode.SetCatch_ViewLookupValidatedResult_SpeciesCode()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "SpeciesCode Codes Validation All Passed. *** All SpeciesCode Codes \
                in The Set & Catch Import are Validated Against SpeciesCode Codes LookUp Table ****")

        def Generate_SpeciesCodeStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'RecordType', 'SpeciesCode'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['SpeciesCode'] = (InvDB_Set_Catch_Analysis.loc[:,['SpeciesCode']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['SpeciesCode'] = (InvDB_Set_Catch_Analysis.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.loc[InvDB_Set_Catch_Analysis['RecordType'] == 2]
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_SpeciesCodeProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()

            time.sleep(1)

            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['SpeciesCode'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'SpeciesCode':'SpeciesCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                            how='left', on ='SpeciesCode')
            Inv_DB_Set_Catch_Analysis1['SpeciesCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['SpeciesCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['SpeciesCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['SpeciesCode','CommonName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['CommonName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['CommonName']]).replace(np.nan, 'None')

            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['SpeciesCode', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'SpeciesCode':'SpeciesCode',
                                                        'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                        'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['SpeciesCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['SpeciesCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['SpeciesCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            window = Tk()
            window.title("SpeciesCode Code Statistics Report - ID-C-01-9")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - SpeciesCode Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="SpeciesCode", anchor=CENTER)
            tree1.heading("#2", text="SpeciesCode Name", anchor=CENTER)
            tree1.heading("#3", text="Count By SpeciesCode", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="SpeciesCode", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')

            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()

        ## LookUp SpeciesCode Code Validation
        QCFailed_SpeciesCode = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_SpeciesCode()
        entryIDSpeciesCode = IntVar(QCFrame, value=9)
        entryTable_SpeciesCode = StringVar(QCFrame, value="SpeciesCode Codes Table")
        entryQCFailed_SpeciesCode = IntVar(QCFrame, value=QCFailed_SpeciesCode)

        entry_ID_SpeciesCode = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDSpeciesCode, width = 3, bd=2)
        entry_ID_SpeciesCode.grid(row =18, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_SpeciesCode = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_SpeciesCode, width = 30, bd=2)
        entry_Table_SpeciesCode.grid(row =18, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_SpeciesCode = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_SpeciesCode, width = 10, bd=2)
        entry_QCFailed_SpeciesCode.grid(row =18, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewSpeciesCodeProfile = Button(QCFrame, text="SpeciesCode QC Failed Results \n (ID-C-01-9)", font=('aerial', 10, 'bold'),
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_SpeciesCodeResultViewer)
        btnViewSpeciesCodeProfile.grid(row =18, column = 3, padx=50, pady =2, sticky =W)
        btnSpeciesCodeReport = Button(QCFrame, text="SpeciesCode Code Statistics \n (ID-C-01-9)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_SpeciesCodeStat_Report)
        btnSpeciesCodeReport.grid(row =18, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_DirectedSpecies():
        ## Defining Functions For DirectedSpecies
        def QCFailed_DirectedSpeciesResultViewer():
            QCFailed_DirectedSpecies = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_DirectedSpecies()
            QCFailed_DirectedSpeciesCount = int(QCFailed_DirectedSpecies)
            if QCFailed_DirectedSpeciesCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DirectedSpecies.SetCatch_ViewLookupValidatedResult_DirectedSpecies()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "DirectedSpecies Codes Validation All Passed. *** All DirectedSpecies Codes \
                in The Set & Catch Import are Validated Against DirectedSpecies Codes LookUp Table ****")

        def Generate_DirectedSpeciesStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'RecordType', 'DirectedSpecies'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['DirectedSpecies'] = (InvDB_Set_Catch_Analysis.loc[:,['DirectedSpecies']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['DirectedSpecies'] = (InvDB_Set_Catch_Analysis.loc[:,['DirectedSpecies']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_SpeciesCodeProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table, columns = ['SpeciesCode', 'CommonName'])
            Inv_DB_Lookup_Table.rename(columns={'SpeciesCode':'DirectedSpeciesCode', 'CommonName':'DirectedSpeciesName'},inplace = True)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()

            time.sleep(1)

            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['DirectedSpecies'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'DirectedSpecies':'DirectedSpeciesCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                                                    how='left', on ='DirectedSpeciesCode')
            Inv_DB_Set_Catch_Analysis1['DirectedSpeciesCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['DirectedSpeciesCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['DirectedSpeciesCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['DirectedSpeciesCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['DirectedSpeciesCode','DirectedSpeciesName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['DirectedSpeciesName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['DirectedSpeciesName']]).replace(np.nan, 'None')

            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['DirectedSpecies', 'DeploymentIdentifier'],as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'DirectedSpecies':'DirectedSpeciesCode',
                                                       'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                       'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['DirectedSpeciesCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['DirectedSpeciesCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['DirectedSpeciesCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['DirectedSpeciesCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            
            window = Tk()
            window.title("DirectedSpeciesCode Statistics Report - ID-C-01-10")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - DirectedSpeciesCode Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="DirectedSpeciesCode", anchor=CENTER)
            tree1.heading("#2", text="DirectedSpeciesCode Name", anchor=CENTER)
            tree1.heading("#3", text="Count By DirectedSpeciesCode", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="DirectedSpeciesCode", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')

            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()
        
        ## LookUp DirectedSpecies Code Validation
        QCFailed_DirectedSpecies = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_DirectedSpecies()
        entryIDDirectedSpecies = IntVar(QCFrame, value=10)
        entryTable_DirectedSpecies = StringVar(QCFrame, value="DirectedSpecies Codes Table")
        entryQCFailed_DirectedSpecies = IntVar(QCFrame, value=QCFailed_DirectedSpecies)

        entry_ID_DirectedSpecies = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDDirectedSpecies, width = 3, bd=2)
        entry_ID_DirectedSpecies.grid(row =20, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_DirectedSpecies = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_DirectedSpecies, width = 30, bd=2)
        entry_Table_DirectedSpecies.grid(row =20, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entry_QCFailed_DirectedSpecies = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_DirectedSpecies, width = 10, bd=2)
        entry_QCFailed_DirectedSpecies.grid(row =20, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewDirectedSpeciesProfile = Button(QCFrame, text="DirectedSpecies QC Failed Results \n (ID-C-01-10)", font=('aerial', 10, 'bold'),
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_DirectedSpeciesResultViewer)
        btnViewDirectedSpeciesProfile.grid(row =20, column = 3, padx=50, pady =2, sticky =W)
        btnDirectedSpeciesCodeReport = Button(QCFrame, text="DirectedSpecies Code Statistics \n (ID-C-01-10)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_DirectedSpeciesStat_Report)
        btnDirectedSpeciesCodeReport.grid(row =20, column = 4, padx=15, pady =2, sticky =W)

    def SimpleQC_TableLookUp_VesselClass():
        ## Defining Functions For VesselClass
        def QCFailed_VesselClassResultViewer():
            QCFailed_VesselClass = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_VesselClass()
            QCFailed_VesselClassCount = int(QCFailed_VesselClass)
            if QCFailed_VesselClassCount>0:
                    DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_VesselClass.SetCatch_ViewLookupValidatedResult_VesselClass()
            else:
                tkinter.messagebox.showinfo("LookUp Table Validation Message",
                "VesselClass Codes Validation All Passed. *** All VesselClass Codes \
                in The Set & Catch Import are Validated Against VesselClass Codes LookUp Table ****")

        def Generate_VesselClassStat_Report():
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)    
            InvDB_Set_Catch_Analysis = pd.read_sql_query("select * from DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn_DB_Set_Catch_Analysis)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis, columns = ['DataBase_ID', 'DeploymentUID', 'VesselClass'])
            Inv_DB_Set_Catch_Analysis = Inv_DB_Set_Catch_Analysis.reset_index(drop=True)
            InvDB_Set_Catch_Analysis['VesselClass'] = (InvDB_Set_Catch_Analysis.loc[:,['VesselClass']]).replace('', 99999999)
            InvDB_Set_Catch_Analysis['VesselClass'] = (InvDB_Set_Catch_Analysis.loc[:,['VesselClass']]).astype(int, errors='ignore')
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            InvDB_Set_Catch_Analysis['DeploymentIdentifier'] = InvDB_Set_Catch_Analysis['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            InvDB_Set_Catch_Analysis = InvDB_Set_Catch_Analysis.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis = pd.DataFrame(InvDB_Set_Catch_Analysis)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            conn_DB_Lookup_Table= sqlite3.connect(DB_Lookup_Table)    
            InvDB_Lookup_Table = pd.read_sql_query("select * from DFO_NL_ASOP_VesselClassProfile ;", conn_DB_Lookup_Table)
            Inv_DB_Lookup_Table = pd.DataFrame(InvDB_Lookup_Table)
            conn_DB_Lookup_Table.commit()
            conn_DB_Lookup_Table.close()

            time.sleep(1)

            Inv_DB_Set_Catch_Analysis1   = Inv_DB_Set_Catch_Analysis.groupby(['VesselClass'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis1   = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1.rename(columns={'VesselClass':'VesselClassCode', 'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis1 = pd.DataFrame(Inv_DB_Set_Catch_Analysis1)
            Inv_DB_Set_Catch_Analysis1 = pd.merge(Inv_DB_Set_Catch_Analysis1, Inv_DB_Lookup_Table,
                            how='left', on ='VesselClassCode')
            Inv_DB_Set_Catch_Analysis1['VesselClassCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['VesselClassCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis1['VesselClassCode'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['VesselClassCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis1 = Inv_DB_Set_Catch_Analysis1.loc[:,['VesselClassCode','VesselClassName', 'TotalCount']]
            Inv_DB_Set_Catch_Analysis1['VesselClassName'] = (Inv_DB_Set_Catch_Analysis1.loc[:,['VesselClassName']]).replace(np.nan, 'None')

            Inv_DB_Set_Catch_Analysis2   = Inv_DB_Set_Catch_Analysis.groupby(['VesselClass', 'DeploymentIdentifier'], as_index=False).DataBase_ID.count()
            Inv_DB_Set_Catch_Analysis2   = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            Inv_DB_Set_Catch_Analysis2.rename(columns={'VesselClass':'VesselClassCode',
                                                        'DeploymentIdentifier': 'DeploymentIdentifier', 
                                                        'DataBase_ID':'TotalCount'},inplace = True)
            Inv_DB_Set_Catch_Analysis2['VesselClassCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['VesselClassCode']]).astype(int, errors='ignore')
            Inv_DB_Set_Catch_Analysis2['VesselClassCode'] = (Inv_DB_Set_Catch_Analysis2.loc[:,['VesselClassCode']]).replace(99999999, '')           
            Inv_DB_Set_Catch_Analysis2 = Inv_DB_Set_Catch_Analysis2.reset_index(drop=True)
            Inv_DB_Set_Catch_Analysis2 = pd.DataFrame(Inv_DB_Set_Catch_Analysis2)
            window = Tk()
            window.title("VesselClass Code Statistics Report - ID-C-01-11")
            window.config(bg="ghost white")
            width = 1200
            height = 500
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width/2) - (width/2)
            y = (screen_height/2) - (height/2)
            window.geometry("%dx%d+%d+%d" % (width, height, x, y))
            window.grid_rowconfigure(1, weight=1)
            window.grid_columnconfigure(0, weight=1)
            window.resizable(0, 0)
            TitleFrame = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
            TitleFrame.pack(side = TOP)
            lblTitleFrame = Label(TitleFrame, font=('aerial', 12, 'bold'), text="** Set & Catch Statistical Summary - VesselClass Codes **", bg="aliceblue")
            lblTitleFrame.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
            TableMargin1 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin1.pack(side=LEFT)
            tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary1 = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
            scrollbary1.pack(side ='right', fill ='y')
            tree1.configure(yscrollcommand = scrollbary1.set)
            scrollbarx1 = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
            scrollbarx1.pack(side ='bottom', fill ='x')
            tree1.configure(xscrollcommand = scrollbarx1.set)
            tree1.heading("#1", text="VesselClass Codes", anchor=CENTER)
            tree1.heading("#2", text="VesselClass Name", anchor=CENTER)
            tree1.heading("#3", text="Count By VesselClass", anchor=CENTER)
            tree1.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree1.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
            tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
            tree1.pack()
            TableMargin2 = Frame(window, bd = 2, padx= 20, pady= 2, relief = RIDGE, bg="aliceblue")
            TableMargin2.pack(side=LEFT)
            tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"),selectmode="extended",
                                        height=20, show='headings')
            scrollbary2 = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
            scrollbary2.pack(side ='right', fill ='y')
            tree2.configure(yscrollcommand = scrollbary2.set)
            scrollbarx2 = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
            scrollbarx2.pack(side ='bottom', fill ='x')
            tree2.configure(xscrollcommand = scrollbarx2.set)
            tree2.heading("#1", text="VesselClass Codes", anchor=CENTER)
            tree2.heading("#2", text="DeploymentIdentifier (Year-ASOC-Deployment#)", anchor=CENTER)
            tree2.heading("#3", text="Event Count", anchor=CENTER)
            tree2.column('#1', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
            tree2.column('#2', stretch=NO, minwidth=0, width=420, anchor = tk.CENTER)
            tree2.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
            tree2.pack()
            style = ttk.Style(window)
            style.theme_use('clam')
            style.configure(".", font=('aerial', 10), foreground="black")
            style.configure("Treeview", foreground='black')
            style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')

            countIndex1 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis1)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis1.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(Inv_DB_Set_Catch_Analysis2)):
                if countIndex2 % 2 == 0:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(Inv_DB_Set_Catch_Analysis2.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")
            window.mainloop()
        
        ## LookUp VesselClass Code Validation
        QCFailed_VesselClass = DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult_DBCount.SetCatch_NumberOf_FailedQC_VesselClass()
        entryIDVesselClass = IntVar(QCFrame, value=11)
        entryTable_VesselClass = StringVar(QCFrame, value="VesselClass Codes Table")
        entryQCFailed_VesselClass = IntVar(QCFrame, value=QCFailed_VesselClass)

        entry_ID_VesselClass = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryIDVesselClass, width = 3, bd=2)
        entry_ID_VesselClass.grid(row =22, column = 0, padx=2, pady =2, ipady = 5, sticky =W)

        entry_Table_VesselClass = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, 
                                    textvariable = entryTable_VesselClass, width = 30, bd=2)
        entry_Table_VesselClass.grid(row =22, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        entryCount_QCFailed_VesselClass = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_VesselClass, width = 10, bd=2)
        entryCount_QCFailed_VesselClass.grid(row =22, column = 2, padx=20, pady =2, ipady = 5, sticky =W)

        btnViewVesselClassProfile = Button(QCFrame, text="VesselClass QC Failed Results \n (ID-C-01-11)", font=('aerial', 10, 'bold'),
                                        bg ="aliceblue", height =2, width=28, bd=2, anchor="c", padx=10,
                                        command = QCFailed_VesselClassResultViewer)
        btnViewVesselClassProfile.grid(row =22, column = 3, padx=50, pady =2, sticky =W)
        btnVesselClassCodeReport = Button(QCFrame, text="VesselClass Code Statistics \n (ID-C-01-11)", font=('aerial', 10, 'bold'), 
                                        bg ="aliceblue", height =2, width=25, bd=2, anchor="c", padx=5,
                                        command = Generate_VesselClassStat_Report)
        btnVesselClassCodeReport.grid(row =22, column = 4, padx=15, pady =2, sticky =W)

    SimpleQC_TableLookUp_ASOCCode()
    SimpleQC_TableLookUp_Country()
    SimpleQC_TableLookUp_DataSource()
    SimpleQC_TableLookUp_GearDamage()
    SimpleQC_TableLookUp_GearType()
    SimpleQC_TableLookUp_NAFODivision()
    SimpleQC_TableLookUp_UnitArea()
    SimpleQC_TableLookUp_Quota()
    SimpleQC_TableLookUp_SetType()
    SimpleQC_TableLookUp_SpeciesCode()
    SimpleQC_TableLookUp_DirectedSpecies()
    SimpleQC_TableLookUp_VesselClass()

    lbl_Total_QCFailed = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Failed In QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCFailed.grid(row =0, column = 3, padx=4, pady =2)
    Set_Catch_TotalFailed = (QCFailed_ASOCCode+QCFailed_Country+\
                            QCFailed_DataSource+QCFailed_GearDamage+\
                            QCFailed_GearType+QCFailed_NAFODivision+\
                            QCFailed_UnitArea+QCFailed_Quota+\
                            QCFailed_SetType+QCFailed_SpeciesCode+\
                            QCFailed_DirectedSpecies+QCFailed_VesselClass
                           )
    Total_QC_Failed = IntVar(Topframe, value=Set_Catch_TotalFailed)
    entry_Total_QCFailed = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Failed, width = 8, bd=2)
    entry_Total_QCFailed.grid(row =1, column = 3, padx=1, pady =5)

    ## Defining Reload Functions
    def ReloadQCFailedSummary():
        entry_Total_QCFailed.delete(0,END)
        Reload_SetCatch_RunLookUpTableValidation = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation.SetCatch_RunLookUpTableValidation()
        TotalFailedQC_LookUpTable = Reload_SetCatch_RunLookUpTableValidation[1]
        entry_Total_QCFailed.insert(tk.END,TotalFailedQC_LookUpTable)
        SimpleQC_TableLookUp_ASOCCode()
        SimpleQC_TableLookUp_Country()
        SimpleQC_TableLookUp_DataSource()
        SimpleQC_TableLookUp_GearDamage()
        SimpleQC_TableLookUp_GearType()
        SimpleQC_TableLookUp_NAFODivision()
        SimpleQC_TableLookUp_UnitArea()
        SimpleQC_TableLookUp_Quota()
        SimpleQC_TableLookUp_SetType()
        SimpleQC_TableLookUp_SpeciesCode()
        SimpleQC_TableLookUp_DirectedSpecies()
        SimpleQC_TableLookUp_VesselClass()
        
    ## Defining Bottom Frame
    BottomFrame = Frame(root, bd = 2, padx= 3, pady= 1, relief = RIDGE, bg="aliceblue")
    BottomFrame.pack(side = BOTTOM)
    btnRefreashReload = Button(BottomFrame, text="Reload QC Failed Summary", font=('aerial', 12, 'bold'), 
                                        bg ="aliceblue", height =2, width=22, bd=2, anchor=tk.CENTER, padx=5,
                                        command = ReloadQCFailedSummary)
    btnRefreashReload.grid(row =0, column = 0, padx=1, pady =1, sticky =W)

    root.mainloop()
