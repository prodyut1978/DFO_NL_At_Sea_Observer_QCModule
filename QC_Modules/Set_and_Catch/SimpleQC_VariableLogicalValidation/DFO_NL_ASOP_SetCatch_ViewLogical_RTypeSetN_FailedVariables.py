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

def ViewLogicalRT_SNValidatedResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Logical Validator - ID-C-04-1")
    window.geometry("1420x830+200+100")
    window.config(bg="cadet blue")

    ## Top Frame
    TopFrame = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    TopFrame.pack(side = TOP, padx= 0, pady=0)

    lbl_TopFrame = Label(TopFrame, font=('aerial', 10, 'bold'), text="A. QC Fail Table :")
    lbl_TopFrame.grid(row =1, column = 0, padx=2, pady =1, ipady=1, sticky =W)

    ListVariableListA = ['Select RecordType-SetNumber Logical Fail View Type', 
                         'View Case-A: QC Fail With Multi RecordType1 Presents In A Set',
                         'View Case-B: QC Fail With Null RecordType1 Presents In A Set', 
                         'View Case-A,B: QC Fail With Multi Or Null RecordType1 Presents In A Set']
    VariableList        = StringVar(TopFrame, value ='')
    entry_ViewVarResults  = ttk.Combobox(TopFrame, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable = VariableList, width = 50, state='readonly')
    entry_ViewVarResults.grid(row =1, column = 1, padx=40, pady =4, ipady= 4, sticky =W)
    entry_ViewVarResults['values'] = ListVariableListA
    entry_ViewVarResults.current(0)

    EntryDepNum       = IntVar(TopFrame, value ='Enter DeploymentNumber')
    entry_DepNumforSearch = Entry(TopFrame, font=('aerial', 10), justify='center',
                                textvariable = EntryDepNum, width = 25, bd=2)
    entry_DepNumforSearch.grid(row =0, column = 1, padx=10, pady =2, ipady =5, sticky =E)

    ListFilterBy = ['Both RecType 1&2', 
                    'RecType-1 Only']
    FilterByList        = StringVar(TopFrame, value ='')
    entry_FilterByList  = ttk.Combobox(TopFrame, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable =FilterByList, width = 18, state='readonly')
    entry_FilterByList.grid(row =1, column = 2, padx=1, pady =4, ipady= 4, sticky =W)
    entry_FilterByList['values'] = ListFilterBy
    entry_FilterByList.current(0)

    lbl_TotalFailedEntries = Label(TopFrame, font=('aerial', 10 , 'bold'), text="# Of Set Failed :")
    lbl_TotalFailedEntries.grid(row =0, column = 0, padx=1, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(TopFrame, value='')
    txtTotalFailedEntries = Entry(TopFrame, font=('aerial',12),textvariable = TotalFailedEntries, width = 5, bd=1)
    txtTotalFailedEntries.grid(row =0, column = 0, padx=120, pady =1, ipady =1, sticky =W)

    txtDisplayMessageSystem = Entry(TopFrame, font=('aerial', 9), justify='center',
                            textvariable = StringVar(window, value='QC Message Display'), width = 84, bd=2)
    txtDisplayMessageSystem.grid(row =0, column = 1, padx=40, pady =2, ipady =5, sticky =W)

    Tableframe = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    ## Tree1 Table View 
    Tableframe = Frame(window, width = 40)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", "column4", 
                    "column5", "column6", "column7", "column8"), height=22, show='headings')
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
    tree1.heading("#4", text="RecordType", anchor=CENTER)
    tree1.heading("#5", text="DeploymentNumber", anchor=CENTER)
    tree1.heading("#6", text="SetNumber", anchor=CENTER)
    tree1.heading("#7", text="RecType-SetNumber-QC Message", anchor=CENTER)
    tree1.heading("#8", text="QC CaseType", anchor=CENTER)
    
    tree1.column('#1', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=450, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)

   # Frame Of Update modules
    UpdateDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    UpdateDB_Entryframe.pack(side =LEFT, padx=2, pady =2)

    lbl_UpdateDB_Header = Label(UpdateDB_Entryframe, font=('aerial', 11, 'bold','underline'),
                                bg= "cadet blue", text="Update / Delete Database ")
    lbl_UpdateDB_Header.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_SelectTableEntries = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Table Entries:")
    lbl_SelectTableEntries.grid(row =4, column = 0, padx=2, pady =2, sticky =W)
    NumberRowSelected       = IntVar(UpdateDB_Entryframe, value ='# Of Selected')
    entry_NumberRowSelected = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), justify='center',
                                textvariable = NumberRowSelected, width = 15, bd=1)
    entry_NumberRowSelected.grid(row =4, column = 0, padx=2, pady =4, ipady =4, sticky =E)

    lbl_Select_List_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 2. Select Variable :")
    lbl_Select_List_Variable.grid(row =6, column = 0, padx=2, pady =2, sticky =W)
    
    ListVariableListA = ['DeploymentNumber','SetNumber','RecordType']
    VariableListA        = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = VariableListA, width = 18, state='readonly')
    entry_UpdateVariableList.grid(row =8, column = 0, padx=10, pady =2, ipady= 2, sticky =W)
    entry_UpdateVariableList['values'] = sorted(list(ListVariableListA))

    lbl_EntryUpdate_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 3. Enter Updated Value :")
    lbl_EntryUpdate_Variable.grid(row =10, column = 0, padx=2, pady =2, sticky =W)
    
    UpdateValue_VariableA       = IntVar(UpdateDB_Entryframe, value ='')
    entry_UpdateValue_VariableA = Entry(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = UpdateValue_VariableA, width = 15, bd=2)
    entry_UpdateValue_VariableA.grid(row =12, column = 0, padx=10, pady =2, ipady =2, sticky =W)

    EntryDataType_Variable       = StringVar(UpdateDB_Entryframe, value ='Variable Type')
    entry_EntryDataType_Variable = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), 
                                        textvariable = EntryDataType_Variable, width = 15, bd=1)
    entry_EntryDataType_Variable.grid(row =12, column = 0, padx=4, pady =4, ipady =4, sticky =E)

    ## ####Frame Of search modules ########
    SearchDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SearchDB_Entryframe.pack(side =LEFT, padx=10, pady =2)

    lbl_SearchDB_Header = Label(SearchDB_Entryframe, font=('aerial', 11, 'bold','underline'), 
                                bg= "cadet blue", text="Search Database:")
    lbl_SearchDB_Header.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_SelectSinglevariableSearch_A = Label(SearchDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Variable :")
    lbl_SelectSinglevariableSearch_A.grid(row =3, column = 0, padx=2, pady =1, ipady= 4, sticky =W)

    ListVariableSearch = ['DeploymentUID','DeploymentNumber',
                          'SetNumber', 'RecordType',
                          'QCRecordType_SetNumber']
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

    ## ### Frame QC Failed Summary ####
    SummaryQCframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.pack(side =LEFT, padx=4, pady =3)

    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    Summaryframetree = ttk.Treeview(Summaryframe, column=("column1", "column2", 
                                                          "column3", "column4",
                                                          "column5"),
                                    height=11, show='headings')
    scrollbary = ttk.Scrollbar(Summaryframe, orient ="vertical", command=Summaryframetree.yview)
    scrollbary.pack(side ='right', fill ='y')
    Summaryframetree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(Summaryframe, orient ="horizontal", command=Summaryframetree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    Summaryframetree.configure(xscrollcommand = scrollbarx.set)
    Summaryframetree.heading("#1", text="DeploymentUID", anchor=CENTER)
    Summaryframetree.heading("#2", text="RecType1 Count/Set ", anchor=CENTER)
    Summaryframetree.heading("#3", text="RecordType", anchor=CENTER)
    Summaryframetree.heading("#4", text="SetNum", anchor=CENTER)
    Summaryframetree.heading("#5", text="DepNum", anchor=CENTER)
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)            
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    Summaryframetree.column('#3', stretch=NO, minwidth=0, width=90, anchor=tk.CENTER)
    Summaryframetree.column('#4', stretch=NO, minwidth=0, width=80, anchor=tk.CENTER)
    Summaryframetree.column('#5', stretch=NO, minwidth=0, width=80, anchor=tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    style = ttk.Style(Summaryframetree)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    Summaryframetree.pack(side = BOTTOM)

    # ### Frame Generate QC Failed Summary ####
    GenSummaryQCframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    GenSummaryQCframe.pack(side =LEFT, padx=4, pady =2)
    
    GenSummaryDisplay = tk.Frame(GenSummaryQCframe, bg= "aliceblue")
    GenSummaryDisplay.pack(side = BOTTOM, pady=0)
    txtGenSummaryDisplayMsg = Entry(GenSummaryDisplay, font=('aerial', 10),
                            textvariable = StringVar(window, value='QC Summary Message'), width = 35, bd=2)
    txtGenSummaryDisplayMsg.grid(row =0, column = 0, padx=10, pady =4, ipady =5, sticky =E)

    lbl_ToUpdateEntriesCount = Label(GenSummaryDisplay, font=('aerial', 11 , 'bold'), text=" A: # Of Set Entries To Update")
    lbl_ToUpdateEntriesCount.grid(row =2, column = 0, padx=2, pady =4, ipady=4, sticky =W)
    ToUpdateEntriesCount = IntVar(GenSummaryDisplay, value='')
    txtToUpdateEntriesCount = Entry(GenSummaryDisplay, font=('aerial',11),
                                   textvariable = ToUpdateEntriesCount, 
                                   width = 8, bd=2)
    txtToUpdateEntriesCount.grid(row =4, column = 0, padx=20, pady =3, ipady =5, sticky =W)
   
    lbl_AlreadyUpdateEntriesCount = Label(GenSummaryDisplay, font=('aerial', 11 , 'bold'), text=" B: # Of Set Entries Updated")
    lbl_AlreadyUpdateEntriesCount.grid(row =6, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    AlreadyUpdateEntriesCount = IntVar(GenSummaryDisplay, value='')
    txtAlreadyUpdateEntriesCount = Entry(GenSummaryDisplay, font=('aerial',11),
                                   textvariable = AlreadyUpdateEntriesCount, 
                                   width = 8, bd=2)
    txtAlreadyUpdateEntriesCount.grid(row =8, column = 0, padx=20, pady =3, ipady =5, sticky =W)

    ## Define Functions
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'RecordType','DeploymentNumber',
                            'SetNumber','QCRecordType_SetNumber', 'QC_CaseType']
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
                        DataBase_ID                 = (df.loc[:,'DataBase_ID']).fillna(99999999).astype(int)
                        RecordIdentifier            = (df.loc[:,'RecordIdentifier']).fillna(99999999).astype(int)
                        DeploymentUID               = (df.loc[:,'DeploymentUID']).fillna(8888888).astype(str)
                        RecordType                  = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        DeploymentNumber            = (df.loc[:,'DeploymentNumber']).fillna(99999999).astype(int, errors='ignore')
                        SetNumber                   = (df.loc[:,'SetNumber']).fillna(99999999).astype(int, errors='ignore')
                        QCRecordType_SetNumber      = (df.loc[:,'QCRecordType_SetNumber']).fillna(8888888).astype(str, errors='ignore')
                       
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID,\
                                        RecordType, DeploymentNumber, SetNumber, QCRecordType_SetNumber]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns =  {0:'DataBase_ID',  1: 'RecordIdentifier',  2: 'DeploymentUID',
                                                 3:'RecordType',   4:'DeploymentNumber',   5:'SetNumber', 
                                                 6:'QCRecordType_SetNumber'
                                                },inplace = True)
                        Raw_Imported_Df = pd.DataFrame(catdf)
                        Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0, '.'], '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([8888888, '8888888', '.'], 'None')
                        Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                        Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                        
                        RecType_1_QCMessage = 'Only One & Atleast One RecordType1 Per SetNumber'
                        RecType_2_QCMessage =''
                        Raw_Imported_Df['QCRecordType_SetNumber'] = np.where(Raw_Imported_Df['RecordType']== 1, 
                                            RecType_1_QCMessage, RecType_2_QCMessage)
                        Raw_Imported_Df = Raw_Imported_Df.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'RecordType','DeploymentNumber','SetNumber', 'QCRecordType_SetNumber']]
                        Raw_Imported_Df.sort_values(by=['DeploymentUID','DeploymentNumber','SetNumber','RecordType'], inplace=True)
                        Raw_Imported_Df  = Raw_Imported_Df.reset_index(drop=True)
                        Raw_Imported_Df  = pd.DataFrame(Raw_Imported_Df)
                        
                        CheckEmptyNessColumn = Raw_Imported_Df[
                                            (Raw_Imported_Df.DataBase_ID=='') |
                                            (Raw_Imported_Df.RecordIdentifier=='') |
                                            (Raw_Imported_Df.DeploymentUID=='None') |
                                            (Raw_Imported_Df.DeploymentUID=='') |
                                            (Raw_Imported_Df.RecordType=='')|                                        
                                            (Raw_Imported_Df.DeploymentNumber=='') |
                                            (Raw_Imported_Df.SetNumber=='')
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
                                list_item_RecordType = (rowValue[3])
                                list_item_DeploymentNumber = (rowValue[4])
                                list_item_SetNumber = (rowValue[5])
                                list_item_QCRecordType_SetNumber = (rowValue[6])
                                list_item_QC_CaseType = 'Case: Updated'
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_DeploymentUID,
                                                    list_item_RecordType,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    ))
                                UpdateRecordList_QCFailDB.append((
                                                    list_item_DeploymentUID,
                                                    list_item_RecordType,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_QCRecordType_SetNumber,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    ))
                            
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentUID =?,\
                                                    RecordType = ?, DeploymentNumber = ?, SetNumber = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdateRecordList_SetCatchDB)
                            cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET DeploymentUID =?,\
                                                    RecordType = ?, DeploymentNumber = ?, SetNumber = ?,\
                                                    QCRecordType_SetNumber = ?, QC_CaseType=?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdateRecordList_QCFailDB)
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Logical.commit()
                            conn_DB_SetCatch_Validation_Logical.close()
                            txtDisplayMessageSystem.delete(0,END)
                            txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                    else:
                        messagebox.showerror('Import File Empty Variables', "Please Check The Null Variable Input")
        txtDisplayMessageSystem.insert(tk.END,'  & Update Successfully')
        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Imported Entries")  
    
    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def ClearTablesAll():
        tree1.delete(*tree1.get_children())
        Summaryframetree.delete(*Summaryframetree.get_children())
        txtTotalFailedEntries.delete(0,END)

    def ClearEntries():
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateValue_VariableA.delete(0,END)
        entry_NumberRowSelected.delete(0,END)     
    
    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select RecordType-SetNumber Logical Fail View Type', 
                         'View Case-A: QC Fail With Multi RecordType1 Presents In A Set',
                         'View Case-B: QC Fail With Null RecordType1 Presents In A Set', 
                         'View Case-A,B: QC Fail With Multi Or Null RecordType1 Presents In A Set']
        QCRecT_SNmsg = ['Only One RecordType1 Allowed Per SetNumber',
                        'Atleast One RecordType1 Must Present Per SetNumber']
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Logical)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows)
            rows = rows.reset_index(drop=True)
            rows.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 
                                 2:'DeploymentUID', 3:'RecordType',
                                 4:'DeploymentNumber', 5:'SetNumber', 
                                 6:'QCRecordType_SetNumber', 7:'QC_CaseType'},inplace = True)
            if getVarnameToView == ListVariableListA[3]:
                rows = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[2]:
                rows = rows[(rows.QCRecordType_SetNumber) == QCRecT_SNmsg[1]]
                rows = rows.reset_index(drop=True)
                rows = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[1]:
                rows = rows[(rows.QCRecordType_SetNumber) == QCRecT_SNmsg[0]]
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
        ListVariableListA = ['Select RecordType-SetNumber Logical Fail View Type', 
                         'View Case-A: QC Fail With Multi RecordType1 Presents In A Set',
                         'View Case-B: QC Fail With Null RecordType1 Presents In A Set', 
                         'View Case-A,B: QC Fail With Multi Or Null RecordType1 Presents In A Set']
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        if len(rows) >0 :
            rows.sort_values(by=['DeploymentUID', 'DeploymentNumber','SetNumber',
                                 'RecordType'], inplace=True)
            rows  = rows.reset_index(drop=True)
            rows  = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[0]:
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(0, 'Select RecordType-SetNumber View Type From DropDown & Run View Selected Button')
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
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(0, ('Populated  -' + getVarnameToView))
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 'Empty QC Fail DB. Nothing to Display')

    def callbackFuncSelectView(event):
        ListVariableListA = ['Select RecordType-SetNumber Logical Fail View Type', 
                         'View Case-A: QC Fail With Multi RecordType1 Presents In A Set',
                         'View Case-B: QC Fail With Null RecordType1 Presents In A Set', 
                         'View Case-A,B: QC Fail With Multi Or Null RecordType1 Presents In A Set']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            tree1.delete(*tree1.get_children())
            
        if(SelVariableView ==ListVariableListA[0]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'For A Set With RecType-1,2 - Only & Atleast One RecordType 1 Must Present Per SetNumber')
            
        if(SelVariableView ==ListVariableListA[1]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'View Case-A: QC Fail With Multi RecordType1 Presence In A Set')
            
        if(SelVariableView ==ListVariableListA[2]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'View Case-B: QC Fail With Null RecordType1 Presence In A Set')

        if(SelVariableView ==ListVariableListA[3]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'View Case-A,B: QC Fail With Multi Or Null RecordType1 Presents In A Set')   
       
    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        data = data.drop_duplicates(subset=['DeploymentUID','DeploymentNumber','SetNumber'], keep="first")
        if len(data)>0:
            QCFailedTotalEntries = len(data)       
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)
        else:
            QCFailedTotalEntries = 0     
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)
        conn.commit()
        conn.close()
        return QCFailedTotalEntries

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def Export_LogicalFailed_RT_SN_CSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber;", conn)
            if len(Complete_df) >0:
                Complete_df.sort_values(by=['DeploymentUID','DeploymentNumber','SetNumber','RecordType'], inplace=True)
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("QC Failed Logical RecType-SetNumber","QC Failed Logical RecType-SetNumber Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("QC Failed Logical RecType-SetNumber Report Message","Please Select File Name To Export")
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
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber ORDER BY `DataBase_ID` ASC ;", conn)
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
        Ref_FailedQC_InSetcatchDB.sort_values(by=['DeploymentNumber','SetNumber','RecordType'], inplace=True)
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
            SelvariableIdentifier = sd[4]
            entry_DepNumforSearch.insert(tk.END,SelvariableIdentifier)
            txtDisplayMessageSystem.insert(tk.END,(QcMessage + SelvariableIdentifier))
        len_curItems = len(curItems)
        if len_curItems < 20001:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,len_curItems)
        else:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,'MaxLimit Exceed')
    
    def SetcatchDB_VariableList():
        GetSetCatchDB_VariableList = ['RecordType','DeploymentNumber','SetNumber']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, 
                                         UpdateRecordList_SetCatchDB, 
                                         UpdateRecordList_QCFailDB,
                                         UpdateCase_QCFailDB):
        
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

        conn_Validation_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur_Validation_Logical=conn_Validation_Logical.cursor()
        
        ## Updaing SetCatch DB
        if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_SetCatchDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList_SetCatchDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_SetCatchDB)

        ### Updating QC Failed DB
        if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET RecordType = ?, \
                                                 QCRecordType_SetNumber =?\
                                                 WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET QC_CaseType = ?\
                                                 WHERE DeploymentUID =?", 
                                                UpdateCase_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET DeploymentNumber = ?, \
                                                 QCRecordType_SetNumber =?\
                                                 WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET QC_CaseType = ?\
                                                 WHERE DeploymentUID =?", 
                                                UpdateCase_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET SetNumber = ?, \
                                                 QCRecordType_SetNumber =?\
                                                 WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET QC_CaseType = ?\
                                                 WHERE DeploymentUID =?", 
                                                UpdateCase_QCFailDB)
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Logical.commit()
        conn_Validation_Logical.close()
        UpdateDeploymentUIDAfterUpdate()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18 = ['DeploymentNumber','SetNumber', 'RecordType']
                        
            Var_Class_String7 = ['DeploymentUID']
            
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
                        UpdateCase_QCFailDB =[]   
                        for item in tree1.selection():
                            list_item = (tree1.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            list_item_QCRecordType_SetNumber =(list_item[6])
                            list_item_QC_CaseType = 'Case: Updated'
                            
                            UpdateRecordList_SetCatchDB.append((get_UpdateValue_UpdatedVariable, 
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                            
                            UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,
                                                        list_item_QCRecordType_SetNumber,
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                            
                            UpdateCase_QCFailDB.append((list_item_QC_CaseType, 
                                                        list_item_DeploymentUID))
                            
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, 
                                                        UpdateRecordList_SetCatchDB,
                                                        UpdateRecordList_QCFailDB,
                                                        UpdateCase_QCFailDB)
                        
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(tk.END,"Set & Catch Database Updated Successfully")
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")    
                        
                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                        iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                                                                    "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                        if iUpdateSlected >0:
                            UpdateRecordList_SetCatchDB =[]
                            UpdateRecordList_QCFailDB =[]
                            UpdateCase_QCFailDB =[]   
                            for item in tree1.selection():
                                list_item = (tree1.item(item, 'values'))
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                list_item_QCRecordType_SetNumber =(list_item[6])
                                list_item_QC_CaseType = 'Case: Updated'
                                
                                UpdateRecordList_SetCatchDB.append((get_UpdateValue_UpdatedVariable, 
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                                
                                UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,
                                                        list_item_QCRecordType_SetNumber,
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                            
                                UpdateCase_QCFailDB.append((list_item_QC_CaseType, 
                                                            list_item_DeploymentUID))
                            
                            Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, 
                                                             UpdateRecordList_SetCatchDB, 
                                                             UpdateRecordList_QCFailDB)
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
            
                tree1.delete(*tree1.get_children())
                entry_ViewVarResults.current(0)
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
            EntryDataType_Variable = 'Alpha Numeric'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)
        else:
            EntryDataType_Variable = 'Numeric'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)

    def Combo_input_QCRecordType_SetNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT QCRecordType_SetNumber FROM SetCatch_QCFailedLogical_RecordType_SetNumber")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT DeploymentNumber FROM SetCatch_QCFailedLogical_RecordType_SetNumber")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SetNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT SetNumber FROM SetCatch_QCFailedLogical_RecordType_SetNumber")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentUID():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT DeploymentUID FROM SetCatch_QCFailedLogical_RecordType_SetNumber")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_RecordType():
        con= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=con.cursor()
        cur.execute("SELECT RecordType FROM SetCatch_QCFailedLogical_RecordType_SetNumber")
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
        if VariableListA == 'QCRecordType_SetNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_QCRecordType_SetNumber())))])
        
    def SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value):
        ListVariableSearch = ['DeploymentUID','DeploymentNumber','SetNumber', 'RecordType',
                              'QCRecordType_SetNumber']
        conn= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur=conn.cursor()

        if get_SearchSingleVariable == ListVariableSearch[0]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber WHERE DeploymentUID = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[1]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber WHERE DeploymentNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[2]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber WHERE SetNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[3]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber WHERE RecordType = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[4]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            if(get_SearchSingleVariable_Value!='None'):
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber WHERE QCRecordType_SetNumber = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber WHERE QCRecordType_SetNumber = ?", (get_SearchSingleVariable_Value,))
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
                                            3:'RecordType',   4:'DeploymentNumber',   5:'SetNumber', 
                                            6:'QCRecordType_SetNumber'},inplace = True)
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

    def GenSummaryQC_Backend():
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
         ## QC On RecordType_SetNumber
        RecordType_SetNumber_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber','RecordType',]]).replace(['','None'], 99999999)
        
        RecordType_SetNumber_FailLogical[['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber','SetNumber', 'RecordType']] = RecordType_SetNumber_FailLogical[
                            ['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber','SetNumber', 'RecordType']
                            ].astype(int)
        RecordType_SetNumber_FailLogical[['DeploymentUID']] = RecordType_SetNumber_FailLogical[['DeploymentUID']].astype(str)

        ## Building QC_FailLogical_RSSummary_1
        QC_FailLogical_RSSummary   = RecordType_SetNumber_FailLogical.groupby(
            ['DeploymentUID', 'DeploymentNumber', 'SetNumber', 'RecordType'], as_index=False).DataBase_ID.count()
        QC_FailLogical_RSSummary   = pd.DataFrame(QC_FailLogical_RSSummary)
        QC_FailLogical_RSSummary.rename(columns={'DeploymentUID':'DeploymentUID',
                                                 'DeploymentNumber':'DeploymentNumber',
                                                 'SetNumber':'SetNumber',
                                                 'RecordType': 'RecordType', 
                                                 'DataBase_ID':'CountRecType1PresencePerSet'},inplace = True)
        QC_FailLogical_RSSummary = QC_FailLogical_RSSummary[(QC_FailLogical_RSSummary.RecordType == 1)&
                                            (QC_FailLogical_RSSummary.CountRecType1PresencePerSet > 1)]
        
        QC_FailLogical_RSSummary[['DeploymentNumber','SetNumber', 'RecordType']] = QC_FailLogical_RSSummary[['DeploymentNumber', 'SetNumber', 'RecordType']].replace([99999999], '')
        QC_FailLogical_RSSummary  = QC_FailLogical_RSSummary.reset_index(drop=True)
        QC_FailLogical_RSSummary  = pd.DataFrame(QC_FailLogical_RSSummary)
        
        ## Building QC_FailLogical_RSSummary_2
        QC_FailLogical_RSSummary2   = RecordType_SetNumber_FailLogical.groupby(['DeploymentUID', 'DeploymentNumber',
                                    'SetNumber'], as_index=False)['RecordType'].apply(lambda x: sum((x==1)))
        QC_FailLogical_RSSummary2.rename(columns={'DeploymentUID':'DeploymentUID',
                                                  'DeploymentNumber':'DeploymentNumber',
                                                  'SetNumber':'SetNumber',
                                                  'RecordType': 'CountRecType1PresencePerSet'
                                                },inplace = True)
        QC_FailLogical_RSSummary2 = QC_FailLogical_RSSummary2[(QC_FailLogical_RSSummary2.CountRecType1PresencePerSet == 0)]
        QC_FailLogical_RSSummary2['RecordType'] =1
        QC_FailLogical_RSSummary2 = QC_FailLogical_RSSummary2.loc[:,['DeploymentUID', 'SetNumber','DeploymentNumber',
                                                                    'RecordType','CountRecType1PresencePerSet']]
        QC_FailLogical_RSSummary2[['DeploymentNumber','SetNumber', 'RecordType']] = QC_FailLogical_RSSummary2[['DeploymentNumber','SetNumber', 'RecordType']].replace([99999999], '')
        QC_FailLogical_RSSummary2  = QC_FailLogical_RSSummary2.reset_index(drop=True)
        QC_FailLogical_RSSummary2  = pd.DataFrame(QC_FailLogical_RSSummary2)
        ## Combining
        QC_FailLogical_RSSummary = pd.concat([QC_FailLogical_RSSummary, QC_FailLogical_RSSummary2])
        QC_FailLogical_RSSummary = QC_FailLogical_RSSummary.loc[:,['DeploymentUID', 
                                                                    'CountRecType1PresencePerSet', 
                                                                    'RecordType',
                                                                    'SetNumber',
                                                                    'DeploymentNumber']]
        QC_FailLogical_RSSummary  = QC_FailLogical_RSSummary.reset_index(drop=True)
        QC_FailLogical_RSSummary  = pd.DataFrame(QC_FailLogical_RSSummary)
        return QC_FailLogical_RSSummary
    
    def GenSummaryQC():
        QC_FailLogical_RSSummary = GenSummaryQC_Backend()
        Update_RSSummary_DB(QC_FailLogical_RSSummary)

        TotalNumOfSetFail = QCFailedTotalEntries()
        TotalNumOfSetFail = int(TotalNumOfSetFail)
        NumOfSetToUpdate = int(len(QC_FailLogical_RSSummary))
        NumOfSetAlreayUpdated = TotalNumOfSetFail - NumOfSetToUpdate
        txtToUpdateEntriesCount.delete(0,END)
        txtAlreadyUpdateEntriesCount.delete(0,END)
        txtToUpdateEntriesCount.insert(tk.END,NumOfSetToUpdate)
        txtAlreadyUpdateEntriesCount.insert(tk.END,NumOfSetAlreayUpdated)

        if len(QC_FailLogical_RSSummary) >0:
            QCFailSummaryDF  = pd.DataFrame(QC_FailLogical_RSSummary)
            QCFailSummaryDF[['CountRecType1PresencePerSet']] = QCFailSummaryDF[['CountRecType1PresencePerSet']].astype(int)
            QCFailSummaryDF[['RecordType']] = QCFailSummaryDF[['RecordType']].astype(int)
            QCFailSummaryDF[['SetNumber']] = QCFailSummaryDF[['SetNumber']].astype(int)
            QCFailSummaryDF[['DeploymentNumber']] = QCFailSummaryDF[['DeploymentNumber']].astype(int)
            QCFailSummaryDF.sort_values(by=['DeploymentNumber', 'SetNumber'], inplace=True, ascending=True)
            QCFailSummaryDF  = QCFailSummaryDF.reset_index(drop=True)
            QCFailSummaryDF = pd.DataFrame(QCFailSummaryDF)
            Summaryframetree.delete(*Summaryframetree.get_children())
            countIndex1 = 0
            for each_rec in range(len(QCFailSummaryDF)):
                if countIndex1 % 2 == 0:
                    Summaryframetree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("even",))
                else:
                    Summaryframetree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            Summaryframetree.tag_configure("even",foreground="black", background="lightgreen")
            Summaryframetree.tag_configure("odd",foreground="black", background="ghost white")
            
        else:
            Summaryframetree.delete(*Summaryframetree.get_children())
            messagebox.showinfo('QC Fail Summary Message', "No Multiple Or Null RecordType1 Present")

    def populateGenSummaryQC():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
            cursor = conn.cursor()
            QC_FailLogical_RSSummary = pd.read_sql_query("SELECT * FROM Logical_RecordType_SetNumber_FailSummary;", conn)
            QC_FailLogical_RSSummary = QC_FailLogical_RSSummary.loc[:,['DeploymentUID', 
                                                                    'CountRecType1PresencePerSet', 
                                                                    'RecordType',
                                                                    'SetNumber',
                                                                    'DeploymentNumber']]
            TotalNumOfSetFail = QCFailedTotalEntries()
            TotalNumOfSetFail = int(TotalNumOfSetFail)
            NumOfSetToUpdate = int(len(QC_FailLogical_RSSummary))
            NumOfSetAlreayUpdated = TotalNumOfSetFail - NumOfSetToUpdate
            txtToUpdateEntriesCount.delete(0,END)
            txtAlreadyUpdateEntriesCount.delete(0,END)
            txtToUpdateEntriesCount.insert(tk.END,NumOfSetToUpdate)
            txtAlreadyUpdateEntriesCount.insert(tk.END,NumOfSetAlreayUpdated)           
            if len(QC_FailLogical_RSSummary) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(QC_FailLogical_RSSummary)
                SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                QCFailSummaryDF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                QCFailSummaryDF[['CountRecType1PresencePerSet']] = QCFailSummaryDF[['CountRecType1PresencePerSet']].astype(int)
                QCFailSummaryDF[['RecordType']] = QCFailSummaryDF[['RecordType']].astype(int)
                QCFailSummaryDF[['SetNumber']] = QCFailSummaryDF[['SetNumber']].astype(int)
                QCFailSummaryDF[['DeploymentNumber']] = QCFailSummaryDF[['DeploymentNumber']].astype(int)
                QCFailSummaryDF.sort_values(by=['DeploymentNumber', 'SetNumber'], inplace=True, ascending=True)
                QCFailSummaryDF  = QCFailSummaryDF.reset_index(drop=True)
                QCFailSummaryDF = pd.DataFrame(QCFailSummaryDF)
                Summaryframetree.delete(*Summaryframetree.get_children())
                countIndex1 = 0
                for each_rec in range(len(QCFailSummaryDF)):
                    if countIndex1 % 2 == 0:
                        Summaryframetree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("even",))
                    else:
                        Summaryframetree.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                Summaryframetree.tag_configure("even",foreground="black", background="lightgreen")
                Summaryframetree.tag_configure("odd",foreground="black", background="ghost white")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def InventoryRec3(event):
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber ORDER BY `DataBase_ID` ASC ;", conn)
        QCFailDF  = pd.DataFrame(Complete_df)
        nm =Summaryframetree.selection()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            NumberEntriesInSet = sd[1]
            txtDisplayMessageSystem.delete(0,END)
            txtGenSummaryDisplayMsg.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END,(("DepUID :") + SelvariableIdentifier + "-- Number Of RecType 1 /Set -- " + NumberEntriesInSet))
            tree1.delete(*tree1.get_children())
            QCFailDF_Selected = QCFailDF[(
            (QCFailDF['DeploymentUID'] == SelvariableIdentifier) 
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
            txtGenSummaryDisplayMsg.insert(tk.END,(("#Entries On Selected Set :") + str(len(QCFailDF_Selected))))        
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END, (' Please Select Only One Entries To View'))
        
        cursor.close()
        conn.close()

    def UpdateDeploymentUIDAfterUpdate():
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
        
        def GetQCFailedDB_DF():
            try:
                conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SetNumber ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    QCFailedDB_DF  = pd.DataFrame(Complete_df)

                    QCFailedDB_DF = QCFailedDB_DF.replace(np.nan, 99999999)
                    QCFailedDB_DF = QCFailedDB_DF.replace('', 99999999)
                    QCFailedDB_DF[['DataBase_ID','RecordIdentifier','RecordType',
                                'DeploymentNumber','SetNumber']] = QCFailedDB_DF[
                                ['DataBase_ID','RecordIdentifier','RecordType',
                                'DeploymentNumber','SetNumber']].astype(int)
                    QCFailedDB_DF = QCFailedDB_DF.replace(99999999, '')
                    QCFailedDB_DF['DeploymentIdentifier'] = QCFailedDB_DF["DeploymentUID"].str[0:10] + "-" + \
                                                                      QCFailedDB_DF["DeploymentNumber"].map(str)+"-"+ \
                                                                      QCFailedDB_DF["SetNumber"].map(str)
                    QCFailedDB_DF = QCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                                         'DeploymentIdentifier','RecordType',\
                                                         'DeploymentNumber', 'SetNumber', \
                                                         'QCRecordType_SetNumber']]
                    QCFailedDB_DF.rename(columns={'DataBase_ID':'DataBase_ID', 
                                                'RecordIdentifier':'RecordIdentifier',
                                                'DeploymentIdentifier':'DeploymentUID',     
                                                'RecordType':'RecordType',
                                                'DeploymentNumber':'DeploymentNumber',     
                                                'SetNumber':'SetNumber',
                                                'QCRecordType_SetNumber':'QCRecordType_SetNumber',
                                                },inplace = True)
                    QCFailedDB_DF  = QCFailedDB_DF.reset_index(drop=True)
                    QCFailedDB_DF  = pd.DataFrame(QCFailedDB_DF)
                    return QCFailedDB_DF
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

         ## Get RecordType_SetNumber Profile
        QCFailedDB_DF_Get = GetQCFailedDB_DF()
        UpdatedQCFailed =[]
        df_rows = QCFailedDB_DF_Get.to_numpy().tolist()
        for row in df_rows:
            rowValue = row
            list_item_DataBase_ID = int(rowValue[0])
            list_item_RecordIdentifier = int(rowValue[1])
            list_item_DeploymentUID = (rowValue[2])
            list_item_RecordType = (rowValue[3])
            list_item_DeploymentNumber = (rowValue[4])
            list_item_SetNumber = (rowValue[5])
            list_item_QCRecordType_SetNumber = (rowValue[6])
            
            UpdatedQCFailed.append((
                    list_item_DeploymentUID,
                    list_item_RecordType,
                    list_item_DeploymentNumber,
                    list_item_SetNumber,
                    list_item_QCRecordType_SetNumber,
                    list_item_DataBase_ID,
                    list_item_RecordIdentifier,
                    ))
        ## DB Update Executing
        conn_DB_SetCatch_Validation_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur_DB_SetCatch_Validation_Logical=conn_DB_SetCatch_Validation_Logical.cursor()
        cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET DeploymentUID =?, RecordType = ?, \
                                                    DeploymentNumber = ?, SetNumber = ?,\
                                                    QCRecordType_SetNumber = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdatedQCFailed)
        conn_DB_SetCatch_Validation_Logical.commit()
        conn_DB_SetCatch_Validation_Logical.close()
        txtDisplayMessageSystem.delete(0,END)
        txtDisplayMessageSystem.insert(tk.END,'Finished Update')
        tkinter.messagebox.showinfo("Update Message","Update Successfully")   
   
    def Update_RSSummary_DB(QC_FailLogical_RSSummary):
        try:
            QC_FailLogical_RSSummary = QC_FailLogical_RSSummary.loc[:,
                                        ['DeploymentUID', 
                                         'DeploymentNumber', 
                                         'SetNumber',
                                         'RecordType',
                                         'CountRecType1PresencePerSet']]
            QC_FailLogical_RSSummary  = QC_FailLogical_RSSummary.reset_index(drop=True)
            QC_FailLogical_RSSummary  = pd.DataFrame(QC_FailLogical_RSSummary)

            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Logical)
            cursor = sqliteConnection.cursor()
            QC_FailLogical_RSSummary.to_sql('Logical_RecordType_SetNumber_FailSummary',
                                        sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def DeleteSelectedEntries():
        SelectionTree = tree1.selection()
        if len(SelectionTree)>0:
            iDelete = tkinter.messagebox.askyesno("Delete Entry From DFO-NL-ASOP Set & Catch QC Database", 
                            "Confirm If You Want To Delete The Selection Entries From DFO-NL-ASOP Set & Catch QC Database")
            if iDelete >0:
                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

                conn_Validation_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
                cur_Validation_Logical=conn_Validation_Logical.cursor()
                UpdateCase_QCFailDB =[]  
                for selected_item in tree1.selection():
                    list_item = (tree1.item(selected_item, 'values'))
                    list_item_DeploymentUID = (list_item[2])
                    list_item_QC_CaseType = 'Case: Updated'
                    UpdateCase_QCFailDB.append((list_item_QC_CaseType, 
                                                    list_item_DeploymentUID))
                    cur_DB_Set_Catch_Analysis.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DataBase_ID =? \
                                AND RecordIdentifier =? AND DeploymentUID = ? ",(tree1.set(selected_item, '#1'), \
                                tree1.set(selected_item, '#2'),tree1.set(selected_item, '#3'),))
                    cur_Validation_Logical.execute("DELETE FROM SetCatch_QCFailedLogical_RecordType_SetNumber WHERE DataBase_ID =? \
                                AND RecordIdentifier =? AND DeploymentUID = ? ",(tree1.set(selected_item, '#1'), \
                                tree1.set(selected_item, '#2'),tree1.set(selected_item, '#3'),))
                    conn_DB_Set_Catch_Analysis.commit()
                    conn_Validation_Logical.commit()
                    tree1.delete(selected_item)
                
                cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SetNumber SET QC_CaseType = ?\
                                                 WHERE DeploymentUID =?", 
                                                UpdateCase_QCFailDB)
                
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
                conn_Validation_Logical.commit()
                conn_Validation_Logical.close()
                entry_ViewVarResults.current(1)
                viewQCFailed_VariablesProfile()
                return
        else:
            tkinter.messagebox.showinfo("Delete Error","Please Select Entries From Table")

    def SearchDepNumFromSetCatchDB():
        ListFilterBy = ['Both RecType 1&2', 
                        'RecType-1 Only']
        get_TabAQCview = (entry_FilterByList.get())
        if (len(get_TabAQCview)) > 0:
            try:
                get_DepNumforSearch = int(entry_DepNumforSearch.get())
            except:
                messagebox.showerror('Search Variable Datatype Error Message', "Search Value Must Be Integer Value")
            checkinttype = isinstance(get_DepNumforSearch,int)
            if checkinttype == True:  
                conn_DB= sqlite3.connect(DB_Set_Catch_Analysis)
                if (get_DepNumforSearch) >= 0:
                    if (get_TabAQCview == ListFilterBy[0]):           
                        get_SearchSingleVariable_Value = (get_DepNumforSearch)
                        rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                        rows = rows[(rows.DeploymentNumber) == get_SearchSingleVariable_Value]
                        rows  = rows.reset_index(drop=True)
                        QCFail_DF  = pd.DataFrame(rows)
                        ExcelViewEditBackend(QCFail_DF)
                    
                    if (get_TabAQCview == ListFilterBy[1]):           
                        get_SearchSingleVariable_Value = (get_DepNumforSearch)
                        rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                        rows = rows[((rows.DeploymentNumber) == get_SearchSingleVariable_Value)&\
                                    ((rows.RecordType) == 1)]
                        rows  = rows.reset_index(drop=True)
                        QCFail_DF  = pd.DataFrame(rows)
                        ExcelViewEditBackend(QCFail_DF)
                conn_DB.commit()
                conn_DB.close()    
    
    def ExcelViewEditBackend(QCFail_DF):
        Ref_FailedQC_InSetcatchDB  = pd.DataFrame(QCFail_DF)
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

    ## Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    ## ComboBox
    entry_UpdateVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable1)
    entry_SearchVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable2)
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ## Populate QC Summary
    populateGenSummaryQC()
    QCFailedTotalEntries()

    # ## Button Wizard :
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
    button_UpdateSelectedDBEntries.grid(row =14, column = 0, padx=10, pady =1, ipady =4, sticky =W)

    button_Clear_EntriesUpdate = Button(UpdateDB_Entryframe, bd = 2, text ="Clear", width = 5,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearEntries)
    button_Clear_EntriesUpdate.grid(row =8, column = 0, padx=2, pady =2, ipady =1, sticky =E)

    button_Delete_EntriesUpdate = Button(UpdateDB_Entryframe, bd = 2, text ="Delete", width = 5,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =DeleteSelectedEntries)
    button_Delete_EntriesUpdate.grid(row =6, column = 0, padx=2, pady =2, ipady =1, sticky =E)


    ## Buttons On Search Frame
    button_SearchSingleVariableQuery = Button(SearchDB_Entryframe, bd = 2, text ="Run Single Variable Search ", width = 26,
                                height=2, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunSingleVariableSearchQuery)
    button_SearchSingleVariableQuery.grid(row =14, column = 0, padx=10, pady =3, ipady =3, sticky =W)

    # Buttons On Generate QC Failed Summary Frame
    button_GenSummaryQC = Button(GenSummaryQCframe, bd = 2, text ="Generate QC Fail Summary ", width = 26,
                                height=1, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSummaryQC)
    button_GenSummaryQC.pack(side =TOP, padx=10, pady =3, ipady =3)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    importexport = Menu(menu, tearoff=0)
    view = Menu(menu, tearoff=0)
    Update  = Menu(menu, tearoff=0)

    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Import/Export", menu=importexport)
    menu.add_cascade(label="View", menu=view)
    menu.add_cascade(label="Update", menu=Update)
   
    filemenu.add_command(label="Exit", command=iExit)
    importexport.add_command(label="Export Failed Results (.csv)", command=Export_LogicalFailed_RT_SN_CSV)
    importexport.add_command(label="Import & Update DB (.csv)", command=ImportAndUpdateSetCatchDB)
    view.add_command(label="Ref All Results In Set&Catch DB", command=RefFailedToSetcatchDB)
    Update.add_command(label="Update DeplymentUID", command=UpdateDeploymentUIDAfterUpdate)
   
    Treepopup.add_command(label="Delete Seleted Entries", command=DeleteSelectedEntries)
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack()
    window.mainloop()


