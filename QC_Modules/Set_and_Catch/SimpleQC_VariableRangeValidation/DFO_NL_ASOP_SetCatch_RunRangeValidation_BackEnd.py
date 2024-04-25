from tkinter import*
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import ttk, filedialog
import sqlite3
import pandas as pd
import datetime

def RunSetCatch_RunRangeValidation_BackEnd():
    today = datetime.date.today()
    Currentyear = today.year

    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
    Path_CSV_VariablesRangeFile = './External_Import/VariablesRangeTable_Import/CSV_RangeVariables_ValidationTable/DFO_NL_ASOP_RangeVariables_ValidationTable.csv'

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

    def SubmitImport_To_DBStorage(ImportedVariablesRangeDF):
        try:
            Import_To_DBStorage = pd.DataFrame(ImportedVariablesRangeDF)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Import_To_DBStorage.to_sql('SetCatch_RangeLimitVariables_Define', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def Gen_RangeVariables_FromArchivedCSV():
        df_CSV_VariablesRangeFile = pd.read_csv(Path_CSV_VariablesRangeFile, sep=',' , low_memory=False)
        df_CSV_VariablesRangeFile = df_CSV_VariablesRangeFile.reset_index(drop=True)
        ImportedVariablesRangeDF = pd.DataFrame(df_CSV_VariablesRangeFile)
        ImportedVariablesRangeDF.at[0,'UpperRangeLimitValue']=Currentyear
        ImportedVariablesRangeDF['LowerRangeLimitValue'] = (ImportedVariablesRangeDF.loc[:,
                                                    ['LowerRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
        ImportedVariablesRangeDF['UpperRangeLimitValue'] = (ImportedVariablesRangeDF.loc[:,
                                                    ['UpperRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
        ImportedVariablesRangeDF = ImportedVariablesRangeDF.replace(9999999, '')
        SubmitImport_To_DBStorage(ImportedVariablesRangeDF)

    Get_RangeLimitVariables = fetchData_RangeLimitVariables()
    if (len(Get_RangeLimitVariables)) <= 0:
        Gen_RangeVariables_FromArchivedCSV()
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        
    ## Calender Variables Limit Fetching
    Year_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[0,'LowerRangeLimitValue'])
    Year_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[0,'UpperRangeLimitValue'])
    Year_QCNullValue= Get_RangeLimitVariables.at[0,'QCNullValue']

    Month_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[1,'LowerRangeLimitValue'])
    Month_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[1,'UpperRangeLimitValue'])
    Month_QCNullValue= Get_RangeLimitVariables.at[1,'QCNullValue']

    HaulMonth_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[2,'LowerRangeLimitValue'])
    HaulMonth_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[2,'UpperRangeLimitValue'])
    HaulMonth_QCNullValue= Get_RangeLimitVariables.at[2,'QCNullValue']

    Day_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[3,'LowerRangeLimitValue'])
    Day_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[3,'UpperRangeLimitValue'])
    Day_QCNullValue= Get_RangeLimitVariables.at[3,'QCNullValue']

    HaulDay_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[4,'LowerRangeLimitValue'])
    HaulDay_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[4,'UpperRangeLimitValue'])
    HaulDay_QCNullValue= Get_RangeLimitVariables.at[4,'QCNullValue']

    ## Positional Variables Limit Fetching
    PositionPrecision_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[5,'LowerRangeLimitValue'])
    PositionPrecision_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[5,'UpperRangeLimitValue'])
    PositionPrecision_QCNullValue= Get_RangeLimitVariables.at[5,'QCNullValue']

    StartLatitude_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
    StartLatitude_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
    StartLatitude_QCNullValue= Get_RangeLimitVariables.at[6,'QCNullValue']

    StartLongitude_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
    StartLongitude_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
    StartLongitude_QCNullValue= Get_RangeLimitVariables.at[7,'QCNullValue']

    EndLatitude_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
    EndLatitude_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
    EndLatitude_QCNullValue= Get_RangeLimitVariables.at[8,'QCNullValue']

    EndLongitude_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
    EndLongitude_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
    EndLongitude_QCNullValue= Get_RangeLimitVariables.at[9,'QCNullValue']

    InOut200MileLimit_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[10,'LowerRangeLimitValue'])
    InOut200MileLimit_UpperRangeLimitValue=  int(Get_RangeLimitVariables.at[10,'UpperRangeLimitValue'])
    InOut200MileLimit_QCNullValue= Get_RangeLimitVariables.at[10,'QCNullValue']

    ## GearVariables Variables Limit Fetching
    RollerBobbbinDiameter_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[11,'LowerRangeLimitValue'])
    RollerBobbbinDiameter_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[11,'UpperRangeLimitValue'])
    RollerBobbbinDiameter_QCNullValue= Get_RangeLimitVariables.at[11,'QCNullValue']

    NumberGillnets_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[12,'LowerRangeLimitValue'])
    NumberGillnets_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[12,'UpperRangeLimitValue'])
    NumberGillnets_QCNullValue= Get_RangeLimitVariables.at[12,'QCNullValue']

    AverageGillnetLength_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[13,'LowerRangeLimitValue'])
    AverageGillnetLength_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[13,'UpperRangeLimitValue'])
    AverageGillnetLength_QCNullValue= Get_RangeLimitVariables.at[13,'QCNullValue']

    GrateBarSpacing_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[14,'LowerRangeLimitValue'])
    GrateBarSpacing_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[14,'UpperRangeLimitValue'])
    GrateBarSpacing_QCNullValue= Get_RangeLimitVariables.at[14,'QCNullValue']

    NumberPots_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[15,'LowerRangeLimitValue'])
    NumberPots_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[15,'UpperRangeLimitValue'])
    NumberPots_QCNullValue= Get_RangeLimitVariables.at[15,'QCNullValue']

    NumberPotReleasedCrab_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[16,'LowerRangeLimitValue'])
    NumberPotReleasedCrab_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[16,'UpperRangeLimitValue'])
    NumberPotReleasedCrab_QCNullValue= Get_RangeLimitVariables.at[16,'QCNullValue']

    ## CatchVariables Variables Limit Fetching

    RecordType_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[18,'LowerRangeLimitValue'])
    RecordType_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[18,'UpperRangeLimitValue'])
    RecordType_QCNullValue= Get_RangeLimitVariables.at[18,'QCNullValue']

    AverageTowSpeed_LowerRangeLimitValue= float(Get_RangeLimitVariables.at[17,'LowerRangeLimitValue'])
    AverageTowSpeed_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[17,'UpperRangeLimitValue'])
    AverageTowSpeed_QCNullValue= Get_RangeLimitVariables.at[17,'QCNullValue']

    KeptWeight_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[19,'LowerRangeLimitValue'])
    KeptWeight_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[19,'UpperRangeLimitValue'])
    KeptWeight_QCNullValue= Get_RangeLimitVariables.at[19,'QCNullValue']

    DiscardWeight_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[20,'LowerRangeLimitValue'])
    DiscardWeight_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[20,'UpperRangeLimitValue'])
    DiscardWeight_QCNullValue= Get_RangeLimitVariables.at[20,'QCNullValue']

    NumberIndividuals_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[21,'LowerRangeLimitValue'])
    NumberIndividuals_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[21,'UpperRangeLimitValue'])
    NumberIndividuals_QCNullValue= Get_RangeLimitVariables.at[21,'QCNullValue']

    NumberWindows_LowerRangeLimitValue= int(Get_RangeLimitVariables.at[22,'LowerRangeLimitValue'])
    NumberWindows_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[22,'UpperRangeLimitValue'])
    NumberWindows_QCNullValue= Get_RangeLimitVariables.at[22,'QCNullValue']

    def RunRangeValidation_BackEnd_CalenderVariables():

        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                                                       'Year', 'Day', 'Month', 'HaulDay',  'HaulMonth']]
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

        def Submit_QCFailedRange_CalVariables(FailedValidation_CalenderVariablesDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(FailedValidation_CalenderVariablesDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_CalenderVariables', sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Gen_QC_Message_Year(y):
            if y == 99999999:
                return 'Null Year - Failed'
            elif y < Year_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((y > Year_UpperRangeLimitValue) & (y < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_Day(d):
            if d == 99999999:
                return 'Null Day - Failed'
            elif d < Day_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((d > Day_UpperRangeLimitValue) & (d < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_Month(m):
            if m == 99999999:
                return 'Null Month - Failed'
            elif m < Month_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((m > Month_UpperRangeLimitValue) & (m < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_HaulDay(d):
            if d == 99999999:
                return 'Null HaulDay - Failed'
            elif d < HaulDay_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((d > HaulDay_UpperRangeLimitValue) & (d < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_HaulMonth(m):
            if m == 99999999:
                return 'Null HaulMonth - Failed'
            elif m < HaulMonth_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((m > HaulMonth_UpperRangeLimitValue) & (m < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF= (SetCatchProfileDB_DF.loc[:,
            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
             'Year','Day', 'Month', 'HaulDay', 'HaulMonth']]).replace('', 99999999)
        SetCatchProfileDB_DF['RecordType'] = (SetCatchProfileDB_DF.loc[:,['RecordType']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['Year'] = (SetCatchProfileDB_DF.loc[:,['Year']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['Day'] = (SetCatchProfileDB_DF.loc[:,['Day']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['Month'] = (SetCatchProfileDB_DF.loc[:,['Month']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['HaulDay'] = (SetCatchProfileDB_DF.loc[:,['HaulDay']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['HaulMonth'] = (SetCatchProfileDB_DF.loc[:,['HaulMonth']]).astype(int, errors='ignore')
        QCFailedRange_CalenderVariables = SetCatchProfileDB_DF[
                    (SetCatchProfileDB_DF.Year <Year_LowerRangeLimitValue)| 
                    (SetCatchProfileDB_DF.Year >Year_UpperRangeLimitValue)|

                    (SetCatchProfileDB_DF.Day <Day_LowerRangeLimitValue)| 
                    (SetCatchProfileDB_DF.Day >Day_UpperRangeLimitValue)|

                    (SetCatchProfileDB_DF.Month <Month_LowerRangeLimitValue)| 
                    (SetCatchProfileDB_DF.Month >Month_UpperRangeLimitValue)|

                    (SetCatchProfileDB_DF.HaulDay <HaulDay_LowerRangeLimitValue)| 
                    (SetCatchProfileDB_DF.HaulDay >HaulDay_UpperRangeLimitValue)|

                    (SetCatchProfileDB_DF.HaulMonth <HaulMonth_LowerRangeLimitValue)| 
                    (SetCatchProfileDB_DF.HaulMonth >HaulMonth_UpperRangeLimitValue) 
                    ]
        QCFailedRange_CalenderVariables  = QCFailedRange_CalenderVariables.reset_index(drop=True)
        QCFailedRange_CalenderVariables  = pd.DataFrame(QCFailedRange_CalenderVariables)
        QCFailedRange_CalenderVariables['YearRangeQC'] = QCFailedRange_CalenderVariables['Year'].apply(Gen_QC_Message_Year)
        QCFailedRange_CalenderVariables['DayRangeQC'] = QCFailedRange_CalenderVariables['Day'].apply(Gen_QC_Message_Day)
        QCFailedRange_CalenderVariables['MonthRangeQC'] = QCFailedRange_CalenderVariables['Month'].apply(Gen_QC_Message_Month)
        QCFailedRange_CalenderVariables['HaulDayRangeQC'] = QCFailedRange_CalenderVariables['HaulDay'].apply(Gen_QC_Message_HaulDay)
        QCFailedRange_CalenderVariables['HaulMonthRangeQC'] = QCFailedRange_CalenderVariables['HaulMonth'].apply(Gen_QC_Message_HaulMonth)
        
        QCFailedRange_CalenderVariables= (QCFailedRange_CalenderVariables.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                        'Year',
                                        'Day', 'Month', 
                                        'HaulDay',  'HaulMonth', 
                                        'YearRangeQC',
                                        'DayRangeQC', 'MonthRangeQC',
                                        'HaulDayRangeQC', 'HaulMonthRangeQC']]).replace(99999999, '')
        QCFailedRange_CalenderVariables['DeploymentIdentifier'] = 'None'
        QCFailedRange_CalenderVariables  = QCFailedRange_CalenderVariables.reset_index(drop=True)
        QCFailedRange_CalenderVariables  = pd.DataFrame(QCFailedRange_CalenderVariables)

        ## CalenderVariables Filter- Year
        Filtered_QCFailedRange_Year = QCFailedRange_CalenderVariables[(
            (QCFailedRange_CalenderVariables.YearRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CalenderVariables.YearRangeQC == 'Lower Range Failed')|
            (QCFailedRange_CalenderVariables.YearRangeQC == 'Null Year - Failed'))]
        Filtered_QCFailedRange_Year  = Filtered_QCFailedRange_Year.reset_index(drop=True)
        Filtered_QCFailedRange_Year  = pd.DataFrame(Filtered_QCFailedRange_Year)
        Filtered_QCFailedRange_Year['QC_Message'] = 'Case-Year-RangeQC'
        Filtered_QCFailedRange_Year  = Filtered_QCFailedRange_Year.reset_index(drop=True)
        Filtered_QCFailedRange_Year  = pd.DataFrame(Filtered_QCFailedRange_Year)

        ## CalenderVariables Filter- Day
        Filtered_QCFailedRange_Day = QCFailedRange_CalenderVariables[(
            (QCFailedRange_CalenderVariables.DayRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CalenderVariables.DayRangeQC == 'Lower Range Failed')|
            (QCFailedRange_CalenderVariables.DayRangeQC == 'Null Day - Failed'))]
        Filtered_QCFailedRange_Day  = Filtered_QCFailedRange_Day.reset_index(drop=True)
        Filtered_QCFailedRange_Day  = pd.DataFrame(Filtered_QCFailedRange_Day)
        Filtered_QCFailedRange_Day['QC_Message'] = 'Case-Day-RangeQC'
        Filtered_QCFailedRange_Day  = Filtered_QCFailedRange_Day.reset_index(drop=True)
        Filtered_QCFailedRange_Day  = pd.DataFrame(Filtered_QCFailedRange_Day)

        ## CalenderVariables Filter- Month
        Filtered_QCFailedRange_Month = QCFailedRange_CalenderVariables[(
            (QCFailedRange_CalenderVariables.MonthRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CalenderVariables.MonthRangeQC == 'Lower Range Failed')|
            (QCFailedRange_CalenderVariables.MonthRangeQC == 'Null Month - Failed'))]
        Filtered_QCFailedRange_Month  = Filtered_QCFailedRange_Month.reset_index(drop=True)
        Filtered_QCFailedRange_Month  = pd.DataFrame(Filtered_QCFailedRange_Month)
        Filtered_QCFailedRange_Month['QC_Message'] = 'Case-Month-RangeQC'
        Filtered_QCFailedRange_Month  = Filtered_QCFailedRange_Month.reset_index(drop=True)
        Filtered_QCFailedRange_Month  = pd.DataFrame(Filtered_QCFailedRange_Month)

        ## CalenderVariables Filter- HaulDay
        Filtered_QCFailedRange_HaulDay = QCFailedRange_CalenderVariables[(
            (QCFailedRange_CalenderVariables.HaulDayRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CalenderVariables.HaulDayRangeQC == 'Lower Range Failed')|
            (QCFailedRange_CalenderVariables.HaulDayRangeQC == 'Null HaulDay - Failed'))]
        Filtered_QCFailedRange_HaulDay  = Filtered_QCFailedRange_HaulDay.reset_index(drop=True)
        Filtered_QCFailedRange_HaulDay  = pd.DataFrame(Filtered_QCFailedRange_HaulDay)
        Filtered_QCFailedRange_HaulDay['QC_Message'] = 'Case-HaulDay-RangeQC'
        Filtered_QCFailedRange_HaulDay  = Filtered_QCFailedRange_HaulDay.reset_index(drop=True)
        Filtered_QCFailedRange_HaulDay  = pd.DataFrame(Filtered_QCFailedRange_HaulDay)

        ## CalenderVariables Filter- HaulMonth
        Filtered_QCFailedRange_HaulMonth = QCFailedRange_CalenderVariables[(
            (QCFailedRange_CalenderVariables.HaulMonthRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CalenderVariables.HaulMonthRangeQC == 'Lower Range Failed')|
            (QCFailedRange_CalenderVariables.HaulMonthRangeQC == 'Null HaulMonth - Failed'))]
        Filtered_QCFailedRange_HaulMonth  = Filtered_QCFailedRange_HaulMonth.reset_index(drop=True)
        Filtered_QCFailedRange_HaulMonth  = pd.DataFrame(Filtered_QCFailedRange_HaulMonth)
        Filtered_QCFailedRange_HaulMonth['QC_Message'] = 'Case-HaulMonth-RangeQC'
        Filtered_QCFailedRange_HaulMonth  = Filtered_QCFailedRange_HaulMonth.reset_index(drop=True)
        Filtered_QCFailedRange_HaulMonth  = pd.DataFrame(Filtered_QCFailedRange_HaulMonth)

        ## Combining By Concatenation
        QCFailedRange_CalenderVariables = pd.concat([Filtered_QCFailedRange_Year,
                                                      Filtered_QCFailedRange_Day,
                                                      Filtered_QCFailedRange_Month,
                                                      Filtered_QCFailedRange_HaulDay,
                                                      Filtered_QCFailedRange_HaulMonth])
        QCFailedRange_CalenderVariables  = QCFailedRange_CalenderVariables.reset_index(drop=True)
        QCFailedRange_CalenderVariables  = pd.DataFrame(QCFailedRange_CalenderVariables)
        Submit_QCFailedRange_CalVariables(QCFailedRange_CalenderVariables)
        Length_FailedCalenderVariables = len(QCFailedRange_CalenderVariables)
        return Length_FailedCalenderVariables

    def RunRangeValidation_BackEnd_PositionalVariables():

        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                                            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                            'PositionPrecision', 'StartLatitude', 'StartLongitude', 
                                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]
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

        def Submit_QCFailedRange_PosVar(FailedValidation_PositionalVariablesDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(FailedValidation_PositionalVariablesDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_PositionalVariables', sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Gen_QC_Message_PositionPrecision(y):
            if y == 99999999:
                return 'Null PositionPrecision - Failed'
            elif y < PositionPrecision_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif y > PositionPrecision_UpperRangeLimitValue:
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_StartLatitude(d):
            if d == 99999999:
                return 'Null StartLatitude - Failed'
            elif d < StartLatitude_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif d > StartLatitude_UpperRangeLimitValue:
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_StartLongitude(m):
            if m == 99999999:
                return 'Null StartLongitude - Failed'
            elif m < StartLongitude_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif m > StartLongitude_UpperRangeLimitValue:
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_EndLatitude(d):
            if d == 99999999:
                return 'Null EndLatitude - Failed'
            elif d < EndLatitude_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif d > EndLatitude_UpperRangeLimitValue:
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_EndLongitude(m):
            if m == 99999999:
                return 'Null EndLongitude - Failed'
            elif m < EndLongitude_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif m > EndLongitude_UpperRangeLimitValue:
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_InOut200MileLimit(n):
            if n == 99999999:
                return 'Null InOut200MileLimit - Failed'
            elif n < InOut200MileLimit_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif n > InOut200MileLimit_UpperRangeLimitValue:
                return 'Upper Range Failed'
            else:
                return 'Ok'

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'PositionPrecision', 'StartLatitude', 'StartLongitude',
                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit']]).replace('', 99999999)
        SetCatchProfileDB_DF['RecordType'] = (SetCatchProfileDB_DF.loc[:,['RecordType']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['PositionPrecision'] = (SetCatchProfileDB_DF.loc[:,['PositionPrecision']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['StartLatitude'] = (SetCatchProfileDB_DF.loc[:,['StartLatitude']]).astype(float, errors='ignore')
        SetCatchProfileDB_DF['StartLongitude'] = (SetCatchProfileDB_DF.loc[:,['StartLongitude']]).astype(float, errors='ignore')
        SetCatchProfileDB_DF['EndLatitude'] = (SetCatchProfileDB_DF.loc[:,['EndLatitude']]).astype(float, errors='ignore')
        SetCatchProfileDB_DF['EndLongitude'] = (SetCatchProfileDB_DF.loc[:,['EndLongitude']]).astype(float, errors='ignore')
        SetCatchProfileDB_DF['InOut200MileLimit'] = (SetCatchProfileDB_DF.loc[:,['InOut200MileLimit']]).astype(int, errors='ignore')

        QCFailedRange_PositionalVariables = SetCatchProfileDB_DF[
                                            (SetCatchProfileDB_DF.PositionPrecision <PositionPrecision_LowerRangeLimitValue)| 
                                            (SetCatchProfileDB_DF.PositionPrecision >PositionPrecision_UpperRangeLimitValue)|

                                            (SetCatchProfileDB_DF.StartLatitude <StartLatitude_LowerRangeLimitValue)| 
                                            (SetCatchProfileDB_DF.StartLatitude >StartLatitude_UpperRangeLimitValue)|

                                            (SetCatchProfileDB_DF.StartLongitude <StartLongitude_LowerRangeLimitValue)| 
                                            (SetCatchProfileDB_DF.StartLongitude >StartLongitude_UpperRangeLimitValue)|

                                            (SetCatchProfileDB_DF.EndLatitude <EndLatitude_LowerRangeLimitValue)| 
                                            (SetCatchProfileDB_DF.EndLatitude >EndLatitude_UpperRangeLimitValue)|

                                            (SetCatchProfileDB_DF.EndLongitude <EndLongitude_LowerRangeLimitValue)| 
                                            (SetCatchProfileDB_DF.EndLongitude >EndLongitude_UpperRangeLimitValue)|

                                            (SetCatchProfileDB_DF.InOut200MileLimit <InOut200MileLimit_LowerRangeLimitValue)| 
                                            (SetCatchProfileDB_DF.InOut200MileLimit >InOut200MileLimit_UpperRangeLimitValue)
                                            ]
        QCFailedRange_PositionalVariables  = QCFailedRange_PositionalVariables.reset_index(drop=True)
        QCFailedRange_PositionalVariables  = pd.DataFrame(QCFailedRange_PositionalVariables)

        QCFailedRange_PositionalVariables['PositionPrecisionRangeQC'] = QCFailedRange_PositionalVariables['PositionPrecision'].apply(Gen_QC_Message_PositionPrecision)
        QCFailedRange_PositionalVariables['StartLatitudeRangeQC'] = QCFailedRange_PositionalVariables['StartLatitude'].apply(Gen_QC_Message_StartLatitude)
        QCFailedRange_PositionalVariables['StartLongitudeRangeQC'] = QCFailedRange_PositionalVariables['StartLongitude'].apply(Gen_QC_Message_StartLongitude)
        QCFailedRange_PositionalVariables['EndLatitudeRangeQC'] = QCFailedRange_PositionalVariables['EndLatitude'].apply(Gen_QC_Message_EndLatitude)
        QCFailedRange_PositionalVariables['EndLongitudeRangeQC'] = QCFailedRange_PositionalVariables['EndLongitude'].apply(Gen_QC_Message_EndLongitude)
        QCFailedRange_PositionalVariables['InOut200MileLimitRangeQC'] = QCFailedRange_PositionalVariables['InOut200MileLimit'].apply(Gen_QC_Message_InOut200MileLimit)
        QCFailedRange_PositionalVariables= (QCFailedRange_PositionalVariables.loc[:,[
                                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                            'PositionPrecision', 'StartLatitude', 'StartLongitude',
                                            'EndLatitude', 'EndLongitude', 'InOut200MileLimit',
                                            'PositionPrecisionRangeQC', 'StartLatitudeRangeQC',
                                            'StartLongitudeRangeQC', 'EndLatitudeRangeQC',
                                            'EndLongitudeRangeQC', 'InOut200MileLimitRangeQC']]).replace(99999999, '')
        QCFailedRange_PositionalVariables['DeploymentIdentifier'] = 'None'
        QCFailedRange_PositionalVariables  = QCFailedRange_PositionalVariables.reset_index(drop=True)
        QCFailedRange_PositionalVariables  = pd.DataFrame(QCFailedRange_PositionalVariables)

        ## PositionalVariables Filter- PositionPrecision
        Filtered_QCFailedRange_PP = QCFailedRange_PositionalVariables[(
            (QCFailedRange_PositionalVariables.PositionPrecisionRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_PositionalVariables.PositionPrecisionRangeQC == 'Lower Range Failed')|
            (QCFailedRange_PositionalVariables.PositionPrecisionRangeQC == 'Null PositionPrecision - Failed'))]
        Filtered_QCFailedRange_PP  = Filtered_QCFailedRange_PP.reset_index(drop=True)
        Filtered_QCFailedRange_PP  = pd.DataFrame(Filtered_QCFailedRange_PP)
        Filtered_QCFailedRange_PP['QC_Message'] = 'Case-PP-RangeQC'
        Filtered_QCFailedRange_PP  = Filtered_QCFailedRange_PP.reset_index(drop=True)
        Filtered_QCFailedRange_PP  = pd.DataFrame(Filtered_QCFailedRange_PP)

        ## PositionalVariables Filter- StartLatitude
        Filtered_QCFailedRange_SLat = QCFailedRange_PositionalVariables[(
            (QCFailedRange_PositionalVariables.StartLatitudeRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_PositionalVariables.StartLatitudeRangeQC == 'Lower Range Failed')|
            (QCFailedRange_PositionalVariables.StartLatitudeRangeQC == 'Null StartLatitude - Failed'))]
        Filtered_QCFailedRange_SLat  = Filtered_QCFailedRange_SLat.reset_index(drop=True)
        Filtered_QCFailedRange_SLat  = pd.DataFrame(Filtered_QCFailedRange_SLat)
        Filtered_QCFailedRange_SLat['QC_Message'] = 'Case-SLat-RangeQC'
        Filtered_QCFailedRange_SLat  = Filtered_QCFailedRange_SLat.reset_index(drop=True)
        Filtered_QCFailedRange_SLat  = pd.DataFrame(Filtered_QCFailedRange_SLat)

        ## PositionalVariables Filter- StartLongitude
        Filtered_QCFailedRange_SLon = QCFailedRange_PositionalVariables[(
            (QCFailedRange_PositionalVariables.StartLongitudeRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_PositionalVariables.StartLongitudeRangeQC == 'Lower Range Failed')|
            (QCFailedRange_PositionalVariables.StartLongitudeRangeQC == 'Null StartLongitude - Failed'))]
        Filtered_QCFailedRange_SLon  = Filtered_QCFailedRange_SLon.reset_index(drop=True)
        Filtered_QCFailedRange_SLon  = pd.DataFrame(Filtered_QCFailedRange_SLon)
        Filtered_QCFailedRange_SLon['QC_Message'] = 'Case-SLon-RangeQC'
        Filtered_QCFailedRange_SLon  = Filtered_QCFailedRange_SLon.reset_index(drop=True)
        Filtered_QCFailedRange_SLon  = pd.DataFrame(Filtered_QCFailedRange_SLon)

        ## PositionalVariables Filter- EndLatitude
        Filtered_QCFailedRange_ELat = QCFailedRange_PositionalVariables[(
            (QCFailedRange_PositionalVariables.EndLatitudeRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_PositionalVariables.EndLatitudeRangeQC == 'Lower Range Failed')|
            (QCFailedRange_PositionalVariables.EndLatitudeRangeQC == 'Null EndLatitude - Failed'))]
        Filtered_QCFailedRange_ELat  = Filtered_QCFailedRange_ELat.reset_index(drop=True)
        Filtered_QCFailedRange_ELat  = pd.DataFrame(Filtered_QCFailedRange_ELat)
        Filtered_QCFailedRange_ELat['QC_Message'] = 'Case-ELat-RangeQC'
        Filtered_QCFailedRange_ELat  = Filtered_QCFailedRange_ELat.reset_index(drop=True)
        Filtered_QCFailedRange_ELat  = pd.DataFrame(Filtered_QCFailedRange_ELat)

        ## PositionalVariables Filter- EndLongitude
        Filtered_QCFailedRange_ELon = QCFailedRange_PositionalVariables[(
            (QCFailedRange_PositionalVariables.EndLongitudeRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_PositionalVariables.EndLongitudeRangeQC == 'Lower Range Failed')|
            (QCFailedRange_PositionalVariables.EndLongitudeRangeQC == 'Null EndLongitude - Failed'))]
        Filtered_QCFailedRange_ELon  = Filtered_QCFailedRange_ELon.reset_index(drop=True)
        Filtered_QCFailedRange_ELon  = pd.DataFrame(Filtered_QCFailedRange_ELon)
        Filtered_QCFailedRange_ELon['QC_Message'] = 'Case-ELon-RangeQC'
        Filtered_QCFailedRange_ELon  = Filtered_QCFailedRange_ELon.reset_index(drop=True)
        Filtered_QCFailedRange_ELon  = pd.DataFrame(Filtered_QCFailedRange_ELon)

        ## PositionalVariables Filter- InOut200MileLimit
        Filtered_QCFailedRange_IO200ML = QCFailedRange_PositionalVariables[(
            (QCFailedRange_PositionalVariables.InOut200MileLimitRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_PositionalVariables.InOut200MileLimitRangeQC == 'Lower Range Failed')|
            (QCFailedRange_PositionalVariables.InOut200MileLimitRangeQC == 'Null InOut200MileLimit - Failed'))]
        Filtered_QCFailedRange_IO200ML  = Filtered_QCFailedRange_IO200ML.reset_index(drop=True)
        Filtered_QCFailedRange_IO200ML  = pd.DataFrame(Filtered_QCFailedRange_IO200ML)
        Filtered_QCFailedRange_IO200ML['QC_Message'] = 'Case-IO200ML-RangeQC'
        Filtered_QCFailedRange_IO200ML  = Filtered_QCFailedRange_IO200ML.reset_index(drop=True)
        Filtered_QCFailedRange_IO200ML  = pd.DataFrame(Filtered_QCFailedRange_IO200ML)

        ## Combining By Concatenation
        QCFailedRange_PositionalVariables = pd.concat([Filtered_QCFailedRange_PP,
                                                      Filtered_QCFailedRange_SLat,
                                                      Filtered_QCFailedRange_SLon,
                                                      Filtered_QCFailedRange_ELat,
                                                      Filtered_QCFailedRange_ELon,
                                                      Filtered_QCFailedRange_IO200ML])
        QCFailedRange_PositionalVariables  = QCFailedRange_PositionalVariables.reset_index(drop=True)
        QCFailedRange_PositionalVariables  = pd.DataFrame(QCFailedRange_PositionalVariables)
        Submit_QCFailedRange_PosVar(QCFailedRange_PositionalVariables)
        Length_FailedPositionalVariables = len(QCFailedRange_PositionalVariables)
        return Length_FailedPositionalVariables
        
    def RunRangeValidation_BackEnd_GearVariables():
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                                            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                            'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                                            'GrateBarSpacing', 'NumberPots', 'NumberPotReleasedCrab']]
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

        def Submit_QCFailedRange_GearVariables(FailedValidation_GearVariablesDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(FailedValidation_GearVariablesDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_GearVariables', sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Gen_QC_Message_RollerBobbbinDiameter(y):
            if y == 99999999:
                return 'Blank'
            elif y < RollerBobbbinDiameter_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((y > RollerBobbbinDiameter_UpperRangeLimitValue) & (y < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_NumberGillnets(d):
            if d == 99999999:
                return 'Blank'
            elif d < NumberGillnets_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((d > NumberGillnets_UpperRangeLimitValue) & (d < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_AverageGillnetLength(m):
            if m == 99999999:
                return 'Blank'
            elif m < AverageGillnetLength_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((m > AverageGillnetLength_UpperRangeLimitValue) & (m < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_GrateBarSpacing(d):
            if d == 99999999:
                return 'Blank'
            elif d < GrateBarSpacing_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((d > GrateBarSpacing_UpperRangeLimitValue) & (d < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_NumberPots(m):
            if m == 99999999:
                return 'Blank'
            elif m < NumberPots_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((m > NumberPots_UpperRangeLimitValue) & (m < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_NumberPotReleasedCrab(n):
            if n == 99999999:
                return 'Blank'
            elif n < NumberPotReleasedCrab_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((n > NumberPotReleasedCrab_UpperRangeLimitValue) & (n < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                            'GrateBarSpacing', 'NumberPots', 'NumberPotReleasedCrab']]).replace('', 99999999)
        SetCatchProfileDB_DF['RecordType'] = (SetCatchProfileDB_DF.loc[:,['RecordType']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['RollerBobbbinDiameter'] = (SetCatchProfileDB_DF.loc[:,['RollerBobbbinDiameter']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['NumberGillnets'] = (SetCatchProfileDB_DF.loc[:,['NumberGillnets']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['AverageGillnetLength'] = (SetCatchProfileDB_DF.loc[:,['AverageGillnetLength']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['GrateBarSpacing'] = (SetCatchProfileDB_DF.loc[:,['GrateBarSpacing']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['NumberPots'] = (SetCatchProfileDB_DF.loc[:,['NumberPots']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['NumberPotReleasedCrab'] = (SetCatchProfileDB_DF.loc[:,['NumberPotReleasedCrab']]).astype(int, errors='ignore')

        QCFailedRange_GearVariables = SetCatchProfileDB_DF[
                                            (SetCatchProfileDB_DF.RollerBobbbinDiameter < RollerBobbbinDiameter_LowerRangeLimitValue)| 
                                            ((SetCatchProfileDB_DF.RollerBobbbinDiameter > RollerBobbbinDiameter_UpperRangeLimitValue) &
                                            (SetCatchProfileDB_DF.RollerBobbbinDiameter <99999999))|
                                            
                                            (SetCatchProfileDB_DF.NumberGillnets < NumberGillnets_LowerRangeLimitValue)| 
                                            ((SetCatchProfileDB_DF.NumberGillnets > NumberGillnets_UpperRangeLimitValue) &
                                            (SetCatchProfileDB_DF.NumberGillnets < 99999999))|

                                            (SetCatchProfileDB_DF.AverageGillnetLength < AverageGillnetLength_LowerRangeLimitValue)| 
                                            ((SetCatchProfileDB_DF.AverageGillnetLength > AverageGillnetLength_UpperRangeLimitValue) &
                                            (SetCatchProfileDB_DF.AverageGillnetLength < 99999999))|
                                            
                                            ((SetCatchProfileDB_DF.GrateBarSpacing < GrateBarSpacing_LowerRangeLimitValue)| 
                                            (SetCatchProfileDB_DF.GrateBarSpacing > GrateBarSpacing_UpperRangeLimitValue) &
                                            (SetCatchProfileDB_DF.GrateBarSpacing < 99999999))|

                                            (SetCatchProfileDB_DF.NumberPots < NumberPots_LowerRangeLimitValue)| 
                                            ((SetCatchProfileDB_DF.NumberPots > NumberPots_UpperRangeLimitValue) &
                                            (SetCatchProfileDB_DF.NumberPots < 99999999))|

                                            (SetCatchProfileDB_DF.NumberPotReleasedCrab < NumberPotReleasedCrab_LowerRangeLimitValue)| 
                                            ((SetCatchProfileDB_DF.NumberPotReleasedCrab > NumberPotReleasedCrab_UpperRangeLimitValue) &
                                            (SetCatchProfileDB_DF.NumberPotReleasedCrab < 99999999))]
        
        QCFailedRange_GearVariables  = QCFailedRange_GearVariables.reset_index(drop=True)
        QCFailedRange_GearVariables  = pd.DataFrame(QCFailedRange_GearVariables)

        QCFailedRange_GearVariables['RollerBobbbinDiameterRangeQC'] = QCFailedRange_GearVariables['RollerBobbbinDiameter'].apply(Gen_QC_Message_RollerBobbbinDiameter)
        QCFailedRange_GearVariables['NumberGillnetsRangeQC'] = QCFailedRange_GearVariables['NumberGillnets'].apply(Gen_QC_Message_NumberGillnets)
        QCFailedRange_GearVariables['AverageGillnetLengthRangeQC'] = QCFailedRange_GearVariables['AverageGillnetLength'].apply(Gen_QC_Message_AverageGillnetLength)
        QCFailedRange_GearVariables['GrateBarSpacingRangeQC'] = QCFailedRange_GearVariables['GrateBarSpacing'].apply(Gen_QC_Message_GrateBarSpacing)
        QCFailedRange_GearVariables['NumberPotsRangeQC'] = QCFailedRange_GearVariables['NumberPots'].apply(Gen_QC_Message_NumberPots)
        QCFailedRange_GearVariables['NumberPotReleasedCrabRangeQC'] = QCFailedRange_GearVariables['NumberPotReleasedCrab'].apply(Gen_QC_Message_NumberPotReleasedCrab)
        QCFailedRange_GearVariables= (QCFailedRange_GearVariables.loc[:,[
                                    'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                    'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength',
                                    'GrateBarSpacing', 'NumberPots', 'NumberPotReleasedCrab',
                                    'RollerBobbbinDiameterRangeQC', 'NumberGillnetsRangeQC',
                                    'AverageGillnetLengthRangeQC', 'GrateBarSpacingRangeQC',
                                    'NumberPotsRangeQC', 'NumberPotReleasedCrabRangeQC']]).replace(99999999, '')
        QCFailedRange_GearVariables['DeploymentIdentifier'] = 'None'
        QCFailedRange_GearVariables  = QCFailedRange_GearVariables.reset_index(drop=True)
        QCFailedRange_GearVariables  = pd.DataFrame(QCFailedRange_GearVariables)

         ## GearVariables Filter- RollerBobbbinDiameter
        Filtered_QCFailedRange_RBD = QCFailedRange_GearVariables[(
            (QCFailedRange_GearVariables.RollerBobbbinDiameterRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_GearVariables.RollerBobbbinDiameterRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_RBD  = Filtered_QCFailedRange_RBD.reset_index(drop=True)
        Filtered_QCFailedRange_RBD  = pd.DataFrame(Filtered_QCFailedRange_RBD)
        Filtered_QCFailedRange_RBD['QC_Message'] = 'Case-RBD-RangeQC'
        Filtered_QCFailedRange_RBD  = Filtered_QCFailedRange_RBD.reset_index(drop=True)
        Filtered_QCFailedRange_RBD  = pd.DataFrame(Filtered_QCFailedRange_RBD)

        ## GearVariables Filter- NumberGillnets
        Filtered_QCFailedRange_NG = QCFailedRange_GearVariables[(
            (QCFailedRange_GearVariables.NumberGillnetsRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_GearVariables.NumberGillnetsRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_NG  = Filtered_QCFailedRange_NG.reset_index(drop=True)
        Filtered_QCFailedRange_NG  = pd.DataFrame(Filtered_QCFailedRange_NG)
        Filtered_QCFailedRange_NG['QC_Message'] = 'Case-NG-RangeQC'
        Filtered_QCFailedRange_NG  = Filtered_QCFailedRange_NG.reset_index(drop=True)
        Filtered_QCFailedRange_NG  = pd.DataFrame(Filtered_QCFailedRange_NG)

        ## GearVariables Filter- AverageGillnetLength
        Filtered_QCFailedRange_AGL = QCFailedRange_GearVariables[(
            (QCFailedRange_GearVariables.AverageGillnetLengthRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_GearVariables.AverageGillnetLengthRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_AGL  = Filtered_QCFailedRange_AGL.reset_index(drop=True)
        Filtered_QCFailedRange_AGL  = pd.DataFrame(Filtered_QCFailedRange_AGL)
        Filtered_QCFailedRange_AGL['QC_Message'] = 'Case-AGL-RangeQC'
        Filtered_QCFailedRange_AGL  = Filtered_QCFailedRange_AGL.reset_index(drop=True)
        Filtered_QCFailedRange_AGL  = pd.DataFrame(Filtered_QCFailedRange_AGL)

        ## GearVariables Filter- GrateBarSpacing
        Filtered_QCFailedRange_GBS = QCFailedRange_GearVariables[(
            (QCFailedRange_GearVariables.GrateBarSpacingRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_GearVariables.GrateBarSpacingRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_GBS  = Filtered_QCFailedRange_GBS.reset_index(drop=True)
        Filtered_QCFailedRange_GBS  = pd.DataFrame(Filtered_QCFailedRange_GBS)
        Filtered_QCFailedRange_GBS['QC_Message'] = 'Case-GBS-RangeQC'
        Filtered_QCFailedRange_GBS  = Filtered_QCFailedRange_GBS.reset_index(drop=True)
        Filtered_QCFailedRange_GBS  = pd.DataFrame(Filtered_QCFailedRange_GBS)

        ## GearVariables Filter- NumberPots
        Filtered_QCFailedRange_NP = QCFailedRange_GearVariables[(
            (QCFailedRange_GearVariables.NumberPotsRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_GearVariables.NumberPotsRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_NP  = Filtered_QCFailedRange_NP.reset_index(drop=True)
        Filtered_QCFailedRange_NP  = pd.DataFrame(Filtered_QCFailedRange_NP)
        Filtered_QCFailedRange_NP['QC_Message'] = 'Case-NP-RangeQC'
        Filtered_QCFailedRange_NP  = Filtered_QCFailedRange_NP.reset_index(drop=True)
        Filtered_QCFailedRange_NP  = pd.DataFrame(Filtered_QCFailedRange_NP)

         ## GearVariables Filter- NumberPotReleasedCrab
        Filtered_QCFailedRange_NPRC = QCFailedRange_GearVariables[(
            (QCFailedRange_GearVariables.NumberPotReleasedCrabRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_GearVariables.NumberPotReleasedCrabRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_NPRC  = Filtered_QCFailedRange_NPRC.reset_index(drop=True)
        Filtered_QCFailedRange_NPRC  = pd.DataFrame(Filtered_QCFailedRange_NPRC)
        Filtered_QCFailedRange_NPRC['QC_Message'] = 'Case-NPRC-RangeQC'
        Filtered_QCFailedRange_NPRC  = Filtered_QCFailedRange_NPRC.reset_index(drop=True)
        Filtered_QCFailedRange_NPRC  = pd.DataFrame(Filtered_QCFailedRange_NPRC)
        ## Combining By Concatenation
        QCFailedRange_GearVariables = pd.concat([Filtered_QCFailedRange_RBD,
                                                Filtered_QCFailedRange_NG,
                                                Filtered_QCFailedRange_AGL,
                                                Filtered_QCFailedRange_GBS,
                                                Filtered_QCFailedRange_NP,
                                                Filtered_QCFailedRange_NPRC])
        QCFailedRange_GearVariables  = QCFailedRange_GearVariables.reset_index(drop=True)
        QCFailedRange_GearVariables  = pd.DataFrame(QCFailedRange_GearVariables)
        Submit_QCFailedRange_GearVariables(QCFailedRange_GearVariables)
        Length_FailedGearVariables = len(QCFailedRange_GearVariables)
        return Length_FailedGearVariables

    def RunRangeValidation_BackEnd_CatchVariables():
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                            'RecordType', 'AverageTowSpeed',  
                                            'KeptWeight', 'DiscardWeight', 
                                            'NumberIndividuals', 'NumberWindows']]
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

        def Submit_QCFailedRange_CatchVariables(FailedValidation_CatchVariablesDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(FailedValidation_CatchVariablesDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_CatchVariables', sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Gen_QC_Message_RecordType(d):
            if d == 99999999:
                return 'Null RecordType - Failed'
            elif d < RecordType_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((d > RecordType_UpperRangeLimitValue) & (d < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_AverageTowSpeed(y):
            if y == 99999999:
                return 'Blank'
            elif y < AverageTowSpeed_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((y > AverageTowSpeed_UpperRangeLimitValue) & (y < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_KeptWeight(d):
            if d == 99999999:
                return 'Blank'
            elif d < KeptWeight_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((d > KeptWeight_UpperRangeLimitValue) & (d < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_DiscardWeight(m):
            if m == 99999999:
                return 'Blank'
            elif m < DiscardWeight_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((m > DiscardWeight_UpperRangeLimitValue) & (m < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_NumberIndividuals(n):
            if n == 99999999:
                return 'Blank'
            elif n < NumberIndividuals_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((n > NumberIndividuals_UpperRangeLimitValue) & (n < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        def Gen_QC_Message_NumberWindows(n):
            if n == 99999999:
                return 'Blank'
            elif n < NumberWindows_LowerRangeLimitValue:
                return 'Lower Range Failed'
            elif ((n > NumberWindows_UpperRangeLimitValue) & (n < 99999999)):
                return 'Upper Range Failed'
            else:
                return 'Ok'

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'RecordType', 'AverageTowSpeed',  
                            'KeptWeight', 'DiscardWeight', 
                            'NumberIndividuals', 'NumberWindows']]).replace('', 99999999)
        SetCatchProfileDB_DF['RecordType'] = (SetCatchProfileDB_DF.loc[:,['RecordType']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['AverageTowSpeed'] = (SetCatchProfileDB_DF.loc[:,['AverageTowSpeed']]).astype(float, errors='ignore')
        SetCatchProfileDB_DF['KeptWeight'] = (SetCatchProfileDB_DF.loc[:,['KeptWeight']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['DiscardWeight'] = (SetCatchProfileDB_DF.loc[:,['DiscardWeight']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['NumberIndividuals'] = (SetCatchProfileDB_DF.loc[:,['NumberIndividuals']]).astype(int, errors='ignore')
        SetCatchProfileDB_DF['NumberWindows'] = (SetCatchProfileDB_DF.loc[:,['NumberWindows']]).astype(int, errors='ignore')
        QCFailedRange_CatchVariables = SetCatchProfileDB_DF[
                                    (SetCatchProfileDB_DF.AverageTowSpeed <AverageTowSpeed_LowerRangeLimitValue)| 
                                    (SetCatchProfileDB_DF.AverageTowSpeed >AverageTowSpeed_UpperRangeLimitValue)&
                                    (SetCatchProfileDB_DF.AverageTowSpeed < 99999999)|

                                    (SetCatchProfileDB_DF.RecordType <RecordType_LowerRangeLimitValue)| 
                                    (SetCatchProfileDB_DF.RecordType >RecordType_UpperRangeLimitValue)|

                                    (SetCatchProfileDB_DF.KeptWeight <KeptWeight_LowerRangeLimitValue)| 
                                    ((SetCatchProfileDB_DF.KeptWeight >KeptWeight_UpperRangeLimitValue) &
                                    (SetCatchProfileDB_DF.KeptWeight < 99999999))|

                                    (SetCatchProfileDB_DF.DiscardWeight <DiscardWeight_LowerRangeLimitValue)| 
                                    ((SetCatchProfileDB_DF.DiscardWeight >DiscardWeight_UpperRangeLimitValue) &
                                    (SetCatchProfileDB_DF.DiscardWeight < 99999999))|

                                    (SetCatchProfileDB_DF.NumberIndividuals <NumberIndividuals_LowerRangeLimitValue)| 
                                    ((SetCatchProfileDB_DF.NumberIndividuals >NumberIndividuals_UpperRangeLimitValue) &
                                    (SetCatchProfileDB_DF.NumberIndividuals <99999999))|

                                    (SetCatchProfileDB_DF.NumberWindows <NumberWindows_LowerRangeLimitValue)| 
                                    ((SetCatchProfileDB_DF.NumberWindows >NumberWindows_UpperRangeLimitValue) &
                                    (SetCatchProfileDB_DF.NumberWindows <99999999))
                                    ]
        QCFailedRange_CatchVariables  = QCFailedRange_CatchVariables.reset_index(drop=True)
        QCFailedRange_CatchVariables  = pd.DataFrame(QCFailedRange_CatchVariables)

        QCFailedRange_CatchVariables['AverageTowSpeedRangeQC'] = QCFailedRange_CatchVariables['AverageTowSpeed'].apply(Gen_QC_Message_AverageTowSpeed)
        QCFailedRange_CatchVariables['RecordTypeRangeQC'] = QCFailedRange_CatchVariables['RecordType'].apply(Gen_QC_Message_RecordType)
        QCFailedRange_CatchVariables['KeptWeightRangeQC'] = QCFailedRange_CatchVariables['KeptWeight'].apply(Gen_QC_Message_KeptWeight)
        QCFailedRange_CatchVariables['DiscardWeightRangeQC'] = QCFailedRange_CatchVariables['DiscardWeight'].apply(Gen_QC_Message_DiscardWeight)
        QCFailedRange_CatchVariables['NumberIndividualsRangeQC'] = QCFailedRange_CatchVariables['NumberIndividuals'].apply(Gen_QC_Message_NumberIndividuals)
        QCFailedRange_CatchVariables['NumberWindowsRangeQC'] = QCFailedRange_CatchVariables['NumberWindows'].apply(Gen_QC_Message_NumberWindows)
        
        QCFailedRange_CatchVariables= (QCFailedRange_CatchVariables.loc[:,[
                                    'DataBase_ID','RecordIdentifier','DeploymentUID',
                                    'RecordType', 'AverageTowSpeed', 'KeptWeight', 
                                    'DiscardWeight', 'NumberIndividuals', 'NumberWindows',
                                    'RecordTypeRangeQC','AverageTowSpeedRangeQC', 'KeptWeightRangeQC',
                                    'DiscardWeightRangeQC', 'NumberIndividualsRangeQC', 'NumberWindowsRangeQC']]).replace(99999999, '')
        
        QCFailedRange_CatchVariables['DeploymentIdentifier'] = 'None' 
        QCFailedRange_CatchVariables  = QCFailedRange_CatchVariables.reset_index(drop=True)
        QCFailedRange_CatchVariables  = pd.DataFrame(QCFailedRange_CatchVariables)

        ## GearVariables Filter- AverageTowSpeed
        Filtered_QCFailedRange_ATS = QCFailedRange_CatchVariables[(
            (QCFailedRange_CatchVariables.AverageTowSpeedRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CatchVariables.AverageTowSpeedRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_ATS  = Filtered_QCFailedRange_ATS.reset_index(drop=True)
        Filtered_QCFailedRange_ATS  = pd.DataFrame(Filtered_QCFailedRange_ATS)
        Filtered_QCFailedRange_ATS['QC_Message'] = 'Case-ATS-RangeQC'
        Filtered_QCFailedRange_ATS  = Filtered_QCFailedRange_ATS.reset_index(drop=True)
        Filtered_QCFailedRange_ATS  = pd.DataFrame(Filtered_QCFailedRange_ATS)

        ## GearVariables Filter- RecordType
        Filtered_QCFailedRange_RT = QCFailedRange_CatchVariables[(
            (QCFailedRange_CatchVariables.RecordTypeRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CatchVariables.RecordTypeRangeQC == 'Lower Range Failed')|
            (QCFailedRange_CatchVariables.RecordTypeRangeQC == 'Null RecordType - Failed')
            )]
        Filtered_QCFailedRange_RT  = Filtered_QCFailedRange_RT.reset_index(drop=True)
        Filtered_QCFailedRange_RT  = pd.DataFrame(Filtered_QCFailedRange_RT)
        Filtered_QCFailedRange_RT['QC_Message'] = 'Case-RT-RangeQC'
        Filtered_QCFailedRange_RT  = Filtered_QCFailedRange_RT.reset_index(drop=True)
        Filtered_QCFailedRange_RT  = pd.DataFrame(Filtered_QCFailedRange_RT)

        ## GearVariables Filter- KeptWeight
        Filtered_QCFailedRange_KW = QCFailedRange_CatchVariables[(
            (QCFailedRange_CatchVariables.KeptWeightRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CatchVariables.KeptWeightRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_KW  = Filtered_QCFailedRange_KW.reset_index(drop=True)
        Filtered_QCFailedRange_KW  = pd.DataFrame(Filtered_QCFailedRange_KW)
        Filtered_QCFailedRange_KW['QC_Message'] = 'Case-KW-RangeQC'
        Filtered_QCFailedRange_KW  = Filtered_QCFailedRange_KW.reset_index(drop=True)
        Filtered_QCFailedRange_KW  = pd.DataFrame(Filtered_QCFailedRange_KW)

        ## GearVariables Filter- DiscardWeight
        Filtered_QCFailedRange_DW = QCFailedRange_CatchVariables[(
            (QCFailedRange_CatchVariables.DiscardWeightRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CatchVariables.DiscardWeightRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_DW  = Filtered_QCFailedRange_DW.reset_index(drop=True)
        Filtered_QCFailedRange_DW  = pd.DataFrame(Filtered_QCFailedRange_DW)
        Filtered_QCFailedRange_DW['QC_Message'] = 'Case-DW-RangeQC'
        Filtered_QCFailedRange_DW  = Filtered_QCFailedRange_DW.reset_index(drop=True)
        Filtered_QCFailedRange_DW  = pd.DataFrame(Filtered_QCFailedRange_DW)

        ## GearVariables Filter- NumberIndividuals
        Filtered_QCFailedRange_NI = QCFailedRange_CatchVariables[(
            (QCFailedRange_CatchVariables.NumberIndividualsRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CatchVariables.NumberIndividualsRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_NI  = Filtered_QCFailedRange_NI.reset_index(drop=True)
        Filtered_QCFailedRange_NI  = pd.DataFrame(Filtered_QCFailedRange_NI)
        Filtered_QCFailedRange_NI['QC_Message'] = 'Case-NI-RangeQC'
        Filtered_QCFailedRange_NI  = Filtered_QCFailedRange_NI.reset_index(drop=True)
        Filtered_QCFailedRange_NI  = pd.DataFrame(Filtered_QCFailedRange_NI)

         ## GearVariables Filter- NumberWindows
        Filtered_QCFailedRange_NW = QCFailedRange_CatchVariables[(
            (QCFailedRange_CatchVariables.NumberWindowsRangeQC == 'Upper Range Failed')| 
            (QCFailedRange_CatchVariables.NumberWindowsRangeQC == 'Lower Range Failed'))]
        Filtered_QCFailedRange_NW  = Filtered_QCFailedRange_NW.reset_index(drop=True)
        Filtered_QCFailedRange_NW  = pd.DataFrame(Filtered_QCFailedRange_NW)
        Filtered_QCFailedRange_NW['QC_Message'] = 'Case-NW-RangeQC'
        Filtered_QCFailedRange_NW  = Filtered_QCFailedRange_NW.reset_index(drop=True)
        Filtered_QCFailedRange_NW  = pd.DataFrame(Filtered_QCFailedRange_NW)

        ## Combining By Concatenation
        QCFailedRange_CatchVariables = pd.concat([Filtered_QCFailedRange_ATS,
                                                  Filtered_QCFailedRange_RT,
                                                  Filtered_QCFailedRange_KW,
                                                  Filtered_QCFailedRange_DW,
                                                  Filtered_QCFailedRange_NI,
                                                  Filtered_QCFailedRange_NW])
        QCFailedRange_CatchVariables  = QCFailedRange_CatchVariables.reset_index(drop=True)
        QCFailedRange_CatchVariables  = pd.DataFrame(QCFailedRange_CatchVariables)
        Submit_QCFailedRange_CatchVariables(QCFailedRange_CatchVariables)
        Length_FailedCatchVariables = len(QCFailedRange_CatchVariables)
        return Length_FailedCatchVariables

    FailedRangeValidation_CalenderVariables = RunRangeValidation_BackEnd_CalenderVariables()
    FailedRangeValidation_PositionalVariables = RunRangeValidation_BackEnd_PositionalVariables()
    FailedRangeValidation_GearVariables = RunRangeValidation_BackEnd_GearVariables()
    FailedRangeValidation_CatchVariables = RunRangeValidation_BackEnd_CatchVariables()
    TotalFailedQC_RangeValidation = (int(FailedRangeValidation_CalenderVariables) + \
                                    int(FailedRangeValidation_PositionalVariables) + \
                                    int(FailedRangeValidation_GearVariables) + \
                                    int(FailedRangeValidation_CatchVariables) )
    return TotalFailedQC_RangeValidation