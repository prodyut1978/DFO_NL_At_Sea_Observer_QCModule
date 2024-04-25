import sys
from tkinter import *
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import ttk

from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_ViewConsist_Yr_Cntry_Qta_Failed
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_ViewConsist_SubTrip_VessSideN_Failed
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_ViewConsist_VessVariables_Failed
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_ViewConsist_Calender_Failed
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_ViewConsist_MobileGear_Failed
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_RunConsistencyValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_Misc_Support

def SetCatch_ViewConsistencyValidatedResult():
    root=tk.Toplevel()
    root.title ("DFO-NL-ASOP Variable Consistency Validation QC - ID-C-05")
    root.geometry('1140x850+200+20')
    root.config(bg="aliceblue")
    Topframe = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    
    lbl_Total_QCEntries = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Entries For QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCEntries.grid(row =0, column = 0, padx=4, pady =2)
    
    Set_Catch_TotalEntries =DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_Entries()
    Total_QC_Entries = IntVar(Topframe, value=Set_Catch_TotalEntries)
    entry_Total_QCEntries = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Entries, width = 8, bd=2)
    entry_Total_QCEntries.grid(row =1, column = 0, padx=2, pady =1)

    ## Get File Name Imported File
    ImportedFileName = DFO_NL_ASOP_Misc_Support.GetPickledImportedFileName()
    ImportedFileName = ImportedFileName.split(",")
    ImportedFileName =(ImportedFileName[0])
    TextString =  '( File Name : ' + ImportedFileName + ' )'
    lblHeader = Label(Topframe, font=('aerial', 12, 'bold'), 
                text=("  ** Simple QC & Validation Summary- ID-C-05 : Variable Consistency QC  **  ") + '\n' + TextString, 
                bg="aliceblue")
    lblHeader.grid(row =1, column = 1, padx=40, pady =2, sticky =W, columnspan =2)
    Topframe.pack(side = TOP)
    TableMargin1 = Frame(root, bd = 2, padx= 2, pady= 2, relief = RIDGE, bg="aliceblue")
    TableMargin1.pack(side=TOP)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", 
                                               "column3", "column4", 
                                               "column5"), height=0,
                                                show='headings')
    tree1.heading("#1", text="ID-C-05", anchor=CENTER)
    tree1.heading("#2", text="QC Variables Name", anchor=CENTER)
    tree1.heading("#3", text="Total QC Failed", anchor=CENTER)
    tree1.heading("#4", text="View Failed Results & Update Set & Catch DB", anchor=CENTER)
    tree1.heading("#5", text="QC Variables Consistency Details", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=55)       
    tree1.column('#2', stretch=NO, minwidth=0, width=160)            
    tree1.column('#3', stretch=NO, minwidth=0, width=160)
    tree1.column('#4', stretch=NO, minwidth=0, width=320)
    tree1.column('#5', stretch=NO, minwidth=0, width=440)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'),background ="aliceblue", foreground='black')
    tree1.pack()
    QCFrame = Frame(TableMargin1, bd = 2, padx= 0, pady= 5, relief = RIDGE, bg="white")
    QCFrame.pack(side = LEFT)
    QCFailed_YCQVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_YCQ())
    QCFailed_VesselVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Vessel())
    QCFailed_VesselVariables = QCFailed_VesselVariables[0]
    QCFailed_CalenderVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Calender())
    QCFailed_MGVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_MG())

    def SimpleQC_ConsistencyFailed_YearCountryQuota():
        def QCFailed_YCQVariablesResultViewer():
            QCFailed_YCQVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_YCQ())
            QCFailed_YCQVariables =int(QCFailed_YCQVariables)
            if QCFailed_YCQVariables>0:
                    DFO_NL_ASOP_SetCatch_ViewConsist_Yr_Cntry_Qta_Failed.ViewConsis_Yr_Cntry_Qta_ValResult()
            else:
                tkinter.messagebox.showinfo("Year-Country-Quota Type Variables Table Consistency Validation Message",
                "Year-Country-Quota Type Variables Table Consistency Validation All Passed. *** All Year-Country-Quota Variables Table Consistency \
                in The Set & Catch Import are Validated Against Year-Country-Quota Variables ****")
        
        ConsistencyYCQ_FailedVariables = IntVar(QCFrame, value=0)
        entry_ConsistencyYCQ_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = ConsistencyYCQ_FailedVariables, width = 3, bd=2)
        entry_ConsistencyYCQ_FailedVariables.grid(row =0, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        List_ConsistencyYCQ_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =6, width =20)
        List_ConsistencyYCQ_FailedVariables.insert( 1," ")
        List_ConsistencyYCQ_FailedVariables.insert( 2," 1: ASOC-DepNum Code   ")
        
        List_ConsistencyYCQ_FailedVariables.insert( 3," ")
        List_ConsistencyYCQ_FailedVariables.insert( 4," 2: Country/Quota   ")
        List_ConsistencyYCQ_FailedVariables.insert( 5," ")

        List_ConsistencyYCQ_FailedVariables.insert( 6," 3:  Year  ")
        List_ConsistencyYCQ_FailedVariables.insert( 7," ")
        
        List_ConsistencyYCQ_FailedVariables.grid(row =0, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_ConsistencyYCQ = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_YCQ())
        QCFailed_ConsistencyYCQ =int(QCFailed_ConsistencyYCQ)
        entryQCFailed_Consis = IntVar(QCFrame, value=QCFailed_ConsistencyYCQ)
        entry_QCFailed_ConsistencyYCQ = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_Consis, width = 10, bd=2)
        entry_QCFailed_ConsistencyYCQ.grid(row =0, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedConsistencyYCQ = Button(QCFrame, text="QC View & Update DB \n (ID-C-05-0)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_YCQVariablesResultViewer)
        btnViewQCFailedConsistencyYCQ.grid(row =0, column = 3, padx=90, pady =2, sticky =W)
        ConsistencyYCQVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =6, width =60)
       
        ConsistencyYCQVariables.insert( 1," ")
        ConsistencyYCQVariables.insert( 2," 1 - Year Same In All Records Within ASOC- Deployment Code")
        ConsistencyYCQVariables.insert( 3," ")

        ConsistencyYCQVariables.insert( 4," 2 - Country Same In All Records Within ASOC- Deployment Code")
        ConsistencyYCQVariables.insert( 6," ")
        
        
        ConsistencyYCQVariables.insert( 7," 3 - Quota Same In All Records Within ASOC- Deployment Code")
        ConsistencyYCQVariables.insert( 8," ")
       
        ConsistencyYCQVariables.grid(row =0, column = 4, padx=15, pady =2, ipady = 5, sticky =W)
        
    def SimpleQC_ConsistencyFailed_SubTripN_VessSideN():
        def QCFailed_SubTripN_VessSideNResultViewer():
            QCFailed_SubTripN_VessSideN = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Vessel())
            QCFailed_SubTripN_VessSideN = QCFailed_SubTripN_VessSideN[1]
            QCFailed_SubTripN_VessSideN =int(QCFailed_SubTripN_VessSideN)
            if QCFailed_SubTripN_VessSideN>0:
                DFO_NL_ASOP_SetCatch_ViewConsist_SubTrip_VessSideN_Failed.ViewConsis_VSN_STN_ValResult()
            else:
                tkinter.messagebox.showinfo("Vessel Type Variables Table Consistency Validation Message",
                "Vessel Type Variables Table Consistency Validation All Passed. *** All Vessel Variables Table Consistency \
                in The Set & Catch Import are Validated Against Vessel Variables ****")
        
        SubTripN_VessSideN_FailedVariables = IntVar(QCFrame, value=2)
        entry_SubTripN_VessSideN_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = SubTripN_VessSideN_FailedVariables, width = 3, bd=2)
        entry_SubTripN_VessSideN_FailedVariables.grid(row =4, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        
        List_SubTripN_VessSideN_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =5, width =20)
        List_SubTripN_VessSideN_FailedVariables.insert( 1," ")
        List_SubTripN_VessSideN_FailedVariables.insert( 2," 1: SubTripNumber   ")
        
        List_SubTripN_VessSideN_FailedVariables.insert( 3," ")
        List_SubTripN_VessSideN_FailedVariables.insert( 4," 2: VesselSideNumber   ")
        List_SubTripN_VessSideN_FailedVariables.insert( 5," ")
        List_SubTripN_VessSideN_FailedVariables.grid(row =4, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_SubTripN_VessSideN = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Vessel())
        QCFailed_SubTripN_VessSideN =int(QCFailed_SubTripN_VessSideN[1])
        entryQCFailed_VessConsis = IntVar(QCFrame, value=QCFailed_SubTripN_VessSideN)
        entry_QCFailed_SubTripN_VessSideN = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_VessConsis, width = 10, bd=2)
        entry_QCFailed_SubTripN_VessSideN.grid(row =4, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedSubTripN_VessSideN = Button(QCFrame, text="QC View & Update DB \n (ID-C-05-2)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_SubTripN_VessSideNResultViewer)
        btnViewQCFailedSubTripN_VessSideN.grid(row =4, column = 3, padx=90, pady =2, sticky =W)
      
        ConsistencySubTripN_VessSideN = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =6, width =60)
        ConsistencySubTripN_VessSideN.insert( 1," ")
        ConsistencySubTripN_VessSideN.insert( 2," ** Within Year-ASOC-Obs#-Dep#-Country/Quota-VessClass Code : ")
        
        ConsistencySubTripN_VessSideN.insert( 3," ")
        ConsistencySubTripN_VessSideN.insert( 4," VesselSideNumber Must Be Consistent In Each SubTripNumber")
        ConsistencySubTripN_VessSideN.insert( 5," ")
        ConsistencySubTripN_VessSideN.insert( 6," When VesselsideNumber Changes, SubTripNumber Must Change")
        
        ConsistencySubTripN_VessSideN.grid(row =4, column = 4, padx=15, pady =2, ipady = 5, sticky =W)
 
    def SimpleQC_ConsistencyFailed_VesselVariables():
        def QCFailed_VesselVariablesResultViewer():
            QCFailed_VesselVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Vessel())
            QCFailed_VesselVariables = QCFailed_VesselVariables[2]
            QCFailed_VesselVariables =int(QCFailed_VesselVariables)
            if QCFailed_VesselVariables>0:
                DFO_NL_ASOP_SetCatch_ViewConsist_VessVariables_Failed.ViewConsis_VessVariables_ValResult()
            else:
                tkinter.messagebox.showinfo("Vessel Type Variables Table Consistency Validation Message",
                "Vessel Type Variables Table Consistency Validation All Passed. *** All Vessel Variables Table Consistency \
                in The Set & Catch Import are Validated Against Vessel Variables ****")
        
        ConsistencyVessel_FailedVariables = IntVar(QCFrame, value=1)
        entry_ConsistencyVessel_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = ConsistencyVessel_FailedVariables, width = 3, bd=2)
        entry_ConsistencyVessel_FailedVariables.grid(row =2, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        
        List_ConsistencyVessel_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =8, width =20)
        List_ConsistencyVessel_FailedVariables.insert( 1," ")
        List_ConsistencyVessel_FailedVariables.insert( 2," 1: VesselSideNumber   ")
        
        List_ConsistencyVessel_FailedVariables.insert( 3," ")
        List_ConsistencyVessel_FailedVariables.insert( 4," 2: VesselClass   ")
        List_ConsistencyVessel_FailedVariables.insert( 5," ")

        List_ConsistencyVessel_FailedVariables.insert( 6," 3: VesselLength   ")
        List_ConsistencyVessel_FailedVariables.insert( 7," ")

        List_ConsistencyVessel_FailedVariables.insert( 8," 4: VesselHorsepower   ")
        
        List_ConsistencyVessel_FailedVariables.grid(row =2, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_ConsistencyVessel = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Vessel())
        QCFailed_ConsistencyVessel =int(QCFailed_ConsistencyVessel[2])
        entryQCFailed_VessConsis = IntVar(QCFrame, value=QCFailed_ConsistencyVessel)
        entry_QCFailed_ConsistencyVessel = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_VessConsis, width = 10, bd=2)
        entry_QCFailed_ConsistencyVessel.grid(row =2, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedConsistencyVessel = Button(QCFrame, text="QC View & Update DB \n (ID-C-05-1)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_VesselVariablesResultViewer)
        btnViewQCFailedConsistencyVessel.grid(row =2, column = 3, padx=90, pady =2, sticky =W)
      
        ConsistencyVesselVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =10, width =60)
        ConsistencyVesselVariables.insert( 1," ")
        ConsistencyVesselVariables.insert( 2," ** Within Year-ASOC-Obs#-Dep#-Country/Quota Code : ")
        
        ConsistencyVesselVariables.insert( 3," ")
        ConsistencyVesselVariables.insert( 4," 1 - VesselClass Must Consistent With VesselSideNumber")
        
        ConsistencyVesselVariables.insert( 5," ")
        ConsistencyVesselVariables.insert( 6," 2 - VesselLength Must Consistent With VesselSideNumber")

        ConsistencyVesselVariables.insert( 7," ")
        ConsistencyVesselVariables.insert( 8," 3 - VesselHorsepower Must Consistent With VesselSideNumber")
       
        ConsistencyVesselVariables.grid(row =2, column = 4, padx=15, pady =2, ipady = 5, sticky =W)
    
    def SimpleQC_ConsistencyFailed_CalenderVariables():
        def QCFailed_CalenderVariablesResultViewer():
            QCFailed_CalenderVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Calender())
            QCFailed_CalenderVariables =int(QCFailed_CalenderVariables)
            if QCFailed_CalenderVariables>0:
                DFO_NL_ASOP_SetCatch_ViewConsist_Calender_Failed.ViewConsis_Calender_ValResult()
            else:
                tkinter.messagebox.showinfo("Calender Type Variables Table Consistency Validation Message",
                "Calender Type Variables Table Consistency Validation All Passed. *** All Calender Variables Table Consistency \
                in The Set & Catch Import are Validated Against Calender Variables ****")
        
        ConsistencyCalender_FailedVariables = IntVar(QCFrame, value=3)
        entry_ConsistencyCalender_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = ConsistencyCalender_FailedVariables, width = 3, bd=2)
        entry_ConsistencyCalender_FailedVariables.grid(row =6, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        
        List_ConsistencyCalender_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =4, width =20)
        List_ConsistencyCalender_FailedVariables.insert( 1," ")
        List_ConsistencyCalender_FailedVariables.insert( 2," 1: Day/Month")
        
        List_ConsistencyCalender_FailedVariables.insert( 3," ")
        List_ConsistencyCalender_FailedVariables.insert( 4," 2: HaulDay/HaulMonth ")

        List_ConsistencyCalender_FailedVariables.grid(row =6, column = 1, padx=20, pady =2, ipady = 5, sticky =W)

        QCFailed_ConsistencyCalender = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_Calender())
        QCFailed_ConsistencyCalender =int(QCFailed_ConsistencyCalender)
        entryQCFailed_CalenderConsis = IntVar(QCFrame, value=QCFailed_ConsistencyCalender)
        entry_QCFailed_ConsistencyCalender = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_CalenderConsis, width = 10, bd=2)
        entry_QCFailed_ConsistencyCalender.grid(row =6, column = 2, padx=2, pady =2, ipady = 5, sticky =W)

        btnViewQCFailedConsistencyCalender = Button(QCFrame, text="QC View & Update DB \n (ID-C-05-3)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_CalenderVariablesResultViewer)
        btnViewQCFailedConsistencyCalender.grid(row =6, column = 3, padx=90, pady =2, sticky =W)
        ConsistencyCalenderVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =4, width =60)
       
        ConsistencyCalenderVariables.insert( 1," ")
        ConsistencyCalenderVariables.insert( 2," ** For Current Set Within ASOC- Deployment Code")
        ConsistencyCalenderVariables.insert( 3,"  ")
        ConsistencyCalenderVariables.insert( 4," Year/Day/Month is Same Or Before Year/HaulDay/HaulMonth")
        ConsistencyCalenderVariables.grid(row =6, column = 4, padx=15, pady =2, ipady = 5, sticky =W)

    def SimpleQC_ConsistencyFailed_MobileGear():
        def QCFailed_MGVariablesResultViewer():
            QCFailed_MGVariables = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_MG())
            QCFailed_MGVariables =int(QCFailed_MGVariables)
            if QCFailed_MGVariables>0:
                DFO_NL_ASOP_SetCatch_ViewConsist_MobileGear_Failed.ViewConsis_MobileGear_ValResult()
            else:
                tkinter.messagebox.showinfo("MG Type Variables Table Consistency Validation Message",
                "MG Type Variables Table Consistency Validation All Passed. *** All MG Variables Table Consistency \
                in The Set & Catch Import are Validated Against MG Variables ****")
        ConsistencyMG_FailedVariables = IntVar(QCFrame, value=4)
        entry_ConsistencyMG_FailedVariables = Entry(QCFrame, font=('aerial', 10, 'bold'), state=DISABLED, justify='center',
                                textvariable = ConsistencyMG_FailedVariables, width = 3, bd=2)
        entry_ConsistencyMG_FailedVariables.grid(row =8, column = 0, padx=10, pady =2, ipady = 5, sticky =W)
        List_ConsistencyMG_FailedVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =2, width =20)
        List_ConsistencyMG_FailedVariables.insert( 1," ")
        List_ConsistencyMG_FailedVariables.insert( 2," 1: Mobile Gear   ")
        List_ConsistencyMG_FailedVariables.grid(row =8, column = 1, padx=20, pady =2, ipady = 5, sticky =W)
        QCFailed_ConsistencyMG = (DFO_NL_ASOP_SetCatch_ViewConsValRes_DBCount.SetCatch_NumberOf_ConsistncyFailedQC_MG())
        QCFailed_ConsistencyMG = int(QCFailed_ConsistencyMG)
        entryQCFailed_MGConsis = IntVar(QCFrame, value=QCFailed_ConsistencyMG)
        entry_QCFailed_ConsistencyMG = Entry(QCFrame, font=('aerial', 10, 'bold'), justify='center',
                                textvariable = entryQCFailed_MGConsis, width = 10, bd=2)
        entry_QCFailed_ConsistencyMG.grid(row =8, column = 2, padx=2, pady =2, ipady = 5, sticky =W)
        btnViewQCFailedConsistencyMG = Button(QCFrame, text="QC View & Update DB \n (ID-C-05-4)", font=('aerial', 10, 'bold'),
                                    bg ="aliceblue", height =3, width=20, bd=2, anchor="w", padx=10,
                                    command = QCFailed_MGVariablesResultViewer)
        btnViewQCFailedConsistencyMG.grid(row =8, column = 3, padx=90, pady =2, sticky =W)
        ConsistencyMGVariables = Listbox(QCFrame, font=('aerial', 9, 'bold'), height =8, width =60)
        ConsistencyMGVariables.insert( 1," ")
        ConsistencyMGVariables.insert( 2," ** Mobile Gear - For Current Set Within Deployment")
        ConsistencyMGVariables.insert( 3," ")
        ConsistencyMGVariables.insert( 4," Year/Day/Month/StartTime + Duration Is Equal Or Less Than (= <) To ")
        ConsistencyMGVariables.insert( 5," ")
        ConsistencyMGVariables.insert( 6," Year/Day/Month/StartTime Of Following Set Within Same Deployment")
        ConsistencyMGVariables.insert( 7," ")
        ConsistencyMGVariables.insert( 8," (Must Require Non-Empty Columns Of Year/Day/Month/StartTime/Duration)")
        ConsistencyMGVariables.grid(row =8, column = 4, padx=15, pady =2, ipady = 5, sticky =W)

    SimpleQC_ConsistencyFailed_YearCountryQuota()
    SimpleQC_ConsistencyFailed_SubTripN_VessSideN()
    SimpleQC_ConsistencyFailed_VesselVariables()
    SimpleQC_ConsistencyFailed_CalenderVariables()
    SimpleQC_ConsistencyFailed_MobileGear()

    lbl_Total_QCFailed = Label(Topframe, font=('aerial', 12, 'bold'), text="Total Failed In QC :" , bg="aliceblue", fg ='black')
    lbl_Total_QCFailed.grid(row =0, column = 3, padx=4, pady =2)
    Set_Catch_TotalFailed = (int(QCFailed_YCQVariables)+\
                             int(QCFailed_VesselVariables)+\
                             int(QCFailed_CalenderVariables)+\
                             int(QCFailed_MGVariables))
    Total_QC_Failed = IntVar(Topframe, value=Set_Catch_TotalFailed)
    entry_Total_QCFailed = Entry(Topframe, font=('aerial', 12, 'bold'), justify='center',
                            textvariable = Total_QC_Failed, width = 8, bd=2)
    entry_Total_QCFailed.grid(row =1, column = 3, padx=1, pady =5)

    ## Defining Reload Functions
    def ReloadQCFailedSummary():
        entry_Total_QCFailed.delete(0,END)
        Reload_SetCatch_Runconsist = DFO_NL_ASOP_SetCatch_RunConsistencyValidation.SetCatch_VariableConsistencyValidation()
        TotalFailedQC_Consistency = Reload_SetCatch_Runconsist[1]
        entry_Total_QCFailed.insert(tk.END,TotalFailedQC_Consistency)
        SimpleQC_ConsistencyFailed_YearCountryQuota()
        SimpleQC_ConsistencyFailed_SubTripN_VessSideN()
        SimpleQC_ConsistencyFailed_VesselVariables()
        SimpleQC_ConsistencyFailed_CalenderVariables()
        SimpleQC_ConsistencyFailed_MobileGear()
    
    ## Defining Bottom Frame
    BottomFrame = Frame(root, bd = 2, padx= 3, pady= 4, relief = RIDGE, bg="aliceblue")
    BottomFrame.pack(side = BOTTOM)
    btnRefreashReload = Button(BottomFrame, text="Reload QC Failed Summary", font=('aerial', 12, 'bold'), 
                                        bg ="aliceblue", height =2, width=22, bd=2, anchor=tk.CENTER, padx=5,
                                        command = ReloadQCFailedSummary)
    btnRefreashReload.grid(row =0, column = 0, padx=1, pady =4, sticky =W)
    root.mainloop()


