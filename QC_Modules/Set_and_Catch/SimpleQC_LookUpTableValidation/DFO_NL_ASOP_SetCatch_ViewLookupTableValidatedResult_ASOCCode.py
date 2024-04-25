#Front End
from tkinter import*
import tkinter.messagebox
from tkinter import ttk, filedialog
from tkinter import messagebox
import tkinter as tk
import sqlite3
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilenames
from tkinter import simpledialog
import pandas as pd
from pandastable import Table
import numpy as np
import functools

def SetCatch_ViewLookupValidatedResult_ASOCCode():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP LookUp ASOCCode Validator - ID-C-01-0")
    window.geometry("980x730+200+100")
    window.config(bg="cadet blue")
    window.resizable(0, 0)

    ## Top Main Frame
    TopMainFrame = Frame(window, bd = 2, padx= 2, pady= 1, relief = RIDGE)
    TopMainFrame.grid(row =0, column = 0, padx=2, pady =1, sticky =W, rowspan =1)

    ## Top Left Frame
    TopLeftframe = Frame(TopMainFrame, bd = 1, padx= 1, pady= 1, relief = RIDGE)
    TopLeftframe.grid(row =0, column = 0, padx=1, pady =1, sticky =W, rowspan =1, columnspan =1)
    DataBase_ID       = IntVar(TopLeftframe, value='')
    RecordIdentifier  = IntVar(TopLeftframe, value='')
    DeploymentUID     = StringVar(TopLeftframe)
    ASOCCode       = IntVar(TopLeftframe, value='')

    lblTitEntry = Label(TopLeftframe, font=('aerial', 11, 'bold'), text="A: ASOCCode QC Failed Profile Details")
    lblTitEntry.grid(row =0, column = 0, padx=0, pady =2, sticky =W, rowspan =1)

    lblDatabaseID = Label(TopLeftframe, font=('aerial', 10, 'bold'), text = "1. DatabaseID :", padx =0, pady= 2)
    lblDatabaseID.grid(row =2, column = 0, padx=4, pady =2, sticky =W)
    txtDatabaseID  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= DataBase_ID, width = 35)
    txtDatabaseID.grid(row =3, column = 0, padx=4, pady =4,ipadx=1, sticky =W)

    lblRecordIdentifier = Label(TopLeftframe, font=('aerial', 10, 'bold'), text = "2. RecordIdentifier :", padx =0, pady= 2)
    lblRecordIdentifier.grid(row =4, column = 0, padx=4, pady =2, sticky =W)
    txtRecordIdentifier  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable = RecordIdentifier, width = 35)
    txtRecordIdentifier.grid(row =5, column = 0, padx=4, pady =4,ipadx=1, sticky =W)

    lblDeploymentUID = Label(TopLeftframe, font=('aerial', 10, 'bold'), text = "3. DeploymentUID (Year-ASOC-Deployment#-Set#) :", padx =0, pady= 2)
    lblDeploymentUID.grid(row =6, column = 0, padx=4, pady =2, sticky =W)
    txtDeploymentUID  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable = DeploymentUID, width = 35)
    txtDeploymentUID.grid(row =7, column = 0, padx=4, pady =4,ipadx=1, sticky =W)

    lblASOCCodeCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), text = "4. ASOCCode :", padx =0, pady= 2)
    lblASOCCodeCode.grid(row =8, column = 0, padx=4, pady =2, sticky =W)
    txtASOCCode  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= ASOCCode, width = 35)
    txtASOCCode.grid(row =9, column = 0, padx=4, pady =4,ipadx=1, sticky =W)

    ## Top Right Frame
    TopRightframe = Frame(TopMainFrame, bd = 1, padx= 5, pady= 1, relief = RIDGE)
    TopRightframe.grid(row =0, column = 3, padx=2, pady =1, sticky =W, rowspan =1)

    lbl_TotalFailedEntries = Label(TopRightframe, font=('aerial', 11, 'bold'), text="Total QC Failed Entries :")
    lbl_TotalFailedEntries.grid(row =0, column = 0, padx=2, pady =2, ipady=2, sticky =W)
    TotalFailedEntries = IntVar(TopRightframe, value='')
    txtTotalFailedEntries = Entry(TopRightframe, font=('aerial', 12, 'bold'),textvariable = TotalFailedEntries, width = 8, bd=2)
    txtTotalFailedEntries.grid(row =1, column = 0, padx=50, pady =2, ipady =5, sticky =W)

    lbl_SelectedFailedEntries = Label(TopRightframe, font=('aerial', 11, 'bold'), text="Selected QC Failed Entries :")
    lbl_SelectedFailedEntries.grid(row =0, column = 0, padx=40, pady =2, ipady=2, sticky =E)
    SelectedFailedEntries = IntVar(TopRightframe, value='')
    txtSelectedFailedEntries = Entry(TopRightframe, font=('aerial', 12, 'bold'),textvariable = SelectedFailedEntries, width = 8, bd=2)
    txtSelectedFailedEntries.grid(row =1, column = 0, padx=100, pady =2, ipady =5, sticky =E)

    lblQCFailedResultASOCCode = Label(TopRightframe, font=('aerial', 11, 'bold'), text="C: View QC Failed Results Table")
    lblQCFailedResultASOCCode.grid(row =2, column = 0, padx=5, pady =2, ipady =2, sticky =W, rowspan =1)
    TableMargin1 = Frame(TopRightframe, bd = 2, padx= 10, pady= 1, relief = RIDGE)
    TableMargin1.grid(row =3, column = 0, padx=0, pady =1, sticky =W, rowspan =1)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4"), height=26, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    tree1.heading("#1", text="DatabaseID", anchor=CENTER)
    tree1.heading("#2", text="RecordIdentifier", anchor=CENTER)
    tree1.heading("#3", text="DeploymentUID", anchor=CENTER)
    tree1.heading("#4", text="ASOCCode", anchor=CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=120, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=180, anchor = W)
    tree1.column('#4', stretch=NO, minwidth=0, width=130, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 10), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree1, tearoff=0)
    tree1.pack()

    ## Top Bottom Left
    TopBottomLeftframe = Frame(TopLeftframe, bd = 1, padx= 1, pady= 1, relief = RIDGE)
    TopBottomLeftframe.grid(row =12, column = 0, padx=2, pady =1, sticky =W, rowspan =1)
    lblSummaryQCFailedResultSpecies = Label(TopBottomLeftframe, font=('aerial', 11, 'bold'), text="B: Generate QC Failed Summary Table")
    lblSummaryQCFailedResultSpecies.grid(row =0, column = 0, padx=5, pady =2, ipady =4, sticky =W, rowspan =1)
    TableMargin2 = Frame(TopBottomLeftframe, bd = 1, padx= 1, pady= 1, relief = RIDGE)
    TableMargin2.grid(row=1, column = 0, padx=2, pady =1, sticky =W, rowspan =1)
    tree2 = ttk.Treeview(TableMargin2, column=("column1", "column2", "column3"), height=13, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin2, orient ="vertical", command=tree2.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree2.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin2, orient ="horizontal", command=tree2.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree2.configure(xscrollcommand = scrollbarx.set)
    tree2.heading("#1", text="DeploymentIdentifier", anchor=CENTER)
    tree2.heading("#2", text="ASOCCode", anchor=CENTER)
    tree2.heading("#3", text="Count", anchor=CENTER)
    tree2.column('#1', stretch=NO, minwidth=0, width=155, anchor = tk.CENTER)            
    tree2.column('#2', stretch=NO, minwidth=0, width=125, anchor = tk.CENTER)
    tree2.column('#3', stretch=NO, minwidth=0, width=70, anchor = tk.CENTER)
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 10), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    Treepopup = Menu(tree2, tearoff=0)
    tree2.pack()

    ## Database connections
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")

    # # All Functions defining
    def Treepopup_do_popup(event):
        try:
            Treepopup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            Treepopup.grab_release()

    def GetASOCCodeProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_ASOCCodeProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                ASOCCodeProfileDB_DF  = pd.DataFrame(Complete_df)
                ASOCCodeProfileDB_DF =ASOCCodeProfileDB_DF.loc[:,["ASOCCode"]]
                ASOCCodeProfileDB_DF  =ASOCCodeProfileDB_DF.reset_index(drop=True)
                ASOCCodeProfileDB_DF.rename(columns={"ASOCCode":"ASOCCode"},inplace = True)
                ASOCCodeProfileDB_DF  = pd.DataFrame(ASOCCodeProfileDB_DF)
                return ASOCCodeProfileDB_DF
            else:
                messagebox.showerror('ASOCCode Lookup Table Message', "Void ASOCCode Lookup Table...Please Import/Insert ASOCCode Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def viewQCFailed():
        try:
            con= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cur=con.cursor()
            cur.execute("SELECT DataBase_ID, RecordIdentifier, DeploymentUID, ASOCCode FROM SetCatch_QCFailedLookUpTable_ASOCCode ORDER BY `DataBase_ID` ASC")
            rows=cur.fetchall()
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_ASOCCodeProfile():
        ClearASOCCodeFailedResultsTable_A()
        countIndex = 0
        rows = viewQCFailed()
        for row in rows:
            if countIndex % 2 == 0:
                tree1.insert("", tk.END, values=row, tags =("even",))
            else:
                tree1.insert("", tk.END, values=row, tags =("odd",))
            countIndex = countIndex+1
        tree1.tag_configure("even",foreground="black", background="lightgreen")
        tree1.tag_configure("odd",foreground="black", background="ghost white")
        QCFailedTotalEntries =len(viewQCFailed())
        txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries) 

    def QCFailedTotalEntries():
        txtTotalFailedEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_ASOCCode ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        QCFailedTotalEntries = len(data)       
        txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)             
        conn.commit()
        conn.close()

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP ASOCCode Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def ClearQCFailedSpeciesProfileDetails():
        txtDatabaseID.delete(0,END)
        txtRecordIdentifier.delete(0,END)
        txtDeploymentUID.delete(0,END)
        txtASOCCode.delete(0,END)
        
    def CheckASOCCodeCodeValidity(UserEntryASOCCodeCode):
        ASOCCodeCodeFound = "Modied/Updated ASOCCode Code Found In ASOCCode lookup Table"
        ASOCCodeCodeNotFound = "Modied/Updated ASOCCode Code Not Found In ASOCCode lookup Table"
        if((UserEntryASOCCodeCode!='')):
            try:
                UserEntryASOCCodeCode = int(UserEntryASOCCodeCode)
                Complete_df = GetASOCCodeProfileDB()
                data = pd.DataFrame(Complete_df)
                data = data.reset_index(drop=True)
                if (UserEntryASOCCodeCode in data["ASOCCode"].unique()) == True: 
                    return ASOCCodeCodeFound
                else: 
                    return ASOCCodeCodeNotFound
            except:
                return tkinter.messagebox.showerror("Update Error"," ASOCCode Must Be Integer Value")
        else:
                return tkinter.messagebox.showerror("Update Error"," ASOCCode Entry Can Not Be Empty")
        
    def Modify_SetCatch_ASOCCodeProfile():
        ASOCCodeCodeFound = "Modied/Updated ASOCCode Code Found In ASOCCode lookup Table"
        ASOCCodeCodeNotFound = "Modied/Updated ASOCCode Code Not Found In ASOCCode lookup Table"
        UserEntryASOCCodeCode = txtASOCCode.get()
        EntryValidityASOCCodeCode = CheckASOCCodeCodeValidity(UserEntryASOCCodeCode)
        if EntryValidityASOCCodeCode == ASOCCodeCodeFound:
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
                        DataBase_ID = int(txtDatabaseID.get())
                        RecordIdentifier = int(txtRecordIdentifier.get())
                        DeploymentUID = txtDeploymentUID.get()
                        ASOCCode = txtASOCCode.get()
                        if (list_item_DatabaseUID == DataBase_ID) & \
                            (list_item_RecordIdentifier == RecordIdentifier) &\
                            (list_item_DeploymentUID == DeploymentUID):
                            if(ASOCCode!=0):
                                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                conn_DB_SetCatch_Validation_LookupTables= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
                                cur_DB_SetCatch_Validation_LookupTables=conn_DB_SetCatch_Validation_LookupTables.cursor()
                                cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (ASOCCode, DataBase_ID, RecordIdentifier, DeploymentUID))
                                cur_DB_SetCatch_Validation_LookupTables.execute("UPDATE SetCatch_QCFailedLookUpTable_ASOCCode SET ASOCCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (ASOCCode, DataBase_ID, RecordIdentifier, DeploymentUID))
                                conn_DB_Set_Catch_Analysis.commit()
                                conn_DB_Set_Catch_Analysis.close()
                                conn_DB_SetCatch_Validation_LookupTables.commit()
                                conn_DB_SetCatch_Validation_LookupTables.close()
                                tree1.delete(*tree1.get_children())
                                tree1.insert("", tk.END,values=(DataBase_ID, RecordIdentifier, DeploymentUID, ASOCCode ))
                                QCFailedTotalEntries()
                                ClearASOCCodeFailedSummaryTable_B()
                            else:
                                tkinter.messagebox.showerror("Update Error"," ASOCCode Entry can not be empty")
                        else:
                            tkinter.messagebox.showerror("Update Error","You Are Not Allowed to Modify DataBase_ID, RecordIdentifier And DeploymentUID")
                else:
                    UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                            "1. Please Select One Entry Only From The ASOCCode Table To Update "  + '\n' + '\n' + 
                            "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                            "3. Please Do Not Update Without Selecting Entry From ASOCCode Table" )
                    tkinter.messagebox.showerror("Update Error Possible Reasons",UpdatePossibleError)
            else:
                tkinter.messagebox.showerror("Update Error Possible Reasons"," Please Select One Entry To Modify")
        else:
            tkinter.messagebox.showerror("Update/Modification Error In Set & Catch DB", ASOCCodeCodeNotFound + ".  " +  "Please Update ASOCCode Lookup Table With The Correct ASOCCode")

    def ClearAllASOCCodeQCFailedTable():
        tree1.delete(*tree1.get_children())
        tree2.delete(*tree2.get_children())
        txtTotalFailedEntries.delete(0,END)
        txtSelectedFailedEntries.delete(0,END)   

    def ClearASOCCodeFailedSummaryTable_B():
        tree2.delete(*tree2.get_children())
        txtSelectedFailedEntries.delete(0,END)

    def ClearASOCCodeFailedResultsTable_A():
        tree1.delete(*tree1.get_children())
        txtTotalFailedEntries.delete(0,END)
        
    def InventoryRec1(event):
        for nm in tree1.selection():
            sd = tree1.item(nm, 'values')
            txtDatabaseID.delete(0,END)
            txtDatabaseID.insert(tk.END,sd[0]) 
            txtRecordIdentifier.delete(0,END)
            txtRecordIdentifier.insert(tk.END,sd[1])                
            txtDeploymentUID.delete(0,END)
            txtDeploymentUID.insert(tk.END,sd[2])
            txtASOCCode.delete(0,END)
            txtASOCCode.insert(tk.END,sd[3])

    def Export_QCFailedASOCCode_CSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_ASOCCode ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("QC Failed ASOCCode Profile","QC Failed ASOCCode Profile Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("QC Failed ASOCCode Profile Report Message","Please Select File Name To Export")
            else:
                messagebox.showerror('Export Error', "Void File... Nothing to Export")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def Modify_MultipleSetCatch_ASOCCodeProfile():
        dfList =[] 
        for child in tree1.get_children():
            df = tree1.item(child)["values"]
            dfList.append(df)
        ListBox_DF = pd.DataFrame(dfList)
        if len(ListBox_DF)>0:
            cur_id = tree1.focus()
            selvalue = tree1.item(cur_id)['values']
            Length_Selected  =  (len(selvalue))
            if Length_Selected != 0:
                SelectionTree = tree1.selection()
                if (len(SelectionTree)>0):
                    iUpdate = tkinter.messagebox.askyesno("Update Multiple Entries In  DFO-NL-ASOP Set & Catch Database", 
                            "Confirm If You Want To Update Multiple ASOCCode Entries In DFO-NL-ASOP Set & Catch Database")
                    if iUpdate >0:
                        application_window = window
                        Input_UpdateAnswer = simpledialog.askstring("Input Updated ASOCCode ", "What is Your Updated ASOCCode Value?",
                                                                parent=application_window)
                        if Input_UpdateAnswer is not None:
                            Input_UpdatedASOCCodeCode = (Input_UpdateAnswer)
                            ASOCCodeCodeFound = "Modied/Updated ASOCCode Code Found In ASOCCode lookup Table"
                            ASOCCodeCodeNotFound = "Modied/Updated ASOCCode Code Not Found In ASOCCode lookup Table"
                            EntryValidityASOCCodeCode = CheckASOCCodeCodeValidity(Input_UpdatedASOCCodeCode)
                            if EntryValidityASOCCodeCode == ASOCCodeCodeFound:
                                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                conn_DB_SetCatch_Validation_LookupTables= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
                                cur_DB_SetCatch_Validation_LookupTables=conn_DB_SetCatch_Validation_LookupTables.cursor()
                                for item in SelectionTree:
                                    list_item = (tree1.item(item, 'values'))
                                    list_item_DatabaseUID = int(list_item[0])
                                    list_item_RecordIdentifier = int(list_item[1])
                                    list_item_DeploymentUID = (list_item[2])
                                    Input_UpdatedASOCCodeCode =int(Input_UpdatedASOCCodeCode)
                                    cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (Input_UpdatedASOCCodeCode, list_item_DatabaseUID, list_item_RecordIdentifier, list_item_DeploymentUID))
                                    cur_DB_SetCatch_Validation_LookupTables.execute("UPDATE SetCatch_QCFailedLookUpTable_ASOCCode SET ASOCCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        (Input_UpdatedASOCCodeCode, list_item_DatabaseUID, list_item_RecordIdentifier, list_item_DeploymentUID))
                                conn_DB_Set_Catch_Analysis.commit()
                                conn_DB_Set_Catch_Analysis.close()
                                conn_DB_SetCatch_Validation_LookupTables.commit()
                                conn_DB_SetCatch_Validation_LookupTables.close()
                                viewQCFailed_ASOCCodeProfile()
                                ClearASOCCodeFailedSummaryTable_B()
                                return
                            else:
                                tkinter.messagebox.showerror("Update/Modification Error In Set & Catch DB",
                                                            ASOCCodeCodeNotFound + ".  " +  
                                                            "Please Update ASOCCode Lookup Table With The Correct ASOCCode")
                        else:
                            tkinter.messagebox.showinfo("Update Error","Please Input Updated ASOCCode Value")   
            else:
                tkinter.messagebox.showinfo("Update Error","Please Select At least One Entries To Update ASOCCode")
        else:
            tkinter.messagebox.showinfo("Update Error","Empty ASOCCode Table. Please Select At least One Entries In The Table To Update ASOCCode ")

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
            conn = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_ASOCCode ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','ASOCCode','DeploymentIdentifier']]
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
        SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[SetCatchProfileDB_DF['RecordType'] == 2]
        SetCatchProfileDB_DF['DataBase_ID'] = (SetCatchProfileDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['RecordIdentifier'] = (SetCatchProfileDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['ASOCCode'] = (SetCatchProfileDB_DF.loc[:,['ASOCCode']]).replace('', 99999999)
        SetCatchProfileDB_DF['ASOCCode'] = (SetCatchProfileDB_DF.loc[:,['ASOCCode']]).astype(int, errors='ignore')
        
        SetCatchQCFailedDB_DF = GetSetCatchQCFailedDB()
        SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        SetCatchQCFailedDB_DF['ASOCCode'] = (SetCatchQCFailedDB_DF.loc[:,['ASOCCode']]).replace('', 99999999)
        SetCatchQCFailedDB_DF['ASOCCode'] = (SetCatchQCFailedDB_DF.loc[:,['ASOCCode']]).astype(int, errors='ignore')

        Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                                    SetCatchQCFailedDB_DF, on = ["DataBase_ID", "RecordIdentifier", "DeploymentUID", "ASOCCode"], indicator=True, 
                                    how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.iloc[:,0:len(list(SetCatchProfileDB_DF.columns))]

        Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['ASOCCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['ASOCCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['ASOCCode']]).replace(99999999, '')

        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
        
        root = tk.Tk()
        root.title ("DFO-NL-ASOP ASOCCode Validation Failed On Set & Catch Imported Data")
        root.geometry("1200x600+200+100")
        root.config(bg="cadet blue")
        root.resizable(0, 0)
        Tableframe = tk.Frame(root, width = 1150, height = 800, bd = 2, padx= 3, pady= 10, relief = RIDGE)
        Tableframe.pack(fill='both', expand=True)
        tree = ttk.Treeview(Tableframe, height=27, selectmode ='browse')
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
        style.configure("Treeview.Heading",font=('aerial', 8,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
        tree.pack()
        List_Columns = list(Ref_FailedQC_InSetcatchDB.columns)
        tree['column'] = List_Columns
        tree['show'] = "headings"
        for col in tree['column']:
            tree.heading(col, text=col, anchor = tk.CENTER)
            tree.column(col, stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
        df_rows = Ref_FailedQC_InSetcatchDB.to_numpy().tolist()
        countIndex = 0
        for row in df_rows:
            if countIndex % 2 == 0:
                tree.insert("", "end", values =row, tags =("even",))
            else:
                tree.insert("", "end", values =row, tags =("odd",))
            countIndex = countIndex+1
        tree.tag_configure("even",foreground="black", background="lightblue")
        tree.tag_configure("odd",foreground="black", background="ghost white")
        root.mainloop()

    def SubmitDataFrameToQCFailedDB(DataFrameToSubmit):
        try:
            Import_To_DBStorage = pd.DataFrame(DataFrameToSubmit)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Import_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_ASOCCode', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def GenDepIdfier_Col_SetCatchFailDB():
        QCFailedASOCCodeDB= GetSetCatchQCFailedDB()
        if len(QCFailedASOCCodeDB)>0:
            txtTotalFailedEntries.delete(0,END)
            QCFailedASOCCodeDB['DeploymentIdentifier'] = QCFailedASOCCodeDB['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            QCFailedASOCCodeDB['DeploymentIdentifier'] = QCFailedASOCCodeDB['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            QCFailedASOCCodeDB = QCFailedASOCCodeDB.reset_index(drop=True)
            DataFrameToSubmit = pd.DataFrame(QCFailedASOCCodeDB)
            SubmitDataFrameToQCFailedDB(DataFrameToSubmit)
            QCFailedTotalEntries = len(DataFrameToSubmit)       
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)    

    def GenQCFailedSummaryTable():
        ClearASOCCodeFailedSummaryTable_B()
        QCFailedASOCCodeDB= GetSetCatchQCFailedDB()
        QCFailedASOCCodeDB['ASOCCode'] = (QCFailedASOCCodeDB.loc[:,['ASOCCode']]).replace(99999999, '')
        QCFailedASOCCodeDB['ASOCCode'] = (QCFailedASOCCodeDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
        QCFailedASOCCodeDB   = QCFailedASOCCodeDB.groupby(['DeploymentIdentifier', 'ASOCCode'], as_index=False).DataBase_ID.count()
        QCFailedASOCCodeDB   = pd.DataFrame(QCFailedASOCCodeDB)
        QCFailedASOCCodeDB.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                            'ASOCCode': 'ASOCCode', 
                                            'DataBase_ID':'TotalCount'},inplace = True)
        QCFailedASOCCodeDB['ASOCCode'] = (QCFailedASOCCodeDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
        QCFailedASOCCodeDB['ASOCCode'] = (QCFailedASOCCodeDB.loc[:,['ASOCCode']]).replace(99999999, '')   
        QCFailedASOCCodeDB = QCFailedASOCCodeDB.reset_index(drop=True)
        QCFailedASOCCodeDB = pd.DataFrame(QCFailedASOCCodeDB)
        countIndex1 = 0
        for each_rec in range(len(QCFailedASOCCodeDB)):
            if countIndex1 % 2 == 0:
                tree2.insert("", tk.END, values=list(QCFailedASOCCodeDB.loc[each_rec]), tags =("even",))
            else:
                tree2.insert("", tk.END, values=list(QCFailedASOCCodeDB.loc[each_rec]), tags =("odd",))
            countIndex1 = countIndex1+1
        tree2.tag_configure("even",foreground="black", background="lightblue")
        tree2.tag_configure("odd",foreground="black", background="ghost white")

    def Search_AND_MultiVariableQuery_Backend(DeploymentIdentifier ="", ASOCCode =""):
        try:
            conn_DB_SetCatch_Validation_LookUpTable= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cur_DB_SetCatch_Validation_LookUpTable=conn_DB_SetCatch_Validation_LookUpTable.cursor()

            cur_DB_SetCatch_Validation_LookUpTable.execute("SELECT * FROM SetCatch_QCFailedLookUpTable_ASOCCode WHERE \
                                            (DeploymentIdentifier = :DeploymentIdentifier OR TRIM(COALESCE(:DeploymentIdentifier, '')) = '') AND\
                                            (ASOCCode= :ASOCCode)",\
                                            (DeploymentIdentifier, ASOCCode))
            rows=cur_DB_SetCatch_Validation_LookUpTable.fetchall()
            return rows
        except:
            messagebox.showerror('ASOCCode Variable Error Message', "ASOCCode Query Failed")

    def InventoryRec2(event):
        for nm in tree2.selection():
            sd = tree2.item(nm, 'values')
            txtDatabaseID.delete(0,END)
            txtRecordIdentifier.delete(0,END)          
            txtDeploymentUID.delete(0,END)
            txtDeploymentUID.insert(tk.END,sd[0])
            txtASOCCode.delete(0,END)
            txtASOCCode.insert(tk.END,sd[1])
            DeploymentIdentifier = sd[0]
            ASOCCode = sd[1]
            MultiSearchRows = Search_AND_MultiVariableQuery_Backend(DeploymentIdentifier, ASOCCode)
            MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','ASOCCode','DeploymentIdentifier'])
            MultiSearchRowsDF = MultiSearchRowsDF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','ASOCCode','DeploymentIdentifier']]
            MultiSearchRowsDF.reset_index(drop=True)
            MultiSearchRowsDF  = pd.DataFrame(MultiSearchRowsDF)
            QCFailedSelectedEntries = len(MultiSearchRowsDF) 
            tree1.delete(*tree1.get_children())
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
            txtSelectedFailedEntries.delete(0,END)
            txtSelectedFailedEntries.insert(tk.END,QCFailedSelectedEntries)

    def SummarySelectUpdateClearFromQCFailDB():
        dfList =[] 
        for child in tree2.get_children():
            df = tree2.item(child)["values"]
            dfList.append(df)
        ListBox_DF = pd.DataFrame(dfList)
        if len(ListBox_DF)>0:
            cur_id = tree2.focus()
            selvalue = tree2.item(cur_id)['values']
            Length_Selected  =  (len(selvalue))
            if Length_Selected != 0:
                SelectionTree = tree2.selection()
                if (len(SelectionTree)>0) & (len(SelectionTree)==1) & (len(SelectionTree)<2):
                    application_window = window
                    Input_UpdateAnswer = simpledialog.askstring("Input Updated ASOCCode", "What is Your Updated ASOCCode Value?", parent=application_window)
                    if Input_UpdateAnswer is not None:
                        Input_UpdatedASOCCodeCode = (Input_UpdateAnswer)
                        ASOCCodeCodeFound = "Modied/Updated ASOCCode Code Found In ASOCCode lookup Table"
                        ASOCCodeCodeNotFound = "Modied/Updated ASOCCode Code Not Found In ASOCCode lookup Table"
                        EntryValidityASOCCodeCode = CheckASOCCodeCodeValidity(Input_UpdatedASOCCodeCode)
                        if EntryValidityASOCCodeCode == ASOCCodeCodeFound:
                            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                            conn_DB_SetCatch_Validation_LookupTables= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
                            cur_DB_SetCatch_Validation_LookupTables=conn_DB_SetCatch_Validation_LookupTables.cursor()
                            for child in tree1.get_children():
                                list_item = tree1.item(child)["values"]
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                Input_UpdatedASOCCodeCode =int(Input_UpdatedASOCCodeCode)
                                cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (Input_UpdatedASOCCodeCode, list_item_DatabaseUID, list_item_RecordIdentifier, list_item_DeploymentUID))
                                cur_DB_SetCatch_Validation_LookupTables.execute("DELETE FROM SetCatch_QCFailedLookUpTable_ASOCCode WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID = ? ", 
                                    (list_item_DatabaseUID, list_item_RecordIdentifier, list_item_DeploymentUID,))
                            conn_DB_Set_Catch_Analysis.commit()
                            conn_DB_Set_Catch_Analysis.close()
                            conn_DB_SetCatch_Validation_LookupTables.commit()
                            conn_DB_SetCatch_Validation_LookupTables.close()
                            tree1.delete(*tree1.get_children())
                            txtSelectedFailedEntries.delete(0,END)
                            tree2.delete(SelectionTree)
                            QCFailedTotalEntries()
                            return                     
                        else:
                            tkinter.messagebox.showerror("Update/Modification Error In Set & Catch DB", ASOCCodeCodeNotFound + ".  " +  "Please Update ASOCCode Lookup Table With The Correct ASOCCode")
                    else:
                        tkinter.messagebox.showinfo("Update Error","Please Input Updated ASOCCode Value")   
                else:
                    tkinter.messagebox.showerror("Update Error Possible Reasons"," Please Do Not Select Multi Entry From Table B To Update")
            else:
                tkinter.messagebox.showerror("Update Error Possible Reasons"," Please Select One Entry From Table B To Update")
        else:
            tkinter.messagebox.showinfo("Update Error","Empty ASOCCode Summary Table : B")

    # Tree 1 & 2 View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    tree2.bind('<<TreeviewSelect>>',InventoryRec2)

    # Generate Deployment Identifier Column In QC Failed DB
    GenDepIdfier_Col_SetCatchFailDB()

    ## Button Wizard : Entries A
    btnModifyASOCCodeProfile = Button(TopLeftframe, text="Modify Code & Update DB", font=('aerial', 10, 'bold'), 
                            height =1, width=25, bd=2, command = Modify_SetCatch_ASOCCodeProfile)
    btnModifyASOCCodeProfile.grid(row =10, column = 0, padx=2, pady =5, ipady =5, sticky =W)

    btnClearDetails = Button(TopLeftframe, text="Clear Details", font=('aerial', 10, 'bold'),
                            height =1, width=12, bd=1, command = ClearQCFailedSpeciesProfileDetails)
    btnClearDetails.grid(row =10, column = 0, padx=2, pady =5, ipady =5, sticky =E)

    ## Button Wizard : Table B
    btnGenQCFailedASOCCodeSummary = Button(TopBottomLeftframe, text="Generate Failed Summary", font=('aerial', 11, 'bold'), bg='alice blue',
                            height =1, width=21, bd=2, command = GenQCFailedSummaryTable)
    btnGenQCFailedASOCCodeSummary.grid(row =2, column = 0, padx=2, pady =4, ipady =8, sticky =W)

    btnSelectUpdateSummaryTable = Button(TopBottomLeftframe, text="Select-Update &\n Clear", font=('aerial', 11, 'bold'), bg='alice blue',
                                height =1, width=14, bd=2, command = SummarySelectUpdateClearFromQCFailDB)
    btnSelectUpdateSummaryTable.grid(row =2, column = 0, padx=2, pady =5, ipady =8, sticky =E)

    ## Button Wizard : Table C
    btnClearASOCCodeTable = Button(TopRightframe, text="Clear All Table", font=('aerial', 10, 'bold'), 
                                height =1, width=12, bd=1, command = ClearAllASOCCodeQCFailedTable)
    btnClearASOCCodeTable.grid(row =2, column = 0, padx=2, pady =1, ipady =2, sticky =E)

    btnViewQCFailedQCSpeciesResults = Button(TopRightframe, text="View All QC-Failed Results", font=('aerial', 11, 'bold'), bg='alice blue',
                            height =1, width=22, bd=2, command = viewQCFailed_ASOCCodeProfile)
    btnViewQCFailedQCSpeciesResults.grid(row =4, column = 0, padx=2, pady =2, ipady =4, sticky =W)

    btnRefAllResultsInSetCatchDB = Button(TopRightframe, text="Ref All Results In Set&Catch DB", font=('aerial', 11, 'bold'), bg='alice blue',
                                height =1, width=26, bd=2, command = RefFailedToSetcatchDB)
    btnRefAllResultsInSetCatchDB.grid(row =4, column = 0, padx=2, pady =2, ipady =4, sticky =E)

    # ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)  
    filemenu.add_command(label="Exit", command=iExit)
    filemenu.add_command(label="Export DB All QC Failed Results", command=Export_QCFailedASOCCode_CSV)

    Treepopup.add_command(label="Modify & Update DB With Selected ASOCCode In Table C", command=Modify_MultipleSetCatch_ASOCCodeProfile)
    Treepopup.add_separator()
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    window.mainloop()










