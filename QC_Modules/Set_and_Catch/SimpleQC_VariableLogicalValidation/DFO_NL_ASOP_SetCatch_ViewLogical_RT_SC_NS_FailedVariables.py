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

def ViewLogical_RT_NS_SpCode_ValidatedResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Logical Validator - ID-C-04-3")
    window.geometry("1250x800+200+100")
    window.config(bg="cadet blue")

    ## Top Frame
    Topframe = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Topframe.pack(side = TOP)


    txtDisplayMessageSystem = Listbox(Topframe, font=('aerial', 9, 'bold'), 
                                      height =3, width =80)
    txtDisplayMessageSystem.grid(row =0, column = 0, padx=200, pady =5, ipady =5, sticky =E)

    lbl_QCDisplay = Label(Topframe, font=('aerial', 10, 'bold'), text="A: QCFailed Display Table:")
    lbl_QCDisplay.grid(row =0, column = 0, padx=2, pady =1, sticky =W)

    lbl_TotalFailedEntries = Label(Topframe, font=('aerial', 10 , 'bold'), bg= "cadet blue", text="# Of Set Failed :")
    lbl_TotalFailedEntries.grid(row =2, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(Topframe, value='')
    txtTotalFailedEntries = Entry(Topframe, font=('aerial',10),textvariable = TotalFailedEntries, width = 5, bd=1)
    txtTotalFailedEntries.grid(row =2, column = 0, padx=115, pady =1, ipady =1, sticky =W)

    lbl_SelectedCaseTypeEntries = Label(Topframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" QC Fail On Selected CaseType")
    lbl_SelectedCaseTypeEntries.grid(row =2, column = 0, padx=60, pady =1, sticky =E)
    SelectedCaseTypeEntries       = IntVar(Topframe, value ='')
    entry_SelectedCaseTypeEntries = Entry(Topframe, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = SelectedCaseTypeEntries, width = 6, bd=1)
    entry_SelectedCaseTypeEntries.grid(row =2, column = 0, padx=2, pady =1, ipady =1, sticky =E)
    
    ## Table Frame Define
    Tableframe = tk.Frame(window, width = 40)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    
    ## SelectViewResultsRun Frame Wizard :
    SelectViewResultsRun = Frame(Tableframe, width = 80)
    SelectViewResultsRun.pack(side = TOP, padx= 0, pady=0)
    ListVariableListA = ['Select Logical Variable Pair From DropDown & Run View Selected Button', 
                         'Case-A SpeciesCode - RecType1 @ Each Set',
                         'Case-B SpeciesCode - RecType2 - NumberSpecies @ Each Set']
    VariableList        = StringVar(SelectViewResultsRun, value ='')
    entry_ViewVarResults  = ttk.Combobox(SelectViewResultsRun, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable = VariableList, width = 80, state='readonly')
    entry_ViewVarResults.grid(row =0, column = 0, padx=2, pady =4, ipady= 4, sticky =E)
    entry_ViewVarResults['values'] = ListVariableListA
    entry_ViewVarResults.current(0)

    EntryDepNum       = IntVar(SelectViewResultsRun, value ='Enter DeploymentNumber')
    entry_DepNumforSearch = Entry(SelectViewResultsRun, font=('aerial', 10), justify='center',
                                textvariable = EntryDepNum, width = 25, bd=2)
    entry_DepNumforSearch.grid(row =0, column = 4, padx=150, pady =2, ipady =2, sticky =W)

    txtQCVariableView = Entry(SelectViewResultsRun, font=('aerial', 9),
                            textvariable = StringVar(window, value='QC Variable'), width = 25, bd=2)
    txtQCVariableView.grid(row =1, column = 0, padx=200, pady =2, ipady =5, sticky =W)

    txtRelatedQCVariableView = Entry(SelectViewResultsRun, font=('aerial', 9),
                            textvariable = StringVar(window, value='Related QC Variable'), width = 25, bd=2)
    txtRelatedQCVariableView.grid(row =1, column = 0, padx=2, pady =2, ipady =5, sticky =E)

    ## Tree1 Define
    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", 
                    "column4", "column5", "column6", 
                    "column7", "column8", "column9"), height=15, show='headings')
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
    tree1.heading("#8", text="SpeciesCode", anchor=CENTER)
    tree1.heading("#9", text="QCCaseType", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)            
    tree1.column('#9', stretch=NO, minwidth=0, width=190, anchor = tk.CENTER)
    style = ttk.Style(Tableframe)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 8), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)

    # Frame Of Update modules
    UpdateDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    UpdateDB_Entryframe.pack(side =LEFT, padx=2, pady =2)

    lbl_UpdateDB_Header = Label(UpdateDB_Entryframe, font=('aerial', 11, 'bold','underline'),
                                bg= "cadet blue", text="Update Database ")
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
    lbl_Select_List_Variable.grid(row =6, column = 0, padx=10, pady =2, sticky =W)
    
    ListVariableListA = ['DeploymentNumber','SetNumber','RecordType',
                         'NumberSpecies', 'SpeciesCode']
    VariableListA        = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = VariableListA, width = 24, state='readonly')
    entry_UpdateVariableList.grid(row =8, column = 0, padx=50, pady =2, ipady= 2, sticky =W)
    entry_UpdateVariableList['values'] = sorted(list(ListVariableListA))

    lbl_EntryUpdate_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 3. Enter Updated Value :")
    lbl_EntryUpdate_Variable.grid(row =10, column = 0, padx=10, pady =2, sticky =W)
    
    UpdateValue_VariableA       = IntVar(UpdateDB_Entryframe, value ='')
    entry_UpdateValue_VariableA = Entry(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = UpdateValue_VariableA, width = 25, bd=2)
    entry_UpdateValue_VariableA.grid(row =12, column = 0, padx=50, pady =2, ipady =2, sticky =W)

## ######### Frame Generate QC Failed Summary ############
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

    SelResultOverviewtree = ttk.Treeview(SelResultOverview,  
                                         column=("column1", "column2", "column3", "column4", "column5"),
                                         height=8, show='headings')
    scrollbary = ttk.Scrollbar(SelResultOverview, orient ="vertical", command=SelResultOverviewtree.yview)
    scrollbary.pack(side ='right', fill ='y')
    SelResultOverviewtree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(SelResultOverview, orient ="horizontal", command=SelResultOverviewtree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    SelResultOverviewtree.configure(xscrollcommand = scrollbarx.set)
    SelResultOverviewtree.heading("#1", text="DeploymentUID", anchor=CENTER)
    SelResultOverviewtree.heading("#2", text="QCCaseType", anchor=CENTER)
    SelResultOverviewtree.heading("#3", text="TotalRecords", anchor=CENTER)
    SelResultOverviewtree.heading("#4", text="#SpecesCode/SetN", anchor=CENTER)
    SelResultOverviewtree.heading("#5", text="MeanNumSpeces", anchor=CENTER)
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)             
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    SelResultOverviewtree.column('#4', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)
    SelResultOverviewtree.column('#5', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = BOTTOM)

## ####All Defined Functions ########
    
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber','RecordType',
                            'NumberSpecies', 'SpeciesCode']
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
                    List_Columns_Import = List_Columns_Import[:-2]
                    Return_Message = ImportColumnCheck(List_Columns_Import)
                    if Return_Message == ReturnMatchedMessage:
                        df = df.iloc[:,:]
                        DataBase_ID = (df.loc[:,'DataBase_ID']).fillna(99999999).astype(int)
                        RecordIdentifier = (df.loc[:,'RecordIdentifier']).fillna(99999999).astype(int)
                        DeploymentUID = (df.loc[:,'DeploymentUID']).fillna(8888888).astype(str)
                        DeploymentNumber = (df.loc[:,'DeploymentNumber']).fillna(99999999).astype(int, errors='ignore')
                        SetNumber = (df.loc[:,'SetNumber']).fillna(99999999).astype(str, errors='ignore')
                        RecordType = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        NumberSpecies = (df.loc[:,'NumberSpecies']).fillna(99999999).astype(int, errors='ignore')
                        SpeciesCode = (df.loc[:,'SpeciesCode']).fillna(99999999).astype(int, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID, \
                                        DeploymentNumber, SetNumber, \
                                        RecordType, NumberSpecies, \
                                        SpeciesCode]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns=  {0:'DataBase_ID', 1: 'RecordIdentifier', 2: 'DeploymentUID',
                                                3:'DeploymentNumber', 4:'SetNumber', 5:'RecordType', 
                                                6:'NumberSpecies', 7:'SpeciesCode'},inplace = True)
                        Raw_Imported_Df = pd.DataFrame(catdf)
                        Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0, '.', 'Null'], '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([8888888, '8888888', '.','Null'], 'None')
                        Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                        Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                        CheckEmptyNessColumn = Raw_Imported_Df[
                                            (Raw_Imported_Df.DataBase_ID =='') |
                                            (Raw_Imported_Df.RecordIdentifier =='') |
                                            (Raw_Imported_Df.DeploymentUID =='None') |
                                            (Raw_Imported_Df.DeploymentUID =='') |
                                            (Raw_Imported_Df.RecordType =='') |
                                            (Raw_Imported_Df.DeploymentNumber =='') |
                                            (Raw_Imported_Df.SetNumber =='')
                                            ]
                    Len_CheckEmptyNessColumn =len(CheckEmptyNessColumn)
                    if Len_CheckEmptyNessColumn==0:
                        Length_Raw_Imported_Df  =  len(Raw_Imported_Df)
                        if Length_Raw_Imported_Df <250000:
                            UpdateRecordList_SetCatchDB =[]
                            Update_RT_SC_Failed =[]
                            Update_NS_SC_Failed =[]
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
                                list_item_SpeciesCode = (rowValue[7])
                                list_item_QCCaseType = ''
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_RecordType,
                                                    list_item_NumberSpecies,
                                                    list_item_SpeciesCode,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                Update_RT_SC_Failed.append((
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_RecordType,
                                                    list_item_NumberSpecies,
                                                    list_item_SpeciesCode,
                                                    list_item_QCCaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                Update_NS_SC_Failed.append((
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_RecordType,
                                                    list_item_NumberSpecies,
                                                    list_item_SpeciesCode,
                                                    list_item_QCCaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                                 
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ?, \
                                                    SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                                    SpeciesCode = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                            
                            cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET DeploymentNumber = ?, \
                                                    SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                                    SpeciesCode = ?, QCCaseType = ? \
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    Update_RT_SC_Failed)
                            
                            cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET DeploymentNumber = ?, \
                                                    SetNumber = ?, RecordType = ?, NumberSpecies = ? , \
                                                    SpeciesCode = ?, QCCaseType = ? \
                                                    WHERE DataBase_ID = ? AND RecordIdentifier = ? AND DeploymentUID = ?", 
                                                    Update_NS_SC_Failed)
                            
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Logical.commit()
                            conn_DB_SetCatch_Validation_Logical.close()
                            viewQCFailed_VariablesProfile()
                            txtDisplayMessageSystem.delete(0,END)
                            txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                    else:
                        messagebox.showerror('Empty Variables', "Please Check Null Variables (DataBase_ID, RecordIdentifier, DeploymentUID,\
                                              DeploymentNumber, SetNumber, RecordType) Input")

    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def ClearTablesAll():
        tree1.delete(*tree1.get_children())
        txtTotalFailedEntries.delete(0,END)
        entry_SelectedCaseTypeEntries.delete(0,END)
        txtQCVariableView.delete(0,END)
        txtRelatedQCVariableView.delete(0,END)
        txtDisplayMessageSystem.delete(0,END)
        
    def ClearEntries():
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateValue_VariableA.delete(0,END)
        entry_NumberRowSelected.delete(0,END)
    
    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select Logical Variable Pair From DropDown & Run View Selected Button', 
                         'Case-A SpeciesCode - RecType1 @ Each Set',
                         'Case-B SpeciesCode - RecType2 - NumberSpecies @ Each Set']
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Logical)
            cur=con.cursor()
            if getVarnameToView == ListVariableListA[1]:
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SpeciesCode ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == ListVariableListA[2]:
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode ORDER BY `DataBase_ID` ASC")
            rows=cur.fetchall()
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_VariablesProfile():
        ListVariableListA = ['Select Logical Variable Pair From DropDown & Run View Selected Button', 
                         'Case-A SpeciesCode - RecType1 @ Each Set',
                         'Case-B SpeciesCode - RecType2 - NumberSpecies @ Each Set']
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        entry_SelectedCaseTypeEntries.delete(0,END)
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 
                             2:'DeploymentUID', 3:'DeploymentNumber',
                             4:'SetNumber', 5:'RecordType', 
                             6:'NumberSpecies', 7:'SpeciesCode', 
                             8:'QCCaseType'},inplace = True)
        if len(rows) >0 :
            if getVarnameToView == ListVariableListA[0]:
                txtDisplayMessageSystem.insert(1, 'Select Logical Variable Pair From DropDown & Run View Selected Button')
                txtDisplayMessageSystem.insert(2, '& Run View Selected Button')

            if getVarnameToView == ListVariableListA[1]:
                rows.sort_values(by=['DeploymentUID','DeploymentNumber',
                    'SetNumber','RecordType'], inplace=True)
                rows  = rows.reset_index(drop=True)
                rows  = pd.DataFrame(rows)
                CaseATotalFail = rows.DeploymentUID.unique().size
                entry_SelectedCaseTypeEntries.insert(tk.END,CaseATotalFail)
                
            if getVarnameToView == ListVariableListA[2]:
                rows.sort_values(by=['DeploymentUID','DeploymentNumber',
                    'SetNumber','RecordType'], inplace=True)
                rows  = rows.reset_index(drop=True)
                rows  = pd.DataFrame(rows)
                CaseATotalFail = rows.DeploymentUID.unique().size
                entry_SelectedCaseTypeEntries.insert(tk.END,CaseATotalFail)
                
            countIndex1 = 0
            for each_rec in range(len(rows)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightgreen")
            tree1.tag_configure("odd",foreground="black", background="ghost white")
        
    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM Logical_RecType_SpecsCode_NumbSpecs_FailSummary;", conn)
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
 
    def QCFailedExcelViewAll():
        ## Definging getQCFailedDB from DB
        def getQCFailedDB():
            try:
                conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
                cursor = conn.cursor()
                RType_SPCode_df = pd.read_sql_query("SELECT * FROM \
                SetCatch_QCFailedLogical_RecordType_SpeciesCode ORDER BY `DataBase_ID` ASC ;", conn)
                NumSpeces_Speccode_df = pd.read_sql_query("SELECT * FROM \
                SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode ORDER BY `DataBase_ID` ASC ;", conn)
                ## For RType_SPCode_df
                RType_SPCode_df = pd.DataFrame(RType_SPCode_df)
                RType_SPCode_df['DataBase_ID'] = (RType_SPCode_df.loc[:,['DataBase_ID']]).astype(int)
                RType_SPCode_df['RecordIdentifier'] = (RType_SPCode_df.loc[:,['RecordIdentifier']]).astype(int)
                RType_SPCode_df['DeploymentUID'] = (RType_SPCode_df.loc[:,['DeploymentUID']]).astype(str)

                RType_SPCode_df['DeploymentNumber'] = (RType_SPCode_df.loc[:,['DeploymentNumber']]).fillna(99999999)
                RType_SPCode_df['DeploymentNumber'] = (RType_SPCode_df.loc[:,['DeploymentNumber']]).replace([''], 99999999)
                RType_SPCode_df['DeploymentNumber'] = (RType_SPCode_df.loc[:,['DeploymentNumber']]).astype(int)
                
                RType_SPCode_df['SetNumber'] = (RType_SPCode_df.loc[:,['SetNumber']]).fillna(99999999)
                RType_SPCode_df['SetNumber'] = (RType_SPCode_df.loc[:,['SetNumber']]).replace([''], 99999999)
                RType_SPCode_df['SetNumber'] = (RType_SPCode_df.loc[:,['SetNumber']]).astype(int)
                
                RType_SPCode_df['RecordType'] = (RType_SPCode_df.loc[:,['RecordType']]).fillna(99999999)
                RType_SPCode_df['RecordType'] = (RType_SPCode_df.loc[:,['RecordType']]).replace([''], 99999999)
                RType_SPCode_df['RecordType'] = (RType_SPCode_df.loc[:,['RecordType']]).astype(int)
                
                RType_SPCode_df['NumberSpecies'] = (RType_SPCode_df.loc[:,['NumberSpecies']]).fillna(99999999)
                RType_SPCode_df['NumberSpecies'] = (RType_SPCode_df.loc[:,['NumberSpecies']]).replace([''], 99999999)
                RType_SPCode_df['NumberSpecies'] = (RType_SPCode_df.loc[:,['NumberSpecies']]).astype(int)

                RType_SPCode_df['SpeciesCode'] = (RType_SPCode_df.loc[:,['SpeciesCode']]).fillna(99999999)
                RType_SPCode_df['SpeciesCode'] = (RType_SPCode_df.loc[:,['SpeciesCode']]).replace([''], 99999999)
                RType_SPCode_df['SpeciesCode'] = (RType_SPCode_df.loc[:,['SpeciesCode']]).astype(int)
                RType_SPCode_df = RType_SPCode_df.reset_index(drop=True)
                RType_SPCode_df = pd.DataFrame(RType_SPCode_df)
                ## For NumSpeces_Speccode_df
                NumSpeces_Speccode_df = pd.DataFrame(NumSpeces_Speccode_df)
                NumSpeces_Speccode_df['DataBase_ID'] = (NumSpeces_Speccode_df.loc[:,['DataBase_ID']]).astype(int)
                NumSpeces_Speccode_df['RecordIdentifier'] = (NumSpeces_Speccode_df.loc[:,['RecordIdentifier']]).astype(int)
                NumSpeces_Speccode_df['DeploymentUID'] = (NumSpeces_Speccode_df.loc[:,['DeploymentUID']]).astype(str)

                NumSpeces_Speccode_df['DeploymentNumber'] = (NumSpeces_Speccode_df.loc[:,['DeploymentNumber']]).fillna(99999999)
                NumSpeces_Speccode_df['DeploymentNumber'] = (NumSpeces_Speccode_df.loc[:,['DeploymentNumber']]).replace([''], 99999999)
                NumSpeces_Speccode_df['DeploymentNumber'] = (NumSpeces_Speccode_df.loc[:,['DeploymentNumber']]).astype(int)
                
                NumSpeces_Speccode_df['SetNumber'] = (NumSpeces_Speccode_df.loc[:,['SetNumber']]).fillna(99999999)
                NumSpeces_Speccode_df['SetNumber'] = (NumSpeces_Speccode_df.loc[:,['SetNumber']]).replace([''], 99999999)
                NumSpeces_Speccode_df['SetNumber'] = (NumSpeces_Speccode_df.loc[:,['SetNumber']]).astype(int)
                
                NumSpeces_Speccode_df['RecordType'] = (NumSpeces_Speccode_df.loc[:,['RecordType']]).fillna(99999999)
                NumSpeces_Speccode_df['RecordType'] = (NumSpeces_Speccode_df.loc[:,['RecordType']]).replace([''], 99999999)
                NumSpeces_Speccode_df['RecordType'] = (NumSpeces_Speccode_df.loc[:,['RecordType']]).astype(int)
                
                NumSpeces_Speccode_df['NumberSpecies'] = (NumSpeces_Speccode_df.loc[:,['NumberSpecies']]).fillna(99999999)
                NumSpeces_Speccode_df['NumberSpecies'] = (NumSpeces_Speccode_df.loc[:,['NumberSpecies']]).replace([''], 99999999)
                NumSpeces_Speccode_df['NumberSpecies'] = (NumSpeces_Speccode_df.loc[:,['NumberSpecies']]).astype(int)

                NumSpeces_Speccode_df['SpeciesCode'] = (NumSpeces_Speccode_df.loc[:,['SpeciesCode']]).fillna(99999999)
                NumSpeces_Speccode_df['SpeciesCode'] = (NumSpeces_Speccode_df.loc[:,['SpeciesCode']]).replace([''], 99999999)
                NumSpeces_Speccode_df['SpeciesCode'] = (NumSpeces_Speccode_df.loc[:,['SpeciesCode']]).astype(int)
                NumSpeces_Speccode_df = NumSpeces_Speccode_df.reset_index(drop=True)
                NumSpeces_Speccode_df = pd.DataFrame(NumSpeces_Speccode_df)
                
                ## Merging RType_SPCode_df, NumSpeces_Speccode_df
                SetCatchQCFailedDB_DF = pd.merge(RType_SPCode_df, NumSpeces_Speccode_df, 
                                        how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID',
                                                           'DeploymentNumber','SetNumber','RecordType',
                                                           'NumberSpecies', 'SpeciesCode'])
                SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int)
                SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int)
                SetCatchQCFailedDB_DF['DeploymentUID'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentUID']]).astype(str)

                SetCatchQCFailedDB_DF['DeploymentNumber'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
                SetCatchQCFailedDB_DF['DeploymentNumber'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
                SetCatchQCFailedDB_DF['DeploymentNumber'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentNumber']]).astype(int)
                
                SetCatchQCFailedDB_DF['SetNumber'] = (SetCatchQCFailedDB_DF.loc[:,['SetNumber']]).fillna(99999999)
                SetCatchQCFailedDB_DF['SetNumber'] = (SetCatchQCFailedDB_DF.loc[:,['SetNumber']]).replace([''], 99999999)
                SetCatchQCFailedDB_DF['SetNumber'] = (SetCatchQCFailedDB_DF.loc[:,['SetNumber']]).astype(int)
                
                SetCatchQCFailedDB_DF['RecordType'] = (SetCatchQCFailedDB_DF.loc[:,['RecordType']]).fillna(99999999)
                SetCatchQCFailedDB_DF['RecordType'] = (SetCatchQCFailedDB_DF.loc[:,['RecordType']]).replace([''], 99999999)
                SetCatchQCFailedDB_DF['RecordType'] = (SetCatchQCFailedDB_DF.loc[:,['RecordType']]).astype(int)
                
                SetCatchQCFailedDB_DF['NumberSpecies'] = (SetCatchQCFailedDB_DF.loc[:,['NumberSpecies']]).fillna(99999999)
                SetCatchQCFailedDB_DF['NumberSpecies'] = (SetCatchQCFailedDB_DF.loc[:,['NumberSpecies']]).replace([''], 99999999)
                SetCatchQCFailedDB_DF['NumberSpecies'] = (SetCatchQCFailedDB_DF.loc[:,['NumberSpecies']]).astype(int)

                SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).fillna(99999999)
                SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).replace([''], 99999999)
                SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).astype(int)

                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(np.nan, '')
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace([99999999, 99999999.0, '.', 'Null'], '')
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace([8888888, '8888888', '.','Null'], 'None')
               
                if len(SetCatchQCFailedDB_DF) >0:
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                         'DeploymentNumber','SetNumber','RecordType',
                                         'NumberSpecies', 'SpeciesCode',
                                         'QCCaseType_x', 'QCCaseType_y']]
                    SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int)
                    SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int)
                    SetCatchQCFailedDB_DF['DeploymentUID'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentUID']]).astype(str)
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    return SetCatchQCFailedDB_DF
                else:
                    return SetCatchQCFailedDB_DF
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        ## Getting getQCFailedDB
        QCFailedExcelViewDB  = getQCFailedDB()
        if len(QCFailedExcelViewDB) >0:
            QC_FailLogical_DF = pd.DataFrame(QCFailedExcelViewDB)
            ExcelViewEditBackend_RecType_1_2(QC_FailLogical_DF)
                       
    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def Export_FailedLogicalVariablesCSV():
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF['DataBase_ID'] = (SetCatchProfileDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['RecordIdentifier'] = (SetCatchProfileDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        SetCatchQCFailedDB_DF = GetSetCatchQCFailedDB()
        SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        Exp_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                                    SetCatchQCFailedDB_DF,
                                    on = ["DataBase_ID", 
                                          "RecordIdentifier", 
                                          "DeploymentUID"
                                         ], 
                                    indicator=True, 
                                    how='outer').query('_merge == "both"')
        Exp_FailedQC_InSetcatchDB  = Exp_FailedQC_InSetcatchDB.iloc[:,
                                    0:len(list(SetCatchProfileDB_DF.columns))+2]

        Exp_FailedQC_InSetcatchDB['DataBase_ID'] = (Exp_FailedQC_InSetcatchDB.loc[:,
                                 ['DataBase_ID']]).astype(int, errors='ignore')
        Exp_FailedQC_InSetcatchDB['RecordIdentifier'] = (Exp_FailedQC_InSetcatchDB.loc[:,
                                 ['RecordIdentifier']]).astype(int, errors='ignore')

        Exp_FailedQC_InSetcatchDB  = Exp_FailedQC_InSetcatchDB.reset_index(drop=True)
        Complete_df  = pd.DataFrame(Exp_FailedQC_InSetcatchDB)
        
        Complete_df = Complete_df.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'DeploymentNumber','SetNumber','RecordType',
                                        'NumberSpecies', 'SpeciesCode',
                                        'QCCaseType_x','QCCaseType_y']]
        Complete_df.sort_values(by=['DeploymentNumber','SetNumber','RecordType'], inplace=True)
        if len(Complete_df) >0:
            Export_MasterTB_DF  = pd.DataFrame(Complete_df)
            Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
            filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                    defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
            if len(filename) >0:
                Export_MasterTB_DF.to_csv(filename,index=None)
                tkinter.messagebox.showinfo("QC Failed Logical Profile","QC Failed Logical Profile Report Saved as CSV")
            else:
                tkinter.messagebox.showinfo("QC Failed Logical Profile Report Message","Please Select File Name To Export")
        else:
            messagebox.showerror('Export Error', "Void File... Nothing to Export")

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
            RType_SPCode_df = pd.read_sql_query("SELECT * FROM \
            SetCatch_QCFailedLogical_RecordType_SpeciesCode ORDER BY `DataBase_ID` ASC ;", conn)
            NumSpeces_Speccode_df = pd.read_sql_query("SELECT * FROM \
            SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode ORDER BY `DataBase_ID` ASC ;", conn)
            RType_SPCode_df = pd.DataFrame(RType_SPCode_df)
            RType_SPCode_df['DataBase_ID'] = (RType_SPCode_df.loc[:,['DataBase_ID']]).astype(int)
            RType_SPCode_df['RecordIdentifier'] = (RType_SPCode_df.loc[:,['RecordIdentifier']]).astype(int)
            RType_SPCode_df['DeploymentUID'] = (RType_SPCode_df.loc[:,['DeploymentUID']]).astype(str)

            RType_SPCode_df['DeploymentNumber'] = (RType_SPCode_df.loc[:,['DeploymentNumber']]).fillna(99999999)
            RType_SPCode_df['DeploymentNumber'] = (RType_SPCode_df.loc[:,['DeploymentNumber']]).replace([''], 99999999)
            RType_SPCode_df['DeploymentNumber'] = (RType_SPCode_df.loc[:,['DeploymentNumber']]).astype(int)
            
            RType_SPCode_df['SetNumber'] = (RType_SPCode_df.loc[:,['SetNumber']]).fillna(99999999)
            RType_SPCode_df['SetNumber'] = (RType_SPCode_df.loc[:,['SetNumber']]).replace([''], 99999999)
            RType_SPCode_df['SetNumber'] = (RType_SPCode_df.loc[:,['SetNumber']]).astype(int)
            
            RType_SPCode_df['RecordType'] = (RType_SPCode_df.loc[:,['RecordType']]).fillna(99999999)
            RType_SPCode_df['RecordType'] = (RType_SPCode_df.loc[:,['RecordType']]).replace([''], 99999999)
            RType_SPCode_df['RecordType'] = (RType_SPCode_df.loc[:,['RecordType']]).astype(int)
            
            RType_SPCode_df['NumberSpecies'] = (RType_SPCode_df.loc[:,['NumberSpecies']]).fillna(99999999)
            RType_SPCode_df['NumberSpecies'] = (RType_SPCode_df.loc[:,['NumberSpecies']]).replace([''], 99999999)
            RType_SPCode_df['NumberSpecies'] = (RType_SPCode_df.loc[:,['NumberSpecies']]).astype(int)

            RType_SPCode_df['SpeciesCode'] = (RType_SPCode_df.loc[:,['SpeciesCode']]).fillna(99999999)
            RType_SPCode_df['SpeciesCode'] = (RType_SPCode_df.loc[:,['SpeciesCode']]).replace([''], 99999999)
            RType_SPCode_df['SpeciesCode'] = (RType_SPCode_df.loc[:,['SpeciesCode']]).astype(int)
            RType_SPCode_df = RType_SPCode_df.reset_index(drop=True)
            RType_SPCode_df = pd.DataFrame(RType_SPCode_df)
            
            NumSpeces_Speccode_df = pd.DataFrame(NumSpeces_Speccode_df)
            NumSpeces_Speccode_df['DataBase_ID'] = (NumSpeces_Speccode_df.loc[:,['DataBase_ID']]).astype(int)
            NumSpeces_Speccode_df['RecordIdentifier'] = (NumSpeces_Speccode_df.loc[:,['RecordIdentifier']]).astype(int)
            NumSpeces_Speccode_df['DeploymentUID'] = (NumSpeces_Speccode_df.loc[:,['DeploymentUID']]).astype(str)

            NumSpeces_Speccode_df['DeploymentNumber'] = (NumSpeces_Speccode_df.loc[:,['DeploymentNumber']]).fillna(99999999)
            NumSpeces_Speccode_df['DeploymentNumber'] = (NumSpeces_Speccode_df.loc[:,['DeploymentNumber']]).replace([''], 99999999)
            NumSpeces_Speccode_df['DeploymentNumber'] = (NumSpeces_Speccode_df.loc[:,['DeploymentNumber']]).astype(int)
            
            NumSpeces_Speccode_df['SetNumber'] = (NumSpeces_Speccode_df.loc[:,['SetNumber']]).fillna(99999999)
            NumSpeces_Speccode_df['SetNumber'] = (NumSpeces_Speccode_df.loc[:,['SetNumber']]).replace([''], 99999999)
            NumSpeces_Speccode_df['SetNumber'] = (NumSpeces_Speccode_df.loc[:,['SetNumber']]).astype(int)
            
            NumSpeces_Speccode_df['RecordType'] = (NumSpeces_Speccode_df.loc[:,['RecordType']]).fillna(99999999)
            NumSpeces_Speccode_df['RecordType'] = (NumSpeces_Speccode_df.loc[:,['RecordType']]).replace([''], 99999999)
            NumSpeces_Speccode_df['RecordType'] = (NumSpeces_Speccode_df.loc[:,['RecordType']]).astype(int)
            
            NumSpeces_Speccode_df['NumberSpecies'] = (NumSpeces_Speccode_df.loc[:,['NumberSpecies']]).fillna(99999999)
            NumSpeces_Speccode_df['NumberSpecies'] = (NumSpeces_Speccode_df.loc[:,['NumberSpecies']]).replace([''], 99999999)
            NumSpeces_Speccode_df['NumberSpecies'] = (NumSpeces_Speccode_df.loc[:,['NumberSpecies']]).astype(int)

            NumSpeces_Speccode_df['SpeciesCode'] = (NumSpeces_Speccode_df.loc[:,['SpeciesCode']]).fillna(99999999)
            NumSpeces_Speccode_df['SpeciesCode'] = (NumSpeces_Speccode_df.loc[:,['SpeciesCode']]).replace([''], 99999999)
            NumSpeces_Speccode_df['SpeciesCode'] = (NumSpeces_Speccode_df.loc[:,['SpeciesCode']]).astype(int)
            NumSpeces_Speccode_df = NumSpeces_Speccode_df.reset_index(drop=True)
            NumSpeces_Speccode_df = pd.DataFrame(NumSpeces_Speccode_df)
            
            
            SetCatchQCFailedDB_DF = pd.merge(RType_SPCode_df, NumSpeces_Speccode_df, 
                                    how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID',
                                                        'DeploymentNumber','SetNumber','RecordType',
                                                        'NumberSpecies', 'SpeciesCode'])
            SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int)
            SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int)
            SetCatchQCFailedDB_DF['DeploymentUID'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentUID']]).astype(str)

            SetCatchQCFailedDB_DF['DeploymentNumber'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
            SetCatchQCFailedDB_DF['DeploymentNumber'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
            SetCatchQCFailedDB_DF['DeploymentNumber'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentNumber']]).astype(int)
            
            SetCatchQCFailedDB_DF['SetNumber'] = (SetCatchQCFailedDB_DF.loc[:,['SetNumber']]).fillna(99999999)
            SetCatchQCFailedDB_DF['SetNumber'] = (SetCatchQCFailedDB_DF.loc[:,['SetNumber']]).replace([''], 99999999)
            SetCatchQCFailedDB_DF['SetNumber'] = (SetCatchQCFailedDB_DF.loc[:,['SetNumber']]).astype(int)
            
            SetCatchQCFailedDB_DF['RecordType'] = (SetCatchQCFailedDB_DF.loc[:,['RecordType']]).fillna(99999999)
            SetCatchQCFailedDB_DF['RecordType'] = (SetCatchQCFailedDB_DF.loc[:,['RecordType']]).replace([''], 99999999)
            SetCatchQCFailedDB_DF['RecordType'] = (SetCatchQCFailedDB_DF.loc[:,['RecordType']]).astype(int)
            
            SetCatchQCFailedDB_DF['NumberSpecies'] = (SetCatchQCFailedDB_DF.loc[:,['NumberSpecies']]).fillna(99999999)
            SetCatchQCFailedDB_DF['NumberSpecies'] = (SetCatchQCFailedDB_DF.loc[:,['NumberSpecies']]).replace([''], 99999999)
            SetCatchQCFailedDB_DF['NumberSpecies'] = (SetCatchQCFailedDB_DF.loc[:,['NumberSpecies']]).astype(int)

            SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).fillna(99999999)
            SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).replace([''], 99999999)
            SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).astype(int)

            SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(np.nan, '')
            SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace([99999999, 99999999.0, '.', 'Null'], '')
            SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace([8888888, '8888888', '.','Null'], 'None')
            
            if len(SetCatchQCFailedDB_DF) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,
                                        ['DataBase_ID',
                                         'RecordIdentifier',
                                         'DeploymentUID',
                                         'QCCaseType_x', 
                                         'QCCaseType_y']]
                SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int)
                SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int)
                SetCatchQCFailedDB_DF['DeploymentUID'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentUID']]).astype(str)
                SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                return SetCatchQCFailedDB_DF
            else:
                return SetCatchQCFailedDB_DF
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
        GetSetCatchDB_VariableList = ['DeploymentNumber','SetNumber','RecordType',
                                      'NumberSpecies', 'SpeciesCode']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                         UpdateRecordList_QCFailDB, get_entry_ViewVarResults,
                                         UpdateQCMsg_QCFailDB):
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

        conn_Validation_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
        cur_Validation_Logical=conn_Validation_Logical.cursor()
        
        ## Updaing SetCatch DB
        if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)

        if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberSpecies = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
                
        if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SpeciesCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
        
        ### Updating QC Failed DB
        GetQCFailed_VariableList = ['DeploymentNumber','SetNumber','RecordType',
                                      'NumberSpecies', 'SpeciesCode']
        ListVariableSelect = ['Case-A SpeciesCode - RecType1 @ Each Set',
                              'Case-B SpeciesCode - RecType2 - NumberSpecies @ Each Set']
        
        ## RecordType_SpeciesCode
        ## Case-A
        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                               SET DeploymentNumber =  \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                               UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)

        if (get_Updated_Variable == GetQCFailed_VariableList[1])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                               SET SetNumber = ?  \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[2])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                               SET RecordType = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)

        if (get_Updated_Variable == GetQCFailed_VariableList[3])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                               SET NumberSpecies = ?  \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)

        if (get_Updated_Variable == GetQCFailed_VariableList[4])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                               SET SpeciesCode = ?  \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)
        ## NumberSpecies_SpeciesCode
        ## Case-B
        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                                               SET DeploymentNumber = ?\
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)

        if (get_Updated_Variable == GetQCFailed_VariableList[1])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                                               SET SetNumber = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)


        if (get_Updated_Variable == GetQCFailed_VariableList[2])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                                               SET RecordType = ?\
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)

        if (get_Updated_Variable == GetQCFailed_VariableList[3])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                                               SET NumberSpecies = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)

        if (get_Updated_Variable == GetQCFailed_VariableList[4])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                                               SET SpeciesCode = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET QCCaseType =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)      
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Logical.commit()
        conn_Validation_Logical.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18=['DeploymentNumber','SetNumber','RecordType']
            Var_Class_String7 =['DeploymentUID']
            Var_Class_IntB27  = ['NumberSpecies', 'SpeciesCode']
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
        get_Updated_Variable = entry_UpdateVariableList.get()
        get_UpdateValue_UpdatedVariable = entry_UpdateValue_VariableA.get()
        get_entry_ViewVarResults = entry_ViewVarResults.get()
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
                        UpdateRecordList =[]
                        UpdateRecordList_QCFailDB =[]
                        UpdateQCMsg_QCFailDB =[]  
                        for item in tree1.selection():
                            list_item = (tree1.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            list_item_QCCaseType = ''
                            UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DatabaseUID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                            UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,  
                                                            list_item_DatabaseUID,
                                                            list_item_RecordIdentifier,
                                                            list_item_DeploymentUID))
                            UpdateQCMsg_QCFailDB.append((list_item_QCCaseType,
                                                        list_item_DeploymentUID))
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                                        UpdateRecordList_QCFailDB, get_entry_ViewVarResults,
                                                        UpdateQCMsg_QCFailDB)
                        viewQCFailed_VariablesProfile()
                        GenSummaryQC()
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")
                        
                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                        iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                                                                    "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                        if iUpdateSlected >0:
                            UpdateRecordList =[]
                            UpdateRecordList_QCFailDB =[]
                            UpdateQCMsg_QCFailDB =[] 
                            for item in tree1.selection():
                                list_item = (tree1.item(item, 'values'))
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                list_item_QCCaseType = ''
                                UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                                UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,
                                                            list_item_DatabaseUID,
                                                            list_item_RecordIdentifier,
                                                            list_item_DeploymentUID))
                                UpdateQCMsg_QCFailDB.append((list_item_QCCaseType,
                                                            list_item_DeploymentUID))
                            Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                                            UpdateRecordList_QCFailDB, get_entry_ViewVarResults,
                                                            UpdateQCMsg_QCFailDB)
                            viewQCFailed_VariablesProfile()
                            GenSummaryQC()
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
            EntryDataType_Variable = 'Numeric'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)

    def callbackFuncSelectView(event):
        ListVariableListA = ['Select Logical Variable Pair From DropDown & Run View Selected Button', 
                         'Case-A SpeciesCode - RecType1 @ Each Set',
                         'Case-B SpeciesCode - RecType2 - NumberSpecies @ Each Set']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            txtQCVariableView.delete(0,END)
            txtRelatedQCVariableView.delete(0,END)
            tree1.delete(*tree1.get_children())
        
        if(SelVariableView ==ListVariableListA[0]):
            txtQCVariableView.delete(0,END)
            txtRelatedQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'QC Variable')
            txtRelatedQCVariableView.insert(tk.END, 'Related QC Variable')
            tree1.delete(*tree1.get_children())
            
        if(SelVariableView ==ListVariableListA[1]):
            txtQCVariableView.delete(0,END)
            txtRelatedQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'RecType1')
            txtRelatedQCVariableView.insert(tk.END, 'SpeciesCode')
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Case - A : For RecordType1 @ Each Set')
            txtDisplayMessageSystem.insert(2, 'SpeciesCode Must Be Blank ')
            tree1.delete(*tree1.get_children())
        
        if(SelVariableView ==ListVariableListA[2]):
            txtQCVariableView.delete(0,END)
            txtRelatedQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'RecType2 & NumberSpecies')
            txtRelatedQCVariableView.insert(tk.END, 'SpeciesCode')
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Case -B : For RecordType2 @ Each Set CountSum Of SpeciesCode')
            txtDisplayMessageSystem.insert(2, 'Must Equal To NumberSpecies')
            txtDisplayMessageSystem.insert(3, '& NumberSpecies Must Be Same')
            txtDisplayMessageSystem.insert(4, '')
            tree1.delete(*tree1.get_children())

    def GenSummaryQC():
        QCMsg = ['RecTyp1 & SpecsCode @ Each Set',
                 'Case - A',
                 'RecTyp2 & CountSpecsCode & NumbSpecs @ Each Set',
                 'Case - B']
        txtToUpdateEntriesCount.delete(0,END)
        txtAlreadyUpdateEntriesCount.delete(0,END)
        gettotalQCfailCount = QCFailedTotalEntries()
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        RecTyp_SpecCode_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                ORDER BY `DataBase_ID` ASC ;", conn)
        NumSpec_SpecCode_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                            ORDER BY `DataBase_ID` ASC ;", conn)
        RecTyp_SpecCode_df = pd.DataFrame(RecTyp_SpecCode_df)
        NumSpec_SpecCode_df = pd.DataFrame(NumSpec_SpecCode_df)
        cursor.close()
        conn.close()

        ## Populating ToUpdateEntriesCount & AlreadyUpdateEntriesCount
        if len(RecTyp_SpecCode_df) > 0:
            Update_RT_SC_df = RecTyp_SpecCode_df[(RecTyp_SpecCode_df.QCCaseType == QCMsg[1])]
            Count_Update_RT_SC_df = int(Update_RT_SC_df.DeploymentUID.unique().size)
        else:
            Count_Update_RT_SC_df = 0
        if len(NumSpec_SpecCode_df) > 0:   
            Update_NS_SC_df = NumSpec_SpecCode_df[(NumSpec_SpecCode_df.QCCaseType == QCMsg[3])]
            Count_Update_NS_SC_df = int(Update_NS_SC_df.DeploymentUID.unique().size)
        else:
            Count_Update_NS_SC_df = 0
        QCFailedSummaryCountUpdate = Count_Update_RT_SC_df + Count_Update_NS_SC_df
        AlreadyUpdateEntriesCount =  int(gettotalQCfailCount) - int(QCFailedSummaryCountUpdate)
        txtToUpdateEntriesCount.insert(tk.END,QCFailedSummaryCountUpdate)
        txtAlreadyUpdateEntriesCount.insert(tk.END,AlreadyUpdateEntriesCount)
       
        ## For RecTyp_SpecCode_df
        if len(RecTyp_SpecCode_df) >0:
            SetCatchQCFailedDB_DF  = pd.DataFrame(RecTyp_SpecCode_df)
            Summary_RecTyp_SpecCode_df= SetCatchQCFailedDB_DF.groupby(['QCCaseType'],  
                    as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(np.unique(x))))
            Summary_RecTyp_SpecCode_df  = Summary_RecTyp_SpecCode_df.reset_index(drop=True)
            Summary_RecTyp_SpecCode_df  = pd.DataFrame(Summary_RecTyp_SpecCode_df)
            CaseA_RecTyp_SpecCode_df = Summary_RecTyp_SpecCode_df[
                                      (Summary_RecTyp_SpecCode_df.QCCaseType ==QCMsg[1])]
            if len(CaseA_RecTyp_SpecCode_df)>0:
                ValueCaseA_RecTyp_SpecCode_df = (CaseA_RecTyp_SpecCode_df.iloc[0]['DeploymentUID'])
            else:
                ValueCaseA_RecTyp_SpecCode_df = 0
            
            QCEntries_CaseA= len(SetCatchQCFailedDB_DF[
                                (SetCatchQCFailedDB_DF.QCCaseType ==QCMsg[1])])
        else:
            ValueCaseA_RecTyp_SpecCode_df = 0
            QCEntries_CaseA = 0
        
        ## For NumSpec_SpecCode_df
        if len(NumSpec_SpecCode_df) >0:
            SetCatchQCFailedDB_DF  = pd.DataFrame(NumSpec_SpecCode_df)
            Summary_NumSpec_SpecCode_df= SetCatchQCFailedDB_DF.groupby(['QCCaseType'],  
                    as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(np.unique(x))))
            Summary_NumSpec_SpecCode_df  = Summary_NumSpec_SpecCode_df.reset_index(drop=True)
            Summary_NumSpec_SpecCode_df  = pd.DataFrame(Summary_NumSpec_SpecCode_df)
            CaseA_NumSpec_SpecCode_df = Summary_NumSpec_SpecCode_df[
                                      (Summary_NumSpec_SpecCode_df.QCCaseType ==QCMsg[3])]
            if len(CaseA_NumSpec_SpecCode_df)>0:
                ValueCaseB_NumSpec_SpecCode_df = (CaseA_NumSpec_SpecCode_df.iloc[0]['DeploymentUID'])
            else:
                ValueCaseB_NumSpec_SpecCode_df = 0
            QCEntries_CaseB= len (SetCatchQCFailedDB_DF[
                                      (SetCatchQCFailedDB_DF.QCCaseType ==QCMsg[3])])
        else:
            ValueCaseB_NumSpec_SpecCode_df = 0
            QCEntries_CaseB = 0
       
       ## Building QC Summary DF With RecTyp_SpecCode_df & NumSpec_SpecCode_df
        QCFailAppend = {'QCCaseType':  [QCMsg[1], QCMsg[3]],
                        'QCFailCount': [ValueCaseA_RecTyp_SpecCode_df,
                                        ValueCaseB_NumSpec_SpecCode_df],
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
        
    def InventoryRec3(event):
        ListVariableListA = ['Case - A', 'Case - B']
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        RecTyp_SpecCode_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                ORDER BY `DataBase_ID` ASC ;", conn)
        NumSpec_SpecCode_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                            ORDER BY `DataBase_ID` ASC ;", conn)
        ## Case-A DF 
        RecTyp_SpecCode_df = pd.DataFrame(RecTyp_SpecCode_df)
        ## Case-B DF 
        NumSpec_SpecCode_df = pd.DataFrame(NumSpec_SpecCode_df)
        cursor.close()
        conn.close()
        ## Summary frame Table B Selection
        nm =Summaryframetree.selection()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            NumberEntriesInSet = sd[1]
            txtSummaryDisplayMsg.delete(0,END)
            txtSummaryDisplayMsg.insert(tk.END,((" Type : ") +
                                                SelvariableIdentifier + ' ' +' & '+
                                                "Number Of Set Failed: " + 
                                                NumberEntriesInSet))
            
            if (int(NumberEntriesInSet) > 0):
                ## Main Table A Displaying 
                if(SelvariableIdentifier ==ListVariableListA[0]):
                    tree1.delete(*tree1.get_children())
                    txtQCVariableView.delete(0,END)
                    txtRelatedQCVariableView.delete(0,END)
                    txtQCVariableView.insert(tk.END, 'RecType1')
                    txtRelatedQCVariableView.insert(tk.END, 'SpeciesCode')
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'Case - A : For RecordType1 @ Each Set')
                    txtDisplayMessageSystem.insert(2, 'SpeciesCode Must Be Blank ')

                    RecTyp_SpecCode_df  = RecTyp_SpecCode_df.reset_index(drop=True)
                    QCFailDF_Selected  = pd.DataFrame(RecTyp_SpecCode_df)
                    QCFailDF_Selected.sort_values(by=['DeploymentUID', 'DeploymentNumber',
                            'SetNumber','RecordType'], inplace=True)
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
                    entry_ViewVarResults.current(1)

                if(SelvariableIdentifier ==ListVariableListA[1]):
                    tree1.delete(*tree1.get_children())
                    txtQCVariableView.delete(0,END)
                    txtRelatedQCVariableView.delete(0,END)
                    txtQCVariableView.insert(tk.END, 'RecType2 & NumberSpecies')
                    txtRelatedQCVariableView.insert(tk.END, 'SpeciesCode')
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'Case -B : For RecordType2 @ Each Set CountSum Of SpeciesCode')
                    txtDisplayMessageSystem.insert(2, 'Must Equal To NumberSpecies')
                    txtDisplayMessageSystem.insert(3, '& NumberSpecies Must Be Same')
                    txtDisplayMessageSystem.insert(4, '')

                    NumSpec_SpecCode_df  = NumSpec_SpecCode_df.reset_index(drop=True)
                    QCFailDF_Selected  = pd.DataFrame(NumSpec_SpecCode_df)
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
                    entry_ViewVarResults.current(2)

                ### Selected Results Overview
                ## Case-A Filter From RecTyp_SpecCode_df
                if(SelvariableIdentifier == ListVariableListA[0]):
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                    entry_SelResultOverview.delete(0,END)
                    RecTyp_SpecCode_df = RecTyp_SpecCode_df.loc[:,['DeploymentUID',
                                            'DeploymentNumber', 'SetNumber', 'RecordType', 
                                            'NumberSpecies', 'SpeciesCode',
                                            'QCCaseType']]
                    CaseA_RecTyp_SpecCode_df = RecTyp_SpecCode_df[(
                            (RecTyp_SpecCode_df['QCCaseType'] == SelvariableIdentifier) 
                            )]
                    CaseA_RecTyp_SpecCode_df  = CaseA_RecTyp_SpecCode_df.reset_index(drop=True)
                    CaseA_Overview  = pd.DataFrame(CaseA_RecTyp_SpecCode_df)
                    CaseA_Overview.sort_values(by=['DeploymentNumber','SetNumber','RecordType'], inplace=True)
                    CaseA_Overview = CaseA_Overview.loc[:,['DeploymentUID','QCCaseType',
                                                        'SetNumber',  'NumberSpecies', 
                                                        'SpeciesCode']]
                    CaseA_Overview  = CaseA_Overview.reset_index(drop=True)
                    CaseA_Overview  = pd.DataFrame(CaseA_Overview)
                    
                    CaseA_Overview_DF = CaseA_Overview.groupby(['DeploymentUID', 'QCCaseType'], as_index=False).\
                        aggregate({'SetNumber':'count', 'SpeciesCode':lambda x: x.nunique(),
                                'NumberSpecies':lambda x: round((x.mean()), 1)})
                    
                    CaseA_Overview_DF.rename(columns={'DeploymentUID':'DeploymentUID', 
                                                    'QCCaseType':'QCCaseType',
                                                    'SetNumber':'#Entries/SetN',     
                                                    'SpeciesCode':'#SpecesCode/SetN',
                                                    'NumberSpecies':'MeanNumSpeces'
                                                    },inplace = True)
                    CaseA_Overview_DF = pd.DataFrame(CaseA_Overview_DF)
                    CaseA_Overview_DF[['#Entries/SetN']] = CaseA_Overview_DF[['#Entries/SetN']].astype(int)
                    CaseA_Overview_DF[['#SpecesCode/SetN']] = CaseA_Overview_DF[['#SpecesCode/SetN']].astype(int)
                    CaseA_Overview_DF.sort_values(by=['DeploymentUID'], inplace=True, ascending=True)
                    CaseA_Overview_DF  = CaseA_Overview_DF.reset_index(drop=True)
                    CaseA_Overview_DF  = pd.DataFrame(CaseA_Overview_DF)
                    countIndex1 = 0
                    for each_rec in range(len(CaseA_Overview_DF)):
                        if countIndex1 % 2 == 0:
                            SelResultOverviewtree.insert("", tk.END, values=list(CaseA_Overview_DF.loc[each_rec]), tags =("even",))
                        else:
                            SelResultOverviewtree.insert("", tk.END, values=list(CaseA_Overview_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    SelResultOverviewtree.tag_configure("even",foreground="black", background="lightgreen")
                    SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
                    entry_SelResultOverview.delete(0,END)
                    entry_SelResultOverview.insert(tk.END,((" Case-A Unique DeploymentUID Found : ") +
                                                            NumberEntriesInSet))
               
                ## Case-B Filter From NumSpec_SpecCode_df
                if(SelvariableIdentifier == ListVariableListA[1]):
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                    entry_SelResultOverview.delete(0,END)
                    NumSpec_SpecCode_df = NumSpec_SpecCode_df.loc[:,['DeploymentUID',
                                            'DeploymentNumber', 'SetNumber', 'RecordType',
                                            'NumberSpecies', 'SpeciesCode',
                                            'QCCaseType']]
                    CaseB_NumSpec_SpecCode_df = NumSpec_SpecCode_df[(
                            (NumSpec_SpecCode_df['QCCaseType'] == SelvariableIdentifier) 
                            )]
                    CaseB_NumSpec_SpecCode_df  = CaseB_NumSpec_SpecCode_df.reset_index(drop=True)
                    CaseB_Overview  = pd.DataFrame(CaseB_NumSpec_SpecCode_df)
                    CaseB_Overview.sort_values(by=['DeploymentNumber','SetNumber','RecordType'], inplace=True)
                    CaseB_Overview = CaseB_Overview.loc[:,['DeploymentUID','QCCaseType',
                                                        'SetNumber','NumberSpecies', 
                                                        'SpeciesCode']]
                    CaseB_Overview  = CaseB_Overview.reset_index(drop=True)
                    
                    CaseB_Overview_DF  = pd.DataFrame(CaseB_Overview)
                    CaseB_Overview_DF = CaseB_Overview_DF.groupby(['DeploymentUID', 'QCCaseType'], as_index=False).\
                        aggregate({'SetNumber':'count', 'SpeciesCode':lambda x: (np.count_nonzero(x)),
                                'NumberSpecies':lambda x: round((x.mean()), 1)})
                    CaseB_Overview_DF.rename(columns={'DeploymentUID':'DeploymentUID', 'QCCaseType':'QCCaseType',
                                                    'SetNumber':'#Entries/SetN',     
                                                    'SpeciesCode':'#SpecesCode/SetN',
                                                    'NumberSpecies':'MeanNumSpeces'
                                                    },inplace = True)
                    CaseB_Overview_DF = pd.DataFrame(CaseB_Overview_DF)
                    CaseB_Overview_DF[['#Entries/SetN']] = CaseB_Overview_DF[['#Entries/SetN']].astype(int)
                    CaseB_Overview_DF[['#SpecesCode/SetN']] = CaseB_Overview_DF[['#SpecesCode/SetN']].astype(int)
                    CaseB_Overview_DF.sort_values(by=['DeploymentUID'], inplace=True, ascending=True)
                    CaseB_Overview_DF  = CaseB_Overview_DF.reset_index(drop=True)
                    CaseB_Overview_DF  = pd.DataFrame(CaseB_Overview_DF)
                    countIndex1 = 0
                    for each_rec in range(len(CaseB_Overview_DF)):
                        if countIndex1 % 2 == 0:
                            SelResultOverviewtree.insert("", tk.END, values=list(CaseB_Overview_DF.loc[each_rec]), tags =("even",))
                        else:
                            SelResultOverviewtree.insert("", tk.END, values=list(CaseB_Overview_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    SelResultOverviewtree.tag_configure("even",foreground="black", background="lightgreen")
                    SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
                    entry_SelResultOverview.delete(0,END)
                    entry_SelResultOverview.insert(tk.END,((" Case-B Unique DeploymentUID Found : ") +
                                                            NumberEntriesInSet))
            
            else:
                entry_SelResultOverview.delete(0,END)
                entry_SelResultOverview.insert(tk.END,"Empty QCCaseType - All Updated Or No Fail Found")
                tree1.delete(*tree1.get_children())
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                txtQCVariableView.delete(0,END)
                txtRelatedQCVariableView.delete(0,END)
                entry_ViewVarResults.current(0)
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'Zero SetQCFailCount Failed In Selected Case Type')
                txtDisplayMessageSystem.insert(2, 'Please Select Not Zero SetQCFailCount Entry')
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, (' Please Select Only One Entries To View'))

    def InventoryRec4(event):
        ListCaseType = ['Case - A', 'Case - B']
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        cursor = conn.cursor()
        RecTyp_SpecCode_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SpeciesCode \
                                ORDER BY `DataBase_ID` ASC ;", conn)
        NumSpec_SpecCode_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode \
                            ORDER BY `DataBase_ID` ASC ;", conn)
        ## Case-A DF 
        RecTyp_SpecCode_df = pd.DataFrame(RecTyp_SpecCode_df)
        ## Case-B DF 
        NumSpec_SpecCode_df = pd.DataFrame(NumSpec_SpecCode_df)
        cursor.close()
        conn.close()
        ## Concat Both RecTyp_SpecCode_df & NumSpec_SpecCode_df
        QCFailDF  = pd.concat([RecTyp_SpecCode_df, NumSpec_SpecCode_df])
        QCFailDF  = QCFailDF.reset_index(drop=True)
        QCFailDF  = pd.DataFrame(QCFailDF)
        
        ## SelResultOverviewtree selection
        nm =SelResultOverviewtree.selection()
        if len(nm) ==1:
            sd = SelResultOverviewtree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            SelectedQCCaseType = sd[1]
            NumberEntriesInSet = sd[2]
            entry_SelResultOverview.delete(0,END)
            entry_SelResultOverview.insert(tk.END,(("Selected DeploymentUID : ") +
                                                SelvariableIdentifier))
            tree1.delete(*tree1.get_children())
            if (SelectedQCCaseType == ListCaseType[0]):
                QCFailDF_Selected = QCFailDF[(
                (QCFailDF['DeploymentUID'] == SelvariableIdentifier) &
                (QCFailDF['QCCaseType'] == SelectedQCCaseType)
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
                QCFailDF_Selected = QCFailDF[(
                (QCFailDF['DeploymentUID'] == SelvariableIdentifier) &
                (QCFailDF['QCCaseType'] == SelectedQCCaseType)
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
            txtDisplayMessageSystem.insert(1, (' Please Select Only One Entries To View'))
    
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
                            'DeploymentNumber','SetNumber','RecordType',
                            'NumberSpecies', 'SpeciesCode']]).replace(
                            ['', None, np.nan, 'None'], 99999999)
                
                Complete_df[['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber', 'SetNumber', 'RecordType',
                            'NumberSpecies','SpeciesCode']] = Complete_df[
                            ['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber', 'SetNumber', 'RecordType',
                            'NumberSpecies','SpeciesCode']].astype(int)
                
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
                Update_RT_SC_Failed =[]
                Update_NS_SC_Failed =[]
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
                    list_item_SpeciesCode = (rowValue[7])
                    list_item_QCCaseType = 'Case Updated'
                    
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_RecordType,
                                        list_item_NumberSpecies,
                                        list_item_SpeciesCode,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                    
                    Update_RT_SC_Failed.append((
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_RecordType,
                                        list_item_NumberSpecies,
                                        list_item_SpeciesCode,
                                        list_item_QCCaseType,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                    
                    Update_NS_SC_Failed.append((
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_RecordType,
                                        list_item_NumberSpecies,
                                        list_item_SpeciesCode,
                                        list_item_QCCaseType,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                                                 
                            ## DB Update Executing
                
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ?, \
                                        SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                        SpeciesCode = ?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdateRecordList_SetCatchDB)
                            
                cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET DeploymentNumber = ?, \
                                        SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                        SpeciesCode = ?, QCCaseType = ? \
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        Update_RT_SC_Failed)
                            
                cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET DeploymentNumber = ?, \
                                        SetNumber = ?, RecordType = ?, NumberSpecies = ? , \
                                        SpeciesCode = ?, QCCaseType = ? \
                                        WHERE DataBase_ID = ? AND RecordIdentifier = ? AND DeploymentUID = ?", 
                                        Update_NS_SC_Failed)
                            
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
                     'DeploymentNumber','SetNumber','RecordType',
                     'NumberSpecies', 'SpeciesCode']])
                QCFailedLogical_DF  = pd.DataFrame(rows)
                ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF)
   
    def SearchDepUIDNumFromSetCatchDB():
        get_DepUIDforSearch = entry_SelResultOverview.get()
        get_DepUIDforSearch = get_DepUIDforSearch.split(" : ")
        get_SelMsg = str(get_DepUIDforSearch[0])
        if get_SelMsg == ("Selected DeploymentUID"):
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
                        'DeploymentNumber','SetNumber','RecordType',
                        'NumberSpecies', 'SpeciesCode']])
                QCFailedLogical_DF  = pd.DataFrame(rows)
                ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF)
    
    def UpdateDeploymentUIDAfterUpdate():
        ## Update DepUID In SetCatch DB
        def UpdateSetcatchDB():
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
        
        ## Update DepUID In QC Fail DB
        def UpdateQCFailedDB():
            def GetUpdateQCFailedListDF(Complete_df):
                SetCatchQCFailed_DF  = pd.DataFrame(Complete_df)
                def BuildUpdatedDepUID(SetCatchQCFailed_DF):
                    try:
                        if len(SetCatchQCFailed_DF) >0:
                            SetCatchQCFailed_DF[['Year', 'ASOCCode', 
                                                 'DeploymentNumberTemp', 'SetNumberTemp']
                                                 ] = SetCatchQCFailed_DF.DeploymentUID.str.split("-", expand = True)
                            SetCatchQCFailed_DF = SetCatchQCFailed_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                                                            'Year','ASOCCode','DeploymentNumber',
                                                                            'SetNumber']]
                            SetCatchQCFailed_DF = SetCatchQCFailed_DF.replace(np.nan, 99999999)
                            SetCatchQCFailed_DF = SetCatchQCFailed_DF.replace('', 99999999)
                            SetCatchQCFailed_DF[['DataBase_ID','RecordIdentifier',
                                                'Year','ASOCCode','DeploymentNumber',
                                                'SetNumber']] = SetCatchQCFailed_DF[
                                                ['DataBase_ID','RecordIdentifier',
                                                'Year','ASOCCode','DeploymentNumber',
                                                'SetNumber']].astype(int)
                            SetCatchQCFailed_DF = SetCatchQCFailed_DF.replace(99999999, '')
                            SetCatchQCFailed_DF['DeploymentUID'] = SetCatchQCFailed_DF["Year"].map(str) + "-" + \
                                                                    SetCatchQCFailed_DF["ASOCCode"].map(str)+ "-" +\
                                                                    SetCatchQCFailed_DF["DeploymentNumber"].map(str)+"-"+ \
                                                                    SetCatchQCFailed_DF["SetNumber"].map(str)
                            SetCatchQCFailed_DF = SetCatchQCFailed_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                                'Year','ASOCCode','DeploymentNumber',
                                                                                'SetNumber']]
                        
                            SetCatchQCFailed_DF  = SetCatchQCFailed_DF.reset_index(drop=True)
                            SetCatchQCFailed_DF  = pd.DataFrame(SetCatchQCFailed_DF)
                            return SetCatchQCFailed_DF
                        else:
                            return SetCatchQCFailed_DF
                    except sqlite3.Error as error:
                        print('Error occured - ', error)
                
                SetCatchQCFailedDB_DF = BuildUpdatedDepUID(SetCatchQCFailed_DF)
                UpdateQCFailedListDF =[]
                if len(SetCatchQCFailedDB_DF) >0:
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
                        UpdateQCFailedListDF.append((
                                    list_item_DeploymentUID,
                                    list_item_DeploymentNumber,
                                    list_item_SetNumber,
                                    list_item_DataBase_ID,
                                    list_item_RecordIdentifier,
                                    ))
                return UpdateQCFailedListDF
                
            conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
            cursor = conn.cursor()
            RS_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecordType_SpeciesCode;", conn)
            NS_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode;", conn)
            RS_FailConsistency_DF = pd.DataFrame(RS_FailConsistency_DF)
            NS_FailConsistency_DF = pd.DataFrame(NS_FailConsistency_DF)
            cursor.close()
            conn.close()

            RS_FailList_Get = GetUpdateQCFailedListDF(RS_FailConsistency_DF)
            NS_FailList_Get = GetUpdateQCFailedListDF(NS_FailConsistency_DF)
           
            ## DB Update Executing
            conn_DB_Set_Catch_Logical= sqlite3.connect(DB_SetCatch_Validation_Logical)
            cur_DB_Set_Catch_Logical=conn_DB_Set_Catch_Logical.cursor()
            if (len(RS_FailList_Get)) > 0:
                cur_DB_Set_Catch_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecordType_SpeciesCode SET DeploymentUID =?, \
                                                    DeploymentNumber = ?, SetNumber = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    RS_FailList_Get)
            if (len(NS_FailList_Get)) > 0:
                cur_DB_Set_Catch_Logical.executemany("UPDATE SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode SET DeploymentUID =?, \
                                                    DeploymentNumber = ?, SetNumber = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    NS_FailList_Get)
            conn_DB_Set_Catch_Logical.commit()
            conn_DB_Set_Catch_Logical.close()
                    
        ## Updating QC Fail DB - SetCatch DB
        UpdateSetcatchDB()
        ## Updating QC Fail DB - Year-Country- Quota
        UpdateQCFailedDB()
        tree1.delete(*tree1.get_children())
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    # Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    SelResultOverviewtree.bind('<<TreeviewSelect>>',InventoryRec4)
    ## ComboBox Select
    entry_UpdateVariableList.bind('<<ComboboxSelected>>', callbackFuncSelectVariable1)
    
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ## Gen QC Summary
    GenSummaryQC()
    QCFailedTotalEntries()

    # SelectViewResultsRun Button
    btnViewQCFailedQCResults = Button(SelectViewResultsRun, text="View Selected Results", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=18, bd=1, command = viewQCFailed_VariablesProfile)
    btnViewQCFailedQCResults.grid(row =0, column = 3, padx=2, pady =2, ipady =2, sticky =W)

    btnSearchDepSetCatchDB = Button(SelectViewResultsRun, text="Search SetCatch Deployment", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=25, bd=1, command = SearchDepNumFromSetCatchDB)
    btnSearchDepSetCatchDB.grid(row =1, column = 4, padx=140, pady =2, ipady =2, sticky =W)
    
    # Top Frame Button
    btnClearTable = Button(Topframe, text="Clear Table", font=('aerial', 9, 'bold'), bg='alice blue',
                                height =1, width=12, bd=1, command = ClearTablesAll)
    btnClearTable.grid(row =2, column = 0, padx=200, pady =2, ipady =2, sticky =W)

    ### Buttons On Update Frame
    button_UpdateSelectedDBEntries = Button(UpdateDB_Entryframe, bd = 2, text ="Update Selected Table Entries\n (DB Update)", width = 25,
                                height=2, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =UpdateSelected_SetCatch_DBEntries)
    button_UpdateSelectedDBEntries.grid(row =14, column = 0, padx=10, pady =1, ipady =4, sticky =W)

    button_Clear_EntriesUpdate = Button(UpdateDB_Entryframe, bd = 2, text ="Clear Entries", width = 10,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearEntries)
    button_Clear_EntriesUpdate.grid(row =6, column = 0, padx=15, pady =2, ipady =1, sticky =E)


    # Buttons On Generate QC Failed Summary Frame
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
    ImportExport.add_command(label="Export Failed Results (.csv)", command=Export_FailedLogicalVariablesCSV)
    ImportExport.add_command(label="Import & Update DB (.csv)", command=ImportAndUpdateSetCatchDB)
    View.add_command(label="View QC Failed All Results", command=QCFailedExcelViewAll)
    View.add_command(label="Ref-QCFail To Set&Catch DB", command=RefFailedToSetcatchDB)
    Update.add_command(label="Update DeplymentUID", command=UpdateDeploymentUIDAfterUpdate)
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack(side = LEFT)
    window.mainloop()

