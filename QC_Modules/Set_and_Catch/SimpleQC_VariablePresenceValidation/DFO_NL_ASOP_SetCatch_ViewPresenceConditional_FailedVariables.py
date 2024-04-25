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
DB_SetCatch_Validation_Presence = ("./BackEnd/Sqlite3_DB/QC_Check_PresenceConsistency_DB/DFO_NL_ASOP_SetCatch_PresenceValidation.db")

from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation \
import DFO_NL_ASOP_ExcelViewPresenceConditional_FailedVariables as ExcelView_DeploymentSearch

def ViewPresenceConditionalValidatedResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Presence Validator ID-C-03-1")
    window.geometry("1300x805+200+100")
    window.config(bg="cadet blue")

    ## Top Frame
    TopFrame = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    TopFrame.pack(side = TOP, padx= 0, pady=0)
    lbl_TopFrame = Label(TopFrame, font=('aerial', 10, 'bold'), bg= "cadet blue", text="A. QC Fail Table (Presence) :")
    lbl_TopFrame.grid(row =1, column = 0, padx=2, pady =1, ipady=1, sticky =W)

    ListVariableListA = ['Select Variable & Run View Selected QC Button', 'AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                        'NumberGillnets','AverageGillnetLength','NumberHooks', 'NumberWindows', 'NumberPots']
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

    lbl_TotalFailedEntries = Label(TopFrame, font=('aerial', 10 , 'bold'), text="# Of QC Failed :")
    lbl_TotalFailedEntries.grid(row =0, column = 0, padx=1, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(TopFrame, value='')
    txtTotalFailedEntries = Entry(TopFrame, font=('aerial',12),textvariable = TotalFailedEntries, width = 8, bd=1)
    txtTotalFailedEntries.grid(row =0, column = 0, padx=120, pady =1, ipady =1, sticky =W)

    txtDisplayMessageSystem = Entry(TopFrame, font=('aerial', 9), justify='center',
                            textvariable = StringVar(window, value='QC Message Display'), width = 84, bd=2)
    txtDisplayMessageSystem.grid(row =0, column = 1, padx=40, pady =2, ipady =5, sticky =W)

    Tableframe = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Tableframe.pack(side = TOP, padx= 0, pady=0)

    ### Define Table Frame And TreeView1
    Tableframe = Frame(window, width = 40)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", "column4", 
                    "column5", "column6",  "column7",  "column8"), height=21, show='headings')
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
    tree1.heading("#5", text="GearType", anchor=CENTER)
    tree1.heading("#6", text="Value Of Selected QC Variable ↑↑↑", anchor=CENTER)
    tree1.heading("#7", text="QC Message On Selected Variable", anchor=CENTER)
    tree1.heading("#8", text="QC_CaseType", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=350, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=490, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=170, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)

    ## Frame Of update modules
    UpdateDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    UpdateDB_Entryframe.pack(side =LEFT, padx=10, pady =2)
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
    NumberRowSelected       = IntVar(UpdateDB_Entryframe, value ='# Row Selected')
    entry_NumberRowSelected = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), justify='center',
                                textvariable = NumberRowSelected, width = 15, bd=1)
    entry_NumberRowSelected.grid(row =4, column = 0, padx=2, pady =4, ipady =4, sticky =E)

    lbl_Select_List_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 2. Select Variable :")
    lbl_Select_List_Variable.grid(row =6, column = 0, padx=2, pady =2, sticky =W)

    ListUpdateVar = ['AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                     'NumberGillnets','AverageGillnetLength',
                     'NumberHooks','NumberWindows', 'NumberPots',
                     'GearType']
    UpdateVar = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = UpdateVar, width = 24, state='readonly')
    entry_UpdateVariableList.grid(row =8, column = 0, padx=50, pady =2, ipady= 2, sticky =W)
    entry_UpdateVariableList['values'] = sorted(list(ListUpdateVar))

    lbl_EntryUpdate_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 3. Enter Updated Value :")
    lbl_EntryUpdate_Variable.grid(row =10, column = 0, padx=2, pady =2, sticky =W)
    
    UpdateValue_VariableA       = IntVar(UpdateDB_Entryframe, value ='')
    entry_UpdateValue_VariableA = Entry(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = UpdateValue_VariableA, width = 25, bd=2)
    entry_UpdateValue_VariableA.grid(row =12, column = 0, padx=50, pady =2, ipady =2, sticky =W)

    ## ####Frame Of search modules ###
    SearchDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SearchDB_Entryframe.pack(side =LEFT, padx=10, pady =2)

    lbl_SearchDB_Header = Label(SearchDB_Entryframe, font=('aerial', 12, 'bold','underline'), 
                                bg= "cadet blue", text="Search Database:")
    lbl_SearchDB_Header.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_SelectSinglevariableSearch_A = Label(SearchDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Variable :")
    lbl_SelectSinglevariableSearch_A.grid(row =3, column = 0, padx=2, pady =1, ipady= 4, sticky =W)
    
    ListVariableSearch = ['AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                        'NumberGillnets','AverageGillnetLength','NumberHooks','NumberWindows', 'NumberPots']
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

    ###### SummaryQCframe Generate QC Failed Summary ###
    SummaryQCframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.pack(side =LEFT, padx=10, pady =2)
    
    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    Summaryframetree = ttk.Treeview(Summaryframe, column=("column1", "column2", "column3"),height=9, show='headings')
    scrollbary = ttk.Scrollbar(Summaryframe, orient ="vertical", command=Summaryframetree.yview)
    scrollbary.pack(side ='right', fill ='y')
    Summaryframetree.configure(yscrollcommand = scrollbary.set)
    Summaryframetree.heading("#1", text="QC Variable", anchor = W)
    Summaryframetree.heading("#2", text="Fail Count")
    Summaryframetree.heading("#3", text="Update Count")
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=140, anchor = W)            
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    Summaryframetree.column('#3', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    Summaryframetree.pack(side = BOTTOM)
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    SelectViewFilter = ['RecType-1&2', 'RecType 1 Only']
    SelectFilterView        = StringVar(SummaryDisplay, value ='')
    entry_SelectFilterView  = ttk.Combobox(SummaryDisplay, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable =SelectFilterView, width = 15, state='readonly')
    entry_SelectFilterView.pack(side =RIGHT, anchor = E)
    entry_SelectFilterView['values'] = SelectViewFilter
    entry_SelectFilterView.current(1)
    SummaryDisplay.pack(side = LEFT, pady=0)

    # Define TreeView SelResultOverviewtree
    SelQCVariableDisplay = tk.Frame(window, bg= "aliceblue")
    SelQCVariable      = StringVar(SelQCVariableDisplay, value ='QC Variable')
    entry_SelQCVariable = Entry(SelQCVariableDisplay, font=('aerial', 10, 'bold'),  justify = tk.CENTER,
                            textvariable = SelQCVariable, width = 18, bd=2)
    entry_SelQCVariable.grid(row =0, column = 0, padx=2, pady =2, ipady =2, sticky =W)

    SelQCVariableDisplay.pack(side = TOP, pady=0, anchor = CENTER)
    SelResultOverview = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SelResultOverview.pack(side =LEFT, padx=2, pady =2)
    SelResultOverviewtree = ttk.Treeview(SelResultOverview,  
                            column=("column1", "column2", 
                                    "column3", "column4" 
                                    ), height=9, show='headings')
    scrollbary = ttk.Scrollbar(SelResultOverview, orient ="vertical", command=SelResultOverviewtree.yview)
    scrollbary.pack(side ='right', fill ='y')
    SelResultOverviewtree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(SelResultOverview, orient ="horizontal", command=SelResultOverviewtree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    SelResultOverviewtree.configure(xscrollcommand = scrollbarx.set)
    SelResultOverviewtree.heading("#1", text="Year", anchor=CENTER)
    SelResultOverviewtree.heading("#2", text="ASOC", anchor=CENTER)
    SelResultOverviewtree.heading("#3", text="Dep#", anchor=CENTER)
    SelResultOverviewtree.heading("#4", text="# Of Fail", anchor=CENTER)
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)             
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)
    SelResultOverviewtree.column('#4', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = BOTTOM)
    
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType','AverageTowSpeed','CodendMeshSize', 
                            'MeshSizeMG', 'NumberGillnets',  'AverageGillnetLength',
                            'NumberHooks', 'NumberWindows', 'NumberPots',
                            'QCAverageTowSpeed','QCCodendMeshSize','QCMeshSizeMG',
                            'QCNumberGillnets','QCAverageGillnetLength','QCNumberHooks',
                            'QCNumberWindows', 'QCNumberPots']
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
            return ReturnMatchedMessage
        else: 
            return ReturnMisMatchedMessage

    def ImportAndUpdateSetCatchDB():
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        conn_DB_SetCatch_Validation_Presence= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur_DB_SetCatch_Validation_Presence=conn_DB_SetCatch_Validation_Presence.cursor()
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
                        RecordType                  = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        GearType                    = (df.loc[:,'GearType']).fillna(99999999).astype(int, errors='ignore')
                        AverageTowSpeed             = (df.loc[:,'AverageTowSpeed']).fillna(99999999).astype(float, errors='ignore')
                        CodendMeshSize              = (df.loc[:,'CodendMeshSize']).fillna(99999999).astype(str, errors='ignore')
                        MeshSizeMG                  = (df.loc[:,'MeshSizeMG']).fillna(99999999).astype(int, errors='ignore')
                        NumberGillnets              = (df.loc[:,'NumberGillnets']).fillna(99999999).astype(int, errors='ignore')
                        AverageGillnetLength        = (df.loc[:,'AverageGillnetLength']).fillna(99999999).astype(int, errors='ignore')
                        NumberHooks                 = (df.loc[:,'NumberHooks']).fillna(99999999).astype(int, errors='ignore')
                        NumberWindows               = (df.loc[:,'NumberWindows']).fillna(99999999).astype(int, errors='ignore')
                        NumberPots                  = (df.loc[:,'NumberPots']).fillna(99999999).astype(int, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID,RecordType,\
                                        GearType,AverageTowSpeed, CodendMeshSize,\
                                        MeshSizeMG, NumberGillnets,  AverageGillnetLength,\
                                        NumberHooks, NumberWindows, NumberPots]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns=  {0:'DataBase_ID',1: 'RecordIdentifier',2: 'DeploymentUID', 3:'RecordType',
                                                4:'GearType',   5:'AverageTowSpeed',  6:'CodendMeshSize', 
                                                7:'MeshSizeMG', 8:'NumberGillnets',   9:'AverageGillnetLength', 
                                                10:'NumberHooks', 11:'NumberWindows',  12: 'NumberPots'},inplace = True)
                        Raw_Imported_Df = pd.DataFrame(catdf)
                        Raw_Imported_Df = Raw_Imported_Df.replace('     ', 99999999)
                        Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0, '.'], '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([8888888, '8888888', '.','99999999'], 'None')
                        Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                        Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                        CheckEmptyNessColumn = Raw_Imported_Df[
                                            (Raw_Imported_Df.DataBase_ID=='') |
                                            (Raw_Imported_Df.RecordIdentifier=='') |
                                            (Raw_Imported_Df.DeploymentUID=='None') |
                                            (Raw_Imported_Df.DeploymentUID=='') |
                                            (Raw_Imported_Df.RecordType=='') |
                                            (Raw_Imported_Df.GearType=='')
                                            ]
                    Len_CheckEmptyNessColumn =len(CheckEmptyNessColumn)
                    if Len_CheckEmptyNessColumn==0:
                        Length_Raw_Imported_Df  =  len(Raw_Imported_Df)
                        if Length_Raw_Imported_Df <250000:
                            UpdateRecordList_SetCatchDB =[]
                            UpdateAverageTowSpeedDB_Failed =[]
                            UpdateCodendMeshSizeDB_Failed =[]
                            UpdateMeshSizeMGDB_Failed =[]
                            UpdateNumberGillnetsDB_Failed =[]
                            UpdateAverageGillnetLengthDB_Failed =[]
                            UpdateNumberHooksDB_Failed =[]
                            UpdateNumberWindowsDB_Failed =[]
                            UpdateNumberPotsDB_Failed =[]

                            df_rows = Raw_Imported_Df.to_numpy().tolist()
                            for row in df_rows:
                                rowValue = row
                                list_item_DataBase_ID = int(rowValue[0])
                                list_item_RecordIdentifier = int(rowValue[1])
                                list_item_DeploymentUID = (rowValue[2])
                                list_item_RecordType = (rowValue[3])
                                list_item_GearType = (rowValue[4])
                                list_item_AverageTowSpeed = (rowValue[5])
                                list_item_CodendMeshSize = (rowValue[6])
                                list_item_MeshSizeMG = (rowValue[7])
                                list_item_NumberGillnets = (rowValue[8])
                                list_item_AverageGillnetLength = (rowValue[9])
                                list_item_NumberHooks = (rowValue[10])
                                list_item_NumberWindows = (rowValue[11])
                                list_item_NumberPots = (rowValue[12])
                                list_item_QC_CaseType = 'Case-Updated'
                                
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_AverageTowSpeed,
                                                    list_item_CodendMeshSize,
                                                    list_item_MeshSizeMG,
                                                    list_item_NumberGillnets,
                                                    list_item_AverageGillnetLength,
                                                    list_item_NumberHooks,
                                                    list_item_NumberWindows,
                                                    list_item_NumberPots,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                UpdateAverageTowSpeedDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_AverageTowSpeed,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                UpdateCodendMeshSizeDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_CodendMeshSize,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                UpdateMeshSizeMGDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_MeshSizeMG,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                UpdateNumberGillnetsDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_NumberGillnets,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                UpdateAverageGillnetLengthDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_AverageGillnetLength,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                UpdateNumberHooksDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_NumberHooks,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))

                                UpdateNumberWindowsDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_NumberWindows,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))

                                UpdateNumberPotsDB_Failed.append((
                                                    list_item_RecordType,
                                                    list_item_GearType,
                                                    list_item_NumberPots,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))                                
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ?, GearType = ?, \
                                                    AverageTowSpeed = ?, CodendMeshSize = ?, MeshSizeMG = ?, NumberGillnets = ?,\
                                                    AverageGillnetLength = ?, NumberHooks = ?, NumberWindows = ?, NumberPots = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageTowSpeed SET RecordType = ?, GearType = ?, \
                                                    AverageTowSpeed = ?,  QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateAverageTowSpeedDB_Failed)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_CodendMeshSize SET RecordType = ?, GearType = ?, \
                                                    CodendMeshSize = ?,  QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateCodendMeshSizeDB_Failed)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MeshSizeMG SET RecordType = ?, GearType = ?, \
                                                    MeshSizeMG = ?, QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateMeshSizeMGDB_Failed)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberGillnets SET RecordType = ?, GearType = ?, \
                                                    NumberGillnets = ?, QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateNumberGillnetsDB_Failed)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageGillnetLength SET RecordType = ?, GearType = ?, \
                                                    AverageGillnetLength = ?, QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateAverageGillnetLengthDB_Failed)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberHooks SET RecordType = ?, GearType = ?, \
                                                    NumberHooks = ?, QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateNumberHooksDB_Failed)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberWindows SET RecordType = ?, GearType = ?, \
                                                    NumberWindows = ?, QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateNumberWindowsDB_Failed)
                            
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberPots SET RecordType = ?, GearType = ?, \
                                                    NumberPots = ?, QC_CaseType = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateNumberPotsDB_Failed)

                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Presence.commit()
                            conn_DB_SetCatch_Validation_Presence.close()
                            txtDisplayMessageSystem.delete(0,END)
                            txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                            tkinter.messagebox.showinfo("Finished Update","Successfully Finished Update")
                    else:
                        messagebox.showerror('Empty Variables', "Please Check Null Variables (DataBase_ID, RecordIdentifier, DeploymentUID,\
                                        GearType) Input")

    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def ClearTablesAll():
        tree1.delete(*tree1.get_children())
        txtTotalFailedEntries.delete(0,END)
        entry_ViewVarResults.current(0)
        txtDisplayMessageSystem.delete(0,END)

    def ClearUpdateEntries():
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateValue_VariableA.delete(0,END)
        entry_NumberRowSelected.delete(0,END)
        entry_UpdateVariableList.set('')
        entry_NumberRowSelected.insert(0, '# Row Selected')
        entry_EntryDataType_Variable.insert(0, 'Variable Type')  

    def ClearSearchEntries():
        entry_SearchVariableList.set('')
        entry_SearchValue_Variable_A.set('')
        txtTotalSearchEntries.delete(0,END)
    
    def viewQCFailed(getVarnameToView):
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Presence)
            cur=con.cursor()
            if getVarnameToView == "AverageTowSpeed":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == "CodendMeshSize":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == "MeshSizeMG":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == "NumberGillnets":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == "AverageGillnetLength":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == "NumberHooks":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == "NumberWindows":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows ORDER BY `DataBase_ID` ASC")
            if getVarnameToView == "NumberPots":
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberPots ORDER BY `DataBase_ID` ASC")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows)
            rows = rows.reset_index(drop=True)
            rows.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 
                                 2:'DeploymentUID', 3:'RecordType',
                                 4:'GearType', 5: getVarnameToView, 
                                 6:'QC_Message', 7:'QC_CaseType'
                                 },inplace = True)
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_VariablesProfile():
        ListVariableListA = ['Select Variable & Run View Selected QC Button', 
                             'AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                             'NumberGillnets','AverageGillnetLength','NumberHooks', 
                             'NumberWindows', 'NumberPots']
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        if len(rows) >0 :
            rows.sort_values(by=['DeploymentUID','RecordType'], inplace=True)
            rows  = rows.reset_index(drop=True)
            rows  = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[0]:
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(0, 'Select Presence View Type From DropDown & Run View Selected Button')
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
                txtDisplayMessageSystem.insert(0, 'Populated ' + getVarnameToView + ' Presence Fail Entries')
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 'Empty QC Fail DB. Nothing to Display')

    def QCFailedExcelViewAll():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        cursor = conn.cursor()
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF['DataBase_ID'] = (SetCatchProfileDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['RecordIdentifier'] = (SetCatchProfileDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        AverageTowSpeed_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed ORDER BY `DataBase_ID` ASC ;", conn)
        CodendMeshSize_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize ORDER BY `DataBase_ID` ASC ;", conn)
        MeshSizeMG_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG ORDER BY `DataBase_ID` ASC ;", conn)
        NumberGillnets_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets ORDER BY `DataBase_ID` ASC ;", conn)
        AverageGillnetLength_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength ORDER BY `DataBase_ID` ASC ;", conn)
        NumberHooks_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks ORDER BY `DataBase_ID` ASC ;", conn)
        NumberWindows_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows ORDER BY `DataBase_ID` ASC ;", conn)
        NumberPots_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots ORDER BY `DataBase_ID` ASC ;", conn)
        conn.commit()
        conn.close()
        NumberWindows_df = pd.DataFrame(NumberWindows_df)
        NumberWindows_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberWindows_df  = NumberWindows_df.reset_index(drop=True)
        NumberWindows_df = pd.DataFrame(NumberWindows_df)

        NumberPots_df = pd.DataFrame(NumberPots_df)
        NumberPots_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberPots_df  = NumberPots_df.reset_index(drop=True)
        NumberPots_df = pd.DataFrame(NumberPots_df)

        AverageTowSpeed_df = pd.DataFrame(AverageTowSpeed_df)
        AverageTowSpeed_df.drop(['QC_CaseType'], axis=1, inplace=True)
        AverageTowSpeed_df  = AverageTowSpeed_df.reset_index(drop=True)
        AverageTowSpeed_df = pd.DataFrame(AverageTowSpeed_df)

        CodendMeshSize_df = pd.DataFrame(CodendMeshSize_df)
        CodendMeshSize_df.drop(['QC_CaseType'], axis=1, inplace=True)
        CodendMeshSize_df  = CodendMeshSize_df.reset_index(drop=True)
        CodendMeshSize_df = pd.DataFrame(CodendMeshSize_df)

        MeshSizeMG_df = pd.DataFrame(MeshSizeMG_df)
        MeshSizeMG_df.drop(['QC_CaseType'], axis=1, inplace=True)
        MeshSizeMG_df  = MeshSizeMG_df.reset_index(drop=True)
        MeshSizeMG_df = pd.DataFrame(MeshSizeMG_df)

        NumberGillnets_df = pd.DataFrame(NumberGillnets_df)
        NumberGillnets_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberGillnets_df  = NumberGillnets_df.reset_index(drop=True)
        NumberGillnets_df = pd.DataFrame(NumberGillnets_df)

        AverageGillnetLength_df = pd.DataFrame(AverageGillnetLength_df)
        AverageGillnetLength_df.drop(['QC_CaseType'], axis=1, inplace=True)
        AverageGillnetLength_df  = AverageGillnetLength_df.reset_index(drop=True)
        AverageGillnetLength_df = pd.DataFrame(AverageGillnetLength_df)

        NumberHooks_df = pd.DataFrame(NumberHooks_df)
        NumberHooks_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberHooks_df  = NumberHooks_df.reset_index(drop=True)
        NumberHooks_df = pd.DataFrame(NumberHooks_df)
        
        SetCatchQCFailedDB_DF = pd.merge(pd.merge(NumberGillnets_df, AverageGillnetLength_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID', 'RecordType', 'GearType']), 
                                NumberHooks_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        SetCatchQCFailedDB_DF = pd.merge(pd.merge(SetCatchQCFailedDB_DF, MeshSizeMG_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType']), 
                        CodendMeshSize_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        SetCatchQCFailedDB_DF = pd.merge(pd.merge(SetCatchQCFailedDB_DF, AverageTowSpeed_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType']),
                                NumberWindows_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        SetCatchQCFailedDB_DF = pd.merge(SetCatchQCFailedDB_DF, NumberPots_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        
        SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'QCAverageTowSpeed','QCCodendMeshSize','QCMeshSizeMG',
                                        'QCNumberGillnets','QCAverageGillnetLength','QCNumberHooks',
                                        'QCNumberWindows','QCNumberPots']]
        Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                                    SetCatchQCFailedDB_DF, on = ["DataBase_ID", "RecordIdentifier", "DeploymentUID"], indicator=True, 
                                    how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
        Complete_df  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
        Complete_df = Complete_df.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                         'GearType','AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                                         'NumberGillnets','AverageGillnetLength','NumberHooks', 'NumberWindows', 'NumberPots',
                                         'QCAverageTowSpeed','QCCodendMeshSize','QCMeshSizeMG',
                                         'QCNumberGillnets','QCAverageGillnetLength','QCNumberHooks',
                                         'QCNumberWindows', 'QCNumberPots']]
        Complete_df  = pd.DataFrame(Complete_df)
        Complete_df.sort_values(
            by=['DeploymentUID','RecordType'], inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        QC_FailPresence_DF  = pd.DataFrame(Complete_df)
        ExcelViewEditBackend_RecType_1_2(QC_FailPresence_DF)
                  
    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def Export_FailedCSV():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF['DataBase_ID'] = (SetCatchProfileDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['RecordIdentifier'] = (SetCatchProfileDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        AverageTowSpeed_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed ORDER BY `DataBase_ID` ASC ;", conn)
        CodendMeshSize_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize ORDER BY `DataBase_ID` ASC ;", conn)
        MeshSizeMG_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG ORDER BY `DataBase_ID` ASC ;", conn)
        NumberGillnets_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets ORDER BY `DataBase_ID` ASC ;", conn)
        AverageGillnetLength_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength ORDER BY `DataBase_ID` ASC ;", conn)
        NumberHooks_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks ORDER BY `DataBase_ID` ASC ;", conn)
        NumberWindows_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows ORDER BY `DataBase_ID` ASC ;", conn)
        NumberPots_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots ORDER BY `DataBase_ID` ASC ;", conn)
        conn.commit()
        conn.close()

        NumberWindows_df = pd.DataFrame(NumberWindows_df)
        NumberWindows_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberWindows_df  = NumberWindows_df.reset_index(drop=True)
        NumberWindows_df = pd.DataFrame(NumberWindows_df)

        NumberPots_df = pd.DataFrame(NumberPots_df)
        NumberPots_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberPots_df  = NumberPots_df.reset_index(drop=True)
        NumberPots_df = pd.DataFrame(NumberPots_df)

        AverageTowSpeed_df = pd.DataFrame(AverageTowSpeed_df)
        AverageTowSpeed_df.drop(['QC_CaseType'], axis=1, inplace=True)
        AverageTowSpeed_df  = AverageTowSpeed_df.reset_index(drop=True)
        AverageTowSpeed_df = pd.DataFrame(AverageTowSpeed_df)

        CodendMeshSize_df = pd.DataFrame(CodendMeshSize_df)
        CodendMeshSize_df.drop(['QC_CaseType'], axis=1, inplace=True)
        CodendMeshSize_df  = CodendMeshSize_df.reset_index(drop=True)
        CodendMeshSize_df = pd.DataFrame(CodendMeshSize_df)

        MeshSizeMG_df = pd.DataFrame(MeshSizeMG_df)
        MeshSizeMG_df.drop(['QC_CaseType'], axis=1, inplace=True)
        MeshSizeMG_df  = MeshSizeMG_df.reset_index(drop=True)
        MeshSizeMG_df = pd.DataFrame(MeshSizeMG_df)

        NumberGillnets_df = pd.DataFrame(NumberGillnets_df)
        NumberGillnets_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberGillnets_df  = NumberGillnets_df.reset_index(drop=True)
        NumberGillnets_df = pd.DataFrame(NumberGillnets_df)

        AverageGillnetLength_df = pd.DataFrame(AverageGillnetLength_df)
        AverageGillnetLength_df.drop(['QC_CaseType'], axis=1, inplace=True)
        AverageGillnetLength_df  = AverageGillnetLength_df.reset_index(drop=True)
        AverageGillnetLength_df = pd.DataFrame(AverageGillnetLength_df)

        NumberHooks_df = pd.DataFrame(NumberHooks_df)
        NumberHooks_df.drop(['QC_CaseType'], axis=1, inplace=True)
        NumberHooks_df  = NumberHooks_df.reset_index(drop=True)
        NumberHooks_df = pd.DataFrame(NumberHooks_df)
        
        SetCatchQCFailedDB_DF = pd.merge(pd.merge(NumberGillnets_df, AverageGillnetLength_df, how ='outer', 
                                on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID', 'RecordType', 'GearType']), 
                                NumberHooks_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        SetCatchQCFailedDB_DF = pd.merge(pd.merge(SetCatchQCFailedDB_DF, MeshSizeMG_df, how ='outer', 
                                on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType']), 
                                CodendMeshSize_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        SetCatchQCFailedDB_DF = pd.merge(pd.merge(SetCatchQCFailedDB_DF, AverageTowSpeed_df, how ='outer', 
                                on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType']),
                                NumberWindows_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        SetCatchQCFailedDB_DF = pd.merge(SetCatchQCFailedDB_DF, NumberPots_df, how ='outer', 
                                on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
        
        SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'QCAverageTowSpeed','QCCodendMeshSize','QCMeshSizeMG',
                                'QCNumberGillnets','QCAverageGillnetLength','QCNumberHooks',
                                'QCNumberWindows','QCNumberPots']]
        Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                                    SetCatchQCFailedDB_DF, 
                                    on = ["DataBase_ID", "RecordIdentifier", "DeploymentUID"], indicator=True, 
                                    how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')

        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
        Complete_df  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
        Complete_df = Complete_df.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                         'GearType','AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                                         'NumberGillnets','AverageGillnetLength','NumberHooks', 'NumberWindows', 'NumberPots',
                                         'QCAverageTowSpeed','QCCodendMeshSize','QCMeshSizeMG',
                                         'QCNumberGillnets','QCAverageGillnetLength','QCNumberHooks',
                                         'QCNumberWindows', 'QCNumberPots']]
        Complete_df  = pd.DataFrame(Complete_df)
        Complete_df.sort_values(by=['DeploymentUID','RecordType'], inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        Complete_df  = pd.DataFrame(Complete_df)
        if len(Complete_df) >0:
            Export_MasterTB_DF  = pd.DataFrame(Complete_df)
            Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
            filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                    defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
            if len(filename) >0:
                Export_MasterTB_DF.to_csv(filename,index=None)
                tkinter.messagebox.showinfo("QC Failed Presence Profile","QC Failed Presence Profile Report Saved as CSV")
            else:
                tkinter.messagebox.showinfo("QC Failed Presence Profile Report Message","Please Select File Name To Export")
        else:
            messagebox.showerror('Export Error', "Void File... Nothing to Export")

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn)
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
            conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
            cursor = conn.cursor()
            AverageTowSpeed_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed ORDER BY `DataBase_ID` ASC ;", conn)
            CodendMeshSize_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize ORDER BY `DataBase_ID` ASC ;", conn)
            MeshSizeMG_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG ORDER BY `DataBase_ID` ASC ;", conn)
            NumberGillnets_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets ORDER BY `DataBase_ID` ASC ;", conn)
            AverageGillnetLength_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength ORDER BY `DataBase_ID` ASC ;", conn)
            NumberHooks_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks ORDER BY `DataBase_ID` ASC ;", conn)
            NumberWindows_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows ORDER BY `DataBase_ID` ASC ;", conn)
            NumberPots_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots ORDER BY `DataBase_ID` ASC ;", conn)
            
            AverageTowSpeed_df = pd.DataFrame(AverageTowSpeed_df)
            CodendMeshSize_df = pd.DataFrame(CodendMeshSize_df)
            MeshSizeMG_df = pd.DataFrame(MeshSizeMG_df)
            NumberGillnets_df = pd.DataFrame(NumberGillnets_df)
            AverageGillnetLength_df = pd.DataFrame(AverageGillnetLength_df)
            NumberHooks_df = pd.DataFrame(NumberHooks_df)
            NumberWindows_df = pd.DataFrame(NumberWindows_df)
            NumberPots_df = pd.DataFrame(NumberPots_df) 
            
            SetCatchQCFailedDB_DF = pd.merge(pd.merge(NumberGillnets_df, AverageGillnetLength_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID', 'RecordType', 'GearType']), 
                                NumberHooks_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
            SetCatchQCFailedDB_DF = pd.merge(pd.merge(SetCatchQCFailedDB_DF, MeshSizeMG_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType']), 
                            CodendMeshSize_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
            SetCatchQCFailedDB_DF = pd.merge(pd.merge(SetCatchQCFailedDB_DF, AverageTowSpeed_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType']),
                                    NumberWindows_df, how ='outer', on=['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
            SetCatchQCFailedDB_DF = pd.merge(SetCatchQCFailedDB_DF, NumberPots_df, how ='outer', on= ['DataBase_ID', 'RecordIdentifier','DeploymentUID','RecordType','GearType'])
            
            SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                            'QCAverageTowSpeed','QCCodendMeshSize','QCMeshSizeMG',
                                            'QCNumberGillnets','QCAverageGillnetLength','QCNumberHooks',
                                            'QCNumberWindows','QCNumberPots']]
            if len(SetCatchQCFailedDB_DF) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID']]
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
        GetSetCatchDB_VariableList = ['AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                                    'NumberGillnets','AverageGillnetLength',
                                    'NumberHooks', 'NumberWindows', 'NumberPots',
                                    'GearType']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, UpdateQCFailList,
                                         get_RectypeSelection,UpdateRecordList1,
                                         UpdateQCFailList1, getVarnameToView):
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

        conn_Validation_Presence= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur_Validation_Presence=conn_Validation_Presence.cursor()

        SelectFilterViewList = ['RecType-1&2','RecType 1 Only']
        ListVariableListA = ['AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                             'NumberGillnets','AverageGillnetLength','NumberHooks', 
                             'NumberWindows', 'NumberPots']

        ## Updaing SetCatch DB For RecType-1&2
        if get_RectypeSelection == SelectFilterViewList[0]:
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET CodendMeshSize = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeMG = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberGillnets = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageGillnetLength = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberHooks = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberWindows = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPots = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            ### Updating QC Failed DB

            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageTowSpeed \
                        SET AverageTowSpeed = ?, QC_CaseType = ? \
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateQCFailList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_CodendMeshSize \
                        SET CodendMeshSize = ? , QC_CaseType = ?\
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateQCFailList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MeshSizeMG \
                        SET MeshSizeMG = ? , QC_CaseType = ?\
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateQCFailList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberGillnets \
                        SET NumberGillnets = ? , QC_CaseType = ?\
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateQCFailList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageGillnetLength \
                        SET AverageGillnetLength = ? , QC_CaseType = ?\
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateQCFailList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberHooks \
                        SET NumberHooks = ? , QC_CaseType = ?\
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateQCFailList))
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberWindows \
                        SET NumberWindows = ? , QC_CaseType = ?\
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateQCFailList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberPots \
                        SET NumberPots = ? , QC_CaseType = ?\
                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateQCFailList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                if getVarnameToView == ListVariableListA[0]:
                    cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageTowSpeed \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))
                if getVarnameToView == ListVariableListA[1]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_CodendMeshSize \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))
                if getVarnameToView == ListVariableListA[2]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MeshSizeMG \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))
                if getVarnameToView == ListVariableListA[3]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberGillnets \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))
                if getVarnameToView == ListVariableListA[4]:
                    cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageGillnetLength \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))
                if getVarnameToView == ListVariableListA[5]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberHooks \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))
                if getVarnameToView == ListVariableListA[6]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberWindows \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))
                if getVarnameToView == ListVariableListA[7]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberPots \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                            (UpdateQCFailList))

        if get_RectypeSelection == SelectFilterViewList[1]:
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET CodendMeshSize = ? WHERE DeploymentUID =?", 
                    UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeMG = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberGillnets = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageGillnetLength = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberHooks = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberWindows = ? WHERE DeploymentUID =?", 
                    (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPots = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearType = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            ### Updating QC Failed DB
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageTowSpeed \
                        SET AverageTowSpeed = ?, QC_CaseType = ? \
                        WHERE DeploymentUID =?", 
                        UpdateQCFailList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_CodendMeshSize \
                        SET CodendMeshSize = ? , QC_CaseType = ?\
                        WHERE DeploymentUID =?", 
                        UpdateQCFailList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MeshSizeMG \
                        SET MeshSizeMG = ? , QC_CaseType = ?\
                        WHERE DeploymentUID =?", 
                        UpdateQCFailList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberGillnets \
                        SET NumberGillnets = ? , QC_CaseType = ?\
                        WHERE DeploymentUID =?", 
                        (UpdateQCFailList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageGillnetLength \
                        SET AverageGillnetLength = ? , QC_CaseType = ?\
                        WHERE DeploymentUID =?", 
                        (UpdateQCFailList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberHooks \
                        SET NumberHooks = ? , QC_CaseType = ?\
                        WHERE DeploymentUID =?", 
                        (UpdateQCFailList1))
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberWindows \
                        SET NumberWindows = ? , QC_CaseType = ?\
                        WHERE DeploymentUID =?", 
                        (UpdateQCFailList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberPots \
                        SET NumberPots = ? , QC_CaseType = ?\
                        WHERE DeploymentUID =?", 
                        (UpdateQCFailList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                if getVarnameToView == ListVariableListA[0]:
                    cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageTowSpeed \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DeploymentUID =?", 
                            (UpdateQCFailList1))
                if getVarnameToView == ListVariableListA[1]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_CodendMeshSize \
                                SET GearType = ? , QC_CaseType = ?\
                                WHERE DeploymentUID =?", 
                                (UpdateQCFailList1))
                if getVarnameToView == ListVariableListA[2]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MeshSizeMG \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DeploymentUID =?", 
                            (UpdateQCFailList1))
                if getVarnameToView == ListVariableListA[3]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberGillnets \
                                SET GearType = ? , QC_CaseType = ?\
                                WHERE DeploymentUID =?", 
                                (UpdateQCFailList1))
                if getVarnameToView == ListVariableListA[4]:
                    cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_AverageGillnetLength \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DeploymentUID =?", 
                            (UpdateQCFailList1))
                if getVarnameToView == ListVariableListA[5]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberHooks \
                                SET GearType = ? , QC_CaseType = ?\
                                WHERE DeploymentUID =?", 
                                (UpdateQCFailList1))
                if getVarnameToView == ListVariableListA[6]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberWindows \
                            SET GearType = ? , QC_CaseType = ?\
                            WHERE DeploymentUID =?", 
                            (UpdateQCFailList1))
                if getVarnameToView == ListVariableListA[7]:
                        cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_NumberPots \
                                SET GearType = ? , QC_CaseType = ?\
                                WHERE DeploymentUID =?", 
                                (UpdateQCFailList1))

        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Presence.commit()
        conn_Validation_Presence.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18=['GearType']
            
            Var_Class_FloatA7= ['AverageTowSpeed']
            
            Var_Class_String7 =['DeploymentUID']
            
            Var_Class_IntB27  = ['CodendMeshSize','MeshSizeMG',
                            'NumberGillnets','AverageGillnetLength','NumberHooks', 'NumberWindows', 'NumberPots']

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
            
            if get_Updated_Variable in Var_Class_FloatA7:
                if(len(get_UpdateValue_UpdatedVariable)!=0):
                    try:
                        get_UpdateValue_UpdatedVariable = float(get_UpdateValue_UpdatedVariable)
                        return get_UpdateValue_UpdatedVariable
                    except:
                        messagebox.showerror('Update Variable Datatype Error Message', 
                                            "Updated Value Must Be Float Value")
                        return ReturnFail
                else:
                    get_UpdateValue_UpdatedVariable = (get_UpdateValue_UpdatedVariable)
                    return get_UpdateValue_UpdatedVariable

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
        getVarnameToView = entry_ViewVarResults.get()
        get_RectypeSelection = entry_SelectFilterView.get()
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
                        UpdateRecordList =[]
                        UpdateQCFailList =[]
                        UpdateRecordList1 =[]
                        UpdateQCFailList1 =[]    
                        for item in tree1.selection():
                            list_item = (tree1.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            list_item_QC_CaseType = 'Case-Updated'
                            UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DatabaseUID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                            UpdateQCFailList.append((get_UpdateValue_UpdatedVariable,
                                                    list_item_QC_CaseType,
                                                    list_item_DatabaseUID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                            UpdateRecordList1.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DeploymentUID))
                            UpdateQCFailList1.append((get_UpdateValue_UpdatedVariable,
                                                    list_item_QC_CaseType,
                                                    list_item_DeploymentUID))
                        
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, UpdateQCFailList,
                                                        get_RectypeSelection,UpdateRecordList1,
                                                        UpdateQCFailList1, getVarnameToView)
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(tk.END,"Set & Catch Database Updated Successfully")
                        viewQCFailed_VariablesProfile()
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")
                        
                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                        iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                                                                    "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                        if iUpdateSlected >0:
                            UpdateRecordList =[]
                            UpdateQCFailList =[]
                            UpdateRecordList1 =[]
                            UpdateQCFailList1 =[]  
                            for item in tree1.selection():
                                list_item = (tree1.item(item, 'values'))
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                list_item_QC_CaseType = 'Case-Updated'
                                UpdateRecordList.append((get_UpdateValue_UpdatedVariable,
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                                UpdateQCFailList.append((get_UpdateValue_UpdatedVariable,
                                                    list_item_QC_CaseType,
                                                    list_item_DatabaseUID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                UpdateRecordList1.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DeploymentUID))
                                UpdateQCFailList1.append((get_UpdateValue_UpdatedVariable,
                                                    list_item_QC_CaseType,
                                                    list_item_DeploymentUID))
                            Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, UpdateQCFailList,
                                                            get_RectypeSelection,UpdateRecordList1,
                                                            UpdateQCFailList1, getVarnameToView)
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
            else:
                messagebox.showerror('Update Error',
                                "Please Select Atleast One Entries Tp Update") 
        else:
            messagebox.showerror('Update Error',
                                "Please Check Variable DataType And Follow Proper Update Step") 

    def callbackFuncSelectVariable1(event):
        VariableListA = entry_UpdateVariableList.get()
        print('Selected Update Variable Name :'+ VariableListA)
        if len(VariableListA)!= 0:
            entry_UpdateValue_VariableA.delete(0,END)
        if(VariableListA=='AverageTowSpeed'):
            EntryDataType_Variable = 'Float DataType Only'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)
        else:
            EntryDataType_Variable = 'Numeric DataType Only'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)

    def Combo_input_AverageTowSpeed():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT AverageTowSpeed FROM SetCatch_QCFailedPresence_AverageTowSpeed")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_CodendMeshSize():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT CodendMeshSize FROM SetCatch_QCFailedPresence_CodendMeshSize")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_MeshSizeMG():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT MeshSizeMG FROM SetCatch_QCFailedPresence_MeshSizeMG")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberGillnets():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT NumberGillnets FROM SetCatch_QCFailedPresence_NumberGillnets")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_AverageGillnetLength():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT AverageGillnetLength FROM SetCatch_QCFailedPresence_AverageGillnetLength")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberHooks():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT NumberHooks FROM SetCatch_QCFailedPresence_NumberHooks")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberWindows():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT NumberWindows FROM SetCatch_QCFailedPresence_NumberWindows")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberPots():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT NumberPots FROM SetCatch_QCFailedPresence_NumberPots")
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
        
        if VariableListA == 'AverageTowSpeed':
            entry_SearchValue_Variable_A['values'] = sorted([float(i) if i else np.nan for i in list(set((Combo_input_AverageTowSpeed())))])
        if VariableListA == 'CodendMeshSize':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_CodendMeshSize())))])
        if VariableListA == 'MeshSizeMG':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_MeshSizeMG())))])
        if VariableListA == 'NumberGillnets':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberGillnets())))])
        if VariableListA == 'AverageGillnetLength':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_AverageGillnetLength())))])
        if VariableListA == 'NumberHooks':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberHooks())))])
        if VariableListA == 'NumberWindows':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberWindows())))])
        if VariableListA == 'NumberPots':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberPots())))])
    
    def SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value):
        ListVariableSearch = ['AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                            'NumberGillnets','AverageGillnetLength','NumberHooks', 'NumberWindows', 'NumberPots']
        conn= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=conn.cursor()

        if get_SearchSingleVariable == ListVariableSearch[0]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = float(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed WHERE AverageTowSpeed = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "AverageTowSpeed Must Be Float Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed WHERE AverageTowSpeed = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[1]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize WHERE CodendMeshSize = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "CodendMeshSize Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize WHERE CodendMeshSize = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[2]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG WHERE MeshSizeMG = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "MeshSizeMG Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG WHERE MeshSizeMG = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[3]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets WHERE NumberGillnets = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "NumberGillnets Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets WHERE NumberGillnets = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[4]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength WHERE AverageGillnetLength = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "AverageGillnetLength Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength WHERE AverageGillnetLength = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[5]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks WHERE NumberHooks = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "NumberHooks Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks WHERE NumberHooks = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[6]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows WHERE NumberWindows = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "NumberWindows Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows WHERE NumberWindows = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[7]:
            if(get_SearchSingleVariable_Value!='NaN'):
                    try:
                        get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                        cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberPots WHERE NumberPots = ?", (get_SearchSingleVariable_Value,))
                        rows=cur.fetchall()
                        return rows
                    except:
                        messagebox.showerror('Search Variable Datatype Error Message', "NumberPots Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur.execute("SELECT * FROM SetCatch_QCFailedPresence_NumberPots WHERE NumberPots = ?", (get_SearchSingleVariable_Value,))
                rows=cur.fetchall()
                return rows

        conn.commit()
        conn.close()

    def RunSingleVariableSearchQuery():
        get_SearchSingleVariable        = entry_SearchVariableList.get()
        get_SearchSingleVariable_Value  = entry_SearchValue_Variable_A.get()
        QCget_SearchSingleVariable = 'QC'+ get_SearchSingleVariable
        if(len(get_SearchSingleVariable)!=0) & (len(get_SearchSingleVariable_Value)!=0):    
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            entry_ViewVarResults.set(get_SearchSingleVariable)
            txtDisplayMessageSystem.insert(tk.END,(("Variable Search :") + get_SearchSingleVariable))
            rows = SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value)
            rows = pd.DataFrame(rows)
            rows.reset_index(drop=True)
            SingleSearchRowsDF = pd.DataFrame(rows)
            SingleSearchRowsDF.rename(columns={0:'DataBase_ID', 1: 'RecordIdentifier', 2: 'DeploymentUID',
                                                3:'GearType',   4: get_SearchSingleVariable,   
                                                5: QCget_SearchSingleVariable
                                                }, inplace = True)
            
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
        try:
            LenGenSummaryQC = RunPresenceConditional_FailedVariables()
        except:
            print('Error Occured In Generating QC Summary')
        finally:
            if LenGenSummaryQC > -1 :
                conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
                cursor = conn.cursor()
                AverageTowSpeed_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed;", conn)
                CodendMeshSize_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize;", conn)
                MeshSizeMG_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG;", conn)
                NumberGillnets_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets;", conn)
                AverageGillnetLength_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength;", conn)
                NumberHooks_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks;", conn)
                NumberWindows_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows;", conn)
                NumberPots_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots;", conn)
                cursor.close()
                conn.close()

                AverageTowSpeed_df = (pd.DataFrame(AverageTowSpeed_df))
                CodendMeshSize_df = (pd.DataFrame(CodendMeshSize_df))
                MeshSizeMG_df = (pd.DataFrame(MeshSizeMG_df))
                NumberGillnets_df = (pd.DataFrame(NumberGillnets_df))
                AverageGillnetLength_df = (pd.DataFrame(AverageGillnetLength_df))
                NumberHooks_df = (pd.DataFrame(NumberHooks_df))
                NumberWindows_df = (pd.DataFrame(NumberWindows_df))
                NumberPots_df = (pd.DataFrame(NumberPots_df))
                
                Len_AverageTowSpeed_df = len((AverageTowSpeed_df))
                Len_CodendMeshSize_df = len((CodendMeshSize_df))
                Len_MeshSizeMG_df = len((MeshSizeMG_df))
                Len_NumberGillnets_df = len((NumberGillnets_df))
                Len_AverageGillnetLength_df = len((AverageGillnetLength_df))
                Len_NumberHooks_df = len((NumberHooks_df))
                Len_NumberWindows_df = len((NumberWindows_df))
                Len_NumberPots_df = len((NumberPots_df))

                QC_CaseUpdateMsg = 'Case-Updated'
                Update_AverageTowSpeed_df = len(AverageTowSpeed_df[
                                ((AverageTowSpeed_df.QC_CaseType) == QC_CaseUpdateMsg)])
                Update_CodendMeshSize_df = len(CodendMeshSize_df[
                                ((CodendMeshSize_df.QC_CaseType) == QC_CaseUpdateMsg)])
                Update_MeshSizeMG_df = len(MeshSizeMG_df[
                                ((MeshSizeMG_df.QC_CaseType) == QC_CaseUpdateMsg)])
                Update_NumberGillnets_df = len(NumberGillnets_df[
                                ((NumberGillnets_df.QC_CaseType) == QC_CaseUpdateMsg)])
                Update_AverageGillnetLength_df = len(AverageGillnetLength_df[
                                ((AverageGillnetLength_df.QC_CaseType) == QC_CaseUpdateMsg)])
                Update_NumberHooks_df = len(NumberHooks_df[
                                ((NumberHooks_df.QC_CaseType) == QC_CaseUpdateMsg)])
                Update_NumberWindows_df = len(NumberWindows_df[
                                ((NumberWindows_df.QC_CaseType) == QC_CaseUpdateMsg)])
                Update_NumberPots_df = len(NumberPots_df[
                                ((NumberPots_df.QC_CaseType) == QC_CaseUpdateMsg)])
        
                ListVariableName = ['AverageTowSpeed','CodendMeshSize',
                                    'MeshSizeMG','NumberGillnets',
                                    'AverageGillnetLength','NumberHooks',
                                    'NumberWindows', 'NumberPots']
                QCFailCount = [Len_AverageTowSpeed_df, Len_CodendMeshSize_df, 
                            Len_MeshSizeMG_df, Len_NumberGillnets_df,
                            Len_AverageGillnetLength_df, Len_NumberHooks_df, 
                            Len_NumberWindows_df, Len_NumberPots_df]
                QCUpdateCount = [Update_AverageTowSpeed_df, Update_CodendMeshSize_df, 
                            Update_MeshSizeMG_df, Update_NumberGillnets_df,
                            Update_AverageGillnetLength_df, Update_NumberHooks_df, 
                            Update_NumberWindows_df, Update_NumberPots_df]
                
                QCFailAppend = {'VariableName': ListVariableName, 
                                'QCFailCount': QCFailCount,
                                'QCUpdateCount': QCUpdateCount} 
                QCFailSummaryDF = pd.DataFrame(QCFailAppend)

                if len(QCFailSummaryDF) >0:
                    QCFailSummaryDF[['QCFailCount', 'QCUpdateCount']] = QCFailSummaryDF[['QCFailCount', 'QCUpdateCount']].astype(int)
                    QCFailSummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
                    QCFailSummaryDF = QCFailSummaryDF.reset_index(drop=True)
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
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        cursor = conn.cursor()
        AverageTowSpeed_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed ORDER BY `DataBase_ID` ASC ;", conn)
        CodendMeshSize_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize ORDER BY `DataBase_ID` ASC ;", conn)
        MeshSizeMG_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG ORDER BY `DataBase_ID` ASC ;", conn)
        NumberGillnets_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets ORDER BY `DataBase_ID` ASC ;", conn)
        AverageGillnetLength_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength ORDER BY `DataBase_ID` ASC ;", conn)
        NumberHooks_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks ORDER BY `DataBase_ID` ASC ;", conn)
        NumberWindows_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows ORDER BY `DataBase_ID` ASC ;", conn)
        NumberPots_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots ORDER BY `DataBase_ID` ASC ;", conn)
        cursor.close()
        conn.close()
        get_RectypeSelection = entry_SelectFilterView.get()
        SelectViewFilter = ['RecType-1&2', 'RecType 1 Only']
        if(get_RectypeSelection ==SelectViewFilter[0]):
            AverageTowSpeed_df = pd.DataFrame(AverageTowSpeed_df)
            CodendMeshSize_df = pd.DataFrame(CodendMeshSize_df)
            MeshSizeMG_df = pd.DataFrame(MeshSizeMG_df)
            NumberGillnets_df = pd.DataFrame(NumberGillnets_df)
            AverageGillnetLength_df = pd.DataFrame(AverageGillnetLength_df)
            NumberHooks_df = pd.DataFrame(NumberHooks_df)
            NumberWindows_df = pd.DataFrame(NumberWindows_df)
            NumberPots_df = pd.DataFrame(NumberPots_df)
        else:
            AverageTowSpeed_df = pd.DataFrame(AverageTowSpeed_df)
            AverageTowSpeed_df = AverageTowSpeed_df[((AverageTowSpeed_df.RecordType) == 1)]
            AverageTowSpeed_df  = AverageTowSpeed_df.reset_index(drop=True)
            AverageTowSpeed_df  = pd.DataFrame(AverageTowSpeed_df)

            CodendMeshSize_df = pd.DataFrame(CodendMeshSize_df)
            CodendMeshSize_df = CodendMeshSize_df[((CodendMeshSize_df.RecordType) == 1)]
            CodendMeshSize_df  = CodendMeshSize_df.reset_index(drop=True)
            CodendMeshSize_df  = pd.DataFrame(CodendMeshSize_df)
            
            MeshSizeMG_df = pd.DataFrame(MeshSizeMG_df)
            MeshSizeMG_df = MeshSizeMG_df[((MeshSizeMG_df.RecordType) == 1)]
            MeshSizeMG_df  = MeshSizeMG_df.reset_index(drop=True)
            MeshSizeMG_df  = pd.DataFrame(MeshSizeMG_df)

            NumberGillnets_df = pd.DataFrame(NumberGillnets_df)
            NumberGillnets_df = NumberGillnets_df[((NumberGillnets_df.RecordType) == 1)]
            NumberGillnets_df  = NumberGillnets_df.reset_index(drop=True)
            NumberGillnets_df  = pd.DataFrame(NumberGillnets_df)

            AverageGillnetLength_df = pd.DataFrame(AverageGillnetLength_df)
            AverageGillnetLength_df = AverageGillnetLength_df[((AverageGillnetLength_df.RecordType) == 1)]
            AverageGillnetLength_df  = AverageGillnetLength_df.reset_index(drop=True)
            AverageGillnetLength_df  = pd.DataFrame(AverageGillnetLength_df)

            NumberHooks_df = pd.DataFrame(NumberHooks_df)
            NumberHooks_df = NumberHooks_df[((NumberHooks_df.RecordType) == 1)]
            NumberHooks_df  = NumberHooks_df.reset_index(drop=True)
            NumberHooks_df  = pd.DataFrame(NumberHooks_df)

            NumberWindows_df = pd.DataFrame(NumberWindows_df)
            NumberWindows_df = NumberWindows_df[((NumberWindows_df.RecordType) == 1)]
            NumberWindows_df  = NumberWindows_df.reset_index(drop=True)
            NumberWindows_df  = pd.DataFrame(NumberWindows_df)

            NumberPots_df = pd.DataFrame(NumberPots_df)
            NumberPots_df = NumberPots_df[((NumberPots_df.RecordType) == 1)]
            NumberPots_df  = NumberPots_df.reset_index(drop=True)
            NumberPots_df  = pd.DataFrame(NumberPots_df)

        ListVariableName = ['AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                            'NumberGillnets','AverageGillnetLength','NumberHooks', 'NumberWindows', 'NumberPots']
        nm = Summaryframetree.selection()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            entry_ViewVarResults.set(SelvariableIdentifier)
            entry_SelQCVariable.delete(0,END)
            entry_SelQCVariable.insert(tk.END, (SelvariableIdentifier))

            ## Select AverageTowSpeed
            if SelvariableIdentifier == ListVariableName[0]:
                tree1.delete(*tree1.get_children())
                AverageTowSpeed_df  = AverageTowSpeed_df.reset_index(drop=True)
                QCFailedAverageTowSpeed  = pd.DataFrame(AverageTowSpeed_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedAverageTowSpeed)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedAverageTowSpeed.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedAverageTowSpeed.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[4,5,7,8,10,13,14,15,20,22,64,65] Then AvgTowSpeed == 0|Blank, Else > 0|NoBlank')
            
            ## Select CodendMeshSize
            if SelvariableIdentifier == ListVariableName[1]:
                tree1.delete(*tree1.get_children())
                CodendMeshSize_df  = CodendMeshSize_df.reset_index(drop=True)
                QCFailedCodendMeshSize  = pd.DataFrame(CodendMeshSize_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedCodendMeshSize)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedCodendMeshSize.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedCodendMeshSize.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[1,2,3,9,16,17,18,21,24,66,67,97] Then CodendMeshSize == NoBlank, Else Blank')

            ## Select MeshSizeMG
            if SelvariableIdentifier == ListVariableName[2]:
                tree1.delete(*tree1.get_children())
                MeshSizeMG_df  = MeshSizeMG_df.reset_index(drop=True)
                QCFailedMeshSizeMG  = pd.DataFrame(MeshSizeMG_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedMeshSizeMG)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedMeshSizeMG.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedMeshSizeMG.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[1,2,3,6,9,16,17,18,21,23,24,66,67,97] Then MeshSize_MG == NoBlank, Else Blank')

            ## Select NumberGillnets
            if SelvariableIdentifier == ListVariableName[3]:
                tree1.delete(*tree1.get_children())
                NumberGillnets_df  = NumberGillnets_df.reset_index(drop=True)
                QCFailedNumberGillnets  = pd.DataFrame(NumberGillnets_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedNumberGillnets)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedNumberGillnets.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedNumberGillnets.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[5,15] Then NumberGillnets == NoBlank, Else Blank')

            ## Select AverageGillnetLength
            if SelvariableIdentifier == ListVariableName[4]:
                tree1.delete(*tree1.get_children())
                AverageGillnetLength_df  = AverageGillnetLength_df.reset_index(drop=True)
                QCFailedAverageGillnetLength  = pd.DataFrame(AverageGillnetLength_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedAverageGillnetLength)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedAverageGillnetLength.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedAverageGillnetLength.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[5,15] Then AverageGillnetLength == NoBlank, Else Blank')
            
            ## Select NumberHooks
            if SelvariableIdentifier == ListVariableName[5]:
                tree1.delete(*tree1.get_children())
                NumberHooks_df  = NumberHooks_df.reset_index(drop=True)
                QCFailedNumberHooks  = pd.DataFrame(NumberHooks_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedNumberHooks)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedNumberHooks.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedNumberHooks.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[7,8,22] Then NumberHooks == NoBlank, Else Blank')

            ## Select NumberWindows
            if SelvariableIdentifier == ListVariableName[6]:
                tree1.delete(*tree1.get_children())
                NumberWindows_df  = NumberWindows_df.reset_index(drop=True)
                QCFailedNumberWindows  = pd.DataFrame(NumberWindows_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedNumberWindows)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedNumberWindows.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedNumberWindows.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[1,2,16,17,18,21,66,67] Then NumberWindows == NoBlank, Else Blank')

            ## Select NumberPots
            if SelvariableIdentifier == ListVariableName[7]:
                tree1.delete(*tree1.get_children())
                NumberPots_df  = NumberPots_df.reset_index(drop=True)
                QCFailedNumberPots  = pd.DataFrame(NumberPots_df)
                countIndex1 = 0
                for each_rec in range(len(QCFailedNumberPots)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailedNumberPots.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailedNumberPots.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'If GType[64] Then NumberPots == NoBlank, Else Blank')
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END, (' Please Select Only One Entries To View'))
    
    def QCFailedtotalEntries():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        cursor = conn.cursor()
        AverageTowSpeed_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed;", conn)
        CodendMeshSize_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize;", conn)
        MeshSizeMG_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG;", conn)
        NumberGillnets_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets;", conn)
        AverageGillnetLength_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength;", conn)
        NumberHooks_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks;", conn)
        NumberWindows_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows;", conn)
        NumberPots_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots;", conn)
        cursor.close()
        conn.close()
        
        Count_AverageTowSpeed_df = len(pd.DataFrame(AverageTowSpeed_df))
        Count_CodendMeshSize_df = len(pd.DataFrame(CodendMeshSize_df))
        Count_MeshSizeMG_df = len(pd.DataFrame(MeshSizeMG_df))
        Count_NumberGillnets_df = len(pd.DataFrame(NumberGillnets_df))
        Count_AverageGillnetLength_df = len(pd.DataFrame(AverageGillnetLength_df))
        Count_NumberHooks_df = len(pd.DataFrame(NumberHooks_df))
        Count_NumberWindows_df = len(pd.DataFrame(NumberWindows_df))
        Count_NumberPots_df = len(pd.DataFrame(NumberPots_df))
        QCFailTotalEntries =    (Count_AverageTowSpeed_df +\
                                 Count_CodendMeshSize_df+\
                                 Count_MeshSizeMG_df+\
                                 Count_NumberGillnets_df+\
                                 Count_AverageGillnetLength_df+\
                                 Count_NumberHooks_df+\
                                 Count_NumberWindows_df+\
                                 Count_NumberPots_df
                                 )
        txtTotalFailedEntries.delete(0,END)
        txtTotalFailedEntries.insert(tk.END,QCFailTotalEntries)
        return QCFailTotalEntries         

    def callbackFuncSelectView(event):
        ListVariableListA = ['Select Variable & Run View Selected QC Button', 
                             'AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                             'NumberGillnets','AverageGillnetLength',
                             'NumberHooks', 'NumberWindows', 'NumberPots']
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
            txtDisplayMessageSystem.insert(1, 'If GType[4,5,7,8,10,13,14,15,20,22,64,65] Then AvgTowSpeed == 0|Blank, Else > 0|NoBlank')
            
        if(SelVariableView ==ListVariableListA[2]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'If GType[1,2,3,9,16,17,18,21,24,66,67,97] Then CodendMeshSize == NoBlank, Else Blank')
        
        if(SelVariableView ==ListVariableListA[3]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'If GType[1,2,3,6,9,16,17,18,21,23,24,66,67,97] Then MeshSize_MG == NoBlank, Else Blank')
            
        if(SelVariableView ==ListVariableListA[4]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'If GType[5,15] Then NumberGillnets == NoBlank, Else Blank')
        
        if(SelVariableView ==ListVariableListA[5]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'If GType[5,15] Then AverageGillnetLength == NoBlank, Else Blank')
            
        if(SelVariableView ==ListVariableListA[6]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'If GType[7,8,22] Then NumberHooks == NoBlank, Else Blank')
        
        if(SelVariableView ==ListVariableListA[7]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'If GType[1,2,16,17,18,21,66,67] Then NumberWindows == NoBlank, Else Blank')
            
        if(SelVariableView ==ListVariableListA[8]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'If GType[64] Then NumberPots == NoBlank, Else Blank')

    def ExcelViewEditBackend_RecType_1_2(QC_FailPresence_DF, get_SearchSingleVariable_Value):
        if len(QC_FailPresence_DF) >0:
            QC_FailPresence_DF  = QC_FailPresence_DF.reset_index(drop=True)
            QC_FailPresence_DF  = pd.DataFrame(QC_FailPresence_DF)
            get_DepNumSearchValue = int(get_SearchSingleVariable_Value)   
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0,'Viewing QC Failed Excel File In Seperate Window')
            ExcelView_DeploymentSearch.ExcelViewPresnceCond_Rec_1_2_SetCatchDB(QC_FailPresence_DF,get_DepNumSearchValue)

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
                rows.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber','SetNumber','RecordType'], inplace=True)
                rows  = rows.reset_index(drop=True)
                rows  = pd.DataFrame(rows)
                rows = rows[(rows.DeploymentNumber) == get_SearchSingleVariable_Value]
                rows  = rows.reset_index(drop=True)
                rows= (rows.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
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
                'NumberIndividuals']])
                QC_FailPresence_DF  = pd.DataFrame(rows)
                ExcelViewEditBackend_RecType_1_2(QC_FailPresence_DF, get_SearchSingleVariable_Value)

    def UpdateDeploymentUIDAfterUpdate():
        ## Defining Functions
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

        UpdateSetcatchDB()
        tree1.delete(*tree1.get_children())
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    def GenDeploymentSummary():
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        ListUpdateVar = ['AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                        'NumberGillnets','AverageGillnetLength',
                        'NumberHooks','NumberWindows', 'NumberPots']
        getVarnameToView = entry_SelQCVariable.get()
        if getVarnameToView in (ListUpdateVar):
            conn= sqlite3.connect(DB_SetCatch_Validation_Presence)
            if getVarnameToView == "AverageTowSpeed":
                 SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed;", conn)
            if getVarnameToView == "CodendMeshSize":
                SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize  ;", conn)
            if getVarnameToView == "MeshSizeMG":
                SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG  ;", conn)
            if getVarnameToView == "NumberGillnets":
                SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets  ;", conn)
            if getVarnameToView == "AverageGillnetLength":
                SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength  ;", conn)
            if getVarnameToView == "NumberHooks":
                SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks  ;", conn)
            if getVarnameToView == "NumberWindows":
                SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows  ;", conn)
            if getVarnameToView == "NumberPots":
                SetCatchQCFailed_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots  ;", conn)
            conn.commit()
            conn.close()
            if len(SetCatchQCFailed_DF) >0:
                SetCatchQCFailed_DF = SetCatchQCFailed_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                    'DeploymentUID']]
                SetCatchQCFailed_DF  = SetCatchQCFailed_DF.reset_index(drop=True)
                SetCatchQCFailed_DF  = pd.DataFrame(SetCatchQCFailed_DF)
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
                Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                    SetCatchQCFailed_DF, 
                    on = ['DataBase_ID','RecordIdentifier','DeploymentUID'], indicator=True, 
                    how='outer').query('_merge == "both"')
                
                Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
                Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
                Ref_FailedQC_InSetcatchDB['ASOCCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
                Ref_FailedQC_InSetcatchDB['Year'] = (Ref_FailedQC_InSetcatchDB.loc[:,['Year']]).astype(int, errors='ignore')
                Ref_FailedQC_InSetcatchDB['DeploymentNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DeploymentNumber']]).astype(int, errors='ignore')
                Ref_FailedQC_InSetcatchDB['SetNumber'] = (Ref_FailedQC_InSetcatchDB.loc[:,['SetNumber']]).astype(int, errors='ignore')
                
                Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
                Complete_df  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
                Complete_df = Complete_df.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                'Year','ASOCCode', 'DeploymentNumber']]
                Complete_df  = pd.DataFrame(Complete_df)
                Complete_df.sort_values(
                    by=['Year','ASOCCode', 'DeploymentNumber'], inplace=True)
                Complete_df  = Complete_df.reset_index(drop=True)
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.groupby(
                    ['Year', 'ASOCCode','DeploymentNumber'],  
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

    def ClearSummary():
        SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
        Summaryframetree.delete(*Summaryframetree.get_children())
        entry_SelQCVariable.delete(0,END)
        entry_SelQCVariable.insert(tk.END,'QC Variable')

    def RunPresenceConditional_FailedVariables():
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                         'RecordType','GearType',
                        'AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                        'NumberGillnets','AverageGillnetLength','NumberHooks',
                        'NumberWindows', 'NumberPots']]
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

        def Submit_PresenceConditional_DB(AverageTowSpeedDB_Failed, CodendMeshSizeDB_Failed,
                                        MeshSizeMGDB_Failed, NumberGillnetsDB_Failed,
                                        AverageGillnetLengthDB_Failed, NumberHooksDB_Failed,
                                        NumberWindowsDB_Failed, NumberPotsDB_Failed):
            try:
                AverageTowSpeedDB_Failed = pd.DataFrame(AverageTowSpeedDB_Failed)
                CodendMeshSizeDB_Failed = pd.DataFrame(CodendMeshSizeDB_Failed)
                MeshSizeMGDB_Failed = pd.DataFrame(MeshSizeMGDB_Failed)
                NumberGillnetsDB_Failed = pd.DataFrame(NumberGillnetsDB_Failed)
                AverageGillnetLengthDB_Failed = pd.DataFrame(AverageGillnetLengthDB_Failed)
                NumberHooksDB_Failed = pd.DataFrame(NumberHooksDB_Failed)
                NumberWindowsDB_Failed = pd.DataFrame(NumberWindowsDB_Failed)
                NumberPotsDB_Failed = pd.DataFrame(NumberPotsDB_Failed)

                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Presence)
                cursor = sqliteConnection.cursor()
                AverageTowSpeedDB_Failed.to_sql('SetCatch_QCFailedPresence_AverageTowSpeed',
                                            sqliteConnection, if_exists="replace", index =False)
                CodendMeshSizeDB_Failed.to_sql('SetCatch_QCFailedPresence_CodendMeshSize',
                                            sqliteConnection, if_exists="replace", index =False)
                MeshSizeMGDB_Failed.to_sql('SetCatch_QCFailedPresence_MeshSizeMG',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberGillnetsDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberGillnets',
                                            sqliteConnection, if_exists="replace", index =False)
                AverageGillnetLengthDB_Failed.to_sql('SetCatch_QCFailedPresence_AverageGillnetLength',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberHooksDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberHooks',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberWindowsDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberWindows',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberPotsDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberPots',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        
        ## AverageTowSpeed QC
        GearType_AverageTowSpeed= [4,5,7,8,10,13,14,15,20,22,64,65]
        NotinList_AverageTowSpeed =[0.0, 0, 99999999.0, 99999999]
        AverageTowSpeedDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'AverageTowSpeed']]).replace(['','None'], 99999999)
        AverageTowSpeedDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= AverageTowSpeedDB_DF[
                ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        AverageTowSpeedDB_DF[['DeploymentUID']] = AverageTowSpeedDB_DF[['DeploymentUID']].astype(str)
        AverageTowSpeedDB_DF[['AverageTowSpeed']] = AverageTowSpeedDB_DF[['AverageTowSpeed']].astype(float)

        AverageTowSpeedDB_Failed =[]
        AverageTowSpeedDB_DF_1 = AverageTowSpeedDB_DF[(
                                (AverageTowSpeedDB_DF['GearType'].isin(GearType_AverageTowSpeed)) &\
                                (~(AverageTowSpeedDB_DF['AverageTowSpeed'].isin(NotinList_AverageTowSpeed)))
                                    )]
        AverageTowSpeedDB_DF_2 = AverageTowSpeedDB_DF[(
                                (~(AverageTowSpeedDB_DF['GearType'].isin(GearType_AverageTowSpeed))) &\
                                ((AverageTowSpeedDB_DF['AverageTowSpeed'].isin(NotinList_AverageTowSpeed)))
                                    )]
        
        AverageTowSpeedDB_Failed = pd.concat([AverageTowSpeedDB_DF_1, AverageTowSpeedDB_DF_2])
        AverageTowSpeedDB_Failed= (AverageTowSpeedDB_Failed.loc[:,[
                                        'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                        'GearType', 'AverageTowSpeed']]).replace([99999999.0, 99999999], '')
        AverageTowSpeedDB_Failed['QCAverageTowSpeed'] ="GType[4,5,7,8,10,13,14,15,20,22,64,65]=>AvgTowSpeed =0|Blank, Else > 0|NoBlank"
        AverageTowSpeedDB_Failed['QC_CaseType'] = 'Case-ATS'
        AverageTowSpeedDB_Failed  = AverageTowSpeedDB_Failed.reset_index(drop=True)
        AverageTowSpeedDB_Failed  = pd.DataFrame(AverageTowSpeedDB_Failed)

        ## CodendMeshSize QC
        GearType_CodendMeshSize= [1,2,3,9,16,17,18,21,24,66,67,97]
        NotinList_CodendMeshSize =[0, 99999999]
        CodendMeshSizeDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'CodendMeshSize']]).replace(['','None'], 99999999)
        CodendMeshSizeDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= CodendMeshSizeDB_DF[
                          ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        CodendMeshSizeDB_DF[['DeploymentUID']] = CodendMeshSizeDB_DF[['DeploymentUID']].astype(str)
        CodendMeshSizeDB_DF[['CodendMeshSize']] = CodendMeshSizeDB_DF[['CodendMeshSize']].astype(int)

        CodendMeshSizeDB_Failed =[]
        CodendMeshSizeDB_DF_1 = CodendMeshSizeDB_DF[(
                                (CodendMeshSizeDB_DF['GearType'].isin(GearType_CodendMeshSize)) &\
                                ((CodendMeshSizeDB_DF['CodendMeshSize'].isin(NotinList_CodendMeshSize)))
                                                        )]
        CodendMeshSizeDB_DF_2 = CodendMeshSizeDB_DF[(
                                (~(CodendMeshSizeDB_DF['GearType'].isin(GearType_CodendMeshSize))) &\
                                (~((CodendMeshSizeDB_DF['CodendMeshSize'].isin(NotinList_CodendMeshSize))))
                                                        )]
        CodendMeshSizeDB_Failed = pd.concat([CodendMeshSizeDB_DF_1, CodendMeshSizeDB_DF_2])
        CodendMeshSizeDB_Failed= (CodendMeshSizeDB_Failed.loc[:,[
                                        'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                        'GearType', 'CodendMeshSize']]).replace([99999999], '')
        CodendMeshSizeDB_Failed['QCCodendMeshSize'] ="GType[1,2,3,9,16,17,18,21,24,66,67,97]=>CodendMeshSize=NoBlank, Else Blank"
        CodendMeshSizeDB_Failed['QC_CaseType'] = 'Case-CMS'
        CodendMeshSizeDB_Failed  = CodendMeshSizeDB_Failed.reset_index(drop=True)
        CodendMeshSizeDB_Failed  = pd.DataFrame(CodendMeshSizeDB_Failed)

        ## MeshSizeMG QC
        GearType_MeshSizeMG= [1,2,3,6,9,16,17,18,21,23,24,66,67,97]
        NotinList_MeshSizeMG =[0, 99999999]
        MeshSizeMGDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'MeshSizeMG']]).replace(['','None'], 99999999)
        MeshSizeMGDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= MeshSizeMGDB_DF[
            ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        MeshSizeMGDB_DF[['DeploymentUID']] = MeshSizeMGDB_DF[['DeploymentUID']].astype(str)
        MeshSizeMGDB_DF[['MeshSizeMG']] = MeshSizeMGDB_DF[['MeshSizeMG']].astype(int)

        MeshSizeMGDB_Failed =[]
        MeshSizeMGDB_DF_1 = MeshSizeMGDB_DF[(
                                (MeshSizeMGDB_DF['GearType'].isin(GearType_MeshSizeMG)) &\
                                ((MeshSizeMGDB_DF['MeshSizeMG'].isin(NotinList_MeshSizeMG)))
                                        )]
        MeshSizeMGDB_DF_2 = MeshSizeMGDB_DF[(
                                (~(MeshSizeMGDB_DF['GearType'].isin(GearType_MeshSizeMG))) &\
                                (~((MeshSizeMGDB_DF['MeshSizeMG'].isin(NotinList_MeshSizeMG))))
                                        )]
        MeshSizeMGDB_Failed = pd.concat([MeshSizeMGDB_DF_1,MeshSizeMGDB_DF_2]) 
        MeshSizeMGDB_Failed= (MeshSizeMGDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'MeshSizeMG']]).replace([99999999], '')
        MeshSizeMGDB_Failed['QCMeshSizeMG'] ="GType[1,2,3,6,9,16,17,18,21,23,24,66,67,97]=>MeshSize_MG=NoBlank, Else Blank"
        MeshSizeMGDB_Failed['QC_CaseType'] = 'Case-MSMG'
        MeshSizeMGDB_Failed  = MeshSizeMGDB_Failed.reset_index(drop=True)
        MeshSizeMGDB_Failed  = pd.DataFrame(MeshSizeMGDB_Failed)
        
        ## NumberGillnets QC
        GearType_NumberGillnets= [5, 15]
        NotinList_NumberGillnets =[0, 99999999]
        NumberGillnetsDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'NumberGillnets']]).replace(['','None'], 99999999)
        NumberGillnetsDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberGillnetsDB_DF[
              ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberGillnetsDB_DF[['DeploymentUID']] = NumberGillnetsDB_DF[['DeploymentUID']].astype(str)
        NumberGillnetsDB_DF[['NumberGillnets']] = NumberGillnetsDB_DF[['NumberGillnets']].astype(int)

        NumberGillnetsDB_Failed =[]
        NumberGillnetsDB_DF_1 = NumberGillnetsDB_DF[(
                                (NumberGillnetsDB_DF['GearType'].isin(GearType_NumberGillnets)) &\
                                ((NumberGillnetsDB_DF['NumberGillnets'].isin(NotinList_NumberGillnets)))
                                        )]
        NumberGillnetsDB_DF_2 = NumberGillnetsDB_DF[(
                                (~(NumberGillnetsDB_DF['GearType'].isin(GearType_NumberGillnets))) &\
                                (~((NumberGillnetsDB_DF['NumberGillnets'].isin(NotinList_NumberGillnets))))
                                        )]
        NumberGillnetsDB_Failed = pd.concat([NumberGillnetsDB_DF_1, NumberGillnetsDB_DF_2])
        NumberGillnetsDB_Failed= (NumberGillnetsDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberGillnets']]).replace([99999999], '')
        NumberGillnetsDB_Failed['QCNumberGillnets'] ="GType[5,15]=>NumberGillnets=NoBlank, Else Blank"
        NumberGillnetsDB_Failed['QC_CaseType'] = 'Case-NG'
        NumberGillnetsDB_Failed  = NumberGillnetsDB_Failed.reset_index(drop=True)
        NumberGillnetsDB_Failed  = pd.DataFrame(NumberGillnetsDB_Failed)

        ## AverageGillnetLength QC
        GearType_AverageGillnetLength= [5, 15]
        NotinList_AverageGillnetLength =[0, 99999999]
        AverageGillnetLengthDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID', 'RecordType',
                                'GearType', 'AverageGillnetLength']]).replace(['','None'], 99999999)
        AverageGillnetLengthDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= AverageGillnetLengthDB_DF[
              ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        AverageGillnetLengthDB_DF[['DeploymentUID']] = AverageGillnetLengthDB_DF[['DeploymentUID']].astype(str)
        AverageGillnetLengthDB_DF[['AverageGillnetLength']] = AverageGillnetLengthDB_DF[['AverageGillnetLength']].astype(int)

        AverageGillnetLengthDB_Failed =[]
        AverageGillnetLengthDB_DF_1 = AverageGillnetLengthDB_DF[(
                                (AverageGillnetLengthDB_DF['GearType'].isin(GearType_AverageGillnetLength)) &\
                                ((AverageGillnetLengthDB_DF['AverageGillnetLength'].isin(NotinList_AverageGillnetLength)))
                                        )]
        AverageGillnetLengthDB_DF_2 = AverageGillnetLengthDB_DF[(
                                (~(AverageGillnetLengthDB_DF['GearType'].isin(GearType_AverageGillnetLength))) &\
                                (~((AverageGillnetLengthDB_DF['AverageGillnetLength'].isin(NotinList_AverageGillnetLength))))
                                        )]
        AverageGillnetLengthDB_Failed =  pd.concat([AverageGillnetLengthDB_DF_1,AverageGillnetLengthDB_DF_2])
        AverageGillnetLengthDB_Failed= (AverageGillnetLengthDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'AverageGillnetLength']]).replace([99999999], '')
        AverageGillnetLengthDB_Failed['QCAverageGillnetLength'] ="GType[5,15]=>AverageGillnetLength=NoBlank, Else Blank"
        AverageGillnetLengthDB_Failed['QC_CaseType'] = 'Case-AGL'
        AverageGillnetLengthDB_Failed  = AverageGillnetLengthDB_Failed.reset_index(drop=True)
        AverageGillnetLengthDB_Failed  = pd.DataFrame(AverageGillnetLengthDB_Failed)

        ## NumberHooks QC
        GearType_NumberHooks= [7,8,22]
        NotinList_NumberHooks =[0, 99999999]
        NumberHooksDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID', 'RecordType',
                                'GearType', 'NumberHooks']]).replace(['','None'], 99999999)
        NumberHooksDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberHooksDB_DF[
                 ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberHooksDB_DF[['DeploymentUID']] = NumberHooksDB_DF[['DeploymentUID']].astype(str)
        NumberHooksDB_DF[['NumberHooks']] = NumberHooksDB_DF[['NumberHooks']].astype(int)

        NumberHooksDB_Failed =[]
        NumberHooksDB_DF_1 = NumberHooksDB_DF[(
                                (NumberHooksDB_DF['GearType'].isin(GearType_NumberHooks)) &\
                                ((NumberHooksDB_DF['NumberHooks'].isin(NotinList_NumberHooks)))
                                        )]
        NumberHooksDB_DF_2 = NumberHooksDB_DF[(
                                (~(NumberHooksDB_DF['GearType'].isin(GearType_NumberHooks))) &\
                                (~((NumberHooksDB_DF['NumberHooks'].isin(NotinList_NumberHooks))))
                                )]
        NumberHooksDB_Failed = pd.concat([NumberHooksDB_DF_1, NumberHooksDB_DF_2])
        NumberHooksDB_Failed= (NumberHooksDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberHooks']]).replace([99999999], '')
        NumberHooksDB_Failed['QCNumberHooks'] ="GType[7,8,22]=>NumberHooks=NoBlank, Else Blank"
        NumberHooksDB_Failed['QC_CaseType'] = 'Case-NH'
        NumberHooksDB_Failed  = NumberHooksDB_Failed.reset_index(drop=True)
        NumberHooksDB_Failed  = pd.DataFrame(NumberHooksDB_Failed)

        ## NumberWindows QC
        GearType_NumberWindows= [1,2,16,17,18,21,66,67]
        NotinList_NumberWindows =[99999999]
        NumberWindowsDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'NumberWindows']]).replace(['','None'], 99999999)
        NumberWindowsDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberWindowsDB_DF[
               ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberWindowsDB_DF[['DeploymentUID']] = NumberWindowsDB_DF[['DeploymentUID']].astype(str)
        NumberWindowsDB_DF[['NumberWindows']] = NumberWindowsDB_DF[['NumberWindows']].astype(int)

        NumberWindowsDB_Failed =[]
        NumberWindowsDB_DF_1 = NumberWindowsDB_DF[(
                                (NumberWindowsDB_DF['GearType'].isin(GearType_NumberWindows)) &\
                                ((NumberWindowsDB_DF['NumberWindows'].isin(NotinList_NumberWindows)))
                                        )]
        NumberWindowsDB_DF_2 = NumberWindowsDB_DF[(
                        (~(NumberWindowsDB_DF['GearType'].isin(GearType_NumberWindows))) &\
                        (~(NumberWindowsDB_DF['NumberWindows'].isin(NotinList_NumberWindows)))
                            )]
        NumberWindowsDB_Failed =  pd.concat([NumberWindowsDB_DF_1, NumberWindowsDB_DF_2])
        NumberWindowsDB_Failed= (NumberWindowsDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberWindows']]).replace([99999999], '')
        NumberWindowsDB_Failed['QCNumberWindows'] ="GType[1,2,16,17,18,21,66,67]=>NumberWindows=NoBlank, Else Blank"
        NumberWindowsDB_Failed['QC_CaseType'] = 'Case-NW'
        NumberWindowsDB_Failed  = NumberWindowsDB_Failed.reset_index(drop=True)
        NumberWindowsDB_Failed  = pd.DataFrame(NumberWindowsDB_Failed)

        ## NumberPots QC
        GearType_NumberPots= [64]
        NotinList_NumberPots =[99999999]
        NumberPotsDB_DF= (SetCatchProfileDB_DF.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                        'GearType', 'NumberPots']]).replace(['','None'], 99999999)
        NumberPotsDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberPotsDB_DF[
                        ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberPotsDB_DF[['DeploymentUID']] = NumberPotsDB_DF[['DeploymentUID']].astype(str)
        NumberPotsDB_DF[['NumberPots']] = NumberPotsDB_DF[['NumberPots']].astype(int)

        NumberPotsDB_Failed =[]
        NumberPotsDB_DF_1  = NumberPotsDB_DF[(
                            (NumberPotsDB_DF['GearType'].isin(GearType_NumberPots)) &\
                            ((NumberPotsDB_DF['NumberPots'].isin(NotinList_NumberPots)))
                                )]
        
        NumberPotsDB_DF_2 = NumberPotsDB_DF[(
                        (~(NumberPotsDB_DF['GearType'].isin(GearType_NumberPots))) &\
                        (~(NumberPotsDB_DF['NumberPots'].isin(NotinList_NumberPots)))
                            )]
        
        NumberPotsDB_Failed = pd.concat([NumberPotsDB_DF_1, NumberPotsDB_DF_2])
        NumberPotsDB_Failed= (NumberPotsDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberPots']]).replace([99999999.0, 99999999], '')
        NumberPotsDB_Failed['QCNumberPots'] ="GType[64]=>NumberPots=NoBlank, Else Blank"
        NumberPotsDB_Failed['QC_CaseType'] = 'Case-NP'
        NumberPotsDB_Failed  = NumberPotsDB_Failed.reset_index(drop=True)
        NumberPotsDB_Failed  = pd.DataFrame(NumberPotsDB_Failed)
        
        ## Submit To Presence Conditional DB Storage
        Submit_PresenceConditional_DB(AverageTowSpeedDB_Failed, CodendMeshSizeDB_Failed,
                                    MeshSizeMGDB_Failed, NumberGillnetsDB_Failed,
                                    AverageGillnetLengthDB_Failed, NumberHooksDB_Failed,
                                    NumberWindowsDB_Failed, NumberPotsDB_Failed)
        
        Length_FailedConditionalDF = (len(AverageTowSpeedDB_Failed)+\
                                    len(CodendMeshSizeDB_Failed) +\
                                    len(MeshSizeMGDB_Failed)+\
                                    len(NumberGillnetsDB_Failed) +\
                                    len(AverageGillnetLengthDB_Failed)+\
                                    len(NumberHooksDB_Failed) +\
                                    len(NumberWindowsDB_Failed) +\
                                    len(NumberPotsDB_Failed)
                                    )
        return Length_FailedConditionalDF
    
    def GenStartSummaryQC():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        cursor = conn.cursor()
        AverageTowSpeed_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed;", conn)
        CodendMeshSize_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize;", conn)
        MeshSizeMG_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG;", conn)
        NumberGillnets_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets;", conn)
        AverageGillnetLength_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength;", conn)
        NumberHooks_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks;", conn)
        NumberWindows_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows;", conn)
        NumberPots_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots;", conn)
        cursor.close()
        conn.close()

        AverageTowSpeed_df = (pd.DataFrame(AverageTowSpeed_df))
        CodendMeshSize_df = (pd.DataFrame(CodendMeshSize_df))
        MeshSizeMG_df = (pd.DataFrame(MeshSizeMG_df))
        NumberGillnets_df = (pd.DataFrame(NumberGillnets_df))
        AverageGillnetLength_df = (pd.DataFrame(AverageGillnetLength_df))
        NumberHooks_df = (pd.DataFrame(NumberHooks_df))
        NumberWindows_df = (pd.DataFrame(NumberWindows_df))
        NumberPots_df = (pd.DataFrame(NumberPots_df))
        
        Len_AverageTowSpeed_df = len((AverageTowSpeed_df))
        Len_CodendMeshSize_df = len((CodendMeshSize_df))
        Len_MeshSizeMG_df = len((MeshSizeMG_df))
        Len_NumberGillnets_df = len((NumberGillnets_df))
        Len_AverageGillnetLength_df = len((AverageGillnetLength_df))
        Len_NumberHooks_df = len((NumberHooks_df))
        Len_NumberWindows_df = len((NumberWindows_df))
        Len_NumberPots_df = len((NumberPots_df))

        QC_CaseUpdateMsg = 'Case-Updated'
        Update_AverageTowSpeed_df = len(AverageTowSpeed_df[
                        ((AverageTowSpeed_df.QC_CaseType) == QC_CaseUpdateMsg)])
        Update_CodendMeshSize_df = len(CodendMeshSize_df[
                        ((CodendMeshSize_df.QC_CaseType) == QC_CaseUpdateMsg)])
        Update_MeshSizeMG_df = len(MeshSizeMG_df[
                        ((MeshSizeMG_df.QC_CaseType) == QC_CaseUpdateMsg)])
        Update_NumberGillnets_df = len(NumberGillnets_df[
                        ((NumberGillnets_df.QC_CaseType) == QC_CaseUpdateMsg)])
        Update_AverageGillnetLength_df = len(AverageGillnetLength_df[
                        ((AverageGillnetLength_df.QC_CaseType) == QC_CaseUpdateMsg)])
        Update_NumberHooks_df = len(NumberHooks_df[
                        ((NumberHooks_df.QC_CaseType) == QC_CaseUpdateMsg)])
        Update_NumberWindows_df = len(NumberWindows_df[
                        ((NumberWindows_df.QC_CaseType) == QC_CaseUpdateMsg)])
        Update_NumberPots_df = len(NumberPots_df[
                        ((NumberPots_df.QC_CaseType) == QC_CaseUpdateMsg)])
 
        ListVariableName = ['AverageTowSpeed','CodendMeshSize',
                            'MeshSizeMG','NumberGillnets',
                            'AverageGillnetLength','NumberHooks',
                            'NumberWindows', 'NumberPots']
        QCFailCount = [Len_AverageTowSpeed_df, Len_CodendMeshSize_df, 
                       Len_MeshSizeMG_df, Len_NumberGillnets_df,
                       Len_AverageGillnetLength_df, Len_NumberHooks_df, 
                       Len_NumberWindows_df, Len_NumberPots_df]
        QCUpdateCount = [Update_AverageTowSpeed_df, Update_CodendMeshSize_df, 
                       Update_MeshSizeMG_df, Update_NumberGillnets_df,
                       Update_AverageGillnetLength_df, Update_NumberHooks_df, 
                       Update_NumberWindows_df, Update_NumberPots_df]
        
        QCFailAppend = {'VariableName': ListVariableName, 
                        'QCFailCount': QCFailCount,
                        'QCUpdateCount': QCUpdateCount} 
        QCFailSummaryDF = pd.DataFrame(QCFailAppend)
        if len(QCFailSummaryDF) >0:
            QCFailSummaryDF[['QCFailCount', 'QCUpdateCount']] = QCFailSummaryDF[['QCFailCount', 'QCUpdateCount']].astype(int)
            QCFailSummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
            QCFailSummaryDF = QCFailSummaryDF.reset_index(drop=True)
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
    
    # # Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    ## ComboBox Select
    entry_UpdateVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable1)
    entry_SearchVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable2)
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ## Gen Summary
    QCFailedtotalEntries()
    GenStartSummaryQC()

    ## Button Frame Wizard :
    btnViewQCFailedQCResults = Button(TopFrame, text="View Selected Results", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=18, bd=1, command = viewQCFailed_VariablesProfile)
    btnViewQCFailedQCResults.grid(row =1, column = 1, padx=365, pady =2, ipady =2, sticky =W)

    btnClearTable = Button(TopFrame, text="Clear Table", font=('aerial', 10, 'bold'), bg='alice blue',
                             height =1, width=10, bd=1, command = ClearTablesAll)
    btnClearTable.grid(row =1, column = 1, padx=270, pady =2, ipady =2, sticky =E)

    btnSearchDepSetCatchDB = Button(TopFrame, text="Search Deployment", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=20, bd=1, command = SearchDepNumFromSetCatchDB)
    btnSearchDepSetCatchDB.grid(row =1, column = 1, padx=20, pady =2, ipady =2, sticky =E)

    
    ### Buttons On Update Frame
    button_UpdateSelectedDBEntries = Button(UpdateDB_Entryframe, bd = 2, text ="Update Selected Table Entries\n (DB Update)", width = 25,
                                height=2, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =UpdateSelected_SetCatch_DBEntries)
    button_UpdateSelectedDBEntries.grid(row =14, column = 0, padx=10, pady =5, ipady =4, sticky =W)

    button_Clear_EntriesUpdate = Button(UpdateDB_Entryframe, bd = 1, text ="Clear Entries", width = 11,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearUpdateEntries)
    button_Clear_EntriesUpdate.grid(row =6, column = 0, padx=5, pady =2, ipady =1, sticky =E)

    ### Buttons On Search Frame
    button_SearchSingleVariableQuery = Button(SearchDB_Entryframe, bd = 2, text ="Run Single Variable Search\n (DB Search) ", width = 26,
                                height=2, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunSingleVariableSearchQuery)
    button_SearchSingleVariableQuery.grid(row =14, column = 0, padx=2, pady =6, ipady =6, sticky =W)

    button_Clear_EntriesSearch = Button(SearchDB_Entryframe, bd = 1, text ="Clear Entries", width = 11,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearSearchEntries)
    button_Clear_EntriesSearch.grid(row =3, column = 0, padx=5, pady =2, ipady =1, sticky =E)

    ## Buttons On Generate QC Failed Summary Frame
    button_GenSummaryQC = Button(Summaryframe, bd = 1, text ="Generate QC Summary ", width = 20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSummaryQC)
    button_GenSummaryQC.pack(side =TOP, anchor = CENTER)
    button_ClrSelView = Button(SummaryDisplay, bd = 1, text ="Clear Summary", width = 13,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearSummary)
    button_ClrSelView.pack(side =TOP, anchor = W)

    button_GenDepQCSummary = Button(SelQCVariableDisplay, bd = 1, text ="Deployment Summary", width = 19,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenDeploymentSummary)
    button_GenDepQCSummary.grid(row =0, column = 1, padx=50, pady =2, ipady =2, sticky =W)

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
    ImportExport.add_command(label="Export Failed Results (.csv)", command=Export_FailedCSV)
    ImportExport.add_command(label="Import & Update DB (.csv)", command=ImportAndUpdateSetCatchDB)
    View.add_command(label="View Edit & Update QCFailed Results", command=QCFailedExcelViewAll)
    View.add_command(label="Ref-QCFail To Set&Catch DB", command=RefFailedToSetcatchDB)
    Update.add_command(label="Update SetCatch DB DeplymentUID", command=UpdateDeploymentUIDAfterUpdate)
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack()
    window.mainloop()

