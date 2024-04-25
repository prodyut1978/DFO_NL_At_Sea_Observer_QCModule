#Front End
from tkinter import*
import tkinter.messagebox
from tkinter import ttk, filedialog
from tkinter import messagebox
import tkinter as tk
import sqlite3
import pandas as pd
import numpy as np
from pandastable import Table, config
import functools

## Database connections
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Logical = ("./BackEnd/Sqlite3_DB/QC_Check_LogicalConsistency_DB/DFO_NL_ASOP_SetCatch_LogicalValidation.db")

def ViewLogicalNSpeciesValidatedResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Logical Validator - ID-C-04-2")
    window.geometry("1350x820+200+100")
    window.config(bg="cadet blue")
    ## Top Frame
    TopFrame = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    TopFrame.pack(side = TOP, padx= 0, pady=0)

    lbl_TopFrame = Label(TopFrame, font=('aerial', 10, 'bold'), bg= "cadet blue", text="A. QC Fail Table (RecType-NSpecies) :")
    lbl_TopFrame.grid(row =1, column = 0, padx=2, pady =1, ipady=1, sticky =W)

    ListVariableListA = ['Select RecType-NSpecies Logical View Type', 
                         'View RecType-NSpecies Logical Fail With Case-A,B',
                         'View RecType-NSpecies Logical Fail With Case-A Only',
                         'View RecType-NSpecies Logical Fail With Case-B Only'
                         ]
    VariableList        = StringVar(TopFrame, value ='')
    entry_ViewVarResults  = ttk.Combobox(TopFrame, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable = VariableList, width = 50, state='readonly')
    entry_ViewVarResults.grid(row =1, column = 1, padx=40, pady =4, ipady= 4, sticky =W)
    entry_ViewVarResults['values'] = ListVariableListA
    entry_ViewVarResults.current(0)

    EntryDepNum       = IntVar(TopFrame, value ='Enter DeploymentNumber')
    entry_DepNumforSearch = Entry(TopFrame, font=('aerial', 10), justify='center',
                                textvariable = EntryDepNum, width = 23, bd=2)
    entry_DepNumforSearch.grid(row =0, column = 1, padx=2, pady =2, ipady =2, sticky =E)

    lbl_TotalFailedEntries = Label(TopFrame, font=('aerial', 10 , 'bold'), text="# Of Set Failed :")
    lbl_TotalFailedEntries.grid(row =0, column = 0, padx=1, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(TopFrame, value='')
    txtTotalFailedEntries = Entry(TopFrame, font=('aerial',10),textvariable = TotalFailedEntries, width = 5, bd=1)
    txtTotalFailedEntries.grid(row =0, column = 0, padx=120, pady =1, ipady =1, sticky =W)

    txtDisplayMessageSystem = Entry(TopFrame, font=('aerial', 9), justify='center',
                            textvariable = StringVar(window, value='QC Message Display'), width = 84, bd=2)
    txtDisplayMessageSystem.grid(row =0, column = 1, padx=40, pady =2, ipady =5, sticky =W)

    Tableframe = Frame(window, width = 40)
    Tableframe.pack(side = TOP, padx= 0, pady=0)

    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", "column4", 
                    "column5", "column6", "column7", "column8",
                    "column9"), height=21, show='headings')
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
    tree1.heading("#1", text="DatabaseID", anchor=CENTER)
    tree1.heading("#2", text="RecordIdentifier", anchor=CENTER)
    tree1.heading("#3", text="DeploymentUID", anchor=CENTER)
    tree1.heading("#4", text="DeploymentNumber", anchor=CENTER)
    tree1.heading("#5", text="SetNumber", anchor=CENTER)
    tree1.heading("#6", text="RecordType", anchor=CENTER)
    tree1.heading("#7", text="NumberSpecies", anchor=CENTER)
    tree1.heading("#8", text="RecType-NSpecies-QC Message", anchor=CENTER)
    tree1.heading("#9", text="QCCaseType", anchor=CENTER)
    
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=460, anchor = tk.CENTER)
    tree1.column('#9', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
   
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)

    ## Frame Of update modules
    UpdateDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    UpdateDB_Entryframe.pack(side =LEFT, padx=2, pady =2)

    lbl_UpdateDB_Header = Label(UpdateDB_Entryframe, font=('aerial', 12, 'bold','underline'),
                                bg= "cadet blue", text="Update Database :")
    lbl_UpdateDB_Header.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    EntryDataType_Variable       = StringVar(UpdateDB_Entryframe, value ='Variable Type')
    entry_EntryDataType_Variable = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), 
                                        textvariable = EntryDataType_Variable, width = 15, bd=1)
    entry_EntryDataType_Variable.grid(row =2, column = 0, padx=4, pady =4, ipady =4, sticky =E)

    lbl_SelectTableEntries = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Table Entries:")
    lbl_SelectTableEntries.grid(row =4, column = 0, padx=2, pady =2, sticky =W)
    NumberRowSelected       = IntVar(UpdateDB_Entryframe, value ='# Of Selected')
    entry_NumberRowSelected = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), justify='center',
                                textvariable = NumberRowSelected, width = 15, bd=1)
    entry_NumberRowSelected.grid(row =4, column = 0, padx=2, pady =4, ipady =4, sticky =E)

    lbl_Select_List_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 2. Select Variable :")
    lbl_Select_List_Variable.grid(row =6, column = 0, padx=2, pady =4, sticky =W)
    
    ListVariableListA = ['DeploymentNumber','SetNumber','RecordType','NumberSpecies']
    VariableListA        = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = VariableListA, width = 24, state='readonly')
    entry_UpdateVariableList.grid(row =8, column = 0, padx=10, pady =2, ipady= 4, sticky =W)
    entry_UpdateVariableList['values'] = sorted(list(ListVariableListA))

    lbl_EntryUpdate_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 3. Enter Updated Value :")
    lbl_EntryUpdate_Variable.grid(row =10, column = 0, padx=2, pady =2, sticky =W)

    UpdateValue_VariableA       = IntVar(UpdateDB_Entryframe, value ='')
    entry_UpdateValue_VariableA = Entry(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = UpdateValue_VariableA, width = 25, bd=2)
    entry_UpdateValue_VariableA.grid(row =12, column = 0, padx=10, pady =2, ipady =4, sticky =W)

    ## ### Frame Of search modules #######
    SearchDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SearchDB_Entryframe.pack(side =LEFT, padx=10, pady =2)

    lbl_SearchDB_Header = Label(SearchDB_Entryframe, font=('aerial', 12, 'bold','underline'), 
                                bg= "cadet blue", text="Search Database:")
    lbl_SearchDB_Header.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_SelectSinglevariableSearch_A = Label(SearchDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Variable :")
    lbl_SelectSinglevariableSearch_A.grid(row =3, column = 0, padx=2, pady =1, ipady= 4, sticky =W)

    ListVariableSearch = ['DeploymentUID','DeploymentNumber','SetNumber', 'RecordType',
                          'NumberSpecies', 'QCRecordType_NumberSpecies','QCCaseType']
    VariableListSearch = StringVar(SearchDB_Entryframe, value ='')
    entry_SearchVariableList = ttk.Combobox(SearchDB_Entryframe, font=('aerial', 10, 'bold'), 
                               textvariable = VariableListSearch, width = 22, state='readonly')
    entry_SearchVariableList.grid(row =4, column = 0, padx=20, pady =1, ipady= 1, sticky =W)
    entry_SearchVariableList['values'] = sorted(list(ListVariableSearch))

    lbl_EntrySearch_Variable = Label(SearchDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 2. Enter Search Query :")
    lbl_EntrySearch_Variable.grid(row =5, column = 0, padx=2, pady =2, ipady= 4, sticky =W)

    SearchValue_Variable_A       = StringVar(SearchDB_Entryframe, value ='')
    entry_SearchValue_Variable_A = ttk.Combobox(SearchDB_Entryframe, font=('aerial', 10, 'bold'), 
                                            textvariable = SearchValue_Variable_A, width = 22)
    entry_SearchValue_Variable_A.grid(row =6, column = 0, padx=20, pady =1, ipady =1, sticky =W)

    lbl_TotalSearchEntries = Label(SearchDB_Entryframe, font=('aerial', 10 , 'bold'),
                             bg= "cadet blue", text="3. # Of Search Entries :")
    lbl_TotalSearchEntries.grid(row =7, column = 0, padx=2, pady =2, ipady=4, sticky =W)
    TotalSearchEntries = IntVar(SearchDB_Entryframe, value='')
    txtTotalSearchEntries = Entry(SearchDB_Entryframe, font=('aerial',8),
                            textvariable = TotalSearchEntries, width = 8, bd=1)
    txtTotalSearchEntries.grid(row =7, column = 0, padx=40, pady =4, ipady =4, sticky =E)

    ## ############ Frame Generate QC Failed Summary ########
    SummaryQCframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.pack(side =LEFT, padx=10, pady =2)


    lbl_SummaryQCframe = Label(SummaryQCframe, font=('aerial', 11, 'bold','underline'), 
                                bg= "cadet blue", text="B: QC Summary")
    lbl_SummaryQCframe.pack(side =TOP, anchor = W)

    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    Summaryframetree = ttk.Treeview(Summaryframe, column=("column1", "column2", "column3"),
                                    height=3, show='headings')
    scrollbary = ttk.Scrollbar(Summaryframe, orient ="vertical", command=Summaryframetree.yview)
    scrollbary.pack(side ='right', fill ='y')
    Summaryframetree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(Summaryframe, orient ="horizontal", command=Summaryframetree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    Summaryframetree.configure(xscrollcommand = scrollbarx.set)
    Summaryframetree.heading("#1", text="QCCaseType", anchor=CENTER)
    Summaryframetree.heading("#2", text="SetQCFail Count ", anchor=CENTER)
    Summaryframetree.heading("#3", text="QC Entries", anchor=CENTER)
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)            
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    Summaryframetree.column('#3', stretch=NO, minwidth=0, width=125, anchor=tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    style = ttk.Style(Summaryframetree)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    Summaryframetree.pack(side = BOTTOM)
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    SummaryDisplay.pack(side = BOTTOM, pady=0)
    txtSummaryDisplayMsg = Entry(SummaryDisplay, font=('aerial', 10),
                            textvariable = StringVar(window, value='QC Summary Message'), width = 50, bd=2)
    txtSummaryDisplayMsg.grid(row =0, column = 0, padx=10, pady =2, ipady =5, sticky =E)

    lbl_ToUpdateEntriesCount = Label(SummaryDisplay, font=('aerial', 9 , 'bold'), text="Total Set To Update")
    lbl_ToUpdateEntriesCount.grid(row =2, column = 0, padx=2, pady =2, ipady=2, sticky =E)
    ToUpdateEntriesCount = IntVar(SummaryDisplay, value='')
    txtToUpdateEntriesCount = Entry(SummaryDisplay, font=('aerial',8),
                                   textvariable = ToUpdateEntriesCount, 
                                   width = 8, bd=1)
    txtToUpdateEntriesCount.grid(row =4, column = 0, padx=20, pady =2, ipady =5, sticky =E)
    lbl_AlreadyUpdateEntriesCount = Label(SummaryDisplay, font=('aerial', 9 , 'bold'), text="Total Set Updated")
    lbl_AlreadyUpdateEntriesCount.grid(row =2, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    AlreadyUpdateEntriesCount = IntVar(SummaryDisplay, value='')
    txtAlreadyUpdateEntriesCount = Entry(SummaryDisplay, font=('aerial',8),
                                   textvariable = AlreadyUpdateEntriesCount, 
                                   width = 8, bd=1)
    txtAlreadyUpdateEntriesCount.grid(row =4, column = 0, padx=20, pady =2, ipady =5, sticky =W)
    
    ##### Frame Of Selected Results Overview modules #####
    SelResultOverview = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SelResultOverview.pack(side =LEFT, padx=2, pady =2)
    SelResultOV      = StringVar(SelResultOverview, value ='C: Selected Results Overview')
    entry_SelResultOverview = Entry(SelResultOverview, font=('aerial', 10, 'bold'), 
                            textvariable = SelResultOV, width = 40, bd=2)
    entry_SelResultOverview.pack(side =TOP,pady =2, ipady =2, anchor = W)

    SelResultOverviewtree = ttk.Treeview(SelResultOverview,  column=("column1", "column2", "column3"),
                                         height=8, show='headings')
    scrollbary = ttk.Scrollbar(SelResultOverview, orient ="vertical", command=SelResultOverviewtree.yview)
    scrollbary.pack(side ='right', fill ='y')
    SelResultOverviewtree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(SelResultOverview, orient ="horizontal", command=SelResultOverviewtree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    SelResultOverviewtree.configure(xscrollcommand = scrollbarx.set)
    SelResultOverviewtree.heading("#1", text="DeploymentUID", anchor=CENTER)
    SelResultOverviewtree.heading("#2", text="QCCaseType ", anchor=CENTER)
    SelResultOverviewtree.heading("#3", text="# Of Entries/SetNumber ", anchor=CENTER)
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)            
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = BOTTOM)
    
    ## Define Functions
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber',
                            'RecordType','NumberSpecies', 
                            'QCRecordType_NumberSpecies', 'QCCaseType']
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
            return ReturnMatchedMessage
        else: 
            return ReturnMisMatchedMessage

    def ImportAndUpdateSetCatchDB():
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        conn_DB_SetCatch_Validation_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur_DB_SetCatch_Validation_Logical=conn_DB_SetCatch_Validation_Logical.cursor()
        txtDisplayMessageSystem.delete(0,END)
        txtDisplayMessageSystem.insert(tk.END,'Select Modified CSV File To Update DB')
        tree1.delete(*tree1.get_children())
        Filename = filedialog.askopenfilenames(title="Select Updated QC Failed CSV File", 
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.")))
        Length_filename  =  len(Filename)
        if Length_filename >0:
            for filename in Filename:
                if filename.endswith('.csv'):
                    filename = r"{}".format(filename)
                    df = pd.read_csv(filename, sep=',' , low_memory=False)
                    List_Columns_Import = list(df.columns)
                    Return_Message = ImportColumnCheck(List_Columns_Import)
                    if Return_Message == ReturnMatchedMessage:
                        df = df.iloc[:,:]
                        DataBase_ID= (df.loc[:,'DataBase_ID']).fillna(99999999).astype(int)
                        RecordIdentifier= (df.loc[:,'RecordIdentifier']).fillna(99999999).astype(int)
                        DeploymentUID= (df.loc[:,'DeploymentUID']).fillna(8888888).astype(str)
                        DeploymentNumber            = (df.loc[:,'DeploymentNumber']).fillna(99999999).astype(int, errors='ignore')
                        SetNumber                   = (df.loc[:,'SetNumber']).fillna(99999999).astype(int, errors='ignore')
                        RecordType                  = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        NumberSpecies               = (df.loc[:,'NumberSpecies']).fillna(99999999).astype(int, errors='ignore')
                        QCRecordType_NumberSpecies  = (df.loc[:,'QCRecordType_NumberSpecies']).fillna(8888888).astype(str, errors='ignore')
                        QCCaseType                  = (df.loc[:,'QCCaseType']).fillna(8888888).astype(str, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID,\
                                        DeploymentNumber, SetNumber,\
                                        RecordType, NumberSpecies,\
                                        QCRecordType_NumberSpecies, QCCaseType]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns =  {0:'DataBase_ID',1: 'RecordIdentifier',2: 'DeploymentUID',
                                                3:'DeploymentNumber',   4:'SetNumber',   5:'RecordType', 
                                                6:'NumberSpecies', 7:'QCRecordType_NumberSpecies', 8:'QCCaseType'
                                                },inplace = True)
                        Raw_Imported_Df = pd.DataFrame(catdf)
                        Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0, '.'], '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([8888888, '8888888', '.'], 'None')
                        Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                        Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                        CheckEmptyNessColumn = Raw_Imported_Df[
                                            (Raw_Imported_Df.DataBase_ID=='') |
                                            (Raw_Imported_Df.RecordIdentifier=='') |
                                            (Raw_Imported_Df.DeploymentUID=='None') |
                                            (Raw_Imported_Df.DeploymentUID=='') |                                           
                                            (Raw_Imported_Df.DeploymentNumber=='') |
                                            (Raw_Imported_Df.SetNumber=='')|
                                            (Raw_Imported_Df.RecordType=='')
                                            ]
                    Len_CheckEmptyNessColumn =len(CheckEmptyNessColumn)
                    if Len_CheckEmptyNessColumn==0:
                        Length_Raw_Imported_Df  =  len(Raw_Imported_Df)
                        if Length_Raw_Imported_Df <250000:
                            UpdateRecordList_SetCatchDB =[]
                            UpdateRecordList_QCFailDB =[]
                            df_rows = Raw_Imported_Df.to_numpy().tolist()
                            for row in df_rows:
                                rowValue = row
                                list_item_DataBase_ID = int(rowValue[0])
                                list_item_RecordIdentifier = int(rowValue[1])
                                list_item_DeploymentUID = (rowValue[2])
                                list_item_DeploymentNumber = (rowValue[3])
                                list_item_SetNumber = (rowValue[4])
                                list_item_RecordType = (rowValue[5])
                                list_item_NumberSpecies = (rowValue[6])
                                list_item_QCRecordType_NumberSpecies = (rowValue[7])
                                list_item_QCCaseType = 'Case Updated'
                                
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_DeploymentUID,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_RecordType,
                                                    list_item_NumberSpecies,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    ))
                                UpdateRecordList_QCFailDB.append((
                                                    list_item_DeploymentUID,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_RecordType,
                                                    list_item_NumberSpecies,
                                                    list_item_QCRecordType_NumberSpecies,
                                                    list_item_QCCaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    ))
                            
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentUID =?, DeploymentNumber = ?, \
                                                    SetNumber = ?, RecordType = ?, NumberSpecies = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdateRecordList_SetCatchDB)
                            cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET DeploymentUID =?, DeploymentNumber = ?, \
                                                    SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                                    QCRecordType_NumberSpecies = ?, QCCaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdateRecordList_QCFailDB)
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Logical.commit()
                            conn_DB_SetCatch_Validation_Logical.close()
                            viewQCFailed_VariablesProfile()
                            txtDisplayMessageSystem.delete(0,END)
                            txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                    else:
                        messagebox.showerror('Import File Empty Variables', "Please Check The Null Variable Input")

    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def ClearTablesAll():
        tree1.delete(*tree1.get_children())
        txtTotalFailedEntries.delete(0,END)
        entry_ViewVarResults.current(0)
    
    def ClearEntries():
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateValue_VariableA.delete(0,END)
        entry_NumberRowSelected.delete(0,END)

    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select RecType-NSpecies Logical View Type', 
                         'View RecType-NSpecies Logical Fail With Case-A,B',
                         'View RecType-NSpecies Logical Fail With Case-A Only',
                         'View RecType-NSpecies Logical Fail With Case-B Only'
                            ]
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Logical)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows)
            rows = rows.reset_index(drop=True)
            rows.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 
                                 2:'DeploymentUID', 3:'DeploymentNumber',
                                 4:'SetNumber', 5:'RecordType', 
                                 6:'NumberSpecies', 7:'QCRecordType_NumberSpecies', 
                                 8:'QCCaseType'},inplace = True)
            if getVarnameToView == ListVariableListA[1]:
                rows = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[2]:
                rows = rows[(rows.QCRecordType_NumberSpecies) == 'Case-A: In A Set With Only RecType1, NumberSpecies Must 0 or Blank']
                rows = rows.reset_index(drop=True)
                rows = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[3]:
                rows = rows[(rows.QCRecordType_NumberSpecies) == 'Case-B: In A Set With RecType-1/2, NumberSpecies Must Same For Each RecType']
                rows = rows.reset_index(drop=True)
                rows = pd.DataFrame(rows)
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_VariablesProfile():
        ListVariableListA = ['Select RecType-NSpecies Logical View Type', 
                         'View RecType-NSpecies Logical Fail With Case-A,B',
                         'View RecType-NSpecies Logical Fail With Case-A Only',
                         'View RecType-NSpecies Logical Fail With Case-B Only'
                            ]
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        if len(rows) >0 :
            rows.sort_values(by=['DeploymentNumber','SetNumber',
                                 'RecordType'], inplace=True)
            rows  = rows.reset_index(drop=True)
            rows  = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[0]:
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(0, 'Select RecType-NSpecies View Type From DropDown & Run View Selected Button')
            else:
                countIndex1 = 0
                for each_rec in range(len(rows)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 'Empty QC Fail DB. Nothing to Display')
           
    def callbackFuncSelectView(event):
        ListVariableListA = ['Select RecType-NSpecies Logical View Type', 
                         'View RecType-NSpecies Logical Fail With Case-A,B',
                         'View RecType-NSpecies Logical Fail With Case-A Only',
                         'View RecType-NSpecies Logical Fail With Case-B Only']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            tree1.delete(*tree1.get_children())
            
        if(SelVariableView ==ListVariableListA[0]):
            tree1.delete(*tree1.get_children())
            
            
        if(SelVariableView ==ListVariableListA[1]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'A Set With Only RecType 1, RecType 1 & 2 : NumSpecies > Null/Zero, Same For Both RecType 1 & 2')
            
        if(SelVariableView ==ListVariableListA[2]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Case-A: In A Set With Only RecType1, NumberSpecies Must 0 or Blank')
    
        if(SelVariableView ==ListVariableListA[3]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Case-B: In A Set With RecType-1/2, NumberSpecies Must Same For Each RecType')
    
    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM Logical_RecordType_NumberSpecies_FailSummary;", conn)
        conn.commit()
        conn.close()
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        if len(data)>0:
            QCFailedTotalEntries = sum(data['QCFailCount'])
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)                   
        else:
            QCFailedTotalEntries = 0     
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)
        return QCFailedTotalEntries

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def Export_LogicalFailed_RN_CSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("QC Failed Logical RecType-NumberSpecies","QC Failed Logical RecType-NumberSpecies Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("QC Failed Logical RecType-NumberSpecies Report Message","Please Select File Name To Export")
            else:
                messagebox.showerror('Export Error', "Void File... Nothing to Export")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                return SetCatchProfileDB_DF
            else:
                messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchQCFailedDB():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID']]
                SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                return SetCatchQCFailedDB_DF
            else:
                return Complete_df
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def RefFailedToSetcatchDB():
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF['DataBase_ID'] = (SetCatchProfileDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['RecordIdentifier'] = (SetCatchProfileDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        SetCatchQCFailedDB_DF = GetSetCatchQCFailedDB()
        SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                                    SetCatchQCFailedDB_DF, on = ["DataBase_ID", "RecordIdentifier", "DeploymentUID"], indicator=True, 
                                    how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.iloc[:,0:len(list(SetCatchProfileDB_DF.columns))]

        Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
        windows = tk.Toplevel()
        windows.title ("Excel Table View Observer Set & Catch QC Database")
        windows.geometry('1600x755+40+40')
        windows.config(bg="cadet blue")
        frame = tk.Frame(windows)
        frame.pack(fill=BOTH, expand=1)
        pt = Table(frame, dataframe = Ref_FailedQC_InSetcatchDB, showtoolbar=True, showstatusbar=True)
        pt.setRowColors(rows=range(1,len(Ref_FailedQC_InSetcatchDB),2), clr='lightblue', cols='all')
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
        windows.mainloop()
        
    def InventoryRec1(event):
        entry_DepNumforSearch.delete(0,END)
        txtDisplayMessageSystem.delete(0,END)
        QcMessage = 'Run SetCatch DB Search For DepNum : '
        curItems = tree1.selection()
        if len(curItems)==1:
            sd = tree1.item(curItems, 'values')
            SelvariableDepUID = sd[2]
            SelvariableIdentifier = sd[3]
            entry_DepNumforSearch.insert(tk.END,SelvariableIdentifier)
            txtDisplayMessageSystem.insert(tk.END,(QcMessage + SelvariableIdentifier))
            entry_SelResultOverview.delete(0,END)
            entry_SelResultOverview.insert(tk.END,(("Selected DeploymentUID : ") +
                                                SelvariableDepUID))
        len_curItems = len(curItems)
        if len_curItems < 20001:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,len_curItems)
        else:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,'MaxLimit Exceed')

    def SetcatchDB_VariableList():
        GetSetCatchDB_VariableList = ['DeploymentNumber','SetNumber', 'RecordType','NumberSpecies']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList_SetCatchDB, 
                                         UpdateRecordList_QCFailDB, UpdateQCMsg_QCFailDB):
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

        conn_Validation_Presence= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur_Validation_Presence=conn_Validation_Presence.cursor()
        
        ## Updaing SetCatch DB
        if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_SetCatchDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList_SetCatchDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_SetCatchDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberSpecies = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList_SetCatchDB))

        ### Updating QC Failed DB
        if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET DeploymentNumber = ?\
                                                 WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)
            
            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET QCRecordType_NumberSpecies =?, QCCaseType =? \
                                                 WHERE DeploymentUID =?", 
                    UpdateQCMsg_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET SetNumber = ?\
                                                 WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList_QCFailDB)
            
            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET QCRecordType_NumberSpecies =?, QCCaseType =? \
                                                 WHERE DeploymentUID =?", 
                UpdateQCMsg_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET RecordType = ?\
                                                 WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList_QCFailDB)

            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET QCRecordType_NumberSpecies =?, QCCaseType =? \
                                                 WHERE DeploymentUID =?", 
                UpdateQCMsg_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET NumberSpecies = ?\
                                                 WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                (UpdateRecordList_QCFailDB))
    
            cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET QCRecordType_NumberSpecies =?, QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                UpdateQCMsg_QCFailDB)

        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Presence.commit()
        conn_Validation_Presence.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18 = ['DeploymentNumber','SetNumber', 'RecordType']
                        
            Var_Class_String7 = ['DeploymentUID']
            
            Var_Class_IntB27  = ['NumberSpecies']

            ReturnFail ="ReturnFail"

            if get_Updated_Variable in Var_Class_IntA18:
                if(len(get_UpdateValue_UpdatedVariable)!=0):
                    try:
                        get_UpdateValue_UpdatedVariable = int(get_UpdateValue_UpdatedVariable)
                        return get_UpdateValue_UpdatedVariable
                    except:
                        messagebox.showerror('Update Variable Datatype Error Message', "Updated Value Must Be Integer Value")
                        return ReturnFail
                else:
                    messagebox.showerror('Update Variable Error Message',
                                        "Updated Value Can Not Be Null")
                    return ReturnFail
            
            if get_Updated_Variable in Var_Class_String7:
                if(len(get_UpdateValue_UpdatedVariable)!=0):
                    try:
                        get_UpdateValue_UpdatedVariable = int(get_UpdateValue_UpdatedVariable)
                        return get_UpdateValue_UpdatedVariable
                    except:
                        get_UpdateValue_UpdatedVariable = (get_UpdateValue_UpdatedVariable)
                        return get_UpdateValue_UpdatedVariable
                else:
                    get_UpdateValue_UpdatedVariable = 'None'
                    return get_UpdateValue_UpdatedVariable
            
            if get_Updated_Variable in Var_Class_IntB27:
                if(len(get_UpdateValue_UpdatedVariable)!=0):
                    try:
                        get_UpdateValue_UpdatedVariable = int(get_UpdateValue_UpdatedVariable)
                        return get_UpdateValue_UpdatedVariable
                    except:
                        messagebox.showerror('Update Variable Datatype Error Message', "Updated Value Must Be Integer Value")
                        return ReturnFail
                else:
                    get_UpdateValue_UpdatedVariable = (get_UpdateValue_UpdatedVariable)
                    return get_UpdateValue_UpdatedVariable

    def UpdateSelected_SetCatch_DBEntries():
        ReturnFail ="ReturnFail"
        txtDisplayMessageSystem.delete(0,END)
        txtDisplayMessageSystem.insert(tk.END,"Please Wait Updating Selected Entries")
        get_Updated_Variable = entry_UpdateVariableList.get()
        get_UpdateValue_UpdatedVariable = entry_UpdateValue_VariableA.get()
        get_UpdateValue_UpdatedVariable = QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable)
        if (get_UpdateValue_UpdatedVariable != ReturnFail) & (len(get_Updated_Variable)!=0):
            curItems = tree1.selection()
            if len(curItems)>0:
                ListBox_DF = (tree1.get_children())       
                ## Update SetCatch DB
                if (len(ListBox_DF)>0)& (len(ListBox_DF)<20001):          
                    if(len(get_Updated_Variable)==0) & ((get_UpdateValue_UpdatedVariable)==''):
                        messagebox.showerror('Update Entries Missing',
                                        "Selection of Variable From List Entries Or Updated \
                                        Variable Value Entry Missing Or Both Entries Missing")
                        
                    if(len(get_Updated_Variable)==0) & ((get_UpdateValue_UpdatedVariable)!=''):
                        messagebox.showerror('Update Entries Missing',
                                            "Selection of Variable From List Entries Or Updated \
                                            Variable Value Entry Missing Or Both Entries Missing")

                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)!=''):
                        UpdateRecordList_SetCatchDB =[]
                        UpdateRecordList_QCFailDB =[]
                        UpdateQCMsg_QCFailDB =[]  
                        for item in tree1.selection():
                            list_item = (tree1.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            list_item_QCRecordType_NumberSpecies = ''
                            list_item_QCCaseType = ''
                            UpdateRecordList_SetCatchDB.append((get_UpdateValue_UpdatedVariable, 
                                                                list_item_DatabaseUID,
                                                                list_item_RecordIdentifier,
                                                                list_item_DeploymentUID))
                            
                            UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,
                                                            list_item_DatabaseUID,
                                                            list_item_RecordIdentifier,
                                                            list_item_DeploymentUID))
                            UpdateQCMsg_QCFailDB.append((list_item_QCRecordType_NumberSpecies,
                                                        list_item_QCCaseType,
                                                        list_item_DeploymentUID))
                        
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList_SetCatchDB, 
                                                        UpdateRecordList_QCFailDB, UpdateQCMsg_QCFailDB)
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(tk.END,"Set & Catch Database Updated Successfully")
                        viewQCFailed_VariablesProfile()
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")
                        
                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                        iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                                                                    "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                        if iUpdateSlected >0:
                            UpdateRecordList_SetCatchDB =[]
                            UpdateRecordList_QCFailDB =[]
                            UpdateQCMsg_QCFailDB =[]   
                            for item in tree1.selection():
                                list_item = (tree1.item(item, 'values'))
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                list_item_QCRecordType_NumberSpecies = ''
                                list_item_QCCaseType = ''
                                UpdateRecordList_SetCatchDB.append((get_UpdateValue_UpdatedVariable, 
                                                                    list_item_DatabaseUID,
                                                                    list_item_RecordIdentifier,
                                                                    list_item_DeploymentUID))
                                
                                UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,
                                                            list_item_DatabaseUID,
                                                            list_item_RecordIdentifier,
                                                            list_item_DeploymentUID))
                                
                                UpdateQCMsg_QCFailDB.append((list_item_QCRecordType_NumberSpecies,
                                                        list_item_QCCaseType,
                                                        list_item_DeploymentUID))
                                
                            Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList_SetCatchDB, 
                                                            UpdateRecordList_QCFailDB, UpdateQCMsg_QCFailDB)
                            viewQCFailed_VariablesProfile()
                            tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")    
                
                ## Empty Selection Case
                if (len(ListBox_DF)<0)|((ListBox_DF) ==[]):
                    tkinter.messagebox.showinfo("Update Error","Empty Set & Catch Table\
                                                Selection. Please Select At least One \
                                                Entries In the Table To Update The Variable")
                
                ## Max Limit Update Exceed Case Limiting Because Of Slow Performance 
                if (len(ListBox_DF)>20000):
                    tkinter.messagebox.showinfo("Update Selection Max Case","Max Limit For Update Selection Is 20,000 \
                                                Please Select A Batch Of 20,000 Entries Each Time If You Need To Update More")  
                
                GenSummaryQC()
            else:
                messagebox.showerror('Update Error',
                                "Please Select Atleast One Entries To Update") 
        else:
            messagebox.showerror('Update Error',
                                "Please Check Variable DataType And Follow Proper Update Step") 

    def callbackFuncSelectVariable1(event):
        VariableListA = entry_UpdateVariableList.get()
        print('Selected Update Variable Name :'+ VariableListA)
        if len(VariableListA)!= 0:
            entry_UpdateValue_VariableA.delete(0,END)
        if(VariableListA=='ObserverNumber')|\
        (VariableListA=='SubTripNumber')|\
        (VariableListA=='VesselSideNumber')|\
        (VariableListA=='NAFODivision')|\
        (VariableListA=='DetailedCatchSpeciesCompCode')|\
        (VariableListA=='UnitArea'):
            EntryDataType_Variable = 'AlphaNumeric'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)
        else:
            EntryDataType_Variable = 'Numeric'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)

    def Combo_input_QCCaseType():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT QCCaseType FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_QCRecordType_NumberSpecies():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT QCRecordType_NumberSpecies FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberSpecies():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT NumberSpecies FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT DeploymentNumber FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SetNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT SetNumber FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentUID():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT DeploymentUID FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_RecordType():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT RecordType FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def callbackFuncSelectVariable2(event):
        VariableListA = entry_SearchVariableList.get()
        print('Selected Search Variable Name :'+ VariableListA)
        if len(VariableListA)!= 0:
            entry_SearchValue_Variable_A.delete(0,END)
        
        if VariableListA == 'DeploymentUID':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else None for i in list(set((Combo_input_DeploymentUID())))])       
        if VariableListA == 'DeploymentNumber':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_DeploymentNumber())))])
        if VariableListA == 'SetNumber':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_SetNumber())))])
        if VariableListA == 'RecordType':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_RecordType())))])
        if VariableListA == 'NumberSpecies':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberSpecies())))])
        
        if VariableListA == 'QCRecordType_NumberSpecies':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_QCRecordType_NumberSpecies())))])
        if VariableListA == 'QCCaseType':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_QCCaseType())))])
        
    def SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value):
        ListVariableSearch = ['DeploymentUID','DeploymentNumber','SetNumber', 'RecordType',
                              'NumberSpecies', 'QCRecordType_NumberSpecies','QCCaseType']
        conn= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=conn.cursor()

        if get_SearchSingleVariable == ListVariableSearch[0]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE DeploymentUID = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[1]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE DeploymentNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[2]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE SetNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[3]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE RecordType = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[4]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE NumberSpecies = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[5]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            if(get_SearchSingleVariable_Value!='None'):
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE QCRecordType_NumberSpecies = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE QCRecordType_NumberSpecies = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows 

        if get_SearchSingleVariable == ListVariableSearch[6]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            if(get_SearchSingleVariable_Value!='None'):
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE QCCaseType = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies WHERE QCCaseType = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        conn.commit()
        conn.close()

    def RunSingleVariableSearchQuery():
        get_SearchSingleVariable        = entry_SearchVariableList.get()
        get_SearchSingleVariable_Value  = entry_SearchValue_Variable_A.get()
        if(len(get_SearchSingleVariable)!=0) & (len(get_SearchSingleVariable_Value)!=0):    
            tree1.delete(*tree1.get_children())
            rows = SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value)
            rows = pd.DataFrame(rows)
            rows.reset_index(drop=True)
            SingleSearchRowsDF = pd.DataFrame(rows)
            SingleSearchRowsDF.rename(columns={0:'DataBase_ID',1: 'RecordIdentifier',2: 'DeploymentUID',
                                            3:'DeploymentNumber',   4:'SetNumber',   5:'RecordType', 
                                            6:'NumberSpecies', 7:'QCRecordType_NumberSpecies', 8:'QCCaseType'},inplace = True)
            df_rows = rows.to_numpy().tolist()
            if rows is not None:
                for row in df_rows:
                    if row[0]%2 == 0:
                        tree1.insert("", "end", values =row, tags =("even2",))
                    else:
                        tree1.insert("", "end", values =row, tags =("odd2",))
            tree1.tag_configure("even2",foreground="black", background="lightblue")
            tree1.tag_configure("odd2",foreground="black", background="ghost white")
            txtTotalSearchEntries.delete(0,END)
            txtTotalSearchEntries.insert(tk.END,len(SingleSearchRowsDF)) 
        else:
            messagebox.showerror('Search Entries Missing', "Search Variable Entry Or Search Value Entry Missing Or Both Entries Missing")

    def GenSummaryQC():
        QCMsg = ['Case-A: In A Set With Only RecType1, NumberSpecies Must 0 or Blank',
                 'Case - A',
                 'Case-B: In A Set With RecType-1/2, NumberSpecies Must Same For Each RecType',
                 'Case - B']
        txtToUpdateEntriesCount.delete(0,END)
        txtAlreadyUpdateEntriesCount.delete(0,END)
        gettotalQCfailCount = QCFailedTotalEntries()
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies ORDER BY `DataBase_ID` ASC ;", conn)
        cursor.close()
        conn.close()
        if len(Complete_df) >0:
            SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
            Summary_RecTyp_NSpecs= SetCatchQCFailedDB_DF.groupby(['QCCaseType', 'QCRecordType_NumberSpecies'],  
                    as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(np.unique(x))))
            Summary_RecTyp_NSpecs  = Summary_RecTyp_NSpecs.reset_index(drop=True)
            Summary_RecTyp_NSpecs  = pd.DataFrame(Summary_RecTyp_NSpecs)
            
            CaseA_RecTyp_NSpecs = Summary_RecTyp_NSpecs[
                                    (Summary_RecTyp_NSpecs.QCCaseType ==QCMsg[1]) &\
                                    (Summary_RecTyp_NSpecs.QCRecordType_NumberSpecies ==QCMsg[0])
                                  ]
            QCEntries_CaseA= len(SetCatchQCFailedDB_DF[
                                (SetCatchQCFailedDB_DF.QCCaseType ==QCMsg[1])])
            
            CaseB_RecTyp_NSpecs = Summary_RecTyp_NSpecs[
                        (Summary_RecTyp_NSpecs.QCCaseType ==QCMsg[3]) &\
                        (Summary_RecTyp_NSpecs.QCRecordType_NumberSpecies ==QCMsg[2])
                        ]
            QCEntries_CaseB= len(SetCatchQCFailedDB_DF[
                                (SetCatchQCFailedDB_DF.QCCaseType ==QCMsg[3])])
            
            if len(CaseA_RecTyp_NSpecs)>0:
                ValueCaseA_RecTyp_NSpecs = (CaseA_RecTyp_NSpecs.iloc[0]['DeploymentUID'])
            else:
                ValueCaseA_RecTyp_NSpecs = 0
            
            if len(CaseB_RecTyp_NSpecs)>0:
                ValueCaseB_RecTyp_NSpecs = (CaseB_RecTyp_NSpecs.iloc[0]['DeploymentUID'])
            else:
                ValueCaseB_RecTyp_NSpecs = 0
            
            QCFailAppend = {'QCCaseType': [QCMsg[1], QCMsg[3]],
                            'QCFailCount': [ValueCaseA_RecTyp_NSpecs, ValueCaseB_RecTyp_NSpecs],
                            'QCEntries':[QCEntries_CaseA, QCEntries_CaseB]}
            QCFailSummaryDF = pd.DataFrame(QCFailAppend)
            QCFailSummaryDF[['QCFailCount']] = QCFailSummaryDF[['QCFailCount']].astype(int)
            QCFailSummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
            QCFailSummaryDF  = QCFailSummaryDF.reset_index(drop=True)
            QCFailSummaryDF = pd.DataFrame(QCFailSummaryDF)
            Summaryframetree.delete(*Summaryframetree.get_children())
            SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
            countIndex1 = 0
            for each_rec in range(len(QCFailSummaryDF)):
                if countIndex1 % 2 == 0:
                    Summaryframetree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("even",))
                else:
                    Summaryframetree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            Summaryframetree.tag_configure("even",foreground="black", background="lightgreen")
            Summaryframetree.tag_configure("odd",foreground="black", background="ghost white")
            txtSummaryDisplayMsg.delete(0,END)
            txtSummaryDisplayMsg.insert(tk.END,"QC Summary Generated. Select & View Each QCCaseType Fail List")
            
            QCFailedSummaryCountUpdate = ValueCaseA_RecTyp_NSpecs + ValueCaseB_RecTyp_NSpecs
            AlreadyUpdateEntriesCount =  int(gettotalQCfailCount) - int(QCFailedSummaryCountUpdate)
            txtToUpdateEntriesCount.insert(tk.END,QCFailedSummaryCountUpdate)
            txtAlreadyUpdateEntriesCount.insert(tk.END,AlreadyUpdateEntriesCount)
        else:
            messagebox.showinfo('Empty Database', "Empty Database Nothing to Generate")
            txtSummaryDisplayMsg.delete(0,END)
            txtSummaryDisplayMsg.insert(tk.END,"Empty Database Nothing to Generate")

    def InventoryRec3(event):
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies ORDER BY `DataBase_ID` ASC ;", conn)
        cursor.close()
        conn.close()
        QCFailDF  = pd.DataFrame(Complete_df)
        nm =Summaryframetree.selection()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            NumberEntriesInSet = sd[1]
            txtSummaryDisplayMsg.delete(0,END)
            
            ListVariableListA = [
                         'Case - A',
                         'Case - B']
            if SelvariableIdentifier == ListVariableListA[0]:
                entry_ViewVarResults.current(2)
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'Case-A: In A Set With Only RecType1, NumberSpecies Must 0 or Blank')
            if SelvariableIdentifier == ListVariableListA[1]:
                entry_ViewVarResults.current(3)
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'Case-B: In A Set With RecType-1/2, NumberSpecies Must Same For Each RecType')

            if (int(NumberEntriesInSet)) > 0:
                txtSummaryDisplayMsg.insert(tk.END,((" QCCaseType : ") +
                                                    SelvariableIdentifier + ' ' +' & '+
                                                    "QCFailCount : " + 
                                                    NumberEntriesInSet))
            else:
                txtSummaryDisplayMsg.insert(tk.END,((" QCCaseType : ") +
                                                    SelvariableIdentifier + ' ' +' & '+
                                                    "QCFailCount : " + 
                                                    NumberEntriesInSet +
                                                    " >>> All Updated or No QC Failed " ))
            
            tree1.delete(*tree1.get_children())
            QCFailDF_Selected = QCFailDF[(
            (QCFailDF['QCCaseType'] == SelvariableIdentifier) 
            )]
            QCFailDF_Selected  = QCFailDF_Selected.reset_index(drop=True)
            QCFailDF_Selected  = pd.DataFrame(QCFailDF_Selected)
            QCFailDF_Selected.sort_values(by=['DeploymentUID','DeploymentNumber','SetNumber','RecordType'], inplace=True)
            QCFailDF_Selected  = QCFailDF_Selected.reset_index(drop=True)
            QCFailDF_Selected  = pd.DataFrame(QCFailDF_Selected)
            countIndex1 = 0
            for each_rec in range(len(QCFailDF_Selected)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(QCFailDF_Selected.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(QCFailDF_Selected.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightgreen")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            ## QC_FailLogical_RNSummary Overview
            SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
            QC_FailLogical_RNSummary = QCFailDF_Selected.loc[:,['DeploymentUID',
                                        'QCCaseType', 'SetNumber']]
            if (len(QC_FailLogical_RNSummary) > 0) & (int(NumberEntriesInSet) > 0):
                QC_FailLogical_RNSummary = QC_FailLogical_RNSummary.groupby(['DeploymentUID', 'QCCaseType'],  
                            as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(x)))
            
                QC_FailLogical_RNSummary.rename(columns={'DeploymentUID':'DeploymentUID', 'QCCaseType':'QCCaseType',     
                                                'SetNumber':'# Of Entries/SetNumber',
                                                },inplace = True)
                QC_FailLogical_RNSummary = QC_FailLogical_RNSummary.loc[:,['DeploymentUID',
                                            'QCCaseType','# Of Entries/SetNumber']]
                QCFailSummaryDF = pd.DataFrame(QC_FailLogical_RNSummary)
                QCFailSummaryDF[['# Of Entries/SetNumber']] = QCFailSummaryDF[['# Of Entries/SetNumber']].astype(int)
                QCFailSummaryDF.sort_values(by=['DeploymentUID'], inplace=True, ascending=False)

                QCFailSummaryDF  = QCFailSummaryDF.reset_index(drop=True)
                QCFailSummaryDF  = pd.DataFrame(QCFailSummaryDF)
                countIndex1 = 0
                for each_rec in range(len(QCFailSummaryDF)):
                    if countIndex1 % 2 == 0:
                        SelResultOverviewtree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("even",))
                    else:
                        SelResultOverviewtree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                SelResultOverviewtree.tag_configure("even",foreground="black", background="lightgreen")
                SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
                entry_SelResultOverview.delete(0,END)
                entry_SelResultOverview.insert(tk.END,((" Unique DeploymentUID Found : ") +
                                                        NumberEntriesInSet))

            else:
                entry_SelResultOverview.delete(0,END)
                entry_SelResultOverview.insert(tk.END,"Empty QCCaseType - All Updated Or No Fail Found")
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END, (' Please Select Only One Entries To View'))

    def UpdateDeploymentUIDAfterUpdate():
        DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
        DB_SetCatch_Validation_Logical = ("./BackEnd/Sqlite3_DB/QC_Check_LogicalConsistency_DB/DFO_NL_ASOP_SetCatch_LogicalValidation.db")
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                                                        'Year','ASOCCode','DeploymentNumber',
                                                                        'SetNumber']]
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(np.nan, 99999999)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace('', 99999999)
                    SetCatchQCFailedDB_DF[['DataBase_ID','RecordIdentifier',
                                            'Year','ASOCCode','DeploymentNumber',
                                            'SetNumber']] = SetCatchQCFailedDB_DF[
                                            ['DataBase_ID','RecordIdentifier',
                                            'Year','ASOCCode','DeploymentNumber',
                                            'SetNumber']].astype(int)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(99999999, '')
                    SetCatchQCFailedDB_DF['DeploymentUID'] = SetCatchQCFailedDB_DF["Year"].map(str) + "-" + \
                                                            SetCatchQCFailedDB_DF["ASOCCode"].map(str)+ "-" +\
                                                            SetCatchQCFailedDB_DF["DeploymentNumber"].map(str)+"-"+ \
                                                            SetCatchQCFailedDB_DF["SetNumber"].map(str)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                        'Year','ASOCCode','DeploymentNumber',
                                                                        'SetNumber']]
                
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    return SetCatchQCFailedDB_DF
                else:
                    return Complete_df
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        def GetQCFailedLogicalNSpeciesDB():
            try:
                conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    NSpeciesDBQCFailedDB_DF  = pd.DataFrame(Complete_df)

                    NSpeciesDBQCFailedDB_DF = NSpeciesDBQCFailedDB_DF.replace(np.nan, 99999999)
                    NSpeciesDBQCFailedDB_DF = NSpeciesDBQCFailedDB_DF.replace('', 99999999)
                    NSpeciesDBQCFailedDB_DF[['DataBase_ID','RecordIdentifier',
                                            'DeploymentNumber','SetNumber']] = NSpeciesDBQCFailedDB_DF[
                                            ['DataBase_ID','RecordIdentifier',
                                            'DeploymentNumber','SetNumber']].astype(int)
                    NSpeciesDBQCFailedDB_DF = NSpeciesDBQCFailedDB_DF.replace(99999999, '')
                    NSpeciesDBQCFailedDB_DF['DeploymentIdentifier'] = NSpeciesDBQCFailedDB_DF["DeploymentUID"].str[0:10] + "-" + \
                                                                      NSpeciesDBQCFailedDB_DF["DeploymentNumber"].map(str)+"-"+ \
                                                                      NSpeciesDBQCFailedDB_DF["SetNumber"].map(str)
                    NSpeciesDBQCFailedDB_DF = NSpeciesDBQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                                                        'DeploymentIdentifier','DeploymentNumber',\
                                                                        'SetNumber', 'RecordType', \
                                                                        'NumberSpecies', 'QCRecordType_NumberSpecies', 'QCCaseType']]
                    NSpeciesDBQCFailedDB_DF.rename(columns={'DataBase_ID':'DataBase_ID', 
                                                            'RecordIdentifier':'RecordIdentifier',
                                                            'DeploymentIdentifier':'DeploymentUID',     
                                                            'DeploymentNumber':'DeploymentNumber',
                                                            'SetNumber':'SetNumber',     
                                                            'RecordType':'RecordType',
                                                            'NumberSpecies':'NumberSpecies',
                                                            'QCRecordType_NumberSpecies':'QCRecordType_NumberSpecies',     
                                                            'QCCaseType':'QCCaseType',
                                                            },inplace = True)
                    NSpeciesDBQCFailedDB_DF  = NSpeciesDBQCFailedDB_DF.reset_index(drop=True)
                    NSpeciesDBQCFailedDB_DF  = pd.DataFrame(NSpeciesDBQCFailedDB_DF)
                    return NSpeciesDBQCFailedDB_DF
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
        UpdateRecordList_SetCatchDB =[]
        df_rows = SetCatchQCFailedDB_DF.to_numpy().tolist()
        for row in df_rows:
            rowValue = row
            list_item_DataBase_ID = int(rowValue[0])
            list_item_RecordIdentifier = int(rowValue[1])
            list_item_DeploymentUID = (rowValue[2])
            list_item_Year = (rowValue[3])
            list_item_ASOCCode = (rowValue[4])
            list_item_DeploymentNumber = (rowValue[5])
            list_item_SetNumber = (rowValue[6])
            UpdateRecordList_SetCatchDB.append((
                        list_item_DeploymentUID,
                        list_item_Year,
                        list_item_ASOCCode,
                        list_item_DeploymentNumber,
                        list_item_SetNumber,
                        list_item_DataBase_ID,
                        list_item_RecordIdentifier,
                        ))
        ## DB Update Executing
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentUID =?, Year = ?, \
                                            ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                            WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                            UpdateRecordList_SetCatchDB)
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()

         ## Get NSpeciesDBQCFailedDB_DF Profile
        NSpeciesDBQCFailedDB_DF = GetQCFailedLogicalNSpeciesDB()
        UpdatedNSpeciesDBQCFailed =[]
        df_rows = NSpeciesDBQCFailedDB_DF.to_numpy().tolist()
        for row in df_rows:
            rowValue = row
            list_item_DataBase_ID = int(rowValue[0])
            list_item_RecordIdentifier = int(rowValue[1])
            list_item_DeploymentUID = (rowValue[2])
            list_item_DeploymentNumber = (rowValue[3])
            list_item_SetNumber = (rowValue[4])
            list_item_RecordType = (rowValue[5])
            list_item_NumberSpecies = (rowValue[6])
            list_item_QCRecordType_NumberSpecies = (rowValue[7])
            list_item_QCCaseType = (rowValue[8])
            UpdatedNSpeciesDBQCFailed.append((
                    list_item_DeploymentUID,
                    list_item_DeploymentNumber,
                    list_item_SetNumber,
                    list_item_RecordType,
                    list_item_NumberSpecies,
                    list_item_QCRecordType_NumberSpecies,
                    list_item_QCCaseType,
                    list_item_DataBase_ID,
                    list_item_RecordIdentifier,
                    ))
        ## DB Update Executing
        conn_DB_SetCatch_Validation_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur_DB_SetCatch_Validation_Logical=conn_DB_SetCatch_Validation_Logical.cursor()
        cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET DeploymentUID =?, DeploymentNumber = ?, \
                                                    SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                                    QCRecordType_NumberSpecies = ?, QCCaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdatedNSpeciesDBQCFailed)
        conn_DB_SetCatch_Validation_Logical.commit()
        conn_DB_SetCatch_Validation_Logical.close()
        viewQCFailed_VariablesProfile()
        txtDisplayMessageSystem.delete(0,END)
        txtDisplayMessageSystem.insert(tk.END,'Finished Update')
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    def InventoryRec4(event):
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies ORDER BY `DataBase_ID` ASC ;", conn)
        cursor.close()
        conn.close()
        QCFailDF  = pd.DataFrame(Complete_df)
        nm =SelResultOverviewtree.selection()
        if len(nm) ==1:
            sd = SelResultOverviewtree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            NumberEntriesInSet = sd[2]
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END,(("Selected DeploymentUID : ") +
                                                SelvariableIdentifier + ' ' +' & '+
                                                "# Of Entries/SetNumber : " + 
                                                NumberEntriesInSet))
            entry_SelResultOverview.delete(0,END)
            entry_SelResultOverview.insert(tk.END,(("Selected DeploymentUID : ") +
                                                SelvariableIdentifier))
            tree1.delete(*tree1.get_children())
            QCFailDF_Selected = QCFailDF[(
            (QCFailDF['DeploymentUID'] == SelvariableIdentifier) 
            )]
            QCFailDF_Selected  = QCFailDF_Selected.reset_index(drop=True)
            QCFailDF_Selected  = pd.DataFrame(QCFailDF_Selected)
            QCFailDF_Selected.sort_values(by=['DeploymentNumber','SetNumber','RecordType'], inplace=True)
            QCFailDF_Selected  = QCFailDF_Selected.reset_index(drop=True)
            QCFailDF_Selected  = pd.DataFrame(QCFailDF_Selected)
            countIndex1 = 0
            for each_rec in range(len(QCFailDF_Selected)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(QCFailDF_Selected.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(QCFailDF_Selected.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="grey")
            tree1.tag_configure("odd",foreground="black", background="grey")
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END, (' Please Select Only One Entries To View'))
    
    def ExcelViewEditBackend_RecType_1_2(QC_FailLogical_DF):
        if len(QC_FailLogical_DF) >0:
            QC_FailLogical_DF.sort_values(by=['DeploymentUID', 'DeploymentNumber',
                'SetNumber','RecordType'], inplace=True)
            QC_FailLogical_DF  = QC_FailLogical_DF.reset_index(drop=True)
            QC_FailLogical_DF  = pd.DataFrame(QC_FailLogical_DF)   
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0,'Viewing Searched QC Failed Excel File In Seperate Window')
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = QC_FailLogical_DF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(QC_FailLogical_DF),2), clr='lightblue', cols='all')
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
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber',
                            'RecordType','NumberSpecies']]).replace(
                            ['', None, np.nan, 'None'], 99999999)
                
                Complete_df[['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber', 'SetNumber', 'RecordType',
                            'NumberSpecies']] = Complete_df[
                            ['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber', 'SetNumber', 'RecordType',
                            'NumberSpecies']].astype(int)
                
                Complete_df[['DeploymentUID']] = Complete_df[['DeploymentUID']].astype(str)
                
                Complete_df = Complete_df.replace([99999999, 99999999.0, '99999999'], '')
                if len(Complete_df) >0:
                    iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                            "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                    if iSubmit >0:
                        try:
                            BackendSubmitAndUpdateDB(Complete_df)
                        except sqlite3.Error as error:
                            print('Error occured - ', error)
                        finally:
                            pt.redraw()
                            tkinter.messagebox.showinfo("Submit Success","Successfully Submitted Update To Database")
                else:
                    tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

            def BackendSubmitAndUpdateDB(Complete_df):
                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                conn_DB_SetCatch_Validation_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
                cur_DB_SetCatch_Validation_Logical=conn_DB_SetCatch_Validation_Logical.cursor()
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList_QCFailDB =[]
                df_rows = Complete_df.to_numpy().tolist()
                for row in df_rows:
                    rowValue = row
                    list_item_DataBase_ID = int(rowValue[0])
                    list_item_RecordIdentifier = int(rowValue[1])
                    list_item_DeploymentUID = (rowValue[2])
                    list_item_DeploymentNumber = (rowValue[3])
                    list_item_SetNumber = (rowValue[4])
                    list_item_RecordType = (rowValue[5])
                    list_item_NumberSpecies = (rowValue[6])
                    list_item_QCCaseType = 'Case Updated'
                    
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_DeploymentUID,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_RecordType,
                                        list_item_NumberSpecies,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        ))
                    UpdateRecordList_QCFailDB.append((
                                        list_item_DeploymentUID,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_RecordType,
                                        list_item_NumberSpecies,
                                        list_item_QCCaseType,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        ))
                            
                            ## DB Update Executing
                
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentUID =?, DeploymentNumber = ?, \
                                        SetNumber = ?, RecordType = ?, NumberSpecies = ?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                        UpdateRecordList_SetCatchDB)
                cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_NumberSpecies SET DeploymentUID =?, DeploymentNumber = ?, \
                                        SetNumber = ?, RecordType = ?, NumberSpecies = ?, QCCaseType = ?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                        UpdateRecordList_QCFailDB)
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
                conn_DB_SetCatch_Validation_Logical.commit()
                conn_DB_SetCatch_Validation_Logical.close()

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
                                                bg= "cadet blue", text="NB : Do Not Edit Columns : DataBase_ID, RecordIdentifier, DeplymentUID")
            lbl_CautionSteps.grid(row =10, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_CautionSteps_1 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="NB : Edit/Modify Year/ASOC/DepN/SetN Columns Requires Edit DeplymentUID Accordingly")
            lbl_CautionSteps_1.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)
            windows.mainloop() 
    
    def SearchDepNumFromSetCatchDB():
        try:
            get_DepNumforSearch = int(entry_DepNumforSearch.get())
        except:
            messagebox.showerror('Search Variable Datatype Error Message', "Search Value Must Be Integer Value")
        checkinttype = isinstance(get_DepNumforSearch,int)
        if checkinttype == True:  
            conn_DB= sqlite3.connect(DB_Set_Catch_Analysis)
            if (get_DepNumforSearch) >= 0:       
                get_SearchSingleVariable_Value = (get_DepNumforSearch)
                rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                conn_DB.commit()
                conn_DB.close() 
                rows = rows[(rows.DeploymentNumber) == get_SearchSingleVariable_Value]
                rows  = rows.reset_index(drop=True)
                rows= (rows.loc[:,
                    ['DataBase_ID','RecordIdentifier','DeploymentUID',
                    'DeploymentNumber','SetNumber',
                    'RecordType','NumberSpecies']])
                QCFailedLogical_DF  = pd.DataFrame(rows)
                ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF)
    
    def SearchDepUIDNumFromSetCatchDB():
        get_DepUIDforSearch = entry_SelResultOverview.get()
        get_DepUIDforSearch = get_DepUIDforSearch.split(" : ")
        get_DepUIDforSearch =str(get_DepUIDforSearch[1])
        conn_DB= sqlite3.connect(DB_Set_Catch_Analysis)
        if len(get_DepUIDforSearch) >= 0:       
            get_SearchSingleVariable_Value = (get_DepUIDforSearch)
            rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
            conn_DB.commit()
            conn_DB.close() 
            rows = rows[(rows.DeploymentUID) == get_SearchSingleVariable_Value]
            rows  = rows.reset_index(drop=True)
            rows= (rows.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                'DeploymentNumber','SetNumber',
                'RecordType','NumberSpecies']])
            QCFailedLogical_DF  = pd.DataFrame(rows)
            ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF)
    
    def QCFailedExcelViewAll():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        SetCatchQCFailedDB_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_NumberSpecies;", conn)
        SetCatchQCFailedDB_DF = pd.DataFrame(SetCatchQCFailedDB_DF)
        cursor.close()
        conn.close()
        SetCatchQCFailedDB_DF= (SetCatchQCFailedDB_DF.loc[:,
            ['DataBase_ID','RecordIdentifier','DeploymentUID',
            'DeploymentNumber','SetNumber',
            'RecordType','NumberSpecies',
            'QCRecordType_NumberSpecies', 'QCCaseType']])
        SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
        QCFailedLogical_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
        ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF)
    
    ## Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    SelResultOverviewtree.bind('<<TreeviewSelect>>',InventoryRec4)
    
    ## ComboBox
    entry_UpdateVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable1)
    entry_SearchVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable2)
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ## GenSummaryQC
    GenSummaryQC()
    QCFailedTotalEntries()

    # ## Button Wizard :
    Buttonframe = Frame(Tableframe, width = 40)
    Buttonframe.pack(side = TOP, padx= 0, pady=0)
    btnViewQCFailedQCResults = Button(TopFrame, text="View Selected Results", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=18, bd=1, command = viewQCFailed_VariablesProfile)
    btnViewQCFailedQCResults.grid(row =1, column = 1, padx=365, pady =2, ipady =2, sticky =W)

    btnClearTable = Button(TopFrame, text="Clear Table", font=('aerial', 10, 'bold'), bg='alice blue',
                             height =1, width=10, bd=1, command = ClearTablesAll)
    btnClearTable.grid(row =1, column = 1, padx=270, pady =2, ipady =2, sticky =E)

    btnSearchDepSetCatchDB = Button(TopFrame, text="Search SetCatch Deployment", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=25, bd=1, command = SearchDepNumFromSetCatchDB)
    btnSearchDepSetCatchDB.grid(row =1, column = 1, padx=2, pady =2, ipady =2, sticky =E)

    ### Buttons On Update Frame
    button_UpdateSelectedDBEntries = Button(UpdateDB_Entryframe, bd = 2, text ="Update Selected Table Entries\n (DB Update)", width = 25,
                                height=2, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =UpdateSelected_SetCatch_DBEntries)
    button_UpdateSelectedDBEntries.grid(row =14, column = 0, padx=10, pady =5, ipady =4, sticky =W)

    button_Clear_EntriesUpdate = Button(UpdateDB_Entryframe, bd = 2, text ="Clear Entries", width = 10,
                                height=1, font=('aerial', 8, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearEntries)
    button_Clear_EntriesUpdate.grid(row =6, column = 0, padx=15, pady =2, ipady =2, sticky =E)

    ### Buttons On Search Frame
    button_SearchSingleVariableQuery = Button(SearchDB_Entryframe, bd = 2, text ="Run Single Variable Search\n (DB Search) ", width = 26,
                                height=2, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunSingleVariableSearchQuery)
    button_SearchSingleVariableQuery.grid(row =14, column = 0, padx=2, pady =8, ipady =8, sticky =W)


    ## Buttons On Generate QC Failed Summary Frame
    button_GenSummaryQC = Button(Summaryframe, bd = 2, text ="Generate QC Fail Summary ", width = 26,
                                height=1, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSummaryQC)
    button_GenSummaryQC.pack(side =TOP)

    button_SearchDepUID = Button(SelResultOverview, bd = 1, text ="Select & Search SetCatch DepUID", width = 28,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =SearchDepUIDNumFromSetCatchDB)
    button_SearchDepUID.pack(side =TOP,pady =2, ipady =2, anchor = W)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    ImportExport  = Menu(menu, tearoff=0)
    View  = Menu(menu, tearoff=0)
    Update  = Menu(menu, tearoff=0)
    
    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Import/Export", menu=ImportExport)
    menu.add_cascade(label="View", menu=View)
    menu.add_cascade(label="Update", menu=Update)

    filemenu.add_command(label="Exit", command=iExit)
    ImportExport.add_command(label="Export Failed Results (.csv)", command=Export_LogicalFailed_RN_CSV)
    ImportExport.add_command(label="Import & Update DB (.csv)", command=ImportAndUpdateSetCatchDB)
    View.add_command(label="View Edit & Update QCFailed Results", command=QCFailedExcelViewAll)
    View.add_command(label="Ref-QCFail To Set&Catch DB", command=RefFailedToSetcatchDB)
    Update.add_command(label="Update DeplymentUID", command=UpdateDeploymentUIDAfterUpdate)
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack()
    window.mainloop()


