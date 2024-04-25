from tkinter import *
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd


from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_SetCatch_RunIntegratedAreaCalValidation
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_Misc_Support
Path_CSV_NAFOBoundary = './External_Import/AreaCalculated_Import/CSV_AreaProfile/DFO_NL_ASOP_NAFOAreaProfile.csv'
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_ViewNAFOAreaCalcQCResults
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_Plot_NAFO_QCFail
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_ViewUnitAreaCalcQCResults
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_Plot_UnitArea_QCFail

def SetCatch_ViewIntegratedCalcResult():
    root=tk.Toplevel()
    root.title ("DFO-NL-ASOP Integrated Calculation Validation QC - ID-D-03")
    root.geometry('1200x740+400+100')
    root.config(bg="aliceblue")
    Topframe = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")

    lbl_Total_QCEntries = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Set Entries For QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCEntries.grid(row =0, column = 0, padx=4, pady =2)
    Set_Catch_TotalEntries =DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_NumberOf_Entries()  
    Total_QC_Entries = IntVar(Topframe, value=Set_Catch_TotalEntries)
    entry_Total_QCEntries = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Entries, width = 8, bd=2)
    entry_Total_QCEntries.grid(row =0, column = 1, padx=1, pady =5)

    Topframe.pack(side = TOP)
    Midframe = Frame(root, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
    Midframe.pack(side = TOP)

    ## Get File Name Imported File
    ImportedFileName = DFO_NL_ASOP_Misc_Support.GetPickledImportedFileName()
    ImportedFileName = ImportedFileName.split(",")
    ImportedFileName =(ImportedFileName[0])
    TextString =  '( File Name : ' + ImportedFileName + ' )'
    lblHeader = Label(Midframe, font=('aerial', 12, 'bold'), 
                text=("  ** Integrated QC & Validation Summary- ID-D-03 : Variable Calculation QC  **  ") + '\n' + TextString,
                bg="aliceblue")
    lblHeader.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
    
    TableMargin1 = Frame(root, bd = 2, padx= 2, pady= 2, relief = RIDGE, bg="aliceblue")
    TableMargin1.pack(side=TOP)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4", "column5"), height=0, show='headings')
    tree1.heading("#1", text="ID-D-03", anchor=CENTER)
    tree1.heading("#2", text="QC Variables Name", anchor=CENTER)
    tree1.heading("#3", text="Total QC Failed", anchor=CENTER)
    tree1.heading("#4", text="View Failed Results & Update Set & Catch DB", anchor=CENTER)
    tree1.heading("#5", text="QC Variables Range Details", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=55)       
    tree1.column('#2', stretch=NO, minwidth=0, width=180)            
    tree1.column('#3', stretch=NO, minwidth=0, width=160)
    tree1.column('#4', stretch=NO, minwidth=0, width=370)
    tree1.column('#5', stretch=NO, minwidth=0, width=400)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'),background ="aliceblue", foreground='black')
    tree1.pack()
    QCFrame = Frame(TableMargin1, bd = 2, padx= 0, pady= 5, relief = RIDGE, bg="white")
    QCFrame.pack(side = LEFT)
    QCFailed_NAFOAreaCalc = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_FailCount_NAFOAreaCalc()
    QCFailed_UnitArea = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_FailCount_UnitAreaCalc()
    
    def IntegratedQC_AreaCalc_NAFO():

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

        def QCFailed_NAFOResultViewer():
            QCFailed_NAFO = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_FailCount_NAFOAreaCalc()
            QCFailed_NAFO =int(QCFailed_NAFO)
            DFO_NL_ASOP_ViewNAFOAreaCalcQCResults.ViewCalcValidatedResult_NAFOArea()
            
        def QCFailed_NAFOResultPlotter():
            DFO_NL_ASOP_Plot_NAFO_QCFail.Plot_NAFOArea_QCFailList()
        
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
        
        entryID_NAFO = IntVar(QCFrame, value=0)
        entry_entryID_NAFO = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_NAFO, width = 3, bd=2)
        entry_entryID_NAFO.grid(row =0, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_NAFO = Listbox(QCFrame, font=('aerial', 8, 'bold'), height =5, width =22)
        List_entryID_NAFO.insert(1, " NAFODivision")
        List_entryID_NAFO.insert(2, " Start/End-Lat & Start/End-Lon")
        List_entryID_NAFO.insert(3, " NAFOPolygonArea")
        List_entryID_NAFO.insert(4, " StartPoints & EndPoints")
        List_entryID_NAFO.insert(5, " NAFOAreaValidityCheck")
        List_entryID_NAFO.grid(row =0, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_NAFO = (DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_FailCount_NAFOAreaCalc())
        QCFailed_NAFO =int(QCFailed_NAFO)
        entryQCFailed_NAFODiv = IntVar(QCFrame, value=QCFailed_NAFO)
        entry_QCFailed_NAFO = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_NAFODiv, width = 10, bd=2)
        entry_QCFailed_NAFO.grid(row =0, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedNAFO = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-D-03-0)", 
                                    font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_NAFOResultViewer)
        btnViewQCFailedNAFO.grid(row =0, column = 3, padx=60, pady =1, sticky =W)

        btnMapQCFailedNAFO = Button(QCFrame, text="Map NAFO & View QC Failed Variables \n (ID-D-03-1)", 
                                    font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_NAFOResultPlotter)
        btnMapQCFailedNAFO.grid(row =1, column = 3, padx=60, pady =1, sticky =W)

        RangeDetails_NAFO = Listbox(QCFrame, font=('aerial', 9), height =11, width =60)
        RangeDetails_NAFO.insert(1, " Condition : << Within Lat Long Range Defined In Range Table >> ")
        RangeDetails_NAFO.insert(2, (" <<  Start/End Lat/Lon (StartPoints & EndPoints) Must Be Within NAFO Area  >> "))
        
        RangeDetails_NAFO.insert(3, (" Variables Constraints : " ))
        
        RangeDetails_NAFO.insert(4, (" StartLatLon Range : " + \
            (str(SLat_LowerRangeLimitValue) + ' , ' + str(SLon_LowerRangeLimitValue)) + " - " +\
            (str(SLat_UpperRangeLimitValue) + ' , ' + str(SLon_UpperRangeLimitValue))
            ))
        RangeDetails_NAFO.insert(5, (" EndtLatLon Range : " + \
            (str(ELat_LowerRangeLimitValue) + ' , ' + str(ELon_LowerRangeLimitValue)) + " - " +\
            (str(ELat_UpperRangeLimitValue) + ' , ' + str(ELon_UpperRangeLimitValue))
            ))
        RangeDetails_NAFO.insert(6, (" NAFOBoundaryPoints : Imported For Each NAFODivision" ))
        RangeDetails_NAFO.insert(6, (" Ref: QCMain View > TopMenu AreaRange > View & Define NAFO Area" ))
        RangeDetails_NAFO.insert(8, (" QC Formulation :  " ))

        RangeDetails_NAFO.insert(9, " StartPoints & EndPoints : Points(Start/End LatLon) ")
        RangeDetails_NAFO.insert(10, " NAFOPolygonArea: Polygon(NAFOBoundaryPoints)")
        RangeDetails_NAFO.insert(11, " NAFOAreaValidityCheck : (Start/End Points).within(NAFOPolygonArea)")
        RangeDetails_NAFO.grid(row =0, column = 4, padx=1, pady =2, ipady = 5, sticky =W)
            
    def IntegratedQC_AreaCalc_UnitArea():

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

        def QCFailed_UnitAreaResultViewer():
            QCFailed_UnitArea = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_FailCount_UnitAreaCalc()
            QCFailed_UnitArea =int(QCFailed_UnitArea)
            DFO_NL_ASOP_ViewUnitAreaCalcQCResults.ViewCalcValidatedResult_UnitArea()
            
        def QCFailed_UnitAreaResultPlotter():
            DFO_NL_ASOP_Plot_UnitArea_QCFail.Plot_UnitArea_QCFailList()
        
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
        
        entryID_UnitArea = IntVar(QCFrame, value=1)
        entry_entryID_UnitArea = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_UnitArea, width = 3, bd=2)
        entry_entryID_UnitArea.grid(row =3, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_UnitArea = Listbox(QCFrame, font=('aerial', 8, 'bold'), height =5, width =22)
        List_entryID_UnitArea.insert(1, " UnitArea")
        List_entryID_UnitArea.insert(2, " Start/End-Lat & Start/End-Lon")
        List_entryID_UnitArea.insert(3, " UnitAreaPolygonArea")
        List_entryID_UnitArea.insert(4, " StartPoints & EndPoints")
        List_entryID_UnitArea.insert(5, " UnitAreaAreaValidityCheck")
        List_entryID_UnitArea.grid(row =3, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_UnitArea = (DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_FailCount_UnitAreaCalc())
        QCFailed_UnitArea =int(QCFailed_UnitArea)
        entryQCFailed_UnitAreaDiv = IntVar(QCFrame, value=QCFailed_UnitArea)
        entry_QCFailed_UnitArea = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_UnitAreaDiv, width = 10, bd=2)
        entry_QCFailed_UnitArea.grid(row =3, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedUnitArea = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-D-03-2)", 
                                    font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_UnitAreaResultViewer)
        btnViewQCFailedUnitArea.grid(row =3, column = 3, padx=60, pady =1, sticky =W)

        btnMapQCFailedUnitArea = Button(QCFrame, text="Map UnitArea & View QC Failed Variables \n (ID-D-03-3)", 
                                    font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_UnitAreaResultPlotter)
        btnMapQCFailedUnitArea.grid(row =4, column = 3, padx=60, pady =1, sticky =W)

        RangeDetails_UnitArea = Listbox(QCFrame, font=('aerial', 9), height =11, width =60)
        RangeDetails_UnitArea.insert(1, " Condition : << Within Lat Long Range Defined In Range Table >> ")
        RangeDetails_UnitArea.insert(2, (" <<  Start/End Lat/Lon (StartPoints & EndPoints) Must Be Within Assigned UnitArea  >> "))
        
        RangeDetails_UnitArea.insert(3, (" Variables Constraints : " ))
        
        RangeDetails_UnitArea.insert(4, (" StartLatLon Range : " + \
            (str(SLat_LowerRangeLimitValue) + ' , ' + str(SLon_LowerRangeLimitValue)) + " - " +\
            (str(SLat_UpperRangeLimitValue) + ' , ' + str(SLon_UpperRangeLimitValue))
            ))
        RangeDetails_UnitArea.insert(5, (" EndtLatLon Range : " + \
            (str(ELat_LowerRangeLimitValue) + ' , ' + str(ELon_LowerRangeLimitValue)) + " - " +\
            (str(ELat_UpperRangeLimitValue) + ' , ' + str(ELon_UpperRangeLimitValue))
            ))
        RangeDetails_UnitArea.insert(6, (" UnitAreaBoundaryPoints : Imported For Each UnitAreaDivision" ))
        RangeDetails_UnitArea.insert(6, (" Ref: QCMain View > TopMenu AreaRange > View & Define UnitArea Area" ))
        RangeDetails_UnitArea.insert(8, (" QC Formulation :  " ))

        RangeDetails_UnitArea.insert(9, " StartPoints & EndPoints : Points(Start/End LatLon) ")
        RangeDetails_UnitArea.insert(10, " UnitAreaPolygonArea: Polygon(UnitAreaBoundaryPoints)")
        RangeDetails_UnitArea.insert(11, " UnitAreaAreaValidityCheck : (Start/End Points).within(UnitAreaPolygonArea)")
        RangeDetails_UnitArea.grid(row =3, column = 4, padx=1, pady =15, ipady = 5, sticky =W)

    IntegratedQC_AreaCalc_NAFO()
    IntegratedQC_AreaCalc_UnitArea()
   
    lbl_Total_QCFailed = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Set Failed In QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCFailed.grid(row =0, column = 2, padx=4, pady =2)
    Set_Catch_TotalFailed = (int(QCFailed_NAFOAreaCalc) + int(QCFailed_UnitArea))
    Total_QC_Failed = IntVar(Topframe, value=Set_Catch_TotalFailed)
    entry_Total_QCFailed = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Failed, width = 8, bd=2)
    entry_Total_QCFailed.grid(row =0, column = 3, padx=1, pady =5)

    ## Defining Reload Functions
    def ReloadQCFailedSummary():
        entry_Total_QCFailed.delete(0,END)
        Reload_Areacalc = DFO_NL_ASOP_SetCatch_RunIntegratedAreaCalValidation.SetCatch_IntegratedAreaCalcValidation()
        TotalFailedQC= Reload_Areacalc[1]
        entry_Total_QCFailed.insert(tk.END,TotalFailedQC)
        IntegratedQC_AreaCalc_NAFO()
        IntegratedQC_AreaCalc_UnitArea()
        
    ## Defining Bottom Frame
    BottomFrame = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    BottomFrame.pack(side = BOTTOM)
    btnRefreashReload = Button(BottomFrame, text="Reload QC Failed Summary", font=('aerial', 12, 'bold'), 
                                        bg ="aliceblue", height =2, width=22, bd=2, anchor=tk.CENTER, padx=5,
                                        command = ReloadQCFailedSummary)
    btnRefreashReload.grid(row =0, column = 0, padx=1, pady =4, sticky =W)

    root.mainloop()

