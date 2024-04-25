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

def ViewRangeValidatedResult_PositionalVariables():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Range Validator - ID-C-02-1")
    window.geometry("1340x838+200+100")
    window.config(bg="cadet blue")
    window.resizable(0, 0)
    ## Positional Variables Limit Fetching
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
    PP_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[5,'LowerRangeLimitValue'])
    PP_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[5,'UpperRangeLimitValue'])
    PP_QCNullValue= Get_RangeLimitVariables.at[5,'QCNullValue']

    SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
    SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
    SLat_QCNullValue= Get_RangeLimitVariables.at[6,'QCNullValue']

    SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
    SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
    SLon_QCNullValue= Get_RangeLimitVariables.at[7,'QCNullValue']

    ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
    ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
    ELat_QCNullValue= Get_RangeLimitVariables.at[8,'QCNullValue']

    ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
    ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
    ELon_QCNullValue= Get_RangeLimitVariables.at[9,'QCNullValue']

    IO200ML_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[10,'LowerRangeLimitValue'])
    IO200ML_UpperRangeLimitValue=  int(Get_RangeLimitVariables.at[10,'UpperRangeLimitValue'])
    IO200ML_QCNullValue= Get_RangeLimitVariables.at[10,'QCNullValue']


    ## Top Main Frame
    TopMainFrame = Frame(window, bd = 2, padx= 1, pady= 1, relief = RIDGE)
    TopMainFrame.grid(row =0, column = 0, padx=1, pady =1, sticky =W, rowspan =1)

    ## Top Left Frame - Positional profile
    TopLeftframe = Frame(TopMainFrame, bd = 1, padx= 1, pady= 1, relief = RIDGE)
    TopLeftframe.grid(row =0, column = 0, padx=1, pady =1, sticky =W, rowspan =1, columnspan =1)
    DataBase_ID       = IntVar(TopLeftframe, value='')
    RecordIdentifier  = IntVar(TopLeftframe, value='')
    DeploymentUID     = StringVar(TopLeftframe)
    PositionPrecision  = IntVar(TopLeftframe, value='')
    StartLatitude  = IntVar(TopLeftframe, value='')
    StartLongitude  = IntVar(TopLeftframe, value='')
    EndLatitude  = IntVar(TopLeftframe, value='')
    EndLongitude  = IntVar(TopLeftframe, value='')
    InOut200MileLimit  = IntVar(TopLeftframe, value='')

    lblTitEntry = Label(TopLeftframe, font=('aerial', 11, 'bold'), text=" Positional Variables Profile: ")
    lblTitEntry.grid(row =0, column = 0, padx=0, pady =1, sticky =W, rowspan =1)

    lblDeploymentUID = Label(TopLeftframe, font=('aerial', 10, 'bold'), text = "0. DeploymentUID :", padx =0, pady= 2)
    lblDeploymentUID.grid(row =2, column = 0, padx=4, pady =2, sticky =W)
    txtDeploymentUID  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable = DeploymentUID, state=DISABLED, width = 18)
    txtDeploymentUID.grid(row =3, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblPositionPrecisionCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), 
    text = ("1. PositionPrecision :" + ' ('+ str(PP_LowerRangeLimitValue) + " - " + str(PP_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblPositionPrecisionCode.grid(row =4, column = 0, padx=4, pady =2, sticky =W)
    txtPositionPrecision  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= PositionPrecision, width = 18)
    txtPositionPrecision.grid(row =5, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblStartLatitudeCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), 
    text = ("2. StartLatitude :" + ' (' + str(SLat_LowerRangeLimitValue) + " - " + str(SLat_UpperRangeLimitValue) + ')'),
    padx =0, pady= 2)
    lblStartLatitudeCode.grid(row =6, column = 0, padx=0, pady =2, sticky =W)
    txtStartLatitude  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= StartLatitude, width = 18)
    txtStartLatitude.grid(row =7, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblStartLongitudeCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), 
    text = ("3. StartLongitude :" + ' ('+ str(SLon_LowerRangeLimitValue) + " - " + str(SLon_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblStartLongitudeCode.grid(row =8, column = 0, padx=4, pady =2, sticky =W)
    txtStartLongitude  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= StartLongitude, width = 18)
    txtStartLongitude.grid(row =9, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblEndLatitudeCode = Label(TopLeftframe, font=('aerial', 10, 'bold'),
    text = ("4. EndLatitude :" + ' ('+ str(ELat_LowerRangeLimitValue) + " - " + str(ELat_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblEndLatitudeCode.grid(row =10, column = 0, padx=4, pady =2, sticky =W)
    txtEndLatitude  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= EndLatitude, width = 18)
    txtEndLatitude.grid(row =11, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblEndLongitudeCode = Label(TopLeftframe, font=('aerial', 10, 'bold'),
    text = ("5. EndLongitude :" + ' ('+ str(ELon_LowerRangeLimitValue) + " - " + str(ELon_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblEndLongitudeCode.grid(row =12, column = 0, padx=4, pady =2, sticky =W)
    txtEndLongitude  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= EndLongitude, width = 18)
    txtEndLongitude.grid(row =13, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    lblInOut200MileLimitCode = Label(TopLeftframe, font=('aerial', 10, 'bold'),
    text = ("6. InOut200MileLimit :" + ' ('+ str(IO200ML_LowerRangeLimitValue) + " - " + str(IO200ML_UpperRangeLimitValue) + ')'), 
    padx =0, pady= 2)
    lblInOut200MileLimitCode.grid(row =14, column = 0, padx=4, pady =2, sticky =W)
    txtInOut200MileLimit  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= InOut200MileLimit, width = 18)
    txtInOut200MileLimit.grid(row =15, column = 0, padx=25, pady =4,ipadx=1, sticky =W)

    ### Fail Count
    lbl_TotalFailedEntries = Label(TopLeftframe, font=('aerial', 9 , 'bold'), text="Total QC Failed Entries :")
    lbl_TotalFailedEntries.grid(row =17, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(TopLeftframe, value='')
    txtTotalFailedEntries = Entry(TopLeftframe, font=('aerial',9),textvariable = TotalFailedEntries, width = 8, bd=1)
    txtTotalFailedEntries.grid(row =18, column = 0, padx=40, pady =1, ipady =1, sticky =W)

    lbl_SelectedFailedEntries = Label(TopLeftframe, font=('aerial', 10, 'bold'), text="Selected QC Failed Entries :")
    lbl_SelectedFailedEntries.grid(row =19, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    SelectedFailedEntries = IntVar(TopLeftframe, value='')
    txtSelectedFailedEntries = Entry(TopLeftframe, font=('aerial', 9),textvariable = SelectedFailedEntries, width = 8, bd=2)
    txtSelectedFailedEntries.grid(row =20, column = 0, padx=40, pady =1, ipady =1, sticky =W)

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
    
    ListVariableListA = ['PositionPrecision', 'StartLatitude', 'StartLongitude',
                         'EndLatitude', 'EndLongitude', 'InOut200MileLimit']
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
    TableMargin0.grid(row =1, column = 0, padx=0, pady =1, sticky =W, rowspan =1)
    tree0 = ttk.Treeview(TableMargin0, 
            column=("column1", "column2", "column3","column4", "column5", "column6"), 
            height=1, show='headings')
    tree0.heading("#1", text="QCPositionPrecision", anchor=CENTER)
    tree0.heading("#2", text="QCStartLatitude", anchor=CENTER)
    tree0.heading("#3", text="QCStartLongitude", anchor=CENTER)
    tree0.heading("#4", text="QCEndLatitude", anchor=CENTER)
    tree0.heading("#5", text="QCEndLongitude", anchor=CENTER)
    tree0.heading("#6", text="QCInOut200MileLimit", anchor=CENTER)
    tree0.column('#1', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree0.column('#2', stretch=NO, minwidth=0, width=165, anchor = tk.CENTER)
    tree0.column('#3', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)            
    tree0.column('#4', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree0.column('#5', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree0.column('#6', stretch=NO, minwidth=0, width=180, anchor = tk.CENTER)
    tree0.pack()
    
    ## Table B: View QC Failed Results Table
    lblTableB = Label(TopRightframe, font=('aerial', 11, 'bold'), text="B: QC Failed Results")
    lblTableB.grid(row =2, column = 0, padx=5, pady =2, ipady =2, sticky =W, rowspan =1)
    ListToSelViewVarList = ['Select QC Variable & View Fail Results',
                                '1: PositionPrecision',
                                '2: StartLatitude',
                                '3: StartLongitude',
                                '4: EndLatitude',
                                '5: EndLongitude',
                                '6: InOut200MileLimit']
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
                                            "column9", "column10"), height=18, show='headings')
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
    tree1.heading("#5", text="PositionPrecision", anchor=CENTER)
    tree1.heading("#6", text="StartLatitude", anchor=CENTER)
    tree1.heading("#7", text="StartLongitude", anchor=CENTER)
    tree1.heading("#8", text="EndLatitude", anchor=CENTER)
    tree1.heading("#9", text="EndLongitude", anchor=CENTER)
    tree1.heading("#10", text="InOut200MileLimit", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=0, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=157, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=140, anchor = tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=135, anchor = tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree1.column('#9', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree1.column('#10', stretch=NO, minwidth=0, width=175, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 9), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 9,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)
    tree1.pack()

    ## Bottom Left
    SummaryQCframe = tk.Frame(TopRightframe, bd = 2,relief = RIDGE, bg= "cadet blue")
    SummaryQCframe.grid(row=5, column = 0, padx=1, pady =1, sticky =W, rowspan =1)

    Summaryframe = tk.Frame(SummaryQCframe, bg= "aliceblue")
    tree3 = ttk.Treeview(Summaryframe, column=("column1", "column2", "column3", "column4"),height=8, show='headings')
    scrollbary = ttk.Scrollbar(Summaryframe, orient ="vertical", command=tree3.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree3.configure(yscrollcommand = scrollbary.set)
    tree3.heading("#1", text="QC Variable Name", anchor = W)
    tree3.heading("#2", text="# Of Fail Entries")
    tree3.heading("#3", text="# Of Entries Updated")
    tree3.heading("#4", text="QC Null Value")
    tree3.column('#1', stretch=NO, minwidth=0, width=135, anchor = W)            
    tree3.column('#2', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    tree3.column('#3', stretch=NO, minwidth=0, width=145, anchor = tk.CENTER)
    tree3.column('#4', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
    Summaryframe.pack(side = BOTTOM, pady=0)
    tree3.pack(side = BOTTOM)
    SummaryDisplay = tk.Frame(SummaryQCframe, bg= "aliceblue")
    lblTableC = Label(SummaryQCframe, font=('aerial', 11, 'bold'), text="C: QC Fail OverView", bg='cadet blue')
    lblTableC.pack(side =LEFT, anchor = E)
    SummaryDisplay.pack(side = LEFT, pady=0)

    ## Bottom Right
    DepSummaryframe = Frame(TopRightframe, bd = 1, padx= 1, pady= 1, relief = RIDGE, bg='cadet blue')
    DepSummaryframe.grid(row=5, column = 0, padx=80, pady =1, sticky =E, rowspan =1)
    
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
    tree2.column('#1', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)            
    tree2.column('#2', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    tree2.column('#3', stretch=NO, minwidth=0, width=110, anchor = tk.CENTER)
    tree2.column('#4', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
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
                                '1: PositionPrecision',
                                '2: StartLatitude',
                                '3: StartLongitude',
                                '4: EndLatitude',
                                '5: EndLongitude',
                                '6: InOut200MileLimit']
    entry_ListSelecteVariables  = ttk.Combobox(TopRightframe, font=('aerial', 10, 'bold'), 
                                                width = 45, state='readonly')
    entry_ListSelecteVariables['values'] = ListSelecteVariables
    entry_ListSelecteVariables.current(0)
    entry_ListSelecteVariables.grid(row=6, column = 0, padx=300, pady =1, sticky =E, rowspan =1)

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
                    PositionPrecision = (df.loc[:,'PositionPrecision']).fillna(99999999).astype(int, errors='ignore')
                    StartLatitude=(df.loc[:,'StartLatitude']).fillna(99999999).astype(float, errors='ignore')
                    StartLongitude=(df.loc[:,'StartLongitude']).fillna(99999999).astype(float, errors='ignore')
                    EndLatitude= (df.loc[:,'EndLatitude']).fillna(99999999).astype(float, errors='ignore')
                    EndLongitude= (df.loc[:,'EndLongitude']).fillna(99999999).astype(float, errors='ignore')
                    InOut200MileLimit = (df.loc[:,'InOut200MileLimit']).fillna(99999999).astype(int, errors='ignore')
                    column_names = [DataBase_ID, RecordIdentifier, DeploymentUID, RecordType,
                                    PositionPrecision,StartLatitude, StartLongitude, 
                                    EndLatitude, EndLongitude, InOut200MileLimit]
                    catdf = pd.concat (column_names,axis=1,ignore_index =True)
                    catdf.rename(columns={0:'DataBase_ID', 1:'RecordIdentifier', 
                                          2:'DeploymentUID', 3:'RecordType',
                                          4:'PositionPrecision', 5:'StartLatitude',
                                          6:'StartLongitude', 7:'EndLatitude', 
                                          8:'EndLongitude', 9:'InOut200MileLimit'},inplace = True)
                    Raw_Imported_Df = pd.DataFrame(catdf)
                    Raw_Imported_Df['DataBase_ID']=(Raw_Imported_Df.loc[:,'DataBase_ID']).astype(int, errors='ignore')
                    Raw_Imported_Df['RecordIdentifier']=(Raw_Imported_Df.loc[:,'RecordIdentifier']).astype(int, errors='ignore')
                    Raw_Imported_Df['RecordType']=(Raw_Imported_Df.loc[:,'RecordType']).astype(int, errors='ignore')
                    Raw_Imported_Df['PositionPrecision']=(Raw_Imported_Df.loc[:,'PositionPrecision']).astype(int, errors='ignore')
                    Raw_Imported_Df['StartLatitude']=(Raw_Imported_Df.loc[:,'StartLatitude']).astype(float, errors='ignore')
                    Raw_Imported_Df['StartLongitude']=(Raw_Imported_Df.loc[:,'StartLongitude']).astype(float, errors='ignore')
                    Raw_Imported_Df['EndLatitude']= (Raw_Imported_Df.loc[:,'EndLatitude']).astype(float, errors='ignore')
                    Raw_Imported_Df['EndLongitude']= (Raw_Imported_Df.loc[:,'EndLongitude']).astype(float, errors='ignore')
                    Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                    Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0], '')
                    Raw_Imported_Df = Raw_Imported_Df.replace(8888888, 'None')
                    Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                    Raw_Imported_Df = pd.DataFrame(Raw_Imported_Df)
                    CheckEmptyNessColumn = Raw_Imported_Df[
                                        (Raw_Imported_Df.DataBase_ID=='') |
                                        (Raw_Imported_Df.RecordIdentifier=='') |
                                        (Raw_Imported_Df.PositionPrecision=='')]
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
                                list_item_PositionPrecision = (rowValue[4])
                                list_item_StartLatitude = (rowValue[5])
                                list_item_StartLongitude = (rowValue[6])
                                list_item_EndLatitude = (rowValue[7])
                                list_item_EndLongitude = (rowValue[8])
                                list_item_InOut200MileLimit = (rowValue[9])

                                UpdateRecordList_SetCatchDB.append((
                                                    list_item_RecordType,
                                                    list_item_PositionPrecision,
                                                    list_item_StartLatitude,
                                                    list_item_StartLongitude,
                                                    list_item_EndLatitude,
                                                    list_item_EndLongitude,
                                                    list_item_InOut200MileLimit,
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                                
                                UpdateRecordList_QCFailDB.append((
                                                    list_item_RecordType,
                                                    list_item_PositionPrecision,
                                                    list_item_StartLatitude,
                                                    list_item_StartLongitude,
                                                    list_item_EndLatitude,
                                                    list_item_EndLongitude, 
                                                    list_item_InOut200MileLimit, 
                                                    'Updated','Updated','Updated',
                                                    'Updated','Updated','Updated',
                                                    list_item_DataBase_ID,
                                                    list_item_RecordIdentifier,
                                                    list_item_DeploymentUID))
                            ## DB Update Executing
                            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ?, PositionPrecision = ?, \
                                                    StartLatitude = ?, StartLongitude = ?, EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =? \
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables SET RecordType = ?, PositionPrecision = ?, \
                                                    StartLatitude = ?, StartLongitude = ?, EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =?, \
                                                    PositionPrecisionRangeQC = ?, StartLatitudeRangeQC = ?, StartLongitudeRangeQC = ?,\
                                                    EndLatitudeRangeQC = ?, EndLongitudeRangeQC = ?, InOut200MileLimitRangeQC =?\
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
                            SetCatchQCFailedDB_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC ;", 
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
                            SetCatchProfileDB_DF['PositionPrecision']=(SetCatchProfileDB_DF.loc[:,'PositionPrecision']).astype(int, errors='ignore')
                            SetCatchProfileDB_DF['StartLatitude']=(SetCatchProfileDB_DF.loc[:,'StartLatitude']).astype(float, errors='ignore')
                            SetCatchProfileDB_DF['StartLongitude']=(SetCatchProfileDB_DF.loc[:,'StartLongitude']).astype(float, errors='ignore')
                            SetCatchProfileDB_DF['EndLatitude']= (SetCatchProfileDB_DF.loc[:,'EndLatitude']).astype(float, errors='ignore')
                            SetCatchProfileDB_DF['EndLongitude']= (SetCatchProfileDB_DF.loc[:,'EndLongitude']).astype(float, errors='ignore')
                            SetCatchProfileDB_DF['InOut200MileLimit']= (SetCatchProfileDB_DF.loc[:,'InOut200MileLimit']).astype(int, errors='ignore')
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
                            SetCatchQCFailedDB_DF['PositionPrecision']=(SetCatchQCFailedDB_DF.loc[:,'PositionPrecision']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['StartLatitude']=(SetCatchQCFailedDB_DF.loc[:,'StartLatitude']).astype(float, errors='ignore')
                            SetCatchQCFailedDB_DF['StartLongitude']=(SetCatchQCFailedDB_DF.loc[:,'StartLongitude']).astype(float, errors='ignore')
                            SetCatchQCFailedDB_DF['EndLatitude']= (SetCatchQCFailedDB_DF.loc[:,'EndLatitude']).astype(float, errors='ignore')
                            SetCatchQCFailedDB_DF['EndLongitude']= (SetCatchQCFailedDB_DF.loc[:,'EndLongitude']).astype(float, errors='ignore')
                            SetCatchQCFailedDB_DF['InOut200MileLimit']=(SetCatchQCFailedDB_DF.loc[:,'InOut200MileLimit']).astype(int, errors='ignore')
                            SetCatchQCFailedDB_DF['PositionPrecisionRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['StartLatitudeRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['StartLongitudeRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['EndLatitudeRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['EndLongitudeRangeQC']='Updated'
                            SetCatchQCFailedDB_DF['InOut200MileLimitRangeQC']='Updated'
                            try:
                                Submit_To_DBStorage = pd.DataFrame(SetCatchQCFailedDB_DF)
                                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_PositionalVariables', 
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
                        messagebox.showerror('Empty Values In Variable Columns', "Please Check DataBase_ID, RecordIdentifier, PositionPrecision Columns")

    def Export_FailedCSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC ;", conn)
            Complete_df = Complete_df.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                 'PositionPrecision', 'StartLatitude', 'StartLongitude',
                 'EndLatitude', 'EndLongitude', 'InOut200MileLimit',
                 'PositionPrecisionRangeQC', 'StartLatitudeRangeQC', 'StartLongitudeRangeQC',
                 'EndLatitudeRangeQC', 'EndLongitudeRangeQC', 'InOut200MileLimitRangeQC']]
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
                    tkinter.messagebox.showinfo("QC Failed PositionalVariables Profile","QC Failed PositionalVariables Profile Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("QC Failed PositionalVariables Profile Report Message","Please Select File Name To Export")
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
                                '1: PositionPrecision',
                                '2: StartLatitude',
                                '3: StartLongitude',
                                '4: EndLatitude',
                                '5: EndLongitude',
                                '6: InOut200MileLimit']
        if getVarnameToView == ListVariableListA[1]:
            QCMsgVariable = 'Case-PP-RangeQC'
        if getVarnameToView == ListVariableListA[2]:
            QCMsgVariable = 'Case-SLat-RangeQC'
        if getVarnameToView == ListVariableListA[3]:
            QCMsgVariable = 'Case-SLon-RangeQC'
        if getVarnameToView == ListVariableListA[4]:
            QCMsgVariable = 'Case-ELat-RangeQC'
        if getVarnameToView == ListVariableListA[5]:
            QCMsgVariable = 'Case-ELon-RangeQC'
        if getVarnameToView == ListVariableListA[6]:
            QCMsgVariable = 'Case-IO200ML-RangeQC'
       
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_Range)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows, 
            columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                      'PositionPrecision', 'StartLatitude', 'StartLongitude',
                      'EndLatitude', 'EndLongitude', 'InOut200MileLimit',
                      'PositionPrecisionRangeQC', 'StartLatitudeRangeQC', 'StartLongitudeRangeQC',
                      'EndLatitudeRangeQC', 'EndLongitudeRangeQC', 'InOut200MileLimitRangeQC', 
                      'DeploymentIdentifier', 'QC_Message'])
            
            rows = rows[((rows['QC_Message'] == QCMsgVariable)
                        )]
            rows = rows.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
            
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
        ListVariableListA = ['1: PositionPrecision',
                            '2: StartLatitude',
                            '3: StartLongitude',
                            '4: EndLatitude',
                            '5: EndLongitude',
                            '6: InOut200MileLimit']
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
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        QCFailedTotalEntries = len(data)       
        txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)             
        conn.commit()
        conn.close()

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP PositionalVariables Profile", "Confirm If You Want To Exit")
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

        txtPositionPrecision.delete(0,END)
        txtStartLatitude.delete(0,END)
        txtStartLongitude.delete(0,END)
        txtEndLatitude.delete(0,END)
        txtEndLongitude.delete(0,END)
        txtInOut200MileLimit.delete(0,END)
        
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
                        PositionPrecision = int(txtPositionPrecision.get())
                    except:
                        PositionPrecision = (txtPositionPrecision.get())
                    try:
                        StartLatitude = float(txtStartLatitude.get())
                    except:
                        StartLatitude = (txtStartLatitude.get())
                    try:
                        StartLongitude = float(txtStartLongitude.get())
                    except:
                        StartLongitude = (txtStartLongitude.get())
                    try:
                        EndLatitude = float(txtEndLatitude.get())
                    except:
                        EndLatitude = (txtEndLatitude.get())
                    try:
                        EndLongitude = float(txtEndLongitude.get())
                    except:
                        EndLongitude = (txtEndLongitude.get())
                    try:
                        InOut200MileLimit = int(txtInOut200MileLimit.get())
                    except:
                        InOut200MileLimit = txtInOut200MileLimit.get()
                    
                    if (PositionPrecision!=''):
                        ## DB Connect
                        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                        
                        conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
                        cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
                        
                        ## DB Update
                        cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ?, \
                            StartLatitude = ?, StartLongitude = ?, \
                            EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =? \
                            WHERE DeploymentUID =?", 
                            (PositionPrecision, StartLatitude, StartLongitude, \
                            EndLatitude, EndLongitude, InOut200MileLimit, \
                            list_item_DeploymentUID))
                        
                        cur_DB_SetCatch_Validation_Range.execute("UPDATE SetCatch_QCFailedRange_PositionalVariables SET PositionPrecision = ?, \
                            StartLatitude = ?, StartLongitude = ?, \
                            EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =?, \
                            PositionPrecisionRangeQC = ?, StartLatitudeRangeQC = ?, StartLongitudeRangeQC = ?,\
                            EndLatitudeRangeQC = ?, EndLongitudeRangeQC = ?, InOut200MileLimitRangeQC =?\
                            WHERE DeploymentUID =?", 
                            (PositionPrecision, StartLatitude, StartLongitude, \
                            EndLatitude, EndLongitude, InOut200MileLimit, 'Updated','Updated','Updated',\
                            'Updated','Updated','Updated', list_item_DeploymentUID))
                        
                        conn_DB_Set_Catch_Analysis.commit()
                        conn_DB_Set_Catch_Analysis.close()
                        
                        conn_DB_SetCatch_Validation_Range.commit()
                        conn_DB_SetCatch_Validation_Range.close()

                        tree1.delete(*tree1.get_children())
                        tree1.insert("", tk.END,values=(list_item_DatabaseUID, 
                                                        list_item_RecordIdentifier, 
                                                        list_item_DeploymentUID,
                                                        list_item_RecordType,
                                                        PositionPrecision,
                                                        StartLatitude, 
                                                        StartLongitude, 
                                                        EndLatitude, 
                                                        EndLongitude, 
                                                        InOut200MileLimit))
                    else:
                        tkinter.messagebox.showinfo("Update Error",
                                            "PositionPrecision Variables CanNot Be Null")
            else:
                UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                        "1. Please Select One Entry Only From The PositionalVariables Table To Update "  + '\n' + '\n' + 
                        "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                        "3. Please Do Not Update Without Selecting Entry From PositionalVariables Table" )
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
            cur_DB_SetCatch_Validation_Range.execute("SELECT PositionPrecisionRangeQC, StartLatitudeRangeQC, StartLongitudeRangeQC,\
                                                    EndLatitudeRangeQC, EndLongitudeRangeQC, InOut200MileLimitRangeQC \
                                                    FROM SetCatch_QCFailedRange_PositionalVariables WHERE \
                                                    (DataBase_ID = :DataBase_ID) AND\
                                                    (RecordIdentifier = :RecordIdentifier) AND\
                                                    (DeploymentUID= :DeploymentUID)",\
                                                    (DataBase_ID, RecordIdentifier, DeploymentUID))
            rows=cur_DB_SetCatch_Validation_Range.fetchall()
            return rows
        except:
            messagebox.showerror('PositionalVariables Variable Error Message', "PositionalVariables Query Failed")

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
                columns =['PositionPrecisionRangeQC', 
                        'StartLatitudeRangeQC', 
                        'StartLongitudeRangeQC',
                        'EndLatitudeRangeQC', 
                        'EndLongitudeRangeQC', 
                        'InOut200MileLimitRangeQC'])
                GetDisplayMessageDF.reset_index(drop=True)
                GetDisplayMessageDF  = pd.DataFrame(GetDisplayMessageDF)
                Tree0ViewBackend(GetDisplayMessageDF)

                txtDeploymentUID.config(state= "normal")
                txtDeploymentUID.delete(0,END)
                txtDeploymentUID.insert(tk.END,sd[2])
                txtDeploymentUID.config(state= "disabled")
                
                txtPositionPrecision.delete(0,END)
                txtPositionPrecision.insert(tk.END,sd[4])

                txtStartLatitude.delete(0,END)
                txtStartLatitude.insert(tk.END,sd[5])

                txtStartLongitude.delete(0,END)
                txtStartLongitude.insert(tk.END,sd[6])

                txtEndLatitude.delete(0,END)
                txtEndLatitude.insert(tk.END,sd[7])

                txtEndLongitude.delete(0,END)
                txtEndLongitude.insert(tk.END,sd[8])

                txtInOut200MileLimit.delete(0,END)
                txtInOut200MileLimit.insert(tk.END,sd[9])       
        
    def Modify_MultipleSetCatch_PositionalVariablesProfile():
        ListBox_DF = (tree1.get_children())
        if len(ListBox_DF)>0:
            cur_id = tree1.focus()
            selvalue = tree1.item(cur_id)['values']
            Length_Selected  =  (len(selvalue))
            if Length_Selected != 0:
                SelectionTree = tree1.selection()
                if (len(SelectionTree)>0):
                    iUpdate = tkinter.messagebox.askyesno("Update Multiple Entries In  DFO-NL-ASOP Set & Catch Database", 
                            "Confirm If You Want To Update Multiple PositionalVariables Entries In DFO-NL-ASOP Set & Catch Database")
                    if iUpdate >0:
                        SelectionTree = tree1.selection()
                        CurrentEntryPositionPrecision = txtPositionPrecision.get()
                        CurrentEntryStartLatitude = txtStartLatitude.get()
                        CurrentEntryStartLongitude = txtStartLongitude.get()
                        CurrentEntryEndLatitude = txtEndLatitude.get()
                        CurrentEntryEndLongitude = txtEndLongitude.get()
                        CurrentEntryInOut200MileLimit = txtInOut200MileLimit.get()
                        Modify_Multiple_BackEnd(CurrentEntryPositionPrecision, CurrentEntryStartLatitude,
                                                CurrentEntryStartLongitude, CurrentEntryEndLatitude,
                                                CurrentEntryEndLongitude, CurrentEntryInOut200MileLimit, SelectionTree)
            else:
                tkinter.messagebox.showinfo("Update Error","Please Select At least One Entries To Update PositionalVariables")
        else:
            tkinter.messagebox.showinfo("Update Error","Empty PositionalVariables Table. Please Select At least One Entries In The Table To Update PositionalVariables ")

    def Modify_Multiple_BackEnd(CurrentEntryPositionPrecision, CurrentEntryStartLatitude,
                                CurrentEntryStartLongitude, CurrentEntryEndLatitude,
                                CurrentEntryEndLongitude, CurrentEntryInOut200MileLimit, SelectionTree):
        application_window=tk.Tk()
        application_window.title ("Update Variables : Positional Type")
        application_window.geometry('420x300+100+40')
        application_window.config(bg="aliceblue")

        lbl_UpdateEntry = Label(application_window, font=('aerial', 11, 'bold'), 
                        bg= "aliceblue", text="Provide Updated Positional Variables Entry : ")
        lbl_UpdateEntry.grid(row =0, column = 0, padx=3, pady =10)

        lbl_Entries_PositionPrecision = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" A. Entries For PositionPrecision :")
        lbl_Entries_PositionPrecision.grid(row =1, column = 0, padx=3, pady =2, sticky =W)
        UpdateValue_PositionPrecision       = IntVar(application_window, value =CurrentEntryPositionPrecision)
        entry_UpdateValue_PositionPrecision = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                        textvariable = UpdateValue_PositionPrecision, width = 10)
        entry_UpdateValue_PositionPrecision.grid(row =1, column = 1, padx=5, pady =2, ipady =2, sticky =W)

        lbl_Entries_StartLatitude = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" B. Entries For StartLatitude :")
        lbl_Entries_StartLatitude.grid(row =2, column = 0, padx=3, pady =10, sticky =W)
        UpdateValue_StartLatitude       = IntVar(application_window, value = CurrentEntryStartLatitude)
        entry_UpdateValue_StartLatitude = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                textvariable = UpdateValue_StartLatitude, width = 10)
        entry_UpdateValue_StartLatitude.grid(row =2, column = 1, padx=5, pady =10, ipady =2, sticky =W)

        lbl_Entries_StartLongitude = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" C. Entries For StartLongitude :")
        lbl_Entries_StartLongitude.grid(row =3, column = 0, padx=3, pady =2, sticky =W)
        UpdateValue_StartLongitude       = IntVar(application_window, value =CurrentEntryStartLongitude)
        entry_UpdateValue_StartLongitude = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                        textvariable = UpdateValue_StartLongitude, width = 10)
        entry_UpdateValue_StartLongitude.grid(row =3, column = 1, padx=5, pady =2, ipady =2, sticky =W)

        lbl_Entries_EndLatitude = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" D. Entries For EndLatitude :")
        lbl_Entries_EndLatitude.grid(row =4, column = 0, padx=3, pady =10, sticky =W)
        UpdateValue_EndLatitude       = IntVar(application_window, value = CurrentEntryEndLatitude)
        entry_UpdateValue_EndLatitude = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                textvariable = UpdateValue_EndLatitude, width = 10)
        entry_UpdateValue_EndLatitude.grid(row =4, column = 1, padx=5, pady =10, ipady =2, sticky =W)

        lbl_Entries_EndLongitude = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" E. Entries For EndLongitude :")
        lbl_Entries_EndLongitude.grid(row =5, column = 0, padx=3, pady =2, sticky =W)
        UpdateValue_EndLongitude       = IntVar(application_window, value =CurrentEntryEndLongitude)
        entry_UpdateValue_EndLongitude = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                        textvariable = UpdateValue_EndLongitude, width = 10)
        entry_UpdateValue_EndLongitude.grid(row =5, column = 1, padx=5, pady =2, ipady =2, sticky =W)

        lbl_Entries_InOut200MileLimit = Label(application_window, font=('aerial', 10, 'bold'),bg= "aliceblue",
                                    text=" F. Entries For InOut200MileLimit :")
        lbl_Entries_InOut200MileLimit.grid(row =6, column = 0, padx=3, pady =10, sticky =W)
        UpdateValue_InOut200MileLimit       = IntVar(application_window, value = CurrentEntryInOut200MileLimit)
        entry_UpdateValue_InOut200MileLimit = Entry(application_window, font=('aerial', 10, 'bold'), 
                                                textvariable = UpdateValue_InOut200MileLimit, width = 10)
        entry_UpdateValue_InOut200MileLimit.grid(row =6, column = 1, padx=5, pady =10, ipady =2, sticky =W)
        SelectionTree = SelectionTree

        def SubmitForupdate():
            try:
                UpdateValue_PositionPrecision = int(entry_UpdateValue_PositionPrecision.get())
            except:
                UpdateValue_PositionPrecision = entry_UpdateValue_PositionPrecision.get()
            try:
                UpdateValue_StartLatitude = float(entry_UpdateValue_StartLatitude.get())
            except:
                UpdateValue_StartLatitude = entry_UpdateValue_StartLatitude.get()
            try:
                UpdateValue_StartLongitude = float(entry_UpdateValue_StartLongitude.get())
            except:
                UpdateValue_StartLongitude = entry_UpdateValue_StartLongitude.get()
            try:
                UpdateValue_EndLatitude = float(entry_UpdateValue_EndLatitude.get())
            except:
                UpdateValue_EndLatitude = float(entry_UpdateValue_EndLatitude.get())
            try:
                UpdateValue_EndLongitude = float(entry_UpdateValue_EndLongitude.get())
            except:
                UpdateValue_EndLongitude = entry_UpdateValue_EndLongitude.get()
            try:
                UpdateValue_InOut200MileLimit = int(entry_UpdateValue_InOut200MileLimit.get())
            except:
                UpdateValue_InOut200MileLimit = entry_UpdateValue_InOut200MileLimit.get()
            
            if (UpdateValue_PositionPrecision!=''):
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
                        UpdateRecordList_SetCatchDB.append((UpdateValue_PositionPrecision,
                                                UpdateValue_StartLatitude,
                                                UpdateValue_StartLongitude,
                                                UpdateValue_EndLatitude,
                                                UpdateValue_EndLongitude,
                                                UpdateValue_InOut200MileLimit,
                                                list_item_DatabaseUID,
                                                list_item_RecordIdentifier,
                                                list_item_DeploymentUID))
                        UpdateRecordList_QCFailDB.append((UpdateValue_PositionPrecision,
                                                UpdateValue_StartLatitude,
                                                UpdateValue_StartLongitude,
                                                UpdateValue_EndLatitude,
                                                UpdateValue_EndLongitude, 
                                                UpdateValue_InOut200MileLimit,
                                                'Updated','Updated','Updated',
                                                'Updated','Updated','Updated',
                                                list_item_DatabaseUID,
                                                list_item_RecordIdentifier,
                                                list_item_DeploymentUID))
                        
                    ## DB Update Executing
                    cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ?, \
                                                    StartLatitude = ?, StartLongitude = ?, EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =? \
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                    cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables SET PositionPrecision = ?, \
                                                    StartLatitude = ?, StartLongitude = ?, EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =?, \
                                                    PositionPrecisionRangeQC = ?, StartLatitudeRangeQC = ?, StartLongitudeRangeQC = ?,\
                                                    EndLatitudeRangeQC = ?, EndLongitudeRangeQC = ?, InOut200MileLimitRangeQC =?\
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
                else:
                    ## Update Selecting DF with user Input
                    SelectedRow_List = []
                    for child in SelectionTree:
                        SelectedRow_List.append(tree1.item(child)["values"])
                    SelectedRow_ListDF = pd.DataFrame(SelectedRow_List, columns=["DataBase_ID", "RecordIdentifier", 
                                                                                 "DeploymentUID", "RecordType",
                                                                                 "PositionPrecision", "StartLatitude", 
                                                                                 "StartLongitude", "EndLatitude",
                                                                                 "EndLongitude", "InOut200MileLimit"])
                    SelectedRow_ListDF.loc[:,['PositionPrecision']]=UpdateValue_PositionPrecision
                    SelectedRow_ListDF.loc[:,['StartLatitude']]=UpdateValue_StartLatitude
                    SelectedRow_ListDF.loc[:,['StartLongitude']]=UpdateValue_StartLongitude
                    SelectedRow_ListDF.loc[:,['EndLatitude']]=UpdateValue_EndLatitude
                    SelectedRow_ListDF.loc[:,['EndLongitude']]=UpdateValue_EndLongitude
                    SelectedRow_ListDF.loc[:,['InOut200MileLimit']]=UpdateValue_InOut200MileLimit
                    SelectedRow_ListDF['DataBase_ID']=(SelectedRow_ListDF.loc[:,'DataBase_ID']).astype(int, errors='ignore')
                    SelectedRow_ListDF['RecordIdentifier']=(SelectedRow_ListDF.loc[:,'RecordIdentifier']).astype(int, errors='ignore')
                    SelectedRow_ListDF['RecordType']=(SelectedRow_ListDF.loc[:,'RecordType']).astype(int, errors='ignore')
                    Raw_Imported_Df = pd.DataFrame(SelectedRow_ListDF)
                    Raw_Imported_Df = Raw_Imported_Df.reset_index(drop=True)
                    Raw_Imported_Df.set_index('DataBase_ID', inplace=True)
                    ## GetSetCatchProfileDB
                    SetCatchProfileDB_DF = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", 
                                                                conn_DB_Set_Catch_Analysis)
                    SetCatchProfileDB_DF = pd.DataFrame(SetCatchProfileDB_DF)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF.set_index('DataBase_ID', inplace=True)
                    ## GetSetPositionalQCFailedDB
                    SetCatchQCFailedDB_DF = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC ;", 
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
                    SetCatchProfileDB_DF['PositionPrecision']=(SetCatchProfileDB_DF.loc[:,'PositionPrecision']).astype(int, errors='ignore')
                    SetCatchProfileDB_DF['StartLatitude']=(SetCatchProfileDB_DF.loc[:,'StartLatitude']).astype(float, errors='ignore')
                    SetCatchProfileDB_DF['StartLongitude']=(SetCatchProfileDB_DF.loc[:,'StartLongitude']).astype(float, errors='ignore')
                    SetCatchProfileDB_DF['EndLatitude']= (SetCatchProfileDB_DF.loc[:,'EndLatitude']).astype(float, errors='ignore')
                    SetCatchProfileDB_DF['EndLongitude']= (SetCatchProfileDB_DF.loc[:,'EndLongitude']).astype(float, errors='ignore')
                    SetCatchProfileDB_DF['InOut200MileLimit']= (SetCatchProfileDB_DF.loc[:,'InOut200MileLimit']).astype(int, errors='ignore')
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

                    ## Update QC Failed Catch variable range
                    SetCatchQCFailedDB_DF.update(Raw_Imported_Df)
                    SetCatchQCFailedDB_DF.reset_index(inplace=True)
                    SetCatchQCFailedDB_DF['DataBase_ID']=(SetCatchQCFailedDB_DF.loc[:,'DataBase_ID']).astype(int, errors='ignore')
                    SetCatchQCFailedDB_DF['RecordIdentifier']=(SetCatchQCFailedDB_DF.loc[:,'RecordIdentifier']).astype(int, errors='ignore')
                    SetCatchQCFailedDB_DF['RecordType']=(SetCatchQCFailedDB_DF.loc[:,'RecordType']).astype(int, errors='ignore')
                    SetCatchQCFailedDB_DF['PositionPrecision']=(SetCatchQCFailedDB_DF.loc[:,'PositionPrecision']).astype(int, errors='ignore')
                    SetCatchQCFailedDB_DF['StartLatitude']=(SetCatchQCFailedDB_DF.loc[:,'StartLatitude']).astype(float, errors='ignore')
                    SetCatchQCFailedDB_DF['StartLongitude']=(SetCatchQCFailedDB_DF.loc[:,'StartLongitude']).astype(float, errors='ignore')
                    SetCatchQCFailedDB_DF['EndLatitude']= (SetCatchQCFailedDB_DF.loc[:,'EndLatitude']).astype(float, errors='ignore')
                    SetCatchQCFailedDB_DF['EndLongitude']= (SetCatchQCFailedDB_DF.loc[:,'EndLongitude']).astype(float, errors='ignore')
                    SetCatchQCFailedDB_DF['InOut200MileLimit']= (SetCatchQCFailedDB_DF.loc[:,'InOut200MileLimit']).astype(int, errors='ignore')
                    SetCatchQCFailedDB_DF['PositionPrecisionRangeQC']='Updated'
                    SetCatchQCFailedDB_DF['StartLatitudeRangeQC']='Updated'
                    SetCatchQCFailedDB_DF['StartLongitudeRangeQC']='Updated'
                    SetCatchQCFailedDB_DF['EndLatitudeRangeQC']='Updated'
                    SetCatchQCFailedDB_DF['EndLongitudeRangeQC']='Updated'
                    SetCatchQCFailedDB_DF['InOut200MileLimitRangeQC']='Updated'
                    try:
                        Submit_To_DBStorage = pd.DataFrame(SetCatchQCFailedDB_DF)
                        Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_PositionalVariables', 
                                                    conn_DB_SetCatch_Validation_Range, if_exists="replace",index = False)
                        conn_DB_SetCatch_Validation_Range.commit()
                    except sqlite3.Error as error:
                        print('Error occured - ', error)
                    finally:
                        if conn_DB_SetCatch_Validation_Range:
                            cur_DB_SetCatch_Validation_Range.close()
                            conn_DB_SetCatch_Validation_Range.close()
                    application_window.destroy()

                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(tk.END,'Finished Update')
                    tkinter.messagebox.showinfo("Update Success","Successfully Updated The Imported Entries")  
            else:
                tkinter.messagebox.showinfo("Update Error",
                                            "PositionPrecision Variables CanNot Be Null")
        
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
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC ;", conn)
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
        
    def SubmitDataFrameToQCFailedDB(DataFrameToSubmit):
        try:
            Import_To_DBStorage = pd.DataFrame(DataFrameToSubmit)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Import_To_DBStorage.to_sql('SetCatch_QCFailedRange_PositionalVariables', sqliteConnection, if_exists="replace", index =False)
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
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC ;", conn)
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
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC ;", conn)
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
        QCFailedPositionalVariablesDB= GenQCFailedSummaryTable_Backend()
        ListSelecteVariables = ['Select Variable & Run Deployment Summary',
                                '1: PositionPrecision',
                                '2: StartLatitude',
                                '3: StartLongitude',
                                '4: EndLatitude',
                                '5: EndLongitude',
                                '6: InOut200MileLimit']
        getentry_ListSelecteVariables = entry_ListSelecteVariables.get()
        
        if getentry_ListSelecteVariables == ListSelecteVariables[0]:
            tkinter.messagebox.showinfo("Run Failed Summary QC Message","Please Select Variable Name To Run")
        
        if getentry_ListSelecteVariables == ListSelecteVariables[1]:
            QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID', 'RecordType',
                                'PositionPrecision','PositionPrecisionRangeQC','DeploymentIdentifier', 'QC_Message']])
            
            QCFailedPositionalVariablesDB = QCFailedPositionalVariablesDB[(
                (QCFailedPositionalVariablesDB.QC_Message == 'Case-PP-RangeQC'))]
            QCFailedPositionalVariablesDB  = QCFailedPositionalVariablesDB.reset_index(drop=True)
            QCFailedPositionalVariablesDB  = pd.DataFrame(QCFailedPositionalVariablesDB)
            
            Tree1QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                 'PositionPrecision']])
            Tree1QCFailedPositionalVariablesDB['StartLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['StartLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['InOut200MileLimit'] =''
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedPositionalVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailGearVarSummTab_C   = QCFailedPositionalVariablesDB.groupby(['DeploymentIdentifier', 'PositionPrecision'], as_index=False).DataBase_ID.count()
            QCFailGearVarSummTab_C   = pd.DataFrame(QCFailGearVarSummTab_C)
            QCFailGearVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'PositionPrecision':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailGearVarSummTab_C['PositionalVariables'] =QCFailGearVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailGearVarSummTab_C = QCFailGearVarSummTab_C.reset_index(drop=True)
            QCFailGearVarSummTab_C = pd.DataFrame(QCFailGearVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailGearVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[2]:
            QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                'StartLatitude','StartLatitudeRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedPositionalVariablesDB = QCFailedPositionalVariablesDB[(
                (QCFailedPositionalVariablesDB.QC_Message == 'Case-SLat-RangeQC'))]
            QCFailedPositionalVariablesDB  = QCFailedPositionalVariablesDB.reset_index(drop=True)
            QCFailedPositionalVariablesDB  = pd.DataFrame(QCFailedPositionalVariablesDB)
           
            Tree1QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                'StartLatitude']])
            Tree1QCFailedPositionalVariablesDB['PositionPrecision'] =''
            Tree1QCFailedPositionalVariablesDB['StartLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['InOut200MileLimit'] =''
            Tree1QCFailedPositionalVariablesDB= (Tree1QCFailedPositionalVariablesDB.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                'PositionPrecision', 'StartLatitude',
                'StartLongitude','EndLatitude', 
                'EndLongitude', 'InOut200MileLimit']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedPositionalVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailGearVarSummTab_C   = QCFailedPositionalVariablesDB.groupby(['DeploymentIdentifier', 'StartLatitude'], as_index=False).DataBase_ID.count()
            QCFailGearVarSummTab_C   = pd.DataFrame(QCFailGearVarSummTab_C)
            QCFailGearVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'StartLatitude':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailGearVarSummTab_C['PositionalVariables'] =QCFailGearVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailGearVarSummTab_C = QCFailGearVarSummTab_C.reset_index(drop=True)
            QCFailGearVarSummTab_C = pd.DataFrame(QCFailGearVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailGearVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[3]:
            QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'StartLongitude','StartLongitudeRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedPositionalVariablesDB = QCFailedPositionalVariablesDB[(
                (QCFailedPositionalVariablesDB.QC_Message == 'Case-SLon-RangeQC'))]
            QCFailedPositionalVariablesDB  = QCFailedPositionalVariablesDB.reset_index(drop=True)
            QCFailedPositionalVariablesDB  = pd.DataFrame(QCFailedPositionalVariablesDB)
            
            Tree1QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'StartLongitude']])
            Tree1QCFailedPositionalVariablesDB['PositionPrecision'] =''
            Tree1QCFailedPositionalVariablesDB['StartLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['InOut200MileLimit'] =''
            Tree1QCFailedPositionalVariablesDB= (Tree1QCFailedPositionalVariablesDB.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                        'PositionPrecision', 'StartLatitude',
                        'StartLongitude','EndLatitude', 
                        'EndLongitude', 'InOut200MileLimit']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedPositionalVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailGearVarSummTab_C   = QCFailedPositionalVariablesDB.groupby(['DeploymentIdentifier', 'StartLongitude'], as_index=False).DataBase_ID.count()
            QCFailGearVarSummTab_C   = pd.DataFrame(QCFailGearVarSummTab_C)
            QCFailGearVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'StartLongitude':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailGearVarSummTab_C['PositionalVariables'] =QCFailGearVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailGearVarSummTab_C = QCFailGearVarSummTab_C.reset_index(drop=True)
            QCFailGearVarSummTab_C = pd.DataFrame(QCFailGearVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailGearVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[4]:
            QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'EndLatitude','EndLatitudeRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedPositionalVariablesDB = QCFailedPositionalVariablesDB[(
                (QCFailedPositionalVariablesDB.QC_Message == 'Case-ELat-RangeQC'))]
            QCFailedPositionalVariablesDB  = QCFailedPositionalVariablesDB.reset_index(drop=True)
            QCFailedPositionalVariablesDB  = pd.DataFrame(QCFailedPositionalVariablesDB)
           
            Tree1QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'EndLatitude']])
            Tree1QCFailedPositionalVariablesDB['PositionPrecision'] =''
            Tree1QCFailedPositionalVariablesDB['StartLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['StartLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['InOut200MileLimit'] =''
            Tree1QCFailedPositionalVariablesDB= (Tree1QCFailedPositionalVariablesDB.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                        'PositionPrecision', 'StartLatitude',
                        'StartLongitude','EndLatitude', 
                        'EndLongitude', 'InOut200MileLimit']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedPositionalVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailGearVarSummTab_C   = QCFailedPositionalVariablesDB.groupby(['DeploymentIdentifier', 'EndLatitude'], as_index=False).DataBase_ID.count()
            QCFailGearVarSummTab_C   = pd.DataFrame(QCFailGearVarSummTab_C)
            QCFailGearVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'EndLatitude':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailGearVarSummTab_C['PositionalVariables'] =QCFailGearVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailGearVarSummTab_C = QCFailGearVarSummTab_C.reset_index(drop=True)
            QCFailGearVarSummTab_C = pd.DataFrame(QCFailGearVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailGearVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[5]:
            QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'EndLongitude','EndLongitudeRangeQC','DeploymentIdentifier', 'QC_Message']])
            QCFailedPositionalVariablesDB = QCFailedPositionalVariablesDB[(
                (QCFailedPositionalVariablesDB.QC_Message == 'Case-ELon-RangeQC'))]
            QCFailedPositionalVariablesDB  = QCFailedPositionalVariablesDB.reset_index(drop=True)
            QCFailedPositionalVariablesDB  = pd.DataFrame(QCFailedPositionalVariablesDB)
            
            Tree1QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'EndLongitude']])
            Tree1QCFailedPositionalVariablesDB['PositionPrecision'] =''
            Tree1QCFailedPositionalVariablesDB['StartLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['StartLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['InOut200MileLimit'] =''
            Tree1QCFailedPositionalVariablesDB= (Tree1QCFailedPositionalVariablesDB.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                        'PositionPrecision', 'StartLatitude',
                        'StartLongitude','EndLatitude', 
                        'EndLongitude', 'InOut200MileLimit']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedPositionalVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailGearVarSummTab_C   = QCFailedPositionalVariablesDB.groupby(['DeploymentIdentifier', 'EndLongitude'], as_index=False).DataBase_ID.count()
            QCFailGearVarSummTab_C   = pd.DataFrame(QCFailGearVarSummTab_C)
            QCFailGearVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'EndLongitude':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailGearVarSummTab_C['PositionalVariables'] =QCFailGearVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailGearVarSummTab_C = QCFailGearVarSummTab_C.reset_index(drop=True)
            QCFailGearVarSummTab_C = pd.DataFrame(QCFailGearVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailGearVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

        if getentry_ListSelecteVariables == ListSelecteVariables[6]:
            QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                    ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                    'InOut200MileLimit','InOut200MileLimitRangeQC',
                    'DeploymentIdentifier', 'QC_Message']])
            QCFailedPositionalVariablesDB = QCFailedPositionalVariablesDB[(
                (QCFailedPositionalVariablesDB.QC_Message == 'Case-IO200ML-RangeQC'))]
            QCFailedPositionalVariablesDB  = QCFailedPositionalVariablesDB.reset_index(drop=True)
            QCFailedPositionalVariablesDB  = pd.DataFrame(QCFailedPositionalVariablesDB)
           
            Tree1QCFailedPositionalVariablesDB= (QCFailedPositionalVariablesDB.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'InOut200MileLimit']])
            Tree1QCFailedPositionalVariablesDB['PositionPrecision'] =''
            Tree1QCFailedPositionalVariablesDB['StartLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['StartLongitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLatitude'] =''
            Tree1QCFailedPositionalVariablesDB['EndLongitude'] =''
            Tree1QCFailedPositionalVariablesDB= (Tree1QCFailedPositionalVariablesDB.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                        'PositionPrecision', 'StartLatitude',
                        'StartLongitude','EndLatitude', 
                        'EndLongitude', 'InOut200MileLimit']])
            countIndex1 = 0
            for each_rec in range(len(Tree1QCFailedPositionalVariablesDB)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(Tree1QCFailedPositionalVariablesDB.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")

            QCFailGearVarSummTab_C   = QCFailedPositionalVariablesDB.groupby(['DeploymentIdentifier', 'InOut200MileLimit'], as_index=False).DataBase_ID.count()
            QCFailGearVarSummTab_C   = pd.DataFrame(QCFailGearVarSummTab_C)
            QCFailGearVarSummTab_C.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                                'InOut200MileLimit':'VariableValue',
                                                'DataBase_ID':'TotalCount'},inplace = True)
            QCFailGearVarSummTab_C['PositionalVariables'] =QCFailGearVarSummTab_C.shape[0]* [getentry_ListSelecteVariables]
            QCFailGearVarSummTab_C = QCFailGearVarSummTab_C.reset_index(drop=True)
            QCFailGearVarSummTab_C = pd.DataFrame(QCFailGearVarSummTab_C)
            countIndex1 = 0
            for each_rec in range(len(QCFailGearVarSummTab_C)):
                if countIndex1 % 2 == 0:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("even",))
                else:
                    tree2.insert("", tk.END, values=list(QCFailGearVarSummTab_C.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree2.tag_configure("even",foreground="black", background="lightgreen")
            tree2.tag_configure("odd",foreground="black", background="ghost white")

    def Search_DeploymentIdentifier_Backend(DeploymentIdentifier, PositionalVariables):
        ListSelecteVariables = ['1: PositionPrecision',
                            '2: StartLatitude',
                            '3: StartLongitude',
                            '4: EndLatitude',
                            '5: EndLongitude',
                            '6: InOut200MileLimit']
        if PositionalVariables in ListSelecteVariables:
            try:
                conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
                cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
                cur_DB_SetCatch_Validation_Range.execute("SELECT DataBase_ID, RecordIdentifier, DeploymentUID, RecordType,\
                            PositionPrecision, StartLatitude, StartLongitude,\
                            EndLatitude, EndLongitude, InOut200MileLimit, QC_Message \
                            FROM SetCatch_QCFailedRange_PositionalVariables  WHERE \
                            DeploymentIdentifier = ? ",(DeploymentIdentifier,))
                rows=cur_DB_SetCatch_Validation_Range.fetchall()
                return rows
            except:
                messagebox.showerror('PositionalVariables Variable Error Message', "PositionalVariables Query Failed")
        
    def InventoryRec2(event):
        ListSelecteVariables = ['1: PositionPrecision',
                                '2: StartLatitude',
                                '3: StartLongitude',
                                '4: EndLatitude',
                                '5: EndLongitude',
                                '6: InOut200MileLimit']
        for nm in tree2.selection():
            sd = tree2.item(nm, 'values')
            DeploymentIdentifier = sd[0]
            PositionalVariables = sd[3]

            if PositionalVariables == ListSelecteVariables[0]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, PositionalVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType', 
                                        'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                                        'EndLatitude', 'EndLongitude', 'InOut200MileLimit','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                                    (MultiSearchRowsDF.QC_Message == 'Case-PP-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
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
                PositionalVariables_Display = PositionalVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,PositionalVariables_Display)

            if PositionalVariables == ListSelecteVariables[1]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, PositionalVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType',
                                            'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-SLat-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
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
                PositionalVariables_Display = PositionalVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,PositionalVariables_Display)

            if PositionalVariables == ListSelecteVariables[2]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, PositionalVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType',
                                            'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-SLon-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
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
                PositionalVariables_Display = PositionalVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,PositionalVariables_Display)

            if PositionalVariables == ListSelecteVariables[3]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, PositionalVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType',
                                            'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-ELat-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
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
                PositionalVariables_Display = PositionalVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,PositionalVariables_Display)

            if PositionalVariables == ListSelecteVariables[4]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, PositionalVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                                columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType',
                                            'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-ELon-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
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
                PositionalVariables_Display = PositionalVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,PositionalVariables_Display)

            if PositionalVariables == ListSelecteVariables[5]:
                tree1.delete(*tree1.get_children())
                MultiSearchRows = Search_DeploymentIdentifier_Backend(DeploymentIdentifier, PositionalVariables)
                MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, 
                        columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType',
                                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                                'EndLatitude', 'EndLongitude', 'InOut200MileLimit','QC_Message'])
                MultiSearchRowsDF = MultiSearchRowsDF[(
                        (MultiSearchRowsDF.QC_Message == 'Case-IO200ML-RangeQC'))]
                MultiSearchRowsDF = MultiSearchRowsDF.loc[:,
                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
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
                PositionalVariables_Display = PositionalVariables + '  QCFailed'
                txtSelectedFailedEntries.delete(0,END)
                txtDisplayMessageSystem.delete(0,END)
                txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)
                txtDisplayMessageSystem.insert(tk.END,PositionalVariables_Display)

    def GenQCFailOverview():
        tree1.delete(*tree1.get_children())
        tree3.delete(*tree3.get_children())
        QCFailedVariablesDB= GenQCFailedSummaryTable_Backend()
        
        ## PositionPrecision fail Count
        QCFail_PositionPrecision = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-PP-RangeQC'))]
        QCFail_PositionPrecision  = QCFail_PositionPrecision.reset_index(drop=True)
        QCFail_PositionPrecision  = pd.DataFrame(QCFail_PositionPrecision)
        Count_QCFail_PositionPrecision = len(QCFail_PositionPrecision)
        
        QC_FailUpdate_PositionPrecision = QCFail_PositionPrecision[(
                (QCFail_PositionPrecision.PositionPrecisionRangeQC == 'Updated'))]
        
        QC_FailUpdate_PositionPrecision  = QC_FailUpdate_PositionPrecision.reset_index(drop=True)
        QC_FailUpdate_PositionPrecision  = pd.DataFrame(QC_FailUpdate_PositionPrecision)
        UpdateCount_QCFail_PositionPrecision = len(QC_FailUpdate_PositionPrecision)
        
        ## StartLatitude fail Count
        QCFail_StartLatitude = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-SLat-RangeQC'))]
        QCFail_StartLatitude  = QCFail_StartLatitude.reset_index(drop=True)
        QCFail_StartLatitude  = pd.DataFrame(QCFail_StartLatitude)
        Count_QCFail_StartLatitude = len(QCFail_StartLatitude)
        
        QC_FailUpdate_StartLatitude = QCFail_StartLatitude[(
                (QCFail_StartLatitude.StartLatitudeRangeQC == 'Updated'))]
        
        QC_FailUpdate_StartLatitude  = QC_FailUpdate_StartLatitude.reset_index(drop=True)
        QC_FailUpdate_StartLatitude  = pd.DataFrame(QC_FailUpdate_StartLatitude)
        UpdateCount_QCFail_StartLatitude = len(QC_FailUpdate_StartLatitude)
        
        ## StartLongitude fail Count
        QCFail_StartLongitude = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-SLon-RangeQC'))]
        QCFail_StartLongitude  = QCFail_StartLongitude.reset_index(drop=True)
        QCFail_StartLongitude  = pd.DataFrame(QCFail_StartLongitude)
        Count_QCFail_StartLongitude = len(QCFail_StartLongitude)
        
        QC_FailUpdate_StartLongitude = QCFail_StartLongitude[(
                (QCFail_StartLongitude.StartLongitudeRangeQC == 'Updated'))]
        
        QC_FailUpdate_StartLongitude  = QC_FailUpdate_StartLongitude.reset_index(drop=True)
        QC_FailUpdate_StartLongitude  = pd.DataFrame(QC_FailUpdate_StartLongitude)
        UpdateCount_QCFail_StartLongitude = len(QC_FailUpdate_StartLongitude)
        
        ## EndLatitude fail Count
        QCFail_EndLatitude = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-ELat-RangeQC'))]
        QCFail_EndLatitude  = QCFail_EndLatitude.reset_index(drop=True)
        QCFail_EndLatitude  = pd.DataFrame(QCFail_EndLatitude)
        Count_QCFail_EndLatitude = len(QCFail_EndLatitude)
        
        QC_FailUpdate_EndLatitude = QCFail_EndLatitude[(
                (QCFail_EndLatitude.EndLatitudeRangeQC == 'Updated'))]
        
        QC_FailUpdate_EndLatitude  = QC_FailUpdate_EndLatitude.reset_index(drop=True)
        QC_FailUpdate_EndLatitude  = pd.DataFrame(QC_FailUpdate_EndLatitude)
        UpdateCount_QCFail_EndLatitude = len(QC_FailUpdate_EndLatitude)

        ## EndLongitude fail Count
        QCFail_EndLongitude = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-ELon-RangeQC'))]
        QCFail_EndLongitude  = QCFail_EndLongitude.reset_index(drop=True)
        QCFail_EndLongitude  = pd.DataFrame(QCFail_EndLongitude)
        Count_QCFail_EndLongitude = len(QCFail_EndLongitude)
        
        QC_FailUpdate_EndLongitude = QCFail_EndLongitude[(
                (QCFail_EndLongitude.EndLongitudeRangeQC == 'Updated'))]
        
        QC_FailUpdate_EndLongitude  = QC_FailUpdate_EndLongitude.reset_index(drop=True)
        QC_FailUpdate_EndLongitude  = pd.DataFrame(QC_FailUpdate_EndLongitude)
        UpdateCount_QCFail_EndLongitude = len(QC_FailUpdate_EndLongitude)

        ## InOut200MileLimit fail Count
        QCFail_InOut200MileLimit = QCFailedVariablesDB[(
                (QCFailedVariablesDB.QC_Message == 'Case-IO200ML-RangeQC'))]
        QCFail_InOut200MileLimit  = QCFail_InOut200MileLimit.reset_index(drop=True)
        QCFail_InOut200MileLimit  = pd.DataFrame(QCFail_InOut200MileLimit)
        Count_QCFail_InOut200MileLimit = len(QCFail_InOut200MileLimit)
        
        QC_FailUpdate_InOut200MileLimit = QCFail_InOut200MileLimit[(
                (QCFail_InOut200MileLimit.InOut200MileLimitRangeQC == 'Updated'))]
        
        QC_FailUpdate_InOut200MileLimit  = QC_FailUpdate_InOut200MileLimit.reset_index(drop=True)
        QC_FailUpdate_InOut200MileLimit  = pd.DataFrame(QC_FailUpdate_InOut200MileLimit)
        UpdateCount_QCFail_InOut200MileLimit = len(QC_FailUpdate_InOut200MileLimit)

        ## Building OverviewDF
        ListVariableName = ['PositionPrecision','StartLatitude','StartLongitude',
                            'EndLatitude','EndLongitude','InOut200MileLimit']
        QCFailCount =   [Count_QCFail_PositionPrecision,
                         Count_QCFail_StartLatitude, 
                         Count_QCFail_StartLongitude, 
                         Count_QCFail_EndLatitude, 
                         Count_QCFail_EndLongitude,
                         Count_QCFail_InOut200MileLimit]
        UpdateQCFailCount =    [UpdateCount_QCFail_PositionPrecision,
                                UpdateCount_QCFail_StartLatitude, 
                                UpdateCount_QCFail_StartLongitude, 
                                UpdateCount_QCFail_EndLatitude, 
                                UpdateCount_QCFail_EndLongitude,
                                UpdateCount_QCFail_InOut200MileLimit]
        QCNullValue = [PP_QCNullValue,
                       SLat_QCNullValue,
                       SLon_QCNullValue,
                       ELat_QCNullValue,
                       ELon_QCNullValue,
                       IO200ML_QCNullValue]
              
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
        ListSelecteVariables = ['PositionPrecision',
                                'StartLatitude',
                                'StartLongitude',
                                'EndLatitude',
                                'EndLongitude',
                                'InOut200MileLimit']
        ListVariableListA = ['1: PositionPrecision',
                             '2: StartLatitude',
                             '3: StartLongitude',
                             '4: EndLatitude',
                             '5: EndLongitude',
                             '6: InOut200MileLimit']
        nm = tree3.selection()
        if len(nm) ==1:
            sd = tree3.item(nm, 'values')
            SelvariableIdentifier = sd[0]
            if SelvariableIdentifier in ListSelecteVariables:
                if SelvariableIdentifier == ListSelecteVariables[0]:
                    QCMsg1 = ("1. PositionPrecision :" + ' QC Range Value Limit: ('+ str(PP_LowerRangeLimitValue) + " - " + str(PP_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[0]
                    entry_ListToSelViewVarList.current(1)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg1)
                    entry_ListSelecteVariables.current(1)
                    tree2.delete(*tree2.get_children())
            
                if SelvariableIdentifier == ListSelecteVariables[1]:
                    QCMsg2 = ("2. StartLatitude :" + ' QC Range Value Limit: (' + str(SLat_LowerRangeLimitValue) + " - " + str(SLat_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[1]
                    entry_ListToSelViewVarList.current(2)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg2)
                    entry_ListSelecteVariables.current(2)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[2]:
                    QCMsg3 = ("3. StartLongitude :" + ' QC Range Value Limit: ('+ str(SLon_LowerRangeLimitValue) + " - " + str(SLon_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[2]
                    entry_ListToSelViewVarList.current(3)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg3)
                    entry_ListSelecteVariables.current(3)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[3]:
                    QCMsg4 =("4. EndLatitude :" + ' QC Range Value Limit: ('+ str(ELat_LowerRangeLimitValue) + " - " + str(ELat_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[3]
                    entry_ListToSelViewVarList.current(4)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg4)
                    entry_ListSelecteVariables.current(4)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[4]:
                    QCMsg5 =("5. EndLongitude :" + ' QC Range Value Limit: ('+ str(ELon_LowerRangeLimitValue) + " - " + str(ELon_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[4]
                    entry_ListToSelViewVarList.current(5)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg5)
                    entry_ListSelecteVariables.current(5)
                    tree2.delete(*tree2.get_children())

                if SelvariableIdentifier == ListSelecteVariables[5]:
                    QCMsg6 = ("6. InOut200MileLimit :" + ' QC Range Value Limit: ('+ str(IO200ML_LowerRangeLimitValue) + " - " + str(IO200ML_UpperRangeLimitValue) + ')')
                    SelvariableIdentifier = ListVariableListA[5]
                    entry_ListToSelViewVarList.current(6)
                    txtDisplayMessageSystem.delete(0,END)
                    txtDisplayMessageSystem.insert(1, QCMsg6)
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
                                '1: PositionPrecision',
                                '2: StartLatitude',
                                '3: StartLongitude',
                                '4: EndLatitude',
                                '5: EndLongitude',
                                '6: InOut200MileLimit']
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
            QCMsg1 = ("1. PositionPrecision :" + ' QC Range Value Limit: ('+ str(PP_LowerRangeLimitValue) + " - " + str(PP_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg1)
            entry_ListSelecteVariables.current(1)
            entry_UpdateVariableList.current(0)
            
        if(SelVariableView ==ListVariableListA[2]):
            QCMsg2 = ("2. StartLatitude :" + ' QC Range Value Limit: (' + str(SLat_LowerRangeLimitValue) + " - " + str(SLat_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg2)
            entry_ListSelecteVariables.current(2)
            entry_UpdateVariableList.current(1)
        
        if(SelVariableView ==ListVariableListA[3]):
            QCMsg3 = ("3. StartLongitude :" + ' QC Range Value Limit: ('+ str(SLon_LowerRangeLimitValue) + " - " + str(SLon_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg3)
            entry_ListSelecteVariables.current(3)
            entry_UpdateVariableList.current(2)

        if(SelVariableView ==ListVariableListA[4]):
            QCMsg4 =("4. EndLatitude :" + ' QC Range Value Limit: ('+ str(ELat_LowerRangeLimitValue) + " - " + str(ELat_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg4)
            entry_ListSelecteVariables.current(4)
            entry_UpdateVariableList.current(3)
            
        if(SelVariableView ==ListVariableListA[5]):
            QCMsg5 =("5. EndLongitude :" + ' QC Range Value Limit: ('+ str(ELon_LowerRangeLimitValue) + " - " + str(ELon_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg5)
            entry_ListSelecteVariables.current(5)
            entry_UpdateVariableList.current(4)
        
        if(SelVariableView ==ListVariableListA[6]):
            QCMsg6 = ("6. InOut200MileLimit :" + ' QC Range Value Limit: ('+ str(IO200ML_LowerRangeLimitValue) + " - " + str(IO200ML_UpperRangeLimitValue) + ')')
            tree1.delete(*tree1.get_children())
            tree2.delete(*tree2.get_children())
            tree0.delete(*tree0.get_children())
            txtDisplayMessageSystem.delete(0,END)
            txtDisplayMessageSystem.insert(1, QCMsg6)
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
                        ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','RecordType', 
                        'PositionPrecision', 'StartLatitude', 'StartLongitude',\
                        'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
                        ).replace(['', None, np.nan, 'None'], 99999999)
                
                Complete_df[['DataBase_ID', 'RecordIdentifier','RecordType', 
                            'PositionPrecision', 'InOut200MileLimit']] = Complete_df[
                            ['DataBase_ID', 'RecordIdentifier','RecordType', 
                            'PositionPrecision', 'InOut200MileLimit']].astype(int)
                
                Complete_df[['StartLatitude', 'StartLongitude','EndLatitude', 'EndLongitude']] = Complete_df[
                            ['StartLatitude', 'StartLongitude','EndLatitude', 'EndLongitude']].astype(float)
                
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
                    list_item_PositionPrecision = (rowValue[4])
                    list_item_StartLatitude = (rowValue[5])
                    list_item_StartLongitude = (rowValue[6])
                    list_item_EndLatitude = (rowValue[7])
                    list_item_EndLongitude = (rowValue[8])
                    list_item_InOut200MileLimit = (rowValue[9])

                    UpdateRecordList_SetCatchDB.append((
                                        list_item_RecordType,
                                        list_item_PositionPrecision,
                                        list_item_StartLatitude,
                                        list_item_StartLongitude,
                                        list_item_EndLatitude,
                                        list_item_EndLongitude,
                                        list_item_InOut200MileLimit,
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                    
                    UpdateRecordList_QCFailDB.append((
                                        list_item_RecordType,
                                        list_item_PositionPrecision,
                                        list_item_StartLatitude,
                                        list_item_StartLongitude,
                                        list_item_EndLatitude,
                                        list_item_EndLongitude, 
                                        list_item_InOut200MileLimit, 
                                        'Updated','Updated','Updated',
                                        'Updated','Updated','Updated',
                                        list_item_DataBase_ID,
                                        list_item_RecordIdentifier,
                                        list_item_DeploymentUID))
                                             
                ## DB Update Executing
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ?, PositionPrecision = ?, \
                                                    StartLatitude = ?, StartLongitude = ?, EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =? \
                                                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                                    UpdateRecordList_SetCatchDB)
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables SET RecordType = ?, PositionPrecision = ?, \
                                        StartLatitude = ?, StartLongitude = ?, EndLatitude = ?, EndLongitude = ?, InOut200MileLimit =?, \
                                        PositionPrecisionRangeQC = ?, StartLatitudeRangeQC = ?, StartLongitudeRangeQC = ?,\
                                        EndLatitudeRangeQC = ?, EndLongitudeRangeQC = ?, InOut200MileLimitRangeQC =?\
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
                            bg= "cadet blue", text="NB : Edit/Modify Year/ASOC/DepN/SetN Columns Requires Edit DeplymentUID Accordingly")
            lbl_CautionSteps_1.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_CautionSteps_2 = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                                bg= "cadet blue", text="NB : Do Not Delete Any Row And Submit")
            lbl_CautionSteps_2.grid(row =12, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            windows.mainloop() 

    def GetSetcatchQCFailDF():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,
                            ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                            'PositionPrecision', 'StartLatitude', 'StartLongitude',
                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit',
                            'PositionPrecisionRangeQC', 'StartLatitudeRangeQC', 'StartLongitudeRangeQC',
                            'EndLatitudeRangeQC', 'EndLongitudeRangeQC', 'InOut200MileLimitRangeQC', 
                            'DeploymentIdentifier']]
                SetCatchQCFailedDB_DF= (SetCatchQCFailedDB_DF.loc[:,
                        ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 'RecordType', 
                      'PositionPrecision', 'StartLatitude', 'StartLongitude',
                      'EndLatitude', 'EndLongitude', 'InOut200MileLimit',
                      'PositionPrecisionRangeQC', 'StartLatitudeRangeQC', 'StartLongitudeRangeQC',
                      'EndLatitudeRangeQC', 'EndLongitudeRangeQC', 'InOut200MileLimitRangeQC', 
                      'DeploymentIdentifier']]
                        ).replace(['', None, np.nan, 'None'], 99999999)
                
                SetCatchQCFailedDB_DF[['DataBase_ID', 'RecordIdentifier','RecordType', 
                            'PositionPrecision', 'InOut200MileLimit']] = SetCatchQCFailedDB_DF[
                            ['DataBase_ID', 'RecordIdentifier','RecordType', 
                            'PositionPrecision', 'InOut200MileLimit']].astype(int)
                
                SetCatchQCFailedDB_DF[['StartLatitude', 'StartLongitude','EndLatitude', 'EndLongitude']] = SetCatchQCFailedDB_DF[
                            ['StartLatitude', 'StartLongitude','EndLatitude', 'EndLongitude']].astype(float)
                
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

    def SetcatchDB_VariableList():
        GetSetCatchDB_VariableList = ['PositionPrecision', 'StartLatitude', 'StartLongitude',
                                      'EndLatitude', 'EndLongitude', 'InOut200MileLimit']
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
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables\
                    SET PositionPrecision = ?, PositionPrecisionRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                UpdateRecordList)
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables\
                    SET StartLatitude = ?, StartLatitudeRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList)
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables\
                    SET StartLongitude = ?, StartLongitudeRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)

        if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLatitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables\
                    SET EndLatitude = ?, EndLatitudeRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)
                
        if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLongitude = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables\
                    SET EndLongitude = ?, EndLongitudeRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)
            
        if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET InOut200MileLimit = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    (UpdateRecordList))
            cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_PositionalVariables\
                    SET InOut200MileLimit = ?, InOut200MileLimitRangeQC =?\
                    WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                    UpdateRecordList_QCFailDB)
            
        conn_DB_Set_Catch_Analysis.commit()    
        conn_DB_Set_Catch_Analysis.close()
        
        conn_DB_SetCatch_Validation_Range.commit()
        conn_DB_SetCatch_Validation_Range.close()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
            # Performing QC On Variables Value And DataType
            Var_Class_IntA18=['PositionPrecision', 'InOut200MileLimit']
            Var_Class_String7 =['DeploymentUID']
            Var_Class_IntB27  = []
            Var_Class_FloatB27  = ['StartLatitude', 'StartLongitude',
                                   'EndLatitude', 'EndLongitude']
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
    btnModifyPositionalVariablesProfile = Button(TopLeftframe, text="Update Selected DepUID\n(DB Update)", 
                            font=('aerial', 10, 'bold'), fg="blue",
                            height =2, width=25, bd=2, command = UpdateSelectedDepUID)
    btnModifyPositionalVariablesProfile.grid(row =16, column = 0, padx=2, pady =5, ipady =5, sticky =W)

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
    btnGenDepSummary.grid(row=6, column = 0, padx=90, pady =1, sticky =E, rowspan =1)

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
    ImportExport.add_command(label="Export Failed Results (.csv)", command=Export_FailedCSV)
    ImportExport.add_command(label="Import & Update DB (.csv)", command=ImportAndUpdateSetCatchDB)
    View.add_command(label="View Edit & Update QCFailed Results", command=QCFailedExcelViewAll)
    View.add_command(label="Ref-QCFail To Set&Catch DB", command=RefFailedToSetcatchDB)
   
    Treepopup.add_command(label="Exit", command=iExit)
    Treepopup.add_command(label="Modify & Update DB With Selected PositionalVariables In Table C", command=Modify_MultipleSetCatch_PositionalVariablesProfile)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    tree1.pack(side = LEFT)
    window.mainloop()
