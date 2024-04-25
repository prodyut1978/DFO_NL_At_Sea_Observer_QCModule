
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_RunRangeValidation_BackEnd

def SetCatch_VariableRangeValidation():
    TotalFailedQC_RangeValidation = DFO_NL_ASOP_SetCatch_RunRangeValidation_BackEnd.RunSetCatch_RunRangeValidation_BackEnd()
    ReturnFailedMessage = str(TotalFailedQC_RangeValidation) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedQC_RangeValidation > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedQC_RangeValidation