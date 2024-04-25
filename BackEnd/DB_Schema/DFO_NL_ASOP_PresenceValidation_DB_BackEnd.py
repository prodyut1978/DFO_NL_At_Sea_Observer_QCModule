import sqlite3
#backend

DB_SetCatch_Validation_Presence = ("./BackEnd/Sqlite3_DB/QC_Check_PresenceConsistency_DB/DFO_NL_ASOP_SetCatch_PresenceValidation.db")

def get_DB_SetCatch_Validation_Presence():
    conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
    return conn

def DFO_NL_ASOP_PresenceValidation_DB():
    con= sqlite3.connect(DB_SetCatch_Validation_Presence)
    cur=con.cursor()
    # Presence Must
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_MustVariables (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                ASOCCode,ObserverNumber, Year,\
                DeploymentNumber, SubTripNumber, SetNumber,\
                Country, Quota, SetType,\
                VesselSideNumber,VesselClass,Day, \
                Month, HaulDay,  HaulMonth,\
                StartTime, Duration, PositionPrecision,\
                StartLatitude, StartLongitude, EndLatitude,\
                EndLongitude, InOut200MileLimit,  NAFODivision,\
                GearType,RecordType, DetailedCatchSpeciesCompCode,\
                DirectedSpecies, AverageDepth,\
                DataSource)")
    # Presence Conditional
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_ConditionalVariables (\
                DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, AverageTowSpeed, CodendMeshSize,\
                MeshSizeMG, NumberGillnets, AverageGillnetLength, NumberHooks, NumberWindows, NumberPots,\
                QCAverageTowSpeed, QCCodendMeshSize, QCMeshSizeMG,\
                QCNumberGillnets, QCAverageGillnetLength, QCNumberHooks, QCNumberWindows, QCNumberPots)")    

    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_AverageTowSpeed (\
                DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, AverageTowSpeed, QCAverageTowSpeed, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_CodendMeshSize (\
            DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, CodendMeshSize, QCCodendMeshSize, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_MeshSizeMG (\
                DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, MeshSizeMG, QCMeshSizeMG, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_NumberGillnets (\
            DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, NumberGillnets, QCNumberGillnets, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_AverageGillnetLength (\
                DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, AverageGillnetLength, QCAverageGillnetLength, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_NumberHooks (\
            DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, NumberHooks, QCNumberHooks, QC_CaseType)")
   
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_NumberWindows (\
            DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, NumberWindows, QCNumberWindows, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedPresence_NumberPots (\
        DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, GearType, NumberPots, QCNumberPots, QC_CaseType)")
    # Presence Misc
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedMiscPresence_RecTGearDamage (\
        DataBase_ID, RecordIdentifier, DeploymentUID, ASOCCode, DeploymentNumber, SetNumber\
        Year, GearType, RecordType, GearDamage, QC_Message)")

    con.commit()
    cur.close()
    con.close()

