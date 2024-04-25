
from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_IntegratedRangeQC_BackEnd

def SetCatch_IntegratedVariableRangeValidation():
    TotalFailedQC_RangeValidation = DFO_NL_ASOP_SetCatch_IntegratedRangeQC_BackEnd.RunIntegratedRangeValidation_BackEnd()
    ReturnFailedMessage = str(TotalFailedQC_RangeValidation) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedQC_RangeValidation > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedQC_RangeValidation