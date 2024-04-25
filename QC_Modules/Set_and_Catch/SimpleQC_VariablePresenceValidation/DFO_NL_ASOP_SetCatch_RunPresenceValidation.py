
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_SetCatch_RunPresenceValidation_BackEnd

def SetCatch_VariablePresenceValidation():
    TotalFailedQC_PresenceValidation = DFO_NL_ASOP_SetCatch_RunPresenceValidation_BackEnd.RunSetCatch_PresenceValidation_BackEnd()
    ReturnFailedMessage = str(TotalFailedQC_PresenceValidation) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedQC_PresenceValidation > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedQC_PresenceValidation