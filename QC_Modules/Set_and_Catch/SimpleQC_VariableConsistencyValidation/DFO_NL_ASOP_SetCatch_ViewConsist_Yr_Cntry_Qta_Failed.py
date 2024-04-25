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
DB_SetCatch_Validation_Consistency = ("./BackEnd/Sqlite3_DB/QC_Check_ConsistencyValidate_DB/DFO_NL_ASOP_SetCatch_ConsistencyValidation.db")


def ViewConsis_Yr_Cntry_Qta_ValResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Consistency Validator - ID-C-05-0")
    window.geometry("1160x833+200+100")
    window.config(bg="cadet blue")

    ## Top Frame
    Topframe = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Topframe.pack(side = TOP)

    txtDisplayMessageSystem = Listbox(Topframe, font=('aerial', 9, 'bold'), 
                                      height =2, width =80)
    txtDisplayMessageSystem.grid(row =0, column = 0, padx=200, pady =5, ipady =5, sticky =E)

    lbl_QCDisplay = Label(Topframe, font=('aerial', 10, 'bold'), text="A: QCFailed Display Table:")
    lbl_QCDisplay.grid(row =0, column = 0, padx=2, pady =1, sticky =W)

    lbl_TotalFailedEntries = Label(Topframe, font=('aerial', 10 , 'bold'), bg= "cadet blue", text="# Of Deployment Failed :")
    lbl_TotalFailedEntries.grid(row =2, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(Topframe, value='')
    txtTotalFailedEntries = Entry(Topframe, font=('aerial',10),textvariable = TotalFailedEntries, width = 5, bd=1)
    txtTotalFailedEntries.grid(row =2, column = 0, padx=170, pady =1, ipady =1, sticky =W)

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
    ListVariableListA = ['Select Consistency Variable Pair From DropDown & Run View Selected Button', 
                         'Case-A Year - Consistency @ Each Deployment',
                         'Case-B Country - Consistency @ Each Deployment',
                         'Case-C Quota - Consistency @ Each Deployment']
    VariableList        = StringVar(SelectViewResultsRun, value ='')
    entry_ViewVarResults  = ttk.Combobox(SelectViewResultsRun, font=('aerial', 8, 'bold'), justify = tk.RIGHT,
                                        textvariable = VariableList, width = 80, state='readonly')
    entry_ViewVarResults.grid(row =0, column = 0, padx=2, pady =4, ipady= 4, sticky =W)
    entry_ViewVarResults['values'] = ListVariableListA
    entry_ViewVarResults.current(0)
    
    txtQCVariableView = Entry(SelectViewResultsRun, font=('aerial', 10), justify = tk.CENTER,
                            textvariable = StringVar(window, value='QCVariable ↓↓'), width = 22, bd=2)
    txtQCVariableView.grid(row =0, column = 4, padx=2, pady =2, ipady =5, sticky =E)
    
    ## Tree1 Define
    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", 
                    "column4", "column5", "column6", 
                    "column7", "column8", "column9",
                    "column10", "column11","column12", "column13"), height=20, show='headings')
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
    tree1.heading("#4", text="ASOCCode", anchor=CENTER)
    tree1.heading("#5", text="ObserverNumber", anchor=CENTER)
    tree1.heading("#6", text="DeploymentNumber", anchor=CENTER)
    tree1.heading("#7", text="SetNumber", anchor=CENTER)
    tree1.heading("#8", text="VesselSideNumber", anchor=CENTER)
    tree1.heading("#9", text="RecordType", anchor=CENTER)
    tree1.heading("#10", text="Year", anchor=CENTER)
    tree1.heading("#11", text="Country", anchor=CENTER)
    tree1.heading("#12", text="Quota", anchor=CENTER)
    tree1.heading("#13", text="QC Message", anchor=CENTER)
    
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=90, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=82, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)            
    tree1.column('#9', stretch=NO, minwidth=0, width=90, anchor = tk.CENTER)
    tree1.column('#10', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)
    tree1.column('#11', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)
    tree1.column('#12', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)
    tree1.column('#13', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    
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
    
    ListUpdateVar = ['Year','Country','Quota']
    UpdateVar        = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = UpdateVar, width = 24, state='readonly')
    entry_UpdateVariableList.grid(row =8, column = 0, padx=50, pady =2, ipady= 2, sticky =W)
    entry_UpdateVariableList['values'] = sorted(list(ListUpdateVar))

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
    lbl_SummaryQCframe = Label(SummaryQCframe, font=('aerial', 12, 'bold','underline'), 
                                bg= "cadet blue", text="B: QC Summary (Year-Country-Quota)")
    lbl_SummaryQCframe.pack(side =TOP)

    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    Summaryframetree = ttk.Treeview(Summaryframe, column=("column1", "column2"),
                                    height=4, show='headings')
    Summaryframetree.heading("#1", text="QC Variable Name")
    Summaryframetree.heading("#2", text="# Of Deployment Fail In QC")
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=172)            
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
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
    SelQCVariable      = StringVar(SelQCVariableDisplay, value ='QCVariable ↓↓')
    entry_SelQCVariable = Entry(SelQCVariableDisplay, font=('aerial', 10, 'bold'),  justify = tk.CENTER,
                            textvariable = SelQCVariable, width = 13, bd=1)
    entry_SelQCVariable.grid(row =0, column = 0, padx=2, pady =2, ipady =2, sticky =W)

    SearchDepNumSetCatchDB      = StringVar(SelQCVariableDisplay, value ='')
    entry_SearchDepNumSetCatchDB = Entry(SelQCVariableDisplay, font=('aerial', 10, 'bold'),  justify = tk.CENTER,
                            textvariable = SearchDepNumSetCatchDB, width = 8, bd=2)
    entry_SearchDepNumSetCatchDB.grid(row =0, column = 0, padx=220, pady =2, ipady =2, sticky =W)
    
    SelQCVariableDisplay.pack(side = TOP, pady=0, anchor = CENTER)
    SelResultOverview = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SelResultOverview.pack(side =LEFT, padx=1, pady =2)
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
    SelResultOverviewtree.heading("#1", text="QCVariable", anchor=CENTER)
    SelResultOverviewtree.heading("#2", text="DepNum", anchor=CENTER)
    SelResultOverviewtree.heading("#3", text="ASOCCode", anchor=CENTER)
    SelResultOverviewtree.heading("#4", text="ObsNum", anchor=CENTER)
    SelResultOverviewtree.heading("#5", text="# Of Sets", anchor=CENTER)
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=90, anchor = tk.CENTER)             
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=105, anchor = tk.CENTER)
    SelResultOverviewtree.column('#4', stretch=NO, minwidth=0, width=75, anchor = tk.CENTER)
    SelResultOverviewtree.column('#5', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = TOP)

    #######All Defined Functions #########
    
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  ['DataBase_ID','RecordIdentifier','DeploymentUID','ASOCCode','ObserverNumber',
                            'DeploymentNumber','SetNumber','VesselSideNumber','RecordType',
                            'Year', 'Country','Quota','QC_Year','QC_Country','QC_Quota' ]
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
            return ReturnMatchedMessage
        else: 
            return ReturnMisMatchedMessage

    def ImportAndUpdateSetCatchDB():
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        conn_DB_SetCatch_Validation_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cur_DB_SetCatch_Validation_Consistency=conn_DB_SetCatch_Validation_Consistency.cursor()
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
                        ASOCCode = (df.loc[:,'ASOCCode']).fillna(99999999).astype(int, errors='ignore')
                        ObserverNumber = (df.loc[:,'ObserverNumber']).fillna(8888888).astype(str)
                        DeploymentNumber = (df.loc[:,'DeploymentNumber']).fillna(99999999).astype(int, errors='ignore')
                        SetNumber = (df.loc[:,'SetNumber']).fillna(99999999).astype(str, errors='ignore')
                        VesselSideNumber = (df.loc[:,'VesselSideNumber']).fillna(8888888).astype(str)
                        RecordType = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        Year = (df.loc[:,'Year']).fillna(99999999).astype(int, errors='ignore')
                        Country = (df.loc[:,'Country']).fillna(99999999).astype(int, errors='ignore')
                        Quota = (df.loc[:,'Quota']).fillna(99999999).astype(int, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID, ASOCCode,\
                                        ObserverNumber, DeploymentNumber, SetNumber, \
                                        VesselSideNumber, RecordType, Year, Country, Quota]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns=  {0:'DataBase_ID', 1: 'RecordIdentifier', 2: 'DeploymentUID',
                                                3:'ASOCCode', 4:'ObserverNumber', 5:'DeploymentNumber', 
                                                6:'SetNumber', 7:'VesselSideNumber', 8:'RecordType',
                                                9:'Year', 10:'Country', 11:'Quota'},inplace = True)
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
                                            (Raw_Imported_Df.ASOCCode =='') |
                                            (Raw_Imported_Df.DeploymentNumber =='') |
                                            (Raw_Imported_Df.SetNumber =='')|
                                            (Raw_Imported_Df.RecordType =='') |
                                            (Raw_Imported_Df.Year =='') |
                                            (Raw_Imported_Df.Country =='') |
                                            (Raw_Imported_Df.Quota =='')
                                            ]
                    Len_CheckEmptyNessColumn =len(CheckEmptyNessColumn)
                    if Len_CheckEmptyNessColumn==0:
                        Length_Raw_Imported_Df  =  len(Raw_Imported_Df)
                        if Length_Raw_Imported_Df <250000:
                            UpdateRecordList_SetCatchDB =[]
                            Update_Year_Failed =[]
                            Update_Country_Failed =[]
                            Update_Quota_Failed =[]
                            df_rows = Raw_Imported_Df.to_numpy().tolist()
                            for row in df_rows:
                                rowValue = row
                                list_item_DataBase_ID = int(rowValue[0])
                                list_item_RecordIdentifier = int(rowValue[1])
                                list_item_DeploymentUID = (rowValue[2])
                                list_item_ASOCCode = (rowValue[3])
                                list_item_ObserverNumber = (rowValue[4])
                                list_item_DeploymentNumber = (rowValue[5])
                                list_item_SetNumber = (rowValue[6])
                                list_item_VesselSideNumber = (rowValue[7])
                                list_item_RecordType = (rowValue[8])
                                list_item_Year = (rowValue[9])
                                list_item_Country = (rowValue[10])
                                list_item_Quota = (rowValue[11])
                                list_item_QCMsg = ''

                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_RecordType,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                Update_Year_Failed.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_RecordType,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_QCMsg,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                Update_Country_Failed.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_RecordType,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_QCMsg,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                Update_Quota_Failed.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_RecordType,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_QCMsg,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                                 
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ?, \
                                                    ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, VesselSideNumber =?,\
                                                    RecordType = ? , Year = ?, Country = ?, Quota = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                            
                            cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET ASOCCode = ?, \
                                                    ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, VesselSideNumber =?,\
                                                    RecordType = ? , Year = ?, Country = ?, Quota = ?, QC_Year = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    Update_Year_Failed)
                            
                            cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET ASOCCode = ?, \
                                                    ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, VesselSideNumber =?,\
                                                    RecordType = ? , Year = ?, Country = ?, Quota = ?, QC_Country = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    Update_Country_Failed)
                            
                            cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET ASOCCode = ?, \
                                                    ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, VesselSideNumber =?,\
                                                    RecordType = ? , Year = ?, Country = ?, Quota = ?, QC_Quota = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    Update_Quota_Failed)
                            
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Consistency.commit()
                            conn_DB_SetCatch_Validation_Consistency.close()
                            GenSummaryQC()
                            UpdateDeploymentUIDAfterUpdate()
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
        SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
        entry_SelectedCaseTypeEntries.delete(0,END)
        entry_ViewVarResults.current(0)
        
        txtQCVariableView.delete(0,END)
        txtQCVariableView.insert(tk.END,'QCVariable ↓↓')
        entry_SelQCVariable.delete(0,END)
        entry_SelQCVariable.insert(tk.END,'QCVariable ↓↓')
        
        txtDisplayMessageSystem.delete(0,END)
        
    def ClearEntries():
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateValue_VariableA.delete(0,END)
        entry_NumberRowSelected.delete(0,END)
    
    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select Consistency Variable Pair From DropDown & Run View Selected Button', 
                            'Case-A Year - Consistency @ Each Deployment',
                            'Case-B Country - Consistency @ Each Deployment',
                            'Case-C Quota - Consistency @ Each Deployment']
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Consistency)
            cur=con.cursor()
            if getVarnameToView == ListVariableListA[1]:
                cur.execute("SELECT * FROM SetCatch_Year_FailConsistency_DF")
            if getVarnameToView == ListVariableListA[2]:
                cur.execute("SELECT * FROM SetCatch_Country_FailConsistency_DF")
            if getVarnameToView == ListVariableListA[3]:
                cur.execute("SELECT * FROM SetCatch_Quota_FailConsistency_DF")
            rows=cur.fetchall()
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_VariablesProfile():
        ListVariableListA = ['Select Consistency Variable Pair From DropDown & Run View Selected Button', 
                            'Case-A Year - Consistency @ Each Deployment',
                            'Case-B Country - Consistency @ Each Deployment',
                            'Case-C Quota - Consistency @ Each Deployment']
        getVarnameToView = entry_ViewVarResults.get()
        tree1.delete(*tree1.get_children())
        entry_SelectedCaseTypeEntries.delete(0,END)
        rows = viewQCFailed(getVarnameToView)
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 
                             2:'DeploymentUID', 3:'ASOCCode',
                             4:'ObserverNumber', 5:'DeploymentNumber', 
                             6:'SetNumber', 7:'VesselSideNumber', 
                             8:'RecordType', 9:'Year', 
                             10:'Country', 11:'Quota', 
                             12:'QCMessage'},inplace = True)
        if len(rows) >0 :
            if getVarnameToView == ListVariableListA[0]:
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'Select Consistency Variable Pair From DropDown & Run View Selected Button')
            
            if getVarnameToView == ListVariableListA[1]:
                rows = rows.loc[:,
                        ['DataBase_ID','RecordIdentifier',
                         'DeploymentUID','ASOCCode',
                         'ObserverNumber', 'DeploymentNumber',
                         'SetNumber', 'VesselSideNumber',
                         'RecordType', 'Year', 
                         'Country','Quota',
                         'QCMessage']]
                rows.sort_values(by=['ASOCCode','ObserverNumber',
                                     'DeploymentNumber','SetNumber',
                                     'RecordType'], inplace=True)
                rows  = rows.reset_index(drop=True)
                rows  = pd.DataFrame(rows)
                CaseATotalFail = rows.drop_duplicates(
                                     subset=['ASOCCode','ObserverNumber','DeploymentNumber'], keep="first")
                CaseATotalFail = len(CaseATotalFail)
                entry_SelectedCaseTypeEntries.insert(tk.END,CaseATotalFail)
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'Year Must Same In All Records Within ASOC-ObsNum-DepNum')
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                entry_SelQCVariable.delete(0,END)
                entry_SelQCVariable.insert(tk.END,'Year ↓↓')

                FailConsistency_Summary = (rows.groupby([
                    'Year', 'ASOCCode','ObserverNumber','DeploymentNumber'], 
                    as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
                FailConsistency_Summary.rename(columns={'Year':'Year',
                                                        'ASOCCode':'ASOCCode',
                                                        'ObserverNumber': 'ObserverNumber',
                                                        'DeploymentNumber':'DeploymentNumber',
                                                        'SetNumber':'NumOfSetsPerDeploymentNumber'
                                                        },inplace = True)
                FailConsistency_Summary = FailConsistency_Summary.loc[:,
                        ['Year', 'DeploymentNumber', 'ASOCCode','ObserverNumber', 'NumOfSetsPerDeploymentNumber']]
                FailConsistency_Summary.sort_values(by=['ASOCCode','ObserverNumber','DeploymentNumber'], inplace=True)
                FailConsistency_Summary  = FailConsistency_Summary.reset_index(drop=True)
                FailConsistency_Summary  = pd.DataFrame(FailConsistency_Summary)
                
            if getVarnameToView == ListVariableListA[2]:
                rows = rows.loc[:,
                        ['DataBase_ID','RecordIdentifier',
                         'DeploymentUID','ASOCCode',
                         'ObserverNumber', 'DeploymentNumber',
                         'SetNumber', 'VesselSideNumber',
                         'RecordType', 'Year', 
                         'Country','Quota',
                         'QCMessage']]
                rows.sort_values(by=['ASOCCode','ObserverNumber','DeploymentNumber','SetNumber','RecordType'], inplace=True)
                rows  = rows.reset_index(drop=True)
                rows  = pd.DataFrame(rows)
                CaseATotalFail = rows.drop_duplicates(
                                     subset=['ASOCCode','ObserverNumber','DeploymentNumber'], keep="first")
                CaseATotalFail = len(CaseATotalFail)
                entry_SelectedCaseTypeEntries.insert(tk.END,CaseATotalFail)
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'Country Must Same In All Records Within ASOC-ObsNum-DepNum')
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                entry_SelQCVariable.delete(0,END)
                entry_SelQCVariable.insert(tk.END,'Country ↓↓')

                FailConsistency_Summary = (rows.groupby([
                    'Country', 'ASOCCode','ObserverNumber','DeploymentNumber'], 
                    as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
                FailConsistency_Summary.rename(columns={'Country':'Country',
                                                        'ASOCCode':'ASOCCode',
                                                        'ObserverNumber': 'ObserverNumber',
                                                        'DeploymentNumber':'DeploymentNumber',
                                                        'SetNumber':'NumOfSetsPerDeploymentNumber'
                                                        },inplace = True)
                FailConsistency_Summary = FailConsistency_Summary.loc[:,
                        ['Country', 'DeploymentNumber', 'ASOCCode','ObserverNumber', 'NumOfSetsPerDeploymentNumber']]
                FailConsistency_Summary.sort_values(by=['ASOCCode','ObserverNumber','DeploymentNumber'], inplace=True)
                FailConsistency_Summary  = FailConsistency_Summary.reset_index(drop=True)
                FailConsistency_Summary  = pd.DataFrame(FailConsistency_Summary)
            
            if getVarnameToView == ListVariableListA[3]:
                rows = rows.loc[:,
                        ['DataBase_ID','RecordIdentifier',
                         'DeploymentUID','ASOCCode',
                         'ObserverNumber', 'DeploymentNumber',
                         'SetNumber', 'VesselSideNumber',
                         'RecordType', 'Year', 
                         'Country','Quota',
                         'QCMessage']]
                rows.sort_values(
                    by=['ASOCCode','ObserverNumber',
                        'DeploymentNumber','SetNumber',
                        'RecordType'], inplace=True)
                rows  = rows.reset_index(drop=True)
                rows  = pd.DataFrame(rows)
                CaseATotalFail = rows.drop_duplicates(
                                     subset=['ASOCCode','ObserverNumber','DeploymentNumber'], keep="first")
                CaseATotalFail = len(CaseATotalFail)
                entry_SelectedCaseTypeEntries.insert(tk.END,CaseATotalFail)
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(1, 'Quota Must Same In All Records Within ASOC-ObsNum-DepNum')
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                entry_SelQCVariable.delete(0,END)
                entry_SelQCVariable.insert(tk.END,'Quota ↓↓')
                FailConsistency_Summary = (rows.groupby([
                    'Quota', 'ASOCCode','ObserverNumber','DeploymentNumber'], 
                    as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
                FailConsistency_Summary.rename(columns={'Quota':'Quota',
                                                        'ASOCCode':'ASOCCode',
                                                        'ObserverNumber': 'ObserverNumber',
                                                        'DeploymentNumber':'DeploymentNumber',
                                                        'SetNumber':'NumOfSetsPerDeploymentNumber'
                                                        },inplace = True)
                FailConsistency_Summary = FailConsistency_Summary.loc[:,
                        ['Quota', 'DeploymentNumber', 'ASOCCode','ObserverNumber', 'NumOfSetsPerDeploymentNumber']]
                FailConsistency_Summary.sort_values(by=['ASOCCode','ObserverNumber','DeploymentNumber'], inplace=True)
                FailConsistency_Summary  = FailConsistency_Summary.reset_index(drop=True)
                FailConsistency_Summary  = pd.DataFrame(FailConsistency_Summary)
                
            countIndex1 = 0
            for each_rec in range(len(rows)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightgreen")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            countIndex2 = 0
            for each_rec in range(len(FailConsistency_Summary)):
                if countIndex2 % 2 == 0:
                    SelResultOverviewtree.insert("", tk.END, values=list(FailConsistency_Summary.loc[each_rec]), tags =("even",))
                else:
                    SelResultOverviewtree.insert("", tk.END, values=list(FailConsistency_Summary.loc[each_rec]), tags =("odd",))
                countIndex2 = countIndex2+1
            SelResultOverviewtree.tag_configure("even",foreground="black", background="lightgreen")
            SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
        else:
            entry_SelectedCaseTypeEntries.delete(0,END)
            SelQCTotalFail = 0
            entry_SelectedCaseTypeEntries.insert(tk.END,SelQCTotalFail)
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Empty QC Fail Database. Nothing to Display')

    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_YCQ_FailConsis_SummaryDF;", conn)
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
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        
        Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
        Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
        Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
        
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        cursor.close()
        conn.close()

        GetSetCatchDB = GetSetCatchProfileDB()
        
        ## For Year_FailConsistency_DF
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Year_FailConsistency_DF['DataBase_ID'] = (Year_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Year_FailConsistency_DF['RecordIdentifier'] = (Year_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Year_FailConsistency_DF['DeploymentUID'] = (Year_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Year_FailConsistency_DF['ObserverNumber'] = (Year_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Year_FailConsistency_DF['VesselSideNumber'] = (Year_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Year_FailConsistency_DF = Year_FailConsistency_DF.reset_index(drop=True)
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        
        ## For Country_FailConsistency_DF
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Country_FailConsistency_DF['DataBase_ID'] = (Country_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Country_FailConsistency_DF['RecordIdentifier'] = (Country_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Country_FailConsistency_DF['DeploymentUID'] = (Country_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Country_FailConsistency_DF['ObserverNumber'] = (Country_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Country_FailConsistency_DF['VesselSideNumber'] = (Country_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Country_FailConsistency_DF = Country_FailConsistency_DF.reset_index(drop=True)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        
        ## For Quota_FailConsistency_DF
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        Quota_FailConsistency_DF['DataBase_ID'] = (Quota_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Quota_FailConsistency_DF['RecordIdentifier'] = (Quota_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Quota_FailConsistency_DF['DeploymentUID'] = (Quota_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Quota_FailConsistency_DF['ObserverNumber'] = (Quota_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Quota_FailConsistency_DF['VesselSideNumber'] = (Quota_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Quota_FailConsistency_DF = Quota_FailConsistency_DF.reset_index(drop=True)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        
        Merge_CountryQuota = Country_FailConsistency_DF.merge(
                        Quota_FailConsistency_DF, 
                        on = ['DataBase_ID','RecordIdentifier', 
                              'DeploymentUID', 'ASOCCode','ObserverNumber',
                              'DeploymentNumber','SetNumber','VesselSideNumber',
                              'RecordType', 'Year', 'Country', 'Quota'], indicator=True, 
                        how='outer')
        Merge_CountryQuota = Merge_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota', 'QC_Country', 'QC_Quota']]
        Merge_CountryQuota = Merge_CountryQuota.reset_index(drop=True)
        Merge_CountryQuota = pd.DataFrame(Merge_CountryQuota)
        
        Merge_Year_CountryQuota = Year_FailConsistency_DF.merge(
                        Merge_CountryQuota, 
                        on = ['DataBase_ID','RecordIdentifier', 
                              'DeploymentUID', 'ASOCCode','ObserverNumber',
                              'DeploymentNumber','SetNumber','VesselSideNumber',
                              'RecordType', 'Year', 'Country', 'Quota'], indicator=True, 
                        how='outer')
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota',
                         'QC_Year', 'QC_Country', 'QC_Quota']]
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.reset_index(drop=True)
        Merge_Year_CountryQuota = pd.DataFrame(Merge_Year_CountryQuota)
        
        ## merging With SetcatchDB
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID', 
                         'QC_Year', 'QC_Country', 'QC_Quota']]
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.reset_index(drop=True)
        Merge_Year_CountryQuota = pd.DataFrame(Merge_Year_CountryQuota)
        Merge_WithSetCatchDB=  GetSetCatchDB.merge(
                        Merge_Year_CountryQuota, 
                        on = ['DataBase_ID','RecordIdentifier','DeploymentUID'],
                        indicator=True, 
                        how='outer').query('_merge == "both"')
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota',
                         'QC_Year', 'QC_Country', 'QC_Quota']]
        Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode',
             'DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country','Quota']]= Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode',
             'DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country','Quota']].astype(int)
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.replace(99999999, '')
        Merge_WithSetCatchDB = Merge_WithSetCatchDB[(Merge_WithSetCatchDB.RecordType) == 1]
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.reset_index(drop=True)
        Merge_WithSetCatchDB = pd.DataFrame(Merge_WithSetCatchDB)        
        if len(Merge_WithSetCatchDB) >0:
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x765+40+40')
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
                Complete_df = (Complete_df.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                        'DeploymentUID', 'ASOCCode',
                        'ObserverNumber','DeploymentNumber',
                        'SetNumber','VesselSideNumber',
                        'RecordType', 'Year',
                        'Country','Quota']]).replace(
                ['', None, np.nan, 'None'], 99999999)
                
                Complete_df[['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']] = Complete_df[
                        ['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']].astype(int)
                
                Complete_df[['DeploymentUID','ObserverNumber', 'VesselSideNumber']] = Complete_df[
                ['DeploymentUID','ObserverNumber', 'VesselSideNumber']].astype(str)
                Complete_df = Complete_df.replace([99999999, 99999999.0, '99999999'], '')
                Complete_df = Complete_df.reset_index(drop=True)
                Complete_df = pd.DataFrame(Complete_df)    
                if len(Complete_df) >0:
                    iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                            "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                    if iSubmit >0:
                        try:
                            BackendSubmitAndUpdateDB(Complete_df)
                        except sqlite3.Error as error:
                            print('Error occured - ', error)
                        finally:
                            UpdateDeploymentUIDAfterUpdate()
                            pt.redraw()
                            tkinter.messagebox.showinfo("Submit Success","Successfully Submitted Update To Database")
                else:
                    tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

            def BackendSubmitAndUpdateDB(Complete_df):
                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                conn_DB_SetCatch_Validation_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
                cur_DB_SetCatch_Validation_Consistency=conn_DB_SetCatch_Validation_Consistency.cursor()
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList_QCfailDB_Yr =[]
                UpdateRecordList_QCfailDB_Cntry =[]
                UpdateRecordList_QCfailDB_Qta =[]
                df_rows = Complete_df.to_numpy().tolist()
                for row in df_rows:
                    rowValue = row
                    list_item_DataBase_ID = int(rowValue[0])
                    list_item_RecordIdentifier = int(rowValue[1])
                    list_item_DeploymentUID = (rowValue[2])
                    list_item_ASOCCode = (rowValue[3])
                    list_item_ObserverNumber = (rowValue[4])
                    list_item_DeploymentNumber = (rowValue[5])
                    list_item_SetNumber = (rowValue[6])
                    list_item_VesselSideNumber = (rowValue[7])
                    list_item_RecordType = (rowValue[8])
                    list_item_Year = (rowValue[9])
                    list_item_Country = (rowValue[10])
                    list_item_Quota = (rowValue[11])
                    list_item_QCMsg = ''
                    
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_VesselSideNumber,
                                        list_item_Year,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_DeploymentUID))                  
                    
                    UpdateRecordList_QCfailDB_Yr.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_VesselSideNumber,
                                        list_item_Year,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_QCMsg,
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList_QCfailDB_Cntry.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_VesselSideNumber,
                                        list_item_Year,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_QCMsg,
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList_QCfailDB_Qta.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_VesselSideNumber,
                                        list_item_Year,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_QCMsg,
                                        list_item_DeploymentUID))
                                    
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                    ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                    SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =? \
                    WHERE DeploymentUID =?", 
                    UpdateRecordList_SetCatchDB)
                
                cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET \
                    ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                    SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =?, QC_Year =? \
                    WHERE DeploymentUID =?",   
                    UpdateRecordList_QCfailDB_Yr)
                
                cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET \
                    ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                    SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =?, QC_Country =? \
                    WHERE DeploymentUID =?",    
                    UpdateRecordList_QCfailDB_Cntry)
                
                cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET \
                    ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                    SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =?, QC_Quota =? \
                    WHERE DeploymentUID =?",    
                    UpdateRecordList_QCfailDB_Qta)
                                            
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
                conn_DB_SetCatch_Validation_Consistency.commit()
                conn_DB_SetCatch_Validation_Consistency.close()

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

                def UpdateQCFailedDB():
                    def GetUpdateQCFailedListDF(Complete_df):
                        SetCatchQCFailed_DF  = pd.DataFrame(Complete_df)
                        def BuildUpdatedDepUID(SetCatchQCFailed_DF):
                            try:
                                if len(SetCatchQCFailed_DF) >0:
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
                                            list_item_Year,
                                            list_item_ASOCCode,
                                            list_item_DeploymentNumber,
                                            list_item_SetNumber,
                                            list_item_DataBase_ID,
                                            list_item_RecordIdentifier,
                                            ))
                        return UpdateQCFailedListDF
                        
                    conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
                    cursor = conn.cursor()
                    Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
                    Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
                    Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
                    Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
                    Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
                    Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
                    cursor.close()
                    conn.close()

                    Year_FailList_Get = GetUpdateQCFailedListDF(Year_FailConsistency_DF)
                    Country_FailList_Get = GetUpdateQCFailedListDF(Country_FailConsistency_DF)
                    Quota_FailList_Get = GetUpdateQCFailedListDF(Quota_FailConsistency_DF)

                    ## DB Update Executing
                    conn_DB_Set_Catch_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
                    cur_DB_Set_Catch_Consistency=conn_DB_Set_Catch_Consistency.cursor()
                    if (len(Year_FailList_Get)) > 0:
                        cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                            ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                            WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                            Year_FailList_Get)
                    if (len(Country_FailList_Get)) > 0:
                        cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                            ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                            WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                            Country_FailList_Get)
                    if (len(Quota_FailList_Get)) > 0:
                        cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                            ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                            WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                            Quota_FailList_Get)
                    conn_DB_Set_Catch_Consistency.commit()
                    conn_DB_Set_Catch_Consistency.close()
                    
                ## Updating Setcatch DB
                UpdateSetcatchDB()
                ## Updating QC Fail DB - Year-Country- Quota
                UpdateQCFailedDB()

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
            windows.mainloop()   

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def Export_FailedConsistencyVariablesCSV():
        ## Definging getQCFailedDB from DB
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        
        Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
        Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
        Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
        
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        cursor.close()
        conn.close()

        GetSetCatchDB = GetSetCatchProfileDB()
        
        ## For Year_FailConsistency_DF
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Year_FailConsistency_DF['DataBase_ID'] = (Year_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Year_FailConsistency_DF['RecordIdentifier'] = (Year_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Year_FailConsistency_DF['DeploymentUID'] = (Year_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Year_FailConsistency_DF['ObserverNumber'] = (Year_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Year_FailConsistency_DF['VesselSideNumber'] = (Year_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Year_FailConsistency_DF = Year_FailConsistency_DF.reset_index(drop=True)
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        
        ## For Country_FailConsistency_DF
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Country_FailConsistency_DF['DataBase_ID'] = (Country_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Country_FailConsistency_DF['RecordIdentifier'] = (Country_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Country_FailConsistency_DF['DeploymentUID'] = (Country_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Country_FailConsistency_DF['ObserverNumber'] = (Country_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Country_FailConsistency_DF['VesselSideNumber'] = (Country_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Country_FailConsistency_DF = Country_FailConsistency_DF.reset_index(drop=True)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        
        ## For Quota_FailConsistency_DF
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        Quota_FailConsistency_DF['DataBase_ID'] = (Quota_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Quota_FailConsistency_DF['RecordIdentifier'] = (Quota_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Quota_FailConsistency_DF['DeploymentUID'] = (Quota_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Quota_FailConsistency_DF['ObserverNumber'] = (Quota_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Quota_FailConsistency_DF['VesselSideNumber'] = (Quota_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Quota_FailConsistency_DF = Quota_FailConsistency_DF.reset_index(drop=True)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        
        Merge_CountryQuota = Country_FailConsistency_DF.merge(
                        Quota_FailConsistency_DF, 
                        on = ['DataBase_ID','RecordIdentifier', 
                              'DeploymentUID', 'ASOCCode','ObserverNumber',
                              'DeploymentNumber','SetNumber','VesselSideNumber',
                              'RecordType', 'Year', 'Country', 'Quota'], indicator=True, 
                        how='outer')
        Merge_CountryQuota = Merge_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota', 'QC_Country', 'QC_Quota']]
        Merge_CountryQuota = Merge_CountryQuota.reset_index(drop=True)
        Merge_CountryQuota = pd.DataFrame(Merge_CountryQuota)
        
        Merge_Year_CountryQuota = Year_FailConsistency_DF.merge(
                        Merge_CountryQuota, 
                        on = ['DataBase_ID','RecordIdentifier', 
                              'DeploymentUID', 'ASOCCode','ObserverNumber',
                              'DeploymentNumber','SetNumber','VesselSideNumber',
                              'RecordType', 'Year', 'Country', 'Quota'], indicator=True, 
                        how='outer')
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota',
                         'QC_Year', 'QC_Country', 'QC_Quota']]
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.reset_index(drop=True)
        Merge_Year_CountryQuota = pd.DataFrame(Merge_Year_CountryQuota)
        
        ## merging With SetcatchDB
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID', 
                         'QC_Year', 'QC_Country', 'QC_Quota']]
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.reset_index(drop=True)
        Merge_Year_CountryQuota = pd.DataFrame(Merge_Year_CountryQuota)
        Merge_WithSetCatchDB=  GetSetCatchDB.merge(
                        Merge_Year_CountryQuota, 
                        on = ['DataBase_ID','RecordIdentifier','DeploymentUID'],
                        indicator=True, 
                        how='outer').query('_merge == "both"')
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota',
                         'QC_Year', 'QC_Country', 'QC_Quota']]
        Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode',
             'DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country','Quota']]= Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode',
             'DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country','Quota']].astype(int)
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.replace(99999999, '')
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.reset_index(drop=True)
        Merge_WithSetCatchDB = pd.DataFrame(Merge_WithSetCatchDB) 
        Complete_df  = pd.DataFrame(Merge_WithSetCatchDB)
        Complete_df.sort_values(by=['ASOCCode', 'ObserverNumber',
                                    'DeploymentNumber','SetNumber','RecordType'], 
                                inplace=True)
        if len(Complete_df) >0:
            Export_MasterTB_DF  = pd.DataFrame(Complete_df)
            Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
            filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                    defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
            if len(filename) >0:
                Export_MasterTB_DF.to_csv(filename,index=None)
                tkinter.messagebox.showinfo("QC Failed Consistency Profile","QC Failed Consistency Profile Report Saved as CSV")
            else:
                tkinter.messagebox.showinfo("QC Failed Consistency Profile Report Message","Please Select File Name To Export")
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

    def RefFailedToSetcatchDB():
       ## Definging getQCFailedDB from DB
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        
        Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
        Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
        Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
        
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        cursor.close()
        conn.close()

        GetSetCatchDB = GetSetCatchProfileDB()
        GetSetCatchDB['DataBase_ID'] = (GetSetCatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        GetSetCatchDB['RecordIdentifier'] = (GetSetCatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        
       ## For Year_FailConsistency_DF
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Year_FailConsistency_DF['DataBase_ID'] = (Year_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Year_FailConsistency_DF['RecordIdentifier'] = (Year_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Year_FailConsistency_DF['DeploymentUID'] = (Year_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Year_FailConsistency_DF['ASOCCode'] = (Year_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Year_FailConsistency_DF['ObserverNumber'] = (Year_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Year_FailConsistency_DF['DeploymentNumber'] = (Year_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Year_FailConsistency_DF['SetNumber'] = (Year_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Year_FailConsistency_DF['VesselSideNumber'] = (Year_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Year_FailConsistency_DF['RecordType'] = (Year_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Year_FailConsistency_DF['Year'] = (Year_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Year_FailConsistency_DF['Country'] = (Year_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Year_FailConsistency_DF['Quota'] = (Year_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Year_FailConsistency_DF = Year_FailConsistency_DF.reset_index(drop=True)
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        
        ## For Country_FailConsistency_DF
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Country_FailConsistency_DF['DataBase_ID'] = (Country_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Country_FailConsistency_DF['RecordIdentifier'] = (Country_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Country_FailConsistency_DF['DeploymentUID'] = (Country_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Country_FailConsistency_DF['ASOCCode'] = (Country_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Country_FailConsistency_DF['ObserverNumber'] = (Country_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Country_FailConsistency_DF['DeploymentNumber'] = (Country_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Country_FailConsistency_DF['SetNumber'] = (Country_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Country_FailConsistency_DF['VesselSideNumber'] = (Country_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Country_FailConsistency_DF['RecordType'] = (Country_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Country_FailConsistency_DF['Year'] = (Country_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Country_FailConsistency_DF['Country'] = (Country_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Country_FailConsistency_DF['Quota'] = (Country_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Country_FailConsistency_DF = Country_FailConsistency_DF.reset_index(drop=True)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        
        ## For Quota_FailConsistency_DF
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        Quota_FailConsistency_DF['DataBase_ID'] = (Quota_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        Quota_FailConsistency_DF['RecordIdentifier'] = (Quota_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        Quota_FailConsistency_DF['DeploymentUID'] = (Quota_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        Quota_FailConsistency_DF['ASOCCode'] = (Quota_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        Quota_FailConsistency_DF['ObserverNumber'] = (Quota_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        Quota_FailConsistency_DF['DeploymentNumber'] = (Quota_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        Quota_FailConsistency_DF['SetNumber'] = (Quota_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        Quota_FailConsistency_DF['VesselSideNumber'] = (Quota_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)
        
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        Quota_FailConsistency_DF['RecordType'] = (Quota_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Year'] = (Quota_FailConsistency_DF.loc[:,['Year']]).astype(int)

        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Country'] = (Quota_FailConsistency_DF.loc[:,['Country']]).astype(int)

        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        Quota_FailConsistency_DF['Quota'] = (Quota_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        Quota_FailConsistency_DF = Quota_FailConsistency_DF.reset_index(drop=True)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        
        Merge_CountryQuota = Country_FailConsistency_DF.merge(
                        Quota_FailConsistency_DF, 
                        on = ['DataBase_ID','RecordIdentifier', 
                              'DeploymentUID', 'ASOCCode','ObserverNumber',
                              'DeploymentNumber','SetNumber','VesselSideNumber',
                              'RecordType', 'Year', 'Country', 'Quota'], indicator=True, 
                        how='outer')
        Merge_CountryQuota = Merge_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota', 'QC_Country', 'QC_Quota']]
        Merge_CountryQuota = Merge_CountryQuota.reset_index(drop=True)
        Merge_CountryQuota = pd.DataFrame(Merge_CountryQuota)
        
        Merge_Year_CountryQuota = Year_FailConsistency_DF.merge(
                        Merge_CountryQuota, 
                        on = ['DataBase_ID','RecordIdentifier', 
                              'DeploymentUID', 'ASOCCode','ObserverNumber',
                              'DeploymentNumber','SetNumber','VesselSideNumber',
                              'RecordType', 'Year', 'Country', 'Quota'], indicator=True, 
                        how='outer')
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID', 'ASOCCode','ObserverNumber',
                         'DeploymentNumber','SetNumber','VesselSideNumber',
                         'RecordType', 'Year', 'Country', 'Quota',
                         'QC_Year', 'QC_Country', 'QC_Quota']]
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.reset_index(drop=True)
        Merge_Year_CountryQuota = pd.DataFrame(Merge_Year_CountryQuota)
        
        ## merging With SetcatchDB
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID']]
        Merge_Year_CountryQuota = Merge_Year_CountryQuota.reset_index(drop=True)
        Merge_Year_CountryQuota = pd.DataFrame(Merge_Year_CountryQuota)
        Merge_WithSetCatchDB=  GetSetCatchDB.merge(
                        Merge_Year_CountryQuota, 
                        on = ['DataBase_ID','RecordIdentifier','DeploymentUID'],
                        indicator=True, 
                        how='outer').query('_merge == "both"')
        Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode',
             'DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country','Quota']]= Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode',
             'DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country','Quota']].astype(int)
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.replace(99999999, '')
        Merge_WithSetCatchDB = Merge_WithSetCatchDB.reset_index(drop=True)
        Merge_WithSetCatchDB  = Merge_WithSetCatchDB.iloc[:,0:len(list(GetSetCatchDB.columns))]
        
        Ref_FailedQC_InSetcatchDB  = pd.DataFrame(Merge_WithSetCatchDB)
        Ref_FailedQC_InSetcatchDB.sort_values(by=['ASOCCode', 'ObserverNumber',
                                    'DeploymentNumber','SetNumber','RecordType'], 
                                inplace=True)
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
        curItems = tree1.selection()
        if len(curItems)==1:
            sd = tree1.item(curItems, 'values')
            SelvariableIdentifier = sd[2]
        len_curItems = len(curItems)
        if len_curItems < 20001:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,len_curItems)
        else:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,'MaxLimit Exceed')

    def SetcatchDB_VariableList():
        GetSetCatchDB_VariableList = ['Year','Country','Quota']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                         UpdateRecordList_QCFailDB, get_entry_ViewVarResults,
                                         UpdateQCMsg_QCFailDB):
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

        conn_Validation_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cur_Validation_Consistency=conn_Validation_Consistency.cursor()
        
        ## Updaing SetCatch DB
        if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Year = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Country = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Quota = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
        
        ### Updating QC Failed DB
        GetQCFailed_VariableList = ['Year','Country','Quota']
        ListVariableSelect = ['Case-A Year - Consistency @ Each Deployment',
                              'Case-B Country - Consistency @ Each Deployment',
                              'Case-C Quota - Consistency @ Each Deployment']
        
        ## Year-DB Update
        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF \
                                               SET Year = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                               UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET QC_Year =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[1])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF \
                                               SET Country = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                               UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET QC_Year =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[2])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF \
                                        SET Quota = ? \
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET QC_Year =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)

         ## Country-DB Update
        if (get_Updated_Variable == GetQCFailed_VariableList[1])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF \
                                               SET Country = ?  \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET QC_Country =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF \
                                                SET Year = ?  \
                                                WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET QC_Country =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[2])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF \
                                                SET Quota = ?  \
                                                WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET QC_Country =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        ## Quota DB Update
        if (get_Updated_Variable == GetQCFailed_VariableList[2])&(get_entry_ViewVarResults==ListVariableSelect[2]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF \
                                               SET Quota = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET QC_Quota =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[2]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF \
                                               SET Year = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET QC_Quota =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        if (get_Updated_Variable == GetQCFailed_VariableList[1])&(get_entry_ViewVarResults==ListVariableSelect[2]):
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF \
                                               SET Country = ? \
                                               WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
            cur_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET QC_Quota =? \
                                                WHERE DeploymentNumber =?", 
                                                UpdateQCMsg_QCFailDB)
        
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Consistency.commit()
        conn_Validation_Consistency.close()

        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[0]):
            UpdateDeploymentUIDAfterUpdate()
        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[1]):
            UpdateDeploymentUIDAfterUpdate()
        if (get_Updated_Variable == GetQCFailed_VariableList[0])&(get_entry_ViewVarResults==ListVariableSelect[2]):
            UpdateDeploymentUIDAfterUpdate()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18=['Year','Country','Quota']
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
                            list_item_DeploymentNumber = (list_item[5])
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
                                                    list_item_DeploymentNumber))
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
                                list_item_DeploymentNumber = (list_item[5])
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
                                                            list_item_DeploymentNumber))
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
                                "Please Select Atleast One Entries Tp Update") 
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
        ListVariableListA = ['Select Consistency Variable Pair From DropDown & Run View Selected Button', 
                            'Case-A Year - Consistency @ Each Deployment',
                            'Case-B Country - Consistency @ Each Deployment',
                            'Case-C Quota - Consistency @ Each Deployment']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            entry_SelectedCaseTypeEntries.delete(0,END)
            tree1.delete(*tree1.get_children())
            txtQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'QC Variable')
           
        if(SelVariableView ==ListVariableListA[0]):
            entry_SelectedCaseTypeEntries.delete(0,END)
            tree1.delete(*tree1.get_children())
            txtQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'QC Variable ↓↓')
            
        if(SelVariableView ==ListVariableListA[1]):
            entry_SelectedCaseTypeEntries.delete(0,END)
            tree1.delete(*tree1.get_children())
            txtQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'QC Variable : Year ↓↓')
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Year Must Same In All Records Within Deployment')
            
        if(SelVariableView ==ListVariableListA[2]):
            entry_SelectedCaseTypeEntries.delete(0,END)
            tree1.delete(*tree1.get_children())
            txtQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'QC Variable : Country ↓↓')
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Country Must Same In All Records Within Deployment')
        
        if(SelVariableView ==ListVariableListA[3]):
            entry_SelectedCaseTypeEntries.delete(0,END)
            tree1.delete(*tree1.get_children())
            txtQCVariableView.delete(0,END)
            txtQCVariableView.insert(tk.END, 'QC Variable : Quota ↓↓')
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Quota Must Same In All Records Within Deployment')

    def GenSummaryQC():
        txtToUpdateEntriesCount.delete(0,END)
        txtAlreadyUpdateEntriesCount.delete(0,END)
        gettotalQCfailCount = QCFailedTotalEntries()
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
        Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
        Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        cursor.close()
        conn.close()
     
        ## For Year_FailConsistency_DF
        if len(Year_FailConsistency_DF) >0:
            Summary_Year_FailConsistency_DF= Year_FailConsistency_DF.groupby(['ASOCCode', 'ObserverNumber','DeploymentNumber'],  
                    as_index=False)['Year'].apply(lambda x: (len(np.unique(x))))
            Summary_Year_FailConsistency_DF = Summary_Year_FailConsistency_DF[
                        (Summary_Year_FailConsistency_DF.Year) > 1]
            Count_Year_FailConsistency_DF = len(Summary_Year_FailConsistency_DF)
        else:
            Count_Year_FailConsistency_DF = 0
        
        ## For Country_FailConsistency_DF
        if len(Country_FailConsistency_DF) >0:
            Summary_Country_FailConsistency_DF= Country_FailConsistency_DF.groupby(['ASOCCode', 'ObserverNumber','DeploymentNumber'],  
                    as_index=False)['Country'].apply(lambda x: (len(np.unique(x))))
            Summary_Country_FailConsistency_DF = Summary_Country_FailConsistency_DF[
                        (Summary_Country_FailConsistency_DF.Country) > 1]
            Count_Country_FailConsistency_DF = len(Summary_Country_FailConsistency_DF)
        else:
            Count_Country_FailConsistency_DF = 0
        
        ## For Quota_FailConsistency_DF
        if len(Quota_FailConsistency_DF) >0:
            Summary_Quota_FailConsistency_DF= Quota_FailConsistency_DF.groupby(['ASOCCode', 'ObserverNumber','DeploymentNumber'],  
                    as_index=False)['Quota'].apply(lambda x: (len(np.unique(x))))
            Summary_Quota_FailConsistency_DF = Summary_Quota_FailConsistency_DF[
                        (Summary_Quota_FailConsistency_DF.Quota) > 1]
            Count_Quota_FailConsistency_DF = len(Summary_Quota_FailConsistency_DF)
        else:
            Count_Quota_FailConsistency_DF = 0
        
        ### Building Summary DF
        ListYCQ_FailedConsistency = ['Year Consistency',
                                     'Country Consistency',
                                     'Quota Consistency']
        NumYCQ_FailedConsistency = [Count_Year_FailConsistency_DF,
                                    Count_Country_FailConsistency_DF,
                                    Count_Quota_FailConsistency_DF]
        Append_List_NumbFailConsiste = {'VariableName': ListYCQ_FailedConsistency, 
                                        'QCFailCount': NumYCQ_FailedConsistency} 
        YCQ_FailedConsistencySummaryDF = pd.DataFrame(Append_List_NumbFailConsiste)
        YCQ_FailedConsistencySummaryDF[['QCFailCount']] = YCQ_FailedConsistencySummaryDF[['QCFailCount']].astype(int)
        YCQ_FailedConsistencySummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
        YCQ_FailedConsistencySummaryDF  = YCQ_FailedConsistencySummaryDF.reset_index(drop=True)
        YCQ_FailedConsistencySummaryDF  = pd.DataFrame(YCQ_FailedConsistencySummaryDF)
    
        Summaryframetree.delete(*Summaryframetree.get_children())
        SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
        countIndex1 = 0
        for each_rec in range(len(YCQ_FailedConsistencySummaryDF)):
            if countIndex1 % 2 == 0:
                Summaryframetree.insert("", tk.END, values=list(YCQ_FailedConsistencySummaryDF.loc[each_rec]), tags =("even",))
            else:
                Summaryframetree.insert("", tk.END, values=list(YCQ_FailedConsistencySummaryDF.loc[each_rec]), tags =("odd",))
            countIndex1 = countIndex1+1
        Summaryframetree.tag_configure("even",foreground="black", background="lightgreen")
        Summaryframetree.tag_configure("odd",foreground="black", background="ghost white")
        txtSummaryDisplayMsg.delete(0,END)
        txtSummaryDisplayMsg.insert(tk.END,"QC Summary Generated. Select & View Each From List")

        ##Populating ToUpdateEntriesCount & AlreadyUpdateEntriesCount
        QCFailedSummaryCountUpdate = (Count_Year_FailConsistency_DF + \
                                     Count_Country_FailConsistency_DF + \
                                     Count_Quota_FailConsistency_DF)
        AlreadyUpdateEntriesCount =  int(gettotalQCfailCount) - int(QCFailedSummaryCountUpdate)
        txtToUpdateEntriesCount.insert(tk.END,QCFailedSummaryCountUpdate)
        txtAlreadyUpdateEntriesCount.insert(tk.END,AlreadyUpdateEntriesCount)
        
    def InventoryRec3(event):
        ListVariableListA = ['Year Consistency',
                             'Country Consistency',
                             'Quota Consistency']
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
        Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
        Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
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
                                                "# Of Deployment Fail: " + 
                                                NumberEntriesInSet))
            
            if (int(NumberEntriesInSet) > 0):
                ## Main Table A Displaying 
                if(SelvariableIdentifier ==ListVariableListA[0]):
                    tree1.delete(*tree1.get_children())
                    txtQCVariableView.delete(0,END)
                    txtQCVariableView.insert(tk.END, 'Year ↓↓')
                    entry_SelQCVariable.delete(0,END)
                    entry_SelQCVariable.insert(tk.END, 'Year ↓↓')
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'Year Must Same In All Records Within ASOC-ObsNum-DepNum')
                    entry_ViewVarResults.current(1)
                    viewQCFailed_VariablesProfile()
                
                if(SelvariableIdentifier ==ListVariableListA[1]):
                    tree1.delete(*tree1.get_children())
                    txtQCVariableView.delete(0,END)
                    txtQCVariableView.insert(tk.END, 'Country ↓↓')
                    entry_SelQCVariable.delete(0,END)
                    entry_SelQCVariable.insert(tk.END, 'Country ↓↓')
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'Country Must Same In All Records Within ASOC-ObsNum-DepNum')
                    entry_ViewVarResults.current(2)
                    viewQCFailed_VariablesProfile()

                if(SelvariableIdentifier ==ListVariableListA[2]):
                    tree1.delete(*tree1.get_children())
                    txtQCVariableView.delete(0,END)
                    txtQCVariableView.insert(tk.END, 'Quota ↓↓')
                    entry_SelQCVariable.delete(0,END)
                    entry_SelQCVariable.insert(tk.END, 'Quota ↓↓')
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, 'Quota Must Same In All Records Within ASOC-ObsNum-DepNum')
                    entry_ViewVarResults.current(3)
                    viewQCFailed_VariablesProfile()
            
            else:
                txtSummaryDisplayMsg.delete(0,END)
                txtSummaryDisplayMsg.insert(tk.END,"Empty QCCaseType - All Updated Or No Fail Found")
                tree1.delete(*tree1.get_children())
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                txtQCVariableView.delete(0,END)
                entry_ViewVarResults.current(0)
                txtDisplayMessageSystem.delete(0,END)
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, (' Please Select Only One Entries To View'))
            txtSummaryDisplayMsg.delete(0,END)
            txtSummaryDisplayMsg.insert(tk.END,"Please Select Only One Entries To View")

    def InventoryRec4(event):
        ListCaseType = ['Year ↓↓',
                        'Country ↓↓',
                        'Quota ↓↓']
        ListSelCaseType = ['Year ↓↓',
                        'Country ↓↓',
                        'Quota ↓↓']
        tree1.delete(*tree1.get_children())
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
        Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
        Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
        Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
        Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
        Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
        cursor.close()
        conn.close()
        ## SelResultOverviewtree selection
        nm =SelResultOverviewtree.selection()
        if len(nm) ==1:
            sd = SelResultOverviewtree.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            SelectedDepNum = sd[1]
            SelectedASOCNum = sd[2]
            SelectedObsNum = sd[3]
            SelectedNumSet = sd[4]
            getQCVar_entry_SelQCVariable = entry_SelQCVariable.get()
            getQCVar_txtQCVariableView = txtQCVariableView.get()
            txtDisplayMessageSystem.delete(0,END)
            entry_SearchDepNumSetCatchDB.delete(0,END)
            txtDisplayMessageSystem.insert(1, (getQCVar_txtQCVariableView +' Must Same In All Records Within Deployment'))
            txtDisplayMessageSystem.insert(2, (getQCVar_entry_SelQCVariable + ("Code : ") +
                                                SelvariableIdentifier + ' ' +' & '+
                                                "# Of SetNumber Found: " + 
                                                SelectedNumSet))
            entry_SearchDepNumSetCatchDB.insert(tk.END,SelectedDepNum)
            if (getQCVar_entry_SelQCVariable == ListCaseType[0]) &\
            (getQCVar_txtQCVariableView == ListSelCaseType[0]):
                Year_FailConsistency_DF = (Year_FailConsistency_DF.loc[:,
                                    ['DataBase_ID','RecordIdentifier', 
                                    'DeploymentUID', 'ASOCCode',
                                    'ObserverNumber','DeploymentNumber',
                                    'SetNumber','VesselSideNumber',
                                    'RecordType', 'Year',
                                    'Country','Quota', 'QC_Year']]).replace(
                            ['', None, np.nan, 'None'], 99999999)
                            
                Year_FailConsistency_DF[['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']] = Year_FailConsistency_DF[
                        ['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']].astype(int)
                
                Year_FailConsistency_DF[['DeploymentUID','ObserverNumber', 'VesselSideNumber']] = Year_FailConsistency_DF[
                ['DeploymentUID','ObserverNumber', 'VesselSideNumber']].astype(str)
                Year_FailConsistency_DF = Year_FailConsistency_DF.replace([99999999, 99999999.0, '99999999'], '')
                Year_FailConsistency_DF = Year_FailConsistency_DF.reset_index(drop=True)
                Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)    
                try:
                    Year_FailConsistency_DF = Year_FailConsistency_DF[(
                    (Year_FailConsistency_DF['Year'] == int(SelvariableIdentifier)) &\
                    (Year_FailConsistency_DF['DeploymentNumber'] == int(SelectedDepNum)) &\
                    (Year_FailConsistency_DF['ASOCCode'] == int(SelectedASOCNum))
                    )]
                except:
                    Year_FailConsistency_DF = Year_FailConsistency_DF[(
                    (Year_FailConsistency_DF['Year'] == (SelvariableIdentifier)) &\
                    (Year_FailConsistency_DF['DeploymentNumber'] == int(SelectedDepNum)) &\
                    (Year_FailConsistency_DF['ASOCCode'] == int(SelectedASOCNum))
                    )]
                Year_FailConsistency_DF  = Year_FailConsistency_DF.reset_index(drop=True)
                QCFailDF_Selected  = pd.DataFrame(Year_FailConsistency_DF)
                QCFailDF_Selected.sort_values(
                    by=['ASOCCode','ObserverNumber','DeploymentNumber',
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
                tree1.tag_configure("even",foreground="black", background="grey")
                tree1.tag_configure("odd",foreground="black", background="grey")
        
            if (getQCVar_entry_SelQCVariable == ListCaseType[1]) &\
            (getQCVar_txtQCVariableView == ListSelCaseType[1]):
                Country_FailConsistency_DF = (Country_FailConsistency_DF.loc[:,
                                    ['DataBase_ID','RecordIdentifier', 
                                    'DeploymentUID', 'ASOCCode',
                                    'ObserverNumber','DeploymentNumber',
                                    'SetNumber','VesselSideNumber',
                                    'RecordType', 'Year',
                                    'Country','Quota','QC_Country']]).replace(
                            ['', None, np.nan, 'None'], 99999999)
                            
                Country_FailConsistency_DF[['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']] = Country_FailConsistency_DF[
                        ['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']].astype(int)
                
                Country_FailConsistency_DF[['DeploymentUID','ObserverNumber', 'VesselSideNumber']] = Country_FailConsistency_DF[
                ['DeploymentUID','ObserverNumber', 'VesselSideNumber']].astype(str)
                Country_FailConsistency_DF = Country_FailConsistency_DF.replace([99999999, 99999999.0, '99999999'], '')
                Country_FailConsistency_DF = Country_FailConsistency_DF.reset_index(drop=True)
                Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)    
                try:
                    Country_FailConsistency_DF = Country_FailConsistency_DF[(
                    (Country_FailConsistency_DF['Country'] == int(SelvariableIdentifier)) &\
                    (Country_FailConsistency_DF['DeploymentNumber'] == int(SelectedDepNum)) &\
                    (Country_FailConsistency_DF['ASOCCode'] == int(SelectedASOCNum))
                    )]
                except:
                    Country_FailConsistency_DF = Country_FailConsistency_DF[(
                    (Country_FailConsistency_DF['Country'] == (SelvariableIdentifier)) &\
                    (Country_FailConsistency_DF['DeploymentNumber'] == int(SelectedDepNum)) &\
                    (Country_FailConsistency_DF['ASOCCode'] == int(SelectedASOCNum))
                    )]
                Country_FailConsistency_DF  = Country_FailConsistency_DF.reset_index(drop=True)
                QCFailDF_Selected  = pd.DataFrame(Country_FailConsistency_DF)
                QCFailDF_Selected.sort_values(
                    by=['ASOCCode','ObserverNumber','DeploymentNumber',
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
                tree1.tag_configure("even",foreground="black", background="grey")
                tree1.tag_configure("odd",foreground="black", background="grey")
            
            if (getQCVar_entry_SelQCVariable == ListCaseType[2]) &\
            (getQCVar_txtQCVariableView == ListSelCaseType[2]):
                Quota_FailConsistency_DF = (Quota_FailConsistency_DF.loc[:,
                                    ['DataBase_ID','RecordIdentifier', 
                                    'DeploymentUID', 'ASOCCode',
                                    'ObserverNumber','DeploymentNumber',
                                    'SetNumber','VesselSideNumber',
                                    'RecordType', 'Year',
                                    'Country','Quota','QC_Quota']]).replace(
                            ['', None, np.nan, 'None'], 99999999)
                            
                Quota_FailConsistency_DF[['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']] = Quota_FailConsistency_DF[
                        ['DataBase_ID','RecordIdentifier',
                        'ASOCCode','DeploymentNumber', 
                        'SetNumber', 'RecordType', 
                        'Year','Country','Quota']].astype(int)
                
                Quota_FailConsistency_DF[['DeploymentUID','ObserverNumber', 'VesselSideNumber']] = Quota_FailConsistency_DF[
                ['DeploymentUID','ObserverNumber', 'VesselSideNumber']].astype(str)
                Quota_FailConsistency_DF = Quota_FailConsistency_DF.replace([99999999, 99999999.0, '99999999'], '')
                Quota_FailConsistency_DF = Quota_FailConsistency_DF.reset_index(drop=True)
                Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)    
                try:
                    Quota_FailConsistency_DF = Quota_FailConsistency_DF[(
                    (Quota_FailConsistency_DF['Quota'] == int(SelvariableIdentifier)) &\
                    (Quota_FailConsistency_DF['DeploymentNumber'] == int(SelectedDepNum)) &\
                    (Quota_FailConsistency_DF['ASOCCode'] == int(SelectedASOCNum))
                    )]
                except:
                    Quota_FailConsistency_DF = Quota_FailConsistency_DF[(
                    (Quota_FailConsistency_DF['Quota'] == (SelvariableIdentifier)) &\
                    (Quota_FailConsistency_DF['DeploymentNumber'] == int(SelectedDepNum)) &\
                    (Quota_FailConsistency_DF['ASOCCode'] == int(SelectedASOCNum))
                    )]
                Quota_FailConsistency_DF  = Quota_FailConsistency_DF.reset_index(drop=True)
                QCFailDF_Selected  = pd.DataFrame(Quota_FailConsistency_DF)
                QCFailDF_Selected.sort_values(
                    by=['ASOCCode','ObserverNumber','DeploymentNumber',
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
                tree1.tag_configure("even",foreground="black", background="grey")
                tree1.tag_configure("odd",foreground="black", background="grey")
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, (' Please Select Only One Entries To View'))

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
                                    list_item_Year,
                                    list_item_ASOCCode,
                                    list_item_DeploymentNumber,
                                    list_item_SetNumber,
                                    list_item_DataBase_ID,
                                    list_item_RecordIdentifier,
                                    ))
                return UpdateQCFailedListDF
                
            conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
            cursor = conn.cursor()
            Year_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Year_FailConsistency_DF;", conn)
            Country_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Country_FailConsistency_DF;", conn)
            Quota_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_Quota_FailConsistency_DF;", conn)
            Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
            Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
            Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
            cursor.close()
            conn.close()

            Year_FailList_Get = GetUpdateQCFailedListDF(Year_FailConsistency_DF)
            Country_FailList_Get = GetUpdateQCFailedListDF(Country_FailConsistency_DF)
            Quota_FailList_Get = GetUpdateQCFailedListDF(Quota_FailConsistency_DF)

            ## DB Update Executing
            conn_DB_Set_Catch_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
            cur_DB_Set_Catch_Consistency=conn_DB_Set_Catch_Consistency.cursor()
            if (len(Year_FailList_Get)) > 0:
                cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                    ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    Year_FailList_Get)
            if (len(Country_FailList_Get)) > 0:
                cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                    ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    Country_FailList_Get)
            if (len(Quota_FailList_Get)) > 0:
                cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                    ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                    Quota_FailList_Get)
            conn_DB_Set_Catch_Consistency.commit()
            conn_DB_Set_Catch_Consistency.close()
                    
        ## Updating QC Fail DB - SetCatch DB
        UpdateSetcatchDB()
        ## Updating QC Fail DB - Year-Country- Quota
        UpdateQCFailedDB()
        tree1.delete(*tree1.get_children())
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    def SearchDepNumFromSetCatchDB():
        get_DepNumforSearch = (entry_SearchDepNumSetCatchDB.get())
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
                    rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                    conn_DB.commit()
                    conn_DB.close()
                    rows= (rows.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                        'DeploymentUID', 'ASOCCode','ObserverNumber',
                        'DeploymentNumber','SetNumber','VesselSideNumber',
                        'RecordType', 'Year', 'Country', 'Quota']])
                    rows = rows[(rows.DeploymentNumber) == get_SearchSingleVariable_Value]
                    rows  = rows.reset_index(drop=True)
                    rows  = pd.DataFrame(rows)
                    rows['DataBase_ID'] = (rows.loc[:,['DataBase_ID']]).astype(int)
                    rows['RecordIdentifier'] = (rows.loc[:,['RecordIdentifier']]).astype(int)
                    rows['DeploymentUID'] = (rows.loc[:,['DeploymentUID']]).astype(str)

                    rows['ASOCCode'] = (rows.loc[:,['ASOCCode']]).fillna(99999999)
                    rows['ASOCCode'] = (rows.loc[:,['ASOCCode']]).replace([''], 99999999)
                    rows['ASOCCode'] = (rows.loc[:,['ASOCCode']]).astype(int)

                    rows['ObserverNumber'] = (rows.loc[:,['ObserverNumber']]).astype(str)

                    rows['DeploymentNumber'] = (rows.loc[:,['DeploymentNumber']]).fillna(99999999)
                    rows['DeploymentNumber'] = (rows.loc[:,['DeploymentNumber']]).replace([''], 99999999)
                    rows['DeploymentNumber'] = (rows.loc[:,['DeploymentNumber']]).astype(int)
                    
                    rows['SetNumber'] = (rows.loc[:,['SetNumber']]).fillna(99999999)
                    rows['SetNumber'] = (rows.loc[:,['SetNumber']]).replace([''], 99999999)
                    rows['SetNumber'] = (rows.loc[:,['SetNumber']]).astype(int)

                    rows['VesselSideNumber'] = (rows.loc[:,['VesselSideNumber']]).astype(str)
                    
                    rows['RecordType'] = (rows.loc[:,['RecordType']]).fillna(99999999)
                    rows['RecordType'] = (rows.loc[:,['RecordType']]).replace([''], 99999999)
                    rows['RecordType'] = (rows.loc[:,['RecordType']]).astype(int)

                    rows['Year'] = (rows.loc[:,['Year']]).fillna(99999999)
                    rows['Year'] = (rows.loc[:,['Year']]).replace([''], 99999999)
                    rows['Year'] = (rows.loc[:,['Year']]).astype(int)

                    rows['Country'] = (rows.loc[:,['Country']]).fillna(99999999)
                    rows['Country'] = (rows.loc[:,['Country']]).replace([''], 99999999)
                    rows['Country'] = (rows.loc[:,['Country']]).astype(int)
                    
                    rows['Quota'] = (rows.loc[:,['Quota']]).fillna(99999999)
                    rows['Quota'] = (rows.loc[:,['Quota']]).replace([''], 99999999)
                    rows['Quota'] = (rows.loc[:,['Quota']]).astype(int)
                    rows  = rows.reset_index(drop=True)
                    SearchDepNSetCatchDF = pd.DataFrame(rows)
                    SearchDepNSetCatchDF[
                                        ['DataBase_ID','RecordIdentifier', 
                                        'ASOCCode',
                                        'DeploymentNumber','SetNumber',
                                        'RecordType', 'Year','Country','Quota']]= SearchDepNSetCatchDF[
                                        ['DataBase_ID','RecordIdentifier', 
                                        'ASOCCode',
                                        'DeploymentNumber','SetNumber',
                                        'RecordType', 'Year','Country','Quota']].astype(int)
                    SearchDepNSetCatchDF = SearchDepNSetCatchDF.replace(99999999, '')
                    SearchDepNSetCatchDF = SearchDepNSetCatchDF[(SearchDepNSetCatchDF.RecordType) == 1]
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
                            Complete_df = (Complete_df.loc[:,
                                    ['DataBase_ID','RecordIdentifier', 
                                    'DeploymentUID', 'ASOCCode',
                                    'ObserverNumber','DeploymentNumber',
                                    'SetNumber','VesselSideNumber',
                                    'RecordType', 'Year',
                                    'Country','Quota']]).replace(
                            ['', None, np.nan, 'None'], 99999999)
                            
                            Complete_df[['DataBase_ID','RecordIdentifier',
                                    'ASOCCode','DeploymentNumber', 
                                    'SetNumber', 'RecordType', 
                                    'Year','Country','Quota']] = Complete_df[
                                    ['DataBase_ID','RecordIdentifier',
                                    'ASOCCode','DeploymentNumber', 
                                    'SetNumber', 'RecordType', 
                                    'Year','Country','Quota']].astype(int)
                           
                            Complete_df[['DeploymentUID','ObserverNumber', 'VesselSideNumber']] = Complete_df[
                            ['DeploymentUID','ObserverNumber', 'VesselSideNumber']].astype(str)
                            Complete_df = Complete_df.replace([99999999, 99999999.0, '99999999'], '')
                            Complete_df = Complete_df.reset_index(drop=True)
                            Complete_df = pd.DataFrame(Complete_df)    
                            if len(Complete_df) >0:
                                iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                                        "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                                if iSubmit >0:
                                    try:
                                        BackendSubmitAndUpdateDB(Complete_df)
                                    except sqlite3.Error as error:
                                        print('Error occured - ', error)
                                    finally:
                                        UpdateDeploymentUIDAfterUpdate()
                                        pt.redraw()
                                        tkinter.messagebox.showinfo("Submit Success","Successfully Submitted Update To Database")
                            else:
                                tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

                        def BackendSubmitAndUpdateDB(Complete_df):
                            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                            conn_DB_SetCatch_Validation_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
                            cur_DB_SetCatch_Validation_Consistency=conn_DB_SetCatch_Validation_Consistency.cursor()
                            UpdateRecordList_SetCatchDB =[]
                            UpdateRecordList_QCfailDB_Yr =[]
                            UpdateRecordList_QCfailDB_Cntry =[]
                            UpdateRecordList_QCfailDB_Qta =[]
                            df_rows = Complete_df.to_numpy().tolist()
                            for row in df_rows:
                                rowValue = row
                                list_item_DataBase_ID = int(rowValue[0])
                                list_item_RecordIdentifier = int(rowValue[1])
                                list_item_DeploymentUID = (rowValue[2])
                                list_item_ASOCCode = (rowValue[3])
                                list_item_ObserverNumber = (rowValue[4])
                                list_item_DeploymentNumber = (rowValue[5])
                                list_item_SetNumber = (rowValue[6])
                                list_item_VesselSideNumber = (rowValue[7])
                                list_item_RecordType = (rowValue[8])
                                list_item_Year = (rowValue[9])
                                list_item_Country = (rowValue[10])
                                list_item_Quota = (rowValue[11])
                                list_item_QCMsg = ''
                        
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_DeploymentUID))                  
                                
                                UpdateRecordList_QCfailDB_Yr.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_QCMsg,
                                                    list_item_DeploymentUID))
                                
                                UpdateRecordList_QCfailDB_Cntry.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_QCMsg,
                                                    list_item_DeploymentUID))
                                
                                UpdateRecordList_QCfailDB_Qta.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_Year,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_QCMsg,
                                                    list_item_DeploymentUID))
                                                
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                                ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                                SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =? \
                                WHERE DeploymentUID =?", 
                                UpdateRecordList_SetCatchDB)
                            
                            cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Year_FailConsistency_DF SET \
                                ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                                SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =?, QC_Year =? \
                                WHERE DeploymentUID =?",   
                                UpdateRecordList_QCfailDB_Yr)
                            
                            cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Country_FailConsistency_DF SET \
                                ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                                SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =?, QC_Country =? \
                                WHERE DeploymentUID =?",    
                                UpdateRecordList_QCfailDB_Cntry)
                            
                            cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_Quota_FailConsistency_DF SET \
                                ASOCCode = ?, ObserverNumber = ?, DeploymentNumber = ?,\
                                SetNumber = ?, VesselSideNumber = ?, Year =?, Country =?, Quota =?, QC_Quota =? \
                                WHERE DeploymentUID =?",    
                                UpdateRecordList_QCfailDB_Qta)
                                                        
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Consistency.commit()
                            conn_DB_SetCatch_Validation_Consistency.close()

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
                        windows.mainloop()   
                                
                    else:
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(0, 'Empty Search Returned')
                        tkinter.messagebox.showinfo("Empty Set&Catch Entries","Empty Search Returned")     

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
    
    # Top Frame Button
    btnClearTable = Button(Topframe, text="Clear Table", font=('aerial', 9, 'bold'), bg='alice blue',
                                height =1, width=10, bd=1, command = ClearTablesAll)
    btnClearTable.grid(row =2, column = 0, padx=380, pady =2, ipady =2, sticky =W)

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
    button_GenSummaryQC = Button(Summaryframe, bd = 2, text ="Generate QC Summary ", width = 20,
                                height=1, font=('aerial', 11, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSummaryQC)
    button_GenSummaryQC.pack(side =TOP)

    button_SearchDepNumSetCatchDB = Button(SelQCVariableDisplay, bd = 1, text ="View DepNum In SetCatchDB", width = 25,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =SearchDepNumFromSetCatchDB)
    button_SearchDepNumSetCatchDB.grid(row =0, column = 0, padx=35, pady =2, ipady =2, sticky =E)

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
    ImportExport.add_command(label="Export Failed Results (.csv)", command=Export_FailedConsistencyVariablesCSV)
    ImportExport.add_command(label="Import & Update DB (.csv)", command=ImportAndUpdateSetCatchDB)
    View.add_command(label="View Edit & Update QCFailed Results", command=QCFailedExcelViewAll)
    View.add_command(label="Ref-QCFail To Set&Catch DB", command=RefFailedToSetcatchDB)
    Update.add_command(label="Update DeplymentUID", command=UpdateDeploymentUIDAfterUpdate)
    
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack(side = LEFT)
    window.mainloop()



