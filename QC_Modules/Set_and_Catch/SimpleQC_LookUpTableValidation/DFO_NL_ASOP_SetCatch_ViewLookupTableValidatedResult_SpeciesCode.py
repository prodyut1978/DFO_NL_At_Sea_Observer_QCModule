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

def SetCatch_ViewLookupValidatedResult_SpeciesCode():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Lookup SpeciesCode Validator - ID-C-01-9")
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
    SpeciesCode       = IntVar(TopLeftframe, value='')

    lblTitEntry = Label(TopLeftframe, font=('aerial', 11, 'bold'), text="A: SpeciesCode QC Failed Profile Details")
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

    lblSpeciesCodeCode = Label(TopLeftframe, font=('aerial', 10, 'bold'), text = "4. SpeciesCode :", padx =0, pady= 2)
    lblSpeciesCodeCode.grid(row =8, column = 0, padx=4, pady =2, sticky =W)
    txtSpeciesCode  = Entry(TopLeftframe, font=('aerial', 12, 'bold'),textvariable= SpeciesCode, width = 35)
    txtSpeciesCode.grid(row =9, column = 0, padx=4, pady =4,ipadx=1, sticky =W)

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

    lblQCFailedResultSpeciesCode = Label(TopRightframe, font=('aerial', 11, 'bold'), text="C: View QC Failed Results Table")
    lblQCFailedResultSpeciesCode.grid(row =2, column = 0, padx=5, pady =2, ipady =2, sticky =W, rowspan =1)
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
    tree1.heading("#4", text="SpeciesCode", anchor=CENTER)
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
    tree2.heading("#2", text="SpeciesCode", anchor=CENTER)
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

    def GetSpeciesCodeProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SpeciesCodeProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                SpeciesCodeProfileDB_DF  = pd.DataFrame(Complete_df)
                SpeciesCodeProfileDB_DF =SpeciesCodeProfileDB_DF.loc[:,["SpeciesCode"]]
                SpeciesCodeProfileDB_DF  =SpeciesCodeProfileDB_DF.reset_index(drop=True)
                SpeciesCodeProfileDB_DF.rename(columns={"SpeciesCode":"SpeciesCode"},inplace = True)
                SpeciesCodeProfileDB_DF  = pd.DataFrame(SpeciesCodeProfileDB_DF)
                return SpeciesCodeProfileDB_DF
            else:
                messagebox.showerror('SpeciesCode Lookup Table Message', "Void SpeciesCode Lookup Table...Please Import/Insert SpeciesCode Lookup Table")
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
            cur.execute("SELECT DataBase_ID, RecordIdentifier, DeploymentUID, SpeciesCode FROM SetCatch_QCFailedLookUpTable_SpeciesCode ORDER BY `DataBase_ID` ASC")
            rows=cur.fetchall()
            return rows
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if con:
                cur.close()
                con.close()

    def viewQCFailed_SpeciesCodeProfile():
        ClearSpeciesCodeFailedResultsTable_A()
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
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_SpeciesCode ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        QCFailedTotalEntries = len(data)       
        txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)             
        conn.commit()
        conn.close()

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP SpeciesCode Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def ClearQCFailedSpeciesProfileDetails():
        txtDatabaseID.delete(0,END)
        txtRecordIdentifier.delete(0,END)
        txtDeploymentUID.delete(0,END)
        txtSpeciesCode.delete(0,END)
        
    def CheckSpeciesCodeCodeValidity(UserEntrySpeciesCodeCode):
        SpeciesCodeCodeFound = "Modied/Updated SpeciesCode Code Found In SpeciesCode lookup Table"
        SpeciesCodeCodeNotFound = "Modied/Updated SpeciesCode Code Not Found In SpeciesCode lookup Table"
        if((UserEntrySpeciesCodeCode!='')):
            try:
                UserEntrySpeciesCodeCode = int(UserEntrySpeciesCodeCode)
                Complete_df = GetSpeciesCodeProfileDB()
                data = pd.DataFrame(Complete_df)
                data = data.reset_index(drop=True)
                if (UserEntrySpeciesCodeCode in data["SpeciesCode"].unique()) == True: 
                    return SpeciesCodeCodeFound
                else: 
                    return SpeciesCodeCodeNotFound
            except:
                return tkinter.messagebox.showerror("Update Error"," SpeciesCode Must Be Integer Value")
        else:
                return tkinter.messagebox.showerror("Update Error"," SpeciesCode Entry Can Not Be Empty")
        
    def Modify_SetCatch_SpeciesCodeProfile():
        SpeciesCodeCodeFound = "Modied/Updated SpeciesCode Code Found In SpeciesCode lookup Table"
        SpeciesCodeCodeNotFound = "Modied/Updated SpeciesCode Code Not Found In SpeciesCode lookup Table"
        UserEntrySpeciesCodeCode = txtSpeciesCode.get()
        EntryValiditySpeciesCodeCode = CheckSpeciesCodeCodeValidity(UserEntrySpeciesCodeCode)
        if EntryValiditySpeciesCodeCode == SpeciesCodeCodeFound:
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
                        SpeciesCode = txtSpeciesCode.get()
                        if (list_item_DatabaseUID == DataBase_ID) & \
                            (list_item_RecordIdentifier == RecordIdentifier) &\
                            (list_item_DeploymentUID == DeploymentUID):
                            if(SpeciesCode!=0):
                                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                conn_DB_SetCatch_Validation_LookupTables= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
                                cur_DB_SetCatch_Validation_LookupTables=conn_DB_SetCatch_Validation_LookupTables.cursor()
                                cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SpeciesCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (SpeciesCode, DataBase_ID, RecordIdentifier, DeploymentUID))
                                cur_DB_SetCatch_Validation_LookupTables.execute("UPDATE SetCatch_QCFailedLookUpTable_SpeciesCode SET SpeciesCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (SpeciesCode, DataBase_ID, RecordIdentifier, DeploymentUID))
                                conn_DB_Set_Catch_Analysis.commit()
                                conn_DB_Set_Catch_Analysis.close()
                                conn_DB_SetCatch_Validation_LookupTables.commit()
                                conn_DB_SetCatch_Validation_LookupTables.close()
                                tree1.delete(*tree1.get_children())
                                tree1.insert("", tk.END,values=(DataBase_ID, RecordIdentifier, DeploymentUID, SpeciesCode ))
                                QCFailedTotalEntries()
                                ClearSpeciesCodeFailedSummaryTable_B()
                            else:
                                tkinter.messagebox.showerror("Update Error"," SpeciesCode Entry can not be empty")
                        else:
                            tkinter.messagebox.showerror("Update Error","You Are Not Allowed to Modify DataBase_ID, RecordIdentifier And DeploymentUID")
                else:
                    UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                            "1. Please Select One Entry Only From The SpeciesCode Table To Update "  + '\n' + '\n' + 
                            "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                            "3. Please Do Not Update Without Selecting Entry From SpeciesCode Table" )
                    tkinter.messagebox.showerror("Update Error Possible Reasons",UpdatePossibleError)
            else:
                tkinter.messagebox.showerror("Update Error Possible Reasons"," Please Select One Entry To Modify")
        else:
            tkinter.messagebox.showerror("Update/Modification Error In Set & Catch DB", SpeciesCodeCodeNotFound + ".  " +  "Please Update SpeciesCode Lookup Table With The Correct SpeciesCode")

    def ClearAllSpeciesCodeQCFailedTable():
        tree1.delete(*tree1.get_children())
        tree2.delete(*tree2.get_children())
        txtTotalFailedEntries.delete(0,END)
        txtSelectedFailedEntries.delete(0,END)   

    def ClearSpeciesCodeFailedSummaryTable_B():
        tree2.delete(*tree2.get_children())
        txtSelectedFailedEntries.delete(0,END)
    
    def ClearSpeciesCodeFailedResultsTable_A():
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
            txtSpeciesCode.delete(0,END)
            txtSpeciesCode.insert(tk.END,sd[3])

    def Export_QCFailedSpeciesCode_CSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_SpeciesCode ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("QC Failed SpeciesCode Profile","QC Failed SpeciesCode Profile Report Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("QC Failed SpeciesCode Profile Report Message","Please Select File Name To Export")
            else:
                messagebox.showerror('Export Error', "Void File... Nothing to Export")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def Modify_MultipleSetCatch_SpeciesCodeProfile():
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
                            "Confirm If You Want To Update Multiple SpeciesCode Entries In DFO-NL-ASOP Set & Catch Database")
                    if iUpdate >0:
                        application_window = window
                        Input_UpdateAnswer = simpledialog.askstring("Input Updated SpeciesCode ", "What is Your Updated SpeciesCode  Value?",
                                                                parent=application_window)
                        if Input_UpdateAnswer is not None:
                            Input_UpdatedSpeciesCodeCode = (Input_UpdateAnswer)
                            SpeciesCodeCodeFound = "Modied/Updated SpeciesCode Code Found In SpeciesCode lookup Table"
                            SpeciesCodeCodeNotFound = "Modied/Updated SpeciesCode Code Not Found In SpeciesCode lookup Table"
                            EntryValiditySpeciesCodeCode = CheckSpeciesCodeCodeValidity(Input_UpdatedSpeciesCodeCode)
                            if EntryValiditySpeciesCodeCode == SpeciesCodeCodeFound:
                                conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                                cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                                conn_DB_SetCatch_Validation_LookupTables= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
                                cur_DB_SetCatch_Validation_LookupTables=conn_DB_SetCatch_Validation_LookupTables.cursor()
                                for item in SelectionTree:
                                    list_item = (tree1.item(item, 'values'))
                                    list_item_DatabaseUID = int(list_item[0])
                                    list_item_RecordIdentifier = int(list_item[1])
                                    list_item_DeploymentUID = (list_item[2])
                                    Input_UpdatedSpeciesCodeCode =int(Input_UpdatedSpeciesCodeCode)
                                    cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SpeciesCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (Input_UpdatedSpeciesCodeCode, list_item_DatabaseUID, list_item_RecordIdentifier, list_item_DeploymentUID))
                                    cur_DB_SetCatch_Validation_LookupTables.execute("UPDATE SetCatch_QCFailedLookUpTable_SpeciesCode SET SpeciesCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                        (Input_UpdatedSpeciesCodeCode, list_item_DatabaseUID, list_item_RecordIdentifier, list_item_DeploymentUID))
                                conn_DB_Set_Catch_Analysis.commit()
                                conn_DB_Set_Catch_Analysis.close()
                                conn_DB_SetCatch_Validation_LookupTables.commit()
                                conn_DB_SetCatch_Validation_LookupTables.close()
                                viewQCFailed_SpeciesCodeProfile()
                                ClearSpeciesCodeFailedSummaryTable_B()
                                return
                            else:
                                tkinter.messagebox.showerror("Update/Modification Error In Set & Catch DB",
                                                            SpeciesCodeCodeNotFound + ".  " +  
                                                            "Please Update SpeciesCode Lookup Table With The Correct SpeciesCode")
                        else:
                            tkinter.messagebox.showinfo("Update Error","Please Input Updated SpeciesCode Value")   
            else:
                tkinter.messagebox.showinfo("Update Error","Please Select At least One Entries To Update SpeciesCode")
        else:
            tkinter.messagebox.showinfo("Update Error","Empty SpeciesCode Table. Please Select At least One Entries In The Table To Update SpeciesCode ")

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
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_SpeciesCode ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','SpeciesCode','DeploymentIdentifier']]
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
        SetCatchProfileDB_DF['SpeciesCode'] = (SetCatchProfileDB_DF.loc[:,['SpeciesCode']]).replace('', 99999999)
        SetCatchProfileDB_DF['SpeciesCode'] = (SetCatchProfileDB_DF.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
        
        SetCatchQCFailedDB_DF = GetSetCatchQCFailedDB()
        SetCatchQCFailedDB_DF['DataBase_ID'] = (SetCatchQCFailedDB_DF.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        SetCatchQCFailedDB_DF['RecordIdentifier'] = (SetCatchQCFailedDB_DF.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).replace('', 99999999)
        SetCatchQCFailedDB_DF['SpeciesCode'] = (SetCatchQCFailedDB_DF.loc[:,['SpeciesCode']]).astype(int, errors='ignore')

        Ref_FailedQC_InSetcatchDB = SetCatchProfileDB_DF.merge(
                                    SetCatchQCFailedDB_DF, on = ["DataBase_ID", "RecordIdentifier", "DeploymentUID", "SpeciesCode"], indicator=True, 
                                    how='outer').query('_merge == "both"')
        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.iloc[:,0:len(list(SetCatchProfileDB_DF.columns))]

        Ref_FailedQC_InSetcatchDB['DataBase_ID'] = (Ref_FailedQC_InSetcatchDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['RecordIdentifier'] = (Ref_FailedQC_InSetcatchDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['SpeciesCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
        Ref_FailedQC_InSetcatchDB['SpeciesCode'] = (Ref_FailedQC_InSetcatchDB.loc[:,['SpeciesCode']]).replace(99999999, '')

        Ref_FailedQC_InSetcatchDB  = Ref_FailedQC_InSetcatchDB.reset_index(drop=True)
        Ref_FailedQC_InSetcatchDB  = pd.DataFrame(Ref_FailedQC_InSetcatchDB)
        
        root = tk.Tk()
        root.title ("DFO-NL-ASOP SpeciesCode Validation Failed On Set & Catch Imported Data")
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
            Import_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_SpeciesCode', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def GenDepIdfier_Col_SetCatchFailDB():
        QCFailedSpeciesCodeDB= GetSetCatchQCFailedDB()
        if len(QCFailedSpeciesCodeDB)>0:
            txtTotalFailedEntries.delete(0,END)
            QCFailedSpeciesCodeDB['DeploymentIdentifier'] = QCFailedSpeciesCodeDB['DeploymentUID'].apply(lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
            QCFailedSpeciesCodeDB['DeploymentIdentifier'] = QCFailedSpeciesCodeDB['DeploymentIdentifier'].apply(lambda x: x[:-1] if x.endswith('-') else x)
            QCFailedSpeciesCodeDB = QCFailedSpeciesCodeDB.reset_index(drop=True)
            DataFrameToSubmit = pd.DataFrame(QCFailedSpeciesCodeDB)
            SubmitDataFrameToQCFailedDB(DataFrameToSubmit)
            QCFailedTotalEntries = len(DataFrameToSubmit)       
            txtTotalFailedEntries.insert(tk.END,QCFailedTotalEntries)    

    def GenQCFailedSummaryTable():
        ClearSpeciesCodeFailedSummaryTable_B()
        QCFailedSpeciesCodeDB= GetSetCatchQCFailedDB()
        QCFailedSpeciesCodeDB['SpeciesCode'] = (QCFailedSpeciesCodeDB.loc[:,['SpeciesCode']]).replace(99999999, '')
        QCFailedSpeciesCodeDB['SpeciesCode'] = (QCFailedSpeciesCodeDB.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
        QCFailedSpeciesCodeDB   = QCFailedSpeciesCodeDB.groupby(['DeploymentIdentifier', 'SpeciesCode'], as_index=False).DataBase_ID.count()
        QCFailedSpeciesCodeDB   = pd.DataFrame(QCFailedSpeciesCodeDB)
        QCFailedSpeciesCodeDB.rename(columns={'DeploymentIdentifier':'DeploymentIdentifier',
                                            'SpeciesCode': 'SpeciesCode', 
                                            'DataBase_ID':'TotalCount'},inplace = True)
        QCFailedSpeciesCodeDB['SpeciesCode'] = (QCFailedSpeciesCodeDB.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
        QCFailedSpeciesCodeDB['SpeciesCode'] = (QCFailedSpeciesCodeDB.loc[:,['SpeciesCode']]).replace(99999999, '')   
        QCFailedSpeciesCodeDB = QCFailedSpeciesCodeDB.reset_index(drop=True)
        QCFailedSpeciesCodeDB = pd.DataFrame(QCFailedSpeciesCodeDB)
        countIndex1 = 0
        for each_rec in range(len(QCFailedSpeciesCodeDB)):
            if countIndex1 % 2 == 0:
                tree2.insert("", tk.END, values=list(QCFailedSpeciesCodeDB.loc[each_rec]), tags =("even",))
            else:
                tree2.insert("", tk.END, values=list(QCFailedSpeciesCodeDB.loc[each_rec]), tags =("odd",))
            countIndex1 = countIndex1+1
        tree2.tag_configure("even",foreground="black", background="lightblue")
        tree2.tag_configure("odd",foreground="black", background="ghost white")

    def Search_AND_MultiVariableQuery_Backend(DeploymentIdentifier ="", SpeciesCode =""):
        try:
            conn_DB_SetCatch_Validation_LookUpTable= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cur_DB_SetCatch_Validation_LookUpTable=conn_DB_SetCatch_Validation_LookUpTable.cursor()

            cur_DB_SetCatch_Validation_LookUpTable.execute("SELECT * FROM SetCatch_QCFailedLookUpTable_SpeciesCode WHERE \
                                            (DeploymentIdentifier = :DeploymentIdentifier OR TRIM(COALESCE(:DeploymentIdentifier, '')) = '') AND\
                                            (SpeciesCode= :SpeciesCode)",\
                                            (DeploymentIdentifier, SpeciesCode))
            rows=cur_DB_SetCatch_Validation_LookUpTable.fetchall()
            return rows
        except:
            messagebox.showerror('SpeciesCode Variable Error Message', "SpeciesCode Query Failed")

    def InventoryRec2(event):
        for nm in tree2.selection():
            sd = tree2.item(nm, 'values')
            txtDatabaseID.delete(0,END)
            txtRecordIdentifier.delete(0,END)          
            txtDeploymentUID.delete(0,END)
            txtDeploymentUID.insert(tk.END,sd[0])
            txtSpeciesCode.delete(0,END)
            txtSpeciesCode.insert(tk.END,sd[1])
            DeploymentIdentifier = sd[0]
            SpeciesCode = sd[1]
            MultiSearchRows = Search_AND_MultiVariableQuery_Backend(DeploymentIdentifier, SpeciesCode)
            MultiSearchRowsDF = pd.DataFrame(MultiSearchRows, columns =['DataBase_ID', 'RecordIdentifier', 'DeploymentUID','SpeciesCode','DeploymentIdentifier'])
            MultiSearchRowsDF = MultiSearchRowsDF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','SpeciesCode','DeploymentIdentifier']]
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
                    Input_UpdateAnswer = simpledialog.askstring("Input Updated SpeciesCode", "What is Your Updated SpeciesCode Value?", parent=application_window)
                    if Input_UpdateAnswer is not None:
                        Input_UpdatedSpeciesCodeCode = (Input_UpdateAnswer)
                        SpeciesCodeCodeFound = "Modied/Updated SpeciesCode Code Found In SpeciesCode lookup Table"
                        SpeciesCodeCodeNotFound = "Modied/Updated SpeciesCode Code Not Found In SpeciesCode lookup Table"
                        EntryValiditySpeciesCodeCode = CheckSpeciesCodeCodeValidity(Input_UpdatedSpeciesCodeCode)
                        if EntryValiditySpeciesCodeCode == SpeciesCodeCodeFound:
                            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
                            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
                            conn_DB_SetCatch_Validation_LookupTables= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
                            cur_DB_SetCatch_Validation_LookupTables=conn_DB_SetCatch_Validation_LookupTables.cursor()
                            for child in tree1.get_children():
                                list_item = tree1.item(child)["values"]
                                list_item_DatabaseUID = int(list_item[0])
                                list_item_RecordIdentifier = int(list_item[1])
                                list_item_DeploymentUID = (list_item[2])
                                Input_UpdatedSpeciesCodeCode =int(Input_UpdatedSpeciesCodeCode)
                                cur_DB_Set_Catch_Analysis.execute("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SpeciesCode = ? WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID =?", 
                                    (Input_UpdatedSpeciesCodeCode, list_item_DatabaseUID, list_item_RecordIdentifier, list_item_DeploymentUID))
                                cur_DB_SetCatch_Validation_LookupTables.execute("DELETE FROM SetCatch_QCFailedLookUpTable_SpeciesCode WHERE DataBase_ID =? AND RecordIdentifier =? AND DeploymentUID = ? ", 
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
                            tkinter.messagebox.showerror("Update/Modification Error In Set & Catch DB", SpeciesCodeCodeNotFound + ".  " +  "Please Update SpeciesCode Lookup Table With The Correct SpeciesCode")
                    else:
                        tkinter.messagebox.showinfo("Update Error","Please Input Updated SpeciesCode Value")   
                else:
                    tkinter.messagebox.showerror("Update Error Possible Reasons"," Please Do Not Select Multi Entry From Table B To Update")
            else:
                tkinter.messagebox.showerror("Update Error Possible Reasons"," Please Select One Entry From Table B To Update")
        else:
            tkinter.messagebox.showinfo("Update Error","Empty SpeciesCode Summary Table : B")

    # Tree 1 & 2 View Select Event
    tree1.bind('<<TreeviewSelect>>',InventoryRec1)
    tree2.bind('<<TreeviewSelect>>',InventoryRec2)
    
    # Generate Deployment Identifier Column In QC Failed DB
    GenDepIdfier_Col_SetCatchFailDB()

    ## Button Wizard : Entries A
    btnModifySpeciesCodeProfile = Button(TopLeftframe, text="Modify Code & Update DB", font=('aerial', 10, 'bold'), 
                            height =1, width=25, bd=2, command = Modify_SetCatch_SpeciesCodeProfile)
    btnModifySpeciesCodeProfile.grid(row =10, column = 0, padx=2, pady =5, ipady =5, sticky =W)

    btnClearDetails = Button(TopLeftframe, text="Clear Details", font=('aerial', 10, 'bold'),
                            height =1, width=12, bd=1, command = ClearQCFailedSpeciesProfileDetails)
    btnClearDetails.grid(row =10, column = 0, padx=2, pady =5, ipady =5, sticky =E)

    ## Button Wizard : Table B
    btnGenQCFailedSpeciesCodeSummary = Button(TopBottomLeftframe, text="Generate Failed Summary", font=('aerial', 11, 'bold'), bg='alice blue',
                            height =1, width=21, bd=2, command = GenQCFailedSummaryTable)
    btnGenQCFailedSpeciesCodeSummary.grid(row =2, column = 0, padx=2, pady =4, ipady =8, sticky =W)

    btnSelectUpdateSummaryTable = Button(TopBottomLeftframe, text="Select-Update &\n Clear", font=('aerial', 11, 'bold'), bg='alice blue',
                                height =1, width=14, bd=2, command = SummarySelectUpdateClearFromQCFailDB)
    btnSelectUpdateSummaryTable.grid(row =2, column = 0, padx=2, pady =5, ipady =8, sticky =E)

    ## Button Wizard : Table C
    btnClearSpeciesCodeTable = Button(TopRightframe, text="Clear All Table", font=('aerial', 10, 'bold'), 
                                height =1, width=12, bd=1, command = ClearAllSpeciesCodeQCFailedTable)
    btnClearSpeciesCodeTable.grid(row =2, column = 0, padx=2, pady =1, ipady =2, sticky =E)

    btnViewQCFailedQCSpeciesResults = Button(TopRightframe, text="View All QC-Failed Results", font=('aerial', 11, 'bold'), bg='alice blue',
                            height =1, width=22, bd=2, command = viewQCFailed_SpeciesCodeProfile)
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
    filemenu.add_command(label="Export DB All QC Failed Results", command=Export_QCFailedSpeciesCode_CSV)

    Treepopup.add_command(label="Modify & Update DB With Selected SpeciesCode In Table C", command=Modify_MultipleSetCatch_SpeciesCodeProfile)
    Treepopup.add_separator()
    Treepopup.add_command(label="Exit", command=iExit)
    tree1.bind("<Button-3>", Treepopup_do_popup)
    window.mainloop()










