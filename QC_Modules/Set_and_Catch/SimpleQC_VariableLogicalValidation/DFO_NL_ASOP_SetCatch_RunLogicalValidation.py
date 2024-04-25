
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_RunLogicalValidation_BackEnd

def SetCatch_VariableLogicalValidation():
    TotalFailedQC_LogicalValidation = DFO_NL_ASOP_SetCatch_RunLogicalValidation_BackEnd.RunSetCatch_LogicalValidation_BackEnd()
    ReturnFailedMessage = str(TotalFailedQC_LogicalValidation) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedQC_LogicalValidation > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedQC_LogicalValidation