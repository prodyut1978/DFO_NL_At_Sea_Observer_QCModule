
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_RunConsistencyValidation_BackEnd

def SetCatch_VariableConsistencyValidation():
    TotalFailedQC_ConsistencyValidation = DFO_NL_ASOP_SetCatch_RunConsistencyValidation_BackEnd.RunSetCatch_ConsistencyValidation_BackEnd()
    ReturnFailedMessage = str(TotalFailedQC_ConsistencyValidation) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedQC_ConsistencyValidation > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedQC_ConsistencyValidation