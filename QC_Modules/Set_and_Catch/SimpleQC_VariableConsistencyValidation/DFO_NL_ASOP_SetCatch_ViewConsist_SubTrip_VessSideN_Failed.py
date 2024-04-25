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

def ViewConsis_VSN_STN_ValResult():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Consistency Validator - ID-C-05-2")
    window.geometry("1465x825+200+100")
    window.config(bg="cadet blue")

    ## Top Frame Define
    TopFrame = tk.Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    TopFrame.pack(side = TOP, padx= 0, pady=0)

    lbl_TopFrame = Label(TopFrame, font=('aerial', 10, 'bold'), bg= "cadet blue", text="A. QC Fail Table (Vessel-SubTrip#) :")
    lbl_TopFrame.grid(row =1, column = 0, padx=2, pady =1, ipady=1, sticky =W)

    ListVariableListA = ['Select VesselSideNumber-SubTripNumber(VSN-STN) Consistency View Type', 
                        'View VSN-STN Consistency Fail With RecType-1,2',
                        'View VSN-STN Consistency Fail With RecType-1 Only']
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

    lbl_TotalFailedEntries = Label(TopFrame, font=('aerial', 10 , 'bold'), text="# Of SubTrip Failed :")
    lbl_TotalFailedEntries.grid(row =0, column = 0, padx=1, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(TopFrame, value='')
    txtTotalFailedEntries = Entry(TopFrame, font=('aerial',12),textvariable = TotalFailedEntries, width = 4, bd=1)
    txtTotalFailedEntries.grid(row =0, column = 0, padx=132, pady =1, ipady =1, sticky =W)

    txtDisplayMessageSystem = Entry(TopFrame, font=('aerial', 9), justify='center',
                            textvariable = StringVar(window, value='QC Message Display'), width = 84, bd=2)
    txtDisplayMessageSystem.grid(row =0, column = 1, padx=40, pady =2, ipady =5, sticky =W)

    Tableframe = Frame(window, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    # Tree1 Define
    tree1 = ttk.Treeview(Tableframe, 
            column=("column1", "column2", "column3", 
                    "column4", "column5", "column6", 
                    "column7", "column8", "column9",
                    "column10", "column11", "column12", "column13", 
                    "column14", "column15", "column16"), height=22, show='headings')
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
    tree1.heading("#1", text="DB_ID", anchor=CENTER)
    tree1.heading("#2", text="RecordIdentifier", anchor=CENTER)
    tree1.heading("#3", text="DeploymentUID", anchor=CENTER)
    tree1.heading("#4", text="ASOCCode", anchor=CENTER)
    tree1.heading("#5", text="Obs#", anchor=CENTER)
    tree1.heading("#6", text="DeploymentNumber", anchor=CENTER)
    tree1.heading("#7", text="SetNumber", anchor=CENTER)
    tree1.heading("#8", text="Year", anchor=CENTER)
    tree1.heading("#9", text="RecordType", anchor=CENTER)
    tree1.heading("#10", text="Country", anchor=CENTER)
    tree1.heading("#11", text="Quota", anchor=CENTER)
    tree1.heading("#12", text="SubTripNumber", anchor=CENTER)
    tree1.heading("#13", text="VesselSideNumber", anchor=CENTER)
    tree1.heading("#14", text="VesselClass", anchor=CENTER)
    tree1.heading("#15", text="QC_Message", anchor=CENTER)
    tree1.heading("#16", text="QC_CaseType", anchor=CENTER)

    tree1.column('#1', stretch=NO, minwidth=0, width=60, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#9', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    tree1.column('#10', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)
    tree1.column('#11', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    tree1.column('#12', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)            
    tree1.column('#13', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree1.column('#14', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    tree1.column('#15', stretch=NO, minwidth=0, width=430, anchor = tk.CENTER)
    tree1.column('#16', stretch=NO, minwidth=0, width=170, anchor = tk.CENTER)            
    
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
    
    ListUpdateVar = ['SubTripNumber','VesselSideNumber', 'VesselClass']
    UpdateVar = StringVar(UpdateDB_Entryframe, value ='')
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

    ##### Frame Generate QC Failed Summary ############
    SummaryQCframe = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.pack(side =LEFT, padx=10, pady =2)
    lbl_SummaryQCframe = Label(SummaryQCframe, font=('aerial', 10, 'bold','underline'), 
                                bg= "cadet blue", text="B: QC Fail Summary (Vessel-SubTrip#)")
    lbl_SummaryQCframe.pack(side =TOP, anchor =W)
    
    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    Summaryframetree = ttk.Treeview(Summaryframe, column=("column1", "column2",
                        "column3", "column4", "column5", "column6"),height=6, show='headings')
    scrollbary = ttk.Scrollbar(Summaryframe, orient ="vertical", command=Summaryframetree.yview)
    scrollbary.pack(side ='right', fill ='y')
    Summaryframetree.configure(yscrollcommand = scrollbary.set)
    Summaryframetree.heading("#1", text="ASOCCode")
    Summaryframetree.heading("#2", text="ObsNumber")
    Summaryframetree.heading("#3", text="Country")
    Summaryframetree.heading("#4", text="Year")
    Summaryframetree.heading("#5", text="DeploymentNumber")
    Summaryframetree.heading("#6", text="# Of SubTrip Fail In QC")
    Summaryframetree.column('#1', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)            
    Summaryframetree.column('#2', stretch=NO, minwidth=0, width=90, anchor = tk.CENTER)
    Summaryframetree.column('#3', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)            
    Summaryframetree.column('#4', stretch=NO, minwidth=0, width=67, anchor = tk.CENTER)
    Summaryframetree.column('#5', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    Summaryframetree.column('#6', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    Summaryframetree.pack(side = BOTTOM)
    
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    SummaryDisplay.pack(side = BOTTOM, pady=0)
    QcValue = "VSN Inconsistence With STN By Year-ASOC-Obs#-Dep#-Country-Quota-VessClass"
    txtSummaryDisplayMsg = Entry(SummaryDisplay, font=('aerial', 10),
                            textvariable = StringVar(window, value=QcValue), width = 85, bd=2)
    txtSummaryDisplayMsg.grid(row =0, column = 0, padx=2, pady =2, ipady =2, sticky =E)

    lbl_DepNumtoUpdate = Label(SummaryDisplay, font=('aerial', 9 , 'bold'), text="# of DepNum To Update")
    lbl_DepNumtoUpdate.grid(row =2, column = 0, padx=2, pady =1, ipady=1, sticky =W)
    
    DepNumtoUpdateCount = IntVar(SummaryDisplay, value='')
    txtDepNumtoUpdateCount = Entry(SummaryDisplay, font=('aerial',8),
                                   textvariable = DepNumtoUpdateCount, 
                                   width = 8, bd=1)
    txtDepNumtoUpdateCount.grid(row =2, column = 0, padx=140, pady =2, ipady =2, sticky =W)
    
    lbl_TripNumtoUpdate = Label(SummaryDisplay, font=('aerial', 9 , 'bold'), text="# of Trip To Update")
    lbl_TripNumtoUpdate.grid(row =2, column = 0, padx=2, pady =1, ipady=1, sticky =E)
    
    TripNumtoUpdateCount = IntVar(SummaryDisplay, value='')
    txtTripNumtoUpdateCount = Entry(SummaryDisplay, font=('aerial',8),
                                   textvariable = TripNumtoUpdateCount, 
                                   width = 8, bd=1)
    txtTripNumtoUpdateCount.grid(row =2, column = 0, padx=118, pady =2, ipady =2, sticky =E)

    ##### Frame Of Selected Results Overview modules #####
    SelQCVariableDisplay = tk.Frame(window, bg= "aliceblue")
    SelQCVariable      = StringVar(SelQCVariableDisplay, value ='')
    entry_SelQCVariable = Entry(SelQCVariableDisplay, font=('aerial', 10, 'bold'),  justify = tk.CENTER,
                            textvariable = SelQCVariable, width = 13, bd=2)
    entry_SelQCVariable.grid(row =0, column = 0, padx=2, pady =2, ipady =2, sticky =W)

    GenSummarySetcatchDB      = StringVar(SelQCVariableDisplay, value ='ASOC-Obs#-Country-Year-Dep#')
    entry_GenSummarySetcatchDB = Entry(SelQCVariableDisplay, font=('aerial', 8, 'bold'),  justify = tk.CENTER,
                            textvariable = GenSummarySetcatchDB, width = 30, bd=2)
    entry_GenSummarySetcatchDB.grid(row =0, column = 0, padx=345, pady =2, ipady =2, sticky =W)

    SelQCVariableDisplay.pack(side = TOP, pady=0, anchor = CENTER)
    
    # Define TreeView SelResultOverviewtree
    SelResultOverview = tk.Frame(window, bd = 2,relief = RIDGE, bg= "cadet blue")
    SelResultOverview.pack(side =LEFT, padx=2, pady =2)
    SelResultOverviewtree = ttk.Treeview(SelResultOverview,  
                            column=("column1", "column2", 
                                    "column3", "column4", "column5"), height=9, show='headings')
    scrollbary = ttk.Scrollbar(SelResultOverview, orient ="vertical", command=SelResultOverviewtree.yview)
    scrollbary.pack(side ='right', fill ='y')
    SelResultOverviewtree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(SelResultOverview, orient ="horizontal", command=SelResultOverviewtree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    SelResultOverviewtree.configure(xscrollcommand = scrollbarx.set)
    SelResultOverviewtree.heading("#1", text="SubTripNumberUID", anchor=CENTER)
    SelResultOverviewtree.heading("#2", text="VessClass", anchor=CENTER)
    SelResultOverviewtree.heading("#3", text="VessSideNum", anchor=CENTER)
    SelResultOverviewtree.heading("#4", text="#ofSets", anchor=CENTER)
    SelResultOverviewtree.heading("#5", text="#ofRecords", anchor=CENTER)
    
    SelResultOverviewtree.column('#1', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    SelResultOverviewtree.column('#2', stretch=NO, minwidth=0, width=90, anchor = tk.CENTER)             
    SelResultOverviewtree.column('#3', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    SelResultOverviewtree.column('#4', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
    SelResultOverviewtree.column('#5', stretch=NO, minwidth=0, width=80, anchor = tk.CENTER)
   
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    SelResultOverviewtree.pack(side = BOTTOM)

## ######All Defined Functions ####### 
    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names =  [
            'DataBase_ID','RecordIdentifier','DeploymentUID',
            'ASOCCode','ObserverNumber','DeploymentNumber',
            'SetNumber', 'Year','RecordType','Country','Quota',
            'SubTripNumber','VesselSideNumber', 'VesselClass', 
            'QC_Message','QC_CaseType'
            ]
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
                        Year = (df.loc[:,'Year']).fillna(99999999).astype(int, errors='ignore')
                        RecordType = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        Country = (df.loc[:,'Country']).fillna(99999999).astype(int, errors='ignore')
                        Quota = (df.loc[:,'Quota']).fillna(99999999).astype(int, errors='ignore')
                        SubTripNumber = (df.loc[:,'SubTripNumber']).fillna(8888888).astype(str)
                        VesselSideNumber = (df.loc[:,'VesselSideNumber']).fillna(8888888).astype(str)
                        VesselClass = (df.loc[:,'VesselClass']).fillna(99999999).astype(int, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID,\
                                        ASOCCode, ObserverNumber, DeploymentNumber, \
                                        SetNumber, Year, RecordType, Country, Quota, \
                                        SubTripNumber, VesselSideNumber, VesselClass]
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                    if Return_Message == ReturnMatchedMessage:
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns=  {0:'DataBase_ID', 1: 'RecordIdentifier', 2: 'DeploymentUID',
                                                3:'ASOCCode', 4:'ObserverNumber', 5:'DeploymentNumber', 
                                                6:'SetNumber', 7:'Year',
                                                8:'RecordType', 9:'Country', 10:'Quota',
                                                11:'SubTripNumber', 12:'VesselSideNumber', 13:'VesselClass'},inplace = True)
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
                                            (Raw_Imported_Df.VesselClass =='')
                                            ]
                    Len_CheckEmptyNessColumn =len(CheckEmptyNessColumn)
                    if Len_CheckEmptyNessColumn==0:
                        Length_Raw_Imported_Df  =  len(Raw_Imported_Df)
                        if Length_Raw_Imported_Df <250000:
                            UpdateRecordList_SetCatchDB =[]
                            UpdateRecordList_QCfailDB =[]
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
                                list_item_Year = (rowValue[7])
                                list_item_RecordType = (rowValue[8])
                                list_item_Country = (rowValue[9])
                                list_item_Quota = (rowValue[10])
                                list_item_SubTripNumber = (rowValue[11])
                                list_item_VesselSideNumber = (rowValue[12])
                                list_item_VesselClass = (rowValue[13])
                                list_item_QC_CaseType = 'Case: Updated'
                                
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_Year,
                                                    list_item_RecordType,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_SubTripNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_VesselClass,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                UpdateRecordList_QCfailDB.append((
                                                    list_item_ASOCCode,
                                                    list_item_ObserverNumber,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_Year,
                                                    list_item_RecordType,
                                                    list_item_Country,
                                                    list_item_Quota,
                                                    list_item_SubTripNumber,
                                                    list_item_VesselSideNumber,
                                                    list_item_VesselClass,
                                                    list_item_QC_CaseType,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                             
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ?, \
                                                    ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, Year =?,\
                                                    RecordType = ? , Country = ? , Quota = ?, SubTripNumber = ?,\
                                                    VesselSideNumber = ?, VesselClass =?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                            
                            cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF  SET ASOCCode = ?, \
                                                    ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, Year =?,\
                                                    RecordType = ? , Country = ? , Quota = ?, SubTripNumber = ?,\
                                                    VesselSideNumber = ?, VesselClass =?, QC_CaseType =?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_QCfailDB)
                                                     
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Consistency.commit()
                            conn_DB_SetCatch_Validation_Consistency.close()
                            GenSummaryQC()
                            txtDisplayMessageSystem.delete(0,END)
                            txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                            tkinter.messagebox.showinfo("Update Success","Successfully Updated The Imported Entries")
                    else:
                        messagebox.showerror('Empty Variables', "Please Check Null Variables (DataBase_ID, RecordIdentifier, DeploymentUID,\
                                                                ASOCCode, ObserverNumber, DeploymentNumber, \
                                                                SetNumber, VesselSideNumber, RecordType, Country) Input")

    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def ClearTablesAll():
        tree1.delete(*tree1.get_children())
        SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
        Summaryframetree.delete(*Summaryframetree.get_children())
        entry_ViewVarResults.current(0)
        entry_SelQCVariable.delete(0,END)
        txtDisplayMessageSystem.delete(0,END)
        
    def ClearEntries():
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateValue_VariableA.delete(0,END)
        entry_NumberRowSelected.delete(0,END)
    
    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select VesselSideNumber-SubTripNumber(VSN-STN) Consistency View Type', 
                            'View VSN-STN Consistency Fail With RecType-1,2',
                            'View VSN-STN Consistency Fail With RecType-1 Only']
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Consistency)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows)
            rows = rows.reset_index(drop=True)
            rows.rename(columns={0:'DataBase_ID', 1: 'RecordIdentifier', 2: 'DeploymentUID',
                                 3:'ASOCCode', 4:'ObserverNumber', 5:'DeploymentNumber', 
                                 6:'SetNumber', 7:'Year', 8:'RecordType', 9:'Country', 
                                 10:'Quota', 11:'SubTripNumber', 12:'VesselSideNumber', 
                                 13:'VesselClass', 14:'QC_Message'},inplace = True)
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
        ListVariableListA = ['Select VesselSideNumber-SubTripNumber(VSN-STN) Consistency View Type', 
                            'View VSN-STN Consistency Fail With RecType-1,2',
                            'View VSN-STN Consistency Fail With RecType-1 Only']
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
                txtDisplayMessageSystem.insert(0, 'Select VSN-STN View Type From DropDown & Run View Selected Button')
            else:
                countIndex1 = 0
                for each_rec in range(len(rows)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightblue")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                txtDisplayMessageSystem.delete(0,END)
                entry_SelQCVariable.delete(0,END)
                txtDisplayMessageSystem.insert(0, ('Populated - ' + getVarnameToView))
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 'Empty QC Fail DB. Nothing to Display')
            entry_SelQCVariable.delete(0,END)

    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        ListConsistency = ['FailCount_VesselSideNumber_Consistency',
                          'FailCount_VesselClass_Consistency',
                          'FailCount_VesselLength_Consistency',
                          'FailCount_VesselHorsepower_Consistency']
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_Vessel_FailConsis_SummaryDF;", conn)
        conn.commit()
        conn.close()
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_VSN_STN =  data[((data.VariableName) == ListConsistency[0])]
        FailedQC_VSN_STN  = FailedQC_VSN_STN.reset_index(drop=True)
        FailedQC_VSN_STN = pd.DataFrame(FailedQC_VSN_STN)
        if len(FailedQC_VSN_STN)>0:
            QCFailedTotalEntries = sum(FailedQC_VSN_STN['QCFailCount'])
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)                   
        else:
            QCFailedTotalEntries = 0     
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)
        return QCFailedTotalEntries
 
    def QCFailedExcelViewAll():
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        VSN_STN_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF;", conn)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        cursor.close()
        conn.close()

        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        VSN_STN_FailConsistency_DF['DataBase_ID'] = (VSN_STN_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        VSN_STN_FailConsistency_DF['RecordIdentifier'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        VSN_STN_FailConsistency_DF['DeploymentUID'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        VSN_STN_FailConsistency_DF['ObserverNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)
        VSN_STN_FailConsistency_DF['VesselSideNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)

        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).astype(int)

        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).astype(int)
        
        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).astype(int)

        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).astype(int)

        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).astype(int)

        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.replace(99999999, '')
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        VSN_STN_FailConsistency_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                                      'RecordType'], inplace=True)
        VSN_STN_FailConsistency_DF  = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF  = pd.DataFrame(VSN_STN_FailConsistency_DF)      
        
        if len(VSN_STN_FailConsistency_DF) >0:
            tree1.delete(*tree1.get_children())
            entry_ViewVarResults.current(0)
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 
            'Viewing QC Failed Excel File In Seperate Window')
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = VSN_STN_FailConsistency_DF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(VSN_STN_FailConsistency_DF),2), clr='lightblue', cols='all')
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
                        'ASOCCode','ObserverNumber','DeploymentNumber',
                        'SetNumber', 'Year','RecordType','Country','Quota',
                        'SubTripNumber','VesselSideNumber', 'VesselClass']]
                        ).replace(['', None, np.nan, 'None'], 99999999)
                Complete_df[['DataBase_ID','RecordIdentifier',
                            'ASOCCode','DeploymentNumber', 
                            'SetNumber', 'Year', 'RecordType','Country',
                            'Quota','VesselClass']] = Complete_df[
                            ['DataBase_ID','RecordIdentifier',
                            'ASOCCode','DeploymentNumber', 
                            'SetNumber', 'Year', 'RecordType','Country',
                            'Quota','VesselClass']].astype(int)
                Complete_df[['DeploymentUID','ObserverNumber', 
                            'SubTripNumber', 'VesselSideNumber']] = Complete_df[
                            ['DeploymentUID','ObserverNumber', 
                            'SubTripNumber', 'VesselSideNumber']].astype(str)
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
                UpdateRecordList_QCfailDB =[]
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
                    list_item_Year = (rowValue[7])
                    list_item_RecordType = (rowValue[8])
                    list_item_Country = (rowValue[9])
                    list_item_Quota = (rowValue[10])
                    list_item_SubTripNumber = (rowValue[11])
                    list_item_VesselSideNumber = (rowValue[12])
                    list_item_VesselClass = (rowValue[13])
                    list_item_QC_CaseType = 'Case: Updated'
                                
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_Year,
                                        list_item_RecordType,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_SubTripNumber,
                                        list_item_VesselSideNumber,
                                        list_item_VesselClass,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList_QCfailDB.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_Year,
                                        list_item_RecordType,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_SubTripNumber,
                                        list_item_VesselSideNumber,
                                        list_item_VesselClass,
                                        list_item_QC_CaseType,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                                             
                            ## DB Update Executing
                
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ?, \
                                        ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, Year =?,\
                                        RecordType = ? , Country = ? , Quota = ?, SubTripNumber = ?,\
                                        VesselSideNumber = ?, VesselClass =?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdateRecordList_SetCatchDB)
                            
                cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF  SET ASOCCode = ?, \
                                        ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, Year =?,\
                                        RecordType = ? , Country = ? , Quota = ?, SubTripNumber = ?,\
                                        VesselSideNumber = ?, VesselClass =?, QC_CaseType =?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdateRecordList_QCfailDB)
                                            
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
                conn_DB_SetCatch_Validation_Consistency.commit()
                conn_DB_SetCatch_Validation_Consistency.close()

            def UpdateDeploymentUIDAfterUpdate():
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
                            conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
                            cursor = conn.cursor()
                            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF ORDER BY `DataBase_ID` ASC ;", conn)
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
                    conn_DB_Set_Catch_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
                    cur_DB_Set_Catch_Consistency=conn_DB_Set_Catch_Consistency.cursor()
                    cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                        ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                        WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                        UpdateRecordList_SetCatchDB)
                    conn_DB_Set_Catch_Consistency.commit()
                    conn_DB_Set_Catch_Consistency.close()

                UpdateSetcatchDB()
                UpdateQCFailDB()

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

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def Export_FailedConsistencyVariablesCSV():
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        VSN_STN_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF;", conn)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        cursor.close()
        conn.close()

        VSN_STN_FailConsistency_DF['DataBase_ID'] = (VSN_STN_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        VSN_STN_FailConsistency_DF['RecordIdentifier'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        VSN_STN_FailConsistency_DF['DeploymentUID'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        VSN_STN_FailConsistency_DF['ObserverNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).astype(int)

        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).astype(int)

        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).astype(int)

        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).astype(int)
        
        VSN_STN_FailConsistency_DF['SubTripNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SubTripNumber']]).astype(str)
        VSN_STN_FailConsistency_DF['VesselSideNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)

        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).astype(int)

        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        Complete_df = pd.DataFrame(VSN_STN_FailConsistency_DF)
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
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        VSN_STN_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF;", conn)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        cursor.close()
        conn.close()

        GetSetCatchDB = GetSetCatchProfileDB()
        GetSetCatchDB['DataBase_ID'] = (GetSetCatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        GetSetCatchDB['RecordIdentifier'] = (GetSetCatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        
        VSN_STN_FailConsistency_DF['DataBase_ID'] = (VSN_STN_FailConsistency_DF.loc[:,['DataBase_ID']]).astype(int)
        VSN_STN_FailConsistency_DF['RecordIdentifier'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordIdentifier']]).astype(int)
        VSN_STN_FailConsistency_DF['DeploymentUID'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentUID']]).astype(str)

        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['ASOCCode'] = (VSN_STN_FailConsistency_DF.loc[:,['ASOCCode']]).astype(int)

        VSN_STN_FailConsistency_DF['ObserverNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['ObserverNumber']]).astype(str)

        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['DeploymentNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['DeploymentNumber']]).astype(int)
        
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['SetNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SetNumber']]).astype(int)

        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Year'] = (VSN_STN_FailConsistency_DF.loc[:,['Year']]).astype(int)

        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['RecordType'] = (VSN_STN_FailConsistency_DF.loc[:,['RecordType']]).astype(int)

        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Country'] = (VSN_STN_FailConsistency_DF.loc[:,['Country']]).astype(int)

        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['Quota'] = (VSN_STN_FailConsistency_DF.loc[:,['Quota']]).astype(int)
        
        VSN_STN_FailConsistency_DF['SubTripNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['SubTripNumber']]).astype(str)
        VSN_STN_FailConsistency_DF['VesselSideNumber'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselSideNumber']]).astype(str)

        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).fillna(99999999)
        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).replace([''], 99999999)
        VSN_STN_FailConsistency_DF['VesselClass'] = (VSN_STN_FailConsistency_DF.loc[:,['VesselClass']]).astype(int)

        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        
        ## merging With SetcatchDB
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.loc[:,
                        ['DataBase_ID','RecordIdentifier', 
                         'DeploymentUID']]
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        Merge_WithSetCatchDB=  GetSetCatchDB.merge(
                        VSN_STN_FailConsistency_DF, 
                        on = ['DataBase_ID','RecordIdentifier','DeploymentUID'],
                        indicator=True, 
                        how='outer').query('_merge == "both"')
        Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode','DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country',
             'Quota', 'VesselClass']]= Merge_WithSetCatchDB[
            ['DataBase_ID','RecordIdentifier', 
             'ASOCCode','DeploymentNumber','SetNumber',
             'RecordType', 'Year','Country',
             'Quota', 'VesselClass']].astype(int)
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
        entry_DepNumforSearch.delete(0,END)
        txtDisplayMessageSystem.delete(0,END)
        QcMessage = 'Run SetCatch DB Search For DepNum : '
        curItems = tree1.selection()
        if len(curItems)==1:
            sd = tree1.item(curItems, 'values')
            SelvariableIdentifier = sd[5]
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
        GetSetCatchDB_VariableList = ['SubTripNumber','VesselSideNumber', 'VesselClass']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                         UpdateRecordList1, get_entry_ViewVarResults,
                                         UpdateQCMsg_QCFailDB):
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        ListVariableSelect = ['Select VesselSideNumber-SubTripNumber(VSN-STN) Consistency View Type', 
                                'View VSN-STN Consistency Fail With RecType-1,2',
                                'View VSN-STN Consistency Fail With RecType-1 Only']
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

        conn_Validation_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cur_Validation_Consistency=conn_Validation_Consistency.cursor()
        
        if (get_entry_ViewVarResults==ListVariableSelect[1]):
            ## Updaing SetCatch DB
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SubTripNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET SubTripNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET QC_CaseType = ? \
                        WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                        SetNumber =? AND Year =? ",  
                        UpdateQCMsg_QCFailDB)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselSideNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET VesselSideNumber = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET QC_CaseType = ? \
                        WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                        SetNumber =? AND Year =? ",  
                        UpdateQCMsg_QCFailDB)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselClass = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET VesselClass = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET QC_CaseType = ? \
                        WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                        SetNumber =? AND Year =? ",  
                        UpdateQCMsg_QCFailDB)
                       
        if (get_entry_ViewVarResults==ListVariableSelect[2]):
            ## Updaing SetCatch DB
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SubTripNumber = ?\
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ", 
                    UpdateRecordList1)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET SubTripNumber = ?\
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ", 
                    UpdateRecordList1)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET QC_CaseType = ? \
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ",  
                    UpdateQCMsg_QCFailDB)

            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselSideNumber = ?\
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ", 
                    UpdateRecordList1)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET VesselSideNumber = ?\
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ", 
                    UpdateRecordList1)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET QC_CaseType = ? \
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ",  
                    UpdateQCMsg_QCFailDB)

            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselClass = ?\
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ", 
                    UpdateRecordList1)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET VesselClass = ?\
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ", 
                    UpdateRecordList1)
                cur_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET QC_CaseType = ? \
                    WHERE DeploymentUID =? AND ASOCCode =? AND DeploymentNumber =? AND \
                    SetNumber =? AND Year =? ",  
                    UpdateQCMsg_QCFailDB)
            
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_Validation_Consistency.commit()
        conn_Validation_Consistency.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18=['VesselClass']
            Var_Class_String =['SubTripNumber','VesselSideNumber']
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
            
            if get_Updated_Variable in Var_Class_String:
                if(len(get_UpdateValue_UpdatedVariable)!=0):
                    try:
                        get_UpdateValue_UpdatedVariable = str(get_UpdateValue_UpdatedVariable)
                        return get_UpdateValue_UpdatedVariable
                    except:
                        messagebox.showerror('Update Variable Datatype Error Message', "Updated Value Must Be String Value")
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
                        UpdateRecordList1 =[]
                        UpdateQCMsg_QCFailDB =[]  
                        for item in tree1.selection():
                            list_item = (tree1.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            list_item_ASOCCode = (list_item[3])
                            list_item_DeploymentNumber = (list_item[5])
                            list_item_SetNumber = (list_item[6])
                            list_item_Year = (list_item[7])
                            list_item_QC_CaseType = 'Case: Updated'
                            
                            UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DatabaseUID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                            
                            UpdateRecordList1.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DeploymentUID,
                                                    list_item_ASOCCode,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_Year))
                            
                            UpdateQCMsg_QCFailDB.append((list_item_QC_CaseType,
                                                        list_item_DeploymentUID,
                                                        list_item_ASOCCode,
                                                        list_item_DeploymentNumber,
                                                        list_item_SetNumber,
                                                        list_item_Year))
                            
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                                    UpdateRecordList1, get_entry_ViewVarResults,
                                                    UpdateQCMsg_QCFailDB)
                        viewQCFailed_VariablesProfile()
                        # GenSummaryQC()
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")
                        
                    if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                        iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                        "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                        if iUpdateSlected >0:
                            UpdateRecordList =[]
                            UpdateRecordList1 =[]
                            UpdateQCMsg_QCFailDB =[] 
                            for item in tree1.selection():
                                list_item = (tree1.item(item, 'values'))
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                list_item_ASOCCode = (list_item[3])
                                list_item_DeploymentNumber = (list_item[5])
                                list_item_SetNumber = (list_item[6])
                                list_item_Year = (list_item[7])
                                list_item_QC_CaseType = 'Case: Updated'
                                UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                        list_item_DatabaseUID,
                                                        list_item_RecordIdentifier,
                                                        list_item_DeploymentUID))
                                UpdateRecordList1.append((get_UpdateValue_UpdatedVariable, 
                                                    list_item_DeploymentUID,
                                                    list_item_ASOCCode,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_Year))
                                UpdateQCMsg_QCFailDB.append((list_item_QC_CaseType,
                                                    list_item_DeploymentUID,
                                                    list_item_ASOCCode,
                                                    list_item_DeploymentNumber,
                                                    list_item_SetNumber,
                                                    list_item_Year))
                            Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                                    UpdateRecordList1, get_entry_ViewVarResults,
                                                    UpdateQCMsg_QCFailDB)
                            viewQCFailed_VariablesProfile()
                            # GenSummaryQC()
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
        ListVariableListA = ['Select VesselSideNumber-SubTripNumber(VSN-STN) Consistency View Type', 
                        'View VSN-STN Consistency Fail With RecType-1,2',
                        'View VSN-STN Consistency Fail With RecType-1 Only']
        SelVariableView = entry_ViewVarResults.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        if len(SelVariableView)!= 0:
            tree1.delete(*tree1.get_children())
            
        if(SelVariableView ==ListVariableListA[0]):
            tree1.delete(*tree1.get_children())
            
            
        if(SelVariableView ==ListVariableListA[1]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Press Selected Results Button To View VSN-STN Consistency Fail With RecType-1,2')
            
        if(SelVariableView ==ListVariableListA[2]):
            tree1.delete(*tree1.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Press Selected Results Button To View VSN-STN Consistency Fail With RecType-1 Only')
           
    def GenSummaryQC():
        txtDepNumtoUpdateCount.delete(0,END)
        txtTripNumtoUpdateCount.delete(0,END)
        gettotalQCfailCount = QCFailedTotalEntries()
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        VSN_STN_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF;", conn)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        cursor.close()
        conn.close()
        
        if len(VSN_STN_FailConsistency_DF) >0:
            Summaryframetree.delete(*Summaryframetree.get_children())
            VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF[
                        (VSN_STN_FailConsistency_DF.RecordType) == 1]
            VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.reset_index(drop=True)
            Summary_MG_FailConsistency_DF = VSN_STN_FailConsistency_DF.groupby(
                ['ASOCCode', 'ObserverNumber','Country','Year','DeploymentNumber'],  
                    as_index=False)['SubTripNumber'].apply(lambda x: (np.count_nonzero(np.unique(x))))
            Summary_MG_FailConsistency_DF = pd.DataFrame(Summary_MG_FailConsistency_DF)
            Count_DepNumToUpdate = len(Summary_MG_FailConsistency_DF)
            countIndex1 = 0
            for each_rec in range(len(Summary_MG_FailConsistency_DF)):
                if countIndex1 % 2 == 0:
                    Summaryframetree.insert("", tk.END, values=list(Summary_MG_FailConsistency_DF.loc[each_rec]), tags =("even",))
                else:
                    Summaryframetree.insert("", tk.END, values=list(Summary_MG_FailConsistency_DF.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            Summaryframetree.tag_configure("even",foreground="black", background="lightgreen")
            Summaryframetree.tag_configure("odd",foreground="black", background="ghost white")
            txtDepNumtoUpdateCount.insert(tk.END,Count_DepNumToUpdate)
            txtTripNumtoUpdateCount.insert(tk.END,gettotalQCfailCount)
        else:
            Count_DepNumToUpdate = 0
            txtDepNumtoUpdateCount.insert(tk.END,Count_DepNumToUpdate)
            txtTripNumtoUpdateCount.insert(tk.END,gettotalQCfailCount)
              
    def InventoryRec3(event):
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        VSN_STN_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF;", conn)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF[
                        (VSN_STN_FailConsistency_DF.RecordType) == 1]
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        cursor.close()
        conn.close()
        ## Summary frame Table B Selection
        nm =Summaryframetree.selection()
        if len(nm) ==1:
            sd = Summaryframetree.item(nm, 'values')
            SelvariableASOC = sd[0]
            SelvariableObsN= sd[1]
            SelvariableCountry = sd[2]
            SelvariableYr = sd[3]
            SelvariableIdentifier = sd[4]
            entry_DepNumforSearch.delete(0,END)
            entry_DepNumforSearch.insert(tk.END,SelvariableIdentifier)
            try:
                SelvariableIdentifier = int(SelvariableIdentifier)
                SelvariableASOC = int(SelvariableASOC)
                SelvariableCountry = int(SelvariableCountry)
                SelvariableYr = int(SelvariableYr)
            except:
                messagebox.showerror('DepNum Variable Datatype Error Message', "DepNum Must Be Integer Value")
            checkinttype1 = isinstance(SelvariableIdentifier,int)
            checkinttype2 = isinstance(SelvariableASOC,int)
            checkinttype3 = isinstance(SelvariableCountry,int)
            checkinttype4 = isinstance(SelvariableYr,int)
            if  (checkinttype1 == True)& (checkinttype2 == True)&\
                (checkinttype3 == True)&(checkinttype4 == True):  
                NumberEntriesInSet = sd[5]
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(tk.END,((" Selected Deployment Number : ") +
                                                    str(SelvariableIdentifier) + ' ' +' & '+
                                                    "# Of SubTripN Fail Fail: " + 
                                                    str(NumberEntriesInSet)))
                if (int(NumberEntriesInSet) > 0):
                    tree1.delete(*tree1.get_children())
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                    entry_SelQCVariable.delete(0,END)
                    VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF[
                        ((VSN_STN_FailConsistency_DF.DeploymentNumber) == SelvariableIdentifier)&
                        ((VSN_STN_FailConsistency_DF.ASOCCode) == SelvariableASOC)&
                        ((VSN_STN_FailConsistency_DF.ObserverNumber) == SelvariableObsN)&
                        ((VSN_STN_FailConsistency_DF.Country) == SelvariableCountry)&
                        ((VSN_STN_FailConsistency_DF.Year) == SelvariableYr)
                        ]
                    VSN_STN_FailConsistency_DF  = VSN_STN_FailConsistency_DF.reset_index(drop=True)
                    VSN_STN_FailConsistency_DF  = pd.DataFrame(VSN_STN_FailConsistency_DF)
                    countIndex1 = 0
                    for each_rec in range(len(VSN_STN_FailConsistency_DF)):
                        if countIndex1 % 2 == 0:
                            tree1.insert("", tk.END, values=list(VSN_STN_FailConsistency_DF.loc[each_rec]), tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=list(VSN_STN_FailConsistency_DF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    tree1.tag_configure("even",foreground="black", background="lightgreen")
                    tree1.tag_configure("odd",foreground="black", background="ghost white")
                    entry_SelQCVariable.insert(tk.END,"C. QC View")
                    entry_GenSummarySetcatchDB.delete(0,END)
                    GenSummaryString = (str(SelvariableASOC) + '-' +\
                                       str(SelvariableObsN) + '-' +\
                                       str(SelvariableCountry) + '-' +\
                                       str(SelvariableYr) + '-' +\
                                       str(SelvariableIdentifier))
                    entry_GenSummarySetcatchDB.insert(tk.END,GenSummaryString)
                    entry_ViewVarResults.current(2) 
                else:
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(tk.END,"Empty QC Fail - No Fail Found")
                    tree1.delete(*tree1.get_children())
                    SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                    entry_ViewVarResults.current(0)        
        else:
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, (' Please Select Only One Entry To View'))
                   
    def SearchDepNumFromSetCatchDB():
        ListFilterBy = ['Both RecType 1&2', 
                        'RecType-1 Only']
        get_TabAQCview = (entry_FilterByList.get())
        get_DepNumforSearch = (entry_DepNumforSearch.get())
        
        if (len(get_DepNumforSearch)) > 0:
            try:
                get_DepNumforSearch = int(get_DepNumforSearch)
            except:
                messagebox.showerror('Search Variable Datatype Error Message', "Search Value Must Be Integer Value")
            
            checkinttype = isinstance(get_DepNumforSearch,int)
            if checkinttype == True:  
                conn_DB= sqlite3.connect(DB_Set_Catch_Analysis)
                if (get_DepNumforSearch) >= 0:
                    if (get_TabAQCview == ListFilterBy[0]):               
                        get_SearchSingleVariable_Value = (get_DepNumforSearch)
                        rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                        rows= (rows.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota',
                            'SubTripNumber','VesselSideNumber', 'VesselClass']])
                        rows = rows[(rows.DeploymentNumber) == get_SearchSingleVariable_Value]
                        rows  = rows.reset_index(drop=True)
                        VSN_STN_FailConsistency_DF  = pd.DataFrame(rows)
                        ExcelViewEditBackend_RecType_1_2(VSN_STN_FailConsistency_DF)
                    
                    if (get_TabAQCview == ListFilterBy[1]):               
                        get_SearchSingleVariable_Value = (get_DepNumforSearch)
                        rows=pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn_DB)
                        rows= (rows.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota',
                            'SubTripNumber','VesselSideNumber', 'VesselClass']])
                        rows = rows[((rows.DeploymentNumber) == get_SearchSingleVariable_Value)&\
                                    ((rows.RecordType) == 1)]
                        rows  = rows.reset_index(drop=True)
                        VSN_STN_FailConsistency_DF  = pd.DataFrame(rows)
                        ExcelViewEditBackend_RecType_1(VSN_STN_FailConsistency_DF)
                conn_DB.commit()
                conn_DB.close()     

    def ExcelViewEditBackend_RecType_1_2(VSN_STN_FailConsistency_DF):
        if len(VSN_STN_FailConsistency_DF) >0:
            VSN_STN_FailConsistency_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                                      'RecordType'], inplace=True)
            VSN_STN_FailConsistency_DF  = VSN_STN_FailConsistency_DF.reset_index(drop=True)
            VSN_STN_FailConsistency_DF  = pd.DataFrame(VSN_STN_FailConsistency_DF)   
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 
            'Viewing Searched QC Failed Excel File In Seperate Window')
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = VSN_STN_FailConsistency_DF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(VSN_STN_FailConsistency_DF),2), clr='lightblue', cols='all')
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
                        'ASOCCode','ObserverNumber','DeploymentNumber',
                        'SetNumber', 'Year','RecordType','Country','Quota',
                        'SubTripNumber','VesselSideNumber', 'VesselClass']]
                        ).replace(['', None, np.nan, 'None'], 99999999)
                Complete_df[['DataBase_ID','RecordIdentifier',
                            'ASOCCode','DeploymentNumber', 
                            'SetNumber', 'Year', 'RecordType','Country',
                            'Quota','VesselClass']] = Complete_df[
                            ['DataBase_ID','RecordIdentifier',
                            'ASOCCode','DeploymentNumber', 
                            'SetNumber', 'Year', 'RecordType','Country',
                            'Quota','VesselClass']].astype(int)
                Complete_df[['DeploymentUID','ObserverNumber', 
                            'SubTripNumber', 'VesselSideNumber']] = Complete_df[
                            ['DeploymentUID','ObserverNumber', 
                            'SubTripNumber', 'VesselSideNumber']].astype(str)
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
                conn_DB_SetCatch_Validation_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
                cur_DB_SetCatch_Validation_Consistency=conn_DB_SetCatch_Validation_Consistency.cursor()
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList_QCfailDB =[]
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
                    list_item_Year = (rowValue[7])
                    list_item_RecordType = (rowValue[8])
                    list_item_Country = (rowValue[9])
                    list_item_Quota = (rowValue[10])
                    list_item_SubTripNumber = (rowValue[11])
                    list_item_VesselSideNumber = (rowValue[12])
                    list_item_VesselClass = (rowValue[13])
                    list_item_QC_CaseType = 'Case: Updated'         
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_Year,
                                        list_item_RecordType,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_SubTripNumber,
                                        list_item_VesselSideNumber,
                                        list_item_VesselClass,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList_QCfailDB.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_Year,
                                        list_item_RecordType,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_SubTripNumber,
                                        list_item_VesselSideNumber,
                                        list_item_VesselClass,
                                        list_item_QC_CaseType,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                                             
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ?, \
                                        ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, Year =?,\
                                        RecordType = ? , Country = ? , Quota = ?, SubTripNumber = ?,\
                                        VesselSideNumber = ?, VesselClass =?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdateRecordList_SetCatchDB)
                            
                cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF  SET ASOCCode = ?, \
                                        ObserverNumber = ?, DeploymentNumber = ?, SetNumber = ?, Year =?,\
                                        RecordType = ? , Country = ? , Quota = ?, SubTripNumber = ?,\
                                        VesselSideNumber = ?, VesselClass =?, QC_CaseType =?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdateRecordList_QCfailDB)
                                            
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
                                                bg= "cadet blue", text="NB : Do Not Edit Columns : DataBase_ID, RecordIdentifier, DeplymentUID")
            lbl_CautionSteps.grid(row =10, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_CautionSteps_1 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="NB : Edit/Modify Year/ASOC/DepN/SetN Columns Requires Edit DeplymentUID Accordingly")
            lbl_CautionSteps_1.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_CautionSteps_2 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                bg= "cadet blue", text="NB : Do Not Delete Any Row And Submit")
            lbl_CautionSteps_2.grid(row =12, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            windows.mainloop() 

    def ExcelViewEditBackend_RecType_1(VSN_STN_FailConsistency_DF):
        if len(VSN_STN_FailConsistency_DF) >0:
            VSN_STN_FailConsistency_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                                      'RecordType'], inplace=True)
            VSN_STN_FailConsistency_DF  = VSN_STN_FailConsistency_DF.reset_index(drop=True)
            VSN_STN_FailConsistency_DF  = pd.DataFrame(VSN_STN_FailConsistency_DF)   
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 
            'Viewing Searched QC Failed Excel File In Seperate Window')
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = VSN_STN_FailConsistency_DF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(VSN_STN_FailConsistency_DF),2), clr='lightblue', cols='all')
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
                        'ASOCCode','ObserverNumber','DeploymentNumber',
                        'SetNumber', 'Year','RecordType','Country','Quota',
                        'SubTripNumber','VesselSideNumber', 'VesselClass']]
                        ).replace(['', None, np.nan, 'None'], 99999999)
                Complete_df[['DataBase_ID','RecordIdentifier',
                            'ASOCCode','DeploymentNumber', 
                            'SetNumber', 'Year', 'RecordType','Country',
                            'Quota','VesselClass']] = Complete_df[
                            ['DataBase_ID','RecordIdentifier',
                            'ASOCCode','DeploymentNumber', 
                            'SetNumber', 'Year', 'RecordType','Country',
                            'Quota','VesselClass']].astype(int)
                Complete_df[['DeploymentUID','ObserverNumber', 
                            'SubTripNumber', 'VesselSideNumber']] = Complete_df[
                            ['DeploymentUID','ObserverNumber', 
                            'SubTripNumber', 'VesselSideNumber']].astype(str)
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
                conn_DB_SetCatch_Validation_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
                cur_DB_SetCatch_Validation_Consistency=conn_DB_SetCatch_Validation_Consistency.cursor()
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList_QCfailDB =[]
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
                    list_item_Year = (rowValue[7])
                    list_item_RecordType = (rowValue[8])
                    list_item_Country = (rowValue[9])
                    list_item_Quota = (rowValue[10])
                    list_item_SubTripNumber = (rowValue[11])
                    list_item_VesselSideNumber = (rowValue[12])
                    list_item_VesselClass = (rowValue[13])
                    list_item_QC_CaseType = 'Case: Updated'         
                    
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_Year,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_SubTripNumber,
                                        list_item_VesselSideNumber,
                                        list_item_VesselClass,
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList_QCfailDB.append((
                                        list_item_ASOCCode,
                                        list_item_ObserverNumber,
                                        list_item_DeploymentNumber,
                                        list_item_SetNumber,
                                        list_item_Year,
                                        list_item_Country,
                                        list_item_Quota,
                                        list_item_SubTripNumber,
                                        list_item_VesselSideNumber,
                                        list_item_VesselClass,
                                        list_item_QC_CaseType,
                                        list_item_DeploymentUID))
                                    
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                                        ASOCCode =?, ObserverNumber = ?, DeploymentNumber =?, SetNumber =?,\
                                        Year =?, Country =?, Quota = ?, SubTripNumber = ? ,\
                                        VesselSideNumber = ? , VesselClass = ?\
                                        WHERE  DeploymentUID =?", 
                                        UpdateRecordList_SetCatchDB)
                
                cur_DB_SetCatch_Validation_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET \
                                        ASOCCode =?, ObserverNumber = ?, DeploymentNumber =?, SetNumber =?,\
                                        Year =?, Country =?, Quota = ?, SubTripNumber = ? ,\
                                        VesselSideNumber = ? , VesselClass = ?, QC_CaseType =?\
                                        WHERE DeploymentUID = ?", 
                                        UpdateRecordList_QCfailDB)
                                            
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

            lbl_CautionSteps_2 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                bg= "cadet blue", text="NB : Do Not Delete Any Row And Submit")
            lbl_CautionSteps_2.grid(row =12, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)
            windows.mainloop() 

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
                    conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
                    cursor = conn.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF ORDER BY `DataBase_ID` ASC ;", conn)
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
            conn_DB_Set_Catch_Consistency= sqlite3.connect(DB_SetCatch_Validation_Consistency)
            cur_DB_Set_Catch_Consistency=conn_DB_Set_Catch_Consistency.cursor()
            cur_DB_Set_Catch_Consistency.executemany("UPDATE SetCatch_VSN_STN_FailConsistency_DF SET DeploymentUID =?, Year = ?, \
                                                ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                UpdateRecordList_SetCatchDB)
            conn_DB_Set_Catch_Consistency.commit()
            conn_DB_Set_Catch_Consistency.close()

        UpdateSetcatchDB()
        UpdateQCFailDB()
        tree1.delete(*tree1.get_children())
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    def GenSetCatchDBSummary():
        get_StringToSearch = entry_GenSummarySetcatchDB.get()
        if (len(get_StringToSearch)) > 0:
            conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
            cursor = conn.cursor()
            GetSetCatchProfileDF = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF;", conn)
            cursor.close()
            conn.close()
            
            GetSetCatchProfileDF= (GetSetCatchProfileDF.loc[:,
                    ['DataBase_ID','RecordIdentifier','DeploymentUID',
                    'ASOCCode','ObserverNumber','DeploymentNumber',
                    'SetNumber', 'Year','RecordType','Country','Quota',
                    'SubTripNumber','VesselSideNumber', 'VesselClass']])
            
            GetSetCatchProfileDF[
                ['DataBase_ID','RecordIdentifier','ASOCCode','Country', 
                 'Year','DeploymentNumber', 'SetNumber', 'RecordType',
                 'Quota','VesselClass']] = GetSetCatchProfileDF[
                ['DataBase_ID','RecordIdentifier','ASOCCode','Country', 
                 'Year','DeploymentNumber', 'SetNumber', 'RecordType',
                 'Quota','VesselClass']].astype(int)
            
            GetSetCatchProfileDF[
                ['DeploymentUID','ObserverNumber', 'SubTripNumber',
                 'VesselSideNumber']] = GetSetCatchProfileDF[
                ['DeploymentUID','ObserverNumber', 'SubTripNumber',
                 'VesselSideNumber']].astype(str)
            
            GetSetCatchProfileDF  = GetSetCatchProfileDF.reset_index(drop=True)
            GetSetCatchProfileDF  = pd.DataFrame(GetSetCatchProfileDF)

            get_DepUIDToSearch_Split = get_StringToSearch.split("-")
            get_Search_ASOC =get_DepUIDToSearch_Split[0]
            get_Search_ObsN =get_DepUIDToSearch_Split[1]
            get_Search_CounTry =get_DepUIDToSearch_Split[2]
            get_Search_Year =get_DepUIDToSearch_Split[3]
            get_Search_DepN =get_DepUIDToSearch_Split[4]
            try:
                get_Search_ASOC = int(get_Search_ASOC)
                get_Search_ObsN = str(get_Search_ObsN)
                get_Search_CounTry = int(get_Search_CounTry)
                get_Search_Year = int(get_Search_Year)
                get_Search_DepN = int(get_Search_DepN)
            except:
                messagebox.showerror('Search Variable Datatype Error Message', "Values Must Be Integer Value")
            
            checkinttype_ASOC = isinstance(get_Search_ASOC,int)
            checkinttype_Cntry = isinstance(get_Search_CounTry,int)
            checkinttype_Year = isinstance(get_Search_Year,int)
            checkinttype_DepN = isinstance(get_Search_DepN,int)
            
            if (checkinttype_ASOC == True) & (checkinttype_Cntry == True)&\
                (checkinttype_DepN == True) & (checkinttype_Year == True):
                GetSetCatchProfileDF = GetSetCatchProfileDF[
                                ((GetSetCatchProfileDF.ASOCCode) == get_Search_ASOC)&
                                ((GetSetCatchProfileDF.ObserverNumber) == get_Search_ObsN)&
                                ((GetSetCatchProfileDF.Country) == get_Search_CounTry)&
                                ((GetSetCatchProfileDF.Year) == get_Search_Year)&
                                ((GetSetCatchProfileDF.DeploymentNumber) == get_Search_DepN)
                                ]
                GetSetCatchProfileDF  = GetSetCatchProfileDF.reset_index(drop=True)
                GetSetCatchProfileDF  = pd.DataFrame(GetSetCatchProfileDF)

                GetSetCatchProfileDF['SubTripIdentifier'] = GetSetCatchProfileDF["Year"].map(str) + "-" + \
                                                        GetSetCatchProfileDF["ASOCCode"].map(str)+ "-" +\
                                                        GetSetCatchProfileDF["DeploymentNumber"].map(str)+"-"+ \
                                                        GetSetCatchProfileDF["SubTripNumber"].map(str)
                
                GetSetCatchProfileDF = GetSetCatchProfileDF.groupby(
                    ['SubTripIdentifier','VesselClass','VesselSideNumber'],  
                    as_index=False).agg(
                    {"SetNumber": lambda x: x.nunique(),
                     "DataBase_ID": lambda x: x.nunique()})
                GetSetCatchProfileDF  = GetSetCatchProfileDF.reset_index(drop=True)               
                GetSetCatchProfileDF = pd.DataFrame(GetSetCatchProfileDF)
                SelResultOverviewtree.delete(*SelResultOverviewtree.get_children())
                countIndex1 = 0
                for each_rec in range(len(GetSetCatchProfileDF)):
                    if countIndex1 % 2 == 0:
                        SelResultOverviewtree.insert("", tk.END, values=list(GetSetCatchProfileDF.loc[each_rec]), tags =("even",))
                    else:
                        SelResultOverviewtree.insert("", tk.END, values=list(GetSetCatchProfileDF.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                SelResultOverviewtree.tag_configure("even",foreground="black", background="lightyellow")
                SelResultOverviewtree.tag_configure("odd",foreground="black", background="ghost white")
        else:
             messagebox.showerror('Search Format Error', "Please Use Search Convention As : ASOC-Obs#-Country-Year-Dep#") 
    
    def InventoryRec4(event):
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        cursor = conn.cursor()
        VSN_STN_FailConsistency_DF = pd.read_sql_query("SELECT * FROM SetCatch_VSN_STN_FailConsistency_DF;", conn)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        VSN_STN_FailConsistency_DF[
                ['DataBase_ID','RecordIdentifier','ASOCCode','Country', 
                 'Year','DeploymentNumber', 'SetNumber', 'RecordType',
                 'Quota','VesselClass']] = VSN_STN_FailConsistency_DF[
                ['DataBase_ID','RecordIdentifier','ASOCCode','Country', 
                 'Year','DeploymentNumber', 'SetNumber', 'RecordType',
                 'Quota','VesselClass']].astype(int)
            
        VSN_STN_FailConsistency_DF[
                ['DeploymentUID','ObserverNumber', 'SubTripNumber',
                 'VesselSideNumber']] = VSN_STN_FailConsistency_DF[
                ['DeploymentUID','ObserverNumber', 'SubTripNumber',
                 'VesselSideNumber']].astype(str)
            
        VSN_STN_FailConsistency_DF  = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF  = pd.DataFrame(VSN_STN_FailConsistency_DF)
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF[
                        (VSN_STN_FailConsistency_DF.RecordType) == 1]
        VSN_STN_FailConsistency_DF['SubTripIdentifier'] = VSN_STN_FailConsistency_DF["Year"].map(str) + "-" + \
                                                        VSN_STN_FailConsistency_DF["ASOCCode"].map(str)+ "-" +\
                                                        VSN_STN_FailConsistency_DF["DeploymentNumber"].map(str)+"-"+ \
                                                        VSN_STN_FailConsistency_DF["SubTripNumber"].map(str)
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
        cursor.close()
        conn.close()

        nm =SelResultOverviewtree.selection()
        if len(nm) ==1:
            sd = SelResultOverviewtree.item(nm, 'values')
            SubtripUID = sd[0]
            Vessclass  = sd[1]
            VessSideN  = sd[2]
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(tk.END,((" Selected SubTripNumberUID Number : ") +
                                                str(SubtripUID)))
            if (len(Vessclass)) > 0:
                try:
                    get_Vessclass = int(Vessclass)
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "Search Value Must Be Integer Value")
                checkinttype = isinstance(get_Vessclass,int)
                if checkinttype == True: 
                    VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF[
                                ((VSN_STN_FailConsistency_DF.SubTripIdentifier) == SubtripUID)&\
                                ((VSN_STN_FailConsistency_DF.VesselSideNumber) == VessSideN)&\
                                ((VSN_STN_FailConsistency_DF.VesselClass) == get_Vessclass)]
                    VSN_STN_FailConsistency_DF  = VSN_STN_FailConsistency_DF.reset_index(drop=True)
                    VSN_STN_FailConsistency_DF  = pd.DataFrame(VSN_STN_FailConsistency_DF)
                    
                    if (len(VSN_STN_FailConsistency_DF) > 0):
                        tree1.delete(*tree1.get_children())
                        countIndex1 = 0
                        for each_rec in range(len(VSN_STN_FailConsistency_DF)):
                            if countIndex1 % 2 == 0:
                                tree1.insert("", tk.END, values=list(VSN_STN_FailConsistency_DF.loc[each_rec]), tags =("even",))
                            else:
                                tree1.insert("", tk.END, values=list(VSN_STN_FailConsistency_DF.loc[each_rec]), tags =("odd",))
                            countIndex1 = countIndex1+1
                        tree1.tag_configure("even",foreground="black", background="#F0F8FF")
                        tree1.tag_configure("odd",foreground="black", background="#FAEBD7")
                    else:
                        txtDisplayMessageSystem.delete(0,END)
                        txtDisplayMessageSystem.insert(tk.END,((" Empty SubTripNumberUID Selected Return Null Results")))

    # Tree 1 & Summaryframetree View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    Summaryframetree.bind('<<TreeviewSelect>>',InventoryRec3)
    SelResultOverviewtree.bind('<<TreeviewSelect>>',InventoryRec4)
    
    ## ComboBox Select
    entry_UpdateVariableList.bind('<<ComboboxSelected>>', callbackFuncSelectVariable1)
    entry_ViewVarResults.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    ##Gen QC Summary
    GenSummaryQC()
    QCFailedTotalEntries()

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
    button_UpdateSelectedDBEntries.grid(row =14, column = 0, padx=10, pady =1, ipady =4, sticky =W)

    button_Clear_EntriesUpdate = Button(UpdateDB_Entryframe, bd = 2, text ="Clear Entries", width = 10,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ClearEntries)
    button_Clear_EntriesUpdate.grid(row =6, column = 0, padx=15, pady =2, ipady =1, sticky =E)

    ##Buttons On Generate QC Failed Summary Frame
    button_GenSummaryQC = Button(Summaryframe, bd = 1, text ="Generate QC Summary ", width = 20,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSummaryQC)
    button_GenSummaryQC.pack(side =TOP)

    button_GenDBSummary = Button(SelQCVariableDisplay, bd = 1, text ="Gen Set & Catch Summary", width = 26,
                                height=1, font=('aerial', 9, 'bold'), fg="blue", bg="cadet blue", 
                                command =GenSetCatchDBSummary)
    button_GenDBSummary.grid(row =0, column = 0, padx=150, pady =2, ipady =2, sticky =W)

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
