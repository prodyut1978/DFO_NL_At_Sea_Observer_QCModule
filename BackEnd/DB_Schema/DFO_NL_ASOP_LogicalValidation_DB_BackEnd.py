import sqlite3
#backend

DB_SetCatch_Validation_Logical = ("./BackEnd/Sqlite3_DB/QC_Check_LogicalConsistency_DB/DFO_NL_ASOP_SetCatch_LogicalValidation.db")

def get_DB_SetCatch_Validation_Logical():
    conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
    return conn

def DFO_NL_ASOP_LogicalValidation_DB():
    con= sqlite3.connect(DB_SetCatch_Validation_Logical)
    cur=con.cursor()
    
    ## For RunLogicalFailed_CatchVariables
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_CatchVariables (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                RecordType, CodendMeshSize, MeshSizeMG,\
                NumberPotReleasedCrab, DirectedSpecies, EstimatedWeightReleasedCrab,\
                KeptWeight, DiscardWeight)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_CatchVariable_CodendMeshSize (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                CodendMeshSize, MeshSizeMG, RecordType, QCCodendMeshSize, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_CatchVariable_DirectedSpecies (\
                DataBase_ID, RecordIdentifier, DeploymentUID, \
                NumberPotReleasedCrab, DirectedSpecies, RecordType, QCDirectedSpecies, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_CatchVariable_NumberPotReleasedCrab (\
                DataBase_ID, RecordIdentifier, DeploymentUID, \
                EstimatedWeightReleasedCrab, NumberPotReleasedCrab, RecordType, QCNumberPotReleasedCrab, QC_CaseType)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_CatchVariable_KeptWeight_DiscardWeight (\
                DataBase_ID, RecordIdentifier, DeploymentUID, \
                KeptWeight, DiscardWeight, RecordType, QCKeptWeight_DiscardWeight, QC_CaseType)")
    
    ## For RunLogicalFailed_RecordType_SetNumber
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_RecordType_SetNumber (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                RecordType, DeploymentNumber, SetNumber, QCRecordType_SetNumber, QC_CaseType)")
    cur.execute("CREATE TABLE IF NOT EXISTS Logical_RecordType_SetNumber_FailSummary (\
                DeploymentUID, DeploymentNumber, SetNumber, RecordType, CountRecType1PresencePerSet)")
    
    ## For RunLogicalFailed_RecordType_NumberSpecies
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_RecordType_NumberSpecies (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                DeploymentNumber, SetNumber, RecordType, \
                NumberSpecies, QCRecordType_NumberSpecies, QCCaseType)")
    cur.execute("CREATE TABLE IF NOT EXISTS Logical_RecordType_NumberSpecies_FailSummary (\
                QCCaseType, QCRecordType_NumberSpecies, QCFailCount)")


    ## For RunLogicalFailed_RecordType_NumberSpecies_SpeciesCode
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_RecordType_SpeciesCode (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                DeploymentNumber, SetNumber, RecordType, \
                NumberSpecies, SpeciesCode, QCCaseType)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_NumberSpecies_SpeciesCode (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                DeploymentNumber, SetNumber, RecordType, \
                NumberSpecies, SpeciesCode, QCCaseType)")
    cur.execute("CREATE TABLE IF NOT EXISTS Logical_RecType_SpecsCode_NumbSpecs_FailSummary (\
                QCCaseType, QCFailCount)")
    
    ## For RunLogicalFailed_RecType1_DKWeight_NumIndv
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLogical_RecType_KW_DW_NI (\
                DataBase_ID, RecordIdentifier, DeploymentUID,\
                DeploymentNumber, SetNumber, RecordType, \
                NumberSpecies, SpeciesCode, KeptWeight,\
                DiscardWeight, NumberIndividuals, QCMessage)")

    con.commit()
    cur.close()
    con.close()

