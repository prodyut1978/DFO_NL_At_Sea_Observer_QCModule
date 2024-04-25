from tkinter import *
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd


from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_RunIntegratedRangeValidation
from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_Misc_Support
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation import DFO_NL_ASOP_ViewTowDistanceQCResults
from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation import DFO_NL_ASOP_ViewTowSeparationQCResults

def SetCatch_ViewIntegratedRangeResult():
    D2_IRVC = tk.Toplevel()
    D2_IRVC.title ("DFO-NL-ASOP Integrated Range Validation QC - ID-D-02")
    D2_IRVC.geometry('1170x690+400+100')
    D2_IRVC.config(bg="aliceblue")
    Topframe = Frame(D2_IRVC, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")

    lbl_Total_QCEntries = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Set Entries For QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCEntries.grid(row =0, column = 0, padx=4, pady =2)
    Set_Catch_TotalEntries =DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_NumberOf_Entries()  
    Total_QC_Entries = IntVar(Topframe, value=Set_Catch_TotalEntries)
    entry_Total_QCEntries = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Entries, width = 8, bd=2)
    entry_Total_QCEntries.grid(row =0, column = 1, padx=1, pady =5)

    Topframe.pack(side = TOP)
    Midframe = Frame(D2_IRVC, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg="aliceblue")
    Midframe.pack(side = TOP)

    ## Get File Name Imported File
    ImportedFileName = DFO_NL_ASOP_Misc_Support.GetPickledImportedFileName()
    ImportedFileName = ImportedFileName.split(",")
    ImportedFileName =(ImportedFileName[0])
    TextString =  '( File Name : ' + ImportedFileName + ' )'
    lblHeader = Label(Midframe, font=('aerial', 12, 'bold'), 
                text=("  ** Integrated QC & Validation Summary- ID-D-02 : Variable Range QC  **  ") + '\n' + TextString,
                bg="aliceblue")
    lblHeader.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)
    
    TableMargin1 = Frame(D2_IRVC, bd = 2, padx= 2, pady= 2, relief = RIDGE, bg="aliceblue")
    TableMargin1.pack(side=TOP)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4", "column5"), height=0, show='headings')
    tree1.heading("#1", text="ID-D-02", anchor=CENTER)
    tree1.heading("#2", text="QC Variables Name", anchor=CENTER)
    tree1.heading("#3", text="Total QC Failed", anchor=CENTER)
    tree1.heading("#4", text="View Failed Results & Update Set & Catch DB", anchor=CENTER)
    tree1.heading("#5", text="QC Variables Range Details", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=55)       
    tree1.column('#2', stretch=NO, minwidth=0, width=180)            
    tree1.column('#3', stretch=NO, minwidth=0, width=160)
    tree1.column('#4', stretch=NO, minwidth=0, width=370)
    tree1.column('#5', stretch=NO, minwidth=0, width=400)
    style = ttk.Style(D2_IRVC)
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'),background ="aliceblue", foreground='black')
    tree1.pack()
    QCFrame = Frame(TableMargin1, bd = 2, padx= 0, pady= 5, relief = RIDGE, bg="white")
    QCFrame.pack(side = LEFT)

    QCFailed_TowDistance = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_Count_FailedQC_TowDistance()
    QCFailed_TowSeparation = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_Count_FailedQC_TowSeparation()
    
    
    def IntegratedQC_RangeValidation_TowDistance():

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

        def QCFailed_TowDistanceResultViewer():
            QCFailed_TowDistance = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_Count_FailedQC_TowDistance()
            QCFailed_TowDistance =int(QCFailed_TowDistance)
            DFO_NL_ASOP_ViewTowDistanceQCResults.ViewRangeValidatedResult_TowDistance()
          
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
        TowDiff_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[23,'LowerRangeLimitValue'])
        TowDiff_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[23,'UpperRangeLimitValue'])
        
        entryID_TowDistance = IntVar(QCFrame, value=0)
        entry_entryID_TowDistance = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_TowDistance, width = 3, bd=2)
        entry_entryID_TowDistance.grid(row =0, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_TowDistance = Listbox(QCFrame, font=('aerial', 10, 'bold'), height =5, width =22)
        List_entryID_TowDistance.insert(1, " TowDistance")
        List_entryID_TowDistance.insert(2, " Start/End-Lat & Start/End-Lon")
        List_entryID_TowDistance.insert(3, " Set&Catch Distance")
        List_entryID_TowDistance.insert(4, " AvgTowSpeed & Duration")
        List_entryID_TowDistance.insert(5, " TowDifference")
        List_entryID_TowDistance.grid(row =0, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_TowDistance = (DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_Count_FailedQC_TowDistance())
        QCFailed_TowDistance =int(QCFailed_TowDistance)
        entryQCFailed_TowDist = IntVar(QCFrame, value=QCFailed_TowDistance)
        entry_QCFailed_TowDistance = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_TowDist, width = 10, bd=2)
        entry_QCFailed_TowDistance.grid(row =0, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedTowDistance = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-D-02-0)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_TowDistanceResultViewer)
        btnViewQCFailedTowDistance.grid(row =0, column = 3, padx=60, pady =2, sticky =W)

        RangeDetails_TowDistance = Listbox(QCFrame, font=('aerial', 9), height =10, width =55)
        RangeDetails_TowDistance.insert(1, " Condition : << Within Lat Long Range Defined In Range Table >> ")
        RangeDetails_TowDistance.insert(2, (" << TowDifference Can Not Be Greater Than : " + str(TowDiff_UpperRangeLimitValue) + " >> "))
        
        RangeDetails_TowDistance.insert(3, (" Variables Constraints : " ))
        
        RangeDetails_TowDistance.insert(4, (" StartLatLon Range : " + \
            (str(SLat_LowerRangeLimitValue) + ' , ' + str(SLon_LowerRangeLimitValue)) + " - " +\
            (str(SLat_UpperRangeLimitValue) + ' , ' + str(SLon_UpperRangeLimitValue))
            ))
        RangeDetails_TowDistance.insert(5, (" EndtLatLon Range : " + \
            (str(ELat_LowerRangeLimitValue) + ' , ' + str(ELon_LowerRangeLimitValue)) + " - " +\
            (str(ELat_UpperRangeLimitValue) + ' , ' + str(ELon_UpperRangeLimitValue))
            ))
        RangeDetails_TowDistance.insert(6, (" GearType : MG (1,2,3,9,10,14,16,17,18,21,66,67,97) Only" ))
        
        RangeDetails_TowDistance.insert(7, (" QC Formulation :  " ))

        RangeDetails_TowDistance.insert(8, " TowDifference : Abs(TowDistance - S&CDistance)")
        RangeDetails_TowDistance.insert(9, " TowDistance : Dist(StartLatLon - EndtLatLon)")
        RangeDetails_TowDistance.insert(10, " S&CDistance : AverageTowSpeed * Duration")
        RangeDetails_TowDistance.grid(row =0, column = 4, padx=1, pady =2, ipady = 5, sticky =W)
            
    def IntegratedQC_RangeValidation_TowSeparation():

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

        def QCFailed_TowSeparationResultViewer():
            QCFailed_TowSeparation = DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_Count_FailedQC_TowSeparation()
            QCFailed_TowSeparation =int(QCFailed_TowSeparation)
            DFO_NL_ASOP_ViewTowSeparationQCResults.ViewRangeValidatedResult_TowSeparation()
          
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
        MaxTowSepSpeedLimit=float(Get_RangeLimitVariables.at[24,'UpperRangeLimitValue'])
        MaxTowSeparationTolerance=float(Get_RangeLimitVariables.at[25,'UpperRangeLimitValue'])
        
        entryID_TowSeparation = IntVar(QCFrame, value=1)
        entry_entryID_TowSeparation = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = entryID_TowSeparation, width = 3, bd=2)
        entry_entryID_TowSeparation.grid(row =1, column = 0, padx=10, pady =2, ipady = 5, sticky =W)

        List_entryID_TowSeparation = Listbox(QCFrame, font=('aerial', 10, 'bold'), height =5, width =22)
        List_entryID_TowSeparation.insert(1, " TowSeparation")
        List_entryID_TowSeparation.insert(2, " HourSeparation")
        List_entryID_TowSeparation.insert(3, " Start/End Time")
        List_entryID_TowSeparation.insert(4, " AvgTowSpeed & Duration")
        List_entryID_TowSeparation.insert(5, " Start/End-Lat & Start/End-Lon")
        List_entryID_TowSeparation.grid(row =1, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_TowSeparation = (DFO_NL_ASOP_SetCatch_ViewIntegrated_DBCount.SetCatch_Count_FailedQC_TowSeparation())
        QCFailed_TowSeparation =int(QCFailed_TowSeparation)
        entryQCFailed_TowDist = IntVar(QCFrame, value=QCFailed_TowSeparation)
        entry_QCFailed_TowSeparation = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_TowDist, width = 10, bd=2)
        entry_QCFailed_TowSeparation.grid(row =1, column = 2, padx=30, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedTowSeparation = Button(QCFrame, text="View & Update QC Failed Variables \n (ID-D-02-1)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =2, width=30, bd=2, anchor="w", padx=10,
                                    command = QCFailed_TowSeparationResultViewer)
        btnViewQCFailedTowSeparation.grid(row =1, column = 3, padx=60, pady =2, sticky =W)

        RangeDetails_TowSeparation = Listbox(QCFrame, font=('aerial', 9), height =12, width =55)
        RangeDetails_TowSeparation.insert(1, " Condition : << Within Lat Long Range Defined In Range Table >> ")
        RangeDetails_TowSeparation.insert(2, (" << TowSeparation Must Not Greater Than : " ))
        RangeDetails_TowSeparation.insert(3, (" <<  (" + str(MaxTowSepSpeedLimit) + " * HourSeparation ) " + " + " + \
                                                       str(MaxTowSeparationTolerance) + " %" + " >> "))
        RangeDetails_TowSeparation.insert(4, (" Variables Constraints : " ))
        
        RangeDetails_TowSeparation.insert(5, (" StartLatLon Range : " + \
            (str(SLat_LowerRangeLimitValue) + ' , ' + str(SLon_LowerRangeLimitValue)) + " - " +\
            (str(SLat_UpperRangeLimitValue) + ' , ' + str(SLon_UpperRangeLimitValue))
            ))
        RangeDetails_TowSeparation.insert(6, (" EndtLatLon Range : " + \
            (str(ELat_LowerRangeLimitValue) + ' , ' + str(ELon_LowerRangeLimitValue)) + " - " +\
            (str(ELat_UpperRangeLimitValue) + ' , ' + str(ELon_UpperRangeLimitValue))
            ))
        RangeDetails_TowSeparation.insert(7, (" GearType : MG (1,2,3,9,10,14,16,17,18,21,66,67,97) Only" ))
        
        RangeDetails_TowSeparation.insert(8, (" QC Formulation :  " ))

        RangeDetails_TowSeparation.insert(9, " HourSeparation : (EndDateTime (Previous) - StartDateTime (Current))")
        RangeDetails_TowSeparation.insert(10, " TowSeparation : Dist(EndtLatLon (Previous) - StarttLatLon (Current))")
        RangeDetails_TowSeparation.insert(11, " MaxTowSeparation : (HourSeparation * MaxDefinedTowSpeed) + ")
        RangeDetails_TowSeparation.insert(12, " MaxTowSeparationTolerance %")
        RangeDetails_TowSeparation.grid(row =1, column = 4, padx=1, pady =2, ipady = 5, sticky =W)

    IntegratedQC_RangeValidation_TowDistance()
    IntegratedQC_RangeValidation_TowSeparation()

    lbl_Total_QCFailed = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Set Failed In QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCFailed.grid(row =0, column = 2, padx=4, pady =2)
    Set_Catch_TotalFailed = (int(QCFailed_TowDistance) + int(QCFailed_TowSeparation))
    Total_QC_Failed = IntVar(Topframe, value=Set_Catch_TotalFailed)
    entry_Total_QCFailed = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Failed, width = 8, bd=2)
    entry_Total_QCFailed.grid(row =0, column = 3, padx=1, pady =5)

    ## Defining Reload Functions
    def ReloadQCFailedSummary():
        entry_Total_QCFailed.delete(0,END)
        Reload_RangeValidation = DFO_NL_ASOP_SetCatch_RunIntegratedRangeValidation.SetCatch_IntegratedVariableRangeValidation()
        TotalFailedQC= Reload_RangeValidation[1]
        entry_Total_QCFailed.insert(tk.END,TotalFailedQC)
        IntegratedQC_RangeValidation_TowDistance()
        IntegratedQC_RangeValidation_TowSeparation()
        
    ## Defining Bottom Frame
    BottomFrame = Frame(D2_IRVC, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    BottomFrame.pack(side = BOTTOM)
    btnRefreashReload = Button(BottomFrame, text="Reload QC Failed Summary", font=('aerial', 12, 'bold'), 
                                        bg ="aliceblue", height =2, width=22, bd=2, anchor=tk.CENTER, padx=5,
                                        command = ReloadQCFailedSummary)
    btnRefreashReload.grid(row =0, column = 0, padx=1, pady =4, sticky =W)
    D2_IRVC.mainloop()

