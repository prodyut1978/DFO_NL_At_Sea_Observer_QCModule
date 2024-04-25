import sqlite3
#backend

DB_SetCatch_Validation_Consistency = ("./BackEnd/Sqlite3_DB/QC_Check_ConsistencyValidate_DB/DFO_NL_ASOP_SetCatch_ConsistencyValidation.db")

def get_DB_SetCatch_Validation_Consistency():
    conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
    return conn

def DFO_NL_ASOP_ConsistencyValidation_DB():
    con= sqlite3.connect(DB_SetCatch_Validation_Consistency)
    cur=con.cursor()
    
    ## For RunConsistencyFailed_Year_Country_Quota
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_Year_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber, \
                SetNumber, VesselSideNumber, RecordType, Year, \
                Country, Quota, QC_Year)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_Country_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber, \
                SetNumber, VesselSideNumber, RecordType, Year, \
                Country, Quota, QC_Country)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_Quota_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber,\
                SetNumber, VesselSideNumber, RecordType, Year,  \
                Country, Quota, QC_Quota)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_YCQ_FailConsis_SummaryDF (\
                VariableName, QCFailCount)")
    
    ## For RunConsistencyFailed_VesselVariables
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_VSN_STN_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber, \
                SetNumber, Year, RecordType, Country, Quota, \
                SubTripNumber, VesselSideNumber, VesselClass, QC_Message, QC_CaseType)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_VCLS_VSN_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber,\
                SetNumber, Year, RecordType, Country, Quota,\
                VesselClass, VesselSideNumber, QC_Message, QC_CaseType)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_VL_VSN_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber, \
                SetNumber, Year, RecordType, Country, Quota,\
                VesselLength, VesselSideNumber, QC_Message, QC_CaseType)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_VHP_VSN_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber,\
                SetNumber, Year, RecordType, Country, Quota,\
                VesselHorsepower, VesselSideNumber, QC_Message, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_Vessel_FailConsis_SummaryDF (\
                VariableName, QCFailCount)")
    
    ## For RunConsistencyFailed CalenderVariables 
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_DM_HDHM_FailConsistency_DF (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode, ObserverNumber, DeploymentNumber, SetNumber,\
                RecordType, Year, Day, Month,\
                HaulDay,  HaulMonth, StartTime, Duration, QC_Message)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_Calender_FailConsis_SummaryDF (\
                VariableName, QCFailCount)")
    
    ## For RunConsistencyFailed MobileGear 
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_MobileGear_FailConsistency_DF (\
            DataBase_ID, RecordIdentifier, DeploymentUID,\
            ASOCCode, ObserverNumber, DeploymentNumber, \
            SetNumber, VesselSideNumber, RecordType, GearType, Country,\
            Year, Day, Month,\
            StartTime,  Duration, QC_Message)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_MobileGear_FailConsis_SummaryDF (\
                VariableName, QCFailCount)")
    
    con.commit()
    cur.close()
    con.close()

