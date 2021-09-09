import streamlit as st
import pandas as pd
import numpy as np
from utils import rpm_2_rads, rms_2_peak, peak_2_rms, inverse_clarke, load_dataframe

page_config = st.set_page_config(
                                page_title              ="Motor Loss Tool", 
                                page_icon               ="🔻", 
                                )

st.title("Motor")
st.title("Loss")
st.title("Tool")

st.write("This tool is to be used to calculate motor losses from a provided data set.")

t_demanded      = "Torque Demanded [Nm]"
t_estimated     = "Torque Estimated [Nm]"
t_measured      = "Torque Measured [Nm]"
speed_rpm       = "Speed [rpm]"
speed_rads      = "Speed [rad/s]"
vdc             = "DC Voltage [V]"
idc             = "DC Current [A]"
uq_rms          = "Uq Voltage [A RMS]"
ud_rms          = "Ud Voltage [A RMS]"
uq_peak         = "Uq [A Peak]"
ud_peak         = "Ud [A Peak]"
id_rms          = "Id [A RMS]"
iq_rms          = "Iq [A RMS]"
id_peak         = "Id [A Peak]"
iq_peak         = "Iq [A Peak]"
is_rms          = "Stator Current [A]"
i_a             = "Phase A Current [A]"
i_b             = "Phase B Current [A]"
i_c             = "Phase C Current [A]"
loss_inv        = "Inverter Losses [W]"
loss_inv_comp   = "Inverter Losses Compensated [W]"
loss_mtr        = "Motor Losses [W]"
loss_mtr_comp   = "Motor Losses Compensated [W]"
loss_sys        = "System Losses [W]"
pwr_mech        = "Mechanical Power [W}"
pwr_dc          = "DC Power [W]"
pwr_ac          = "AC Power [W]"
pwr_ph          = "Phase Power [W]"


df = pd.DataFrame()

st.markdown("---")

st.subheader("Upload File(s)")
st.checkbox("Show first 10 rows as table", key = "Data Head")
uploaded_file = st.sidebar.file_uploader(   
                                        label="",
                                        accept_multiple_files=True,
                                        type=['csv', 'xlsx']
                                        )

if uploaded_file is None:
    st.info("Please upload file(s)")
    st.stop()

elif uploaded_file is not None:

    original_file_name  = uploaded_file.name

    df, columns  = load_dataframe(uploaded_file=uploaded_file)

if st.session_state["Data Head"] == True:
    st.write(df.head(10))

st.markdown("---")

st.subheader("Details - *Optional*")

st.markdown("---")

st.subheader("Table Configuration")

st.markdown("---")

st.subheader("Transient Removal - *Optional*")

st.markdown("---")

with st.spinner("Calculating signals"):
    # Post process signals

    # Mechanical
    df[speed_rads]              = rpm_2_rads(df[speed_rpm])
    df[pwr_mech]                = df[speed_rads] * df[t_measured]

    # DC Link       
    df[pwr_dc]                  = df[vdc] * df[idc]

    # Phase Peak        
    df[ud_peak]                 = rms_2_peak(df[ud_rms]) 
    df[uq_peak]                 = rms_2_peak(df[uq_rms]) 

    # Phase RMS     
    df[id_rms]                  = peak_2_rms(df[id_peak]) 
    df[iq_rms]                  = peak_2_rms(df[iq_peak]) 
    
    # Phase
    df[is_rms]                  = np.sqrt( ( df[id_rms] * df[id_rms] ) + ( df[iq_rms] * df[iq_rms] ) )
    df[i_a], df[i_b], df[i_c]   = inverse_clarke(df[id_rms],df[iq_rms])
    df[pwr_ph]                  = (3/2) * ( df[ud_peak] * df[id_peak] ) + ( df[uq_peak] * df[iq_peak] ) 

    # Losses
    df[loss_inv]                = df[pwr_dc] - df[pwr_ph]
    df[loss_mtr]                = df[pwr_ph] - df[pwr_mech]
    df[loss_mtr_comp]           = df[pwr_dc] - df[loss_inv_comp] - df[pwr_mech]
    df[loss_sys]                = df[pwr_dc] - df[pwr_mech]

st.subheader("Power and Losses -*Optional*")
st.checkbox("Display Data as Table", key = "Data as Table")
st.checkbox("Plot Powers", key = "Plot Powers")
st.checkbox("Plot Losses", key = "Plot Losses")

if st.session_state["Plot Powers"] == True:
    with st.spinner("Genearting Power Plot"):
        power_plot = ("Power Chart")
        st.write(power_plot)
if st.session_state["Plot Losses"] == True:
    with st.spinner("Genearting Losses Plot"):
        losses_plot = ("Losses Chart")
        st.write(losses_plot)

st.markdown("---")