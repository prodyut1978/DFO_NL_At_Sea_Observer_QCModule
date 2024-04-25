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

def ViewLogical_RecType_KW_DW_NI_Result():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Logical Validator - ID-C-04-4")
    window.geometry("1250x820+200+100")
    window.config(bg="cadet blue")

    ## Top Frame
    Topframe = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Topframe.pack(side = TOP)
    txtDisplayMessageSystem = Listbox(Topframe, font=('aerial', 9, 'bold'), 
                                      height =3, width =80)
    txtDisplayMessageSystem.grid(row =0, column = 0, padx=200, pady =5, ipady =5, sticky =E)

    lbl_QCDisplay = Label(Topframe, font=('aerial', 10, 'bold'), text="A: QCFailed Display Table:")
    lbl_QCDisplay.grid(row =0, column = 0, padx=2, pady =1, sticky =W)

    lbl_TotalFailedEntries = Label(Topframe, font=('aerial', 10 , 'bold'), bg= "cadet blue", text="# Of Entries Failed :")
    lbl_TotalFailedEntries.grid(row =2, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(Topframe, value='')
    txtTotalFailedEntries = Entry(Topframe, font=('aerial',12),textvariable = TotalFailedEntries, width = 5, bd=1)
    txtTotalFailedEntries.grid(row =2, column = 0, padx=134, pady =1, ipady =1, sticky =W)

    lbl_SelectedCaseTypeEntries = Label(Topframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" # Of Unique DepUID Failed : ")
    lbl_SelectedCaseTypeEntries.grid(row =2, column = 0, padx=60, pady =1, sticky =E)
    SelectedCaseTypeEntries       = IntVar(Topframe, value ='')
    entry_SelectedCaseTypeEntries = Entry(Topframe, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = SelectedCaseTypeEntries, width = 6, bd=1)
    entry_SelectedCaseTypeEntries.grid(row =2, column = 0, padx=10, pady =1, ipady =1, sticky =E)
    
    ## Table Frame Define
    Tableframe = tk.Frame(window, width = 40)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    
    SelectViewResultsRun = Frame(Tableframe, width = 80)
    SelectViewResultsRun.pack(side = TOP, padx= 0, pady=0)
    ListVariableListA = ['Select Logical QC Variable From DropDown & Run Selected Button', 
                         'KeptWeight & DiscardWeight & NumberIndividuals - RecType1 @ Each Set'
                         ]
    VariableList        = StringVar(SelectViewResultsRun, value ='')
    entry_ViewVarResults  = ttk.Combobox(SelectViewResultsRun, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable = VariableList, width = 80, state='readonly')
    entry_ViewVarResults.grid(row =0, column = 0, padx=2, pady =4, ipady= 4, sticky =E)
    entry_ViewVarResults['values'] = ListVariableListA
    entry_ViewVarResults.current(0)

    EntryDepNum       = IntVar(SelectViewResultsRun, value ='Enter DeploymentNumber')
    entry_DepNumforSearch = Entry(SelectViewResultsRun, font=('aerial', 10), justify='center',
                                textvariable = EntryDepNum, width = 25, bd=2)
    entry_DepNumforSearch.grid(row =0, column = 3, padx=405, pady =2, ipady =5, sticky =W)

    ## Tree1 Define
    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", 
                    "column4", "column5", "column6", 
                    "column7", "column8", "column9",
                    "column10", "column11", "column12"), height=18, show='headings')
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
    tree1.heading("#9", text="KeptWeight", anchor=CENTER)
    tree1.heading("#10", text="DiscardWeight", anchor=CENTER)
    tree1.heading("#11", text="NumberIndividuals", anchor=CENTER)
    tree1.heading("#12", text="QCMessage", anchor=tk.CENTER)
    
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#9', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree1.column('#10', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree1.column('#11', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)            
    tree1.column('#12', stretch=NO, minwidth=0, width=390, anchor = tk.CENTER)
    
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

    lbl_UpdateDB_Header = Label(UpdateDB_Entryframe, font=('aerial', 12, 'bold','underline'),
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
    
    ListVariableListA = ['KeptWeight','DiscardWeight','NumberIndividuals']
    VariableListA = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
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
    
    ###### SummaryQCframe Generate QC Failed Summary ###
    SummaryQCframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.pack(side =LEFT, padx=10, pady =2)
    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    Summaryframetree = ttk.Treeview(Summaryframe, column=("column1", "column2", "column3"),height=9, show='headings')
    scrollbary = ttk.Scrollbar(Summaryframe, orient ="vertical", command=Summaryframetree.yview)
    scrollbary.pack(side ='right', fill ='y')
    Summaryframetree.configure(yscrollcommand = scrollbary.set)
    Summaryframetree.heading("#1", text="QC Variable Name", anchor = tk.CENTER)
    Summaryframetree.heading("#2", text="RecordType", anchor = tk.CENTER)
    Summaryframetree.heading("#3", text="Fail Count (# Of Non Blank)", anchor = tk.CENTER)
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)                  
    Summaryframetree.column('#3', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    Summaryframetree.pack(side = BOTTOM)
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    SummaryDisplay.pack(side = LEFT, pady=0)

    # Define TreeView SelResultOverviewtree
    SelQCVariableDisplay = tk.Frame(window, bg= "aliceblue")
    SelQCVariable      = StringVar(SelQCVariableDisplay, value ='QC Variable')
    entry_SelQCVariable = Entry(SelQCVariableDisplay, font=('aerial', 10, 'bold'),  justify = tk.CENTER,
                            textvariable = SelQCVariable, width = 20, bd=2)
    entry_SelQCVariable.grid(row =0, column = 0, padx=2, pady =2, ipady =2, sticky =W)

    SelQCVariableDisplay.pack(side = TOP, pady=0, anchor = CENTER)
    SelResultOverview = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SelResultOverview.pack(side =LEFT, padx=2, pady =2)
    SelResultOverviewtree = ttk.Treeview(SelResultOverview,  
                            column=("column1", "column2", 
                                    "column3", "column4", 
                                    "column5"), height=9, show='headings')
    scrollbary = ttk.Scrollbar(SelResultOverview, orient ="vertical", command=SelResultOverviewtree.yview)
    scrollbary.pack(side ='right', fill ='y')
    SelResultOverviewtree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(SelResultOverview, orient ="horizontal", command=SelResultOverviewtree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    SelResultOverviewtree.configure(xscrollcommand = scrollbarx.set)
    SelResultOverviewtree.heading("#1", text="Year", anchor=CENTER)
    SelResultOverviewtree.heading("#2", text="ASOC", anchor=CENTER)
    SelResultOverviewtree.heading("#3", text="Dep#", anchor=CENTER)
    SelResultOverviewtree.heading("#4", text="RecType", anchor=CENTER)
    SelResultOverviewtree.heading("#5", text="# Of QC Fail", anchor=CENTER)
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)             
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)
    SelResultOverviewtree.column('#4', stretch=NO, minwidth=0, width=90, anchor = tk.CENTER)
    SelResultOverviewtree.column('#5', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = BOTTOM)

    ####All Defined Functions ########
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'DeploymentNumber','SetNumber','RecordType',
                            'NumberSpecies', 'SpeciesCode','KeptWeight',
                            'DiscardWeight','NumberIndividuals', 'QCMessage']
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
                        KeptWeight = (df.loc[:,'KeptWeight']).fillna(99999999).astype(int, errors='ignore')
                        DiscardWeight = (df.loc[:,'DiscardWeight']).fillna(99999999).astype(int, errors='ignore')
                        NumberIndividuals = (df.loc[:,'NumberIndividuals']).fillna(99999999).astype(int, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID, \
                                        DeploymentNumber, SetNumber, \
                                        RecordType, NumberSpecies, \
                                        SpeciesCode, KeptWeight, DiscardWeight,\
                                        NumberIndividuals]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns=  {0:'DataBase_ID', 1: 'RecordIdentifier', 2: 'DeploymentUID',
                                                3:'DeploymentNumber', 4:'SetNumber', 5:'RecordType', 
                                                6:'NumberSpecies', 7:'SpeciesCode',
                                                8:'KeptWeight', 9:'DiscardWeight',
                                                10:'NumberIndividuals'},inplace = True)
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
                            UpdatedQCFailedDB =[]
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
                                list_item_KeptWeight = (rowValue[8])
                                list_item_DiscardWeight = (rowValue[9])
                                list_item_NumberIndividuals = (rowValue[10])
                                list_item_QCMessage = ''
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_RecordType,
                                                    list_item_NumberSpecies,
                                                    list_item_SpeciesCode,
                                                    list_item_KeptWeight,
                                                    list_item_DiscardWeight,
                                                    list_item_NumberIndividuals,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                UpdatedQCFailedDB.append((
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_RecordType,
                                                    list_item_NumberSpecies,
                                                    list_item_SpeciesCode,
                                                    list_item_KeptWeight,
                                                    list_item_DiscardWeight,
                                                    list_item_NumberIndividuals,
                                                    list_item_QCMessage,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                           
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ?, \
                                                SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                                SpeciesCode = ?, KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?\
                                                WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_SetCatchDB)
                            
                            cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI SET DeploymentNumber = ?, \
                                                    SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                                    SpeciesCode = ?, KeptWeight = ?, DiscardWeight = ?,\
                                                    NumberIndividuals = ?, QCMessage = ? \
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdatedQCFailedDB)
                                                       
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
        txtDisplayMessageSystem.delete(0,END)
        
    def ClearEntries():
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateValue_VariableA.delete(0,END)
        entry_NumberRowSelected.delete(0,END)
    
    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select Logical QC Variable From DropDown & Run Selected Button', 
                         'KeptWeight & DiscardWeight & NumberIndividuals - RecType1 @ Each Set']
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Logical)
            cur=con.cursor()
            if getVarnameToView == ListVariableListA[1]:
                cur.execute("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI")
            rows=cur.fetchall()
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_VariablesProfile():
        ListVariableListA = ['Select Logical QC Variable From DropDown & Run Selected Button', 
                         'KeptWeight & DiscardWeight & NumberIndividuals - RecType1 @ Each Set']
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        entry_SelectedCaseTypeEntries.delete(0,END)
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows.rename(columns={0:'DataBase_ID', 1: 'RecordIdentifier', 2: 'DeploymentUID',
                            3:'DeploymentNumber', 4:'SetNumber', 5:'RecordType', 
                            6:'NumberSpecies', 7:'SpeciesCode',
                            8:'KeptWeight', 9:'DiscardWeight',
                            10:'NumberIndividuals', 11:'QCMessage'},inplace = True)
        if len(rows) >0 :
            if getVarnameToView == ListVariableListA[0]:
                txtDisplayMessageSystem.insert(1, 'Select Logical Variable Pair From DropDown & Run View Selected Button')
                txtDisplayMessageSystem.insert(2, '& Run View Selected Button')

            if getVarnameToView == ListVariableListA[1]:
                rows = rows.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                        'DeploymentNumber','SetNumber','RecordType',
                        'NumberSpecies', 'SpeciesCode','KeptWeight',
                        'DiscardWeight','NumberIndividuals', 'QCMessage']]
                rows.sort_values(by=['DeploymentNumber','SetNumber','RecordType'], inplace=True)
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
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI;", conn)
        conn.commit()
        conn.close()
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        if len(data)>0:
            QCFailedTotalEntries = len(data)
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)                   
        else:
            QCFailedTotalEntries = 0     
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)
        return QCFailedTotalEntries
 
    def QCFailedExcelViewAll():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        QCFailedLogical_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI ;", conn)
        conn.commit()
        conn.close()
        ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF)

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def Export_FailedLogicalVariablesCSV():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        QCFailedLogical_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI ;", conn)
        conn.commit()
        conn.close()
        if len(QCFailedLogical_DF) >0:
            Export_MasterTB_DF  = pd.DataFrame(QCFailedLogical_DF)
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
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        SetCatchQCFailedDB_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI ;", conn)
        conn.commit()
        conn.close()
        SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int)
        SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int)
        SetCatchQCFailedDB_DF['DeploymentUID'] = (SetCatchQCFailedDB_DF.loc[:,['DeploymentUID']]).astype(str)
        SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
        SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
        return SetCatchQCFailedDB_DF

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
        QcMessage = 'Run SetCatch DB Search For DeploymentNumber : '
        curItems = tree1.selection()
        if len(curItems)==1:
            sd = tree1.item(curItems, 'values')
            SelvariableIdentifier = sd[2]
            get_Search_Split = SelvariableIdentifier.split("-")
            get_DepNum_Search =get_Search_Split[2]
            entry_DepNumforSearch.insert(tk.END,get_DepNum_Search)
            txtDisplayMessageSystem.insert(tk.END,(QcMessage + get_DepNum_Search))
        len_curItems = len(curItems)
        if len_curItems < 20001:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,len_curItems)
        else:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,'MaxLimit Exceed')
    
    def SetcatchDB_VariableList():
        GetSetCatchDB_VariableList = ['KeptWeight','DiscardWeight','NumberIndividuals']
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
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET KeptWeight = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DiscardWeight = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberIndividuals = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
 
        ### Updating QC Failed DB
        GetQCFailed_VariableList = ['KeptWeight','DiscardWeight','NumberIndividuals']
        if (get_Updated_Variable == GetQCFailed_VariableList[0]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI \
                                               SET KeptWeight =  ?\
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                               UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI SET QCMessage =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)

        if (get_Updated_Variable == GetQCFailed_VariableList[1]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI \
                                               SET DiscardWeight = ?  \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI SET QCMessage =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[2]):
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI \
                                               SET NumberIndividuals = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI SET QCMessage =? \
                                                WHERE DeploymentUID =?", 
                                                UpdateQCMsg_QCFailDB)
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Logical.commit()
        conn_Validation_Logical.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_String7 =['DeploymentUID']
            Var_Class_IntB27  = ['KeptWeight','DiscardWeight','NumberIndividuals']
            ReturnFail ="ReturnFail"

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

    def GenSummaryQC():
        ListVariables = ['KeptWeight','DiscardWeight','NumberIndividuals']
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI ;", conn)
        conn.commit()
        conn.close()
        if len(Complete_df) >0:
            SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
            QCFailVarAppend = []
            QCFailNonBlankCount = []
            for List in ListVariables:
                NonBlankCount = len((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[List]!='']))
                ListName = str(List)
                NonBlankCount = str (NonBlankCount) 
                QCFailVarAppend.append(ListName)
                QCFailNonBlankCount.append(NonBlankCount)
            QCFailAppend = {'QCVariableName': QCFailVarAppend, 'NonBlankCount': QCFailNonBlankCount} 
            QCFailSummaryDF = pd.DataFrame(QCFailAppend)
            QCFailSummaryDF['RecordType'] = 1
            QCFailSummaryDF[['RecordType']] = QCFailSummaryDF[['RecordType']].astype(int)
            QCFailSummaryDF[['NonBlankCount']] = QCFailSummaryDF[['NonBlankCount']].astype(int)
            QCFailSummaryDF.sort_values(by=['NonBlankCount'], inplace=True, ascending=False)
            QCFailSummaryDF = QCFailSummaryDF.reset_index(drop=True)
            QCFailSummaryDF = QCFailSummaryDF.loc[:,['QCVariableName','RecordType','NonBlankCount']]
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
            messagebox.showinfo('Empty Database', "Empty Database Nothing to Generate")
       
    def InventoryRec3(event):
        ListVariableName = ['KeptWeight','DiscardWeight','NumberIndividuals']
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI ;", conn)
        conn.commit()
        conn.close()
        if len(Complete_df) > 0:
            SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
            nm = Summaryframetree.selection()
            if len(nm) ==1:
                sd = Summaryframetree.item(nm, 'values')
                SelvariableIdentifier = sd[0]
                entry_SelQCVariable.delete(0,END)
                entry_SelQCVariable.insert(tk.END, (SelvariableIdentifier))

                if SelvariableIdentifier == ListVariableName[0]:
                    tree1.delete(*tree1.get_children())
                    SetCatchQCFailedDB_DF = ((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[SelvariableIdentifier]!='']))
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    countIndex1 = 0
                    for each_rec in range(len(SetCatchQCFailedDB_DF)):
                        if countIndex1 % 2 == 0:
                            tree1.insert("", tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    tree1.tag_configure("even",foreground="black", background="lightgreen")
                    tree1.tag_configure("odd",foreground="black", background="ghost white")
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'For RecordType1 @ Each Set KeptWeight Must be Blank')
                
                if SelvariableIdentifier == ListVariableName[1]:
                    tree1.delete(*tree1.get_children())
                    SetCatchQCFailedDB_DF = ((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[SelvariableIdentifier]!='']))
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    countIndex1 = 0
                    for each_rec in range(len(SetCatchQCFailedDB_DF)):
                        if countIndex1 % 2 == 0:
                            tree1.insert("", tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    tree1.tag_configure("even",foreground="black", background="lightgreen")
                    tree1.tag_configure("odd",foreground="black", background="ghost white")
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'For RecordType1 @ Each Set DiscardWeight Must be Blank')
            
                if SelvariableIdentifier == ListVariableName[2]:
                    tree1.delete(*tree1.get_children())
                    SetCatchQCFailedDB_DF = ((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[SelvariableIdentifier]!='']))
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    countIndex1 = 0
                    for each_rec in range(len(SetCatchQCFailedDB_DF)):
                        if countIndex1 % 2 == 0:
                            tree1.insert("", tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    tree1.tag_configure("even",foreground="black", background="lightgreen")
                    tree1.tag_configure("odd",foreground="black", background="ghost white")
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'For RecordType1 @ Each Set NumberIndividuals Must be Blank')

            else:
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(tk.END, (' Please Select Only One Entries To View'))
                txtDisplayMessageSystem.insert(1, 'For RecordType1 @ Each Set KeptWeight, DiscardWeight, NumberIndividuals Must be Blank')
    
    def ClearSummary():
        SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
        Summaryframetree.delete(*Summaryframetree.get_children())
        entry_SelQCVariable.delete(0,END)
        entry_SelQCVariable.insert(tk.END,'QC Variable')

    def ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF):
        if len(QCFailedLogical_DF) >0:
            QCFailedLogical_DF.sort_values(by=['DeploymentUID', 'DeploymentNumber','SetNumber',
                                                    'RecordType'], inplace=True)
            QCFailedLogical_DF  = QCFailedLogical_DF.reset_index(drop=True)
            QCFailedLogical_DF  = pd.DataFrame(QCFailedLogical_DF)   
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0,'Viewing QC Failed Excel File In Seperate Window')
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = QCFailedLogical_DF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(QCFailedLogical_DF),2), clr='lightblue', cols='all')
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
                    'NumberSpecies', 'SpeciesCode','KeptWeight',
                    'DiscardWeight','NumberIndividuals']]).replace(['',None, np.nan], 99999999)
                Complete_df[['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber','SetNumber','RecordType',
                            'NumberSpecies', 'SpeciesCode',
                            'KeptWeight','DiscardWeight','NumberIndividuals']] = Complete_df[
                            ['DataBase_ID','RecordIdentifier',
                            'DeploymentNumber','SetNumber','RecordType',
                            'NumberSpecies', 'SpeciesCode',
                            'KeptWeight','DiscardWeight','NumberIndividuals']].astype(int)
                Complete_df = Complete_df.replace([99999999, 99999999.0], '')
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
                UpdatedQCFailedDB =[]
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
                    list_item_KeptWeight = (rowValue[8])
                    list_item_DiscardWeight = (rowValue[9])
                    list_item_NumberIndividuals = (rowValue[10])
                    list_item_QCMessage = ''
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_RecordType,
                                        list_item_NumberSpecies,
                                        list_item_SpeciesCode,
                                        list_item_KeptWeight,
                                        list_item_DiscardWeight,
                                        list_item_NumberIndividuals,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                    
                    UpdatedQCFailedDB.append((
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_RecordType,
                                        list_item_NumberSpecies,
                                        list_item_SpeciesCode,
                                        list_item_KeptWeight,
                                        list_item_DiscardWeight,
                                        list_item_NumberIndividuals,
                                        list_item_QCMessage,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                                
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ?, \
                                    SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                    SpeciesCode = ?, KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?\
                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    UpdateRecordList_SetCatchDB)
                
                cur_DB_SetCatch_Validation_Logical.executemany("UPDATE SetCatch_QCFailedLogical_RecType_KW_DW_NI SET DeploymentNumber = ?, \
                                        SetNumber = ?, RecordType = ?, NumberSpecies = ?,\
                                        SpeciesCode = ?, KeptWeight = ?, DiscardWeight = ?,\
                                        NumberIndividuals = ?, QCMessage = ? \
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdatedQCFailedDB)
                                            
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

    def callbackFuncSelectView(event):
        ListVariableListA = ['Select Logical QC Variable From DropDown & Run Selected Button', 
                         'KeptWeight & DiscardWeight & NumberIndividuals - RecType1 @ Each Set']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            tree1.delete(*tree1.get_children())
            
        if(SelVariableView ==ListVariableListA[0]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Select Variable & Run View Selected QC Button')
            
        if(SelVariableView ==ListVariableListA[1]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'For RecordType1 @ Each Set KeptWeight, DiscardWeight & NumberIndividuals Must Be Blank')

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
                    'NumberSpecies', 'SpeciesCode','KeptWeight',
                    'DiscardWeight','NumberIndividuals']])
                QCFailedLogical_DF  = pd.DataFrame(rows)
                ExcelViewEditBackend_RecType_1_2(QCFailedLogical_DF)

    def GenDeploymentSummary():
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        ListVariableName = ['KeptWeight','DiscardWeight','NumberIndividuals']
        getVarnameToView = entry_SelQCVariable.get()
        if getVarnameToView in (ListVariableName):
            conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI ;", conn)
            conn.commit()
            conn.close()
            ## For KeptWeight
            if getVarnameToView == ListVariableName[0]:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
                SetCatchQCFailedDB_DF = ((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[getVarnameToView]!='']))
                SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                if len(SetCatchQCFailedDB_DF) >0:
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                    'DeploymentUID']]
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
                    Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                        SetCatchQCFailedDB_DF, 
                        on = ['DataBase_ID','RecordIdentifier','DeploymentUID'], indicator=True, 
                        how='outer').query('_merge == "both"')
                    
                    Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['ASOCCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['Year'] = (Ref_FailedQC_InSetcatchDB.loc[:,['Year']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['DeploymentNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DeploymentNumber']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['SetNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['SetNumber']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['RecordType'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordType']]).astype(int, errors='ignore')
                    
                    Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
                    Complete_df  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
                    Complete_df = Complete_df.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                    'Year','ASOCCode', 'DeploymentNumber', 'RecordType']]
                    Complete_df = Complete_df[(Complete_df.RecordType) == 1]
                    Complete_df.sort_values(
                        by=['Year','ASOCCode', 'DeploymentNumber'], inplace=True)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.groupby(
                        ['Year', 'ASOCCode','DeploymentNumber', 'RecordType'],  
                        as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(x)))
                    SetCatchQCFailedDB_DF.sort_values(
                        by=['Year', 'ASOCCode','DeploymentNumber'], inplace=True)
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF = pd.DataFrame(SetCatchQCFailedDB_DF)
                    countIndex1 = 0
                    for each_rec in range(len(SetCatchQCFailedDB_DF)):
                        if countIndex1 % 2 == 0:
                            SelResultOverviewtree.insert("", 
                            tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("even",))
                        else:
                            SelResultOverviewtree.insert("", 
                            tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    SelResultOverviewtree.tag_configure("even",foreground="black", background="lightblue")
                    SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
                else:
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(tk.END,"Empty QC Fail - No Fail Found")
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())  

            if getVarnameToView == ListVariableName[1]:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
                SetCatchQCFailedDB_DF = ((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[getVarnameToView]!='']))
                SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                if len(SetCatchQCFailedDB_DF) >0:
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                    'DeploymentUID']]
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
                    Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                        SetCatchQCFailedDB_DF, 
                        on = ['DataBase_ID','RecordIdentifier','DeploymentUID'], indicator=True, 
                        how='outer').query('_merge == "both"')
                    
                    Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['ASOCCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['Year'] = (Ref_FailedQC_InSetcatchDB.loc[:,['Year']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['DeploymentNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DeploymentNumber']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['SetNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['SetNumber']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['RecordType'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordType']]).astype(int, errors='ignore')
                    
                    Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
                    Complete_df  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
                    Complete_df = Complete_df.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                    'Year','ASOCCode', 'DeploymentNumber', 'RecordType']]
                    Complete_df = Complete_df[(Complete_df.RecordType) == 1]
                    Complete_df.sort_values(
                        by=['Year','ASOCCode', 'DeploymentNumber'], inplace=True)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.groupby(
                        ['Year', 'ASOCCode','DeploymentNumber', 'RecordType'],  
                        as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(x)))
                    SetCatchQCFailedDB_DF.sort_values(
                        by=['Year', 'ASOCCode','DeploymentNumber'], inplace=True)
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF = pd.DataFrame(SetCatchQCFailedDB_DF)
                    countIndex1 = 0
                    for each_rec in range(len(SetCatchQCFailedDB_DF)):
                        if countIndex1 % 2 == 0:
                            SelResultOverviewtree.insert("", 
                            tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("even",))
                        else:
                            SelResultOverviewtree.insert("", 
                            tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    SelResultOverviewtree.tag_configure("even",foreground="black", background="lightblue")
                    SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
                else:
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(tk.END,"Empty QC Fail - No Fail Found")
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())  

            if getVarnameToView == ListVariableName[2]:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
                SetCatchQCFailedDB_DF = ((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[getVarnameToView]!='']))
                SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                if len(SetCatchQCFailedDB_DF) >0:
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                    'DeploymentUID']]
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
                    Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                        SetCatchQCFailedDB_DF, 
                        on = ['DataBase_ID','RecordIdentifier','DeploymentUID'], indicator=True, 
                        how='outer').query('_merge == "both"')
                    
                    Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['ASOCCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['Year'] = (Ref_FailedQC_InSetcatchDB.loc[:,['Year']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['DeploymentNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DeploymentNumber']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['SetNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['SetNumber']]).astype(int, errors='ignore')
                    Ref_FailedQC_InSetcatchDB['RecordType'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordType']]).astype(int, errors='ignore')
                    
                    Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
                    Complete_df  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
                    Complete_df = Complete_df.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                    'Year','ASOCCode', 'DeploymentNumber', 'RecordType']]
                    Complete_df = Complete_df[(Complete_df.RecordType) == 1]
                    Complete_df.sort_values(
                        by=['Year','ASOCCode', 'DeploymentNumber'], inplace=True)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.groupby(
                        ['Year', 'ASOCCode','DeploymentNumber', 'RecordType'],  
                        as_index=False)['DeploymentUID'].apply(lambda x: (np.count_nonzero(x)))
                    SetCatchQCFailedDB_DF.sort_values(
                        by=['Year', 'ASOCCode','DeploymentNumber'], inplace=True)
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF = pd.DataFrame(SetCatchQCFailedDB_DF)
                    countIndex1 = 0
                    for each_rec in range(len(SetCatchQCFailedDB_DF)):
                        if countIndex1 % 2 == 0:
                            SelResultOverviewtree.insert("", 
                            tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("even",))
                        else:
                            SelResultOverviewtree.insert("", 
                            tk.END, values=list(SetCatchQCFailedDB_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    SelResultOverviewtree.tag_configure("even",foreground="black", background="lightblue")
                    SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
                else:
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(tk.END,"Empty QC Fail - No Fail Found")
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())  

    # Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    # SelResultOverviewtree.bind('<<TreeviewSelect>>',InventoryRec4)
    ## ComboBox Select
    entry_UpdateVariableList.bind('<<ComboboxSelected>>', callbackFuncSelectVariable1)
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ## Gen QC Summary
    GenSummaryQC()
    QCFailedTotalEntries()

    # SelectViewResultsRun Button
    btnViewQCFailedQCResults = Button(SelectViewResultsRun, text="View Selected Results", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=18, bd=1, command = viewQCFailed_VariablesProfile)
    btnViewQCFailedQCResults.grid(row =0, column = 1, padx=2, pady =2, ipady =2, sticky =W)

    btnSearchDepSetCatchDB = Button(SelectViewResultsRun, text="Search Deployment From Set&Catch DB", 
                            font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=34, bd=1, command = SearchDepNumFromSetCatchDB)
    btnSearchDepSetCatchDB.grid(row =0, column = 3, padx=122, pady =2, ipady =2, sticky =W)
    
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

    button_ClrSelView = Button(SummaryDisplay, bd = 1, text ="Clear Summary", width = 13,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearSummary)
    button_ClrSelView.pack(side =TOP, anchor = W)

    button_GenDepQCSummary = Button(SelQCVariableDisplay, bd = 1, text ="Deployment Summary From Set&Catch DB", width = 36,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenDeploymentSummary)
    button_GenDepQCSummary.grid(row =0, column = 1, padx=10, pady =2, ipady =2, sticky =W)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    ImportExport  = Menu(menu, tearoff=0)
    View  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Import/Export", menu=ImportExport)
    menu.add_cascade(label="View", menu=View)     
    filemenu.add_command(label="Exit", command=iExit)
    ImportExport.add_command(label="Export Failed Results (.csv)", command=Export_FailedLogicalVariablesCSV)
    ImportExport.add_command(label="Import & Update DB (.csv)", command=ImportAndUpdateSetCatchDB)
    View.add_command(label="View QC Failed All Results", command=QCFailedExcelViewAll)
    View.add_command(label="Ref-QCFail To Set&Catch DB", command=RefFailedToSetcatchDB)
    
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack(side = LEFT)
    window.mainloop()



