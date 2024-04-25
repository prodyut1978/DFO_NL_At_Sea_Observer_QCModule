from tkinter import *
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
import numpy as np
import sqlite3
import pandas as pd
from pandastable import Table, config
import sys
import functools

## SetCatch DB Connections
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")

def TreeViewDB_QCAnalysis_SetCatch():
    root=tk.Tk()
    root.title ("View DFO-NL-ASOP View Observer Set & Catch QC Database - B-01")
    root.geometry('1520x810+40+40')
    root.config(bg="cadet blue")
    Topframe = tk.Frame(root, bd = 2, padx= 3, pady= 2, relief = RIDGE)
    Topframe.pack(side = TOP)
    TotalEntriesDB = IntVar(root, value='')
    lbl_Total_DBEntries = Label(Topframe, font=('aerial', 12, 'bold'), bg= "aliceblue", text=" Set & Catch Log Table:")
    lbl_Total_DBEntries.grid(row =0, column = 0, padx=1, pady =2)
    entry_Total_DBEntries = Entry(Topframe, font=('aerial', 10, 'bold'), justify='center',
                                                textvariable = TotalEntriesDB, width = 8, bd=2)
    entry_Total_DBEntries.grid(row =0, column = 1, padx=10, pady =2, ipady=2)
    lbl_SearchTotalEntries = Label(Topframe, font=('aerial', 10, 'bold'), bg= "aliceblue", text="Search Result Entries :")
    lbl_SearchTotalEntries.grid(row =0, column = 7, padx=2, pady =2)
    TotalSearchDB_Results = IntVar(root, value='')
    SearchDB_Results = Entry(Topframe, font=('aerial', 10, 'bold'), justify='center',
                                                textvariable = TotalSearchDB_Results, width = 8, bd=2)
    SearchDB_Results.grid(row =0, column = 8, padx=2, pady =2, ipady=2)
    Tableframe = Frame(root, width = 40)
    Tableframe.pack(side = TOP, padx= 0, pady=0)
    tree = ttk.Treeview(Tableframe, height=22)
    scrollbary = ttk.Scrollbar(Tableframe, orient ="vertical", command=tree.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(Tableframe, orient ="horizontal", command=tree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree.configure(xscrollcommand = scrollbarx.set)
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 8), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), background='Ghost White', 
                    foreground='blue',fieldbackground='Ghost White')
    def get_ObserverSetCatchDB():
        try:
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", sqliteConnection)
            length_Complete_df = len(Complete_df)
            if length_Complete_df > 0:
                try:
                    Complete_df.sort_values(by=['Year', 'ASOCCode', 
                    'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
                    Complete_df = Complete_df.reset_index(drop=True)
                    ObserverSetCatchDB = pd.DataFrame(Complete_df)
                    sqliteConnection.commit()
                    return ObserverSetCatchDB, length_Complete_df
                except:
                    messagebox.showerror('Set & Catch Database DataType Error', "Cannot Sort Database On DeploymentUID")
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
    Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
    if Return_ObserverSetCatchDB !=None:
        Length_ObserverSetCatchDB = Return_ObserverSetCatchDB[1]
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        List_Columns = list(ObserverSetCatchDB.columns)
        tree['column'] = List_Columns
        tree['show'] = "headings"
        for col in tree['column']:
            if (col == 'DataBase_ID')|(col == 'RecordIdentifier'):
                tree.heading(col, text=col, anchor = tk.CENTER)
                tree.column(col, stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
            else:
                tree.heading(col, text=col, anchor = tk.CENTER)
                tree.column(col, stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
        df_rows = ObserverSetCatchDB.to_numpy().tolist()
        countIndex = 0
        for row in df_rows:
            if countIndex % 2 == 0:
                tree.insert("", "end", values =row, tags =("even",))
            else:
                tree.insert("", "end", values =row, tags =("odd",))
            countIndex = countIndex+1
        tree.tag_configure("even",foreground="black", background="lightblue")
        tree.tag_configure("odd",foreground="black", background="ghost white")
        entry_Total_DBEntries.delete(0,END)
        entry_Total_DBEntries.insert(tk.END,Length_ObserverSetCatchDB)
        Treepopup = Menu(tree, tearoff=0)

    ## Frame Of update modules
    ## Row 2
    UpdateDB_Entryframe = tk.Frame(root, bd = 2,relief = RIDGE, bg= "cadet blue")
    UpdateDB_Entryframe.pack(side =LEFT, padx=1, pady =2)

    lbl_UpdateDB_Header = Label(UpdateDB_Entryframe, font=('aerial', 12, 'bold','underline'),
                                bg= "cadet blue", text="Update Set & Catch Database :")
    lbl_UpdateDB_Header.grid(row =2, column = 0, columnspan=2 ,padx=1, pady =2, sticky =W)
    
    ## Row 4
    lbl_UpdateDB_A_IntergerVariable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Entries & Choose Update Method :")
    lbl_UpdateDB_A_IntergerVariable.grid(row =4, column = 0, padx=2, pady =1, sticky =W)

    UpdateMethod = ['Update Method : By Set', 
                    'Update Method : By Entry']
    ChooseMethodBy        = StringVar(UpdateDB_Entryframe, value ='')
    entry_ChooseMethodBy  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), justify = tk.LEFT,
                                        textvariable =ChooseMethodBy, width = 24, state='readonly')
    entry_ChooseMethodBy.grid(row =5, column = 0 ,padx=10, pady =1, ipady= 2, sticky =W)
    entry_ChooseMethodBy['values'] = UpdateMethod
    entry_ChooseMethodBy.current(0)

    lbl_NumberRowSelected = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text="Total Selected \n (Max 20,000)")
    lbl_NumberRowSelected.grid(row =4, column = 1, padx=20, pady =1, sticky =E)

    ## Row 6
    lbl_Select_List_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 2. Select Variable From Drop Down List :")
    lbl_Select_List_Variable.grid(row =6, column = 0, padx=2, pady =4, sticky =W)
    NumberRowSelected       = IntVar(UpdateDB_Entryframe, value ='')
    entry_NumberRowSelected = Entry(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = NumberRowSelected, width = 12, bd=2)
    entry_NumberRowSelected.grid(row =6, column = 1, padx=20, pady =1, ipady =4, sticky =E)

    ## Row 8
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
    VariableListA        = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = VariableListA, width = 35, state='readonly')
    entry_UpdateVariableList.grid(row =8, column = 0, padx=10, pady =2, ipady= 4, sticky =W)
    entry_UpdateVariableList['values'] = (list(ListVariableListA))

    ## Row 10 
    lbl_EntryUpdate_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 3. Enter Corresponding Updated Value :")
    lbl_EntryUpdate_Variable.grid(row =10, column = 0, padx=2, pady =2, sticky =W)

    lbl_EntryDataType_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text="Variable Data Type")
    lbl_EntryDataType_Variable.grid(row =10, column = 1, padx=45, pady =2, sticky =W)

    ## Row 12
    UpdateValue_VariableA       = IntVar(UpdateDB_Entryframe, value ='')
    entry_UpdateValue_VariableA = Entry(UpdateDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = UpdateValue_VariableA, width = 36, bd=2)
    entry_UpdateValue_VariableA.grid(row =12, column = 0, padx=10, pady =2, ipady =4, sticky =W)

    EntryDataType_Variable       = StringVar(UpdateDB_Entryframe, value ='')
    entry_EntryDataType_Variable = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), 
                                        textvariable = EntryDataType_Variable, width = 25, bd=2)
    entry_EntryDataType_Variable.grid(row =12, column = 1, padx=35, pady =2, ipady =4, sticky =W)

    ## ######## Frame Of search modules ##########
    SearchDB_Entryframe = tk.Frame(root, bd = 2,relief = RIDGE, bg= "cadet blue")
    SearchDB_Entryframe.pack(side =LEFT, padx=20, pady =2)

    lbl_DBDisplayMessage = Label(SearchDB_Entryframe, font=('aerial', 13, 'bold'), 
                                bg= "cadet blue", text="System Message Display :")
    lbl_DBDisplayMessage.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)
    EntryDisplayMessageQC       = StringVar(SearchDB_Entryframe, value ='**** Set & Catch Database Operation QC Message Display ****')
    entry_EntryDisplayMessageQC = Entry(SearchDB_Entryframe, font=('aerial', 8, 'bold'), 
                                        textvariable = EntryDisplayMessageQC, width = 70, bd=2)
    entry_EntryDisplayMessageQC.grid(row =0, column = 1, padx=2, pady =2, ipady =4, sticky =W)

    ## Row 2
    lbl_SearchDB_Header = Label(SearchDB_Entryframe, font=('aerial', 13, 'bold','underline'), 
                                bg= "cadet blue", text="Search Set & Catch QC Database:")
    lbl_SearchDB_Header.grid(row =2, column = 0, columnspan=2 ,padx=2, pady =2, sticky =W)

    ######## A. Single Variable Query ########
    ## Row 4
    lbl_SinglevariableSearch_A = Label(SearchDB_Entryframe, font=('aerial', 12, 'bold'),
                                            bg= "cadet blue", text=" A. Single Variable Query :")
    lbl_SinglevariableSearch_A.grid(row =4, column = 0, padx=2, pady =1, sticky =W)

    ## Row 6
    lbl_SelectSinglevariableSearch_A = Label(SearchDB_Entryframe, font=('aerial', 10, 'bold'),
                                            bg= "cadet blue", text=" 1. Select Variable From Drop Down List :")
    lbl_SelectSinglevariableSearch_A.grid(row =6, column = 0, padx=5, pady =1, sticky =W)

    ## Row 8
    ListVariableSearch = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber','SetNumber', 
                        'DeploymentUID', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                        'VesselClass', 'PositionPrecision','NAFODivision','UnitArea', 'GearType', 
                        'CodendMeshSize','MeshSizeMG', 'MeshSizeFG','DataSource', 'DirectedSpecies',
                        'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1','LogbookIDNumber2','SpeciesCode',
                        'GearDamage', 'SubTripNumber','Month','InOut200MileLimit','StatisticalArea',
                        'Day', 'HaulDay', 'HaulMonth','StartTime', 'Duration',
                        'RollerBobbbinDiameter', 'NumberGillnets','AverageGillnetLength','GrateBarSpacing','NumberPots',
                        'NumberPotReleasedCrab','AverageTowSpeed','AverageDepth','NumberWindows','NumberHooks']
    VariableListSearch        = StringVar(SearchDB_Entryframe, value ='')
    entry_SearchVariableList  = ttk.Combobox(SearchDB_Entryframe, font=('aerial', 10, 'bold'), 
                                            textvariable = VariableListSearch, width = 25, state='readonly')
    entry_SearchVariableList.grid(row =8, column = 0, padx=30, pady =1, ipady= 4, sticky =W)
    entry_SearchVariableList['values'] = sorted(list(ListVariableSearch))

    ## Row 10 
    lbl_EntrySearch_Variable = Label(SearchDB_Entryframe, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" 2. Enter Corresponding Search Query :")
    lbl_EntrySearch_Variable.grid(row =10, column = 0, padx=5, pady =2, sticky =W)

    ## Row 12
    SearchValue_Variable_A       = StringVar(SearchDB_Entryframe, value ='')
    entry_SearchValue_Variable_A = ttk.Combobox(SearchDB_Entryframe, font=('aerial', 10, 'bold'), 
                                            textvariable = SearchValue_Variable_A, width = 25)
    entry_SearchValue_Variable_A.grid(row =12, column = 0, padx=30, pady =2, ipady =4, sticky =W)

    ###### B. Multi Variable Search Query (AND/OR) ######
    ## Row 4
    lbl_MultivariableSearch_B = Label(SearchDB_Entryframe, font=('aerial', 12, 'bold'),
                                            bg= "cadet blue", text=" B. Multi Variable Search Query (AND/OR) :")
    lbl_MultivariableSearch_B.grid(row =4, column = 1, padx=30, pady =1, sticky =W)

    ####### C. Textual Search For Alphanumeric Variables #######
    ## Row 10 
    lbl_TextualSearch_C = Label(SearchDB_Entryframe, font=('aerial', 12, 'bold'),
                                            bg= "cadet blue", text=" C. Textual Search For Alphanumeric Variables :")
    lbl_TextualSearch_C.grid(row =10, column = 1, padx=30, pady =1, sticky =W)
    ## Row 12 
    SearchValue_Variable_C       = StringVar(SearchDB_Entryframe, value ='')
    entry_SearchValue_Variable_C = Entry(SearchDB_Entryframe, font=('aerial', 10, 'bold'), 
                                        textvariable = SearchValue_Variable_C, width = 28, bd=2)
    entry_SearchValue_Variable_C.grid(row =12, column = 1, padx=80, pady =2, ipady =4, sticky =W)

    ## ######## Frame Of Copy N Add Entries ##########
    MiscCommandframe = tk.Frame(root, bd = 2,relief = RIDGE, bg= "cadet blue")
    MiscCommandframe.pack(side =LEFT, padx=2, pady =2)

    lbl_Misc_Header = Label(MiscCommandframe, font=('aerial', 11, 'bold','underline'),
                                bg= "cadet blue", text="Misc Operations :")
    lbl_Misc_Header.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =1, sticky =W)

    lbl_CopynAdd_Header = Label(MiscCommandframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text=" A. Select Copy-Edit & Add Entries : \n (Select Any Row )")
    lbl_CopynAdd_Header.grid(row =2, column = 0, columnspan=1 ,padx=5, pady =1, sticky =W)

    lbl_Del_Header = Label(MiscCommandframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text=" B. Select & Delete Entries :")
    lbl_Del_Header.grid(row =6, column = 0, columnspan=1 ,padx=5, pady =2, sticky =W)

    lbl_UpdateTreeViewDB_Header = Label(MiscCommandframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text=" C. Apply Table Edited Entries To DB: \n (DoubleClick Cell For Edit)")
    lbl_UpdateTreeViewDB_Header.grid(row =10, column = 0, columnspan=1 ,padx=5, pady =2, sticky =W)

    ## Define functions
    def iExit():
        tkinter.messagebox.showinfo("Observer Set & Catch QC Database Viewer", "You Must Exit From Set & Catch QC Database Viewer")
        sys.exit() 
        # root.destroy()
        return

    def RootExit():
        iExit= tkinter.messagebox.askyesno("Observer Set & Catch QC Database Viewer", "You Want To Exit From Set & Catch QC Database Viewer ?")
        if iExit >0:
            root.destroy()
            return

    def InventoryRec(event):
        curItems = tree.selection()
        len_curItems = len(curItems)
        if len_curItems < 20001:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,len_curItems)
            if len_curItems == 1:
                for nm in tree.selection():
                    sd = tree.item(nm, 'values')
                    entry_EntryDisplayMessageQC.delete(0,END)
                    entry_EntryDisplayMessageQC.insert(tk.END,('Selected DeploymentUID : ' + sd[2]))
        else:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,'MaxLimit Exceed')

    def InventoryRec1(event):
        curItems = tree.selection()
        len_curItems = len(curItems)
        curItem = tree.focus()
        selcurItem = (tree.item(curItem))
        selcurItemValues = (selcurItem.get("values"))
        GetSetCatchDB_VariableList = [
                            'DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
        if len(selcurItemValues) == len(GetSetCatchDB_VariableList):
            if len_curItems == 1:
                region_clicked = tree.identify_region(event.x, event.y)
                if region_clicked in ("cell", "heading"):
                    item_id = tree.identify("item", event.x, event.y)
                    column_id = tree.identify("column", event.x, event.y)
                    CellData = tree.set(item_id, column_id)
                    IndexValueCol = int(column_id[1:])-1
                    if IndexValueCol > 2:
                        VarName = GetSetCatchDB_VariableList[IndexValueCol]
                        entry_UpdateValue_VariableA.delete(0,END)
                        entry_UpdateValue_VariableA.insert(tk.END,CellData)
                        entry_UpdateVariableList.delete(0,END)
                        entry_UpdateVariableList.current(IndexValueCol-3)

    def View_All_DB_SetCatchEntries():
        button_UpdateCellValueDB.config(state="normal")
        ClearView_DBEntries()
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                Complete_df.sort_values(by=['Year', 'ASOCCode', 
                    'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                List_Columns = list(SetCatchProfileDB_DF.columns)
                tree['column'] = List_Columns
                tree['show'] = "headings"
                for col in tree['column']:
                    if (col == 'DataBase_ID')|(col == 'RecordIdentifier'):
                        tree.heading(col, text=col, anchor = tk.CENTER)
                        tree.column(col, stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
                    else:
                        tree.heading(col, text=col, anchor = tk.CENTER)
                        tree.column(col, stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
                df_rows = SetCatchProfileDB_DF.to_numpy().tolist()
                countIndex = 0
                for row in df_rows:
                    if countIndex % 2 == 0:
                        tree.insert("", "end", values =row, tags =("even",))
                    else:
                        tree.insert("", "end", values =row, tags =("odd",))
                    countIndex = countIndex+1
                tree.tag_configure("even",foreground="black", background="lightblue")
                tree.tag_configure("odd",foreground="black", background="ghost white")
                Length_ObserverSetCatchDB = len(SetCatchProfileDB_DF)
                entry_Total_DBEntries.delete(0,END)
                entry_Total_DBEntries.insert(tk.END,Length_ObserverSetCatchDB)
            else:
                messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', 
                                    "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def View_All_DB_AfterUpdate(get_Updated_Method):
        UpdateMethod = ['Update Method : By Set', 
                        'Update Method : By Entry']
        if get_Updated_Method == UpdateMethod[0]:
            button_UpdateCellValueDB.config(state="normal")
            ClearView_DBEntries()
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF[(SetCatchProfileDB_DF.RecordType) == 1]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    List_Columns = list(SetCatchProfileDB_DF.columns)
                    tree['column'] = List_Columns
                    tree['show'] = "headings"
                    for col in tree['column']:
                        if (col == 'DataBase_ID')|(col == 'RecordIdentifier'):
                            tree.heading(col, text=col, anchor = tk.CENTER)
                            tree.column(col, stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
                        else:
                            tree.heading(col, text=col, anchor = tk.CENTER)
                            tree.column(col, stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
                    df_rows = SetCatchProfileDB_DF.to_numpy().tolist()
                    countIndex = 0
                    for row in df_rows:
                        if countIndex % 2 == 0:
                            tree.insert("", "end", values =row, tags =("even",))
                        else:
                            tree.insert("", "end", values =row, tags =("odd",))
                        countIndex = countIndex+1
                    tree.tag_configure("even",foreground="black", background="lightblue")
                    tree.tag_configure("odd",foreground="black", background="ghost white")
                    Length_ObserverSetCatchDB = len(SetCatchProfileDB_DF)
                    entry_Total_DBEntries.delete(0,END)
                    entry_Total_DBEntries.insert(tk.END,Length_ObserverSetCatchDB)
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', 
                                        "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        if get_Updated_Method == UpdateMethod[1]:
            View_All_DB_SetCatchEntries()

    def TreeView_DataFrame():
        dfList =[] 
        for child in tree.get_children():
            df = tree.item(child)["values"]
            dfList.append(df)
        ListBox_DF = pd.DataFrame(dfList)
        Len_ListBox_DF = len (ListBox_DF)
        return ListBox_DF, Len_ListBox_DF

    def ClearView_DBEntries():
        tree.delete(*tree.get_children())
        entry_Total_DBEntries.delete(0,END)
        entry_NumberRowSelected.delete(0,END)

    def Clear_EntriesUpdate():
        entry_UpdateValue_VariableA.delete(0,END)
        entry_UpdateVariableList.delete(0,END)
        entry_NumberRowSelected.delete(0,END)
        entry_UpdateVariableList.delete(0,END)
        entry_EntryDataType_Variable.delete(0,END)
        entry_UpdateVariableList.current(56)

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

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                         UpdateSetList, get_Updated_Method):
        UpdateMethod = ['Update Method : By Set', 
                        'Update Method : By Entry']
        
        SetNoUpdateList = ['SpeciesCode', 'KeptWeight', 'DiscardWeight', 
                        'EstimatedWeightReleasedCrab', 'NumberIndividuals']

        if get_Updated_Method == UpdateMethod[1]:
            GetSetCatchDB_VariableList = SetcatchDB_VariableList()
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
            
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
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselLength = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))

            if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselHorsepower = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        (UpdateRecordList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Day = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Month = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulDay = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulMonth = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartTime = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Duration = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NAFODivision = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET UnitArea = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StatisticalArea = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET InOut200MileLimit = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET CodendMeshSize = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[30]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeMG = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[31]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeFG = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[32]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RollerBobbbinDiameter = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[33]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberGillnets = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[34]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageGillnetLength = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[35]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GrateBarSpacing = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[36]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET FootropeLength = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[37]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberWindows = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[38]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberHooks = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[39]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPots = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[40]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPotReleasedCrab = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[41]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearDamage = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[42]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[43]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageDepth = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[44]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DataSource = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[45]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DirectedSpecies = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[46]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberSpecies = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[47]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[48]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DetailedCatchSpeciesCompCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[49]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET LogbookIDNumber1 = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[50]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET LogbookIDNumber2 = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[51]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SpeciesCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[52]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET KeptWeight = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[53]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DiscardWeight = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[54]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EstimatedWeightReleasedCrab = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[55]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberIndividuals = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                        UpdateRecordList)
                
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

        if get_Updated_Method == UpdateMethod[0]:
            if get_Updated_Variable not in SetNoUpdateList:
                GetSetCatchDB_VariableList = SetcatchDB_VariableList()
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
                "Set Update For Last five Variable From Table Not Allowed, Please Update By Entry Selection")
                
    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
        # Performing QC On Variables Value And DataType
        Var_Class_IntA18=['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                        'ASOCCode', 'Year', 'DeploymentNumber', 
                        'SetNumber', 'Country', 'Quota', 'SetType',
                        'VesselClass','Day', 'Month','PositionPrecision',
                        'GearType','RecordType','DirectedSpecies','DataSource']
        
        Var_Class_FloatA7= ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                            'EndLongitude','AverageTowSpeed', 'VesselLength']
        
        Var_Class_String7 =['ObserverNumber', 'DeploymentUID', 'StatisticalArea', 
                            'SubTripNumber','NAFODivision', 'VesselSideNumber',
                            'UnitArea','DetailedCatchSpeciesCompCode']
        
        Var_Class_IntB27  = ['VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                            'InOut200MileLimit',  'CodendMeshSize',
                            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                            'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                            'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                            'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                            'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                            'NumberIndividuals']

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
        UpdateMethod = ['Update Method : By Set', 
                        'Update Method : By Entry']
        DefaultUpdateMethod = UpdateMethod[1]
        ReturnFail ="ReturnFail"
        DepUIDUpdateList = ['ASOCCode', 'Year', 'DeploymentNumber', 'SetNumber']
        get_Updated_Method = entry_ChooseMethodBy.get()
        get_Updated_Variable = entry_UpdateVariableList.get()
        get_UpdateValue_UpdatedVariable = entry_UpdateValue_VariableA.get()
        get_UpdateValue_UpdatedVariable = QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable)
        if (get_UpdateValue_UpdatedVariable != ReturnFail) & (len(get_Updated_Variable)!=0):
            entry_EntryDisplayMessageQC.delete(0,END)
            entry_EntryDisplayMessageQC.insert(tk.END,"Please Wait Updating Selected Entries")
            ListBox_DF = tree.selection()
            
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
                    UpdateSetList =[]
                    for item in tree.selection():
                        list_item = (tree.item(item, 'values'))
                        list_item_DatabaseUID = int(list_item[0])
                        list_item_RecordIdentifier = int(list_item[1])
                        list_item_DeploymentUID = (list_item[2])
                        UpdateRecordList.append((get_UpdateValue_UpdatedVariable, list_item_DatabaseUID,
                                                 list_item_RecordIdentifier,list_item_DeploymentUID))
                        UpdateSetList.append((get_UpdateValue_UpdatedVariable, list_item_DeploymentUID))
                    Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, UpdateSetList,get_Updated_Method)
                    entry_EntryDisplayMessageQC.delete(0,END)
                    entry_EntryDisplayMessageQC.insert(tk.END,"Set & Catch Database Updated Successfully")
                    if get_Updated_Variable in DepUIDUpdateList:
                        UpdateDeploymentUIDAfterUpdate()
                        View_All_DB_AfterUpdate(DefaultUpdateMethod)
                    else:
                        View_All_DB_AfterUpdate(DefaultUpdateMethod)
                    tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")
                    
                if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                    iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                                                                "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                    if iUpdateSlected >0:
                        UpdateRecordList =[]
                        UpdateSetList =[] 
                        for item in tree.selection():
                            list_item = (tree.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            UpdateRecordList.append((get_UpdateValue_UpdatedVariable, list_item_DatabaseUID,
                                                 list_item_RecordIdentifier,list_item_DeploymentUID))
                            UpdateSetList.append((get_UpdateValue_UpdatedVariable, list_item_DeploymentUID))
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, UpdateSetList,get_Updated_Method)
                        if get_Updated_Variable in DepUIDUpdateList:
                            UpdateDeploymentUIDAfterUpdate()
                            View_All_DB_AfterUpdate(get_Updated_Method)
                        else:
                            View_All_DB_AfterUpdate(get_Updated_Method)
                        tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")    
            
            ## Empty Selection Case
            if (len(ListBox_DF)<=0)|((ListBox_DF) ==[])|((ListBox_DF) ==()):
                tkinter.messagebox.showinfo("Update Error","Empty Set & Catch Table Selection Please Select At least One Entries In the Table To Update The Variable")
            
            ## Max Limit Update Exceed Case Limiting Because Of Slow Performance 
            if (len(ListBox_DF)>20000):
                tkinter.messagebox.showinfo("Update Selection Max Case","Max Limit For Update Selection Is 20,000 \
                                            Please Select A Batch Of 20,000 Entries Each Time If You Need To Update More")  
        else:
            messagebox.showerror('Update Error',
                                "Please Check Variable DataType And Follow Proper Update Step") 

    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def callbackFuncSelectVariable1(event):
        VariableListA = entry_UpdateVariableList.get()
        print('Selected Update Variable Name :'+ VariableListA)
        if len(VariableListA)!= 0:
            entry_UpdateValue_VariableA.delete(0,END)
        if(VariableListA=='ObserverNumber')|\
        (VariableListA=='SubTripNumber')|\
        (VariableListA=='VesselSideNumber')|\
        (VariableListA=='NAFODivision')|\
        (VariableListA=='StatisticalArea')|\
        (VariableListA=='DetailedCatchSpeciesCompCode')|\
        (VariableListA=='UnitArea'):
            EntryDataType_Variable = 'Alpha Numeric DataType'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)
        
        elif(VariableListA=='Duration')|\
        (VariableListA=='StartLatitude')|\
        (VariableListA=='StartLongitude')|\
        (VariableListA=='EndLatitude')|\
        (VariableListA=='EndLongitude')|\
        (VariableListA=='AverageTowSpeed')|\
        (VariableListA=='VesselLength'):
            EntryDataType_Variable = 'Float DataType'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)
        
        else:
            EntryDataType_Variable = 'Numeric DataType Only'
            entry_EntryDataType_Variable.delete(0,END)
            entry_EntryDataType_Variable.insert(tk.END,EntryDataType_Variable)

    def RunSelCols_SetAndCatchDB():
        win = tk.Tk()
        win.title ("Column Selection View")
        win.geometry("250x300")
        ListBoxDisplay = Listbox(win,selectmode="multiple", font=('aerial', 8, 'bold'),
                                height =6, width =20)
        GetSetCatchDB_VariableList = [
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

        for i in GetSetCatchDB_VariableList:
            ListBoxDisplay.insert(END,i)
        Clear_EntriesUpdate()
        s = Scrollbar()
        scrollbar = ttk.Scrollbar(win, orient= 'vertical')
        scrollbar.pack(side= RIGHT, fill= BOTH)
        ListBoxDisplay.config(yscrollcommand= scrollbar.set)
        scrollbar.config(command= ListBoxDisplay.yview)
        ListBoxDisplay.pack(expand=YES,fill="both")
        def RunSeletView():
            SelectedColumns =[]
            for i in ListBoxDisplay.curselection():
                sel = (ListBoxDisplay.get(i))
                SelectedColumns.append(sel)
            viewSelCols_SetAndCatchDB(SelectedColumns)
            button_UpdateCellValueDB.config(state="disabled")
            win.destroy()
        
        btn_SubmitSelection = Button(win, bd = 2, width = 15,
                    height=1, font=('aerial', 10, 'bold'), 
                    fg="blue", bg="cadet blue", 
                    text='Submit Selection', command=RunSeletView)
        btn_SubmitSelection.pack(side='bottom')
        win.mainloop()
        
    def viewSelCols_SetAndCatchDB(SelectedColumns):
        GetSetCatchDB_Columns = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
        BaseColumns =['DataBase_ID', 'RecordIdentifier','DeploymentUID']
        TreeViewSelectedCols = list(BaseColumns + list((SelectedColumns)))
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        rows=cur.fetchall()
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows.columns = GetSetCatchDB_Columns
        cur.close()
        con.close()
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows = rows.loc[:,TreeViewSelectedCols]
        rows = rows.reset_index(drop=True)
        rows = pd.DataFrame(rows)
        List_Columns = list(rows.columns)
        tree['column'] = List_Columns
        tree['show'] = "headings"
        tree.delete(*tree.get_children())
        for col in tree['column']:
            if (col == 'DataBase_ID')|(col == 'RecordIdentifier'):
                tree.heading(col, text=col, anchor = tk.CENTER)
                tree.column(col, stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
            else:
                tree.heading(col, text=col, anchor = tk.CENTER)
                tree.column(col, stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
        df_rows = rows.to_numpy().tolist()
        countIndex = 0
        for row in df_rows:
            if countIndex % 2 == 0:
                tree.insert("", "end", values =row, tags =("even",))
            else:
                tree.insert("", "end", values =row, tags =("odd",))
            countIndex = countIndex+1
        tree.tag_configure("even",foreground="black", background="lightblue")
        tree.tag_configure("odd",foreground="black", background="ghost white")
        return rows

    def SetAndCatchDBTotalEntries():
        entry_Total_DBEntries.delete(0,END)
        conn = sqlite3.connect(DB_Set_Catch_Analysis)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        TotalEntries = len(data)       
        entry_Total_DBEntries.insert(tk.END,TotalEntries)              
        conn.commit()
        conn.close()

    def DeleteSelectedEntries():
        SelectionTree = tree.selection()
        if len(SelectionTree)>0:
            iDelete = tkinter.messagebox.askyesno("Delete Entry From DFO-NL-ASOP Set & Catch QC Database", 
                            "Confirm If You Want To Delete The Selection Entries From DFO-NL-ASOP Set & Catch QC Database")
            if iDelete >0:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cur = conn.cursor()
                for selected_item in tree.selection():
                    cur.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID = ? ",(tree.set(selected_item, '#1'), tree.set(selected_item, '#2'),tree.set(selected_item, '#3'),))
                    conn.commit()
                    tree.delete(selected_item)
                conn.commit()
                conn.close()
                tree.delete(*tree.get_children())
                View_All_DB_SetCatchEntries()
                return
        else:
            tkinter.messagebox.showinfo("Delete Error","Please Select Entries From SetCatch Table To Delete From Database")

    def DeleteSelectedSet():
        SelectionTree = tree.selection()
        if len(SelectionTree)>0:
            iDelete = tkinter.messagebox.askyesno("Delete Set From DFO-NL-ASOP Set & Catch QC Database", 
                            "Confirm If You Want To Delete The Selection Set From DFO-NL-ASOP Set & Catch QC Database")
            if iDelete >0:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cur = conn.cursor()
                for selected_item in tree.selection():
                    cur.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DeploymentUID =? AND ASOCCode =? AND Year = ? ",(tree.set(selected_item, '#3'), tree.set(selected_item, '#4'),tree.set(selected_item, '#6'),))
                    conn.commit()
                    tree.delete(selected_item)
                conn.commit()
                conn.close()
                tree.delete(*tree.get_children())
                View_All_DB_SetCatchEntries()
                return
        else:
            tkinter.messagebox.showinfo("Delete Error","Please Select Entries From SetCatch Table To Delete From Database")

    def Combo_input_ASOCCode():
            con= sqlite3.connect(DB_Set_Catch_Analysis)
            cur=con.cursor()
            cur.execute("SELECT ASOCCode FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
            data = []
            for row in cur.fetchall():
                data.append(row[0])
            con.close()
            return data

    def Combo_input_ObserverNumber():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT ObserverNumber FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Year():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT Year FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Day():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT Day FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentNumber():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT DeploymentNumber FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SetNumber():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT SetNumber FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DeploymentUID():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT DeploymentUID FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Country():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT Country FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Quota():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT Quota FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SetType():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT SetType FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SubTripNumber():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT SubTripNumber FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_VesselSideNumber():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT VesselSideNumber FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_VesselClass():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT VesselClass FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_PositionPrecision():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT PositionPrecision FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NAFODivision():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT NAFODivision FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_UnitArea():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT UnitArea FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_GearType():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT GearType FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_CodendMeshSize():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT CodendMeshSize FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_MeshSizeMG():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT MeshSizeMG FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_MeshSizeFG():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT MeshSizeFG FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DataSource():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT DataSource FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DirectedSpecies():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT DirectedSpecies FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_RecordType():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT RecordType FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_DetailedCatchSpeciesCompCode():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT DetailedCatchSpeciesCompCode FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_LogbookIDNumber1():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT LogbookIDNumber1 FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_LogbookIDNumber2():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT LogbookIDNumber2 FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_SpeciesCode():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT SpeciesCode FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `SpeciesCode` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_GearDamage():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT GearDamage FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `GearDamage` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_StatisticalArea():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT StatisticalArea FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `StatisticalArea` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Month():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT Month FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `Month` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_InOut200MileLimit():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT InOut200MileLimit FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `InOut200MileLimit` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_HaulDay():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT HaulDay FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `HaulDay` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_HaulMonth():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT HaulMonth FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `HaulMonth` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_StartTime():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT StartTime FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `StartTime` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_Duration():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT Duration FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `Duration` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_RollerBobbbinDiameter():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT RollerBobbbinDiameter FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `RollerBobbbinDiameter` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberGillnets():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT NumberGillnets FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `NumberGillnets` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_AverageGillnetLength():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT AverageGillnetLength FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `AverageGillnetLength` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_GrateBarSpacing():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT GrateBarSpacing FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `GrateBarSpacing` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data
    
    def Combo_input_NumberPots():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT NumberPots FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `NumberPots` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberPotReleasedCrab():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT NumberPotReleasedCrab FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `NumberPotReleasedCrab` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_AverageTowSpeed():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT AverageTowSpeed FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `AverageTowSpeed` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_AverageDepth():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT AverageDepth FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `AverageDepth` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Combo_input_NumberWindows():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT NumberWindows FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `NumberWindows` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data
    
    def Combo_input_NumberHooks():
        con= sqlite3.connect(DB_Set_Catch_Analysis)
        cur=con.cursor()
        cur.execute("SELECT NumberHooks FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `NumberHooks` ASC ;")
        data = []
        for row in cur.fetchall():
            data.append(row[0])
        con.close()
        return data

    def Clear_EntriesSearch():
        SearchDB_Results.delete(0,END)
        entry_SearchVariableList.delete(0,END)
        entry_SearchValue_Variable_A.delete(0,END)
        entry_SearchValue_Variable_C.delete(0,END)

    def callbackFuncSelectVariable2(event):
        VariableListA = entry_SearchVariableList.get()
        print('Selected Search Variable Name :'+ VariableListA)
        if len(VariableListA)!= 0:
            entry_SearchValue_Variable_A.delete(0,END)
        if VariableListA == 'ASOCCode':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_ASOCCode())))])
        if VariableListA == 'ObserverNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else None for i in list(set((Combo_input_ObserverNumber())))])
        if VariableListA == 'Year':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_Year())))])
        if VariableListA == 'DeploymentNumber':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_DeploymentNumber())))])
        if VariableListA == 'SetNumber':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_SetNumber())))])
        
        if VariableListA == 'DeploymentUID':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else None for i in list(set((Combo_input_DeploymentUID())))])
        if VariableListA == 'Country':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_Country())))])
        if VariableListA == 'Quota':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_Quota())))])
        if VariableListA == 'SetType':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_SetType())))])
        if VariableListA == 'VesselSideNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_VesselSideNumber())))])
        
        if VariableListA == 'VesselClass':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_VesselClass())))])
        if VariableListA == 'PositionPrecision':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_PositionPrecision())))])
        if VariableListA == 'NAFODivision':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_NAFODivision())))]) 
        if VariableListA == 'UnitArea':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_UnitArea())))])
        if VariableListA == 'GearType':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_GearType())))])

        if VariableListA == 'CodendMeshSize':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_CodendMeshSize())))])
        if VariableListA == 'MeshSizeMG':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_MeshSizeMG())))])
        if VariableListA == 'MeshSizeFG':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_MeshSizeFG())))])
        if VariableListA == 'DataSource':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_DataSource())))])
        if VariableListA == 'DirectedSpecies':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_DirectedSpecies())))])
        
        if VariableListA == 'RecordType':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_RecordType())))])
        if VariableListA == 'DetailedCatchSpeciesCompCode':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_DetailedCatchSpeciesCompCode())))])
        if VariableListA == 'LogbookIDNumber1':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_LogbookIDNumber1())))])
        if VariableListA == 'LogbookIDNumber2':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_LogbookIDNumber2())))])
        if VariableListA == 'SpeciesCode':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_SpeciesCode())))])
        
        if VariableListA == 'GearDamage':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_GearDamage())))])
        if VariableListA == 'SubTripNumber':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_SubTripNumber())))])
        if VariableListA == 'Month':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_Month())))])
        if VariableListA == 'InOut200MileLimit':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_InOut200MileLimit())))])
        if VariableListA == 'StatisticalArea':
            entry_SearchValue_Variable_A['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_StatisticalArea())))])

        if VariableListA == 'Day':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_Day())))])
        if VariableListA == 'HaulDay':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_HaulDay())))])
        if VariableListA == 'HaulMonth':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_HaulMonth())))])
        if VariableListA == 'StartTime':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_StartTime())))])
        if VariableListA == 'Duration':
            entry_SearchValue_Variable_A['values'] = sorted([float(i) if i else np.nan for i in list(set((Combo_input_Duration())))])

        if VariableListA == 'RollerBobbbinDiameter':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_RollerBobbbinDiameter())))])
        if VariableListA == 'NumberGillnets':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberGillnets())))])
        if VariableListA == 'AverageGillnetLength':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_AverageGillnetLength())))])
        if VariableListA == 'GrateBarSpacing':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_GrateBarSpacing())))])
        if VariableListA == 'NumberPots':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberPots())))])

        if VariableListA == 'NumberPotReleasedCrab':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberPotReleasedCrab())))])
        if VariableListA == 'AverageTowSpeed':
            entry_SearchValue_Variable_A['values'] = sorted([float(i) if i else np.nan for i in list(set((Combo_input_AverageTowSpeed())))])
        if VariableListA == 'AverageDepth':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_AverageDepth())))])
        if VariableListA == 'NumberWindows':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberWindows())))])
        if VariableListA == 'NumberHooks':
            entry_SearchValue_Variable_A['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_NumberHooks())))])

    def SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value):
        ListVariableSearch = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber','SetNumber', 
                            'DeploymentUID', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                            'VesselClass', 'PositionPrecision','NAFODivision','UnitArea', 'GearType', 
                            'CodendMeshSize','MeshSizeMG', 'MeshSizeFG','DataSource', 'DirectedSpecies',
                            'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1','LogbookIDNumber2','SpeciesCode',
                            'GearDamage', 'SubTripNumber','Month','InOut200MileLimit','StatisticalArea',
                            'Day', 'HaulDay', 'HaulMonth','StartTime', 'Duration',
                            'RollerBobbbinDiameter', 'NumberGillnets','AverageGillnetLength','GrateBarSpacing','NumberPots',
                            'NumberPotReleasedCrab','AverageTowSpeed','AverageDepth','NumberWindows','NumberHooks']
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        if get_SearchSingleVariable == ListVariableSearch[0]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE ASOCCode = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "ASOC Code Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE ASOCCode = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[1]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE ObserverNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur_DB_Set_Catch_Analysis.fetchall()
            return rows
        
        if get_SearchSingleVariable == ListVariableSearch[2]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Year = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "Year Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Year = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[3]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DeploymentNumber = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "DeploymentNumber Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DeploymentNumber = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows   
        
        if get_SearchSingleVariable == ListVariableSearch[4]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE SetNumber = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "SetNumber Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE SetNumber = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[5]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DeploymentUID = ?", (get_SearchSingleVariable_Value,))
            rows=cur_DB_Set_Catch_Analysis.fetchall()
            return rows
        
        if get_SearchSingleVariable == ListVariableSearch[6]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Country = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "Country Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Country = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[7]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Quota = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "Quota Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Quota = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows   
        
        if get_SearchSingleVariable == ListVariableSearch[8]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE SetType = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "SetType Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE SetType = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows 
        
        if get_SearchSingleVariable == ListVariableSearch[9]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE VesselSideNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur_DB_Set_Catch_Analysis.fetchall()
            return rows
        
        if get_SearchSingleVariable == ListVariableSearch[10]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE VesselClass = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "VesselClass Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE VesselClass = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows  
        
        if get_SearchSingleVariable == ListVariableSearch[11]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE PositionPrecision = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "PositionPrecision Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE PositionPrecision = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
            
        if get_SearchSingleVariable == ListVariableSearch[12]:
            try:
                get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NAFODivision = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
            except:
                messagebox.showerror('Search Variable Datatype Error Message', "NAFODivision Must Be AlphaNumeric Value")
        
        if get_SearchSingleVariable == ListVariableSearch[13]:
            try:
                get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE UnitArea = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
            except:
                messagebox.showerror('Search Variable Datatype Error Message', "UnitArea Must Be AlphaNumeric Value")   
        
        if get_SearchSingleVariable == ListVariableSearch[14]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE GearType = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "GearType Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE GearType = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows 
        
        if get_SearchSingleVariable == ListVariableSearch[15]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE CodendMeshSize = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "CodendMeshSize Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE CodendMeshSize = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[16]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE MeshSizeMG = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "MeshSizeMG Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE MeshSizeMG = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows   
        
        if get_SearchSingleVariable == ListVariableSearch[17]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE MeshSizeFG = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "MeshSizeFG Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE MeshSizeFG = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows   
        
        if get_SearchSingleVariable == ListVariableSearch[18]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DataSource = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "DataSource Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DataSource = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[19]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DirectedSpecies = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "DirectedSpecies Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DirectedSpecies = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows 
        
        if get_SearchSingleVariable == ListVariableSearch[20]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE RecordType = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "RecordType Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE RecordType = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[21]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DetailedCatchSpeciesCompCode = ?", (get_SearchSingleVariable_Value,))
            rows=cur_DB_Set_Catch_Analysis.fetchall()
            return rows
        
        if get_SearchSingleVariable == ListVariableSearch[22]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE LogbookIDNumber1 = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "LogbookIDNumber1 Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE LogbookIDNumber1 = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
        
        if get_SearchSingleVariable == ListVariableSearch[23]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE LogbookIDNumber2 = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "LogbookIDNumber2 Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE LogbookIDNumber2 = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
            
        if get_SearchSingleVariable == ListVariableSearch[24]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE SpeciesCode = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "SpeciesCode Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE SpeciesCode = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[25]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE GearDamage = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "GearDamage Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE GearDamage = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[26]:
            get_SearchSingleVariable_Value = (get_SearchSingleVariable_Value)
            cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE SubTripNumber = ?", (get_SearchSingleVariable_Value,))
            rows=cur_DB_Set_Catch_Analysis.fetchall()
            return rows

        if get_SearchSingleVariable == ListVariableSearch[27]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Month = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "Month Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Month = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[28]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE InOut200MileLimit = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "InOut200MileLimit Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE InOut200MileLimit = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[29]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE StatisticalArea = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "StatisticalArea Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE StatisticalArea = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[30]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Day = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "Day Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Day = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[31]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE HaulDay = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "HaulDay Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE HaulDay = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[32]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE HaulMonth = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "HaulMonth Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE HaulMonth = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[33]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE StartTime = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "StartTime Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE StartTime = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[34]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = float(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Duration = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "Duration Must Be Float Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE Duration = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[35]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE RollerBobbbinDiameter = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "RollerBobbbinDiameter Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE RollerBobbbinDiameter = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[36]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberGillnets = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "NumberGillnets Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberGillnets = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[37]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE AverageGillnetLength = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "AverageGillnetLength Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE AverageGillnetLength = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[38]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE GrateBarSpacing = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "GrateBarSpacing Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE GrateBarSpacing = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[39]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberPots = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "NumberPots Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberPots = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[40]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberPotReleasedCrab = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "NumberPotReleasedCrab Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberPotReleasedCrab = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[41]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = float(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE AverageTowSpeed = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "AverageTowSpeed Must Be Float Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE AverageTowSpeed = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[42]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE AverageDepth = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "AverageDepth Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE AverageDepth = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[43]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberWindows = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "NumberWindows Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberWindows = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        if get_SearchSingleVariable == ListVariableSearch[44]:
            if(get_SearchSingleVariable_Value!='NaN'):
                try:
                    get_SearchSingleVariable_Value = int(get_SearchSingleVariable_Value)
                    cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberHooks = ?", (get_SearchSingleVariable_Value,))
                    rows=cur_DB_Set_Catch_Analysis.fetchall()
                    return rows
                except:
                    messagebox.showerror('Search Variable Datatype Error Message', "NumberHooks Must Be Numeric Value")
            else:
                get_SearchSingleVariable_Value = ''
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE NumberHooks = ?", (get_SearchSingleVariable_Value,))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows

        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()

    def RunSingleVariableSearchQuery():
        def Submit_To_Set_Catch_SingleSearchTempStorage(SingleSearchRowsDF):
            try:
                TempImport_To_DBStorage = pd.DataFrame(SingleSearchRowsDF)
                sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = sqliteConnection.cursor()
                TempImport_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_SingleSearchTempStorage', sqliteConnection, if_exists="replace",index = False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        get_SearchSingleVariable        = entry_SearchVariableList.get()
        get_SearchSingleVariable_Value  = entry_SearchValue_Variable_A.get()
        if(len(get_SearchSingleVariable)!=0) & (len(get_SearchSingleVariable_Value)!=0):    
            tree.delete(*tree.get_children())
            rows = SearchSingleVariableQuery_Backend(get_SearchSingleVariable, get_SearchSingleVariable_Value)
            rows = pd.DataFrame(rows)
            rows.reset_index(drop=True)
            SingleSearchRowsDF = pd.DataFrame(rows)
            SingleSearchRowsDF.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 2:'DeploymentUID',
                                        3:'ASOCCode', 4:'ObserverNumber', 5:'Year', 6:'DeploymentNumber', 7:'SubTripNumber', 
                                        8:'SetNumber', 9:'Country', 10:'Quota', 11:'SetType', 12:'VesselSideNumber', 
                                        13:'VesselClass', 14:'VesselLength', 15:'VesselHorsepower', 16:'Day', 17:'Month', 
                                        18:'HaulDay', 19:'HaulMonth', 20:'StartTime', 21:'Duration', 22:'PositionPrecision',
                                        23:'StartLatitude', 24:'StartLongitude', 25:'EndLatitude', 26:'EndLongitude', 27:'NAFODivision', 
                                        28:'UnitArea', 29:'StatisticalArea', 30:'InOut200MileLimit', 31:'GearType', 32:'CodendMeshSize', 
                                        33:'MeshSizeMG', 34:'MeshSizeFG', 35:'RollerBobbbinDiameter', 36:'NumberGillnets', 37:'AverageGillnetLength', 
                                        38:'GrateBarSpacing', 39:'FootropeLength', 40:'NumberWindows', 41:'NumberHooks', 42:'NumberPots', 
                                        43:'NumberPotReleasedCrab', 44:'GearDamage', 45:'AverageTowSpeed', 46:'AverageDepth', 47:'DataSource', 
                                        48:'DirectedSpecies', 49:'NumberSpecies', 50:'RecordType', 51:'DetailedCatchSpeciesCompCode', 52:'LogbookIDNumber1', 
                                        53:'LogbookIDNumber2', 54:'SpeciesCode', 55:'KeptWeight', 56:'DiscardWeight', 57:'EstimatedWeightReleasedCrab',
                                        58:'NumberIndividuals'},inplace = True)
            SingleSearchRowsDF.reset_index(drop=True)
            SingleSearchRowsDF = pd.DataFrame(SingleSearchRowsDF)
            if (len(SingleSearchRowsDF))>0:
                Submit_To_Set_Catch_SingleSearchTempStorage(SingleSearchRowsDF)
                cur_Columns = list(tree['columns'])
                SingleSearchRowsDF = SingleSearchRowsDF.loc[:,cur_Columns]
                SingleSearchRowsDF  = SingleSearchRowsDF.reset_index(drop=True)
                SingleSearchRowsDF  = pd.DataFrame(SingleSearchRowsDF)
                if rows is not None:
                    countIndex1 = 0
                    for each_rec in range(len(SingleSearchRowsDF)):
                        if countIndex1 % 2 == 0:
                            tree.insert("", tk.END, values=list(SingleSearchRowsDF.loc[each_rec]), tags =("even",))
                        else:
                            tree.insert("", tk.END, values=list(SingleSearchRowsDF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    tree.tag_configure("even2",foreground="black", background="lightblue")
                    tree.tag_configure("odd2",foreground="black", background="ghost white")
                    Len_ListBox_DF = len(SingleSearchRowsDF)
                    SearchDB_Results.delete(0,END)
                    SearchDB_Results.insert(tk.END,Len_ListBox_DF)
                    button_UpdateCellValueDB.config(state="disabled")
            else:
                tkinter.messagebox.showinfo("Empty Search Results","Empty Search Results Return")
                sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = sqliteConnection.cursor()
                cursor.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_SingleSearchTempStorage")
                sqliteConnection.commit()
                cursor.close()
                sqliteConnection.close()
                SearchDB_Results.delete(0,END)
                SearchDB_Results.insert(tk.END,0) 
        else:
            tree.delete(*tree.get_children())
            messagebox.showerror('Search Entries Missing', "Search Variable Entry Or Search Value Entry Missing Or Both Entries Missing")
            TreeView_DataFrameReturn = TreeView_DataFrame()
            Len_ListBox_DF = TreeView_DataFrameReturn[1]
            SearchDB_Results.delete(0,END)
            SearchDB_Results.insert(tk.END,Len_ListBox_DF)
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = sqliteConnection.cursor()
            cursor.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_SingleSearchTempStorage")
            sqliteConnection.commit()
            cursor.close()
            sqliteConnection.close()

    def ExportSetAndCatch_QC_DB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            Complete_df = Complete_df.iloc[:, 3:len(list(Complete_df.columns))]
            Complete_df = Complete_df.replace('None', '')
            if len(Complete_df) >0:
                Export_MasterSetCatchQCDB_DF  = pd.DataFrame(Complete_df)
                Export_MasterSetCatchQCDB_DF  = Export_MasterSetCatchQCDB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterSetCatchQCDB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("Set And Catch QC Database Profile Message","Set And Catch QC Database Profile Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("Set And Catch QC Database Profile Message","Please Select File Name To Export")
            else:
                messagebox.showerror('Export Error : Set And Catch QC Database Profile Message', "Void File... Nothing to Export")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def ExportSetAndCatch_PopulatedEntries():
        GetSetCatchDB_Columns = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
        getTreeView_DataFrame = TreeView_DataFrame() 
        getExportSearchQueryResults = getTreeView_DataFrame[0]
        getExportSearchQueryResults.columns = GetSetCatchDB_Columns
        Complete_df = pd.DataFrame(getExportSearchQueryResults)
        if len(Complete_df) >0:
                Export_Search_DF  = pd.DataFrame(Complete_df)
                Export_Search_DF  = Export_Search_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_Search_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("Set And Catch QC Database Message","Set And Catch QC Database Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("Set And Catch QC Database Message","Please Select File Name To Export")
        else:
            messagebox.showerror('Export Error : Set And Catch QC Database Message', "Void File... Nothing to Export")

    def RunMultiVariableSearchQuery():
        ClearView_DBEntries()
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_MultiSearchTempStorage ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchMultiSearchTempStorage_DF  = pd.DataFrame(Complete_df)
                SetCatchMultiSearchTempStorage_DF  = SetCatchMultiSearchTempStorage_DF.reset_index(drop=True)
                SetCatchMultiSearchTempStorage_DF  = pd.DataFrame(SetCatchMultiSearchTempStorage_DF)
                df_rows = SetCatchMultiSearchTempStorage_DF.to_numpy().tolist()
                if (len(df_rows))>0:
                    cur_Columns = list(tree['columns'])
                    MultiSearchRowsDF = SetCatchMultiSearchTempStorage_DF.loc[:,cur_Columns]
                    MultiSearchRowsDF  = MultiSearchRowsDF.reset_index(drop=True)
                    MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
                    countIndex1 = 0
                    for each_rec in range(len(MultiSearchRowsDF)):
                        if countIndex1 % 2 == 0:
                            tree.insert("", tk.END, values=list(MultiSearchRowsDF.loc[each_rec]), tags =("even",))
                        else:
                            tree.insert("", tk.END, values=list(MultiSearchRowsDF.loc[each_rec]), tags =("odd",))
                        countIndex1 = countIndex1+1
                    tree.tag_configure("even1",foreground="black", background="lightblue")
                    tree.tag_configure("odd1",foreground="black", background="ghost white")
                    Length_SetCatchMultiSearchTempStorage_DF = len(SetCatchMultiSearchTempStorage_DF)
                    SearchDB_Results.delete(0,END)
                    SearchDB_Results.insert(tk.END,Length_SetCatchMultiSearchTempStorage_DF)
                    button_UpdateCellValueDB.config(state="disabled")
            else:
                SetCatchMultiSearchTempStorage_DF  = pd.DataFrame(Complete_df)
                SetCatchMultiSearchTempStorage_DF  = SetCatchMultiSearchTempStorage_DF.reset_index(drop=True)
                SetCatchMultiSearchTempStorage_DF  = pd.DataFrame(SetCatchMultiSearchTempStorage_DF)
                Length_SetCatchMultiSearchTempStorage_DF = len(SetCatchMultiSearchTempStorage_DF)
                SearchDB_Results.delete(0,END)
                SearchDB_Results.insert(tk.END,Length_SetCatchMultiSearchTempStorage_DF)
                messagebox.showinfo('DFO-NL-ASOP Set & Catch MultiVariable Search Message', 
                                    "Void Results DFO-NL-ASOP Set & Catch MultiVariable Search...Please Run The Search Again")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def BuildMultiSearchQuery():
        root=tk.Tk()
        root.title ("MultiVariable Search Query On Set & Catch QC Database")
        root.geometry('980x400+40+40')
        root.config(bg="cadet blue")
        Topframe = tk.Frame(root, bd = 2,relief = RIDGE)
        lbl_MultiVariableSearchQuery = Label(Topframe, font=('aerial', 14, 'bold'), 
                                    bg= "aliceblue", text="MultiVariable Search Query On Set & Catch QC Database")
        lbl_MultiVariableSearchQuery.grid(row =0, column = 0, padx=1, pady =2)
        Topframe.pack(side =TOP)

        Entryframe = tk.Frame(root, bd = 2,relief = RIDGE, bg ="cadet blue")
        Entryframe.pack(side =LEFT , padx=20, pady =10)

        lbl_Searchtype = Label(Entryframe, font=('aerial', 12, 'bold'),
                                                bg= "cadet blue", text=" A. Select Search Type (OR/AND) :")
        lbl_Searchtype.grid(row =0, column = 0, padx=2, pady =2, sticky =W)

        varSearchType = StringVar(Entryframe, value ="AND")
        varSearchTypeList = ["OR", "AND"]
        entry_Searchtype = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), justify='center',
                                        textvariable = varSearchType, width = 15)
        entry_Searchtype['values'] = sorted(list(varSearchTypeList))
        entry_Searchtype.grid(row =0, column = 1, padx=2, pady =2, sticky =W)
        lbl_EntriesForMultiSearch = Label(Entryframe, font=('aerial', 11, 'bold'),
                                                bg= "cadet blue", text=" B. Entries For MultiVariable Search :")
        lbl_EntriesForMultiSearch.grid(row =2, column = 0, padx=2, pady =2, sticky =W)
        
        # Entries For DeploymentUID
        lbl_Entries_DeploymentUID = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 01. Entries For DeploymentUID :")
        lbl_Entries_DeploymentUID.grid(row =3, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_DeploymentUID       = StringVar(Entryframe)
        entry_SearchValue_DeploymentUID = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_DeploymentUID, width = 25)
        entry_SearchValue_DeploymentUID.grid(row =3, column = 1, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_DeploymentUID['values'] = sorted([str(i) if i else None for i in list(set((Combo_input_DeploymentUID())))])
        
        # Entries For DeploymentNumber
        lbl_Entries_DeploymentNumber = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 02. Entries For DeploymentNumber :")
        lbl_Entries_DeploymentNumber.grid(row =4, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_DeploymentNumber       = IntVar(Entryframe, value ="")
        entry_SearchValue_DeploymentNumber = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_DeploymentNumber, width = 25)
        entry_SearchValue_DeploymentNumber.grid(row =4, column = 1, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_DeploymentNumber['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_DeploymentNumber())))])
        
        # Entries For ASOCCode
        lbl_Entries_ASOCCode = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                    bg= "cadet blue", text=" 03. Entries For ASOCCode :")
        lbl_Entries_ASOCCode.grid(row =5, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_ASOCCode       = IntVar(Entryframe, value ="")
        entry_SearchValue_ASOCCode = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_ASOCCode, width = 25)
        entry_SearchValue_ASOCCode.grid(row =5, column = 1, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_ASOCCode['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_ASOCCode())))])
        
        # Entries For ObserverNumber
        lbl_Entries_ObserverNumber = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 04. Entries For ObserverNumber :")
        lbl_Entries_ObserverNumber.grid(row =6, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_ObserverNumber       = StringVar(Entryframe)
        entry_SearchValue_ObserverNumber = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_ObserverNumber, width = 25)
        entry_SearchValue_ObserverNumber.grid(row =6, column = 1, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_ObserverNumber['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_ObserverNumber())))])
        
        # Entries For SetNumber
        lbl_Entries_SetNumber = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 05. Entries For SetNumber :")
        lbl_Entries_SetNumber.grid(row =7, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_SetNumber       = IntVar(Entryframe, value ="")
        entry_SearchValue_SetNumber = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_SetNumber, width = 25)
        entry_SearchValue_SetNumber.grid(row =7, column = 1, padx= 5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_SetNumber['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_SetNumber())))])

        # Entries For SetType
        lbl_Entries_SetType = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 06. Entries For SetType :")
        lbl_Entries_SetType.grid(row =8, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_SetType       = IntVar(Entryframe, value ="")
        entry_SearchValue_SetType = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_SetType, width = 25)
        entry_SearchValue_SetType.grid(row =8, column = 1, padx= 5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_SetType['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_SetType())))])

        # Entries For SubTripNumber
        lbl_Entries_SubTripNumber = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 07. Entries For SubTripNumber :")
        lbl_Entries_SubTripNumber.grid(row =9, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_SubTripNumber       = StringVar(Entryframe)
        entry_SearchValue_SubTripNumber = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_SubTripNumber, width = 25)
        entry_SearchValue_SubTripNumber.grid(row =9, column = 1, padx= 5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_SubTripNumber['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_SubTripNumber())))])

        # Entries For VesselSideNumber
        lbl_Entries_VesselSideNumber = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 08. Entries For VesselSideNumber :")
        lbl_Entries_VesselSideNumber.grid(row =10, column = 0, padx=15, pady =2, sticky =W)
        SearchValue_VesselSideNumber       = StringVar(Entryframe)
        entry_SearchValue_VesselSideNumber = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_VesselSideNumber, width = 25)
        entry_SearchValue_VesselSideNumber.grid(row =10, column = 1, padx= 5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_VesselSideNumber['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_VesselSideNumber())))])

        
        # Entries For NAFODivision
        lbl_Entries_NAFODivision = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 09. Entries For NAFODivision :")
        lbl_Entries_NAFODivision.grid(row =3, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_NAFODivision       = IntVar(Entryframe, value ="")
        entry_SearchValue_NAFODivision = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_NAFODivision, width = 25)
        entry_SearchValue_NAFODivision.grid(row =3, column = 3, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_NAFODivision['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_NAFODivision())))])

        # Entries For Country
        lbl_Entries_Country = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 10. Entries For Country :")
        lbl_Entries_Country.grid(row =4, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_Country       = IntVar(Entryframe, value ="")
        entry_SearchValue_Country = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_Country, width = 25)
        entry_SearchValue_Country.grid(row =4, column = 3, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_Country['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_Country())))])

        # Entries For UnitArea
        lbl_Entries_UnitArea = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 11. Entries For UnitArea :")
        lbl_Entries_UnitArea.grid(row =5, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_UnitArea       = IntVar(Entryframe, value ="")
        entry_SearchValue_UnitArea = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_UnitArea, width = 25)
        entry_SearchValue_UnitArea.grid(row =5, column = 3, padx= 5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_UnitArea['values'] = sorted([str(i) if i else 'None' for i in list(set((Combo_input_UnitArea())))])

        # Entries For Geartype
        lbl_Entries_GearType = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 12. Entries For GearType :")
        lbl_Entries_GearType.grid(row =6, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_GearType       = IntVar(Entryframe, value ="")
        entry_SearchValue_GearType = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_GearType, width = 25)
        entry_SearchValue_GearType.grid(row =6, column = 3, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_GearType['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_GearType())))])

        # Entries For RecordType
        lbl_Entries_RecordType = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 13. Entries For RecordType :")
        lbl_Entries_RecordType.grid(row =7, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_RecordType       = IntVar(Entryframe, value ="")
        entry_SearchValue_RecordType = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_RecordType, width = 25)
        entry_SearchValue_RecordType.grid(row =7, column = 3, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_RecordType['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_RecordType())))])
        
        # Entries For SpeciesCode
        lbl_Entries_SpeciesCode = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 14. Entries For SpeciesCode :")
        lbl_Entries_SpeciesCode.grid(row =8, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_SpeciesCode       = IntVar(Entryframe, value ="")
        entry_SearchValue_SpeciesCode = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_SpeciesCode, width = 25)
        entry_SearchValue_SpeciesCode.grid(row =8, column = 3, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_SpeciesCode['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_SpeciesCode())))])

        # Entries For DirectedSpecies
        lbl_Entries_DirectedSpecies = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 15. Entries For DirectedSpecies :")
        lbl_Entries_DirectedSpecies.grid(row =9, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_DirectedSpecies       = IntVar(Entryframe, value ="")
        entry_SearchValue_DirectedSpecies = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_DirectedSpecies, width = 25)
        entry_SearchValue_DirectedSpecies.grid(row =9, column = 3, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_DirectedSpecies['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_DirectedSpecies())))])

        # Entries For Day
        lbl_Entries_Day = Label(Entryframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" 16. Entries For Day :")
        lbl_Entries_Day.grid(row =10, column = 2, padx=15, pady =2, sticky =W)
        SearchValue_Day       = IntVar(Entryframe, value ="")
        entry_SearchValue_Day = ttk.Combobox(Entryframe, font=('aerial', 10, 'bold'), 
                                                textvariable = SearchValue_Day, width = 25)
        entry_SearchValue_Day.grid(row =10, column = 3, padx=5, pady =2, ipady =2, sticky =W)
        entry_SearchValue_Day['values'] = sorted([int(i) if i else np.nan for i in list(set((Combo_input_Day())))])

        ## Functions
        def Clear_EntriesSearch():
            entry_SearchValue_Day.delete(0,END)
            entry_SearchValue_DirectedSpecies.delete(0,END)
            entry_SearchValue_SpeciesCode.delete(0,END)
            entry_SearchValue_RecordType.delete(0,END)
            entry_SearchValue_GearType.delete(0,END)
            entry_SearchValue_UnitArea.delete(0,END)
            entry_SearchValue_Country.delete(0,END)
            entry_SearchValue_NAFODivision.delete(0,END)
            entry_SearchValue_VesselSideNumber.delete(0,END)
            entry_SearchValue_SubTripNumber.delete(0,END)
            entry_SearchValue_SetType.delete(0,END)
            entry_SearchValue_SetNumber.delete(0,END)
            entry_SearchValue_ObserverNumber.delete(0,END)
            entry_SearchValue_ASOCCode.delete(0,END)
            entry_SearchValue_DeploymentNumber.delete(0,END)
            entry_SearchValue_DeploymentUID.delete(0,END)
        
        def Submit_To_Set_Catch_MultiSearchTempStorage(MultiSearchRowsDF):
            try:
                TempImport_To_DBStorage = pd.DataFrame(MultiSearchRowsDF)
                sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = sqliteConnection.cursor()
                TempImport_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_MultiSearchTempStorage', sqliteConnection, if_exists="replace",index = False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Search_AND_MultiVariableQuery_Backend(DeploymentUID ="", DeploymentNumber ="", ASOCCode ="", ObserverNumber ="",\
                                                SetNumber ="", SetType ="", SubTripNumber ="", VesselSideNumber ="", NAFODivision ="", Country ="",\
                                                UnitArea ="", GearType ="", RecordType ="", SpeciesCode ="", DirectedSpecies ="", Day =""):
            try:
                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE \
                                                    (DeploymentUID = :DeploymentUID OR TRIM(COALESCE(:DeploymentUID, '')) = '') AND\
                                                    (DeploymentNumber= :DeploymentNumber OR TRIM(COALESCE(:DeploymentNumber, '')) = '') AND\
                                                    (ASOCCode= :ASOCCode OR TRIM(COALESCE(:ASOCCode, '')) = '') AND\
                                                    (ObserverNumber= :ObserverNumber OR TRIM(COALESCE(:ObserverNumber, '')) = '') AND\
                                                    (SetNumber= :SetNumber OR TRIM(COALESCE(:SetNumber, '')) = '') AND\
                                                    (SetType= :SetType OR TRIM(COALESCE(:SetType, '')) = '') AND\
                                                    (SubTripNumber= :SubTripNumber OR TRIM(COALESCE(:SubTripNumber, '')) = '') AND\
                                                    (VesselSideNumber= :VesselSideNumber OR TRIM(COALESCE(:VesselSideNumber, '')) = '') AND\
                                                    (NAFODivision= :NAFODivision OR TRIM(COALESCE(:NAFODivision, '')) = '') AND\
                                                    (Country= :Country OR TRIM(COALESCE(:Country, '')) = '') AND\
                                                    (UnitArea= :UnitArea OR TRIM(COALESCE(:UnitArea, '')) = '') AND\
                                                    (GearType= :GearType OR TRIM(COALESCE(:GearType, '')) = '') AND\
                                                    (RecordType= :RecordType OR TRIM(COALESCE(:RecordType, '')) = '') AND\
                                                    (SpeciesCode= :SpeciesCode OR TRIM(COALESCE(:SpeciesCode, '')) = '') AND\
                                                    (DirectedSpecies= :DirectedSpecies OR TRIM(COALESCE(:DirectedSpecies, '')) = '') AND\
                                                    (Day= :Day OR TRIM(COALESCE(:Day, '')) = '')",\
                                                    (DeploymentUID, DeploymentNumber , ASOCCode , ObserverNumber ,SetNumber, SetType, SubTripNumber,\
                                                    VesselSideNumber , NAFODivision , Country ,UnitArea , GearType , RecordType , SpeciesCode, DirectedSpecies, Day))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
            except:
                messagebox.showerror('Multi Variable Search Error Message', "Multi Search Query Failed")
                
        def Search_OR_MultiVariableQuery_Backend(DeploymentUID ="", DeploymentNumber ="", ASOCCode ="", ObserverNumber ="",\
                                                SetNumber ="", SetType ="", SubTripNumber ="", VesselSideNumber ="", NAFODivision ="", Country ="",\
                                                UnitArea ="", GearType ="", RecordType ="", SpeciesCode ="", DirectedSpecies ="", Day =""):
            try:
                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT WHERE DeploymentUID = ? COLLATE NOCASE OR \
                    DeploymentNumber = ? COLLATE NOCASE OR ASOCCode = ? COLLATE NOCASE OR ObserverNumber = ? COLLATE NOCASE OR \
                    SetNumber = ? COLLATE NOCASE OR SetType = ? COLLATE NOCASE OR SubTripNumber = ? COLLATE NOCASE OR VesselSideNumber = ? COLLATE NOCASE OR NAFODivision = ? OR Country = ? COLLATE NOCASE OR \
                    UnitArea = ? COLLATE NOCASE OR GearType = ? COLLATE NOCASE OR RecordType = ? COLLATE NOCASE OR SpeciesCode = ? COLLATE NOCASE OR DirectedSpecies = ? COLLATE NOCASE OR Day = ? COLLATE NOCASE",\
                    (DeploymentUID, DeploymentNumber , ASOCCode , ObserverNumber ,SetNumber, SetType, SubTripNumber,\
                    VesselSideNumber , NAFODivision , Country ,UnitArea , GearType , RecordType , SpeciesCode, DirectedSpecies, Day ))
                rows=cur_DB_Set_Catch_Analysis.fetchall()
                return rows
            except:
                messagebox.showerror('Multi Variable Search Error Message', "Multi Search Query Failed")

        def SubmitMultiVariableQuery():
            GetSetCatchDB_Columns = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
            get_entry_Searchtype = (entry_Searchtype.get())
            if (get_entry_Searchtype =="AND"):
                get_entry_DeploymentUID = entry_SearchValue_DeploymentUID.get()
                get_entry_DeploymentNumber = (entry_SearchValue_DeploymentNumber.get())
                get_entry_ASOCCode = (entry_SearchValue_ASOCCode.get())
                get_entry_ObserverNumber = (entry_SearchValue_ObserverNumber.get())
                get_entry_SetNumber = (entry_SearchValue_SetNumber.get())
                get_entry_SetType = (entry_SearchValue_SetType.get())
                get_entry_SubTripNumber = (entry_SearchValue_SubTripNumber.get())
                get_entry_VesselSideNumber = (entry_SearchValue_VesselSideNumber.get())

                get_entry_NAFODivision = (entry_SearchValue_NAFODivision.get())
                get_entry_Country = (entry_SearchValue_Country.get())
                get_entry_UnitArea = (entry_SearchValue_UnitArea.get())
                get_entry_GearType = (entry_SearchValue_GearType.get())
                get_entry_RecordType = (entry_SearchValue_RecordType.get())
                get_entry_SpeciesCode = (entry_SearchValue_SpeciesCode.get())
                get_entry_DirectedSpecies = (entry_SearchValue_DirectedSpecies.get())
                get_entry_Day = (entry_SearchValue_Day.get())

                if (len(get_entry_DeploymentNumber)!=0):
                    if(get_entry_DeploymentNumber!='NaN'):
                        try:
                            get_entry_DeploymentNumber = int(get_entry_DeploymentNumber)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "DeploymentNumber Must Be Numeric Value")
                    else:
                        get_entry_DeploymentNumber = 'VoidValue'
                else:
                    get_entry_DeploymentNumber = (get_entry_DeploymentNumber)
                
                if (len(get_entry_ASOCCode)!=0):
                    if(get_entry_ASOCCode!='NaN'):
                        try:
                            get_entry_ASOCCode = int(get_entry_ASOCCode)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "ASOCCode Must Be Numeric Value")
                    else:
                        get_entry_ASOCCode = 'VoidValue'
                else:
                    get_entry_ASOCCode = (get_entry_ASOCCode)
                
                if (len(get_entry_SetNumber)!=0):
                    if(get_entry_SetNumber!='NaN'):
                        try:
                            get_entry_SetNumber = int(get_entry_SetNumber)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "SetNumber Must Be Numeric Value")
                    else:
                        get_entry_SetNumber = 'VoidValue'
                else:
                    get_entry_SetNumber = (get_entry_SetNumber)
                
                if (len(get_entry_SetType)!=0):
                    if(get_entry_SetType!='NaN'):
                        try:
                            get_entry_SetType = int(get_entry_SetType)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "SetType Must Be Numeric Value")
                    else:
                        get_entry_SetType = 'VoidValue'
                else:
                    get_entry_SetType = (get_entry_SetType)

                if (len(get_entry_Country)!=0):
                    if(get_entry_Country!='NaN'):
                        try:
                            get_entry_Country = int(get_entry_Country)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "Country Must Be Numeric Value")
                    else:
                        get_entry_Country = 'VoidValue'
                else:
                    get_entry_Country = (get_entry_Country)                

                if (len(get_entry_GearType)!=0):
                    if(get_entry_GearType!='NaN'):
                        try:
                            get_entry_GearType = int(get_entry_GearType)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "GearType Must Be Numeric Value")
                    else:
                        get_entry_GearType = 'VoidValue'
                else:
                    get_entry_GearType = (get_entry_GearType)

                if (len(get_entry_RecordType)!=0):
                    if(get_entry_RecordType!='NaN'):
                        try:
                            get_entry_RecordType = int(get_entry_RecordType)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "RecordType Must Be Numeric Value")
                    else:
                        get_entry_RecordType = 'VoidValue'
                else:
                    get_entry_RecordType = (get_entry_RecordType)

                if (len(get_entry_SpeciesCode)!=0):
                    if(get_entry_SpeciesCode!='NaN'):
                        try:
                            get_entry_SpeciesCode = int(get_entry_SpeciesCode)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "SpeciesCode Must Be Numeric Value")
                    else:
                        get_entry_SpeciesCode = 'VoidValue'
                else:
                    get_entry_SpeciesCode = (get_entry_SpeciesCode)                
                
                if (len(get_entry_DirectedSpecies)!=0):
                    if(get_entry_DirectedSpecies!='NaN'):
                        try:
                            get_entry_DirectedSpecies = int(get_entry_DirectedSpecies)
                        except:
                             messagebox.showerror('Search Variable Datatype Error Message', "DirectedSpecies Must Be Numeric Value")
                    else:
                        get_entry_DirectedSpecies = 'VoidValue'
                else:
                    get_entry_DirectedSpecies = (get_entry_DirectedSpecies)

                if (len(get_entry_Day)!=0):
                    if(get_entry_Day!='NaN'):
                        try:
                            get_entry_Day = int(get_entry_Day)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "Day Must Be Numeric Value")
                    else:
                        get_entry_Day = 'VoidValue'
                else:
                    get_entry_Day = (get_entry_Day)

                CheckinVoidvalue = [get_entry_DeploymentNumber, get_entry_ASOCCode, get_entry_SetNumber,get_entry_SetType,
                                    get_entry_Country, get_entry_GearType, get_entry_RecordType, get_entry_SpeciesCode,
                                    get_entry_DirectedSpecies, get_entry_Day]
                if 'VoidValue' in CheckinVoidvalue:
                    messagebox.showinfo('DFO-NL-ASOP Set & Catch MultiVariable AND Search Message', 
                                        "Multi-Search With NaN Or Void Value Cannot Process Right Now. Will Be Implemented Later") 
                else:
                    MultiSearchRows = Search_AND_MultiVariableQuery_Backend(get_entry_DeploymentUID, get_entry_DeploymentNumber,get_entry_ASOCCode,\
                                                                            get_entry_ObserverNumber, get_entry_SetNumber, get_entry_SetType, get_entry_SubTripNumber, get_entry_VesselSideNumber,\
                                                                            get_entry_NAFODivision, get_entry_Country, get_entry_UnitArea,\
                                                                            get_entry_GearType, get_entry_RecordType, get_entry_SpeciesCode, get_entry_DirectedSpecies, get_entry_Day)
                    MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, columns =GetSetCatchDB_Columns)
                    MultiSearchRowsDF.reset_index(drop=True)
                    Submit_To_Set_Catch_MultiSearchTempStorage(MultiSearchRowsDF)
                    messagebox.showinfo('DFO-NL-ASOP Set & Catch MultiVariable AND Search Message', 
                                        "Search Results Stored In Database. Please Run View Multi Search Results Button to View The Search Results")   

            if(get_entry_Searchtype =="OR"):
                get_entry_Day = (entry_SearchValue_Day.get())
                get_entry_DirectedSpecies = (entry_SearchValue_DirectedSpecies.get())
                get_entry_SpeciesCode = (entry_SearchValue_SpeciesCode.get())
                get_entry_RecordType = (entry_SearchValue_RecordType.get())
                get_entry_GearType = (entry_SearchValue_GearType.get())
                get_entry_UnitArea = (entry_SearchValue_UnitArea.get())
                get_entry_Country = (entry_SearchValue_Country.get())
                get_entry_NAFODivision = (entry_SearchValue_NAFODivision.get())

                get_entry_VesselSideNumber = (entry_SearchValue_VesselSideNumber.get())
                get_entry_SubTripNumber = (entry_SearchValue_SubTripNumber.get())
                get_entry_SetType = (entry_SearchValue_SetType.get())
                get_entry_SetNumber = (entry_SearchValue_SetNumber.get())
                get_entry_ObserverNumber = (entry_SearchValue_ObserverNumber.get())
                get_entry_ASOCCode = (entry_SearchValue_ASOCCode.get())
                get_entry_DeploymentNumber = (entry_SearchValue_DeploymentNumber.get())
                get_entry_DeploymentUID = entry_SearchValue_DeploymentUID.get()

                if(len(get_entry_Day)!=0):
                    if(get_entry_Day!='NaN'):
                        try:
                            get_entry_Day = int(get_entry_Day)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "Day Must Be Numeric Value")
                    else:
                        get_entry_Day = 'VoidValue' 
                else:
                    get_entry_Day = int(99999999999)
                
                if(len(get_entry_DirectedSpecies)!=0):
                    if(get_entry_DirectedSpecies!='NaN'):
                        try:
                            get_entry_DirectedSpecies = int(get_entry_DirectedSpecies)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "DirectedSpecies Must Be Numeric Value")
                    else:
                        get_entry_DirectedSpecies = 'VoidValue' 
                else:
                    get_entry_DirectedSpecies = int(99999999999)

                if(len(get_entry_SpeciesCode)!=0):
                    if(get_entry_SpeciesCode!='NaN'):
                        try:
                            get_entry_SpeciesCode = int(get_entry_SpeciesCode)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "SpeciesCode Must Be Numeric Value")
                    else:
                        get_entry_SpeciesCode = 'VoidValue' 
                else:
                    get_entry_SpeciesCode = int(99999999999)
                
                if(len(get_entry_RecordType)!=0):
                    if(get_entry_RecordType!='NaN'):
                        try:
                            get_entry_RecordType = int(get_entry_RecordType)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "RecordType Must Be Numeric Value")
                    else:
                        get_entry_RecordType = 'VoidValue' 
                else:
                    get_entry_RecordType = int(99999999999)            
                
                if(len(get_entry_GearType)!=0):
                    if(get_entry_GearType!='NaN'):
                        try:
                            get_entry_GearType = int(get_entry_GearType)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "GearType Must Be Numeric Value")
                    else:
                        get_entry_GearType = 'VoidValue' 
                else:
                    get_entry_GearType = int(99999999999)
                
                if(len(get_entry_UnitArea)!=0):
                    get_entry_UnitArea = str(get_entry_UnitArea)
                else:
                    get_entry_UnitArea = str(99999999999)            

                if(len(get_entry_Country)!=0):
                    if(get_entry_Country!='NaN'):
                        try:
                            get_entry_Country = int(get_entry_Country)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "Country Must Be Numeric Value")
                    else:
                        get_entry_Country = 'VoidValue' 
                else:
                    get_entry_Country = int(99999999999)
                
                if(len(get_entry_NAFODivision)!=0):
                    get_entry_NAFODivision = str(get_entry_NAFODivision)
                else:
                    get_entry_NAFODivision = str(99999999999)            
                
                if(len(get_entry_VesselSideNumber)!=0) :
                    get_entry_VesselSideNumber = str(get_entry_VesselSideNumber)
                else:
                    get_entry_VesselSideNumber = str(99999999999)
                
                if(len(get_entry_SubTripNumber)!=0):
                    get_entry_SubTripNumber = str(get_entry_SubTripNumber)
                else:
                    get_entry_SubTripNumber = str(99999999999)            
                
                if(len(get_entry_SetType)!=0):
                    if(get_entry_SetType!='NaN'):
                        try:
                            get_entry_SetType = int(get_entry_SetType)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "SetType Must Be Numeric Value")
                    else:
                        get_entry_SetType = 'VoidValue' 
                else:
                    get_entry_SetType = int(99999999999)            
                
                if(len(get_entry_SetNumber)!=0):
                    if(get_entry_SetNumber!='NaN'):
                        try:
                            get_entry_SetNumber = int(get_entry_SetNumber)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "SetNumber Must Be Numeric Value")
                    else:
                        get_entry_SetNumber = 'VoidValue'  
                else:
                    get_entry_SetNumber = int(99999999999)             
                
                if(len(get_entry_ObserverNumber)!=0):
                    get_entry_ObserverNumber = str(get_entry_ObserverNumber)
                else:
                    get_entry_ObserverNumber = str(99999999999)

                if(len(get_entry_ASOCCode)!=0):
                    if(get_entry_ASOCCode!='NaN'):
                        try:
                            get_entry_ASOCCode = int(get_entry_ASOCCode)
                        except:
                            messagebox.showerror('Search Variable Datatype Error Message', "ASOCCode Must Be Numeric Value")
                    else:
                        get_entry_ASOCCode = 'VoidValue'     
                else:
                    get_entry_ASOCCode = int(99999999999) 
                
                if(len(get_entry_DeploymentNumber)!=0):
                    if(get_entry_DeploymentNumber!='NaN'):
                        try:
                            get_entry_DeploymentNumber = int(get_entry_DeploymentNumber)
                        except:
                             messagebox.showerror('Search Variable Datatype Error Message', "DeploymentNumber Must Be Numeric Value")
                    else:
                        get_entry_DeploymentNumber = 'VoidValue'
                else:
                    get_entry_DeploymentNumber = int(99999999999) 

                if(len(get_entry_DeploymentUID)!=0):
                    get_entry_DeploymentUID = str(get_entry_DeploymentUID)
                else:
                    get_entry_DeploymentUID = str(99999999999)
                
                CheckinVoidvalue = [get_entry_DeploymentNumber, get_entry_ASOCCode, get_entry_SetNumber,get_entry_SetType,
                                    get_entry_Country, get_entry_GearType, get_entry_RecordType, get_entry_SpeciesCode,
                                    get_entry_DirectedSpecies, get_entry_Day]
                if 'VoidValue' in CheckinVoidvalue:
                    messagebox.showinfo('DFO-NL-ASOP Set & Catch MultiVariable AND Search Message', 
                                        "Multi-Search With NaN Or Void Value Cannot Process Right Now. Will Be Implemented Later")
                else:  
                    MultiSearchRows = Search_OR_MultiVariableQuery_Backend(get_entry_DeploymentUID, get_entry_DeploymentNumber,get_entry_ASOCCode,\
                                                                            get_entry_ObserverNumber, get_entry_SetNumber, get_entry_SetType, get_entry_SubTripNumber, get_entry_VesselSideNumber,\
                                                                            get_entry_NAFODivision, get_entry_Country, get_entry_UnitArea,\
                                                                            get_entry_GearType, get_entry_RecordType, get_entry_SpeciesCode, get_entry_DirectedSpecies, get_entry_Day )
                    MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, columns =GetSetCatchDB_Columns)
                    MultiSearchRowsDF.reset_index(drop=True)
                    Submit_To_Set_Catch_MultiSearchTempStorage(MultiSearchRowsDF)
                    messagebox.showinfo('DFO-NL-ASOP Set & Catch MultiVariable OR Search Message', 
                                        "Search Results Stored In Database. Please Run View Multi Search Results Button to View The Search Results")

        ## Buttons
        button_SearchMultiVariableQuery = Button(Entryframe, bd = 2, text ="Submit Multi Variable Query ", width = 25,
                                    height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                    command =SubmitMultiVariableQuery)
        button_SearchMultiVariableQuery.grid(row =11, column = 3, padx=2, pady =1, ipady =1, sticky =W)


        button_SearchClearEntries = Button(Entryframe, bd = 2, text ="Clear Entries On Search ", width = 24,
                                    height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                    command =Clear_EntriesSearch)
        button_SearchClearEntries.grid(row =11, column = 0, padx=30, pady =5, ipady =1, sticky =W)

        root.mainloop()

    def RunTextualVariableSearchQuery():
        def Submit_To_Set_Catch_TextualSearchTempStorage(TextualSearchRowsDF):
            try:
                TempImport_To_DBStorage = pd.DataFrame(TextualSearchRowsDF)
                sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = sqliteConnection.cursor()
                TempImport_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_TextualSearchTempStorage', sqliteConnection, if_exists="replace",index = False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        get_TextualVariableSearch = entry_SearchValue_Variable_C.get()
        if(len(get_TextualVariableSearch)!=0):    
            tree.delete(*tree.get_children())
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
            try:
                cur_DB_Set_Catch_Analysis.execute("SELECT * FROM `DFO_NL_ASOP_Set_Catch_Analysis_IMPORT` WHERE `DeploymentUID` LIKE ? OR `ObserverNumber` LIKE ? OR\
                                                    `SubTripNumber` LIKE ? OR `VesselSideNumber` LIKE ? ",\
                                                    ('%'+str(get_TextualVariableSearch)+'%', '%'+str(get_TextualVariableSearch)+'%', '%'+str(get_TextualVariableSearch)+'%',\
                                                    '%'+ str(get_TextualVariableSearch)+'%'))            
                fetch = cur_DB_Set_Catch_Analysis.fetchall()
                rows = pd.DataFrame(fetch)
                rows.reset_index(drop=True)
                TextualSearchRowsDF = pd.DataFrame(rows)
                TextualSearchRowsDF.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 2:'DeploymentUID',
                            3:'ASOCCode', 4:'ObserverNumber', 5:'Year', 6:'DeploymentNumber', 7:'SubTripNumber', 
                            8:'SetNumber', 9:'Country', 10:'Quota', 11:'SetType', 12:'VesselSideNumber', 
                            13:'VesselClass', 14:'VesselLength', 15:'VesselHorsepower', 16:'Day', 17:'Month', 
                            18:'HaulDay', 19:'HaulMonth', 20:'StartTime', 21:'Duration', 22:'PositionPrecision',
                            23:'StartLatitude', 24:'StartLongitude', 25:'EndLatitude', 26:'EndLongitude', 27:'NAFODivision', 
                            28:'UnitArea', 29:'StatisticalArea', 30:'InOut200MileLimit', 31:'GearType', 32:'CodendMeshSize', 
                            33:'MeshSizeMG', 34:'MeshSizeFG', 35:'RollerBobbbinDiameter', 36:'NumberGillnets', 37:'AverageGillnetLength', 
                            38:'GrateBarSpacing', 39:'FootropeLength', 40:'NumberWindows', 41:'NumberHooks', 42:'NumberPots', 
                            43:'NumberPotReleasedCrab', 44:'GearDamage', 45:'AverageTowSpeed', 46:'AverageDepth', 47:'DataSource', 
                            48:'DirectedSpecies', 49:'NumberSpecies', 50:'RecordType', 51:'DetailedCatchSpeciesCompCode', 52:'LogbookIDNumber1', 
                            53:'LogbookIDNumber2', 54:'SpeciesCode', 55:'KeptWeight', 56:'DiscardWeight', 57:'EstimatedWeightReleasedCrab',
                            58:'NumberIndividuals'},inplace = True)
                TextualSearchRowsDF.reset_index(drop=True)
                TextualSearchRowsDF = pd.DataFrame(TextualSearchRowsDF)
                if (len(TextualSearchRowsDF))>0:
                    Submit_To_Set_Catch_TextualSearchTempStorage(TextualSearchRowsDF)
                    cur_Columns = list(tree['columns'])
                    TextualSearchRowsDF = TextualSearchRowsDF.loc[:,cur_Columns]
                    TextualSearchRowsDF  = TextualSearchRowsDF.reset_index(drop=True)
                    TextualSearchRowsDF  = pd.DataFrame(TextualSearchRowsDF)
                    if rows is not None:
                        countIndex1 = 0
                        for each_rec in range(len(TextualSearchRowsDF)):
                            if countIndex1 % 2 == 0:
                                tree.insert("", tk.END, values=list(TextualSearchRowsDF.loc[each_rec]), tags =("even",))
                            else:
                                tree.insert("", tk.END, values=list(TextualSearchRowsDF.loc[each_rec]), tags =("odd",))
                            countIndex1 = countIndex1+1
                        tree.tag_configure("even3",foreground="black", background="lightblue")
                        tree.tag_configure("odd3",foreground="black", background="ghost white")
                        cur_DB_Set_Catch_Analysis.close()
                        conn_DB_Set_Catch_Analysis.close()
                        Length_fetchData = len(TextualSearchRowsDF)
                        SearchDB_Results.delete(0,END)
                        SearchDB_Results.insert(tk.END,Length_fetchData)
                        button_UpdateCellValueDB.config(state="disabled")
                else:
                    tkinter.messagebox.showinfo("Empty Search Results","Empty Search Results Return")
                    sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = sqliteConnection.cursor()
                    cursor.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_TextualSearchTempStorage")
                    sqliteConnection.commit()
                    cursor.close()
                    sqliteConnection.close()
                    SearchDB_Results.delete(0,END)
                    SearchDB_Results.insert(tk.END,0) 
            except:
                messagebox.showerror('Textual Variable Search Error Message', "Textual Variable Search Encounter With Error")
        else:
            tree.delete(*tree.get_children())
            messagebox.showerror('Search Entries Missing', "Search Variable Entry Missing")
            TreeView_DataFrameReturn = TreeView_DataFrame()
            Len_ListBox_DF = TreeView_DataFrameReturn[1]
            SearchDB_Results.delete(0,END)
            SearchDB_Results.insert(tk.END,Len_ListBox_DF)
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = sqliteConnection.cursor()
            cursor.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_TextualSearchTempStorage")
            sqliteConnection.commit()
            cursor.close()
            sqliteConnection.close()

    def ExportSearchQueryResults():
        def ExportSetAndCatch_MultiSearchDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_MultiSearchTempStorage ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    Export_MasterSetCatchQCDB_DF  = pd.DataFrame(Complete_df)
                    Export_MasterSetCatchQCDB_DF  = Export_MasterSetCatchQCDB_DF.reset_index(drop=True)
                    filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                            defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                    if len(filename) >0:
                        Export_MasterSetCatchQCDB_DF.to_csv(filename,index=None)
                        tkinter.messagebox.showinfo("Set And Catch QC Database Multi-Search Message","Set And Catch QC Database Multi-Search Report Saved as CSV")
                    else:
                        tkinter.messagebox.showinfo("Set And Catch QC Database Multi-Search Message","Please Select File Name To Export Multi-Search Report")
                else:
                    messagebox.showerror('Export Error : Set And Catch QC Database Multi-Search Message', "Void File... Nothing to Export Multi-Search Report")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        def ExportSetAndCatch_SingleSearchDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_SingleSearchTempStorage ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    Export_MasterSetCatchQCDB_DF  = pd.DataFrame(Complete_df)
                    Export_MasterSetCatchQCDB_DF  = Export_MasterSetCatchQCDB_DF.reset_index(drop=True)
                    filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                            defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                    if len(filename) >0:
                        Export_MasterSetCatchQCDB_DF.to_csv(filename,index=None)
                        tkinter.messagebox.showinfo("Set And Catch QC Database Single-Search Message","Set And Catch QC Database Single-Search Report Saved as CSV")
                    else:
                        tkinter.messagebox.showinfo("Set And Catch QC Database Single-Search Message","Please Select File Name To Export Single-Search Report")
                else:
                    messagebox.showerror('Export Error : Set And Catch QC Database Single-Search Message', "Void File... Nothing to Export Single-Search Report")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        def ExportSetAndCatch_TextualSearchDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_TextualSearchTempStorage ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    Export_MasterSetCatchQCDB_DF  = pd.DataFrame(Complete_df)
                    Export_MasterSetCatchQCDB_DF  = Export_MasterSetCatchQCDB_DF.reset_index(drop=True)
                    filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                            defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                    if len(filename) >0:
                        Export_MasterSetCatchQCDB_DF.to_csv(filename,index=None)
                        tkinter.messagebox.showinfo("Set And Catch QC Database Textual-Search Message","Set And Catch QC Database Textual-Search Report Saved as CSV")
                    else:
                        tkinter.messagebox.showinfo("Set And Catch QC Database Textual-Search Message","Please Select File Name To Export Textual-Search Report")
                else:
                    messagebox.showerror('Export Error : Set And Catch QC Database Textual-Search Message', "Void File... Nothing to Export Textual-Search Report")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        root1=tk.Tk()
        root1.title ("Export Search Query")
        root1.geometry('340x110+400+300')
        root1.config(bg="cadet blue")
        Topframe = tk.Frame(root1, bd = 2,relief = RIDGE)
        Topframe.pack(side =LEFT)
        
        lbl_ExportSearchResultsDB = Label(Topframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" Select Search Query Type To Export :")
        lbl_ExportSearchResultsDB.grid(row =0, column = 0, padx=1, pady =1, sticky =W)

        ListSearchType = ['Export Set And Catch MultiSearch DB', 
                          'Export Set And Catch SingleSearch DB', 
                          'Export Set And Catch TextualSearch DB']
        VariableListSearchType        = StringVar(Topframe, value ='VoidValue')
        entry_ListSearchType  = ttk.Combobox(Topframe, font=('aerial', 10, 'bold'), 
                                                textvariable = VariableListSearchType, width = 44, state='readonly')
        entry_ListSearchType.grid(row =1, column = 0, padx=2, pady =1, ipady= 1, sticky =W)
        entry_ListSearchType['values'] = sorted(list(ListSearchType))

        def ExportSubmitRequest():
            ListSearchType = ['Export Set And Catch MultiSearch DB', 'Export Set And Catch SingleSearch DB', 'Export Set And Catch TextualSearch DB']
            get_entry_ListSearchType = entry_ListSearchType.get()
            if(len(get_entry_ListSearchType)!=0) & ((get_entry_ListSearchType)==ListSearchType[0]):
                RootExit1()
                ExportSetAndCatch_MultiSearchDB()
            
            if(len(get_entry_ListSearchType)!=0) & ((get_entry_ListSearchType)==ListSearchType[1]):
                RootExit1()
                ExportSetAndCatch_SingleSearchDB()
                
            if(len(get_entry_ListSearchType)!=0) & ((get_entry_ListSearchType)==ListSearchType[2]):
                RootExit1()
                ExportSetAndCatch_TextualSearchDB()
            
            if(len(get_entry_ListSearchType)==0):
                messagebox.showerror('Export Search Results Error Message', "Please Select The Search Type To Export Results")
                RootExit1()
        
        def RootExit1():
            root1.destroy()

        button_Submit= Button(Topframe, bd = 2, text ="Export Search Results", width = 20,
                                        height=1, font=('aerial', 11, 'bold'),
                                        fg="blue", bg="aliceblue",
                                        command =ExportSubmitRequest)
        button_Submit.grid(row =2, column = 0, padx=70, pady =2, ipady =1, sticky =W)
        root1.mainloop()
        
    def ViewSearchQueryResults():
        
        def ExcelViewMultiSearchResults():
            
            def get_ViewMultiSearchResults():
                try:
                    sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = sqliteConnection.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_MultiSearchTempStorage ORDER BY `RecordIdentifier` ASC ;", sqliteConnection)
                    length_Complete_df = len(Complete_df)
                    if length_Complete_df > 0:
                        Complete_df = Complete_df.reset_index(drop=True)
                        MultiSearchResultsDB = pd.DataFrame(Complete_df)
                        sqliteConnection.commit()
                        return MultiSearchResultsDB, length_Complete_df
                    else:
                        MultiSearchResultsDB = []
                        length_Complete_df = 0
                        messagebox.showerror('Set & Catch Multi-Search Database Is Empty', 
                                             "Please Run Multi Search Widget To View Search Results")
                        return MultiSearchResultsDB, length_Complete_df
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if sqliteConnection:
                        cursor.close()
                        sqliteConnection.close()
            
            Return_ViewMultiSearchResults = get_ViewMultiSearchResults()
            MultiSearchResultsDB = Return_ViewMultiSearchResults[0]
            length_Complete_df = int(Return_ViewMultiSearchResults[1])
            if length_Complete_df >0:
                windows = tk.Toplevel()
                windows.title ("Excel View Only Multi-Search Query Results")
                windows.geometry('1600x755+40+40')
                windows.config(bg="cadet blue")
                frame = tk.Frame(windows)
                frame.pack(fill=BOTH, expand=1)
                MultiSearchResultsDB = pd.DataFrame(MultiSearchResultsDB, index=None)
                pt = Table(frame, dataframe = MultiSearchResultsDB, showtoolbar=False, showstatusbar=False)
                pt.setRowColors(rows=range(1,len(MultiSearchResultsDB),2), clr='lightblue', cols='all')
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
            else:
                tkinter.messagebox.showinfo("Empty Search Results","Empty Search Results Return")

        def ExcelViewSingleSearchResults():
           
            def get_ViewSingleSearchResults():
                try:
                    sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = sqliteConnection.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_SingleSearchTempStorage ORDER BY `RecordIdentifier` ASC ;", sqliteConnection)
                    length_Complete_df = len(Complete_df)
                    if length_Complete_df > 0:
                        Complete_df = Complete_df.reset_index(drop=True)
                        SingleSearchResultsDB = pd.DataFrame(Complete_df)
                        return SingleSearchResultsDB
                    else:
                        SingleSearchResultsDB = []
                        messagebox.showerror('Set & Catch Single-Search Database Is Empty', 
                                             "Please Run Single Search Widget To View Search Results")
                        return SingleSearchResultsDB
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if sqliteConnection:
                        cursor.close()
                        sqliteConnection.close()
            
            Return_ViewSingleSearchResults = get_ViewSingleSearchResults()
            SingleSearchResultsDB = Return_ViewSingleSearchResults
            length_Complete_df = len(Return_ViewSingleSearchResults)
            
            if length_Complete_df > 0:
                windows = tk.Toplevel()
                windows.title ("Excel View Only Single-Search Query Results")
                windows.geometry('1600x755+40+40')
                windows.config(bg="cadet blue")
                frame = tk.Frame(windows)
                frame.pack(fill=BOTH, expand=1)
                SingleSearchResultsDB = pd.DataFrame(SingleSearchResultsDB, index=None)
                pt = Table(frame, dataframe = SingleSearchResultsDB, showtoolbar=False, showstatusbar=False)
                pt.setRowColors(rows=range(1,len(SingleSearchResultsDB),2), clr='lightblue', cols='all')
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
            else:
                tkinter.messagebox.showinfo("Empty Search Results","Empty Search Results Return")

        def ExcelViewTextualSearchResults():
            
            def get_ViewTextualSearchResults():
                try:
                    sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = sqliteConnection.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_TextualSearchTempStorage ORDER BY `RecordIdentifier` ASC ;", sqliteConnection)
                    length_Complete_df = len(Complete_df)
                    if length_Complete_df > 0:
                        Complete_df = Complete_df.reset_index(drop=True)
                        TextualSearchResultsDB = pd.DataFrame(Complete_df)
                        sqliteConnection.commit()
                        return TextualSearchResultsDB, length_Complete_df
                    else:
                        TextualSearchResultsDB = []
                        length_Complete_df = 0
                        messagebox.showerror('Set & Catch Textual-Search Database Is Empty', 
                                             "Please Run Textual Search Widget To View Search Results")
                        return TextualSearchResultsDB, length_Complete_df
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if sqliteConnection:
                        cursor.close()
                        sqliteConnection.close()
            
            Return_ViewTextualSearchResults = get_ViewTextualSearchResults()
            TextualSearchResultsDB = Return_ViewTextualSearchResults[0]
            length_Complete_df = Return_ViewTextualSearchResults[1]
            if length_Complete_df > 0:
                windows = tk.Toplevel()
                windows.title ("Excel View Only Textual-Search Query Results")
                windows.geometry('1600x755+40+40')
                windows.config(bg="cadet blue")
                frame = tk.Frame(windows)
                frame.pack(fill=BOTH, expand=1)
                TextualSearchResultsDB = pd.DataFrame(TextualSearchResultsDB, index=None)
                pt = Table(frame, dataframe = TextualSearchResultsDB, showtoolbar=False, showstatusbar=False)
                pt.setRowColors(rows=range(1,len(TextualSearchResultsDB),2), clr='lightblue', cols='all')
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
            else:
                tkinter.messagebox.showinfo("Empty Search Results","Empty Search Results Return")

        root1=tk.Tk()
        root1.title ("View Search Query")
        root1.geometry('340x110+400+300')
        root1.config(bg="cadet blue")
        Topframe = tk.Frame(root1, bd = 2,relief = RIDGE)
        Topframe.pack(side =LEFT)

        lbl_ViewSearchResultsDB = Label(Topframe, font=('aerial', 10, 'bold'),
                                                bg= "cadet blue", text=" Select Search Query Type To View :")
        lbl_ViewSearchResultsDB.grid(row =0, column = 0, padx=1, pady =1, sticky =W)

        ListSearchType = ['View Set And Catch MultiSearch DB', 'View Set And Catch SingleSearch DB', 'View Set And Catch TextualSearch DB']
        VariableListSearchType        = StringVar(Topframe, value ='')
        entry_ListSearchType  = ttk.Combobox(Topframe, font=('aerial', 10, 'bold'), 
                                                textvariable = VariableListSearchType, width = 44, state='readonly')
        entry_ListSearchType.grid(row =1, column = 0, padx=2, pady =1, ipady= 1, sticky =W)
        entry_ListSearchType['values'] = sorted(list(ListSearchType))

        def ViewSubmitRequest():
            ListSearchType = ['View Set And Catch MultiSearch DB', 'View Set And Catch SingleSearch DB', 'View Set And Catch TextualSearch DB']
            get_entry_ListSearchType = entry_ListSearchType.get()
            if(len(get_entry_ListSearchType)!=0) & ((get_entry_ListSearchType)==ListSearchType[0]):
                RootExit1()
                ExcelViewMultiSearchResults()
                
            if(len(get_entry_ListSearchType)!=0) & ((get_entry_ListSearchType)==ListSearchType[1]):
                RootExit1()
                ExcelViewSingleSearchResults()
                
            if(len(get_entry_ListSearchType)!=0) & ((get_entry_ListSearchType)==ListSearchType[2]):
                RootExit1()
                ExcelViewTextualSearchResults()
                
            if(len(get_entry_ListSearchType)==0):
                messagebox.showerror('View Search Results Error Message', "Please Select The Search Type To View Results")
                RootExit1() 
        
        def RootExit1():
            root1.destroy()
        
        button_Submit= Button(Topframe, bd = 2, text ="View Search Results", width = 20,
                                        height=1, font=('aerial', 11, 'bold'),
                                        fg="blue", bg="aliceblue",
                                        command =ViewSubmitRequest)
        button_Submit.grid(row =2, column = 0, padx=70, pady =2, ipady =1, sticky =W)
        root1.mainloop()

    def ExportTreeViewSelectionCSV():
        if len(tree.get_children())>0:
            cur_id = tree.focus()
            selvalue = tree.item(cur_id)['values']
            Length_Selected  =  (len(selvalue))
            if Length_Selected != 0:
                SelectionTree = tree.selection()
                row_list = []
                Treeviewcolumns  = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
                for row in SelectionTree:
                    row_list.append(tree.item(row)["values"])
                treeview_df = pd.DataFrame(row_list, columns = Treeviewcolumns)
                if len(treeview_df) >0:
                    Export_treeview_df  = pd.DataFrame(treeview_df)
                    Export_treeview_df  = Export_treeview_df.reset_index(drop=True)
                    filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                    if len(filename) >0:
                        Export_treeview_df.to_csv(filename,index=None)
                        tkinter.messagebox.showinfo("Set And Catch Table Selection Message","Set And Catch Table View Selected Entries Saved as CSV")
                    else:
                        tkinter.messagebox.showinfo("Set And Catch Table Selection Message","Please Select File Name To Export")
                else:
                    messagebox.showerror('Export Error : Set And Catch Table Selection Message', "Void File... Nothing to Export")
            else:
                tkinter.messagebox.showinfo("Set And Catch Table Selection Error","Please Select At least One Entries In the Table To Export")
        else:
            tkinter.messagebox.showinfo("Set And Catch Table Selection","Empty Set & Catch Table. Please Select At least One Entries In the Table To Export")

    def ExcelViewTreeViewSelection():
        if len(tree.get_children())>0:
            cur_id = tree.focus()
            selvalue = tree.item(cur_id)['values']
            Length_Selected  =  (len(selvalue))
            if Length_Selected != 0:
                SelectionTree = tree.selection()
                row_list = []
                Treeviewcolumns  = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
                for row in SelectionTree:
                    row_list.append(tree.item(row)["values"])
                treeview_df = pd.DataFrame(row_list, columns = Treeviewcolumns)
                if len(treeview_df) >0:
                    View_treeview_df  = pd.DataFrame(treeview_df)
                    View_treeview_df  = View_treeview_df.reset_index(drop=True)
                    windows = tk.Toplevel()
                    windows.title ("Excel View Only On Selected Entries")
                    windows.geometry('1600x755+40+40')
                    windows.config(bg="cadet blue")
                    frame = tk.Frame(windows)
                    frame.pack(fill=BOTH, expand=1)
                    pt = Table(frame, dataframe = View_treeview_df, showtoolbar=False, showstatusbar=False)
                    pt.setRowColors(rows=range(1,len(View_treeview_df),2), clr='lightblue', cols='all')
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
                else:
                    messagebox.showerror('Set And Catch Table Selection Message', "Void File... Nothing to View")
            else:
                tkinter.messagebox.showinfo("Set And Catch Table Selection Error","Please Select At least One Entries In the Table To Excel View")
        else:
            tkinter.messagebox.showinfo("Set And Catch Table Selection","Empty Set & Catch Table. Please Select At least One Entries In the Table To Excel View")
    
    def ImportSetCatchCSV_UpdateDB():
        ## Connection to SetCatch DB
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        entry_EntryDisplayMessageQC.delete(0,END)
        tree.delete(*tree.get_children())
        entry_EntryDisplayMessageQC.insert(tk.END,"Please Wait Updating CSV Import")

        def ImportColumnCheck(List_Columns_Import):
            ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
            ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
            DB_column_names = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 
                            'EstimatedWeightReleasedCrab', 'NumberIndividuals']
            if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
                return ReturnMatchedMessage
            else: 
                return ReturnMisMatchedMessage 

        def UpdateSetCatchDB(Raw_Imported_Df):
            try:
                Submit_To_DBStorage = pd.DataFrame(Raw_Imported_Df)
                Submit_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_Analysis_IMPORT', conn_DB_Set_Catch_Analysis, 
                                        if_exists="append",index = False)
                conn_DB_Set_Catch_Analysis.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn_DB_Set_Catch_Analysis:
                    cur_DB_Set_Catch_Analysis.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT\
                        WHERE rowid < (\
                        SELECT MAX(rowid) FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT p2  \
                        WHERE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT.DataBase_ID = p2.DataBase_ID\
                        AND DFO_NL_ASOP_Set_Catch_Analysis_IMPORT.RecordIdentifier = p2.RecordIdentifier\
                        )")
                    conn_DB_Set_Catch_Analysis.commit()

        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        Filename = filedialog.askopenfilenames(title="Select Set&Catch Updated CSV File", 
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
                        DataBase_ID                 = (df.loc[:,'DataBase_ID']).fillna(99999999).astype(int, errors='ignore')
                        RecordIdentifier            = (df.loc[:,'RecordIdentifier']).fillna(99999999).astype(int, errors='ignore')
                        DeploymentUID               = (df.loc[:,'DeploymentUID']).fillna(8888888).astype(int, errors='ignore')
                        ASOCCode                    = (df.loc[:,'ASOCCode']).fillna(99999999).astype(int, errors='ignore')
                        ObserverNumber              = (df.loc[:,'ObserverNumber']).fillna(8888888).astype(int, errors='ignore')
                        Year                        = (df.loc[:,'Year']).fillna(99999999).astype(int, errors='ignore')
                        DeploymentNumber            = (df.loc[:,'DeploymentNumber']).fillna(99999999).astype(int, errors='ignore')
                        SubTripNumber               = (df.loc[:,'SubTripNumber']).fillna(8888888).astype(int, errors='ignore')
                        SetNumber                   = (df.loc[:,'SetNumber']).fillna(99999999).astype(int, errors='ignore')
                        Country                     = (df.loc[:,'Country']).fillna(99999999).astype(int, errors='ignore')
                        Quota                       = (df.loc[:,'Quota']).fillna(99999999).astype(int, errors='ignore')
                        SetType                     = (df.loc[:,'SetType']).fillna(99999999).astype(int, errors='ignore')                
                        VesselSideNumber            = (df.loc[:,'VesselSideNumber']).fillna(8888888).astype(int, errors='ignore')
                        VesselClass                 = (df.loc[:,'VesselClass']).fillna(99999999).astype(int, errors='ignore')
                        VesselLength                = (df.loc[:,'VesselLength']).fillna(99999999).astype(float, errors='ignore')
                        VesselHorsepower            = (df.loc[:,'VesselHorsepower']).fillna(99999999).astype(int, errors='ignore')
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
                        NAFODivision                = (df.loc[:,'NAFODivision']).fillna(8888888).astype(int, errors='ignore')
                        UnitArea                    = (df.loc[:,'UnitArea']).fillna(8888888).astype(int, errors='ignore')
                        StatisticalArea             = (df.loc[:,'StatisticalArea']).fillna(99999999).astype(int, errors='ignore')
                        InOut200MileLimit           = (df.loc[:,'InOut200MileLimit']).fillna(99999999).astype(int, errors='ignore')
                        GearType                    = (df.loc[:,'GearType']).fillna(99999999).astype(int, errors='ignore')
                        CodendMeshSize              = (df.loc[:,'CodendMeshSize']).fillna(99999999).astype(int, errors='ignore')
                        MeshSizeMG                  = (df.loc[:,'MeshSizeMG']).fillna(99999999).astype(int, errors='ignore')
                        MeshSizeFG                  = (df.loc[:,'MeshSizeFG']).fillna(99999999).astype(int, errors='ignore')
                        RollerBobbbinDiameter       = (df.loc[:,'RollerBobbbinDiameter']).fillna(99999999).astype(int, errors='ignore')
                        NumberGillnets              = (df.loc[:,'NumberGillnets']).fillna(99999999).astype(int, errors='ignore')
                        AverageGillnetLength        = (df.loc[:,'AverageGillnetLength']).fillna(99999999).astype(int, errors='ignore')
                        GrateBarSpacing             = (df.loc[:,'GrateBarSpacing']).fillna(99999999).astype(int, errors='ignore')
                        FootropeLength              = (df.loc[:,'FootropeLength']).fillna(99999999).astype(int, errors='ignore')
                        NumberWindows               = (df.loc[:,'NumberWindows']).fillna(99999999).astype(int, errors='ignore')
                        NumberHooks                 = (df.loc[:,'NumberHooks']).fillna(99999999).astype(int, errors='ignore')
                        NumberPots                  = (df.loc[:,'NumberPots']).fillna(99999999).astype(int, errors='ignore')
                        NumberPotReleasedCrab       = (df.loc[:,'NumberPotReleasedCrab']).fillna(99999999).astype(int, errors='ignore')
                        GearDamage                  = (df.loc[:,'GearDamage']).fillna(99999999).astype(int, errors='ignore')
                        AverageTowSpeed             = (df.loc[:,'AverageTowSpeed']).fillna(99999999).astype(float, errors='ignore')
                        AverageDepth                = (df.loc[:,'AverageDepth']).fillna(99999999).astype(int, errors='ignore')
                        DataSource                  = (df.loc[:,'DataSource']).fillna(99999999).astype(int, errors='ignore')
                        DirectedSpecies             = (df.loc[:,'DirectedSpecies']).fillna(99999999).astype(int, errors='ignore')
                        NumberSpecies               = (df.loc[:,'NumberSpecies']).fillna(99999999).astype(int, errors='ignore')
                        RecordType                  = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                        DetailedCatchSpeciesCompCode= (df.loc[:,'DetailedCatchSpeciesCompCode']).fillna(8888888).astype(int, errors='ignore')
                        LogbookIDNumber1            = (df.loc[:,'LogbookIDNumber1']).fillna(99999999).astype(int, errors='ignore')
                        LogbookIDNumber2            = (df.loc[:,'LogbookIDNumber2']).fillna(99999999).astype(int, errors='ignore')
                        SpeciesCode                 = (df.loc[:,'SpeciesCode']).fillna(99999999).astype(int, errors='ignore')
                        KeptWeight                  = (df.loc[:,'KeptWeight']).fillna(99999999).astype(int, errors='ignore')
                        DiscardWeight               = (df.loc[:,'DiscardWeight']).fillna(99999999).astype(int, errors='ignore')
                        EstimatedWeightReleasedCrab = (df.loc[:,'EstimatedWeightReleasedCrab']).fillna(99999999).astype(int, errors='ignore')
                        NumberIndividuals           = (df.loc[:,'NumberIndividuals']).fillna(99999999).astype(int, errors='ignore')
                        column_names = [DataBase_ID, RecordIdentifier, DeploymentUID, ASOCCode, ObserverNumber, 
                                        Year, DeploymentNumber, SubTripNumber, SetNumber, Country, 
                                        Quota, SetType, VesselSideNumber, VesselClass, VesselLength, 
                                        VesselHorsepower, Day, Month, HaulDay, HaulMonth, 
                                        StartTime, Duration, PositionPrecision, StartLatitude, StartLongitude, 
                                        EndLatitude, EndLongitude, NAFODivision, UnitArea, StatisticalArea, 
                                        InOut200MileLimit, GearType, CodendMeshSize, MeshSizeMG, MeshSizeFG, 
                                        RollerBobbbinDiameter,NumberGillnets, AverageGillnetLength, GrateBarSpacing, FootropeLength, 
                                        NumberWindows, NumberHooks, NumberPots, NumberPotReleasedCrab, GearDamage, 
                                        AverageTowSpeed, AverageDepth, DataSource, DirectedSpecies, NumberSpecies, 
                                        RecordType, DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2, SpeciesCode, 
                                        KeptWeight, DiscardWeight, EstimatedWeightReleasedCrab, NumberIndividuals]
                        catdf = pd.concat (column_names,axis=1,ignore_index =True)
                        catdf.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 2:'DeploymentUID', 
                                            3:'ASOCCode', 4:'ObserverNumber', 5:'Year', 6:'DeploymentNumber', 7:'SubTripNumber', 
                                            8:'SetNumber', 9:'Country', 10:'Quota', 11:'SetType', 12:'VesselSideNumber', 
                                            13:'VesselClass', 14:'VesselLength', 15:'VesselHorsepower', 16:'Day', 17:'Month', 
                                            18:'HaulDay', 19:'HaulMonth', 20:'StartTime', 21:'Duration', 22:'PositionPrecision',
                                            23:'StartLatitude', 24:'StartLongitude', 25:'EndLatitude', 26:'EndLongitude', 27:'NAFODivision', 
                                            28:'UnitArea', 29:'StatisticalArea', 30:'InOut200MileLimit', 31:'GearType',
                                            32:'CodendMeshSize', 33:'MeshSizeMG', 34:'MeshSizeFG', 35:'RollerBobbbinDiameter', 36:'NumberGillnets',
                                            37:'AverageGillnetLength', 38:'GrateBarSpacing', 39:'FootropeLength', 40:'NumberWindows', 41:'NumberHooks',
                                            42:'NumberPots', 43:'NumberPotReleasedCrab', 44:'GearDamage', 45:'AverageTowSpeed', 46:'AverageDepth',
                                            47:'DataSource', 48:'DirectedSpecies', 49:'NumberSpecies', 50:'RecordType', 51:'DetailedCatchSpeciesCompCode',
                                            52:'LogbookIDNumber1', 53:'LogbookIDNumber2', 54:'SpeciesCode', 55:'KeptWeight', 56:'DiscardWeight', 
                                            57:'EstimatedWeightReleasedCrab', 58:'NumberIndividuals'},inplace = True)
                        Raw_Imported_Df = pd.DataFrame(catdf)
                        Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([99999999,'99999999'], '')
                        Raw_Imported_Df = Raw_Imported_Df.replace([8888888,'8888888'], 'None')
                        Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                        Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                        Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                        CheckEmptyNessColumn = Raw_Imported_Df[(Raw_Imported_Df.ASOCCode=='')|
                                                        (Raw_Imported_Df.Year=='') |
                                                        (Raw_Imported_Df.Country=='') |
                                                        (Raw_Imported_Df.Quota=='') |
                                                        (Raw_Imported_Df.SetType=='') |
                                                        (Raw_Imported_Df.SetNumber=='') |
                                                        (Raw_Imported_Df.DataBase_ID=='') |
                                                        (Raw_Imported_Df.RecordIdentifier=='') |
                                                        (Raw_Imported_Df.GearType=='') |
                                                        (Raw_Imported_Df.DataSource=='')|
                                                        (Raw_Imported_Df.DirectedSpecies=='')|
                                                        (Raw_Imported_Df.RecordType=='')|
                                                        (Raw_Imported_Df.PositionPrecision=='')|
                                                        (Raw_Imported_Df.Day=='')|
                                                        (Raw_Imported_Df.Month=='')|
                                                        (Raw_Imported_Df.VesselClass=='')|
                                                        (Raw_Imported_Df.UnitArea=='None')|
                                                        (Raw_Imported_Df.UnitArea=='')|
                                                        (Raw_Imported_Df.StartLatitude=='')|
                                                        (Raw_Imported_Df.StartLongitude=='')|
                                                        (Raw_Imported_Df.EndLatitude=='')|
                                                        (Raw_Imported_Df.EndLongitude=='')]
                        Len_CheckEmptyNessColumn =len(CheckEmptyNessColumn)
                        if Len_CheckEmptyNessColumn==0:
                            UpdateSetCatchDB(Raw_Imported_Df)
                            entry_EntryDisplayMessageQC.delete(0,END)
                            entry_EntryDisplayMessageQC.insert(tk.END,"Set & Catch Database Updated Successfully")
                            View_All_DB_SetCatchEntries()
                            tkinter.messagebox.showinfo("Update Success","Successfully Updated The Imported CSV Entries")
                        else:
                            messagebox.showerror('Empty Values In Variable', "Please Check The Empty Variables Values in Columns")
                            NoEmptyVarListMsgDisplay()                                
                    else:
                        messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
        cur_DB_Set_Catch_Analysis.close()
        conn_DB_Set_Catch_Analysis.close()

    def NoEmptyVarListMsgDisplay():
        ShowMSGroot = tk.Tk()
        ShowMSGroot.title ("No Empty Values In Variable Column List")
        ShowMSGroot.geometry("305x350+200+100")
        ShowMSGroot.config(bg="cadet blue")
        ShowMSGroot.resizable(0, 0)
        lbl_Header = Label(ShowMSGroot, font=('aerial', 11, 'bold'), text="Column List (No Empty Value) :")
        lbl_Header.pack()
        df = pd.DataFrame({'Variable Columns': ['DataBase_ID', 'RecordIdentifier',
                                'ASOCCode', 'Country/Quota'
                                'SetType', 'SetNumber',
                                'GearType', 'DataSource',
                                'RecordType', 'DirectedSpecies',
                                'PositionPrecision', 'Year/Day/Month',
                                'VesselClass', 'Start/End Lat-Lon',
                                'UnitArea'],
                        'Variable Presence': ['No Empty Value', 'No Empty Value',
                                                'No Empty Value', 'No Empty Value',
                                                'No Empty Value', 'No Empty Value',
                                                'No Empty Value', 'No Empty Value',
                                                'No Empty Value', 'No Empty Value',
                                                'No Empty Value', 'No Empty Value',
                                                'No Empty Value', 'No Empty/None Value',]})
        df = pd.DataFrame(df)
        List_Columns = list(df.columns)
        ViewTreeMsg = ttk.Treeview(ShowMSGroot, height=15)
        ViewTreeMsg.pack()
        ViewTreeMsg['column'] = List_Columns
        ViewTreeMsg['show'] = "headings"
        for col in ViewTreeMsg['column']:
            ViewTreeMsg.heading(col, text=col, anchor = 'w')
            ViewTreeMsg.column(col, width=150, anchor = 'w')
        for row in df.to_numpy().tolist():
            ViewTreeMsg.insert("","end", values =row)
        ShowMSGroot.mainloop()

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
        View_All_DB_SetCatchEntries()
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    def SelectCopyNAddDB():
        if len(tree.get_children())>0:
            cur_id = tree.focus()
            selvalue = tree.item(cur_id)['values']
            Length_Selected  =  (len(selvalue))
            if Length_Selected != 0:
                SelectionTree = tree.selection()
                row_list = []
                Treeviewcolumns  = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
                for row in SelectionTree:
                    row_list.append(tree.item(row)["values"])
                treeview_df = pd.DataFrame(row_list, columns = Treeviewcolumns)
                Complete_df = treeview_df.iloc[:, 3:len((Treeviewcolumns))]
                Complete_df = Complete_df.replace('None', '')
                if len(Complete_df) >0:
                    Copy_treeview_df  = pd.DataFrame(Complete_df)
                    Copy_treeview_df  = Copy_treeview_df.reset_index(drop=True)
                    ViewSelectCopyNAddDBEntries(Copy_treeview_df)
                else:
                    messagebox.showerror('Copy Error : Set And Catch Table Selection Message', "Void File... Nothing to Copy")
            else:
                tkinter.messagebox.showinfo("Set And Catch Table Selection Error","Please Select At least One Entries In the Table To Copy")
        else:
            tkinter.messagebox.showinfo("Set And Catch Table Selection","Empty Set & Catch Table. Please Select At least One Entries In the Table To Copy")

    def ViewSelectCopyNAddDBEntries(Copy_treeview_df):
        root1=tk.Tk()
        root1.title ("Selected View DFO-NL-ASOP Observer QC Database")
        root1.geometry('1450x310+40+40')
        root1.config(bg="cadet blue")
        Tableframe = Frame(root1, width = 40)
        Tableframe.pack(side = TOP, padx= 0, pady=0)
        tree1 = ttk.Treeview(Tableframe, height=6)
        scrollbary = ttk.Scrollbar(Tableframe, orient ="vertical", command=tree1.yview)
        scrollbary.pack(side ='right', fill ='y')
        tree1.configure(yscrollcommand = scrollbary.set)
        scrollbarx = ttk.Scrollbar(Tableframe, orient ="horizontal", command=tree1.xview)
        scrollbarx.pack(side ='bottom', fill ='x')
        tree1.configure(xscrollcommand = scrollbarx.set)
        style = ttk.Style(root1)
        style.theme_use('clam')
        style.configure(".", font=('aerial', 8), foreground="blue")
        style.configure("Treeview", foreground='black')
        style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                        background='Ghost White',
                        foreground='blue',fieldbackground='Ghost White')
        tree1.pack(side = TOP)
        
        ProcedureFrame = Frame(root1, width = 40,  bg= "cadet blue")
        ProcedureFrame.pack(side = LEFT, padx= 0, pady=0)
        lbl_AddStepProcess = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                bg= "cadet blue", text="Procedure To Edit Cell & Update Value & Add Entries To DB ")
        lbl_AddStepProcess.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

        lbl_AddEntriesDBStep1 = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                bg= "cadet blue", text="1 : Double Click On TreeView Cell Value For Edit")
        lbl_AddEntriesDBStep1.grid(row =2, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

        lbl_AddEntriesDBStep2 = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                bg= "cadet blue", text="2 : After Edit Press Enter (Must) To Modify  Cell Value ")
        lbl_AddEntriesDBStep2.grid(row =4, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

        lbl_AddEntriesDBStep3 = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                bg= "cadet blue", text="3 : Submit Edited Entries (Add) To Set & Catch QC Databse ")
        lbl_AddEntriesDBStep3.grid(row =6, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

        List_Columns = list(Copy_treeview_df.columns)
        tree1['column'] = List_Columns
        tree1['show'] = "headings"
        for col in tree1['column']:
            tree1.heading(col, text=col, anchor = tk.CENTER)
            tree1.column(col, stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
        df_rows = Copy_treeview_df.to_numpy().tolist()
        countIndex = 0
        for row in df_rows:
            if countIndex % 2 == 0:
                tree1.insert("", "end", values =row, tags =("even",))
            else:
                tree1.insert("", "end", values =row, tags =("odd",))
            countIndex = countIndex+1
        tree1.tag_configure("even",foreground="black", background="lightblue")
        tree1.tag_configure("odd",foreground="black", background="ghost white")

        def on_double_click(event):
            regioin_click = tree1.identify_region(event.x, event.y)
            if regioin_click not in ("tree", "cell"):
                return
            column = tree1.identify_column(event.x)
            column_index = int(column[1:]) -1
            selected_iid = tree1.focus()
            selected_values = tree1.item(selected_iid)
            cellValue = selected_values.get("values")[column_index]
            column_box = tree1.bbox(selected_iid, column)
            entry_edit = ttk.Entry(root1, width =column_box[2])
            entry_edit.place(x=column_box[0],
                             y=column_box[1],
                             w=column_box[2],
                             h=column_box[3])
            entry_edit.editing_column_index = column_index
            entry_edit.editing_item_iid = selected_iid
            entry_edit.insert(0, cellValue)
            entry_edit.select_range(0, tk.END)
            entry_edit.focus()

            def on_enter_pressed(event):
                new_text = event.widget.get()
                selected_iid = event.widget.editing_item_iid
                column_index = event.widget.editing_column_index
                if column_index ==-1:
                    tree1.item(selected_iid, text = new_text)
                else:
                    current_values = tree1.item(selected_iid).get("values")
                    current_values[column_index] = new_text
                    tree1.item(selected_iid, values = current_values)
                event.widget.destroy()

            def on_focus_out(event):
                event.widget.destroy()

            entry_edit.bind("<FocusOut>", on_focus_out)
            entry_edit.bind("<Return>", on_enter_pressed)
        
        def AddedEntries_To_DBStorage(AddedComplete_df):
            try:
                AddedEntriesDF = pd.DataFrame(AddedComplete_df)
                sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = sqliteConnection.cursor()
                AddedEntriesDF.to_sql('DFO_NL_ASOP_Set_Catch_Analysis_IMPORT', sqliteConnection,
                                       if_exists="append", index = False, index_label='DataBase_ID')
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def GetSetCatchEndID():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df_DBID = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                Complete_df_RecID = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `RecordIdentifier` ASC ;", conn)

                Complete_df_DBID  = pd.DataFrame(Complete_df_DBID)
                Complete_df_DBID  = Complete_df_DBID.reset_index(drop=True)
                Complete_df_DBID  = pd.DataFrame(Complete_df_DBID)
                GetSetCatchEndDBID = Complete_df_DBID['DataBase_ID'].iloc[-1]
            
                Complete_df_RecID  = pd.DataFrame(Complete_df_RecID)
                Complete_df_RecID  = Complete_df_RecID.reset_index(drop=True)
                Complete_df_RecID  = pd.DataFrame(Complete_df_RecID)
                GetSetCatchEndRecID = Complete_df_RecID['RecordIdentifier'].iloc[-1]
                return GetSetCatchEndDBID, GetSetCatchEndRecID
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        def SubmitToAddEntries():
            tree.delete(*tree.get_children())
            entry_Total_DBEntries.delete(0,END)
            GetSetCatchDB_Columns = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
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
            dfList =[] 
            for child in tree1.get_children():
                df = tree1.item(child)["values"]
                dfList.append(df)
            getTreeView_DataFrame = pd.DataFrame(dfList)
            getTreeView_DataFrame.columns = GetSetCatchDB_Columns
            Complete_df = pd.DataFrame(getTreeView_DataFrame)
            if len(Complete_df) >0:
                    AddedComplete_df  = pd.DataFrame(Complete_df)
                    AddedComplete_df  = AddedComplete_df.reset_index(drop=True)
                    Len_AddedComplete_df = len(AddedComplete_df)
                    AddedComplete_df['DeploymentUID'] = AddedComplete_df["Year"].map(str) + "-" + \
                                                    AddedComplete_df["ASOCCode"].map(str)+ "-" +\
                                                    AddedComplete_df["DeploymentNumber"].map(str)+"-"+ \
                                                    AddedComplete_df["SetNumber"].map(str)
                    AddedComplete_df = AddedComplete_df[['DeploymentUID'] + [x for x in AddedComplete_df.columns if x != 'DeploymentUID']]
                    
                    ReceiveSetCatchEndID = GetSetCatchEndID()
                    GetSetCatchEndDBID = int(ReceiveSetCatchEndID[0])
                    GetSetCatchEndRecID = int(ReceiveSetCatchEndID[1])

                    RecordIdentifier_Get    = GetSetCatchEndRecID + 1
                    RecordIdentifier_Offset = 5
                    AddedComplete_df.insert(loc=0, column="RecordIdentifier", 
                    value = (np.arange(RecordIdentifier_Get, Len_AddedComplete_df + RecordIdentifier_Get) + RecordIdentifier_Offset))

                    DataBase_ID_Get        = GetSetCatchEndDBID + 1
                    DataBase_ID_Get_Offset = 5
                    AddedComplete_df.insert(loc=0, column="DataBase_ID", 
                    value = (np.arange(DataBase_ID_Get, Len_AddedComplete_df + DataBase_ID_Get)+DataBase_ID_Get_Offset))
                    
                    AddedComplete_df  = AddedComplete_df.reset_index(drop=True)
                    AddedComplete_df  = pd.DataFrame(AddedComplete_df)
                    AddedEntries_To_DBStorage(AddedComplete_df)
                    root1.destroy()  
            else:
                messagebox.showerror('Empty treeView', "Void treeview... ")

        tree1.bind("<Double-1>", on_double_click)
        button_SubmitToAddDB = Button(ProcedureFrame, bd = 2, text ="Submit To Add Entries", width =22,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =SubmitToAddEntries)
        button_SubmitToAddDB.grid(row =8, column = 0, padx=20, pady =1, ipady =1, sticky =W)

    def on_double_click(event):
        regioin_click = tree.identify_region(event.x, event.y)
        if regioin_click not in ("tree", "cell"):
            return
        column = tree.identify_column(event.x)
        column_index = int(column[1:]) -1
        selected_iid = tree.focus()
        selected_values = tree.item(selected_iid)
        cellValue = selected_values.get("values")[column_index]
        column_box = tree.bbox(selected_iid, column)
        entry_edit = ttk.Entry(Tableframe, width =column_box[2])
        entry_edit.place(x=column_box[0],
                            y=column_box[1],
                            w=column_box[2],
                            h=column_box[3])
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid
        entry_edit.insert(0, cellValue)
        entry_edit.select_range(0, tk.END)
        entry_edit.focus()

        def on_enter_pressed(event):
            new_text = event.widget.get()
            selected_iid = event.widget.editing_item_iid
            column_index = event.widget.editing_column_index
            if column_index ==-1:
                tree.item(selected_iid, text = new_text)
            else:
                current_values = tree.item(selected_iid).get("values")
                current_values[column_index] = new_text
                tree.item(selected_iid, values = current_values)
            event.widget.destroy()

        def on_focus_out(event):
            event.widget.destroy()

        entry_edit.bind("<FocusOut>", on_focus_out)
        entry_edit.bind("<Return>", on_enter_pressed)

    def ApplyTreeViewTableToDBAfterEdit():
        GetSetCatchDB_Columns = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
        getTreeView_DataFrame = TreeView_DataFrame() 
        getTreeViewTotalEntriesDF = getTreeView_DataFrame[0]
        getTreeViewTotalEntries = int(getTreeView_DataFrame[1])
        getDBTotalEntries = int(entry_Total_DBEntries.get())
        if getTreeViewTotalEntries >= getDBTotalEntries:
            getTreeViewTotalEntriesDF.columns = GetSetCatchDB_Columns
            Complete_df = pd.DataFrame(getTreeViewTotalEntriesDF)
            if len(Complete_df) >0:
                iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                        "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                if iSubmit >0:
                    Complete_df  = pd.DataFrame(Complete_df)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = Complete_df.iloc[:, 1:len(list(Complete_df.columns))]
                    try:
                        sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                        cursor = sqliteConnection.cursor()
                        data = pd.DataFrame(Complete_df)
                        data = data.reset_index(drop=True)
                        data.to_sql('DFO_NL_ASOP_Set_Catch_Analysis_IMPORT', sqliteConnection, if_exists="replace",index_label='DataBase_ID')
                        sqliteConnection.commit()
                    except sqlite3.Error as error:
                        print('Error occured - ', error)
                    finally:
                        if sqliteConnection:
                            cursor.close()
                            sqliteConnection.close()
                            View_All_DB_SetCatchEntries()
                            tkinter.messagebox.showinfo("Update Success","Successfully Update The Set & Catch Database")
            else:
                messagebox.showerror('Empty TreeView Table : Set And Catch QC Database Profile Message', "Void Table")
        else:
            messagebox.showerror('Error in DB Update', "Table Must Be With All Entries From DB")

    def SortView_DeploymentUID():
        GetSetCatchDB_Columns = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
        getTreeView_DataFrame = TreeView_DataFrame()
        getExportSearchQueryResults = getTreeView_DataFrame[0]
        getExportSearchQueryResults.columns = GetSetCatchDB_Columns
        Complete_df = pd.DataFrame(getExportSearchQueryResults)
        Complete_df.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber','SetNumber',
                                                    'RecordType'], inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        Complete_df  = pd.DataFrame(Complete_df)
        if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                List_Columns = list(SetCatchProfileDB_DF.columns)
                ClearView_DBEntries()
                tree['column'] = List_Columns
                tree['show'] = "headings"
                for col in tree['column']:
                    if (col == 'DataBase_ID')|(col == 'RecordIdentifier'):
                        tree.heading(col, text=col, anchor = tk.CENTER)
                        tree.column(col, stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
                    else:
                        tree.heading(col, text=col, anchor = tk.CENTER)
                        tree.column(col, stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
                df_rows = SetCatchProfileDB_DF.to_numpy().tolist()
                countIndex = 0
                for row in df_rows:
                    if countIndex % 2 == 0:
                        tree.insert("", "end", values =row, tags =("even",))
                    else:
                        tree.insert("", "end", values =row, tags =("odd",))
                    countIndex = countIndex+1
                tree.tag_configure("even",foreground="black", background="lightblue")
                tree.tag_configure("odd",foreground="black", background="ghost white")
                Length_ObserverSetCatchDB = len(SetCatchProfileDB_DF)
                entry_Total_DBEntries.delete(0,END)
                entry_Total_DBEntries.insert(tk.END,Length_ObserverSetCatchDB)
                tkinter.messagebox.showinfo("Sorting Success","Successfully Sorted By DeploymentUID")

    def SortView_DataBase_ID():
        GetSetCatchDB_Columns = ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID',
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
        getTreeView_DataFrame = TreeView_DataFrame() 
        getExportSearchQueryResults = getTreeView_DataFrame[0]
        getExportSearchQueryResults.columns = GetSetCatchDB_Columns
        Complete_df = pd.DataFrame(getExportSearchQueryResults)
        Complete_df.sort_values(by=['DataBase_ID', 'RecordIdentifier'], inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        Complete_df  = pd.DataFrame(Complete_df)   
        if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                List_Columns = list(SetCatchProfileDB_DF.columns)
                ClearView_DBEntries()
                tree['column'] = List_Columns
                tree['show'] = "headings"
                for col in tree['column']:
                    if (col == 'DataBase_ID')|(col == 'RecordIdentifier'):
                        tree.heading(col, text=col, anchor = tk.CENTER)
                        tree.column(col, stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
                    else:
                        tree.heading(col, text=col, anchor = tk.CENTER)
                        tree.column(col, stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
                df_rows = SetCatchProfileDB_DF.to_numpy().tolist()
                countIndex = 0
                for row in df_rows:
                    if countIndex % 2 == 0:
                        tree.insert("", "end", values =row, tags =("even",))
                    else:
                        tree.insert("", "end", values =row, tags =("odd",))
                    countIndex = countIndex+1
                tree.tag_configure("even",foreground="black", background="lightblue")
                tree.tag_configure("odd",foreground="black", background="ghost white")
                Length_ObserverSetCatchDB = len(SetCatchProfileDB_DF)
                entry_Total_DBEntries.delete(0,END)
                entry_Total_DBEntries.insert(tk.END,Length_ObserverSetCatchDB)
                tkinter.messagebox.showinfo("Sorting Success","Successfully Sorted By DatabaseID")

    ## Define TreeView Binding And Event Selection
    tree.bind('<<TreeviewSelect>>',InventoryRec)
    tree.bind('<ButtonRelease-1>',InventoryRec1)
    tree.bind("<Double-1>", on_double_click)
    entry_UpdateVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable1)
    entry_SearchVariableList.bind('<<ComboboxSelected>>',callbackFuncSelectVariable2)

    ### Buttons On Topframe
    button_Total_DBEntries = Button(Topframe, bd = 2, text ="Total DB Entries", width = 14,
                                height=1, font=('aerial', 10, 'bold'), 
                                fg="blue", bg="aliceblue",
                                command =SetAndCatchDBTotalEntries)
    button_Total_DBEntries.grid(row =0, column = 2, padx=1, pady =2)

    button_ClearView_DBEntries = Button(Topframe, bd = 2, text ="Clear View", width = 10,
                                        height=1, font=('aerial', 10, 'bold'),
                                        fg="blue", bg="aliceblue", 
                                        command =ClearView_DBEntries)
    button_ClearView_DBEntries.grid(row =0, column = 3, padx=1, pady =2)

    button_Populate_DBEntries = Button(Topframe, bd = 2, text ="Populate Set & Catch QC Database", width = 28,
                                height=1, font=('aerial', 10, 'bold'), 
                                fg="blue", bg="aliceblue",
                                command =View_All_DB_SetCatchEntries)
    button_Populate_DBEntries.grid(row =0, column = 4, padx=1, pady =2)

    button_ViewSelectedColumns = Button(Topframe, bd = 2, text ="View Selected Columns", width = 22,
                                            height=1, font=('aerial', 10, 'bold'), fg="blue", bg="aliceblue", 
                                            command =RunSelCols_SetAndCatchDB)
    button_ViewSelectedColumns.grid(row =0, column = 5, padx=2, pady =1, ipady =1, sticky =W)

    button_ExportSearchQueryResults = Button(Topframe, bd = 2, text ="Export Search Results", width = 18,
                                            height=1, font=('aerial', 10, 'bold'), fg="blue", bg="aliceblue", 
                                            command =ExportSearchQueryResults)
    button_ExportSearchQueryResults.grid(row =0, column = 6, padx=2, pady =1, ipady =1, sticky =W)

    button_ViewSearchQueryResults = Button(Topframe, bd = 2, text ="View Search Results", width = 18,
                                            height=1, font=('aerial', 10, 'bold'), fg="blue", bg="aliceblue", 
                                            command =ViewSearchQueryResults)
    button_ViewSearchQueryResults.grid(row =0, column = 9, padx=3, pady =1, ipady =1, sticky =W)

    ### Buttons On Update Frame
    button_ExportTreeViewSelectionCSV = Button(UpdateDB_Entryframe, bd = 2, text ="Export To CSV", width = 12,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ExportTreeViewSelectionCSV)
    button_ExportTreeViewSelectionCSV.grid(row =8, column = 1, padx=10, pady =2, ipady =1, sticky =E)

    button_UpdateSelectedDBEntries = Button(UpdateDB_Entryframe, bd = 2, text ="Update Selected Table Entries\n (DB Update)", width = 25,
                                height=2, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =UpdateSelected_SetCatch_DBEntries)
    button_UpdateSelectedDBEntries.grid(row =14, column = 0, padx=10, pady =1, ipady =1, sticky =W)

    button_Clear_EntriesUpdate = Button(UpdateDB_Entryframe, bd = 2, text ="Clear Entries", width = 11,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =Clear_EntriesUpdate)
    button_Clear_EntriesUpdate.grid(row =2, column = 1, padx=15, pady =2, ipady =1, sticky =E)

    button_UpdateCSVImportedDBEntries = Button(UpdateDB_Entryframe, bd = 2, text ="Update Imported CSV Entries\n (DB Update)", width = 25,
                                height=2, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ImportSetCatchCSV_UpdateDB)
    button_UpdateCSVImportedDBEntries.grid(row =14, column = 1, padx=10, pady =1, ipady =1, sticky =W)

    ### Buttons On Search Frame
    button_SearchSingleVariableQuery = Button(SearchDB_Entryframe, bd = 2, text ="Run Single Variable Search ", width = 24,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunSingleVariableSearchQuery)
    button_SearchSingleVariableQuery.grid(row =14, column = 0, padx=30, pady =1, ipady =1, sticky =W)

    button_BuildMultiSearchQuery = Button(SearchDB_Entryframe, bd = 2, text ="Build Multi Search Query ", width = 24,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =BuildMultiSearchQuery)
    button_BuildMultiSearchQuery.grid(row =6, column = 1, padx=80, pady =2, ipady =1, sticky =W)

    button_ViewMultiSearchResults = Button(SearchDB_Entryframe, bd = 2, text ="Run Multi Variable Search ", width = 24,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunMultiVariableSearchQuery)
    button_ViewMultiSearchResults.grid(row =8, column = 1, padx=80, pady =2, ipady =1, sticky =W)

    button_SearchTextualVariableQuery = Button(SearchDB_Entryframe, bd = 2, text ="Run Textual Variable Search ", width = 24,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunTextualVariableSearchQuery)
    button_SearchTextualVariableQuery.grid(row =14, column = 1, padx=80, pady =2, ipady =1, sticky =W)

    button_SearchClearEntries = Button(SearchDB_Entryframe, bd = 2, text ="Clear Search", width = 11,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =Clear_EntriesSearch)
    button_SearchClearEntries.grid(row =14, column = 1, padx=5, pady =2, ipady =1, sticky =E)

    ### Buttons SelectCopyNAdd Frame
    button_SelectCopyNAdd = Button(MiscCommandframe, bd = 2, text ="Select-Edit & Add DB Entries", width =24,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =SelectCopyNAddDB)
    button_SelectCopyNAdd.grid(row =4, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    button_SelectCopyNDelete = Button(MiscCommandframe, bd = 2, text ="Delete Selected DB Entries", width =24,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =DeleteSelectedEntries)
    button_SelectCopyNDelete.grid(row =8, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    button_UpdateCellValueDB = Button(MiscCommandframe, bd = 2, text =" Apply LogTable To UpdateDB", width =24,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ApplyTreeViewTableToDBAfterEdit)
    button_UpdateCellValueDB.grid(row =12, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    ## Adding File Menu
    if Return_ObserverSetCatchDB !=None:
        menu = Menu(root)
        root.config(menu=menu)
        filemenu  = Menu(menu, tearoff=0)
        exportmenu  = Menu(menu, tearoff=0)
        updatemenu  = Menu(menu, tearoff=0)
        
        menu.add_cascade(label="File", menu=filemenu)
        menu.add_cascade(label="Export", menu=exportmenu)
        menu.add_cascade(label="Update", menu=updatemenu)

        filemenu.add_command(label="Exit Set & Catch QC Database Viewer", command=RootExit)
        
        exportmenu.add_command(label="Export Set & Catch QC Database", command=ExportSetAndCatch_QC_DB)
        exportmenu.add_command(label="Export Set & Catch Populated Entries", command=ExportSetAndCatch_PopulatedEntries)

        updatemenu.add_command(label="Update DeploymentUID After Year/ASOCCode/DeploymentNumber/SetNumber Updates", command=UpdateDeploymentUIDAfterUpdate)

        Treepopup.add_command(label="Delete Seleted Entries from DB", command=DeleteSelectedEntries)
        Treepopup.add_command(label="Delete Seleted Set from DB", command=DeleteSelectedSet)
        Treepopup.add_command(label="Export Selected Entries In CSV", command=ExportTreeViewSelectionCSV)
        Treepopup.add_command(label="Excel View Only On Selected Entries", command=ExcelViewTreeViewSelection)
        
        Treepopup.add_command(label="Set&Catch Log Table Sort By DeploymentUID", command=SortView_DeploymentUID)
        Treepopup.add_command(label="Set&Catch Log Table Sort By DatabaseID", command=SortView_DataBase_ID)
        
        Treepopup.add_separator()
        Treepopup.add_command(label="System Exit", command=iExit)
        tree.bind("<Button-3>", Treepopup_do_popup)
        tree.pack()
    root.mainloop()



