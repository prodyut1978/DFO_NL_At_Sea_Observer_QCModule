#Front End
from tkinter import*
import tkinter.messagebox
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import sqlite3
import pandas as pd
import numpy as np
from pandastable import Table, config

## Database connections
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_Set_Catch_Misc = ("./BackEnd/Sqlite3_DB/SetCatch_Misc_DB/DFO_NL_ASOP_Set_Catch_Misc.db")

def ViewImportQCFailResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Set & Catch Validator")
    window.geometry("1080x833+200+100")
    window.config(bg="cadet blue")

    ## Top Frame
    Topframe = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Topframe.pack(side = TOP)

    txtDisplayMessageSystem = Listbox(Topframe, font=('aerial', 9, 'bold'), 
                                      height =2, width =80)
    txtDisplayMessageSystem.grid(row =0, column = 0, padx=200, pady =5, ipady =5, sticky =E)

    lbl_QCDisplay = Label(Topframe, font=('aerial', 10, 'bold'), text="A: QCFailed Display Table:")
    lbl_QCDisplay.grid(row =0, column = 0, padx=2, pady =1, sticky =W)

    lbl_TombstoneFailedEntries = Label(Topframe, font=('aerial', 10 , 'bold'), bg= "cadet blue", text="#Tombstone QC Failed :")
    lbl_TombstoneFailedEntries.grid(row =2, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    TombstoneFailedEntries = IntVar(Topframe, value='')
    txtTombstoneFailedEntries = Entry(Topframe, font=('aerial',10, 'bold'),textvariable = TombstoneFailedEntries, width = 5, bd=1)
    txtTombstoneFailedEntries.grid(row =2, column = 0, padx=170, pady =1, ipady =1, sticky =W)

    txtQCVariable = Entry(Topframe, font=('aerial', 9, 'bold'), justify = tk.CENTER,
                            textvariable = StringVar(window, value='QC Variable'), width = 22, bd=2)
    txtQCVariable.grid(row =2, column = 0, padx=284, pady =2, ipady =5, sticky =E)
    
    lbl_DuplicatedeEntries = Label(Topframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text="#Duplicate UID QC Failed :")
    lbl_DuplicatedeEntries.grid(row =2, column = 0, padx=60, pady =1, sticky =E)
    DuplicatedeEntries       = IntVar(Topframe, value ='')
    txtDuplicatedeEntries = Entry(Topframe, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = DuplicatedeEntries, width = 6, bd=1)
    txtDuplicatedeEntries.grid(row =2, column = 0, padx=2, pady =1, ipady =1, sticky =E)

    ## Table Frame Define
    Tableframe = tk.Frame(window, width = 40)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    
    ## SelectViewResultsRun Frame Wizard :
    SelectViewResultsRun = Frame(Tableframe, width = 80)
    SelectViewResultsRun.pack(side = TOP, padx= 0, pady=0, anchor=W)
    ListVariableListA = ['Select QC Failure type From DropDown List', 
                         'Case-A Tombstone QC Check Failure',
                         'Case-B Duplicate DeploymentUID Failure']
    VariableList        = StringVar(SelectViewResultsRun, value ='')
    entry_ViewVarResults  = ttk.Combobox(SelectViewResultsRun, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable = VariableList, width = 40, state='readonly')
    entry_ViewVarResults.grid(row =0, column = 0, padx=2, pady =4, ipady= 4, sticky =W)
    entry_ViewVarResults['values'] = ListVariableListA
    entry_ViewVarResults.current(0)
    
    txtSearchDepUID = Entry(SelectViewResultsRun, font=('aerial', 10, 'bold'), justify = tk.CENTER,
                            textvariable = StringVar(window, value='Entry DeploymentUID'), width = 22, bd=2)
    txtSearchDepUID.grid(row =0, column = 1, padx=315, pady =2, ipady =5, sticky =W)
    
    ## Tree1 Define
    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", 
                    "column4", "column5", "column6",
                     "column7"), height=20, show='headings')
    scrollbary = ttk.Scrollbar(Tableframe, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(Tableframe, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 8), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', 
                    foreground='blue',fieldbackground='Ghost White')
    tree1.heading("#1", text="Year", anchor=CENTER)
    tree1.heading("#2", text="ASOCCode", anchor=CENTER)
    tree1.heading("#3", text="DeploymentNumber", anchor=CENTER)
    tree1.heading("#4", text="SetNumber", anchor=CENTER)
    tree1.heading("#5", text="DeploymentUID", anchor=CENTER)
    tree1.heading("#6", text="QC_Variable", anchor=W)
    tree1.heading("#7", text="QC_Message", anchor=W)
    tree1.column('#1', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    tree1.column('#6', stretch=NO, minwidth=0, width=200, anchor = W)            
    tree1.column('#7', stretch=NO, minwidth=0, width=320, anchor = W)
    style = ttk.Style(Tableframe)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 8), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)

    ##### Frame Generate QC Failed Summary ############
    SummaryQCframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.pack(side =LEFT, padx=10, pady =2)
    lbl_SummaryQCframe = Label(SummaryQCframe, font=('aerial', 12, 'bold','underline'), 
                                bg= "cadet blue", text="B: QC Summary")
    lbl_SummaryQCframe.pack(side =TOP)
    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    Summaryframetree = ttk.Treeview(Summaryframe, column=("column1", "column2"),
                                    height=4, show='headings')
    Summaryframetree.heading("#1", text="QC Variable Name")
    Summaryframetree.heading("#2", text="# Of Entries Fail In QC")
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=188)            
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=185, anchor = tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    Summaryframetree.pack(side = BOTTOM)
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    SummaryDisplay.pack(side = BOTTOM, pady=0)
    txtSummaryDisplayMsg = Entry(SummaryDisplay, font=('aerial', 10),
                            textvariable = StringVar(window, value='QC Summary Message'), width = 50, bd=2)
    txtSummaryDisplayMsg.grid(row =0, column = 0, padx=10, pady =2, ipady =5, sticky =E)
    lbl_ToUpdateEntriesCount = Label(SummaryDisplay, font=('aerial', 9 , 'bold'), text="TotalEntries To Update")
    lbl_ToUpdateEntriesCount.grid(row =2, column = 0, padx=2, pady =1, ipady=1, sticky =E)
    ToUpdateEntriesCount = IntVar(SummaryDisplay, value='')
    txtToUpdateEntriesCount = Entry(SummaryDisplay, font=('aerial',8),
                                   textvariable = ToUpdateEntriesCount, 
                                   width = 8, bd=1)
    txtToUpdateEntriesCount.grid(row =4, column = 0, padx=20, pady =2, ipady =2, sticky =E)
    lbl_AlreadyUpdateEntriesCount = Label(SummaryDisplay, font=('aerial', 9 , 'bold'), text="TotalEntries Updated")
    lbl_AlreadyUpdateEntriesCount.grid(row =2, column = 0, padx=2, pady =1, ipady=1, sticky =W)
    AlreadyUpdateEntriesCount = IntVar(SummaryDisplay, value='')
    txtAlreadyUpdateEntriesCount = Entry(SummaryDisplay, font=('aerial',8),
                                   textvariable = AlreadyUpdateEntriesCount, 
                                   width = 8, bd=1)
    txtAlreadyUpdateEntriesCount.grid(row =4, column = 0, padx=20, pady =2, ipady =2, sticky =W)

    #### Frame Of Selected Results Overview modules #####
    SelQCVariableDisplay = tk.Frame(window, bg= "aliceblue")
    SearchDepNumSetCatchDB      = StringVar(SelQCVariableDisplay, value ='')
    entry_SearchDepNumSetCatchDB = Entry(SelQCVariableDisplay, font=('aerial', 10, 'bold'),  justify = tk.CENTER,
                            textvariable = SearchDepNumSetCatchDB, width = 8, bd=2)
    entry_SearchDepNumSetCatchDB.grid(row =0, column = 0, padx=2, pady =2, ipady =2, sticky =W)

    SelQCVariable      = StringVar(SelQCVariableDisplay, value ='QCVariable ↓↓')
    entry_SelQCVariable = Entry(SelQCVariableDisplay, font=('aerial', 10, 'bold'),  justify = tk.CENTER,
                            textvariable = SelQCVariable, width = 28, bd=1)
    entry_SelQCVariable.grid(row =0, column = 1, padx=150, pady =2, ipady =2, sticky =W)

    SelQCVariableDisplay.pack(side = TOP, pady=0, anchor = CENTER)
    SelResultOverview = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SelResultOverview.pack(side =LEFT, padx=1, pady =2)
    SelResultOverviewtree = ttk.Treeview(SelResultOverview,  
                                         column=("column1", "column2", 
                                                 "column3", "column4"), height=9, show='headings')
    scrollbary = ttk.Scrollbar(SelResultOverview, orient ="vertical", command=SelResultOverviewtree.yview)
    scrollbary.pack(side ='right', fill ='y')
    SelResultOverviewtree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(SelResultOverview, orient ="horizontal", command=SelResultOverviewtree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    SelResultOverviewtree.configure(xscrollcommand = scrollbarx.set)
    SelResultOverviewtree.heading("#1", text="Year", anchor=CENTER)
    SelResultOverviewtree.heading("#2", text="ASOCCode", anchor=CENTER)
    SelResultOverviewtree.heading("#3", text="DeploymentNumber", anchor=CENTER)
    SelResultOverviewtree.heading("#4", text="# Of Set QC Fail", anchor=CENTER)
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)             
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    SelResultOverviewtree.column('#4', stretch=NO, minwidth=0, width=220, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = TOP)

    #######All Defined Functions #########
    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def ClearTablesAll():
        tree1.delete(*tree1.get_children())
        SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
        entry_ViewVarResults.current(0)
        txtSearchDepUID.delete(0,END)
        txtQCVariable.delete(0,END)
        entry_SelQCVariable.delete(0,END)
        entry_SelQCVariable.insert(tk.END,'QCVariable ↓↓')
        txtDisplayMessageSystem.delete(0,END)
        
    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select QC Failure type From DropDown List', 
                         'Case-A Tombstone QC Check Failure',
                         'Case-B Duplicate DeploymentUID Failure']
        try:
            con= sqlite3.connect(DB_Set_Catch_Misc)
            cur=con.cursor()
            if getVarnameToView == ListVariableListA[1]:
                cur.execute("SELECT * FROM DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport")
            if getVarnameToView == ListVariableListA[2]:
                cur.execute("SELECT * FROM DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport")
            rows=cur.fetchall()
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_VariablesProfile():
        ListVariableListA = ['Select QC Failure type From DropDown List', 
                         'Case-A Tombstone QC Check Failure',
                         'Case-B Duplicate DeploymentUID Failure']
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows.rename(columns={0:'Year', 1:'ASOCCode', 
                            2:'DeploymentNumber', 3:'SetNumber',
                            4:'DeploymentUID', 5:'QC_Variable',
                            6:'QC_Message'},inplace = True)
        
        if (len(rows) == 0) | (getVarnameToView == ListVariableListA[0]):
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Select QC Case Type From DropDown & Run View Selected Button')
            txtDisplayMessageSystem.insert(2, 'Nothing to Display')
            
        if (len(rows) >0) & (getVarnameToView == ListVariableListA[1]):
            rows = rows.loc[:,
                    ['Year','ASOCCode','DeploymentNumber',
                    'SetNumber', 'DeploymentUID', 'QC_Variable', 'QC_Message']]
            rows.sort_values(by=['Year','ASOCCode','DeploymentNumber',
                'SetNumber'], inplace=True)
            rows  = rows.reset_index(drop=True)
            rows  = pd.DataFrame(rows)
            countIndex1 = 0
            for each_rec in range(len(rows)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightgreen")
            tree1.tag_configure("odd",foreground="black", background="ghost white")
            
        if (len(rows) >0) & (getVarnameToView == ListVariableListA[2]):
            rows = rows.loc[:,
                    ['Year','ASOCCode','DeploymentNumber',
                    'SetNumber', 'DeploymentUID', 'QC_Variable', 'QC_Message']]
            rows.sort_values(by=['Year','ASOCCode','DeploymentNumber',
                'SetNumber'], inplace=True)
            rows  = rows.reset_index(drop=True)
            rows  = pd.DataFrame(rows)
            countIndex1 = 0
            for each_rec in range(len(rows)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")
            
    def QCFailedTotalEntries():
        txtTombstoneFailedEntries.delete(0,END)
        txtDuplicatedeEntries.delete(0,END)
        conn = sqlite3.connect(DB_Set_Catch_Misc)
        TombstoneQCFailDF= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport;", conn)
        DuplicateUIDQCFailDF= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport;", conn)
        conn.commit()
        conn.close()
        Len_TombstoneQCFailDF = len(TombstoneQCFailDF)
        Len_DuplicateUIDQCFailDF = len(DuplicateUIDQCFailDF)
        txtTombstoneFailedEntries.insert(tk.END,Len_TombstoneQCFailDF)
        txtDuplicatedeEntries.insert(tk.END,Len_DuplicateUIDQCFailDF)
        gettotalQCfailCount = Len_TombstoneQCFailDF + Len_DuplicateUIDQCFailDF
        return gettotalQCfailCount                     
 
    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return
    
    def callbackFuncSelectView(event):
        ListVariableListA = ['Select QC Failure type From DropDown List', 
                            'Case-A Tombstone QC Check Failure',
                            'Case-B Duplicate DeploymentUID Failure']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            tree1.delete(*tree1.get_children())
            
        if(SelVariableView ==ListVariableListA[0]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Select Case A Or B Or C & Press Selected Results Button To View ')
            
        if(SelVariableView ==ListVariableListA[1]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Set Record Plus Catch Record Validation ()')
            txtDisplayMessageSystem.insert(2,' RecordType 1 and RecordType 2 Data Is The Same For Columns 1-51')
            
        if(SelVariableView ==ListVariableListA[2]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Duplicated RecordType1 DeploymentUID Validation')
            txtDisplayMessageSystem.insert(2,' Multiple Duplicated DeploymentUID For RecordType1 In A Set')
        
    def GenSummaryQC():
        txtToUpdateEntriesCount.delete(0,END)
        txtAlreadyUpdateEntriesCount.delete(0,END)
        gettotalQCfailCount = QCFailedTotalEntries()
        conn = sqlite3.connect(DB_Set_Catch_Misc)
        TombstoneQCFailDF= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport;", conn)
        DuplicateUIDQCFailDF= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport;", conn)
        conn.commit()
        conn.close()

        DupUID_Update = DuplicateUIDQCFailDF[(
            (DuplicateUIDQCFailDF.QC_Message != 'Updated - DuplicatedUID Failed')&
            (DuplicateUIDQCFailDF.QC_Message != 'Updated - From Deployment Search'))]
        
        TombstoneQCFailDF ['QC_Message_M'] = TombstoneQCFailDF['QC_Message'].str.slice(0, 7)
        Tombston_Update = TombstoneQCFailDF[(
            (TombstoneQCFailDF.QC_Message_M != 'Updated')&
            (TombstoneQCFailDF.QC_Message != 'Updated - From Deployment Search'))]
        
        TotalEntriesToUpdate = len(DupUID_Update)+ len(Tombston_Update)
        TotalEntriesUpdated = gettotalQCfailCount - TotalEntriesToUpdate
        
        ## For TombstoneQCFailDF
        if len(TombstoneQCFailDF) >0:
            Count_TombstoneQCFailDF = len(TombstoneQCFailDF)
        else:
            Count_TombstoneQCFailDF = 0
        
        ## For DuplicateUIDQCFailDF
        if len(DuplicateUIDQCFailDF) >0:
            Count_DuplicateUIDQCFailDF = len(DuplicateUIDQCFailDF)
        else:
            Count_DuplicateUIDQCFailDF = 0
        
        ### Building Summary DF
        ListFailedConsistency = ['Tombstone QC Fail',
                                 'DuplicateUID QC Fail'
                                ]
        NumFailedConsistency = [Count_TombstoneQCFailDF,
                                Count_DuplicateUIDQCFailDF]
        
        Append_List = {'VariableName': ListFailedConsistency, 
                      'QCFailCount': NumFailedConsistency} 
        FailedDF = pd.DataFrame(Append_List)
        FailedDF[['QCFailCount']] = FailedDF[['QCFailCount']].astype(int)
        FailedDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
        FailedDF  = FailedDF.reset_index(drop=True)
        FailedDF  = pd.DataFrame(FailedDF)
        Summaryframetree.delete(*Summaryframetree.get_children())
        SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
        countIndex1 = 0
        for each_rec in range(len(FailedDF)):
            if countIndex1 % 2 == 0:
                Summaryframetree.insert("", tk.END, values=list(FailedDF.loc[each_rec]), tags =("even",))
            else:
                Summaryframetree.insert("", tk.END, values=list(FailedDF.loc[each_rec]), tags =("odd",))
            countIndex1 = countIndex1+1
        Summaryframetree.tag_configure("even",foreground="black", background="lightblue")
        Summaryframetree.tag_configure("odd",foreground="black", background="lightgreen")
        txtSummaryDisplayMsg.delete(0,END)
        txtSummaryDisplayMsg.insert(tk.END,"QC Summary Generated. Select & View Each From List")

        ##Populating ToUpdateEntriesCount & AlreadyUpdateEntriesCount
        txtToUpdateEntriesCount.insert(tk.END,TotalEntriesToUpdate)
        txtAlreadyUpdateEntriesCount.insert(tk.END,TotalEntriesUpdated)

    def InventoryRec1(event):
        curItems = tree1.selection()
        if len(curItems)==1:
            sd = tree1.item(curItems, 'values')
            SelvariableIdentifier = sd[4]
            QCVariable = sd[5]
            txtSearchDepUID.delete(0,END)
            txtSearchDepUID.insert(tk.END,SelvariableIdentifier)
            txtQCVariable.delete(0,END)
            txtQCVariable.insert(tk.END,QCVariable)
       
    def InventoryRec3(event):
        ListVariableListA = ['Tombstone QC Fail',
                             'DuplicateUID QC Fail']
        ## Summary frame Table B Selection
        nm =Summaryframetree.selection()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            NumberEntriesInSet = sd[1]
            txtSummaryDisplayMsg.delete(0,END)
            txtSummaryDisplayMsg.insert(tk.END,((" Type : ") +
                                                SelvariableIdentifier + ' ' +' & '+
                                                "# Fail: " + 
                                                NumberEntriesInSet))
            
            if (int(NumberEntriesInSet) > 0):
                ## Main Table A Displaying 
                if(SelvariableIdentifier ==ListVariableListA[0]):
                    tree1.delete(*tree1.get_children())
                    entry_SelQCVariable.delete(0,END)
                    entry_SelQCVariable.insert(tk.END,ListVariableListA[0])
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'Set Record Plus Catch Record Validation')
                    txtDisplayMessageSystem.insert(2,'RecordType 1 and RecordType 2 Data Is The Same For Columns 1-51')
                    entry_ViewVarResults.current(1)
                    viewQCFailed_VariablesProfile()
                    SelectQCVarOverview(SelvariableIdentifier)
                
                if(SelvariableIdentifier ==ListVariableListA[1]):
                    tree1.delete(*tree1.get_children())
                    entry_SelQCVariable.delete(0,END)
                    entry_SelQCVariable.insert(tk.END,ListVariableListA[1])
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'Duplicated RecordType1 DeploymentUID Validation')
                    txtDisplayMessageSystem.insert(2, 'Multiple Duplicated DeploymentUID For RecordType1 In A Set')
                    entry_ViewVarResults.current(2)
                    viewQCFailed_VariablesProfile()
                    SelectQCVarOverview(SelvariableIdentifier)
           
            else:
                txtSummaryDisplayMsg.delete(0,END)
                txtSummaryDisplayMsg.insert(tk.END,"Empty QCCaseType - All Updated Or No Fail Found")
                tree1.delete(*tree1.get_children())
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                entry_ViewVarResults.current(0)
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(tk.END,"Empty QCCaseType - All Updated Or No Fail Found")
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, (' Please Select Only One Entries To View'))
            txtSummaryDisplayMsg.delete(0,END)
            txtSummaryDisplayMsg.insert(tk.END,"Please Select Only One Entries To View")
            entry_SelQCVariable.delete(0,END)
            entry_SelQCVariable.insert(tk.END,"QCVariable ↓↓")

    def SelectQCVarOverview(QCVarName):
        ListVariableListA = ['Tombstone QC Fail',
                             'DuplicateUID QC Fail']
        conn = sqlite3.connect(DB_Set_Catch_Misc)
        TombstoneQCFailDF= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport;", conn)
        DuplicateUIDQCFailDF= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport;", conn)
        conn.commit()
        conn.close()
        TombstoneQCFailDF = pd.DataFrame(TombstoneQCFailDF)
        DuplicateUIDQCFailDF = pd.DataFrame(DuplicateUIDQCFailDF)
       
        ## For TombstoneQCFailDF
        if(QCVarName ==ListVariableListA[0]):
            Summary_Tombstone= TombstoneQCFailDF.groupby(
            ['Year','ASOCCode','DeploymentNumber'],  
            as_index=False)
            Summary_Tombstone = Summary_Tombstone.agg({"SetNumber": "count"})
            Summary_Tombstone.sort_values(by=['Year','ASOCCode','DeploymentNumber'], inplace=True)
            Summary_Tombstone = Summary_Tombstone.reset_index(drop=True)
            Summary_Tombstone = pd.DataFrame(Summary_Tombstone)
            SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
            countIndex2 = 0
            for each_rec in range(len(Summary_Tombstone)):
                if countIndex2 % 2 == 0:
                    SelResultOverviewtree.insert("", tk.END, values=list(Summary_Tombstone.loc[each_rec]), tags =("even",))
                else:
                    SelResultOverviewtree.insert("", tk.END, values=list(Summary_Tombstone.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            SelResultOverviewtree.tag_configure("even",foreground="black", background="lightgreen")
            SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
        
        ## For DuplicateUIDQCFailDF
        if(QCVarName ==ListVariableListA[1]):
            Summary_Duplicate= DuplicateUIDQCFailDF.groupby(
            ['Year','ASOCCode','DeploymentNumber'],  
            as_index=False)
            Summary_Duplicate = Summary_Duplicate.agg({"SetNumber": "count"})
            Summary_Duplicate.sort_values(by=['Year','ASOCCode','DeploymentNumber'], inplace=True)
            Summary_Duplicate = Summary_Duplicate.reset_index(drop=True)
            Summary_Duplicate = pd.DataFrame(Summary_Duplicate)
            SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
            countIndex2 = 0
            for each_rec in range(len(Summary_Duplicate)):
                if countIndex2 % 2 == 0:
                    SelResultOverviewtree.insert("", tk.END, values=list(Summary_Duplicate.loc[each_rec]), tags =("even",))
                else:
                    SelResultOverviewtree.insert("", tk.END, values=list(Summary_Duplicate.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            SelResultOverviewtree.tag_configure("even",foreground="black", background="lightblue")
            SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
        
    def InventoryRec4(event):
        nm =SelResultOverviewtree.selection()
        if len(nm) ==1:
            sd = SelResultOverviewtree.item(nm, 'values')
            SelvariableIdentifier = sd[2]
            entry_SearchDepNumSetCatchDB.delete(0,END)
            entry_SearchDepNumSetCatchDB.insert(tk.END,SelvariableIdentifier) 
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, (' Please Select Only One Entries To View'))

    def UpdateDeploymentUIDAfterUpdate():
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT;", conn)
                if len(Complete_df) >0:
                    UpdatedSetcatchDF = pd.DataFrame(Complete_df)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,
                        ['RecordIdentifier','Year','ASOCCode',
                            'DeploymentNumber','SetNumber']]
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(np.nan, 99999999)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace('', 99999999)
                    SetCatchQCFailedDB_DF[['RecordIdentifier',
                                            'Year','ASOCCode','DeploymentNumber',
                                            'SetNumber']] = SetCatchQCFailedDB_DF[
                                            ['RecordIdentifier',
                                            'Year','ASOCCode','DeploymentNumber',
                                            'SetNumber']].astype(int)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(99999999, '')
                    SetCatchQCFailedDB_DF['DeploymentUID'] = SetCatchQCFailedDB_DF["Year"].map(str) + "-" + \
                                                            SetCatchQCFailedDB_DF["ASOCCode"].map(str)+ "-" +\
                                                            SetCatchQCFailedDB_DF["DeploymentNumber"].map(str)+"-"+ \
                                                            SetCatchQCFailedDB_DF["SetNumber"].map(str)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier','DeploymentUID',
                                                                        'Year','ASOCCode','DeploymentNumber',
                                                                        'SetNumber']]
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    UpdatedSetcatchDF.update(SetCatchQCFailedDB_DF)
                    return UpdatedSetcatchDF
                else:
                    return Complete_df
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        ## Get Set And Catch DB Profile
        SetCatchQCFailedDB_DF = GetSetCatchProfileDB()
        # DB Update Executing
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        SetCatchQCFailedDB_DF.to_sql('DFO_NL_ASOP_Set_Catch_TEMP_IMPORT', 
            conn_DB_Set_Catch_Analysis, if_exists="replace",index = False)                         
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        tree1.delete(*tree1.get_children())
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    def SearchDepNumFromSetCatchDB():
        get_DepNumforSearch = (entry_SearchDepNumSetCatchDB.get())
        get_SelQCVariable = entry_SelQCVariable.get()
        if (len(get_DepNumforSearch)) > 0:
            try:
                get_DepNumforSearch = int(get_DepNumforSearch)
            except:
                messagebox.showerror('Search Variable Datatype Error Message', "Search Value Must Be Integer Value")
            checkinttype = isinstance(get_DepNumforSearch,int)
            if checkinttype == True:  
                conn_DB= sqlite3.connect(DB_Set_Catch_Analysis)
                if (get_DepNumforSearch) >= 0:        
                    get_SearchSingleVariable_Value = (get_DepNumforSearch)
                    rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT;", conn_DB)
                    conn_DB.commit()
                    conn_DB.close()
                    
                    rows = rows[(rows.DeploymentNumber) == get_SearchSingleVariable_Value]
                    rows  = rows.reset_index(drop=True)
                    rows  = pd.DataFrame(rows)
                    rows.sort_values(by=['ASOCCode','ObserverNumber',
                                'DeploymentNumber','SetNumber',
                                'RecordType'], inplace=True)
                    SearchDepNSetCatchDF = pd.DataFrame(rows)
                    SearchDepNSetCatchDF = SearchDepNSetCatchDF.loc[:,
                                ['RecordIdentifier','DeploymentUID',
                                'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                                'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                                'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                                'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                                'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                                'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                                'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                                'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                                'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                                'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                'NumberIndividuals']]
                    SearchDepNSetCatchDF = SearchDepNSetCatchDF.reset_index(drop=True)
                    Merge_WithSetCatchDB = pd.DataFrame(SearchDepNSetCatchDF)
                    
                    if len(Merge_WithSetCatchDB) >0:
                        windows = tk.Toplevel()
                        windows.title ("Excel Table View Observer Set & Catch QC Database")
                        windows.geometry('1600x755+40+40')
                        windows.config(bg="cadet blue")
                        frame = tk.Frame(windows)
                        frame.pack(fill=BOTH, expand=1)
                        pt = Table(frame, dataframe = Merge_WithSetCatchDB, showtoolbar=True, showstatusbar=True)
                        pt.setRowColors(rows=range(1,len(Merge_WithSetCatchDB),2), clr='lightblue', cols='all')
                        pt.cellbackgr = 'aliceblue'
                        options = config.load_options()
                        options = { 'align': 'center',
                                    'cellbackgr': '#F4F4F3',
                                    'cellwidth': 120,
                                    'floatprecision': 2,
                                    'thousandseparator': '',
                                    'font': 'Arial',
                                    'fontsize': 8,
                                    'fontstyle': '',
                                    'grid_color': '#ABB1AD',
                                    'linewidth': 1,
                                    'rowheight': 22,
                                    'rowselectedcolor': '#E4DED4',
                                    'textcolor': 'black'}
                        config.apply_options(options, pt)
                        pt.show()
                        
                        ## Define Functions
                        def SubmitToUpdateDB():
                            Complete_df = pd.DataFrame(pt.model.df)
                            Complete_df= (Complete_df.loc[:,
                                    ['RecordIdentifier','DeploymentUID',
                                    'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                                    'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                                    'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                                    'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                                    'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                                    'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                                    'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                                    'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                    'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                                    'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                                    'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                    'NumberIndividuals']]).replace(['', None, np.nan, 
                                    'None', ' ', '  ', '   ', '    '], 99999999)
                            Complete_df[['RecordIdentifier', 'GearDamage',
                                            'ASOCCode', 'Year', 'DeploymentNumber', 
                                            'SetNumber', 'Country', 'Quota', 'SetType',
                                            'VesselClass','Day', 'Month','PositionPrecision',
                                            'GearType','RecordType','DirectedSpecies','DataSource', 
                                            'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                                            'InOut200MileLimit',  'CodendMeshSize',
                                            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                                            'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                                            'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                            'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                                            'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                            'NumberIndividuals']] = Complete_df[
                                        ['RecordIdentifier', 'GearDamage',
                                            'ASOCCode', 'Year', 'DeploymentNumber', 
                                            'SetNumber', 'Country', 'Quota', 'SetType',
                                            'VesselClass','Day', 'Month','PositionPrecision',
                                            'GearType','RecordType','DirectedSpecies','DataSource', 
                                            'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                                            'InOut200MileLimit',  'CodendMeshSize',
                                            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                                            'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                                            'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                            'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                                            'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                            'NumberIndividuals']].astype(int)
                                        
                            Complete_df[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                                        'EndLongitude','AverageTowSpeed', 'VesselLength']] = Complete_df[
                                        ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                                        'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
                                
                            Complete_df['VesselSideNumber'] = pd.to_numeric(Complete_df[
                                        'VesselSideNumber'], downcast='integer', errors='ignore')
                            
                            Complete_df['SubTripNumber'] = pd.to_numeric(Complete_df[
                                        'SubTripNumber'], downcast='integer', errors='ignore')
                                        
                            Complete_df[['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                                        'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                        'UnitArea','DetailedCatchSpeciesCompCode']] = Complete_df[
                                        ['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                                        'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                        'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)

                            Complete_df = Complete_df.loc[:,
                                ['RecordIdentifier','DeploymentUID',
                                'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                                'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                                'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                                'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                                'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                                'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                                'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                                'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                                'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                                'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                'NumberIndividuals']]
                                
                            Complete_df = Complete_df.replace([99999999, 99999999.0, np.nan], '')
                            Complete_df = Complete_df.replace(['99999999.0', '99999999', '.'], 'None')
                            Complete_df  = Complete_df.reset_index(drop=True)
                            Complete_df = pd.DataFrame(Complete_df)
                            
                            if len(Complete_df) >0:
                                iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                                        "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                                if iSubmit >0:
                                    try:
                                        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                        cur_DB_Set_Catch_Analysis.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT WHERE DeploymentNumber =?",\
                                        (get_DepNumforSearch,))
                                        conn_DB_Set_Catch_Analysis.commit()
                                        cur_DB_Set_Catch_Analysis.close()
                                        conn_DB_Set_Catch_Analysis.close()
                                    except sqlite3.Error as error:
                                        print('Error occured - ', error)
                                    finally:
                                        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                        if conn_DB_Set_Catch_Analysis:
                                            Submit_To_DBStorage = pd.DataFrame(Complete_df)
                                            Submit_To_DBStorage = Submit_To_DBStorage.drop_duplicates(
                                            subset=['RecordIdentifier'], keep="last")
                                            Submit_To_DBStorage = Submit_To_DBStorage.reset_index(drop=True)
                                            Submit_To_DBStorage = pd.DataFrame(Submit_To_DBStorage)
                                            Submit_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_TEMP_IMPORT', conn_DB_Set_Catch_Analysis, 
                                                                if_exists="append",index = False)
                                            conn_DB_Set_Catch_Analysis.commit()
                                            cur_DB_Set_Catch_Analysis.close()
                                            conn_DB_Set_Catch_Analysis.close()
                                            pt.redraw()
                                            UpdateQCFailForDeployment(get_DepNumforSearch, get_SelQCVariable)
                                            tkinter.messagebox.showinfo("Submit Success","Successfully Submitted Update To Database")
                            else:
                                tkinter.messagebox.showinfo("Empty Set&Catch DB",
                                "Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")
                            
                        ProcedureFrame = Frame(windows, width = 40,  bg= "cadet blue")
                        ProcedureFrame.pack(side = LEFT, padx= 0, pady=0)
                        lbl_AddStepProcess = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                bg= "cadet blue", text="Procedure To Edit Cell & Update Value & Submit Entries To DB ")
                        lbl_AddStepProcess.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

                        lbl_AddEntriesDBStep1 = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                                bg= "cadet blue", text="1 : Double Click On TreeView Cell For Edit & Press Enter (Must) To Modify  Cell Value")
                        lbl_AddEntriesDBStep1.grid(row =2, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

                        lbl_AddEntriesDBStep2 = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                                bg= "cadet blue", text="2 : Submit Edited Table To Update Set & Catch QC DB ")
                        lbl_AddEntriesDBStep2.grid(row =6, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

                        button_SubmitToUpdateDB = Button(ProcedureFrame, bd = 2, text ="Submit To Update DB", width =18,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =SubmitToUpdateDB)
                        button_SubmitToUpdateDB.grid(row =8, column = 0, padx=12, pady =1, ipady =1, sticky =W)

                        lbl_CautionSteps = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                            bg= "cadet blue", text="NB : Do Not Edit Columns : DataBase_ID And RecordIdentifier")
                        lbl_CautionSteps.grid(row =10, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

                        lbl_CautionSteps_1 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                        bg= "cadet blue", text="NB : Edit/Modify Year/ASOC/DepN/SetN Columns Requires Edit DeplymentUID Accordingly")
                        lbl_CautionSteps_1.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)
                        windows.mainloop()          
                    else:
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(0, 'Empty Search Returned')
                        tkinter.messagebox.showinfo("Empty Set&Catch Entries","Empty Search Returned")     

    def SearchDepUIDFromSetCatchDB():
        get_DepUIDforSearch = (txtSearchDepUID.get())
        get_QCVariable = txtQCVariable.get()
        if (len(get_DepUIDforSearch)) > 0:
            try:
                get_DepUIDforSearch = str(get_DepUIDforSearch)
            except:
                messagebox.showerror('Search Variable Datatype Error Message', "Search Value Must Be String Value")
            checkinttype = isinstance(get_DepUIDforSearch,str)
            if checkinttype == True:  
                conn_DB= sqlite3.connect(DB_Set_Catch_Analysis)
                if len(get_DepUIDforSearch) >= 0:        
                    get_SearchSingleVariable_Value = (get_DepUIDforSearch)
                    rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT;", conn_DB)
                    conn_DB.commit()
                    conn_DB.close()
                    rows = rows[(rows.DeploymentUID) == get_SearchSingleVariable_Value]
                    rows  = rows.reset_index(drop=True)
                    rows  = pd.DataFrame(rows)
                    rows.sort_values(by=['ASOCCode','ObserverNumber',
                                'DeploymentNumber','SetNumber',
                                'RecordType'], inplace=True)
                    SearchDepNSetCatchDF = pd.DataFrame(rows)
                    SearchDepNSetCatchDF = SearchDepNSetCatchDF.loc[:,
                                ['RecordIdentifier','DeploymentUID',
                                'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                                'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                                'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                                'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                                'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                                'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                                'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                                'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                                'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                                'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                'NumberIndividuals']]
                    SearchDepNSetCatchDF = SearchDepNSetCatchDF.reset_index(drop=True)
                    Merge_WithSetCatchDB = pd.DataFrame(SearchDepNSetCatchDF)
                    if len(Merge_WithSetCatchDB) >0:
                        windows = tk.Toplevel()
                        windows.title ("Excel Table View Observer Set & Catch QC Database")
                        windows.geometry('1600x755+40+40')
                        windows.config(bg="cadet blue")
                        frame = tk.Frame(windows)
                        frame.pack(fill=BOTH, expand=1)
                        pt = Table(frame, dataframe = Merge_WithSetCatchDB, showtoolbar=True, showstatusbar=True)
                        pt.setRowColors(rows=range(1,len(Merge_WithSetCatchDB),2), clr='lightblue', cols='all')
                        pt.cellbackgr = 'aliceblue'
                        options = config.load_options()
                        options = { 'align': 'center',
                                    'cellbackgr': '#F4F4F3',
                                    'cellwidth': 120,
                                    'floatprecision': 2,
                                    'thousandseparator': '',
                                    'font': 'Arial',
                                    'fontsize': 8,
                                    'fontstyle': '',
                                    'grid_color': '#ABB1AD',
                                    'linewidth': 1,
                                    'rowheight': 22,
                                    'rowselectedcolor': '#E4DED4',
                                    'textcolor': 'black'}
                        config.apply_options(options, pt)
                        pt.show()
                        ## Define Functions
                        def SubmitToUpdateDB():
                            Complete_df = pd.DataFrame(pt.model.df)
                            Complete_df= (Complete_df.loc[:,
                                    ['RecordIdentifier','DeploymentUID',
                                    'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                                    'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                                    'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                                    'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                                    'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                                    'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                                    'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                                    'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                    'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                                    'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                                    'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                    'NumberIndividuals']]).replace(['', None, np.nan, 
                                    'None', ' ', '  ', '   ', '    '], 99999999)
                            Complete_df[['RecordIdentifier', 'GearDamage',
                                            'ASOCCode', 'Year', 'DeploymentNumber', 
                                            'SetNumber', 'Country', 'Quota', 'SetType',
                                            'VesselClass','Day', 'Month','PositionPrecision',
                                            'GearType','RecordType','DirectedSpecies','DataSource', 
                                            'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                                            'InOut200MileLimit',  'CodendMeshSize',
                                            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                                            'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                                            'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                            'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                                            'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                            'NumberIndividuals']] = Complete_df[
                                        ['RecordIdentifier', 'GearDamage',
                                            'ASOCCode', 'Year', 'DeploymentNumber', 
                                            'SetNumber', 'Country', 'Quota', 'SetType',
                                            'VesselClass','Day', 'Month','PositionPrecision',
                                            'GearType','RecordType','DirectedSpecies','DataSource', 
                                            'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                                            'InOut200MileLimit',  'CodendMeshSize',
                                            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                                            'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                                            'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                            'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                                            'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                            'NumberIndividuals']].astype(int)
                                        
                            Complete_df[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                                        'EndLongitude','AverageTowSpeed', 'VesselLength']] = Complete_df[
                                        ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                                        'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
                                
                            Complete_df['VesselSideNumber'] = pd.to_numeric(Complete_df[
                                        'VesselSideNumber'], downcast='integer', errors='ignore')
                            
                            Complete_df['SubTripNumber'] = pd.to_numeric(Complete_df[
                                        'SubTripNumber'], downcast='integer', errors='ignore')
                                        
                            Complete_df[['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                                        'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                        'UnitArea','DetailedCatchSpeciesCompCode']] = Complete_df[
                                        ['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                                        'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                        'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)

                            Complete_df = Complete_df.loc[:,
                                ['RecordIdentifier','DeploymentUID',
                                'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                                'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                                'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                                'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                                'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                                'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                                'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                                'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                                'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                                'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                'NumberIndividuals']]
                                
                            Complete_df = Complete_df.replace([99999999, 99999999.0, np.nan], '')
                            Complete_df = Complete_df.replace(['99999999.0', '99999999', '.'], 'None')
                            Complete_df  = Complete_df.reset_index(drop=True)
                            Complete_df = pd.DataFrame(Complete_df)
                            if len(Complete_df) >0:
                                iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                                        "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                                if iSubmit >0:
                                    try:
                                        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                        cur_DB_Set_Catch_Analysis.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT WHERE DeploymentUID =?",\
                                        (get_DepUIDforSearch,))
                                        conn_DB_Set_Catch_Analysis.commit()
                                        cur_DB_Set_Catch_Analysis.close()
                                        conn_DB_Set_Catch_Analysis.close()
                                    except sqlite3.Error as error:
                                        print('Error occured - ', error)
                                    finally:
                                        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                        if conn_DB_Set_Catch_Analysis:
                                            Submit_To_DBStorage = pd.DataFrame(Complete_df)
                                            Submit_To_DBStorage = Submit_To_DBStorage.drop_duplicates(
                                            subset=['RecordIdentifier'], keep="last")
                                            Submit_To_DBStorage = Submit_To_DBStorage.reset_index(drop=True)
                                            Submit_To_DBStorage = pd.DataFrame(Submit_To_DBStorage)
                                            Submit_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_TEMP_IMPORT', conn_DB_Set_Catch_Analysis, 
                                                                if_exists="append",index = False)
                                            conn_DB_Set_Catch_Analysis.commit()
                                            cur_DB_Set_Catch_Analysis.close()
                                            conn_DB_Set_Catch_Analysis.close()
                                            pt.redraw()
                                            UpdateQCFailForDepUID(get_DepUIDforSearch, get_QCVariable)
                                            tkinter.messagebox.showinfo("Submit Success","Successfully Submitted Update To Database")
                            else:
                                tkinter.messagebox.showinfo("Empty Set&Catch DB",
                                "Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")
                        
                        ProcedureFrame = Frame(windows, width = 40,  bg= "cadet blue")
                        ProcedureFrame.pack(side = LEFT, padx= 0, pady=0)
                        lbl_AddStepProcess = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                bg= "cadet blue", text="Procedure To Edit Cell & Update Value & Submit Entries To DB ")
                        lbl_AddStepProcess.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

                        lbl_AddEntriesDBStep1 = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                                bg= "cadet blue", text="1 : Double Click On TreeView Cell For Edit & Press Enter (Must) To Modify  Cell Value")
                        lbl_AddEntriesDBStep1.grid(row =2, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

                        lbl_AddEntriesDBStep2 = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                                bg= "cadet blue", text="2 : Submit Edited Table To Update Set & Catch QC DB ")
                        lbl_AddEntriesDBStep2.grid(row =6, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

                        button_SubmitToUpdateDB = Button(ProcedureFrame, bd = 2, text ="Submit To Update DB", width =18,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =SubmitToUpdateDB)
                        button_SubmitToUpdateDB.grid(row =8, column = 0, padx=12, pady =1, ipady =1, sticky =W)

                        lbl_CautionSteps = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                            bg= "cadet blue", text="NB : Do Not Edit Columns : DataBase_ID And RecordIdentifier")
                        lbl_CautionSteps.grid(row =10, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

                        lbl_CautionSteps_1 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                        bg= "cadet blue", text="NB : Edit/Modify Year/ASOC/DepN/SetN Columns Requires Edit DeplymentUID Accordingly")
                        lbl_CautionSteps_1.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)
                        windows.mainloop()                                   
                    else:
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(0, 'Empty Search Returned')
                        tkinter.messagebox.showinfo("Empty Set&Catch Entries","Empty Search Returned")    

    def UpdateQCFailForDepUID(get_DepUIDforSearch, get_QCVariable):
        conn_DB_Set_Catch_Misc= sqlite3.connect(DB_Set_Catch_Misc)
        cur_DB_Set_Catch_Misc=conn_DB_Set_Catch_Misc.cursor()
        if get_QCVariable == 'Year-ASOC-DepN-SetN':
            UpdateQCMsg_QCFailDB =[]
            QC_Message = "Updated - DuplicatedUID Failed"
            UpdateQCMsg_QCFailDB.append((QC_Message,
                                        get_DepUIDforSearch)) 
            cur_DB_Set_Catch_Misc.executemany("UPDATE DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport SET QC_Message =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)
            conn_DB_Set_Catch_Misc.commit()
            conn_DB_Set_Catch_Misc.close()
            tree1.delete(*tree1.get_children())
        else:
            UpdateQCMsg_QCFailDB =[]
            QC_Message = "Updated - " + 'TombstoneQC Failed'
            UpdateQCMsg_QCFailDB.append((QC_Message,
                                        get_DepUIDforSearch
                                        ))
            cur_DB_Set_Catch_Misc.executemany("UPDATE DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport SET QC_Message =? \
                                               WHERE DeploymentUID =?", 
                                               UpdateQCMsg_QCFailDB)
            conn_DB_Set_Catch_Misc.commit()
            conn_DB_Set_Catch_Misc.close()
            tree1.delete(*tree1.get_children())

    def UpdateQCFailForDeployment(get_DepNumforSearch, get_SelQCVariable):
        conn_DB_Set_Catch_Misc= sqlite3.connect(DB_Set_Catch_Misc)
        cur_DB_Set_Catch_Misc=conn_DB_Set_Catch_Misc.cursor()
        if get_SelQCVariable == 'DuplicateUID QC Fail':
            UpdateQCMsg_QCFailDB =[]
            QC_Message = "Updated - From Deployment Search"
            UpdateQCMsg_QCFailDB.append((QC_Message,
                                        get_DepNumforSearch)) 
            cur_DB_Set_Catch_Misc.executemany("UPDATE DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport SET QC_Message =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
            conn_DB_Set_Catch_Misc.commit()
            conn_DB_Set_Catch_Misc.close()
            tree1.delete(*tree1.get_children())
        else:
            UpdateQCMsg_QCFailDB =[]
            QC_Message = "Updated - From Deployment Search" 
            UpdateQCMsg_QCFailDB.append((QC_Message,
                                        get_DepNumforSearch))
            cur_DB_Set_Catch_Misc.executemany("UPDATE DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport SET QC_Message =? \
                                               WHERE DeploymentNumber =?", 
                                               UpdateQCMsg_QCFailDB)
            conn_DB_Set_Catch_Misc.commit()
            conn_DB_Set_Catch_Misc.close()
            tree1.delete(*tree1.get_children())
    
    # Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    SelResultOverviewtree.bind('<<TreeviewSelect>>',InventoryRec4)
    ## ComboBox Select
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ## Gen QC Summary
    GenSummaryQC()
    QCFailedTotalEntries()

    # SelectViewResultsRun Button
    btnViewQCFailedQCResults = Button(SelectViewResultsRun, text="View Selected Results", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=18, bd=1, command = viewQCFailed_VariablesProfile)
    btnViewQCFailedQCResults.grid(row =0, column = 1, padx=1, pady =2, ipady =2, sticky =W)

    btnSearchDepUID = Button(SelectViewResultsRun, text="View DeploymentUID From SetCatchDB", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=33, bd=1, command = SearchDepUIDFromSetCatchDB)
    btnSearchDepUID.grid(row =0, column = 1, padx=37, pady =2, ipady =2, sticky =E)
    
    # Top Frame Button
    btnClearTable = Button(Topframe, text="Clear Table", font=('aerial', 9, 'bold'), bg='alice blue',
                                height =1, width=10, bd=1, command = ClearTablesAll)
    btnClearTable.grid(row =2, column = 0, padx=380, pady =2, ipady =2, sticky =W)

    # Buttons On Generate QC Failed Summary Frame
    button_GenSummaryQC = Button(Summaryframe, bd = 2, text ="Generate QC Summary ", width = 20,
                                height=1, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSummaryQC)
    button_GenSummaryQC.pack(side =TOP)

    button_SearchDepNumSetCatchDB = Button(SelQCVariableDisplay, bd = 1, text ="View DepNum From SetCatchDB", width = 27,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =SearchDepNumFromSetCatchDB)
    button_SearchDepNumSetCatchDB.grid(row =0, column = 0, padx=70, pady =2, ipady =2, sticky =W)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Exit", command=iExit)
    filemenu.add_command(label="Update DeplymentUID", command=UpdateDeploymentUIDAfterUpdate)
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack(side = LEFT)
    window.mainloop()

