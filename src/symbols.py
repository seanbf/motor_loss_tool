from logging import exception

speed_rpm_symbols = [
    "Transducer_Speed_IOP",
    " Transducer_Speed_IOP",
    "Transducer_Speed_MCP",
    " Transducer_Speed_MCP",
    "Transducer_Spd_IOP",
    "Transducer_Spd_MCP",
    "TransducerSpd_IOP",
    "TransducerSpd_MCP",
    " tesInputData.L2mPosSpdArb_RotorSpd_IOP",
    "tesInputData.L2mPosSpdArb_RotorSpd_IOP",
    " tesInputData.L2mPosSpdArb_RotorSpd_MCP",
    "tesInputData.L2mPosSpdArb_RotorSpd_MCP"
]

t_demanded_symbols = [
    "AvaIfData.AvaDataExch_TrqCond_MCP",
    " AvaIfData.AvaDataExch_TrqCond_MCP",
    "AvaIfData.AvaDataExch_TrqCond_IOP",
    " AvaIfData.AvaDataExch_TrqCond_IOP",
    "vcanOutputData.L2mVcan_TarTrq.val_IOP",
    " vcanOutputData.L2mVcan_TarTrq.val_IOP",
    "vcanOutputData.L2mVcan_TarTrq.val_MCP",
    " vcanOutputData.L2mVcan_TarTrq.val_MCP",
    " TesOp_B.L2m_TarTrq_MCP",
    "TesOp_B.L2m_TarTrq_MCP",
    " TesOp_B.L2m_TarTrq_IOP",
    "TesOp_B.L2m_TarTrq_IOP"
]

t_measured_symbols = [
        "Transducer_Torque_IOP",
        "Transducer_Torque_MCP",
        "Transducer_Trq_IOP",
        "Transducer_Trq_MCP",
        "TransducerTrq_IOP",
        "TransducerTrq_MCP"
]

t_estimated_signals = [
    " tesOutputData.L2mTes_EstTrq.val_MCP",
    "tesOutputData.L2mTes_EstTrq.val_MCP",
    " tesOutputData.L2mTes_EstTrq.val_IOP",
    "tesOutputData.L2mTes_EstTrq.val_IOP",
    " TesOp_B.L2mTes_EstTrq_MCP",
    "TesOp_B.L2mTes_EstTrq_MCP",
    " TesOp_B.L2mTes_EstTrq_IOP",
    "TesOp_B.L2mTes_EstTrq_IOP"
]

vdc_symbols = [
    " sensvdcOutputData.L2mSensVdc_Vdc.val_MCP",
    "sensvdcOutputData.L2mSensVdc_Vdc.val_MCP",
    " sensvdcOutputData.L2mSensVdc_Vdc.val_IOP",
    "sensvdcOutputData.L2mSensVdc_Vdc.val_IOP",
    "tesInputData.L2mSensVdc_Vdc_MCP",
    " tesInputData.L2mSensVdc_Vdc_MCP",
    "tesInputData.L2mSensVdc_Vdc_IOP",
    " tesInputData.L2mSensVdc_Vdc_IOP",
]

idc_symbols = [
    " sensidcOutputData.L2mSensIdc_Idc.val_MCP",
    "sensidcOutputData.L2mSensIdc_Idc.val_MCP",
    " sensidcOutputData.L2mSensIdc_Idc.val_IOP",
    "sensidcOutputData.L2mSensIdc_Idc.val_IOP",
    " SensIdcOp_B.L2mSensIdc_IdcPhy_IOP",
    "SensIdcOp_B.L2mSensIdc_IdcPhy_IOP",
    " SensIdcOp_B.L2mSensIdc_IdcPhy_MCP",
    "SensIdcOp_B.L2mSensIdc_IdcPhy_MCP",
    "tesInputData.L2mSensIdc_Idc_IOP",
    " tesInputData.L2mSensIdc_Idc_IOP",
    "tesInputData.L2mSensIdc_Idc_MCP",
    " tesInputData.L2mSensIdc_Idc_MCP"
]

loss_inv_comp_symbols = [
    "InverterEfficiency_MCP",
    "InverterEfficiency_IOP"
]


def symbol_auto_select(symbols_in, compared_symbols):
    
    for signals in compared_symbols:
        try:
            list_index = list(symbols_in).index(signals)
            break
        except:
            list_index = 0

    return list_index