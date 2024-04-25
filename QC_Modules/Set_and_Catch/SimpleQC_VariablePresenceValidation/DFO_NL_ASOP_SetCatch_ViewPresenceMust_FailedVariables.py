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

def ViewPresenceMustValidatedResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Presence Validator ID-C-03-0")
    window.geometry("1480x805+200+100")
    window.config(bg="cadet blue")

    ## Top Frame
    TopFrame = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    TopFrame.pack(side = TOP, padx= 0, pady=0)
    lbl_TopFrame = Label(TopFrame, font=('aerial', 10, 'bold'), text="A. QC Fail Table (Null Variable QC) :")
    lbl_TopFrame.grid(row =1, column = 0, padx=2, pady =1, ipady=1, sticky =W)

    ListVariableListA = ['Select Variable Presence View Type', 
                         'View Not Null Variable Fail With RecType-1,2',
                         'View Not Null Variable Fail With RecType-1 Only']
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

    ListFilterBy = ['View Both RecType-1&2', 
                    'View RecType 1 Only']
    FilterByList        = StringVar(TopFrame, value ='')
    entry_FilterByList  = ttk.Combobox(TopFrame, font=('aerial', 8, 'bold'), justify = tk.LEFT,
                                        textvariable =FilterByList, width = 24, state='disabled')
    entry_FilterByList.grid(row =1, column = 2, padx=1, pady =4, ipady= 4, sticky =W)
    entry_FilterByList['values'] = ListFilterBy
    entry_FilterByList.current(1)

    lbl_TotalFailedEntries = Label(TopFrame, font=('aerial', 10 , 'bold'), text="# Of Set Failed :")
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
                    "column5", "column6", "column7", "column8",
                    "column9", "column10", "column11", "column12", 
                    "column13", "column14", "column15", "column16",
                    "column17", "column18", "column19", "column20", 
                    "column21", "column22", "column23", "column24",
                    "column25", "column26", "column27", "column28", 
                    "column29", "column30", "column31", "column32",
                    "column33"), height=21, show='headings')
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
    tree1.heading("#3", text="DeploymentUID-CI-0", anchor=CENTER)
    tree1.heading("#4", text="ASOCCode", anchor=CENTER)
    tree1.heading("#5", text="ObserverNumber", anchor=CENTER)
    tree1.heading("#6", text="Year", anchor=CENTER)
    tree1.heading("#7", text="DeploymentNumber", anchor=CENTER)
    tree1.heading("#8", text="SubTripNumber-CI-5", anchor=CENTER)
    tree1.heading("#9", text="SetNumber", anchor=CENTER)
    tree1.heading("#10", text="Country", anchor=CENTER)
    tree1.heading("#11", text="Quota", anchor=CENTER)
    tree1.heading("#12", text="SetType", anchor=CENTER)
    tree1.heading("#13", text="VesselSideNumber-CI-10", anchor=CENTER)
    tree1.heading("#14", text="VesselClass", anchor=CENTER)
    tree1.heading("#15", text="Day", anchor=CENTER)
    tree1.heading("#16", text="Month", anchor=CENTER)
    tree1.heading("#17", text="HaulDay", anchor=CENTER)
    tree1.heading("#18", text="HaulMonth-CI-15", anchor=CENTER)
    tree1.heading("#19", text="StartTime", anchor=CENTER)
    tree1.heading("#20", text="Duration", anchor=CENTER)
    tree1.heading("#21", text="PositionPrecision", anchor=CENTER)
    tree1.heading("#22", text="StartLatitude", anchor=CENTER)
    tree1.heading("#23", text="StartLongitude-CI-20", anchor=CENTER)
    tree1.heading("#24", text="EndLatitude", anchor=CENTER)
    tree1.heading("#25", text="EndLongitude", anchor=CENTER)
    tree1.heading("#26", text="InOut200MileLimit", anchor=CENTER)
    tree1.heading("#27", text="NAFODivision", anchor=CENTER)
    tree1.heading("#28", text="GearType-CI-25", anchor=CENTER)
    tree1.heading("#29", text="RecordType", anchor=CENTER)
    tree1.heading("#30", text="DetailedCatchSpeciesCompCode", anchor=CENTER)
    tree1.heading("#31", text="DirectedSpecies", anchor=CENTER)
    tree1.heading("#32", text="AverageDepth", anchor=CENTER)
    tree1.heading("#33", text="DataSource-CI-30", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=60, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree1.column('#9', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#10', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    tree1.column('#11', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)            
    tree1.column('#12', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    tree1.column('#13', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#14', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#15', stretch=NO, minwidth=0, width=50, anchor = tk.CENTER)
    tree1.column('#16', stretch=NO, minwidth=0, width=50, anchor = tk.CENTER)
    tree1.column('#17', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)            
    tree1.column('#18', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree1.column('#19', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#20', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#21', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#22', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#23', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)            
    tree1.column('#24', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#25', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#26', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree1.column('#27', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#28', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#29', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#30', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree1.column('#31', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)            
    tree1.column('#32', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    tree1.column('#33', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    style = ttk.Style(Tableframe)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 8), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
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

    ListUpdateVar = ['ASOCCode','ObserverNumber','Year',
                    'DeploymentNumber','SubTripNumber','SetNumber',
                    'Country','Quota','SetType',
                    'VesselSideNumber','VesselClass','Day', 
                    'Month', 'HaulDay',  'HaulMonth',
                    'StartTime','Duration','PositionPrecision',
                    'StartLatitude','StartLongitude','EndLatitude', 
                    'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                    'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                    'DirectedSpecies', 'AverageDepth',
                    'DataSource']
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

    ######  Frame Of Search Modules ######
    SearchDB_Entryframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SearchDB_Entryframe.pack(side =LEFT, padx=10, pady =2)

    lbl_SearchDB_Header = Label(SearchDB_Entryframe, font=('aerial', 12, 'bold','underline'), 
                                bg= "cadet blue", text="Search Database:")
    lbl_SearchDB_Header.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_SelectSinglevariableSearch_A = Label(SearchDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Variable :")
    lbl_SelectSinglevariableSearch_A.grid(row =3, column = 0, padx=2, pady =1, ipady= 4, sticky =W)

    ListVariableSearch = ['DeploymentUID','ASOCCode','ObserverNumber','Year',
                            'DeploymentNumber','SubTripNumber','SetNumber',
                            'Country','Quota','SetType',
                            'VesselSideNumber','VesselClass','Day', 
                            'Month', 'HaulDay',  'HaulMonth',
                            'StartTime','Duration','PositionPrecision',
                            'StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                            'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                            'DirectedSpecies', 'AverageDepth',
                            'DataSource']
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
    Summaryframetree.heading("#1", text="Column Index (CI)", anchor = tk.CENTER)
    Summaryframetree.heading("#2", text="QC Variable Name", anchor = W)
    Summaryframetree.heading("#3", text="Null Entries Count", anchor = tk.CENTER)
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=200, anchor = W)            
    Summaryframetree.column('#3', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    Summaryframetree.pack(side = BOTTOM)
    
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    SelectViewFilter = ['RecType-1&2', 
                        'RecType 1 Only']
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
    SelResultOverviewtree.heading("#4", text="# Of Null", anchor=CENTER)
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)             
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=90, anchor = tk.CENTER)
    SelResultOverviewtree.column('#4', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = BOTTOM)

    ## Define Functions
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','Year',
                            'DeploymentNumber','SubTripNumber','SetNumber',
                            'Country','Quota','SetType',
                            'VesselSideNumber','VesselClass','Day', 
                            'Month', 'HaulDay',  'HaulMonth',
                            'StartTime','Duration','PositionPrecision',
                            'StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                            'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                            'DirectedSpecies', 'AverageDepth',
                            'DataSource']
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
                        ASOCCode                    = (df.loc[:,'ASOCCode']).fillna(99999999).astype(int, errors='ignore')
                        ObserverNumber              = (df.loc[:,'ObserverNumber']).fillna(8888888).astype(int, errors='ignore')
                        Year                        = (df.loc[:,'Year']).fillna(99999999).astype(int, errors='ignore')
                        DeploymentNumber            = (df.loc[:,'DeploymentNumber']).fillna(99999999).astype(int, errors='ignore')
                        SubTripNumber               = (df.loc[:,'SubTripNumber']).fillna(8888888).astype(int, errors='ignore')
                        SetNumber                   = (df.loc[:,'SetNumber']).fillna(99999999).astype(int, errors='ignore')
                        Country                     = (df.loc[:,'Country']).fillna(99999999).astype(int, errors='ignore')
                        Quota                       = (df.loc[:,'Quota']).fillna(99999999).astype(int, errors='ignore')
                        SetType                     = (df.loc[:,'SetType']).fillna(99999999).astype(int, errors='ignore')                
                        VesselSideNumber            = (df.loc[:,'VesselSideNumber']).fillna(9999999991).astype(str, errors='ignore')
                        VesselClass                 = (df.loc[:,'VesselClass']).fillna(99999999).astype(int, errors='ignore')
                        Day                         = (df.loc[:,'Day']).fillna(99999999).astype(int, errors='ignore')
                        Month                       = (df.loc[:,'Month']).fillna(99999999).astype(int, errors='ignore')
                        HaulDay                     = (df.loc[:,'HaulDay']).fillna(99999999).astype(int, errors='ignore')
                        HaulMonth                   = (df.loc[:,'HaulMonth']).fillna(99999999).astype(int, errors='ignore')
                        StartTime                   = (df.loc[:,'StartTime']).fillna(99999999).astype(int, errors='ignore')
                        Duration                    = (df.loc[:,'Duration']).fillna(99999999).astype(float, errors='ignore')
                        PositionPrecision           = (df.loc[:,'PositionPrecision']).fillna(99999999).astype(int, errors='ignore')
                        StartLatitude               = (df.loc[:,'StartLatitude']).fillna(99999999).astype(float, errors='ignore')
                        StartLongitude              = (df.loc[:,'StartLongitude']).fillna(99999999).astype(float, errors='ignore')
                        EndLatitude                 = (df.loc[:,'EndLatitude']).fillna(99999999).astype(float, errors='ignore')
                        EndLongitude                = (df.loc[:,'EndLongitude']).fillna(99999999).astype(float, errors='ignore')
                        InOut200MileLimit           = (df.loc[:,'InOut200MileLimit']).fillna(99999999).astype(int, errors='ignore')
                        NAFODivision                = (df.loc[:,'NAFODivision']).fillna(8888888).astype(int, errors='ignore')
                        GearType                    = (df.loc[:,'GearType']).fillna(99999999).astype(int, errors='ignore')
                        RecordType                  = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        DetailedCatchSpeciesCompCode= (df.loc[:,'DetailedCatchSpeciesCompCode']).fillna(99999999).astype(str, errors='ignore')
                        DirectedSpecies             = (df.loc[:,'DirectedSpecies']).fillna(99999999).astype(int, errors='ignore')
                        AverageDepth                = (df.loc[:,'AverageDepth']).fillna(99999999).astype(int, errors='ignore')
                        DataSource                  = (df.loc[:,'DataSource']).fillna(99999999).astype(int, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID,\
                                        ASOCCode,ObserverNumber, Year,\
                                        DeploymentNumber, SubTripNumber, SetNumber,\
                                        Country, Quota, SetType,\
                                        VesselSideNumber,VesselClass,Day, \
                                        Month, HaulDay,  HaulMonth,\
                                        StartTime, Duration, PositionPrecision,\
                                        StartLatitude, StartLongitude, EndLatitude,\
                                        EndLongitude, InOut200MileLimit,  NAFODivision,\
                                        GearType,RecordType, DetailedCatchSpeciesCompCode,\
                                        DirectedSpecies, AverageDepth,\
                                        DataSource]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns=  {0:'DataBase_ID',1: 'RecordIdentifier',2: 'DeploymentUID',
                                                3:'ASOCCode',   4:'ObserverNumber',   5:'Year', 
                                                6:'DeploymentNumber', 7:'SubTripNumber', 8:'SetNumber', 
                                                9:'Country', 10:'Quota', 11:'SetType', 
                                                12:'VesselSideNumber', 13:'VesselClass', 14:'Day', 
                                                15:'Month', 16:'HaulDay', 17:'HaulMonth', 
                                                18:'StartTime', 19:'Duration', 20:'PositionPrecision',
                                                21:'StartLatitude', 22:'StartLongitude', 23:'EndLatitude', 
                                                24:'EndLongitude', 25:'InOut200MileLimit', 26:'NAFODivision', 
                                                27:'GearType', 28:'RecordType', 29:'DetailedCatchSpeciesCompCode',
                                                30:'DirectedSpecies', 31:'AverageDepth',
                                                32:'DataSource',   
                                            },inplace = True)
                        Raw_Imported_Df = pd.DataFrame(catdf)
                        Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0, '.', 'Null'], '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([8888888, '8888888', '.','Null'], 'None')
                        Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                        Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                        CheckEmptyNessColumn = Raw_Imported_Df[
                                            (Raw_Imported_Df.DataBase_ID=='') |
                                            (Raw_Imported_Df.RecordIdentifier=='') |
                                            (Raw_Imported_Df.DeploymentUID=='None') |
                                            (Raw_Imported_Df.DeploymentUID=='') |
                                            
                                            (Raw_Imported_Df.ASOCCode=='')|
                                            (Raw_Imported_Df.ObserverNumber=='')|
                                            (Raw_Imported_Df.ObserverNumber=='None')|
                                            (Raw_Imported_Df.Year=='')|

                                            (Raw_Imported_Df.DeploymentNumber=='') |
                                            (Raw_Imported_Df.SubTripNumber=='') |
                                            (Raw_Imported_Df.SubTripNumber=='None') |
                                            (Raw_Imported_Df.SetNumber=='')|

                                            (Raw_Imported_Df.Country=='')|
                                            (Raw_Imported_Df.Quota=='')|
                                            (Raw_Imported_Df.SetType=='') |

                                            (Raw_Imported_Df.VesselSideNumber=='') |
                                            (Raw_Imported_Df.VesselSideNumber=='None') |
                                            (Raw_Imported_Df.VesselClass=='')|
                                            (Raw_Imported_Df.Day=='')|

                                            (Raw_Imported_Df.Month=='')|
                                            (Raw_Imported_Df.HaulDay=='') |
                                            (Raw_Imported_Df.HaulMonth=='') |
                                            
                                            (Raw_Imported_Df.StartTime=='')|
                                            (Raw_Imported_Df.Duration=='')|
                                            (Raw_Imported_Df.PositionPrecision=='')|
                                            
                                            (Raw_Imported_Df.StartLatitude=='')|
                                            (Raw_Imported_Df.StartLongitude=='')|
                                            (Raw_Imported_Df.EndLatitude=='')|

                                            (Raw_Imported_Df.EndLongitude=='')|
                                            (Raw_Imported_Df.InOut200MileLimit=='')|
                                            (Raw_Imported_Df.NAFODivision=='None')|
                                            (Raw_Imported_Df.NAFODivision=='')|

                                            (Raw_Imported_Df.GearType=='')|
                                            (Raw_Imported_Df.RecordType=='')|
                                            (Raw_Imported_Df.DirectedSpecies=='')|

                                            (Raw_Imported_Df.AverageDepth=='')|
                                            (Raw_Imported_Df.DataSource=='')|
                                            (Raw_Imported_Df.DetailedCatchSpeciesCompCode=='None')
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
                                list_item_ASOCCode = (rowValue[3])
                                list_item_ObserverNumber = (rowValue[4])
                                list_item_Year = (rowValue[5])
                                list_item_DeploymentNumber = (rowValue[6])
                                list_item_SubTripNumber = (rowValue[7])
                                list_item_SetNumber = (rowValue[8])
                                list_item_Country = (rowValue[9])
                                list_item_Quota = (rowValue[10])
                                list_item_SetType = (rowValue[11])

                                list_item_VesselSideNumber = (rowValue[12])
                                list_item_VesselClass = (rowValue[13])
                                list_item_Day = (rowValue[14])
                                list_item_Month = (rowValue[15])
                                list_item_HaulDay = (rowValue[16])
                                list_item_HaulMonth = (rowValue[17])
                                list_item_StartTime = (rowValue[18])
                                list_item_Duration = (rowValue[19])
                                list_item_PositionPrecision = (rowValue[20])
                                list_item_StartLatitude = (rowValue[21])
                                list_item_StartLongitude = (rowValue[22])

                                list_item_EndLatitude = (rowValue[23])
                                list_item_EndLongitude = (rowValue[24])
                                list_item_InOut200MileLimit = (rowValue[25])
                                list_item_NAFODivision = (rowValue[26])
                                list_item_GearType = (rowValue[27])
                                list_item_RecordType = (rowValue[28])
                                list_item_DetailedCatchSpeciesCompCode = (rowValue[29])
                                list_item_DirectedSpecies = (rowValue[30])
                                list_item_AverageDepth = (rowValue[31])
                                list_item_DataSource = (rowValue[32])
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_DeploymentUID,
                                                    
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_Year,

                                                    list_item_DeploymentNumber,
                                                    list_item_SubTripNumber,
                                                    list_item_SetNumber,
                                                    
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_SetType,

                                                    list_item_VesselSideNumber,
                                                    list_item_VesselClass,
                                                    list_item_Day,

                                                    list_item_Month,
                                                    list_item_HaulDay,
                                                    list_item_HaulMonth,

                                                    list_item_StartTime,
                                                    list_item_Duration,
                                                    list_item_PositionPrecision,

                                                    list_item_StartLatitude,
                                                    list_item_StartLongitude,
                                                    list_item_EndLatitude,

                                                    list_item_EndLongitude,
                                                    list_item_InOut200MileLimit,
                                                    list_item_NAFODivision,

                                                    list_item_GearType,
                                                    list_item_RecordType,
                                                    list_item_DetailedCatchSpeciesCompCode,

                                                    list_item_DirectedSpecies,
                                                    list_item_AverageDepth,
                                                    list_item_DataSource,

                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    ))
                            
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentUID =?, ASOCCode = ?, \
                                                    ObserverNumber = ?, Year = ?, DeploymentNumber = ?, SubTripNumber = ?,\
                                                    SetNumber = ?, Country = ?, Quota = ?, SetType = ?,\
                                                    VesselSideNumber = ?, VesselClass = ?, Day = ?, Month = ?,\
                                                    HaulDay = ?, HaulMonth = ?, StartTime = ?, Duration = ?,\
                                                    PositionPrecision = ?, StartLatitude = ?, StartLongitude = ?, EndLatitude = ?,\
                                                    EndLongitude = ?, InOut200MileLimit = ?, NAFODivision = ?, GearType = ?,\
                                                    RecordType = ?, DetailedCatchSpeciesCompCode = ?, DirectedSpecies = ?,\
                                                    AverageDepth = ?, DataSource = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdateRecordList_SetCatchDB)
                            cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DeploymentUID =?, ASOCCode = ?, \
                                                    ObserverNumber = ?, Year = ?, DeploymentNumber = ?, SubTripNumber = ?,\
                                                    SetNumber = ?, Country = ?, Quota = ?, SetType = ?,\
                                                    VesselSideNumber = ?, VesselClass = ?, Day = ?, Month = ?,\
                                                    HaulDay = ?, HaulMonth = ?, StartTime = ?, Duration = ?,\
                                                    PositionPrecision = ?, StartLatitude = ?, StartLongitude = ?, EndLatitude = ?,\
                                                    EndLongitude = ?, InOut200MileLimit = ?, NAFODivision = ?, GearType = ?,\
                                                    RecordType = ?, DetailedCatchSpeciesCompCode = ?, DirectedSpecies = ?,\
                                                    AverageDepth = ?, DataSource = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    UpdateRecordList_SetCatchDB)
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Presence.commit()
                            conn_DB_SetCatch_Validation_Presence.close()
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
        ListVariableListA = ['Select Variable Presence View Type', 
                         'View Not Null Variable Fail With RecType-1,2',
                         'View Not Null Variable Fail With RecType-1 Only']
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','Year',
                            'DeploymentNumber','SubTripNumber','SetNumber',
                            'Country','Quota','SetType',
                            'VesselSideNumber','VesselClass','Day', 
                            'Month', 'HaulDay',  'HaulMonth',
                            'StartTime','Duration','PositionPrecision',
                            'StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                            'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                            'DirectedSpecies', 'AverageDepth',
                            'DataSource']
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Presence)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `DataBase_ID` ASC")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows)
            rows = rows.reset_index(drop=True)
            rows.columns =DB_column_names
            if getVarnameToView == ListVariableListA[1]:
                rows = pd.DataFrame(rows)
            if getVarnameToView == ListVariableListA[2]:
                rows = rows[(rows.RecordType) == 1]
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
        ListVariableListA = ['Select Variable Presence View Type', 
                         'View Not Null Variable Fail With RecType-1,2',
                         'View Not Null Variable Fail With RecType-1 Only']
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        if len(rows) >0 :
            rows.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                 'RecordType'], inplace=True)
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
                txtDisplayMessageSystem.insert(0, 'Populated Presence Not Null Variables QC Fail Entries')
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 'Empty QC Fail DB. Nothing to Display') 

    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables;", conn)
        conn.commit()
        conn.close()
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        if len(data)>0:
            QCFailedTotalEntries = data.DeploymentUID.nunique()
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

    def Export_FailedCSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("QC Failed Presence Must Profile","QC Failed Presence Must Profile Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("QC Failed Presence Must Profile Report Message","Please Select File Name To Export")
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
            conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `DataBase_ID` ASC ;", conn)
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
            SelvariableIdentifier = sd[6]
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
        GetSetCatchDB_VariableList = ['ASOCCode','ObserverNumber','Year',
                            'DeploymentNumber','SubTripNumber','SetNumber',
                            'Country','Quota','SetType',
                            'VesselSideNumber','VesselClass','Day', 
                            'Month', 'HaulDay',  'HaulMonth',
                            'StartTime','Duration','PositionPrecision',
                            'StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                            'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                            'DirectedSpecies', 'AverageDepth',
                            'DataSource']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList,
                                        UpdateRecordList1, getSelectFilterView):
        
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        conn_Validation_Presence= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur_Validation_Presence=conn_Validation_Presence.cursor()
        SelectFilterViewList = ['RecType-1&2','RecType 1 Only']
        
        if getSelectFilterView == SelectFilterViewList[0]:
            ## Updaing SetCatch DB
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ObserverNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Year = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SubTripNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Country = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Quota = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[9]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselSideNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[10]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselClass = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[11]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Day = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Month = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulDay = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulMonth = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartTime = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Duration = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET InOut200MileLimit = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NAFODivision = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DetailedCatchSpeciesCompCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DirectedSpecies = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageDepth = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DataSource = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                

            ### Updating QC Failed DB

            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET ASOCCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET ObserverNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Year = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DeploymentNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET SubTripNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET SetNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Country = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Quota = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET SetType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[9]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET VesselSideNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[10]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET VesselClass = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[11]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Day = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Month = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET HaulDay = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET HaulMonth = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET StartTime = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Duration = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET PositionPrecision = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET StartLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET StartLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET EndLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET EndLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET InOut200MileLimit = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET NAFODivision = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET GearType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET RecordType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DetailedCatchSpeciesCompCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DirectedSpecies = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                            
            if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET AverageDepth = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DataSource = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
        
        if getSelectFilterView == SelectFilterViewList[1]:
            ## Updaing SetCatch DB
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ObserverNumber = ? WHERE DeploymentUID =?", 
                    UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Year = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SubTripNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Country = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Quota = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetType = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[9]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselSideNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[10]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselClass = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[11]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Day = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Month = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulDay = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulMonth = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartTime = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Duration = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLatitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLongitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLatitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLongitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET InOut200MileLimit = ? WHERE DeploymentUID =?", 
                    UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NAFODivision = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearType = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DetailedCatchSpeciesCompCode = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DirectedSpecies = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageDepth = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DataSource = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                

            ### Updating QC Failed DB
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET ASOCCode = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET ObserverNumber = ? WHERE DeploymentUID =?", 
                    UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Year = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DeploymentNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET SubTripNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET SetNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Country = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Quota = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET SetType = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[9]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET VesselSideNumber = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[10]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET VesselClass = ? WHERE DeploymentUID =?", 
                        (UpdateRecordList1))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[11]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Day = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Month = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET HaulDay = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET HaulMonth = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET StartTime = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET Duration = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET PositionPrecision = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET StartLatitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET StartLongitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET EndLatitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET EndLongitude = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET InOut200MileLimit = ? WHERE DeploymentUID =?", 
                    UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET NAFODivision = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET GearType = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET RecordType = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DetailedCatchSpeciesCompCode = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DirectedSpecies = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                            
            if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET AverageDepth = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                cur_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DataSource = ? WHERE DeploymentUID =?", 
                        UpdateRecordList1)
         
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Presence.commit()
        conn_Validation_Presence.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18=['ASOCCode', 'Year', 'DeploymentNumber', 
                            'SetNumber', 'Country', 'Quota', 'SetType',
                            'VesselClass','Day', 'Month','PositionPrecision',
                            'GearType','RecordType','DirectedSpecies','DataSource']
            
            Var_Class_FloatA7= ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                                'EndLongitude']
            
            Var_Class_String7 =['ObserverNumber',
                                'SubTripNumber','NAFODivision', 'VesselSideNumber',
                            'DetailedCatchSpeciesCompCode']
            
            Var_Class_IntB27  = ['HaulDay','HaulMonth', 'StartTime',
                                'InOut200MileLimit',  'AverageDepth']

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
        get_Updated_Variable = entry_UpdateVariableList.get()
        get_UpdateValue_UpdatedVariable = entry_UpdateValue_VariableA.get()
        getSelectFilterView = entry_SelectFilterView.get()
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
                        UpdateRecordList1 =[]   
                        for item in tree1.selection():
                            list_item = (tree1.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DatabaseUID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                            UpdateRecordList1.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DeploymentUID,
                                                    ))
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList,
                                                        UpdateRecordList1, getSelectFilterView)
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(tk.END,"Set & Catch Database Updated Successfully")
                        viewQCFailed_VariablesProfile()
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")
                        
                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                        iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                                                                    "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                        if iUpdateSlected >0:
                            UpdateRecordList =[]
                            UpdateRecordList1 =[]  
                            for item in tree1.selection():
                                list_item = (tree1.item(item, 'values'))
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                                UpdateRecordList1.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DeploymentUID,
                                                    ))
                            Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList,
                                                            UpdateRecordList1, getSelectFilterView)
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
        if(VariableListA=='ObserverNumber')|\
        (VariableListA=='SubTripNumber')|\
        (VariableListA=='VesselSideNumber')|\
        (VariableListA=='NAFODivision')|\
        (VariableListA=='DetailedCatchSpeciesCompCode')|\
        (VariableListA=='UnitArea'):
            EntryDataType_Variable = 'Alpha Numeric DataType'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)
        else:
            EntryDataType_Variable = 'Numeric DataType Only'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)

    def callbackFuncSelectView(event):
        ListVariableListA = ['Select Variable Presence View Type', 
                         'View Not Null Variable Fail With RecType-1,2',
                         'View Not Null Variable Fail With RecType-1 Only']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            tree1.delete(*tree1.get_children())
            
        if(SelVariableView ==ListVariableListA[0]):
            tree1.delete(*tree1.get_children())
            entry_SelectFilterView.current(0)
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'View Not Null (Must Not Empty) Variables Fail QC')
             
        if(SelVariableView ==ListVariableListA[1]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'View Not Null Variable Fail QC - Both RecordType-1 & 2')
            entry_SelectFilterView.current(0)

        if(SelVariableView ==ListVariableListA[2]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'View Not Null Variable Fail QC - RecordType-1 Only')
            entry_SelectFilterView.current(1)
            
    def Combo_input_ASOCCode():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT ASOCCode FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_ObserverNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT ObserverNumber FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Year():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT Year FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Day():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT Day FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT DeploymentNumber FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SetNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT SetNumber FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentUID():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT DeploymentUID FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Country():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT Country FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Quota():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT Quota FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SetType():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT SetType FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SubTripNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT SubTripNumber FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_VesselSideNumber():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT VesselSideNumber FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_VesselClass():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT VesselClass FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_PositionPrecision():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT PositionPrecision FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NAFODivision():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT NAFODivision FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_GearType():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT GearType FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DataSource():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT DataSource FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DirectedSpecies():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT DirectedSpecies FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_RecordType():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT RecordType FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DetailedCatchSpeciesCompCode():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT DetailedCatchSpeciesCompCode FROM SetCatch_QCFailedPresence_MustVariables")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Month():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT Month FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `Month` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_InOut200MileLimit():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT InOut200MileLimit FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `InOut200MileLimit` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_HaulDay():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT HaulDay FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `HaulDay` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_HaulMonth():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT HaulMonth FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `HaulMonth` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_StartTime():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT StartTime FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `StartTime` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Duration():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT Duration FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `Duration` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_AverageDepth():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT AverageDepth FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `AverageDepth` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_StartLatitude():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT StartLatitude FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `StartLatitude` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_StartLongitude():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT StartLongitude FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `StartLongitude` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_EndLatitude():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT EndLatitude FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `EndLatitude` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_EndLongitude():
        con= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=con.cursor()
        cur.execute("SELECT EndLongitude FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `EndLongitude` ASC ;")
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
        
        if VariableListA == 'ASOCCode':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_ASOCCode())))])
        if VariableListA == 'ObserverNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_ObserverNumber())))])
        if VariableListA == 'Year':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_Year())))])
        if VariableListA == 'DeploymentNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_DeploymentNumber())))])
        if VariableListA == 'SubTripNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_SubTripNumber())))])
        if VariableListA == 'SetNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_SetNumber())))])
        if VariableListA == 'Country':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_Country())))])
        if VariableListA == 'Quota':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_Quota())))])
        if VariableListA == 'SetType':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_SetType())))])
        if VariableListA == 'VesselSideNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_VesselSideNumber())))])
        if VariableListA == 'VesselClass':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_VesselClass())))])

        if VariableListA == 'Day':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_Day())))])
        if VariableListA == 'Month':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_Month())))])
        if VariableListA == 'HaulDay':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_HaulDay())))])
        if VariableListA == 'HaulMonth':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_HaulMonth())))])
        if VariableListA == 'StartTime':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_StartTime())))])
        if VariableListA == 'Duration':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_Duration())))])
        if VariableListA == 'PositionPrecision':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_PositionPrecision())))])
        if VariableListA == 'StartLatitude':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_StartLatitude())))])
        if VariableListA == 'StartLongitude':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_StartLongitude())))])
        if VariableListA == 'EndLatitude':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_EndLatitude())))])
    
        if VariableListA == 'EndLongitude':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_EndLongitude())))])
        if VariableListA == 'InOut200MileLimit':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_InOut200MileLimit())))])
        if VariableListA == 'NAFODivision':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_NAFODivision())))]) 
        if VariableListA == 'GearType':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_GearType())))])
        if VariableListA == 'RecordType':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_RecordType())))])
        if VariableListA == 'DataSource':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_DataSource())))])
        if VariableListA == 'DirectedSpecies':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_DirectedSpecies())))])
        if VariableListA == 'DetailedCatchSpeciesCompCode':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_DetailedCatchSpeciesCompCode())))])
        if VariableListA == 'AverageDepth':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_AverageDepth())))])
        
    def SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value):
        ListVariableSearch = ['DeploymentUID','ASOCCode','ObserverNumber','Year',
                            'DeploymentNumber','SubTripNumber','SetNumber',
                            'Country','Quota','SetType',
                            'VesselSideNumber','VesselClass','Day', 
                            'Month', 'HaulDay',  'HaulMonth',
                            'StartTime','Duration','PositionPrecision',
                            'StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                            'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                            'DirectedSpecies', 'AverageDepth',
                            'DataSource']
        conn= sqlite3.connect(DB_SetCatch_Validation_Presence)
        cur=conn.cursor()

        if get_SearchSingleVariable == ListVariableSearch[0]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE DeploymentUID = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[1]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE ASOCCode = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[2]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE ObserverNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[3]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE Year = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[4]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE DeploymentNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[5]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE SubTripNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[6]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE SetNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[7]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE Country = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[8]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE Quota = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[9]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE SetType = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[10]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE VesselSideNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[11]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE VesselClass = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[12]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE Day = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[13]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE Month = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[14]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE HaulDay = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[15]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE HaulMonth = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[16]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE StartTime = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[17]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE Duration = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[18]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE PositionPrecision = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[19]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE StartLatitude = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[20]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE StartLongitude = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[21]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE EndLatitude = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[22]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE EndLongitude = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[23]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE InOut200MileLimit = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[24]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE NAFODivision = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[25]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE GearType = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[26]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE RecordType = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[27]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE DetailedCatchSpeciesCompCode = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[28]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE DirectedSpecies = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[29]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE AverageDepth = ?", (get_SearchSingleVariable_Value,))
            rows=cur.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[30]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur.execute("SELECT * FROM SetCatch_QCFailedPresence_MustVariables WHERE DataSource = ?", (get_SearchSingleVariable_Value,))
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
                                                3:'ASOCCode',   4:'ObserverNumber',   5:'Year', 
                                                6:'DeploymentNumber', 7:'SubTripNumber', 8:'SetNumber', 
                                                9:'Country', 10:'Quota', 11:'SetType', 
                                                12:'VesselSideNumber', 13:'VesselClass', 14:'Day', 
                                                15:'Month', 16:'HaulDay', 17:'HaulMonth', 
                                                18:'StartTime', 19:'Duration', 20:'PositionPrecision',
                                                21:'StartLatitude', 22:'StartLongitude', 23:'EndLatitude', 
                                                24:'EndLongitude', 25:'InOut200MileLimit', 26:'NAFODivision', 
                                                27:'GearType', 28:'RecordType', 29:'DetailedCatchSpeciesCompCode',
                                                30:'DirectedSpecies', 31:'AverageDepth',
                                                32:'DataSource'},inplace = True)
            
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
            LenGenSummaryQC = RunPresenceMust_FailedVariables()
        except:
            print('Error Occured In Generating QC Summary')
        finally:
            if LenGenSummaryQC > -1 :
                ListVariables = ['ASOCCode','ObserverNumber','Year',
                                'DeploymentNumber','SubTripNumber','SetNumber',
                                'Country','Quota','SetType',
                                'VesselSideNumber','VesselClass','Day', 
                                'Month', 'HaulDay',  'HaulMonth',
                                'StartTime','Duration','PositionPrecision',
                                'StartLatitude','StartLongitude','EndLatitude', 
                                'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                                'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                                'DirectedSpecies', 'AverageDepth',
                                'DataSource']
                ListVarIndex = list(range(1,len(ListVariables)+1))
                conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables;", conn)
                cursor.close()
                conn.close()
                if len(Complete_df) >0:
                    SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                    QCFailVarAppend = []
                    QCFailNullCount = []
                    
                    for List in ListVariables:
                        Count = len((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[List]=="Null"]))
                        ListName = str(List)
                        NullCount = str (Count) 
                        QCFailVarAppend.append(ListName)
                        QCFailNullCount.append(NullCount)
                    
                    QCFailAppend = {'ColumnIndex': ListVarIndex,
                                    'VariableName': QCFailVarAppend,
                                    'NullCount': QCFailNullCount} 
                    QCFailSummaryDF = pd.DataFrame(QCFailAppend)
                    QCFailSummaryDF[['NullCount']] = QCFailSummaryDF[['NullCount']].astype(int)
                    QCFailSummaryDF.sort_values(by=['NullCount', 'ColumnIndex'], inplace=True, ascending=False)
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

    def GenStartSummaryQC():
        ListVariables = ['ASOCCode','ObserverNumber','Year',
                        'DeploymentNumber','SubTripNumber','SetNumber',
                        'Country','Quota','SetType',
                        'VesselSideNumber','VesselClass','Day', 
                        'Month', 'HaulDay',  'HaulMonth',
                        'StartTime','Duration','PositionPrecision',
                        'StartLatitude','StartLongitude','EndLatitude', 
                        'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                        'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                        'DirectedSpecies', 'AverageDepth',
                        'DataSource']
        ListVarIndex = list(range(1,len(ListVariables)+1))
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        cursor = conn.cursor()
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables;", conn)
        cursor.close()
        conn.close()
        if len(Complete_df) >0:
            SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
            QCFailVarAppend = []
            QCFailNullCount = []
            
            for List in ListVariables:
                Count = len((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[List]=="Null"]))
                ListName = str(List)
                NullCount = str (Count) 
                QCFailVarAppend.append(ListName)
                QCFailNullCount.append(NullCount)
            
            QCFailAppend = {'ColumnIndex': ListVarIndex,
                            'VariableName': QCFailVarAppend,
                            'NullCount': QCFailNullCount} 
            QCFailSummaryDF = pd.DataFrame(QCFailAppend)
            QCFailSummaryDF[['NullCount']] = QCFailSummaryDF[['NullCount']].astype(int)
            QCFailSummaryDF.sort_values(by=['NullCount', 'ColumnIndex'], inplace=True, ascending=False)
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
        nm = Summaryframetree.selection()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableIdentifier = sd[1]
            NullCountSelectedVar = sd[2]
            entry_SelQCVariable.delete(0,END)
            entry_SelQCVariable.insert(tk.END, (SelvariableIdentifier))
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END,(("Variable Select :") + \
            SelvariableIdentifier + "-- Null Count -- " + NullCountSelectedVar))
            SelectAndViewQCSummary()
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END, (' Please Select Only One Entries To View'))
    
    def SelectAndViewQCSummary():
        ListVariableListA = ['RecType-1&2', 
                            'RecType 1 Only']
        nm = Summaryframetree.selection()
        getVarnameToView = entry_SelectFilterView.get()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableIdentifier = sd[1]
            conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables ;", conn)
            cursor.close()
            conn.close()
            
            if getVarnameToView == ListVariableListA[0]:
                QCFailDF  = pd.DataFrame(Complete_df)
                tree1.delete(*tree1.get_children())
                QCFailDF_Selected = QCFailDF[(
                (QCFailDF[SelvariableIdentifier] == 'Null') 
                )]
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
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(tk.END, ('Populated Null Variable Fail -' + SelvariableIdentifier + '- Showing RecordType 1 and 2'))
            
            if getVarnameToView == ListVariableListA[1]:
                QCFailDF = Complete_df[
                                (Complete_df.RecordType) == 1]
                QCFailDF = QCFailDF.reset_index(drop=True)
                QCFailDF = pd.DataFrame(QCFailDF)
                tree1.delete(*tree1.get_children())
                QCFailDF_Selected = QCFailDF[(
                (QCFailDF[SelvariableIdentifier] == 'Null') 
                )]
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
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(tk.END, ('Populated Null Variable Fail -' + SelvariableIdentifier +'- Showing RecordType 1 Only'))

    def SearchDepNumFromSetCatchDB():
        ListFilterBy = ['View Both RecType-1&2', 
                        'View RecType 1 Only']
        try:
            get_DepNumforSearch = int(entry_DepNumforSearch.get())
        except:
            messagebox.showerror('Search Variable Datatype Error Message', "Search Value Must Be Integer Value")
        checkinttype = isinstance(get_DepNumforSearch,int)
        if checkinttype == True:  
            getVarnameToView_1 = entry_FilterByList.get()
            conn_DB= sqlite3.connect(DB_Set_Catch_Analysis)
            if (get_DepNumforSearch) >= 0:
                if (getVarnameToView_1 == ListFilterBy[0]):           
                    get_SearchSingleVariable_Value = (get_DepNumforSearch)
                    rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                    conn_DB.commit()
                    conn_DB.close() 
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
                    rows = rows[(rows.DeploymentNumber) == get_SearchSingleVariable_Value]
                    rows  = rows.reset_index(drop=True)
                    QC_FailPresence_DF  = pd.DataFrame(rows)
                    ExcelViewEditBackend_RecType_1_2(QC_FailPresence_DF, get_SearchSingleVariable_Value)
                
                if (getVarnameToView_1 == ListFilterBy[1]):           
                    get_SearchSingleVariable_Value = (get_DepNumforSearch)
                    rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                    conn_DB.commit()
                    conn_DB.close()  
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
                    rows = rows[((rows.DeploymentNumber) == get_SearchSingleVariable_Value)&\
                                ((rows.RecordType) == 1)]
                    rows  = rows.reset_index(drop=True)
                    QC_FailPresence_DF  = pd.DataFrame(rows)
                    ExcelViewEditBackend_RecType_1_Only(QC_FailPresence_DF, get_SearchSingleVariable_Value)
                      
    def ExcelViewEditBackend_RecType_1_2(QC_FailPresence_DF):
        if len(QC_FailPresence_DF) >0:
            QC_FailPresence_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                                    'RecordType'], inplace=True)
            QC_FailPresence_DF  = QC_FailPresence_DF.reset_index(drop=True)
            QC_FailPresence_DF  = pd.DataFrame(QC_FailPresence_DF)   
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0,'Viewing Searched QC Failed Excel File In Seperate Window')
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = QC_FailPresence_DF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(QC_FailPresence_DF),2), clr='lightblue', cols='all')
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
                conn_DB_SetCatch_Validation_Presence= sqlite3.connect(DB_SetCatch_Validation_Presence)
                cur_DB_SetCatch_Validation_Presence=conn_DB_SetCatch_Validation_Presence.cursor()
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList_QCFailDB =[]
                df_rows = Complete_df.to_numpy().tolist()
                for row in df_rows:
                    rowValue = row
                    list_item_DataBase_ID = int(rowValue[0])
                    list_item_RecordIdentifier = int(rowValue[1])
                    list_item_DeploymentUID = (rowValue[2])
                    list_item_ASOCCode = (rowValue[3])
                    list_item_ObserverNumber = (rowValue[4])
                    list_item_Year = (rowValue[5])
                    list_item_DeploymentNumber = (rowValue[6])
                    list_item_SubTripNumber = (rowValue[7])
                    list_item_SetNumber = (rowValue[8])
                    list_item_Country = (rowValue[9])
                    list_item_Quota = (rowValue[10])
                    list_item_SetType = (rowValue[11])
                    list_item_VesselSideNumber = (rowValue[12])
                    list_item_VesselClass = (rowValue[13])
                    list_item_Day = (rowValue[14])
                    list_item_Month = (rowValue[15])
                    list_item_HaulDay = (rowValue[16])
                    list_item_HaulMonth = (rowValue[17])
                    list_item_StartTime = (rowValue[18])
                    list_item_Duration = (rowValue[19])
                    list_item_PositionPrecision = (rowValue[20])
                    list_item_StartLatitude = (rowValue[21])
                    list_item_StartLongitude = (rowValue[22])

                    list_item_EndLatitude = (rowValue[23])
                    list_item_EndLongitude = (rowValue[24])
                    list_item_InOut200MileLimit = (rowValue[25])
                    list_item_NAFODivision = (rowValue[26])
                    list_item_GearType = (rowValue[27])
                    list_item_RecordType = (rowValue[28])
                    list_item_DetailedCatchSpeciesCompCode = (rowValue[29])
                    list_item_DirectedSpecies = (rowValue[30])
                    list_item_AverageDepth = (rowValue[31])
                    list_item_DataSource = (rowValue[32])
                    
                    UpdateRecordList_SetCatchDB.append((
                        list_item_DeploymentUID,
                        
                        list_item_ASOCCode,
                        list_item_ObserverNumber,
                        list_item_Year,

                        list_item_DeploymentNumber,
                        list_item_SubTripNumber,
                        list_item_SetNumber,
                        
                        list_item_Country,
                        list_item_Quota,
                        list_item_SetType,

                        list_item_VesselSideNumber,
                        list_item_VesselClass,
                        list_item_Day,

                        list_item_Month,
                        list_item_HaulDay,
                        list_item_HaulMonth,

                        list_item_StartTime,
                        list_item_Duration,
                        list_item_PositionPrecision,

                        list_item_StartLatitude,
                        list_item_StartLongitude,
                        list_item_EndLatitude,

                        list_item_EndLongitude,
                        list_item_InOut200MileLimit,
                        list_item_NAFODivision,

                        list_item_GearType,
                        list_item_RecordType,
                        list_item_DetailedCatchSpeciesCompCode,

                        list_item_DirectedSpecies,
                        list_item_AverageDepth,
                        list_item_DataSource,

                        list_item_DataBase_ID,
                        list_item_RecordIdentifier,
                        ))
                            
                            ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentUID =?, ASOCCode = ?, \
                                        ObserverNumber = ?, Year = ?, DeploymentNumber = ?, SubTripNumber = ?,\
                                        SetNumber = ?, Country = ?, Quota = ?, SetType = ?,\
                                        VesselSideNumber = ?, VesselClass = ?, Day = ?, Month = ?,\
                                        HaulDay = ?, HaulMonth = ?, StartTime = ?, Duration = ?,\
                                        PositionPrecision = ?, StartLatitude = ?, StartLongitude = ?, EndLatitude = ?,\
                                        EndLongitude = ?, InOut200MileLimit = ?, NAFODivision = ?, GearType = ?,\
                                        RecordType = ?, DetailedCatchSpeciesCompCode = ?, DirectedSpecies = ?,\
                                        AverageDepth = ?, DataSource = ?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                        UpdateRecordList_SetCatchDB)
                cur_DB_SetCatch_Validation_Presence.executemany("UPDATE SetCatch_QCFailedPresence_MustVariables SET DeploymentUID =?, ASOCCode = ?, \
                                        ObserverNumber = ?, Year = ?, DeploymentNumber = ?, SubTripNumber = ?,\
                                        SetNumber = ?, Country = ?, Quota = ?, SetType = ?,\
                                        VesselSideNumber = ?, VesselClass = ?, Day = ?, Month = ?,\
                                        HaulDay = ?, HaulMonth = ?, StartTime = ?, Duration = ?,\
                                        PositionPrecision = ?, StartLatitude = ?, StartLongitude = ?, EndLatitude = ?,\
                                        EndLongitude = ?, InOut200MileLimit = ?, NAFODivision = ?, GearType = ?,\
                                        RecordType = ?, DetailedCatchSpeciesCompCode = ?, DirectedSpecies = ?,\
                                        AverageDepth = ?, DataSource = ?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                        UpdateRecordList_SetCatchDB)
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
                conn_DB_SetCatch_Validation_Presence.commit()
                conn_DB_SetCatch_Validation_Presence.close()

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
    
    def ExcelViewEditBackend_RecType_1_Only(QC_FailPresence_DF, get_SearchSingleVariable_Value):
        if len(QC_FailPresence_DF) >0:
            QC_FailPresence_DF= (QC_FailPresence_DF.loc[:,
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
                'NumberIndividuals']]).replace(['', None, np.nan, 'None'], 99999999)

            QC_FailPresence_DF[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                            'NumberIndividuals']] = QC_FailPresence_DF[
                            ['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                        
            QC_FailPresence_DF[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                            'EndLongitude','AverageTowSpeed', 'VesselLength']] = QC_FailPresence_DF[
                            ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                            'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
            
            QC_FailPresence_DF['VesselSideNumber'] = pd.to_numeric(QC_FailPresence_DF[
                                'VesselSideNumber'], downcast='integer', errors='ignore')
                    
            QC_FailPresence_DF['SubTripNumber'] = pd.to_numeric(QC_FailPresence_DF[
                        'SubTripNumber'], downcast='integer', errors='ignore')
                    
            QC_FailPresence_DF[['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                            'SubTripNumber','NAFODivision', 'VesselSideNumber',
                            'UnitArea','DetailedCatchSpeciesCompCode']] = QC_FailPresence_DF[
                            ['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                            'SubTripNumber','NAFODivision', 'VesselSideNumber',
                            'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)

            QC_FailPresence_DF = QC_FailPresence_DF.replace([99999999, 99999999.0, np.nan], '')
            QC_FailPresence_DF = QC_FailPresence_DF.replace(['99999999.0', '99999999', '.'], 'None')
            QC_FailPresence_DF= (QC_FailPresence_DF.loc[:,
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
            QC_FailPresence_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                                    'RecordType'], inplace=True)
            QC_FailPresence_DF['ViewDepUID'] = QC_FailPresence_DF.loc[:, 'DeploymentUID']
            QC_FailPresence_DF  = QC_FailPresence_DF.reset_index(drop=True)
            QC_FailPresence_DF  = pd.DataFrame(QC_FailPresence_DF, index=None)   
            
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0,'Viewing Searched QC Failed Excel File In Seperate Window')
            get_DepNumSearchValue = int(get_SearchSingleVariable_Value)
            
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = QC_FailPresence_DF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(QC_FailPresence_DF),2), clr='lightblue', cols='all')
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
            pt.autoResizeColumns()
            pt.prodyutCustomsetindex5_2()
            pt.show()
            
            def SubmitToUpdateDB():
                Complete_df = pd.DataFrame(QC_FailPresence_DF)
                if len(Complete_df) >0:
                    iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                            "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                    if iSubmit >0:
                        Complete_df  = pd.DataFrame(pt.model.df)
                        Complete_df= (Complete_df.loc[:,
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
                            'NumberIndividuals']]).replace(['', None, np.nan, 'None', ' ', '  ', '   ', '    '], 99999999)

                        Complete_df[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                                ['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                        Complete_df['ObserverNumber'] = pd.to_numeric(Complete_df[
                                    'ObserverNumber'], downcast='integer', errors='ignore')
                        
                        Complete_df[['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                                'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                'UnitArea','DetailedCatchSpeciesCompCode']] = Complete_df[
                                ['ObserverNumber', 'DeploymentUID', 'StatisticalArea',
                                'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
                        
                        Complete_df = Complete_df.loc[:,
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
                        'NumberIndividuals']]

                        Complete_df = Complete_df.replace([99999999, 99999999.0, np.nan], '')
                        Complete_df = Complete_df.replace(['99999999.0', '99999999', '.'], 'None')
                        Complete_df  = Complete_df.reset_index(drop=True)
                        Complete_df = pd.DataFrame(Complete_df)
                        if len(Complete_df) >0:
                            try:
                                BackendSubmitAndUpdateDB_UID(Complete_df)
                            except:
                                print('Error Occured In DataBase')
                            finally:
                                pt.redraw()
                                pt.prodyutCustomclearTable()
                                tkinter.messagebox.showinfo("Submitted Set&Catch DB","Successfully Submitted To Update DB")      
                else:
                    tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

            def BackendSubmitAndUpdateDB_UID(Complete_df):
                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList3_SetCatchDB =[]
                df_rows = Complete_df.to_numpy().tolist()
                for row in df_rows:
                    rowValue = row
                    list_item_DataBase_ID = int(rowValue[0])
                    list_item_RecordIdentifier = int(rowValue[1])
                    list_item_DeploymentUID = (rowValue[2])
                    list_item_ASOCCode = (rowValue[3])
                    list_item_ObserverNumber = (rowValue[4])
                    list_item_Year = (rowValue[5])
                    list_item_DeploymentNumber = (rowValue[6])
                    list_item_SubTripNumber = (rowValue[7])
                    list_item_SetNumber = (rowValue[8])
                    list_item_Country = (rowValue[9])
                    list_item_Quota = (rowValue[10])
                    list_item_SetType = (rowValue[11])
                    list_item_VesselSideNumber = (rowValue[12])
                    list_item_VesselClass = (rowValue[13])
                    list_item_VesselLength = (rowValue[14])
                    list_item_VesselHorsepower = (rowValue[15])
                    list_item_Day = (rowValue[16])
                    list_item_Month = (rowValue[17])
                    list_item_HaulDay = (rowValue[18])
                    list_item_HaulMonth = (rowValue[19])
                    list_item_StartTime = (rowValue[20])
                    list_item_Duration = (rowValue[21])
                    list_item_PositionPrecision = (rowValue[22])
                    list_item_StartLatitude = (rowValue[23])
                    list_item_StartLongitude = (rowValue[24])
                    list_item_EndLatitude = (rowValue[25])
                    list_item_EndLongitude = (rowValue[26])
                    list_item_NAFODivision = (rowValue[27])
                    list_item_UnitArea = (rowValue[28])
                    list_item_StatisticalArea = (rowValue[29])
                    list_item_InOut200MileLimit = (rowValue[30])
                    list_item_GearType = (rowValue[31])
                    list_item_CodendMeshSize = (rowValue[32])
                    list_item_MeshSizeMG = (rowValue[33])
                    list_item_MeshSizeFG = (rowValue[34])
                    list_item_RollerBobbbinDiameter = (rowValue[35])
                    list_item_NumberGillnets = (rowValue[36])
                    list_item_AverageGillnetLength = (rowValue[37])
                    list_item_GrateBarSpacing = (rowValue[38])
                    list_item_FootropeLength = (rowValue[39])
                    list_item_NumberWindows = (rowValue[40])
                    list_item_NumberHooks = (rowValue[41])
                    list_item_NumberPots = (rowValue[42])
                    list_item_NumberPotReleasedCrab = (rowValue[43])
                    list_item_GearDamage = (rowValue[44])
                    list_item_AverageTowSpeed = (rowValue[45])
                    list_item_AverageDepth = (rowValue[46])
                    list_item_DataSource = (rowValue[47])
                    list_item_DirectedSpecies = (rowValue[48])
                    list_item_NumberSpecies = (rowValue[49])
                    list_item_RecordType = (rowValue[50])
                    list_item_DetailedCatchSpeciesCompCode = (rowValue[51])
                    list_item_LogbookIDNumber1 = (rowValue[52])
                    list_item_LogbookIDNumber2 = (rowValue[53])
                    list_item_SpeciesCode = (rowValue[54])
                    list_item_KeptWeight = (rowValue[55])
                    list_item_DiscardWeight = (rowValue[56])
                    list_item_EstimatedWeightReleasedCrab = (rowValue[57])
                    list_item_NumberIndividuals = (rowValue[58])
                    
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_ASOCCode,                     
                                        list_item_ObserverNumber,               
                                        list_item_Year,                        
                                        list_item_DeploymentNumber,             
                                        list_item_SubTripNumber,                
                                        list_item_SetNumber,                    
                                        list_item_Country,                      
                                        list_item_Quota,                        
                                        list_item_SetType,                     
                                        list_item_VesselSideNumber,             
                                        list_item_VesselClass,                  
                                        list_item_VesselLength,                 
                                        list_item_VesselHorsepower,             
                                        list_item_Day,                          
                                        list_item_Month,                        
                                        list_item_HaulDay,                      
                                        list_item_HaulMonth,                    
                                        list_item_StartTime,                    
                                        list_item_Duration,                     
                                        list_item_PositionPrecision,            
                                        list_item_StartLatitude,                
                                        list_item_StartLongitude,               
                                        list_item_EndLatitude,                  
                                        list_item_EndLongitude,                 
                                        list_item_NAFODivision,                 
                                        list_item_UnitArea,                     
                                        list_item_StatisticalArea,              
                                        list_item_InOut200MileLimit,            
                                        list_item_GearType,                     
                                        list_item_CodendMeshSize,               
                                        list_item_MeshSizeMG,                   
                                        list_item_MeshSizeFG,                   
                                        list_item_RollerBobbbinDiameter,        
                                        list_item_NumberGillnets,               
                                        list_item_AverageGillnetLength,         
                                        list_item_GrateBarSpacing,              
                                        list_item_FootropeLength,              
                                        list_item_NumberWindows,                
                                        list_item_NumberHooks,                  
                                        list_item_NumberPots,                  
                                        list_item_NumberPotReleasedCrab,       
                                        list_item_GearDamage,                   
                                        list_item_AverageTowSpeed,              
                                        list_item_AverageDepth,                 
                                        list_item_DataSource,                   
                                        list_item_DirectedSpecies,              
                                        list_item_NumberSpecies,                            
                                        list_item_DetailedCatchSpeciesCompCode, 
                                        list_item_LogbookIDNumber1,             
                                        list_item_LogbookIDNumber2,             
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList3_SetCatchDB.append((
                                        list_item_SpeciesCode,                  
                                        list_item_KeptWeight,                   
                                        list_item_DiscardWeight,                
                                        list_item_EstimatedWeightReleasedCrab,  
                                        list_item_NumberIndividuals,
                                        list_item_RecordType, 
                                        list_item_DataBase_ID))  
                                    
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                        ASOCCode =? , ObserverNumber = ?, Year =?, DeploymentNumber =?, SubTripNumber =?,\
                        SetNumber =? , Country = ?, Quota =?, SetType =?, VesselSideNumber =?,\
                        VesselClass =? , VesselLength = ?, VesselHorsepower =?, Day =?, Month =?,\
                        HaulDay =? , HaulMonth = ?, StartTime =?, Duration =?, PositionPrecision =?,\
                        StartLatitude =? , StartLongitude = ?, EndLatitude =?, EndLongitude =?, NAFODivision =?,\
                        UnitArea =? , StatisticalArea = ?, InOut200MileLimit =?, GearType =?, CodendMeshSize =?,\
                        MeshSizeMG =?, MeshSizeFG = ? , RollerBobbbinDiameter = ?, NumberGillnets = ?, AverageGillnetLength =?,\
                        GrateBarSpacing =?, FootropeLength = ? , NumberWindows = ?, NumberHooks = ?, NumberPots =?,\
                        NumberPotReleasedCrab =?, GearDamage = ? , AverageTowSpeed = ?, AverageDepth = ?, DataSource =?,\
                        DirectedSpecies =?, NumberSpecies = ? , DetailedCatchSpeciesCompCode = ?, LogbookIDNumber1 =?, LogbookIDNumber2 =?\
                        WHERE DeploymentUID =?", 
                        UpdateRecordList_SetCatchDB)
                
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                        SpeciesCode = ? , KeptWeight = ?, DiscardWeight = ?,\
                        EstimatedWeightReleasedCrab =?, NumberIndividuals =?\
                        WHERE RecordType =? AND DataBase_ID = ? ", 
                        UpdateRecordList3_SetCatchDB)
                                
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
        
            def get_ObserverSetCatchDB():
                try:
                    sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = sqliteConnection.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", sqliteConnection)
                    length_Complete_df = len(Complete_df)
                    if length_Complete_df > 0:
                        Complete_df = Complete_df[(Complete_df.DeploymentNumber) == get_DepNumSearchValue]
                        Complete_df= (Complete_df.loc[:,
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
                        Complete_df  = Complete_df.reset_index(drop=True)
                        ObserverSetCatchDB = pd.DataFrame(Complete_df)
                        sqliteConnection.commit()
                        return ObserverSetCatchDB, length_Complete_df
                    else:
                        messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if sqliteConnection:
                        cursor.close()
                        sqliteConnection.close()
            
            ### Alternate Procedure-2
            def SelectForUpdateEntry():
                SetCatchColNameList =  [
                        'DataBase_ID','RecordIdentifier','DeploymentUID',
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
                        'NumberIndividuals']
                
                ListVariableListA = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
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
                                'NumberIndividuals']
                rows = pt.getSelectedRowData()
                SelectedvalueDepUID_DF = rows['DeploymentUID']
                SelectedvalueDepUID = SelectedvalueDepUID_DF.iloc[0]
                cols = pt.getSelectedColumn()
                SelectedVariableDF = rows.iloc[:,cols]
                SelectedVariableValue = SelectedVariableDF.iloc[0]
                SelectedVariable = (pd.DataFrame(SelectedVariableDF).columns.tolist())
                SelectedVariable = SelectedVariable[0]
                def findElements(lst1, lst2):
                    return list(map(lst1.__getitem__, lst2))
                getColsSelectedCol = findElements(SetCatchColNameList, [cols])
                getColsSelectedCol = getColsSelectedCol[0]
                if SelectedVariable == getColsSelectedCol :
                    if SelectedVariable in ListVariableListA:
                        entry_DepUIDSelected.delete(0,END)
                        entry_VariableSelected.delete(0,END)
                        entry_VariableValue.delete(0,END)
                        indexSelCol = ListVariableListA.index(SelectedVariable)
                        entry_VariableSelected.current(indexSelCol)
                        entry_DepUIDSelected.insert(tk.END,SelectedvalueDepUID)
                        entry_VariableValue.insert(tk.END,SelectedVariableValue)
                    else:
                        entry_DepUIDSelected.delete(0,END)
                        entry_VariableSelected.delete(0,END)
                        entry_VariableValue.delete(0,END)
                        entry_VariableSelected.current(len(ListVariableListA))

            def SetcatchDB_VariableList():
                GetSetCatchDB_VariableList = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
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
                                    'NumberIndividuals']
                return GetSetCatchDB_VariableList
    
            def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList):
                SetNoUpdateList = ['SpeciesCode', 'KeptWeight', 'DiscardWeight', 
                                'EstimatedWeightReleasedCrab', 'NumberIndividuals']
                UpdateSetList = UpdateRecordList
                if get_Updated_Variable not in SetNoUpdateList:
                    GetSetCatchDB_VariableList = SetcatchDB_VariableList()
                    ## Updating SetCatch DB
                    conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                    cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                    
                    if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ObserverNumber = ? WHERE DeploymentUID =?", 
                            UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Year = ? WHERE DeploymentUID =?", 
                                UpdateSetList)

                    if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SubTripNumber = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                    
                    if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetNumber = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Country = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Quota = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetType = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[9]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselSideNumber = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                    
                    if get_Updated_Variable == GetSetCatchDB_VariableList[10]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselClass = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[11]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselLength = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))

                    if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselHorsepower = ? WHERE DeploymentUID =?", 
                                (UpdateSetList))
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Day = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Month = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulDay = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulMonth = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartTime = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Duration = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLatitude = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLongitude = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLatitude = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLongitude = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NAFODivision = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET UnitArea = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                    
                    if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StatisticalArea = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET InOut200MileLimit = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearType = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET CodendMeshSize = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[30]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeMG = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[31]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeFG = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[32]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RollerBobbbinDiameter = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[33]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberGillnets = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[34]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageGillnetLength = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[35]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GrateBarSpacing = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[36]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET FootropeLength = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[37]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberWindows = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[38]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberHooks = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[39]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPots = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[40]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPotReleasedCrab = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[41]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearDamage = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[42]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[43]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageDepth = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[44]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DataSource = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                        
                    if get_Updated_Variable == GetSetCatchDB_VariableList[45]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DirectedSpecies = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[46]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberSpecies = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[47]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[48]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DetailedCatchSpeciesCompCode = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                    
                    if get_Updated_Variable == GetSetCatchDB_VariableList[49]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET LogbookIDNumber1 = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                            
                    if get_Updated_Variable == GetSetCatchDB_VariableList[50]:
                        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET LogbookIDNumber2 = ? WHERE DeploymentUID =?", 
                                UpdateSetList)
                                
                    conn_DB_Set_Catch_Analysis.commit()
                    conn_DB_Set_Catch_Analysis.close()   
                else:
                    messagebox.showerror('Wrong Variable Selection For Set Update', 
                    "Set Update For Last five Variable From Table Not Allowed, Please Use Submit To Update DB Option")
                    ReloadDBAfterEntryUpdate()

            def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
                # Performing QC On Variables Value And DataType
                Var_Class_IntA18=['ASOCCode', 'Year', 'DeploymentNumber', 
                                'SetNumber', 'Country', 'Quota', 'SetType',
                                'VesselClass','Day', 'Month','PositionPrecision',
                                'GearType','RecordType','DataSource']
                
                Var_Class_FloatA7= ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                                    'EndLongitude','AverageTowSpeed', 'VesselLength']
                
                Var_Class_String7 =['ObserverNumber', 'DeploymentUID', 'StatisticalArea', 
                                    'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                    'UnitArea','DetailedCatchSpeciesCompCode']
                
                Var_Class_IntB27  = ['VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                                    'InOut200MileLimit',  'CodendMeshSize','GearDamage',
                                    'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                                    'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                                    'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                    'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                                    'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                                    'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                    'NumberIndividuals', 'DirectedSpecies']

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

            def ReloadDBAfterEntryUpdate():
                Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
                ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
                ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
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
                        'NumberIndividuals']]
                ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
                'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
                ObserverSetCatchDB['ViewDepUID'] = ObserverSetCatchDB.loc[:, 'DeploymentUID']
                ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
                pt.prodyutCustomclearTable()
                pt.model.df = ObserverSetCatchDB
                pt.model.df.reset_index(drop=True)
                pt.update()
                pt.resetColors()
                pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
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
                pt.autoResizeColumns()
                pt.prodyutCustomsetindex5_2()
                button_SubmitToUpdateDB.config(state="normal")
        
            def UpdateSelected_SetCatch_DBEntries():
                ReturnFail ="ReturnFail"
                DepUIDUpdateList = ['ASOCCode', 'Year', 'DeploymentNumber', 'SetNumber']
                get_Updated_Variable = entry_VariableSelected.get()
                get_UpdateValue_UpdatedVariable = entry_VariableValue.get()
                get_Selested_DepUID = entry_DepUIDSelected.get()
                get_UpdateValue_UpdatedVariable = QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable)
                if (get_UpdateValue_UpdatedVariable != ReturnFail) & (len(get_Updated_Variable)!=0):
                    ListBox_DF = pd.DataFrame(pt.model.df)
                    ## Update SetCatch DB
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
                        list_item_DeploymentUID = get_Selested_DepUID
                        UpdateRecordList.append((get_UpdateValue_UpdatedVariable, list_item_DeploymentUID))
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList)
                        ReloadDBAfterEntryUpdate()
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")

                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                        iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Entry",
                            "Confirm If You Want To Submit Null Entry To QC Database ?")
                        if iSubmit >0:
                            UpdateRecordList =[]
                            list_item_DeploymentUID = get_Selested_DepUID
                            UpdateRecordList.append((get_UpdateValue_UpdatedVariable, list_item_DeploymentUID))
                            Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList)
                            ReloadDBAfterEntryUpdate()
                            tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")

                    # Empty Selection Case
                    if (len(ListBox_DF)<=0):
                        tkinter.messagebox.showinfo("Update Error",
                        "Empty Set & Catch Table Selection Please Select At least One Entries In the Table To Update The Variable")        
                else:
                    messagebox.showerror('Update Error',
                                        "Please Check Variable DataType And Follow Proper Update Step") 

            ## Bottom Left Frame  - " A "  - ProcedureFrame Define
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
                                                bg= "cadet blue", text="NB : Do Not Edit Columns : DataBase_ID, RecordIdentifier, DeplymentUID, RecordType")
            lbl_CautionSteps.grid(row =10, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_CautionSteps_1 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="NB : Edit/Modify Year/ASOC/DepN/SetN Columns Requires Edit DeplymentUID Accordingly")
            lbl_CautionSteps_1.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            ## Frame Of Alternate Update-2 -E 
            QCEditDBEntry = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
            QCEditDBEntry.pack(side =LEFT, padx=3, pady =2)

            lbl_QCEditDBEntry = Label(QCEditDBEntry, font=('aerial', 11, 'bold'),
                                    bg= "cadet blue", text="D: Alternate Procedure - 2 (Cell Edit & Update DB)")
            lbl_QCEditDBEntry.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_Step1_QCEditDBEntry = Label(QCEditDBEntry, font=('aerial', 9, 'bold'),
                                    bg= "cadet blue", text="1 : Select The Cell Entry From Table For Edit")
            lbl_Step1_QCEditDBEntry.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            button_Selforupdate = Button(QCEditDBEntry, bd = 2, text ="Select For Edit & Update", width =20,
                                        height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                        command = SelectForUpdateEntry)
            button_Selforupdate.grid(row =2, column = 1, padx=10, pady =4, ipady =4, sticky =W)

            lbl_SelectedVar_A = Label(QCEditDBEntry, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" A. DeploymentUID Selected For Update :")
            lbl_SelectedVar_A.grid(row =5, column = 0, padx=10, pady =4, sticky =W)
            
            DepUIDSelected       = IntVar(QCEditDBEntry, value ='Selected DeploymentUID')
            entry_DepUIDSelected = Entry(QCEditDBEntry, font=('aerial', 10, 'bold'), justify='left',
                                        textvariable = DepUIDSelected, width = 25, bd=2)
            entry_DepUIDSelected.grid(row =5, column = 1, padx=2, pady =1, ipady =4, sticky =W)

            lbl_SelectedVar_B = Label(QCEditDBEntry, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" B. QC Variable Selected For Update :")
            lbl_SelectedVar_B.grid(row =6, column = 0, padx=10, pady =4, sticky =W)
            
            ListVariableListA = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
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
                                'NumberIndividuals', '']
            VariableListA        = StringVar(QCEditDBEntry, value ='Selected Variable')
            entry_VariableSelected = ttk.Combobox(QCEditDBEntry, font=('aerial', 10, 'bold'), 
                                                textvariable = VariableListA, width = 23, state='readonly')
            entry_VariableSelected.grid(row =6, column = 1, padx=2, pady =1, ipady =4, sticky =W)
            entry_VariableSelected['values'] = (list(ListVariableListA))

            lbl_SelectedVar_C = Label(QCEditDBEntry, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" C. QC Variable Updated Value :")
            lbl_SelectedVar_C.grid(row =7, column = 0, padx=10, pady =4, sticky =W)
            
            VariableSelected       = IntVar(QCEditDBEntry, value ='QC Variable Value')
            entry_VariableValue = Entry(QCEditDBEntry, font=('aerial', 10, 'bold'), justify='left',
                                        textvariable = VariableSelected, width = 25, bd=2)
            entry_VariableValue.grid(row =7, column = 1, padx=2, pady =1, ipady =4, sticky =W)

            lbl_Step3_QCEditDBEntry = Label(QCEditDBEntry, font=('aerial', 9, 'bold'),
                                    bg= "cadet blue", text="2 : Hit Submit & Update Selected Entry To DB ")
            lbl_Step3_QCEditDBEntry.grid(row =8, column = 0, columnspan=1 ,padx=2, pady =1, sticky =W)

            button_SubmitForUpdate = Button(QCEditDBEntry, bd = 2, text ="Submit Updated Entry", width =20,
                                    height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                    command = UpdateSelected_SetCatch_DBEntries)
            button_SubmitForUpdate.grid(row =8, column = 1, padx=10, pady =4, ipady =4, sticky =W)
            windows.mainloop() 
        
    def GenDeploymentSummary():
        ListVariables = ['ASOCCode','ObserverNumber','Year',
                        'DeploymentNumber','SubTripNumber','SetNumber',
                        'Country','Quota','SetType',
                        'VesselSideNumber','VesselClass','Day', 
                        'Month', 'HaulDay',  'HaulMonth',
                        'StartTime','Duration','PositionPrecision',
                        'StartLatitude','StartLongitude','EndLatitude', 
                        'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                        'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                        'DirectedSpecies', 'AverageDepth',
                        'DataSource']
        getVarnameToView_1 = entry_SelQCVariable.get()
        if getVarnameToView_1 in (ListVariables):
            conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables;", conn)
            cursor.close()
            conn.close()
            if len(Complete_df) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF = ((SetCatchQCFailedDB_DF[SetCatchQCFailedDB_DF[getVarnameToView_1]=="Null"]))
                SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                if len(SetCatchQCFailedDB_DF) >0:
                    SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.groupby(
                        ['Year', 'ASOCCode','DeploymentNumber'],  
                        as_index=False)[getVarnameToView_1].apply(lambda x: (np.count_nonzero(x)))
                    SetCatchQCFailedDB_DF.sort_values(
                        by=['Year', 'ASOCCode','DeploymentNumber'], inplace=True)
                    SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                    SetCatchQCFailedDB_DF = pd.DataFrame(SetCatchQCFailedDB_DF)
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children()) 
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

        def UpdateQCFailDB():
            
            def GetQCFailDB():
                try:
                    conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
                    cursor = conn.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables;", conn)
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
            SetCatchQCFailedDB_DF = GetQCFailDB()
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
            conn_DB_Set_Catch_Consistency= sqlite3.connect(DB_SetCatch_Validation_Presence)
            cur_DB_Set_Catch_Consistency=conn_DB_Set_Catch_Consistency.cursor()
            cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_QCFailedMiscPresence_RecTGearDamage SET DeploymentUID =?, Year = ?, \
                                                ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                UpdateRecordList_SetCatchDB)
            conn_DB_Set_Catch_Consistency.commit()
            conn_DB_Set_Catch_Consistency.close()

        UpdateSetcatchDB()
        UpdateQCFailDB()
        tree1.delete(*tree1.get_children())
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")
    
    def QCFailedExcelViewAll():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        cursor = conn.cursor()
        QCFailedMiscPresence_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables;", conn)
        QCFailedMiscPresence_DF = pd.DataFrame(QCFailedMiscPresence_DF)
        cursor.close()
        conn.close()
        rows= (QCFailedMiscPresence_DF.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                'ASOCCode','ObserverNumber','Year',
                'DeploymentNumber','SubTripNumber','SetNumber',
                'Country','Quota','SetType',
                'VesselSideNumber','VesselClass','Day', 
                'Month', 'HaulDay',  'HaulMonth',
                'StartTime','Duration','PositionPrecision',
                'StartLatitude','StartLongitude','EndLatitude', 
                'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                'DirectedSpecies', 'AverageDepth',
                'DataSource']])
        rows = rows[((rows.RecordType) == 1)]
        rows  = rows.reset_index(drop=True)
        QC_FailPresence_DF  = pd.DataFrame(rows)
        ExcelViewEditBackend_RecType_1_Only(QC_FailPresence_DF)

    def RunPresenceMust_FailedVariables():
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                        'ASOCCode','ObserverNumber','Year',
                                                                        'DeploymentNumber','SubTripNumber','SetNumber',
                                                                        'Country','Quota','SetType',
                                                                        'VesselSideNumber','VesselClass','Day', 
                                                                        'Month', 'HaulDay',  'HaulMonth',
                                                                        'StartTime','Duration','PositionPrecision',
                                                                        'StartLatitude','StartLongitude','EndLatitude', 
                                                                        'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                                                                        'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                                                                        'DirectedSpecies', 'AverageDepth','DataSource']]
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

        def Submit_SetCatch_QCFailedPresence(FailedValidation_PresenceMustDF):
            try:
                Submit_To_DBStorage = pd.DataFrame(FailedValidation_PresenceMustDF)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Presence)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedPresence_MustVariables',
                                        sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Gen_QC_NullCheck(y):
            if y == 99999999:
                return 'Null'
            elif y == '99999999':
                return 'Null'
            elif y == 99999999.0:
                return 'Null'
            else:
                return y

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','Year',
                                'DeploymentNumber','SubTripNumber','SetNumber',
                                'Country','Quota','SetType',
                                'VesselSideNumber','VesselClass','Day', 
                                'Month', 'HaulDay',  'HaulMonth',
                                'StartTime','Duration','PositionPrecision',
                                'StartLatitude','StartLongitude','EndLatitude', 
                                'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                                'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                                'DirectedSpecies', 'AverageDepth',
                                'DataSource']]).replace(['','None'], 99999999)
        
        SetCatchProfileDB_DF[['DataBase_ID','RecordIdentifier','ASOCCode','Year',
                                'DeploymentNumber','SetNumber','Country','Quota','SetType',
                                'VesselClass','Day', 'Month', 'HaulDay',  'HaulMonth',
                                'StartTime','PositionPrecision', 'InOut200MileLimit',
                                'GearType','RecordType', 'DirectedSpecies',
                                'AverageDepth','DataSource']] = SetCatchProfileDB_DF[
                                ['DataBase_ID','RecordIdentifier','ASOCCode','Year',
                                'DeploymentNumber','SetNumber','Country','Quota','SetType',
                                'VesselClass','Day', 'Month', 'HaulDay',  'HaulMonth',
                                'StartTime','PositionPrecision', 'InOut200MileLimit',
                                'GearType','RecordType', 'DirectedSpecies',
                                'AverageDepth','DataSource']
                                ].astype(int)
        
        SetCatchProfileDB_DF[['DeploymentUID','ObserverNumber','SubTripNumber',
                            'VesselSideNumber','NAFODivision','DetailedCatchSpeciesCompCode']] = SetCatchProfileDB_DF[
                            ['DeploymentUID','ObserverNumber','SubTripNumber',
                            'VesselSideNumber','NAFODivision', 'DetailedCatchSpeciesCompCode']
                            ].astype(str)
        
        SetCatchProfileDB_DF[['Duration','StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude']] = SetCatchProfileDB_DF[
                            ['Duration','StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude']
                            ].astype(float)
        ColList =['DataBase_ID','RecordIdentifier','DeploymentUID',
                'ASOCCode','ObserverNumber','Year',
                'DeploymentNumber','SubTripNumber','SetNumber',
                'Country','Quota','SetType',
                'VesselSideNumber','VesselClass','Day', 
                'Month', 'HaulDay',  'HaulMonth',
                'StartTime','Duration','PositionPrecision',
                'StartLatitude','StartLongitude','EndLatitude', 
                'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                'DirectedSpecies', 'AverageDepth',
                'DataSource']
        for ColName in ColList:
            SetCatchProfileDB_DF[ColName] = SetCatchProfileDB_DF[ColName].apply(Gen_QC_NullCheck)
        
        FailedValidation_PresenceMustDF= SetCatchProfileDB_DF[(SetCatchProfileDB_DF.DataBase_ID =="Null")|
                        (SetCatchProfileDB_DF.RecordIdentifier =="Null")|
                        (SetCatchProfileDB_DF.DeploymentUID =="Null")|
                        (SetCatchProfileDB_DF.ASOCCode =="Null")|
                        (SetCatchProfileDB_DF.ObserverNumber =="Null")|
                        (SetCatchProfileDB_DF.Year =="Null")|
                        (SetCatchProfileDB_DF.DeploymentNumber =="Null")|
                        (SetCatchProfileDB_DF.SubTripNumber =="Null")|
                        (SetCatchProfileDB_DF.SetNumber =="Null")|
                        (SetCatchProfileDB_DF.Country =="Null")|
                        (SetCatchProfileDB_DF.Quota =="Null")|
                        (SetCatchProfileDB_DF.SetType =="Null")|
                        (SetCatchProfileDB_DF.VesselSideNumber =="Null")|
                        (SetCatchProfileDB_DF.VesselClass =="Null")|
                        (SetCatchProfileDB_DF.Day =="Null")|
                        (SetCatchProfileDB_DF.Month =="Null")|
                        (SetCatchProfileDB_DF.HaulDay =="Null")|
                        (SetCatchProfileDB_DF.HaulMonth =="Null")|
                        (SetCatchProfileDB_DF.StartTime =="Null")|
                        (SetCatchProfileDB_DF.Duration =="Null")|
                        (SetCatchProfileDB_DF.PositionPrecision =="Null")|
                        (SetCatchProfileDB_DF.StartLatitude =="Null")|
                        (SetCatchProfileDB_DF.StartLongitude =="Null")|
                        (SetCatchProfileDB_DF.EndLatitude =="Null")|
                        (SetCatchProfileDB_DF.EndLongitude =="Null")|
                        (SetCatchProfileDB_DF.InOut200MileLimit =="Null")|
                        (SetCatchProfileDB_DF.NAFODivision =="Null")|
                        (SetCatchProfileDB_DF.GearType =="Null")|
                        (SetCatchProfileDB_DF.RecordType =="Null")|
                        (SetCatchProfileDB_DF.DetailedCatchSpeciesCompCode =="Null")|
                        (SetCatchProfileDB_DF.DirectedSpecies =="Null")|
                        (SetCatchProfileDB_DF.AverageDepth =="Null")|
                        (SetCatchProfileDB_DF.DataSource =="Null")
                        ]
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2007, "ObserverNumber"] = 'None'
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2013, "SubTripNumber"] = 'None'
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2013, "DetailedCatchSpeciesCompCode"] = 'None'
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2007, "HaulDay"] = ''
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2007, "HaulMonth"] = ''
        
        FailedValidation_PresenceMustDF  = FailedValidation_PresenceMustDF.reset_index(drop=True)
        FailedValidation_PresenceMustDF  = pd.DataFrame(FailedValidation_PresenceMustDF)

        Submit_SetCatch_QCFailedPresence(FailedValidation_PresenceMustDF)
        Length_FailedPresenceMustDF = len(FailedValidation_PresenceMustDF)
        return Length_FailedPresenceMustDF
    
    ## Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    ## ComboBox
    entry_UpdateVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable1)
    entry_SearchVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable2)
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ## Gen Summary
    QCFailedTotalEntries()
    GenStartSummaryQC()

    # SelectViewResultsRun Button
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

    # Buttons On Generate QC Failed Summary Frame
    button_GenSummaryQC = Button(Summaryframe, bd = 1, text ="Generate QC Summary ", width = 20,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSummaryQC)
    button_GenSummaryQC.pack(side =TOP, anchor = CENTER)

    button_SelView = Button(SummaryDisplay, bd = 1, text ="Select & View", width = 12,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =SelectAndViewQCSummary)
    button_SelView.pack(side =TOP, anchor = W)

    button_GenDepQCSummary = Button(SelQCVariableDisplay, bd = 1, text ="Generate Deployment Summary", width = 28,
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
    Update.add_command(label="Update DeplymentUID", command=UpdateDeploymentUIDAfterUpdate)
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack()
    window.mainloop()

