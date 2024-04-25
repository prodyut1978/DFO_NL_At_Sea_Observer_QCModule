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

## Database connections
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
Path_CSV_VariablesRangeFile = './External_Import/VariablesRangeTable_Import/CSV_RangeVariables_ValidationTable/DFO_NL_ASOP_RangeVariables_ValidationTable.csv'

def ViewRangeValidatedResult_CatchVariables():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Range Validator - ID-C-02-1")
    window.geometry("1420x825+200+100")
    window.config(bg="cadet blue")
    window.resizable(0, 0)
    ## Catch Variables Limit Fetching
    def fetchData_RangeLimitVariables():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_RangeLimitVariables_Define ORDER BY `VariablesID` ASC ;", conn)
            return Complete_df
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()
    Get_RangeLimitVariables = fetchData_RangeLimitVariables()
   # RecordType
    RecordType_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[18,'LowerRangeLimitValue'])
    RecordType_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[18,'UpperRangeLimitValue'])
    RecordType_QCNullValue= Get_RangeLimitVariables.at[18,'QCNullValue']
    #AverageTowSpeed
    AverageTowSpeed_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[17,'LowerRangeLimitValue'])
    AverageTowSpeed_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[17,'UpperRangeLimitValue'])
    AverageTowSpeed_QCNullValue= Get_RangeLimitVariables.at[17,'QCNullValue']
    #KeptWeight
    KeptWeight_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[19,'LowerRangeLimitValue'])
    KeptWeight_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[19,'UpperRangeLimitValue'])
    KeptWeight_QCNullValue= Get_RangeLimitVariables.at[19,'QCNullValue']
    # DiscardWeight
    DiscardWeight_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[20,'LowerRangeLimitValue'])
    DiscardWeight_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[20,'UpperRangeLimitValue'])
    DiscardWeight_QCNullValue= Get_RangeLimitVariables.at[20,'QCNullValue']
    # NumberIndividuals
    NumberIndividuals_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[21,'LowerRangeLimitValue'])
    NumberIndividuals_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[21,'UpperRangeLimitValue'])
    NumberIndividuals_QCNullValue= Get_RangeLimitVariables.at[21,'QCNullValue']
    # NumberWindows
    NumberWindows_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[22,'LowerRangeLimitValue'])
    NumberWindows_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[22,'UpperRangeLimitValue'])
    NumberWindows_QCNullValue= Get_RangeLimitVariables.at[22,'QCNullValue']

    ## Top Main Frame
    TopMainFrame = Frame(window, bd = 2, padx= 1, pady= 1, relief = RIDGE)
    TopMainFrame.grid(row =0, column = 0, padx=1, pady =1, sticky =W, rowspan =1)

    ## Top Left Frame - Catch profile
    TopLeftframe = Frame(TopMainFrame, bd = 1, padx= 1, pady= 1, relief = RIDGE)
    TopLeftframe.grid(row =0, column = 0, padx=1, pady =1, sticky =W, rowspan =1, columnspan =1)
    DataBase_ID       = IntVar(TopLeftframe, value='')
    RecordIdentifier  = IntVar(TopLeftframe, value='')
    DeploymentUID     = StringVar(TopLeftframe)
    AverageTowSpeed  = IntVar(TopLeftframe, value='')
    KeptWeight  = IntVar(TopLeftframe, value='')
    DiscardWeight  = IntVar(TopLeftframe, value='')
    NumberIndividuals  = IntVar(TopLeftframe, value='')
    NumberWindows  = IntVar(TopLeftframe, value='')
    
    lblTitEntry = Label(TopLeftframe, font=('aerial', 11, 'bold'), text=" Variable Profile & Update : ")
    lblTitEntry.grid(row =0, column = 0, padx=0, pady =1, sticky =W, rowspan =1)

    lblDeploymentUID = Label(TopLeftframe, font=('aerial', 10, 'bold'), text = "0. DeploymentUID :", padx =0, pady= 2)
    lblDeploymentUID.grid(row =2, column = 0, padx=4, pady =2, sticky =W)
    txtDeploymentUID  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable = DeploymentUID, state=DISABLED, width = 18)
    txtDeploymentUID.grid(row =3, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblAverageTowSpeedCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), 
    text = ("1. AverageTowSpeed :" + ' ('+ str(AverageTowSpeed_LowerRangeLimitValue) + " - " + str(AverageTowSpeed_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblAverageTowSpeedCode.grid(row =4, column = 0, padx=4, pady =2, sticky =W)
    txtAverageTowSpeed  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= AverageTowSpeed, width = 18)
    txtAverageTowSpeed.grid(row =5, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblKeptWeightCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), 
    text = ("2. KeptWeight :" + ' (' + str(KeptWeight_LowerRangeLimitValue) + " - " + str(KeptWeight_UpperRangeLimitValue) + ')'),
    padx =0, pady= 2)
    lblKeptWeightCode.grid(row =6, column = 0, padx=0, pady =2, sticky =W)
    txtKeptWeight  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= KeptWeight, width = 18)
    txtKeptWeight.grid(row =7, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblDiscardWeightCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), 
    text = ("3. DiscardWeight :" + ' ('+ str(DiscardWeight_LowerRangeLimitValue) + " - " + str(DiscardWeight_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblDiscardWeightCode.grid(row =8, column = 0, padx=4, pady =2, sticky =W)
    txtDiscardWeight  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= DiscardWeight, width = 18)
    txtDiscardWeight.grid(row =9, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblNumberIndividualsCode = Label(TopLeftframe, font=('aerial', 10, 'bold'),
    text = ("4. NumberIndividuals :" + ' ('+ str(NumberIndividuals_LowerRangeLimitValue) + " - " + str(NumberIndividuals_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblNumberIndividualsCode.grid(row =10, column = 0, padx=4, pady =2, sticky =W)
    txtNumberIndividuals  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= NumberIndividuals, width = 18)
    txtNumberIndividuals.grid(row =11, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblNumberWindowsCode = Label(TopLeftframe, font=('aerial', 10, 'bold'),
    text = ("5. NumberWindows :" + ' ('+ str(NumberWindows_LowerRangeLimitValue) + " - " + str(NumberWindows_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblNumberWindowsCode.grid(row =12, column = 0, padx=4, pady =2, sticky =W)
    txtNumberWindows  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= NumberWindows, width = 18)
    txtNumberWindows.grid(row =13, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    ### Fail Count
    lbl_TotalFailedEntries = Label(TopLeftframe, font=('aerial', 9 , 'bold'), text="Total QC Failed Entries :")
    lbl_TotalFailedEntries.grid(row =16, column = 0, padx=2, pady =1, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(TopLeftframe, value='')
    txtTotalFailedEntries = Entry(TopLeftframe, font=('aerial',9),textvariable = TotalFailedEntries, width = 8, bd=1)
    txtTotalFailedEntries.grid(row =17, column = 0, padx=60, pady =1, ipady =1, sticky =W)

    lbl_SelectedFailedEntries = Label(TopLeftframe, font=('aerial', 10, 'bold'), text="Selected QC Failed Entries :")
    lbl_SelectedFailedEntries.grid(row =18, column = 0, padx=2, pady =1, ipady=2, sticky =W)
    SelectedFailedEntries = IntVar(TopLeftframe, value='')
    txtSelectedFailedEntries = Entry(TopLeftframe, font=('aerial', 9),textvariable = SelectedFailedEntries, width = 8, bd=2)
    txtSelectedFailedEntries.grid(row =19, column = 0, padx=60, pady =1, ipady =1, sticky =W)

    # Frame Of Update modules
    UpdateDB_Entryframe = tk.Frame(TopLeftframe, bd = 2,relief = RIDGE)
    UpdateDB_Entryframe.grid(row =21, column = 0, padx=2, pady =2, ipady =5, sticky =W)

    lbl_UpdateDB_Header = Label(UpdateDB_Entryframe, font=('aerial', 11, 'bold'),
                                 text="Update Selected Entries:")
    lbl_UpdateDB_Header.grid(row =2, column = 0, columnspan=1 ,padx=1, pady =2, sticky =W)

    lbl_SelectTableEntries = Label(UpdateDB_Entryframe, font=('aerial', 9, 'bold'),
                                             text=" 1. Select : ")
    lbl_SelectTableEntries.grid(row =4, column = 0, padx=1, pady =1, sticky =W)

    NumberRowSelected       = IntVar(UpdateDB_Entryframe, value =' #Of Tab-B Entries')
    entry_NumberRowSelected = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), justify='center',
                                textvariable = NumberRowSelected, width = 15, bd=1)
    entry_NumberRowSelected.grid(row =4, column = 0, padx=65, pady =1, ipady =1, sticky =W)
   

    lbl_Select_List_Variable = Label(UpdateDB_Entryframe, font=('aerial', 9, 'bold'),
                                     text=" 2. Select Variable To Update:")
    lbl_Select_List_Variable.grid(row =6, column = 0, padx=1, pady =2, sticky =W)
    
    ListVariableListA = ['RecordType', 'AverageTowSpeed', 'KeptWeight', 
                         'DiscardWeight', 'NumberIndividuals', 'NumberWindows']
    VariableListA        = StringVar(UpdateDB_Entryframe, value ='')
    entry_UpdateVariableList  = ttk.Combobox(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), 
                                        textvariable = VariableListA, width = 20, state='readonly')
    entry_UpdateVariableList.grid(row =8, column = 0, padx=15, pady =1, ipady= 1, sticky =W)
    entry_UpdateVariableList['values'] = (list(ListVariableListA))

    lbl_EntryUpdate_Variable = Label(UpdateDB_Entryframe, font=('aerial', 10, 'bold'),
                                   text=" 3. Enter Updated Value :")
    lbl_EntryUpdate_Variable.grid(row =10, column = 0, padx=1, pady =1, sticky =W)
    
    UpdateValue_VariableA       = IntVar(UpdateDB_Entryframe, value ='')
    entry_UpdateValue_VariableA = Entry(UpdateDB_Entryframe, font=('aerial', 8, 'bold'), 
                                        textvariable = UpdateValue_VariableA, width = 22, bd=1)
    entry_UpdateValue_VariableA.grid(row =12, column = 0, padx=15, pady =1, ipady =1, sticky =W)

    ## Top Right Frame
    TopRightframe = Frame(TopMainFrame, bd = 1, padx= 5, pady= 1, relief = RIDGE)
    TopRightframe.grid(row =0, column = 3, padx=2, pady =1, sticky =W, rowspan =1)
    ## Table A: QC Display Table:
    lbl_QCDisplay = Label(TopRightframe, font=('aerial', 11, 'bold'), text="A: QC Message Display")
    lbl_QCDisplay.grid(row =0, column = 0, padx=0, pady =2, ipady=2, sticky =W)
    txtDisplayMessageSystem = Entry(TopRightframe, font=('aerial', 11),justify='center',
                            textvariable = StringVar(window, value='System Display'), width = 100, bd=3)
    txtDisplayMessageSystem.grid(row =0, column = 0, padx=180, pady =2, ipady =5, sticky =W)
    ## Define tree0
    TableMargin0 = Frame(TopRightframe, bd = 2, padx= 3, pady= 1, relief = RIDGE)
    TableMargin0.grid(row =1, column = 0, padx=1, pady =1, sticky =W, rowspan =1)
    tree0 = ttk.Treeview(TableMargin0, 
            column=("column1", "column2", "column3","column4", "column5", "column6"), 
            height=1, show='headings')
    tree0.heading("#1", text="QCRecordType", anchor=CENTER)
    tree0.heading("#2", text="QCAverageTowSpeed", anchor=CENTER)
    tree0.heading("#3", text="QCKeptWeight", anchor=CENTER)
    tree0.heading("#4", text="QCDiscardWeight", anchor=CENTER)
    tree0.heading("#5", text="QCNumberIndividuals", anchor=CENTER)
    tree0.heading("#6", text="QCNumberWindows", anchor=CENTER)
    tree0.column('#1', stretch=NO, minwidth=0, width=210, anchor = tk.CENTER)
    tree0.column('#2', stretch=NO, minwidth=0, width=175, anchor = tk.CENTER)
    tree0.column('#3', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)            
    tree0.column('#4', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree0.column('#5', stretch=NO, minwidth=0, width=190, anchor = tk.CENTER)
    tree0.column('#6', stretch=NO, minwidth=0, width=190, anchor = tk.CENTER)
    tree0.pack()
    
    ## Table B: View QC Failed Results Table
    lblTableB = Label(TopRightframe, font=('aerial', 11, 'bold'), text="B: QC Failed Results")
    lblTableB.grid(row =2, column = 0, padx=5, pady =2, ipady =2, sticky =W, rowspan =1)
    ListToSelViewVarList = ['Select QC Variable & View Fail Results',
                            '1: RecordType',
                            '2: AverageTowSpeed',
                            '3: KeptWeight',
                            '4: DiscardWeight',
                            '5: NumberIndividuals',
                            '6: NumberWindows']
    entry_ListToSelViewVarList  = ttk.Combobox(TopRightframe, font=('aerial', 10, 'bold'), 
                                                width = 40, state='readonly')
    entry_ListToSelViewVarList['values'] = ListToSelViewVarList
    entry_ListToSelViewVarList.current(0)
    entry_ListToSelViewVarList.grid(row =2, column = 0, padx=180, pady =2, ipady= 4, sticky =W)
    ## tree1 Define
    TableMargin1 = Frame(TopRightframe, bd = 2, padx= 10, pady= 1, relief = RIDGE)
    TableMargin1.grid(row =3, column = 0, padx=0, pady =1, sticky =W, rowspan =1)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4", 
                                            "column5", "column6", "column7", "column8", 
                                            "column9"), height=18, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    tree1.heading("#1", text="DatabaseID", anchor=CENTER)
    tree1.heading("#2", text="RecordIdentifier", anchor=CENTER)
    tree1.heading("#3", text="DeploymentUID", anchor=CENTER)
    tree1.heading("#4", text="RecordType", anchor=CENTER)
    tree1.heading("#5", text="AverageTowSpeed", anchor=CENTER)
    tree1.heading("#6", text="KeptWeight", anchor=CENTER)
    tree1.heading("#7", text="DiscardWeight", anchor=CENTER)
    tree1.heading("#8", text="NumberIndividuals", anchor=CENTER)
    tree1.heading("#9", text="NumberWindows", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=155, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#9', stretch=NO, minwidth=0, width=155, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 8), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)
    tree1.pack()

    ## Bottom Left
    SummaryQCframe = tk.Frame(TopRightframe, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.grid(row=5, column = 0, padx=5, pady =1, sticky =W, rowspan =1)
    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    tree3 = ttk.Treeview(Summaryframe, column=("column1", "column2", "column3", "column4"),height=8, show='headings')
    scrollbary = ttk.Scrollbar(Summaryframe, orient ="vertical", command=tree3.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree3.configure(yscrollcommand = scrollbary.set)
    tree3.heading("#1", text="QC Variable Name", anchor = W)
    tree3.heading("#2", text="# Of Fail Entries")
    tree3.heading("#3", text="# Of Entries Updated")
    tree3.heading("#4", text="QC Null Value")
    tree3.column('#1', stretch=NO, minwidth=0, width=130, anchor = W)            
    tree3.column('#2', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    tree3.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree3.column('#4', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    tree3.pack(side = BOTTOM)
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    lblTableC = Label(SummaryQCframe, font=('aerial', 11, 'bold'), text="C: QC Fail OverView", bg='cadet blue')
    lblTableC.pack(side =LEFT, anchor = E)
    SummaryDisplay.pack(side = LEFT, pady=0)

    ## Bottom Right
    DepSummaryframe = Frame(TopRightframe, bd = 1, padx= 1, pady= 1, relief = RIDGE, bg='cadet blue')
    DepSummaryframe.grid(row=5, column = 0, padx=15, pady =1, sticky =E, rowspan =1)
    
    Depframe = tk.Frame(DepSummaryframe, bg= "aliceblue")
    tree2 = ttk.Treeview(Depframe, column=("column1", "column2", "column3", "column4"), height=8, show='headings')
    scrollbary = ttk.Scrollbar(Depframe, orient ="vertical", command=tree3.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree2.configure(yscrollcommand = scrollbary.set)
    tree2.configure(xscrollcommand = scrollbarx.set)
    tree2.heading("#1", text="DeploymentIdentifier", anchor=CENTER)
    tree2.heading("#2", text="VariableValue", anchor=CENTER)
    tree2.heading("#3", text="EntriesCount", anchor=CENTER)
    tree2.heading("#4", text="VariableName", anchor=CENTER)
    tree2.column('#1', stretch=NO, minwidth=0, width=160, anchor = tk.CENTER)            
    tree2.column('#2', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)
    tree2.column('#3', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree2.column('#4', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 10), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree2, tearoff=0)
    Depframe.pack(side = BOTTOM, pady=0)
    tree2.pack(side = BOTTOM)

    DepSummaryDisplay = tk.Frame(DepSummaryframe, bg= "aliceblue")
    lblTableC = Label(DepSummaryframe, font=('aerial', 11, 'bold'), text="D: Deployment Summary", bg='cadet blue')
    lblTableC.pack(side =LEFT, anchor = E)
    DepSummaryDisplay.pack(side = LEFT, pady=0)

    ListSelecteVariables = ['Select Variable & Run Deployment Summary',
                            '1: RecordType',
                            '2: AverageTowSpeed',
                            '3: KeptWeight',
                            '4: DiscardWeight',
                            '5: NumberIndividuals',
                            '6: NumberWindows']
    entry_ListSelecteVariables  = ttk.Combobox(TopRightframe, font=('aerial', 10, 'bold'), 
                                                width = 45, state='readonly')
    entry_ListSelecteVariables['values'] = ListSelecteVariables
    entry_ListSelecteVariables.current(0)
    entry_ListSelecteVariables.grid(row=6, column = 0, padx=290, pady =1, sticky =E, rowspan =1)

    ##### All Function Define
    def ImportAndUpdateSetCatchDB():
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
        cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
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
                    df = df.iloc[:,:]
                    DataBase_ID= (df.loc[:,'DataBase_ID']).fillna(99999999).astype(int, errors='ignore')
                    RecordIdentifier= (df.loc[:,'RecordIdentifier']).fillna(99999999).astype(int, errors='ignore')
                    DeploymentUID= (df.loc[:,'DeploymentUID']).fillna(8888888).astype(str, errors='ignore')
                    RecordType= (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                    AverageTowSpeed = (df.loc[:,'AverageTowSpeed']).fillna(99999999).astype(float, errors='ignore')
                    KeptWeight=(df.loc[:,'KeptWeight']).fillna(99999999).astype(int, errors='ignore')
                    DiscardWeight=(df.loc[:,'DiscardWeight']).fillna(99999999).astype(int, errors='ignore')
                    NumberIndividuals= (df.loc[:,'NumberIndividuals']).fillna(99999999).astype(int, errors='ignore')
                    NumberWindows= (df.loc[:,'NumberWindows']).fillna(99999999).astype(int, errors='ignore')
                    column_names = [DataBase_ID, RecordIdentifier, DeploymentUID, RecordType,
                                    AverageTowSpeed,KeptWeight, DiscardWeight, NumberIndividuals, NumberWindows]
                    catdf = pd.concat (column_names,axis=1,ignore_index =True)
                    catdf.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 
                                          2:'DeploymentUID', 3:'RecordType',
                                          4:'AverageTowSpeed', 5:'KeptWeight',
                                          6:'DiscardWeight', 7:'NumberIndividuals', 
                                          8:'NumberWindows'},inplace = True)
                    Raw_Imported_Df = pd.DataFrame(catdf)
                    Raw_Imported_Df['DataBase_ID']=(Raw_Imported_Df.loc[:,'DataBase_ID']).astype(int, errors='ignore')
                    Raw_Imported_Df['RecordIdentifier']=(Raw_Imported_Df.loc[:,'RecordIdentifier']).astype(int, errors='ignore')
                    Raw_Imported_Df['RecordType']=(Raw_Imported_Df.loc[:,'RecordType']).astype(int, errors='ignore')
                    Raw_Imported_Df['AverageTowSpeed']=(Raw_Imported_Df.loc[:,'AverageTowSpeed']).astype(float, errors='ignore')
                    Raw_Imported_Df['KeptWeight']=(Raw_Imported_Df.loc[:,'KeptWeight']).astype(int, errors='ignore')
                    Raw_Imported_Df['DiscardWeight']=(Raw_Imported_Df.loc[:,'DiscardWeight']).astype(int, errors='ignore')
                    Raw_Imported_Df['NumberIndividuals']= (Raw_Imported_Df.loc[:,'NumberIndividuals']).astype(int, errors='ignore')
                    Raw_Imported_Df['NumberWindows']= (Raw_Imported_Df.loc[:,'NumberWindows']).astype(int, errors='ignore')
                    Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                    Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0], '')
                    Raw_Imported_Df = Raw_Imported_Df.replace(8888888, 'None')
                    Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                    Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                    CheckEmptyNessColumn = Raw_Imported_Df[
                                        (Raw_Imported_Df.DataBase_ID=='') |
                                        (Raw_Imported_Df.RecordIdentifier=='') |
                                        (Raw_Imported_Df.RecordType=='') |
                                        (Raw_Imported_Df.AverageTowSpeed=='')]
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
                                list_item_AverageTowSpeed = (rowValue[4])
                                list_item_KeptWeight = (rowValue[5])
                                list_item_DiscardWeight = (rowValue[6])
                                list_item_NumberIndividuals = (rowValue[7])
                                list_item_NumberWindows = (rowValue[8])
                            
                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_RecordType,
                                                    list_item_AverageTowSpeed,
                                                    list_item_KeptWeight,
                                                    list_item_DiscardWeight,
                                                    list_item_NumberIndividuals,
                                                    list_item_NumberWindows,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                UpdateRecordList_QCFailDB.append((
                                                    list_item_RecordType,
                                                    list_item_AverageTowSpeed,
                                                    list_item_KeptWeight,
                                                    list_item_DiscardWeight,
                                                    list_item_NumberIndividuals,
                                                    list_item_NumberWindows, 
                                                    'Updated','Updated','Updated',
                                                    'Updated','Updated', 'Updated',
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ?, AverageTowSpeed = ?, \
                                                    KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?, NumberWindows = ? \
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables SET RecordType = ?, AverageTowSpeed = ?, \
                                                    KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?, NumberWindows = ?,\
                                                    RecordTypeRangeQC =?, AverageTowSpeedRangeQC = ?, KeptWeightRangeQC = ?, DiscardWeightRangeQC = ?,\
                                                    NumberIndividualsRangeQC = ?, NumberWindowsRangeQC = ?\
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_QCFailDB)
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_Range.commit()
                            conn_DB_SetCatch_Validation_Range.close()
                            txtDisplayMessageSystem.delete(0,END)
                            txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                            tkinter.messagebox.showinfo("Update Success","Successfully Updated The Imported Entries") 
                        else:
                            Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                            Raw_Imported_Df.set_index('DataBase_ID', inplace=True)
                            ## GetSetCatchProfileDB
                            SetCatchProfileDB_DF = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", 
                                                                    conn_DB_Set_Catch_Analysis)
                            SetCatchProfileDB_DF = pd.DataFrame(SetCatchProfileDB_DF)
                            SetCatchProfileDB_DF = SetCatchProfileDB_DF.reset_index(drop=True)
                            SetCatchProfileDB_DF.set_index('DataBase_ID', inplace=True)
                            ## GetSetCatchQCFailedDB
                            SetCatchQCFailedDB_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables ORDER BY `DataBase_ID` ASC ;", 
                                                                    conn_DB_SetCatch_Validation_Range)
                            SetCatchQCFailedDB_DF = pd.DataFrame(SetCatchQCFailedDB_DF)
                            SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.reset_index(drop=True)
                            SetCatchQCFailedDB_DF.set_index('DataBase_ID', inplace=True)
                            
                            ## Update DF SetCatch Imported DB
                            SetCatchProfileDB_DF.update(Raw_Imported_Df)
                            SetCatchProfileDB_DF.reset_index(inplace=True)
                            SetCatchProfileDB_DF['DataBase_ID']=(SetCatchProfileDB_DF.loc[:,'DataBase_ID']).astype(int, errors='ignore')
                            SetCatchProfileDB_DF['RecordIdentifier']=(SetCatchProfileDB_DF.loc[:,'RecordIdentifier']).astype(int, errors='ignore')
                            SetCatchProfileDB_DF['RecordType']=(SetCatchProfileDB_DF.loc[:,'RecordType']).astype(int, errors='ignore')
                            SetCatchProfileDB_DF['AverageTowSpeed']=(SetCatchProfileDB_DF.loc[:,'AverageTowSpeed']).astype(float, errors='ignore')
                            SetCatchProfileDB_DF['KeptWeight']=(SetCatchProfileDB_DF.loc[:,'KeptWeight']).astype(int, errors='ignore')
                            SetCatchProfileDB_DF['DiscardWeight']=(SetCatchProfileDB_DF.loc[:,'DiscardWeight']).astype(int, errors='ignore')
                            SetCatchProfileDB_DF['NumberIndividuals']= (SetCatchProfileDB_DF.loc[:,'NumberIndividuals']).astype(int, errors='ignore')
                            SetCatchProfileDB_DF['NumberWindows']= (SetCatchProfileDB_DF.loc[:,'NumberWindows']).astype(int, errors='ignore')
                            try:
                                Submit_To_DBStorage = pd.DataFrame(SetCatchProfileDB_DF)
                                Submit_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_Analysis_IMPORT', 
                                                        conn_DB_Set_Catch_Analysis, if_exists="replace",index = False)
                                conn_DB_Set_Catch_Analysis.commit()
                            except sqlite3.Error as error:
                                print('Error occured - ', error)
                            finally:
                                if conn_DB_Set_Catch_Analysis:
                                    cur_DB_Set_Catch_Analysis.close()
                                    conn_DB_Set_Catch_Analysis.close()

                            ## Update QC Failed variable range
                            SetCatchQCFailedDB_DF.update(Raw_Imported_Df)
                            SetCatchQCFailedDB_DF.reset_index(inplace=True)
                            SetCatchQCFailedDB_DF['DataBase_ID']=(SetCatchQCFailedDB_DF.loc[:,'DataBase_ID']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['RecordIdentifier']=(SetCatchQCFailedDB_DF.loc[:,'RecordIdentifier']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['RecordType']=(SetCatchQCFailedDB_DF.loc[:,'RecordType']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['AverageTowSpeed']=(SetCatchQCFailedDB_DF.loc[:,'AverageTowSpeed']).astype(float, errors='ignore')
                            SetCatchQCFailedDB_DF['KeptWeight']=(SetCatchQCFailedDB_DF.loc[:,'KeptWeight']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['DiscardWeight']=(SetCatchQCFailedDB_DF.loc[:,'DiscardWeight']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['NumberIndividuals']= (SetCatchQCFailedDB_DF.loc[:,'NumberIndividuals']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['NumberWindows']= (SetCatchQCFailedDB_DF.loc[:,'NumberWindows']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['RecordTypeRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['AverageTowSpeedRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['KeptWeightRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['DiscardWeightRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['NumberIndividualsRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['NumberWindowsRangeQC']='Updated'
                            try:
                                Submit_To_DBStorage = pd.DataFrame(SetCatchQCFailedDB_DF)
                                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_CatchVariables', 
                                                        conn_DB_SetCatch_Validation_Range, if_exists="replace",index = False)
                                conn_DB_SetCatch_Validation_Range.commit()
                            except sqlite3.Error as error:
                                print('Error occured - ', error)
                            finally:
                                if conn_DB_SetCatch_Validation_Range:
                                    cur_DB_SetCatch_Validation_Range.close()
                                    conn_DB_SetCatch_Validation_Range.close()
                            txtDisplayMessageSystem.delete(0,END)
                            txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                            tkinter.messagebox.showinfo("Update Success","Successfully Updated The Imported Entries") 
                    else:
                        messagebox.showerror('Empty Values In Variable Columns', "Please Check DataBase_ID, RecordIdentifier, RecordType, AverageTowSpeed Columns")

    def Export_FailedCSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables ORDER BY `DataBase_ID` ASC ;", conn)
            Complete_df = Complete_df.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 
                 'RecordType', 'AverageTowSpeed', 
                 'KeptWeight', 'DiscardWeight',
                 'NumberIndividuals', 'NumberWindows',
                 'RecordTypeRangeQC', 'AverageTowSpeedRangeQC', 
                 'KeptWeightRangeQC', 'DiscardWeightRangeQC',
                 'NumberIndividualsRangeQC', 'NumberWindowsRangeQC']]
            Complete_df.drop_duplicates(subset=['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType'], 
                                        keep='last', inplace = True)
            Complete_df.sort_values(by=['DataBase_ID', 'RecordIdentifier', 
                                 'DeploymentUID', 'RecordType'], inplace=True)
            Complete_df  = Complete_df.reset_index(drop=True)
            Complete_df  = pd.DataFrame(Complete_df)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("QC Failed CatchVariables Profile","QC Failed CatchVariables Profile Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("QC Failed CatchVariables Profile Report Message","Please Select File Name To Export")
            else:
                messagebox.showerror('Export Error', "Void File... Nothing to Export")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def viewQCFailed(getVarnameToView):
        ListVariableListA = ['Select QC Variable & View Fail Results',
                            '1: RecordType',
                            '2: AverageTowSpeed',
                            '3: KeptWeight',
                            '4: DiscardWeight',
                            '5: NumberIndividuals',
                            '6: NumberWindows']
        if getVarnameToView == ListVariableListA[1]:
            QCMsgVariable = 'Case-RT-RangeQC'
        if getVarnameToView == ListVariableListA[2]:
            QCMsgVariable = 'Case-ATS-RangeQC'
        if getVarnameToView == ListVariableListA[3]:
            QCMsgVariable = 'Case-KW-RangeQC'
        if getVarnameToView == ListVariableListA[4]:
            QCMsgVariable = 'Case-DW-RangeQC'
        if getVarnameToView == ListVariableListA[5]:
            QCMsgVariable = 'Case-NI-RangeQC'
        if getVarnameToView == ListVariableListA[6]:
            QCMsgVariable = 'Case-NW-RangeQC'
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Range)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_QCFailedRange_CatchVariables")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows, 
            columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 
                      'RecordType', 'AverageTowSpeed', 
                      'KeptWeight', 'DiscardWeight', 
                      'NumberIndividuals', 'NumberWindows', 
                      'RecordTypeRangeQC', 'AverageTowSpeedRangeQC', 
                      'KeptWeightRangeQC', 'DiscardWeightRangeQC',
                      'NumberIndividualsRangeQC', 'NumberWindowsRangeQC', 
                      'DeploymentIdentifier', 'QC_Message'])
            
            rows = rows[((rows['QC_Message'] == QCMsgVariable)
                        )]
            rows = rows.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'AverageTowSpeed', 'KeptWeight', 'DiscardWeight', 'NumberIndividuals', 'NumberWindows']]
            rows.sort_values(by=['DataBase_ID', 'RecordIdentifier', 
                                 'DeploymentUID', 'RecordType'], inplace=True)
            rows  = rows.reset_index(drop=True)
            rows  = pd.DataFrame(rows)
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_VariablesProfile():
        getVarnameToView = entry_ListToSelViewVarList.get()
        ListVariableListA =['1: RecordType',
                            '2: AverageTowSpeed',
                            '3: KeptWeight',
                            '4: DiscardWeight',
                            '5: NumberIndividuals',
                            '6: NumberWindows']
        if getVarnameToView in ListVariableListA:
            tree1.delete(*tree1.get_children())
            rows = viewQCFailed(getVarnameToView)
            countIndex1 = 0
            for each_rec in range(len(rows)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(rows.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")
            QCFailedSelEntries =len(rows)
            txtSelectedFailedEntries.delete(0,END)
            txtSelectedFailedEntries.insert(tk.END,QCFailedSelEntries) 

    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        QCFailedTotalEntries = len(data)       
        txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)             
        conn.commit()
        conn.close()

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CatchVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def fetchData_RangeLimitVariables():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_RangeLimitVariables_Define ORDER BY `VariablesID` ASC ;", conn)
            return Complete_df
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def ClearProfile():
        txtDeploymentUID.config(state= "normal")
        txtDeploymentUID.delete(0,END)
        txtDeploymentUID.config(state= "disabled")
        txtAverageTowSpeed.delete(0,END)
        txtKeptWeight.delete(0,END)
        txtDiscardWeight.delete(0,END)
        txtNumberIndividuals.delete(0,END)
        txtNumberWindows.delete(0,END)

    def UpdateSelectedDepUID():
        cur_id = tree1.focus()
        selvalue = tree1.item(cur_id)['values']
        Length_Selected  =  (len(selvalue))
        if Length_Selected != 0:
            SelectionTree = tree1.selection()
            if (len(SelectionTree)>0) & (len(SelectionTree)==1) & (len(SelectionTree)<2):
                iUpdate = tkinter.messagebox.askyesno("Update Entry In DFO-NL-ASOP Set & Catch Database", 
                            "Confirm If You Want To Update In DFO-NL-ASOP Set & Catch Database")
                if iUpdate >0:
                    list_item = (tree1.item(SelectionTree, 'values'))
                    list_item_DatabaseUID = int(list_item[0])
                    list_item_RecordIdentifier = int(list_item[1])
                    list_item_DeploymentUID = (list_item[2])
                    list_item_RecordType = (list_item[3])
                    
                    try:
                        AverageTowSpeed = int(txtAverageTowSpeed.get())
                    except:
                        AverageTowSpeed = (txtAverageTowSpeed.get())
                    try:
                        KeptWeight = int(txtKeptWeight.get())
                    except:
                        KeptWeight = (txtKeptWeight.get())
                    try:
                        DiscardWeight = int(txtDiscardWeight.get())
                    except:
                        DiscardWeight = (txtDiscardWeight.get())
                    try:
                        NumberIndividuals = int(txtNumberIndividuals.get())
                    except:
                        NumberIndividuals = (txtNumberIndividuals.get())
                    try:
                        NumberWindows = int(txtNumberWindows.get())
                    except:
                        NumberWindows = (txtNumberWindows.get())
                     
                    ## DB Connect
                    try:
                        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                        
                        conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
                        cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
                        
                        ## DB Update
                        cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ?, \
                            KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?, NumberWindows = ?\
                            WHERE DeploymentUID =?", 
                            (AverageTowSpeed, KeptWeight, DiscardWeight, NumberIndividuals, NumberWindows, list_item_DeploymentUID))
                        
                        cur_DB_SetCatch_Validation_Range.execute("UPDATE SetCatch_QCFailedRange_CatchVariables SET AverageTowSpeed = ?, \
                            KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?, NumberWindows = ?,\
                            AverageTowSpeedRangeQC = ?, KeptWeightRangeQC = ?, DiscardWeightRangeQC = ?,\
                            NumberIndividualsRangeQC = ?, NumberWindowsRangeQC = ?\
                            WHERE DeploymentUID =?", 
                            (AverageTowSpeed, KeptWeight, DiscardWeight, NumberIndividuals, NumberWindows, \
                            'Updated','Updated','Updated','Updated','Updated', list_item_DeploymentUID))
                            
                    except sqlite3.Error as error:
                        print('Error occured - ', error)
                
                    finally:
                        conn_DB_Set_Catch_Analysis.commit()
                        conn_DB_Set_Catch_Analysis.close()
                        conn_DB_SetCatch_Validation_Range.commit()
                        conn_DB_SetCatch_Validation_Range.close()

                    tree1.delete(*tree1.get_children())
                    tree1.insert("", tk.END,values=(list_item_DatabaseUID,
                                                    list_item_RecordIdentifier, 
                                                    list_item_DeploymentUID, 
                                                    list_item_RecordType,\
                                                    AverageTowSpeed, KeptWeight, DiscardWeight, \
                                                    NumberIndividuals, NumberWindows))
            else:
                UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                        "1. Please Select One Entry Only From The CatchVariables Table To Update "  + '\n' + '\n' + 
                        "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                        "3. Please Do Not Update Without Selecting Entry From CatchVariables Table" )
                tkinter.messagebox.showerror("Update Error Possible Reasons",UpdatePossibleError)
        else:
            tkinter.messagebox.showerror("Update Error Possible Reasons"," Please Select One Entry To Modify")
        
    def ClearTablesAll():
        tree1.delete(*tree1.get_children())
        tree0.delete(*tree0.get_children())
        tree2.delete(*tree2.get_children())
        txtSelectedFailedEntries.delete(0,END)
        txtTotalFailedEntries.delete(0,END)
        txtDisplayMessageSystem.delete(0,END)
        ClearProfile()

    def Tree0ViewBackend(GetDisplayMessageDF):
        df_rows = GetDisplayMessageDF.to_numpy().tolist()
        tree0.delete(*tree0.get_children())
        for row in df_rows:
            tree0.insert("", "end", values =row,tags =("even",))
        tree0.tag_configure("even",foreground="black", background="VioletRed1")

    def GenDisplayMessageTableA_Backend(DataBase_ID ="", RecordIdentifier ="", DeploymentUID =""):
        try:
            conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
            cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
            cur_DB_SetCatch_Validation_Range.execute("SELECT RecordTypeRangeQC, \
                            AverageTowSpeedRangeQC, KeptWeightRangeQC, DiscardWeightRangeQC,\
                            NumberIndividualsRangeQC, NumberWindowsRangeQC\
                            FROM SetCatch_QCFailedRange_CatchVariables WHERE \
                            (DataBase_ID = :DataBase_ID) AND\
                            (RecordIdentifier = :RecordIdentifier) AND\
                            (DeploymentUID= :DeploymentUID)",\
                            (DataBase_ID, RecordIdentifier, DeploymentUID))
            rows=cur_DB_SetCatch_Validation_Range.fetchall()
            return rows
        except:
            messagebox.showerror('CatchVariables Variable Error Message', "CatchVariables Query Failed")

    def InventoryRec1(event):
        SelectionTree = tree1.selection()
        if (len(SelectionTree)>0) & (len(SelectionTree) < 20001):
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,len(SelectionTree))
        else:
            entry_NumberRowSelected.delete(0,END)
            entry_NumberRowSelected.insert(tk.END,'MaxLimit Exceed')
        
        if (len(SelectionTree)>0) & (len(SelectionTree)==1) & (len(SelectionTree)<2):
            for nm in tree1.selection():
                sd = tree1.item(nm, 'values')
                DataBase_ID = int(sd[0])
                RecordIdentifier = int(sd[1])
                DeploymentUID =sd[2]
                GetDisplayMessageTableA = GenDisplayMessageTableA_Backend(DataBase_ID, RecordIdentifier, DeploymentUID)
                GetDisplayMessageDF = pd.DataFrame(GetDisplayMessageTableA, 
                columns =['RecordTypeRangeQC','AverageTowSpeedRangeQC', 
                        'KeptWeightRangeQC', 
                        'DiscardWeightRangeQC',
                        'NumberIndividualsRangeQC', 
                        'NumberWindowsRangeQC'])
                GetDisplayMessageDF.reset_index(drop=True)
                GetDisplayMessageDF  = pd.DataFrame(GetDisplayMessageDF)
                Tree0ViewBackend(GetDisplayMessageDF)

                txtDeploymentUID.config(state= "normal")
                txtDeploymentUID.delete(0,END)
                txtDeploymentUID.insert(tk.END,sd[2])
                txtDeploymentUID.config(state= "disabled")
                
                txtAverageTowSpeed.delete(0,END)
                txtAverageTowSpeed.insert(tk.END,sd[4])

                txtKeptWeight.delete(0,END)
                txtKeptWeight.insert(tk.END,sd[5])

                txtDiscardWeight.delete(0,END)
                txtDiscardWeight.insert(tk.END,sd[6])

                txtNumberIndividuals.delete(0,END)
                txtNumberIndividuals.insert(tk.END,sd[7])

                txtNumberWindows.delete(0,END)
                txtNumberWindows.insert(tk.END,sd[8])
         
    def Modify_MultipleSetCatch_CatchVariablesProfile():
        ListBox_DF = (tree1.get_children())
        if len(ListBox_DF)>0:
            cur_id = tree1.focus()
            selvalue = tree1.item(cur_id)['values']
            Length_Selected  =  (len(selvalue))
            if Length_Selected != 0:
                SelectionTree = tree1.selection()
                if (len(SelectionTree)>0):
                    iUpdate = tkinter.messagebox.askyesno("Update Multiple Entries In  DFO-NL-ASOP Set & Catch Database", 
                            "Confirm If You Want To Update Multiple CatchVariables Entries In DFO-NL-ASOP Set & Catch Database")
                    if iUpdate >0:
                        SelectionTree = tree1.selection()
                        CurrentEntryAverageTowSpeed = txtAverageTowSpeed.get()
                        CurrentEntryKeptWeight = txtKeptWeight.get()
                        CurrentEntryDiscardWeight = txtDiscardWeight.get()
                        CurrentEntryNumberIndividuals = txtNumberIndividuals.get()
                        CurrentEntryNumberWindows = txtNumberWindows.get()
                        Modify_Multiple_BackEnd(CurrentEntryAverageTowSpeed, CurrentEntryKeptWeight,
                                                CurrentEntryDiscardWeight, CurrentEntryNumberIndividuals,
                                                CurrentEntryNumberWindows, SelectionTree)
            else:
                tkinter.messagebox.showinfo("Update Error","Please Select At least One Entries To Update CatchVariables")
        else:
            tkinter.messagebox.showinfo("Update Error","Empty CatchVariables Table. Please Select At least One Entries In The Table To Update CatchVariables ")

    def Modify_Multiple_BackEnd(CurrentEntryAverageTowSpeed, CurrentEntryKeptWeight,
                                CurrentEntryDiscardWeight, CurrentEntryNumberIndividuals,
                                CurrentEntryNumberWindows, SelectionTree):
        application_window=tk.Tk()
        application_window.title ("Update Variables : Catch Type")
        application_window.geometry('420x300+100+40')
        application_window.config(bg="aliceblue")

        lbl_UpdateEntry = Label(application_window, font=('aerial', 11, 'bold'), 
                        bg= "aliceblue", text="Provide Updated Catch Variables Entry : ")
        lbl_UpdateEntry.grid(row =0, column = 0, padx=3, pady =10)

        lbl_Entries_AverageTowSpeed = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" A. Entries For AverageTowSpeed :")
        lbl_Entries_AverageTowSpeed.grid(row =1, column = 0, padx=3, pady =2, sticky =W)
        UpdateValue_AverageTowSpeed       = IntVar(application_window, value =CurrentEntryAverageTowSpeed)
        entry_UpdateValue_AverageTowSpeed = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                        textvariable = UpdateValue_AverageTowSpeed, width = 10)
        entry_UpdateValue_AverageTowSpeed.grid(row =1, column = 1, padx=5, pady =2, ipady =2, sticky =W)

        lbl_Entries_KeptWeight = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" B. Entries For KeptWeight :")
        lbl_Entries_KeptWeight.grid(row =2, column = 0, padx=3, pady =10, sticky =W)
        UpdateValue_KeptWeight       = IntVar(application_window, value = CurrentEntryKeptWeight)
        entry_UpdateValue_KeptWeight = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                textvariable = UpdateValue_KeptWeight, width = 10)
        entry_UpdateValue_KeptWeight.grid(row =2, column = 1, padx=5, pady =10, ipady =2, sticky =W)

        lbl_Entries_DiscardWeight = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" C. Entries For DiscardWeight :")
        lbl_Entries_DiscardWeight.grid(row =3, column = 0, padx=3, pady =2, sticky =W)
        UpdateValue_DiscardWeight       = IntVar(application_window, value =CurrentEntryDiscardWeight)
        entry_UpdateValue_DiscardWeight = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                        textvariable = UpdateValue_DiscardWeight, width = 10)
        entry_UpdateValue_DiscardWeight.grid(row =3, column = 1, padx=5, pady =2, ipady =2, sticky =W)

        lbl_Entries_NumberIndividuals = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" D. Entries For NumberIndividuals :")
        lbl_Entries_NumberIndividuals.grid(row =4, column = 0, padx=3, pady =10, sticky =W)
        UpdateValue_NumberIndividuals       = IntVar(application_window, value = CurrentEntryNumberIndividuals)
        entry_UpdateValue_NumberIndividuals = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                textvariable = UpdateValue_NumberIndividuals, width = 10)
        entry_UpdateValue_NumberIndividuals.grid(row =4, column = 1, padx=5, pady =10, ipady =2, sticky =W)

        lbl_Entries_NumberWindows = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" E. Entries For NumberWindows :")
        lbl_Entries_NumberWindows.grid(row =5, column = 0, padx=3, pady =2, sticky =W)
        UpdateValue_NumberWindows       = IntVar(application_window, value =CurrentEntryNumberWindows)
        entry_UpdateValue_NumberWindows = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                        textvariable = UpdateValue_NumberWindows, width = 10)
        entry_UpdateValue_NumberWindows.grid(row =5, column = 1, padx=5, pady =2, ipady =2, sticky =W)

        SelectionTree = SelectionTree

        def SubmitForupdate():
            try:
                UpdateValue_AverageTowSpeed = float(entry_UpdateValue_AverageTowSpeed.get())
            except:
                UpdateValue_AverageTowSpeed = entry_UpdateValue_AverageTowSpeed.get()
            try:
                UpdateValue_KeptWeight = int(entry_UpdateValue_KeptWeight.get())
            except:
                UpdateValue_KeptWeight = entry_UpdateValue_KeptWeight.get()
            try:
                UpdateValue_DiscardWeight = int(entry_UpdateValue_DiscardWeight.get())
            except:
                UpdateValue_DiscardWeight = entry_UpdateValue_DiscardWeight.get()
            try:
                UpdateValue_NumberIndividuals = int(entry_UpdateValue_NumberIndividuals.get())
            except:
                UpdateValue_NumberIndividuals = (entry_UpdateValue_NumberIndividuals.get())
            try:
                UpdateValue_NumberWindows = int(entry_UpdateValue_NumberWindows.get())
            except:
                UpdateValue_NumberWindows = entry_UpdateValue_NumberWindows.get()
            
            ## DB Connect
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
            conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
            cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
            Length_SelectionTree  =  len(SelectionTree)
            if Length_SelectionTree <250000:
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList_QCFailDB =[]
                for item in SelectionTree:
                    list_item = (tree1.item(item, 'values'))
                    list_item_DatabaseUID = int(list_item[0])
                    list_item_RecordIdentifier = int(list_item[1])
                    list_item_DeploymentUID = (list_item[2])
                    UpdateRecordList_SetCatchDB.append((UpdateValue_AverageTowSpeed,
                                            UpdateValue_KeptWeight,
                                            UpdateValue_DiscardWeight,
                                            UpdateValue_NumberIndividuals,
                                            UpdateValue_NumberWindows,
                                            list_item_DatabaseUID,
                                            list_item_RecordIdentifier,
                                            list_item_DeploymentUID))
                    UpdateRecordList_QCFailDB.append((UpdateValue_AverageTowSpeed,
                                            UpdateValue_KeptWeight,
                                            UpdateValue_DiscardWeight,
                                            UpdateValue_NumberIndividuals,
                                            UpdateValue_NumberWindows, 
                                            'Updated','Updated','Updated',
                                            'Updated','Updated',
                                            list_item_DatabaseUID,
                                            list_item_RecordIdentifier,
                                            list_item_DeploymentUID))
                    
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ?, \
                                                KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?, NumberWindows = ?\
                                                WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_SetCatchDB)
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables SET AverageTowSpeed = ?, \
                                                KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?, NumberWindows = ?,\
                                                AverageTowSpeedRangeQC = ?, KeptWeightRangeQC = ?, DiscardWeightRangeQC = ?,\
                                                NumberIndividualsRangeQC = ?, NumberWindowsRangeQC = ?\
                                                WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                UpdateRecordList_QCFailDB)
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
                conn_DB_SetCatch_Validation_Range.commit()
                conn_DB_SetCatch_Validation_Range.close()
                application_window.destroy()
                txtDisplayMessageSystem.delete(0,END)
                txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                tkinter.messagebox.showinfo("Update Success","Successfully Updated The Imported Entries")
                viewQCFailed_VariablesProfile()

        button_Submit = Button(application_window, bd = 2, text ="Update", width = 8,
                                        height=1, font=('aerial', 10, 'bold'), fg="blue", bg="aliceblue", 
                                        command =SubmitForupdate)
        button_Submit.grid(row =7, column = 1, padx=5, pady =5, ipady =1, sticky =W)
        
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
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables ORDER BY `DataBase_ID` ASC ;", conn)
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
                    'intprecision': 2,
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
        
    def SubmitDataFrameToQCFailedDB(DataFrameToSubmit):
        try:
            Import_To_DBStorage = pd.DataFrame(DataFrameToSubmit)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Import_To_DBStorage.to_sql('SetCatch_QCFailedRange_CatchVariables', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def GenDepIdfier_Col_SetCatchFailDB():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF['DeploymentIdentifier'] = SetCatchQCFailedDB_DF['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
                SetCatchQCFailedDB_DF['DeploymentIdentifier'] = SetCatchQCFailedDB_DF['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.reset_index(drop=True)
                DataFrameToSubmit = pd.DataFrame(SetCatchQCFailedDB_DF)
                SubmitDataFrameToQCFailedDB(DataFrameToSubmit)
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()
        
    def GenQCFailedSummaryTable_Backend():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables ORDER BY `DataBase_ID` ASC ;", conn)
            Complete_df = Complete_df.reset_index(drop=True)
            Complete_df = pd.DataFrame(Complete_df)
            return Complete_df
                
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()   

    def GenQCFailedDepSummaryTable():
        tree1.delete(*tree1.get_children())
        tree2.delete(*tree2.get_children())
        tree0.delete(*tree0.get_children())
        txtSelectedFailedEntries.delete(0,END)
        QCFailedCatchVariablesDB= GenQCFailedSummaryTable_Backend()
        ListSelecteVariables = ['Select Variable & Run Deployment Summary',
                            '1: RecordType',
                            '2: AverageTowSpeed',
                            '3: KeptWeight',
                            '4: DiscardWeight',
                            '5: NumberIndividuals',
                            '6: NumberWindows']
        getentry_ListSelecteVariables = entry_ListSelecteVariables.get()
        
        if getentry_ListSelecteVariables == ListSelecteVariables[0]:
            tkinter.messagebox.showinfo("Run Failed Summary QC Message","Please Select Variable Name To Run")
        
        if getentry_ListSelecteVariables == ListSelecteVariables[1]:
            QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID', 'RecordType',
                                'RecordTypeRangeQC','DeploymentIdentifier', 'QC_Message']])
            
            QCFailedCatchVariablesDB = QCFailedCatchVariablesDB[(
                (QCFailedCatchVariablesDB.QC_Message == 'Case-RT-RangeQC'))]
            QCFailedCatchVariablesDB  = QCFailedCatchVariablesDB.reset_index(drop=True)
            QCFailedCatchVariablesDB  = pd.DataFrame(QCFailedCatchVariablesDB)
            
            Tree1QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType']])
            Tree1QCFailedCatchVariablesDB['AverageTowSpeed'] =''
            Tree1QCFailedCatchVariablesDB['KeptWeight'] =''
            Tree1QCFailedCatchVariablesDB['DiscardWeight'] =''
            Tree1QCFailedCatchVariablesDB['NumberIndividuals'] =''
            Tree1QCFailedCatchVariablesDB['NumberWindows'] =''
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedCatchVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailCatchVarSummTab_C   = QCFailedCatchVariablesDB.groupby(['DeploymentIdentifier', 'RecordType'], as_index=False).DataBase_ID.count()
            QCFailCatchVarSummTab_C   = pd.DataFrame(QCFailCatchVarSummTab_C)
            QCFailCatchVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'RecordType':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailCatchVarSummTab_C['CatchVariables'] =QCFailCatchVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailCatchVarSummTab_C = QCFailCatchVarSummTab_C.reset_index(drop=True)
            QCFailCatchVarSummTab_C = pd.DataFrame(QCFailCatchVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailCatchVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[2]:
            QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                'AverageTowSpeed','AverageTowSpeedRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedCatchVariablesDB = QCFailedCatchVariablesDB[(
                (QCFailedCatchVariablesDB.QC_Message == 'Case-ATS-RangeQC'))]
            QCFailedCatchVariablesDB  = QCFailedCatchVariablesDB.reset_index(drop=True)
            QCFailedCatchVariablesDB  = pd.DataFrame(QCFailedCatchVariablesDB)
           
            Tree1QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','AverageTowSpeed']])
            Tree1QCFailedCatchVariablesDB['KeptWeight'] =''
            Tree1QCFailedCatchVariablesDB['DiscardWeight'] =''
            Tree1QCFailedCatchVariablesDB['NumberIndividuals'] =''
            Tree1QCFailedCatchVariablesDB['NumberWindows'] =''
            Tree1QCFailedCatchVariablesDB= (Tree1QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                'AverageTowSpeed', 'KeptWeight','DiscardWeight','NumberIndividuals', 'NumberWindows']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedCatchVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailCatchVarSummTab_C   = QCFailedCatchVariablesDB.groupby(['DeploymentIdentifier', 'AverageTowSpeed'], as_index=False).DataBase_ID.count()
            QCFailCatchVarSummTab_C   = pd.DataFrame(QCFailCatchVarSummTab_C)
            QCFailCatchVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'AverageTowSpeed':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailCatchVarSummTab_C['CatchVariables'] =QCFailCatchVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailCatchVarSummTab_C = QCFailCatchVarSummTab_C.reset_index(drop=True)
            QCFailCatchVarSummTab_C = pd.DataFrame(QCFailCatchVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailCatchVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[3]:
            QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'KeptWeight','KeptWeightRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedCatchVariablesDB = QCFailedCatchVariablesDB[(
                (QCFailedCatchVariablesDB.QC_Message == 'Case-KW-RangeQC'))]
            QCFailedCatchVariablesDB  = QCFailedCatchVariablesDB.reset_index(drop=True)
            QCFailedCatchVariablesDB  = pd.DataFrame(QCFailedCatchVariablesDB)
            
            Tree1QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','KeptWeight']])
            Tree1QCFailedCatchVariablesDB['AverageTowSpeed'] =''
            Tree1QCFailedCatchVariablesDB['DiscardWeight'] =''
            Tree1QCFailedCatchVariablesDB['NumberIndividuals'] =''
            Tree1QCFailedCatchVariablesDB['NumberWindows'] =''
            Tree1QCFailedCatchVariablesDB= (Tree1QCFailedCatchVariablesDB.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                        'AverageTowSpeed', 'KeptWeight','KeptWeight','NumberIndividuals', 'NumberWindows']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedCatchVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailCatchVarSummTab_C   = QCFailedCatchVariablesDB.groupby(['DeploymentIdentifier', 'KeptWeight'], as_index=False).DataBase_ID.count()
            QCFailCatchVarSummTab_C   = pd.DataFrame(QCFailCatchVarSummTab_C)
            QCFailCatchVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'KeptWeight':'VariableValue','DataBase_ID':'TotalCount'},inplace = True)
            QCFailCatchVarSummTab_C['CatchVariables'] =QCFailCatchVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailCatchVarSummTab_C = QCFailCatchVarSummTab_C.reset_index(drop=True)
            QCFailCatchVarSummTab_C = pd.DataFrame(QCFailCatchVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailCatchVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[4]:
            QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'DiscardWeight','DiscardWeightRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedCatchVariablesDB = QCFailedCatchVariablesDB[(
                (QCFailedCatchVariablesDB.QC_Message == 'Case-DW-RangeQC'))]
            QCFailedCatchVariablesDB  = QCFailedCatchVariablesDB.reset_index(drop=True)
            QCFailedCatchVariablesDB  = pd.DataFrame(QCFailedCatchVariablesDB)
           
            Tree1QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','DiscardWeight']])
            Tree1QCFailedCatchVariablesDB['AverageTowSpeed'] =''
            Tree1QCFailedCatchVariablesDB['KeptWeight'] =''
            Tree1QCFailedCatchVariablesDB['NumberIndividuals'] =''
            Tree1QCFailedCatchVariablesDB['NumberWindows'] =''
            Tree1QCFailedCatchVariablesDB= (Tree1QCFailedCatchVariablesDB.loc[:,
            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
            'AverageTowSpeed', 'KeptWeight','DiscardWeight','NumberIndividuals', 'NumberWindows']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedCatchVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailCatchVarSummTab_C   = QCFailedCatchVariablesDB.groupby(['DeploymentIdentifier', 'DiscardWeight'], as_index=False).DataBase_ID.count()
            QCFailCatchVarSummTab_C   = pd.DataFrame(QCFailCatchVarSummTab_C)
            QCFailCatchVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'DiscardWeight':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailCatchVarSummTab_C['CatchVariables'] =QCFailCatchVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailCatchVarSummTab_C = QCFailCatchVarSummTab_C.reset_index(drop=True)
            QCFailCatchVarSummTab_C = pd.DataFrame(QCFailCatchVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailCatchVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[5]:
            QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                'NumberIndividuals','NumberIndividualsRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedCatchVariablesDB = QCFailedCatchVariablesDB[(
                (QCFailedCatchVariablesDB.QC_Message == 'Case-NI-RangeQC'))]
            QCFailedCatchVariablesDB  = QCFailedCatchVariablesDB.reset_index(drop=True)
            QCFailedCatchVariablesDB  = pd.DataFrame(QCFailedCatchVariablesDB)
            
            Tree1QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','NumberIndividuals']])
            Tree1QCFailedCatchVariablesDB['AverageTowSpeed'] =''
            Tree1QCFailedCatchVariablesDB['KeptWeight'] =''
            Tree1QCFailedCatchVariablesDB['DiscardWeight'] =''
            Tree1QCFailedCatchVariablesDB['NumberWindows'] =''
            Tree1QCFailedCatchVariablesDB= (Tree1QCFailedCatchVariablesDB.loc[:,
            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
            'AverageTowSpeed', 'KeptWeight','DiscardWeight','NumberIndividuals', 'NumberWindows']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedCatchVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailCatchVarSummTab_C   = QCFailedCatchVariablesDB.groupby(['DeploymentIdentifier', 'NumberIndividuals'], as_index=False).DataBase_ID.count()
            QCFailCatchVarSummTab_C   = pd.DataFrame(QCFailCatchVarSummTab_C)
            QCFailCatchVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'NumberIndividuals':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailCatchVarSummTab_C['CatchVariables'] =QCFailCatchVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailCatchVarSummTab_C = QCFailCatchVarSummTab_C.reset_index(drop=True)
            QCFailCatchVarSummTab_C = pd.DataFrame(QCFailCatchVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailCatchVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[6]:
            QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                'NumberWindows','NumberWindowsRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedCatchVariablesDB = QCFailedCatchVariablesDB[(
                (QCFailedCatchVariablesDB.QC_Message == 'Case-NW-RangeQC'))]
            QCFailedCatchVariablesDB  = QCFailedCatchVariablesDB.reset_index(drop=True)
            QCFailedCatchVariablesDB  = pd.DataFrame(QCFailedCatchVariablesDB)
            
            Tree1QCFailedCatchVariablesDB= (QCFailedCatchVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','NumberWindows']])
            Tree1QCFailedCatchVariablesDB['AverageTowSpeed'] =''
            Tree1QCFailedCatchVariablesDB['KeptWeight'] =''
            Tree1QCFailedCatchVariablesDB['DiscardWeight'] =''
            Tree1QCFailedCatchVariablesDB['NumberIndividuals'] =''
            Tree1QCFailedCatchVariablesDB= (Tree1QCFailedCatchVariablesDB.loc[:,
            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
            'AverageTowSpeed', 'KeptWeight','DiscardWeight','NumberIndividuals', 'NumberWindows']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedCatchVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedCatchVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailCatchVarSummTab_C   = QCFailedCatchVariablesDB.groupby(['DeploymentIdentifier', 'NumberWindows'], as_index=False).DataBase_ID.count()
            QCFailCatchVarSummTab_C   = pd.DataFrame(QCFailCatchVarSummTab_C)
            QCFailCatchVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'NumberWindows':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailCatchVarSummTab_C['CatchVariables'] =QCFailCatchVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailCatchVarSummTab_C = QCFailCatchVarSummTab_C.reset_index(drop=True)
            QCFailCatchVarSummTab_C = pd.DataFrame(QCFailCatchVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailCatchVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailCatchVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

    def Search_DeploymentIdentifier_Backend(DeploymentIdentifier, CatchVariables):
        ListSelecteVariables = ['1: RecordType',
                                '2: AverageTowSpeed',
                                '3: KeptWeight',
                                '4: DiscardWeight',
                                '5: NumberIndividuals',
                                '6: NumberWindows']
        if CatchVariables in ListSelecteVariables:
            try:
                conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
                cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
                cur_DB_SetCatch_Validation_Range.execute("SELECT DataBase_ID, RecordIdentifier, DeploymentUID, RecordType,\
                            AverageTowSpeed, KeptWeight, DiscardWeight,\
                            NumberIndividuals, NumberWindows, QC_Message \
                            FROM SetCatch_QCFailedRange_CatchVariables  WHERE \
                            DeploymentIdentifier = ? ",(DeploymentIdentifier,))
                rows=cur_DB_SetCatch_Validation_Range.fetchall()
                return rows
            except:
                messagebox.showerror('CatchVariables Variable Error Message', "CatchVariables Query Failed")
        
    def InventoryRec2(event):
        ListSelecteVariables = ['1: RecordType',
                                '2: AverageTowSpeed',
                                '3: KeptWeight',
                                '4: DiscardWeight',
                                '5: NumberIndividuals',
                                '6: NumberWindows']
        for nm in tree2.selection():
            sd = tree2.item(nm, 'values')
            DeploymentIdentifier = sd[0]
            SelVariableValue = sd[1]
            CatchVariables = sd[3]
            
            if CatchVariables == ListSelecteVariables[0]:

                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, CatchVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType',
                                            'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                                            'NumberIndividuals', 'NumberWindows','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-RT-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                'NumberIndividuals', 'NumberWindows']]
                MultiSearchRowsDF  = MultiSearchRowsDF.reset_index(drop=True)
                MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
                QCFailedSelectedEntries = len(MultiSearchRowsDF) 
                countIndex = 0
                rows = MultiSearchRowsDF.to_numpy().tolist()
                if rows is not None:
                    for row in rows:
                        if countIndex % 2 == 0:
                            tree1.insert("", tk.END, values=row, tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=row, tags =("odd",))
                        countIndex = countIndex+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                CatchVariables_Display = CatchVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,CatchVariables_Display)

            if CatchVariables == ListSelecteVariables[1]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, CatchVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType', 
                                        'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                                        'NumberIndividuals', 'NumberWindows', 'QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                                    (MultiSearchRowsDF.QC_Message == 'Case-ATS-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                'NumberIndividuals', 'NumberWindows', ]]
                MultiSearchRowsDF  = MultiSearchRowsDF.reset_index(drop=True)
                MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
                QCFailedSelectedEntries = len(MultiSearchRowsDF) 
                countIndex = 0
                rows = MultiSearchRowsDF.to_numpy().tolist()
                if rows is not None:
                    for row in rows:
                        if countIndex % 2 == 0:
                            tree1.insert("", tk.END, values=row, tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=row, tags =("odd",))
                        countIndex = countIndex+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                CatchVariables_Display = CatchVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,CatchVariables_Display)

            if CatchVariables == ListSelecteVariables[2]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, CatchVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType',
                                            'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                                            'NumberIndividuals', 'NumberWindows','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-KW-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                'NumberIndividuals', 'NumberWindows', ]]
                MultiSearchRowsDF  = MultiSearchRowsDF.reset_index(drop=True)
                MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
                QCFailedSelectedEntries = len(MultiSearchRowsDF) 
                countIndex = 0
                rows = MultiSearchRowsDF.to_numpy().tolist()
                if rows is not None:
                    for row in rows:
                        if countIndex % 2 == 0:
                            tree1.insert("", tk.END, values=row, tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=row, tags =("odd",))
                        countIndex = countIndex+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                CatchVariables_Display = CatchVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,CatchVariables_Display)

            if CatchVariables == ListSelecteVariables[3]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, CatchVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType',
                                            'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                                            'NumberIndividuals', 'NumberWindows','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-DW-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                'NumberIndividuals', 'NumberWindows', ]]
                MultiSearchRowsDF  = MultiSearchRowsDF.reset_index(drop=True)
                MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
                QCFailedSelectedEntries = len(MultiSearchRowsDF) 
                countIndex = 0
                rows = MultiSearchRowsDF.to_numpy().tolist()
                if rows is not None:
                    for row in rows:
                        if countIndex % 2 == 0:
                            tree1.insert("", tk.END, values=row, tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=row, tags =("odd",))
                        countIndex = countIndex+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                CatchVariables_Display = CatchVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,CatchVariables_Display)

            if CatchVariables == ListSelecteVariables[4]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, CatchVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType',
                                            'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                                            'NumberIndividuals', 'NumberWindows','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-NI-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                'NumberIndividuals', 'NumberWindows', ]]
                MultiSearchRowsDF  = MultiSearchRowsDF.reset_index(drop=True)
                MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
                QCFailedSelectedEntries = len(MultiSearchRowsDF) 
                countIndex = 0
                rows = MultiSearchRowsDF.to_numpy().tolist()
                if rows is not None:
                    for row in rows:
                        if countIndex % 2 == 0:
                            tree1.insert("", tk.END, values=row, tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=row, tags =("odd",))
                        countIndex = countIndex+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                CatchVariables_Display = CatchVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,CatchVariables_Display)

            if CatchVariables == ListSelecteVariables[5]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, CatchVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType',
                                            'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                                            'NumberIndividuals', 'NumberWindows','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-NW-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                'NumberIndividuals', 'NumberWindows', ]]
                MultiSearchRowsDF  = MultiSearchRowsDF.reset_index(drop=True)
                MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
                QCFailedSelectedEntries = len(MultiSearchRowsDF) 
                countIndex = 0
                rows = MultiSearchRowsDF.to_numpy().tolist()
                if rows is not None:
                    for row in rows:
                        if countIndex % 2 == 0:
                            tree1.insert("", tk.END, values=row, tags =("even",))
                        else:
                            tree1.insert("", tk.END, values=row, tags =("odd",))
                        countIndex = countIndex+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                CatchVariables_Display = CatchVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,CatchVariables_Display)

    def GenQCFailOverview():
        tree1.delete(*tree1.get_children())
        tree3.delete(*tree3.get_children())
        QCFailedVariablesDB= GenQCFailedSummaryTable_Backend()

        ## RecordType fail Count
        QCFail_RecordType = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-RT-RangeQC'))]
        QCFail_RecordType  = QCFail_RecordType.reset_index(drop=True)
        QCFail_RecordType  = pd.DataFrame(QCFail_RecordType)
        Count_QCFail_RecordType = len(QCFail_RecordType)
        
        QC_FailUpdate_RecordType = QCFail_RecordType[(
                (QCFail_RecordType.RecordTypeRangeQC == 'Updated'))]
        
        QC_FailUpdate_RecordType  = QC_FailUpdate_RecordType.reset_index(drop=True)
        QC_FailUpdate_RecordType  = pd.DataFrame(QC_FailUpdate_RecordType)
        UpdateCount_QCFail_RecordType = len(QC_FailUpdate_RecordType)
        
        ## AverageTowSpeed fail Count
        QCFail_AverageTowSpeed = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-ATS-RangeQC'))]
        QCFail_AverageTowSpeed  = QCFail_AverageTowSpeed.reset_index(drop=True)
        QCFail_AverageTowSpeed  = pd.DataFrame(QCFail_AverageTowSpeed)
        Count_QCFail_AverageTowSpeed = len(QCFail_AverageTowSpeed)
        
        QC_FailUpdate_AverageTowSpeed = QCFail_AverageTowSpeed[(
                (QCFail_AverageTowSpeed.AverageTowSpeedRangeQC == 'Updated'))]
        
        QC_FailUpdate_AverageTowSpeed  = QC_FailUpdate_AverageTowSpeed.reset_index(drop=True)
        QC_FailUpdate_AverageTowSpeed  = pd.DataFrame(QC_FailUpdate_AverageTowSpeed)
        UpdateCount_QCFail_AverageTowSpeed = len(QC_FailUpdate_AverageTowSpeed)
        
        ## KeptWeight fail Count
        QCFail_KeptWeight = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-KW-RangeQC'))]
        QCFail_KeptWeight  = QCFail_KeptWeight.reset_index(drop=True)
        QCFail_KeptWeight  = pd.DataFrame(QCFail_KeptWeight)
        Count_QCFail_KeptWeight = len(QCFail_KeptWeight)
        
        QC_FailUpdate_KeptWeight = QCFail_KeptWeight[(
                (QCFail_KeptWeight.KeptWeightRangeQC == 'Updated'))]
        
        QC_FailUpdate_KeptWeight  = QC_FailUpdate_KeptWeight.reset_index(drop=True)
        QC_FailUpdate_KeptWeight  = pd.DataFrame(QC_FailUpdate_KeptWeight)
        UpdateCount_QCFail_KeptWeight = len(QC_FailUpdate_KeptWeight)
        
        ## DiscardWeight fail Count
        QCFail_DiscardWeight = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-DW-RangeQC'))]
        QCFail_DiscardWeight  = QCFail_DiscardWeight.reset_index(drop=True)
        QCFail_DiscardWeight  = pd.DataFrame(QCFail_DiscardWeight)
        Count_QCFail_DiscardWeight = len(QCFail_DiscardWeight)
        
        QC_FailUpdate_DiscardWeight = QCFail_DiscardWeight[(
                (QCFail_DiscardWeight.DiscardWeightRangeQC == 'Updated'))]
        
        QC_FailUpdate_DiscardWeight  = QC_FailUpdate_DiscardWeight.reset_index(drop=True)
        QC_FailUpdate_DiscardWeight  = pd.DataFrame(QC_FailUpdate_DiscardWeight)
        UpdateCount_QCFail_DiscardWeight = len(QC_FailUpdate_DiscardWeight)
        
        ## NumberIndividuals fail Count
        QCFail_NumberIndividuals = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-NI-RangeQC'))]
        QCFail_NumberIndividuals  = QCFail_NumberIndividuals.reset_index(drop=True)
        QCFail_NumberIndividuals  = pd.DataFrame(QCFail_NumberIndividuals)
        Count_QCFail_NumberIndividuals = len(QCFail_NumberIndividuals)
        
        QC_FailUpdate_NumberIndividuals = QCFail_NumberIndividuals[(
                (QCFail_NumberIndividuals.NumberIndividualsRangeQC == 'Updated'))]
        
        QC_FailUpdate_NumberIndividuals  = QC_FailUpdate_NumberIndividuals.reset_index(drop=True)
        QC_FailUpdate_NumberIndividuals  = pd.DataFrame(QC_FailUpdate_NumberIndividuals)
        UpdateCount_QCFail_NumberIndividuals = len(QC_FailUpdate_NumberIndividuals)

        ## NumberWindows fail Count
        QCFail_NumberWindows = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-NW-RangeQC'))]
        QCFail_NumberWindows  = QCFail_NumberWindows.reset_index(drop=True)
        QCFail_NumberWindows  = pd.DataFrame(QCFail_NumberWindows)
        Count_QCFail_NumberWindows = len(QCFail_NumberWindows)
        
        QC_FailUpdate_NumberWindows = QCFail_NumberWindows[(
                (QCFail_NumberWindows.NumberWindowsRangeQC == 'Updated'))]
        
        QC_FailUpdate_NumberWindows  = QC_FailUpdate_NumberWindows.reset_index(drop=True)
        QC_FailUpdate_NumberWindows  = pd.DataFrame(QC_FailUpdate_NumberWindows)
        UpdateCount_QCFail_NumberWindows = len(QC_FailUpdate_NumberWindows)

        ## Building OverviewDF
        ListVariableName = ['RecordType','AverageTowSpeed','KeptWeight','DiscardWeight',
                            'NumberIndividuals','NumberWindows',]
        QCFailCount =   [Count_QCFail_RecordType,
                         Count_QCFail_AverageTowSpeed,
                         Count_QCFail_KeptWeight, 
                         Count_QCFail_DiscardWeight, 
                         Count_QCFail_NumberIndividuals, 
                         Count_QCFail_NumberWindows]
        UpdateQCFailCount =    [UpdateCount_QCFail_RecordType,
                                UpdateCount_QCFail_AverageTowSpeed,
                                UpdateCount_QCFail_KeptWeight, 
                                UpdateCount_QCFail_DiscardWeight, 
                                UpdateCount_QCFail_NumberIndividuals, 
                                UpdateCount_QCFail_NumberWindows]
        QCNullValue = [RecordType_QCNullValue,
                       AverageTowSpeed_QCNullValue,
                       KeptWeight_QCNullValue,
                       DiscardWeight_QCNullValue,
                       NumberIndividuals_QCNullValue,
                       NumberWindows_QCNullValue]
        
        QCFailAppend = {'VariableName': ListVariableName, 
                        'QCFailCount': QCFailCount,
                        'QCFailUpdateCount': UpdateQCFailCount,
                        'QCNullValue':QCNullValue} 
        QCFailSummaryDF = pd.DataFrame(QCFailAppend)
        QCFailSummaryDF[['QCFailCount']] = QCFailSummaryDF[['QCFailCount']].astype(int)
        QCFailSummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
        QCFailSummaryDF  = QCFailSummaryDF.reset_index(drop=True)
        QCFailSummaryDF  = pd.DataFrame(QCFailSummaryDF)
        countIndex1 = 0
        for each_rec in range(len(QCFailSummaryDF)):
            if countIndex1 % 2 == 0:
                tree3.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("even",))
            else:
                tree3.insert("", tk.END, values=list(QCFailSummaryDF.loc[each_rec]), tags =("odd",))
            countIndex1 = countIndex1+1
        tree3.tag_configure("even",foreground="black", background="lightgreen")
        tree3.tag_configure("odd",foreground="black", background="ghost white")

    def InventoryRec3(event):
        ListSelecteVariables = ['RecordType',
                                'AverageTowSpeed',
                                'KeptWeight',
                                'DiscardWeight',
                                'NumberIndividuals',
                                'NumberWindows']
        ListVariableListA = ['1: RecordType',
                            '2: AverageTowSpeed',
                            '3: KeptWeight',
                            '4: DiscardWeight',
                            '5: NumberIndividuals',
                            '6: NumberWindows']
        nm = tree3.selection()
        if len(nm) ==1:
            sd = tree3.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            if SelvariableIdentifier in ListSelecteVariables:

                if SelvariableIdentifier == ListSelecteVariables[0]:
                    QCMsg1 = ("1. RecordType :" + ' QC Range Value Limit: ('+ str(RecordType_LowerRangeLimitValue) + " - " + str(RecordType_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[0]
                    entry_ListToSelViewVarList.current(1)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg1)
                    entry_ListSelecteVariables.current(1)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[1]:
                    QCMsg1 = ("2. AverageTowSpeed :" + ' QC Range Value Limit: ('+ str(AverageTowSpeed_LowerRangeLimitValue) + " - " + str(AverageTowSpeed_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[1]
                    entry_ListToSelViewVarList.current(2)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg1)
                    entry_ListSelecteVariables.current(2)
                    tree2.delete(*tree2.get_children())
            
                if SelvariableIdentifier == ListSelecteVariables[2]:
                    QCMsg2 = ("3. KeptWeight :" + ' QC Range Value Limit: (' + str(KeptWeight_LowerRangeLimitValue) + " - " + str(KeptWeight_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[2]
                    entry_ListToSelViewVarList.current(3)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg2)
                    entry_ListSelecteVariables.current(3)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[3]:
                    QCMsg3 = ("4. DiscardWeight :" + ' QC Range Value Limit: ('+ str(DiscardWeight_LowerRangeLimitValue) + " - " + str(DiscardWeight_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[3]
                    entry_ListToSelViewVarList.current(4)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg3)
                    entry_ListSelecteVariables.current(4)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[4]:
                    QCMsg4 =("5. NumberIndividuals :" + ' QC Range Value Limit: ('+ str(NumberIndividuals_LowerRangeLimitValue) + " - " + str(NumberIndividuals_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[4]
                    entry_ListToSelViewVarList.current(5)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg4)
                    entry_ListSelecteVariables.current(5)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[5]:
                    QCMsg5 =("6. NumberWindows :" + ' QC Range Value Limit: ('+ str(NumberWindows_LowerRangeLimitValue) + " - " + str(NumberWindows_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[5]
                    entry_ListToSelViewVarList.current(6)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg5)
                    entry_ListSelecteVariables.current(6)
                    tree2.delete(*tree2.get_children())

                QCFailDF= viewQCFailed(SelvariableIdentifier)
                QCFailDF  = QCFailDF.reset_index(drop=True)
                QCFailDF  = pd.DataFrame(QCFailDF)
                tree1.delete(*tree1.get_children())
                countIndex1 = 0
                for each_rec in range(len(QCFailDF)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(QCFailDF.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(QCFailDF.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightgreen")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
                QCFailedSelectedEntries = len(QCFailDF)
                txtSelectedFailedEntries.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)

    def callbackFuncSelectView(event):
        ListVariableListA = ['Select QC Variable & View Fail Results',
                                '1: RecordType',
                                '2: AverageTowSpeed',
                                '3: KeptWeight',
                                '4: DiscardWeight',
                                '5: NumberIndividuals',
                                '6: NumberWindows']
        SelVariableView = entry_ListToSelViewVarList.get()
        print('Selected Variable Pair Name :'+ SelVariableView)
        
        if len(SelVariableView)!= 0:
            tree0.delete(*tree0.get_children())
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            entry_ListSelecteVariables.current(0)
           
        if(SelVariableView ==ListVariableListA[0]):
            tree0.delete(*tree0.get_children())
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, 'Select Case QC Variable List From DropDown & Press View QC Failed Results Button To View ')
            entry_ListSelecteVariables.current(0)
        
        if(SelVariableView ==ListVariableListA[1]):
            QCMsg1 = ("1. RecordType :" + ' QC Range Value Limit: ('+ str(RecordType_LowerRangeLimitValue) + " - " + str(RecordType_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg1)
            entry_ListSelecteVariables.current(1)
            entry_UpdateVariableList.current(0)

        if(SelVariableView ==ListVariableListA[2]):
            QCMsg1 = ("2. AverageTowSpeed :" + ' QC Range Value Limit: ('+ str(AverageTowSpeed_LowerRangeLimitValue) + " - " + str(AverageTowSpeed_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg1)
            entry_ListSelecteVariables.current(2)
            entry_UpdateVariableList.current(1)
            
        if(SelVariableView ==ListVariableListA[3]):
            QCMsg2 = ("3. KeptWeight :" + ' QC Range Value Limit: (' + str(KeptWeight_LowerRangeLimitValue) + " - " + str(KeptWeight_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg2)
            entry_ListSelecteVariables.current(3)
            entry_UpdateVariableList.current(2)
        
        if(SelVariableView ==ListVariableListA[4]):
            QCMsg3 = ("4. DiscardWeight :" + ' QC Range Value Limit: ('+ str(DiscardWeight_LowerRangeLimitValue) + " - " + str(DiscardWeight_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg3)
            entry_ListSelecteVariables.current(4)
            entry_UpdateVariableList.current(3)

        if(SelVariableView ==ListVariableListA[5]):
            QCMsg4 =("5. NumberIndividuals :" + ' QC Range Value Limit: ('+ str(NumberIndividuals_LowerRangeLimitValue) + " - " + str(NumberIndividuals_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg4)
            entry_ListSelecteVariables.current(5)
            entry_UpdateVariableList.current(4)
            
        if(SelVariableView ==ListVariableListA[6]):
            QCMsg5 =("6. NumberWindows :" + ' QC Range Value Limit: ('+ str(NumberWindows_LowerRangeLimitValue) + " - " + str(NumberWindows_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg5)
            entry_ListSelecteVariables.current(6)
            entry_UpdateVariableList.current(5)
        
    def ExcelViewEditBackend_RecType_1_2(RangeQCFailDF):
        if len(RangeQCFailDF) >0:
            RangeQCFailDF.sort_values(by=['DeploymentUID','RecordType'], inplace=True)
            RangeQCFailDF  = RangeQCFailDF.reset_index(drop=True)
            RangeQCFailDF  = pd.DataFrame(RangeQCFailDF)   
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(0, 
            'Viewing Range QC Failed Entries Excel File In Seperate Window')
            windows = tk.Toplevel()
            windows.title ("Excel Table View Observer Set & Catch QC Database")
            windows.geometry('1600x855+40+40')
            windows.config(bg="cadet blue")
            frame = tk.Frame(windows)
            frame.pack(fill=BOTH, expand=1)
            pt = Table(frame, dataframe = RangeQCFailDF, showtoolbar=True, showstatusbar=True)
            pt.setRowColors(rows=range(1,len(RangeQCFailDF),2), clr='lightblue', cols='all')
            pt.cellbackgr = 'aliceblue'
            options = config.load_options()
            options = { 'align': 'center',
                        'cellbackgr': '#F4F4F3',
                        'cellwidth': 120,
                        'intprecision': 2,
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
                        ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType', 
                        'AverageTowSpeed', 'KeptWeight', 'DiscardWeight',\
                        'NumberIndividuals', 'NumberWindows']]
                        ).replace(['', None, np.nan, 'None'], 99999999)
                
                Complete_df[['DataBase_ID', 'RecordIdentifier','RecordType']] = Complete_df[
                            ['DataBase_ID', 'RecordIdentifier','RecordType']].astype(int)
                
                Complete_df[['KeptWeight', 'DiscardWeight',
                            'NumberIndividuals', 'NumberWindows', ]] = Complete_df[
                            ['KeptWeight', 'DiscardWeight',
                            'NumberIndividuals', 'NumberWindows']].astype(int)
                
                Complete_df[['AverageTowSpeed']] = Complete_df[
                            ['AverageTowSpeed']].astype(float)
                
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
                conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
                cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
                Complete_df = pd.DataFrame(Complete_df)
                UpdateRecordList_SetCatchDB =[]
                UpdateRecordList_QCFailDB =[]
                df_rows = Complete_df.to_numpy().tolist()
                for row in df_rows:
                    rowValue = row
                    list_item_DataBase_ID = int(rowValue[0])
                    list_item_RecordIdentifier = int(rowValue[1])
                    list_item_DeploymentUID = (rowValue[2])
                    list_item_RecordType = (rowValue[3])
                    list_item_AverageTowSpeed = (rowValue[4])
                    list_item_KeptWeight = (rowValue[5])
                    list_item_DiscardWeight = (rowValue[6])
                    list_item_NumberIndividuals = (rowValue[7])
                    list_item_NumberWindows = (rowValue[8])
                    
                    UpdateRecordList_SetCatchDB.append((
                                        list_item_RecordType,
                                        list_item_AverageTowSpeed,
                                        list_item_KeptWeight,
                                        list_item_DiscardWeight,
                                        list_item_NumberIndividuals,
                                        list_item_NumberWindows,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList_QCFailDB.append((
                                        list_item_RecordType,
                                        list_item_AverageTowSpeed,
                                        list_item_KeptWeight,
                                        list_item_DiscardWeight,
                                        list_item_NumberIndividuals,
                                        list_item_NumberWindows, 
                                        'Updated','Updated','Updated',
                                        'Updated','Updated', 'Updated',
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                                             
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ?, AverageTowSpeed = ?, \
                                                    KeptWeight = ?, DiscardWeight = ?, NumberIndividuals = ?, NumberWindows = ? \
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables SET \
                                        RecordType = ?, AverageTowSpeed = ?, \
                                        KeptWeight = ?, DiscardWeight = ?, \
                                        NumberIndividuals = ?, NumberWindows = ?,\
                                        RecordTypeRangeQC = ?, AverageTowSpeedRangeQC = ?, \
                                        KeptWeightRangeQC = ?, DiscardWeightRangeQC = ?,\
                                        NumberIndividualsRangeQC = ?, NumberWindowsRangeQC = ?\
                                        WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        UpdateRecordList_QCFailDB)
                                            
                conn_DB_Set_Catch_Analysis.commit()
                conn_DB_Set_Catch_Analysis.close()
                conn_DB_SetCatch_Validation_Range.commit()
                conn_DB_SetCatch_Validation_Range.close()

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
                            bg= "cadet blue", text="NB : Edit/Modify AverageTowSpeed/ASOC/DepN/SetN Columns Requires Edit DeplymentUID Accordingly")
            lbl_CautionSteps_1.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_CautionSteps_2 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                bg= "cadet blue", text="NB : Do Not Delete Any Row And Submit")
            lbl_CautionSteps_2.grid(row =12, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            windows.mainloop() 

    def GetSetcatchQCFailDF():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables ;", conn)
            if len(Complete_df) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,
                            ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                            'AverageTowSpeed', 'KeptWeight', 'DiscardWeight','NumberIndividuals', 'NumberWindows', 
                            'RecordTypeRangeQC','AverageTowSpeedRangeQC', 'KeptWeightRangeQC', 
                            'DiscardWeightRangeQC','NumberIndividualsRangeQC', 'NumberWindowsRangeQC',
                            'DeploymentIdentifier']]
                
                SetCatchQCFailedDB_DF= (SetCatchQCFailedDB_DF.loc[:,
                        ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                        'AverageTowSpeed', 'KeptWeight', 'DiscardWeight','NumberIndividuals', 'NumberWindows', 
                        'RecordTypeRangeQC','AverageTowSpeedRangeQC', 'KeptWeightRangeQC', 'DiscardWeightRangeQC',
                        'NumberIndividualsRangeQC', 'NumberWindowsRangeQC',
                        'DeploymentIdentifier']]
                        ).replace(['', None, np.nan, 'None'], 99999999)
                
                SetCatchQCFailedDB_DF[['DataBase_ID', 'RecordIdentifier','RecordType', 
                            'KeptWeight', 'DiscardWeight',
                            'NumberIndividuals', 'NumberWindows']] = SetCatchQCFailedDB_DF[
                            ['DataBase_ID', 'RecordIdentifier','RecordType', 
                            'KeptWeight', 'DiscardWeight',
                            'NumberIndividuals', 'NumberWindows']].astype(int)
                
                SetCatchQCFailedDB_DF[['AverageTowSpeed']] = SetCatchQCFailedDB_DF[
                            ['AverageTowSpeed']].astype(float)
                               
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace([99999999, 99999999.0, '99999999'], '')
                SetCatchQCFailedDB_DF.drop_duplicates(subset=['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType'], 
                                        keep='last', inplace = True)
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

    def QCFailedExcelViewAll():
        txtDisplayMessageSystem.delete(0,END)
        txtDisplayMessageSystem.insert(0, 
            'Viewing QC Failed Excel File In Seperate Window')
        QC_FailConsistency_DF = GetSetcatchQCFailDF()
        ExcelViewEditBackend_RecType_1_2(QC_FailConsistency_DF)

    def UpdateDeploymentUIDAfterUpdate():
        ## Defining Functions
        def UpdateSetcatchDB():

            def GetSetCatchProfileDB():
                try:
                    conn = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = conn.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ;", conn)
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
       
    def ApplyUpdateDeploymentUIDAfterUpdate():
        UpdateDeploymentUIDAfterUpdate()
        tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

    def SetcatchDB_VariableList():
        GetSetCatchDB_VariableList = ['RecordType', 'AverageTowSpeed', 'KeptWeight', 
                         'DiscardWeight', 'NumberIndividuals', 'NumberWindows']
        return GetSetCatchDB_VariableList

    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                         UpdateRecordList_QCFailDB):
        GetSetCatchDB_VariableList = SetcatchDB_VariableList()
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()

        conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
        cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
        
        ## Updaing SetCatch DB
        if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables\
                    SET RecordType = ?, RecordTypeRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList)
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables\
                    SET AverageTowSpeed = ?, AverageTowSpeedRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET KeptWeight = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables\
                    SET KeptWeight = ?, KeptWeightRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DiscardWeight = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables\
                    SET DiscardWeight = ?, DiscardWeightRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)
                
        if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberIndividuals = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables\
                    SET NumberIndividuals = ?, NumberIndividualsRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)
            
        if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberWindows = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_CatchVariables\
                    SET NumberWindows = ?, NumberWindowsRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)
        
        conn_DB_Set_Catch_Analysis.close()
        conn_DB_SetCatch_Validation_Range.commit()
        conn_DB_SetCatch_Validation_Range.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18=['RecordType']
            Var_Class_String7 =['DeploymentUID']
            Var_Class_IntB27  = ['KeptWeight', 
                                'DiscardWeight', 'NumberIndividuals', 'NumberWindows']
            Var_Class_FloatB27  = ['AverageTowSpeed']
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
            
            if get_Updated_Variable in Var_Class_FloatB27:
                if(len(get_UpdateValue_UpdatedVariable)!=0):
                    try:
                        get_UpdateValue_UpdatedVariable = float(get_UpdateValue_UpdatedVariable)
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
        get_UpdateValue_UpdatedVariable = QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable)
        if (get_UpdateValue_UpdatedVariable != ReturnFail) & (len(get_Updated_Variable)!=0):
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
                    for item in tree1.selection():
                        list_item = (tree1.item(item, 'values'))
                        list_item_DatabaseUID = int(list_item[0])
                        list_item_RecordIdentifier = int(list_item[1])
                        list_item_DeploymentUID = (list_item[2])
                        list_item_QCMsg = 'Updated'
                        UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                 list_item_DatabaseUID,
                                                 list_item_RecordIdentifier,
                                                 list_item_DeploymentUID))
                        UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,
                                                          list_item_QCMsg,  
                                                          list_item_DatabaseUID,
                                                          list_item_RecordIdentifier,
                                                          list_item_DeploymentUID))
                    Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                                     UpdateRecordList_QCFailDB)
                    viewQCFailed_VariablesProfile()
                    tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")
                    
                if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)==''):
                    iUpdateSlected = tkinter.messagebox.askyesno("Update Variable Missing Value Message", 
                                                                "Selected Variable Has Empty Value To Update. Do You Like TO Proceed Update?")
                    if iUpdateSlected >0:
                        UpdateRecordList =[]
                        UpdateRecordList_QCFailDB =[]
                        for item in tree1.selection():
                            list_item = (tree1.item(item, 'values'))
                            list_item_DatabaseUID = int(list_item[0])
                            list_item_RecordIdentifier = int(list_item[1])
                            list_item_DeploymentUID = (list_item[2])
                            list_item_QCMsg = 'Updated'
                            UpdateRecordList.append((get_UpdateValue_UpdatedVariable, 
                                                     list_item_DatabaseUID,
                                                     list_item_RecordIdentifier,
                                                     list_item_DeploymentUID))
                            UpdateRecordList_QCFailDB.append((get_UpdateValue_UpdatedVariable,
                                                            list_item_QCMsg,
                                                            list_item_DatabaseUID,
                                                            list_item_RecordIdentifier,
                                                            list_item_DeploymentUID))
                            
                        Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList, 
                                                         UpdateRecordList_QCFailDB)
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
                                "Please Check Variable DataType And Follow Proper Update Step") 

    # Tree 1 & 2 View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    tree2.bind('<<TreeviewSelect>>',InventoryRec2)
    tree3.bind('<<TreeviewSelect>>',InventoryRec3)
    ## ComboBox Select Event
    entry_ListToSelViewVarList.bind('<<ComboboxSelected>>', callbackFuncSelectView)
    # Generate Deployment Identifier Column In QC Failed DB
    GenDepIdfier_Col_SetCatchFailDB()
    GenQCFailOverview()
    QCFailedTotalEntries()

    ## Button Wizard : UpdateSelectedDepUID
    btnModifyCatchVariablesProfile = Button(TopLeftframe, text="Update Selected DepUID\n(DB Update)", font=('aerial', 10, 'bold'), fg="blue",
                            height =2, width=25, bd=2, command = UpdateSelectedDepUID)
    btnModifyCatchVariablesProfile.grid(row =15, column = 0, padx=2, pady =5, ipady =5, sticky =W)

    btnClearDetails = Button(TopLeftframe, text="Clear", font=('aerial', 10, 'bold'),
                            height =1, width=4, bd=1, command = ClearProfile)
    btnClearDetails.grid(row =2, column = 0, padx=2, pady =1, ipady =5, sticky =E)

    button_UpdateSelectedDBEntries = Button(UpdateDB_Entryframe, bd = 1, text ="Update Selected Entries\n (DB Update)", width = 25,
                                height=2, font=('aerial', 10, 'bold'), fg="blue",
                                command =UpdateSelected_SetCatch_DBEntries)
    button_UpdateSelectedDBEntries.grid(row =14, column = 0, padx=2, pady =2, ipady =4, sticky =W)

    ## Button Wizard : Table B
    btnViewQCFailedQCResults = Button(TopRightframe, text="View Selected QC Results", font=('aerial', 10, 'bold'), bg='alice blue',
                            height =1, width=22, bd=2, command = viewQCFailed_VariablesProfile)
    btnViewQCFailedQCResults.grid(row =2, column = 0, padx=485, pady =2, ipady =2, sticky =W)

    btnClearTable = Button(TopRightframe, text="Clear Tables", font=('aerial', 10, 'bold'), bg='alice blue',
                                height =1, width=11, bd=1, command = ClearTablesAll)
    btnClearTable.grid(row =2, column = 0, padx=100, pady =1, ipady =2, sticky =E)

    ### Button Generate QC fail Report
    btnGenQCFailReport = Button(TopRightframe, text="Generate QC Fail Overview", font=('aerial', 11, 'bold'), bg='alice blue',
                                height =1, width=25, bd=2, command = GenQCFailOverview)
    btnGenQCFailReport.grid(row=6, column = 0, padx=10, pady =1, sticky =W, rowspan =1)

    btnGenDepSummary = Button(TopRightframe, text="Run Deployment Summary", font=('aerial', 11, 'bold'), bg='alice blue',
                                height =1, width=22, bd=2, command = GenQCFailedDepSummaryTable)
    btnGenDepSummary.grid(row=6, column = 0, padx=70, pady =1, sticky =E, rowspan =1)

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
    Update.add_command(label="Update DeplymentUID", command=ApplyUpdateDeploymentUIDAfterUpdate)
   
    Treepopup.add_command(label="Exit", command=iExit)
    Treepopup.add_command(label="Modify & Update DB With Selected CatchVariables In Table C", command=Modify_MultipleSetCatch_CatchVariablesProfile)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack(side = LEFT)
    window.mainloop()



