from attr import validate
import streamlit as st
import pandas as pd
import numpy as np
from streamlit.state.session_state import SessionState
from src.utils import rpm_2_rads, rms_2_peak, peak_2_rms, inverse_clarke, load_dataframe, col_removal, determine_transients, sample_transients, transient_removal, eff_pc, round_speeds, spd_trq_grid, loss_tables, mtr_loss_table_code
from src.symbols import symbol_auto_select,t_demanded_symbols, t_measured_symbols, speed_rpm_symbols, vdc_symbols, idc_symbols, loss_inv_comp_symbols, ud_rms_symbols, uq_rms_symbols, id_peak_symbols ,iq_peak_symbols
from src.plotter import transient_removal_plot, plot_losses, plot_powers, plot_3D
from src.report import mtr_loss_report_details
from src.colors import sequential_color_dict, diverging_color_dict, plot_color_set

page_config = st.set_page_config(
                                page_title              ="Motor Loss Tool", 
                                page_icon               ="🔻", 
                                )

st.title("Motor Loss Tool 🔻")

st.write("This tool is to be used to calculate motor losses from a provided data set.")

t_demanded      = "Torque Demanded [Nm]"
t_measured      = "Torque Measured [Nm]"
speed_rpm       = "Speed [rpm]"
speed_round     = "Speed [rpm] Rounded"
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
eff_inv         = "Inverter Efficiency [%]"
eff_mtr         = "Motor Efficiency [%]"
eff_sys         = "System Efficiency [%]"
op_quad         = "Operating Quadrant"

df = pd.DataFrame()

st.markdown("---")

st.subheader("Upload File(s)")
st.checkbox("Show first 10 rows as table", key = "Data Head")

uploaded_file = st.file_uploader(   
                                        label="",
                                        accept_multiple_files=True,
                                        type=['csv', 'xlsx']
                                        )

if uploaded_file == []:
    st.info("Please upload file(s) that represent one operating quadrant")
    st.stop()

else:

    df, columns  = load_dataframe(uploaded_files=uploaded_file)
    if st.session_state["Data Head"] == True:
        st.write(df.head(10))
    columns             = list(columns)

    columns.insert(0, "Not Selected")

st.markdown("---")

st.subheader("Details - *Optional*")

st.markdown("---")

st.header("Configure Symbols")
st.write("Signals must be manually selected if auto-select cannot find them.")

st.checkbox("Include MCU Inverter Losses?", key = "Include MCU Inverter Losses", value = True)

st.selectbox(t_measured,list(columns),  key = t_measured, index = symbol_auto_select(columns, t_measured_symbols))

st.selectbox(t_demanded,list(columns), key = t_demanded, index = symbol_auto_select(columns, t_demanded_symbols))

st.selectbox(speed_rpm,list(columns), key = speed_rpm, index = symbol_auto_select(columns, speed_rpm_symbols))

st.selectbox(vdc,list(columns), key = vdc, index = symbol_auto_select(columns, vdc_symbols))

st.selectbox(idc,list(columns), key = idc, index = symbol_auto_select(columns, idc_symbols))

st.selectbox(ud_rms,list(columns), key = ud_rms, index = symbol_auto_select(columns, ud_rms_symbols))

st.selectbox(uq_rms,list(columns), key = uq_rms, index = symbol_auto_select(columns, uq_rms_symbols))

st.selectbox(id_peak,list(columns), key = id_peak, index = symbol_auto_select(columns, id_peak_symbols))

st.selectbox(iq_peak,list(columns), key = iq_peak, index = symbol_auto_select(columns, iq_peak_symbols))

if st.session_state["Include MCU Inverter Losses"] == True:
    st.selectbox(loss_inv_comp,list(columns), key = loss_inv_comp, index = symbol_auto_select(columns, loss_inv_comp_symbols))

st.markdown("---")

st.header("Table Configuration")

table_x_field, table_y_field   = st.columns(2)
table_x_field.number_input("Table Size [X]", min_value=0, max_value=50, value=26, step=1, key = "Table Size [X]")
table_y_field.number_input("Table Size [Y]", min_value=0, max_value=50, value=17, step=1, key = "Table Size [Y]")

torque_x_field, speed_y_field   = st.columns(2)
torque_x_field.number_input("Max Motor Torque", min_value=0, max_value=1000, value=300, step=1, key = "Max Motor Torque")
speed_y_field.number_input("Max Motor Speed", min_value=0, max_value=20000, value=13000, step=1, key = "Max Motor Speed")

torque_bp   = np.linspace(0, int(st.session_state["Max Motor Torque"]), int(st.session_state["Table Size [X]"]), dtype='int')
speed_bp    = np.linspace(0, int(st.session_state["Max Motor Speed"]), int(st.session_state["Table Size [Y]"]), dtype='int')

bp_display = pd.DataFrame(index=torque_bp, columns=speed_bp)
bp_display = bp_display.fillna(value="<Mtr Loss>") 
st.write(bp_display)
st.markdown("---")


df_formatted = col_removal(df, list(st.session_state.values()))

# Rename header to readable
if st.session_state["Include MCU Inverter Losses"] == False:
    df_formatted.rename(columns = {
        st.session_state["t_demanded"]  : t_demanded,    
        st.session_state["t_measured"]  : t_measured,  
        st.session_state["speed_rpm"]   : speed_rpm,         
        st.session_state["vdc"]         : vdc,           
        st.session_state["idc"]         : idc,           
        st.session_state["uq_rms"]      : uq_rms,        
        st.session_state["ud_rms"]      : ud_rms,           
        st.session_state["id_peak"]     : id_peak,       
        st.session_state["iq_peak"]     : iq_peak       
                        }, 
                          inplace = True)
else:
      df_formatted.rename(columns = {
        st.session_state[t_demanded]    : t_demanded,    
        st.session_state[t_measured]    : t_measured,  
        st.session_state[speed_rpm]     : speed_rpm,         
        st.session_state[vdc]           : vdc,           
        st.session_state[idc]           : idc,           
        st.session_state[uq_rms]        : uq_rms,        
        st.session_state[ud_rms]        : ud_rms,           
        st.session_state[id_peak]       : id_peak,       
        st.session_state[iq_peak]       : iq_peak,
        st.session_state[loss_inv_comp] : loss_inv_comp       
                        }, 
                          inplace = True)

if any(value == 'Not Selected' for value in st.session_state.values()) == True:
    st.warning("Please select all symbols")
    st.stop()

with st.spinner("Calculating signals"):
    # Post process signals

    # Mechanical
    df_formatted[speed_rads]              = rpm_2_rads(df_formatted[speed_rpm])
    df_formatted[pwr_mech]                = df_formatted[speed_rads] * df_formatted[t_measured]

    # DC Link       
    df_formatted[pwr_dc]                  = df_formatted[vdc] * df_formatted[idc]

    # Phase Peak        
    df_formatted[ud_peak]                 = rms_2_peak(df_formatted[ud_rms]) 
    df_formatted[uq_peak]                 = rms_2_peak(df_formatted[uq_rms]) 

    # Phase RMS     
    df_formatted[id_rms]                  = peak_2_rms(df_formatted[id_peak]) 
    df_formatted[iq_rms]                  = peak_2_rms(df_formatted[iq_peak]) 
    
    # Phase
    df_formatted[is_rms]                                        = np.sqrt( ( df_formatted[id_rms] * df_formatted[id_rms] ) + ( df_formatted[iq_rms] * df_formatted[iq_rms] ) )
    df_formatted[i_a], df_formatted[i_b], df_formatted[i_c]     = inverse_clarke(df_formatted[id_rms],df_formatted[iq_rms])
    df_formatted[pwr_ac]                                        = (3/2) * ( df_formatted[ud_peak] * df_formatted[id_peak] ) + ( df_formatted[uq_peak] * df_formatted[iq_peak] ) 

    # Losses
    df_formatted[loss_inv]                = df_formatted[pwr_dc] - df_formatted[pwr_ac]
    df_formatted[loss_mtr]                = df_formatted[pwr_ac] - df_formatted[pwr_mech]
    if st.session_state["Include MCU Inverter Losses"] == True:
        df_formatted[loss_mtr_comp]       = df_formatted[pwr_dc] - df_formatted[loss_inv_comp] - df_formatted[pwr_mech]
    df_formatted[loss_sys]                = df_formatted[pwr_dc] - df_formatted[pwr_mech]

st.subheader("Transient Removal - *Optional*")

with st.spinner("Generating transient removal tool"):

    st.write("Make sure the transient removal process is removing the required data; when there is a step change and time taken until steady state is reached.")
    st.markdown("If this is not achieved, adjust the variable `Dwell Period` using the slider below")
    st.markdown("Scan through torque steps using the `Sample` slider to determine if the `Dwell Period` is appropiate for the range of torque steps.")

    dwell_col, sample_col, t_d_filter_col = st.columns(3)
    dwell_col.slider("Dwell Period", min_value=0, max_value=2000, step=1, value= 500, key = "Dwell Period")
    t_d_filter_col.number_input("Torque Demanded Filter", min_value=0.0,max_value=300.0,step=0.1,value=1.0,help="If torque demand is not as consistent as expected i.e. during derate, apply a threshold to ignore changes smaller than the filter",key = "Torque Demanded Filter")

    Step_index, Stop_index          = determine_transients(df_formatted,t_demanded,st.session_state["Torque Demanded Filter"], st.session_state["Dwell Period"]) 
    
    sample_col.slider("Sample", min_value=1, max_value=abs(len(Stop_index)-1), step=1, value= round(abs(len(Stop_index)-1)/2), key = "Sample")


    transient_sample                = sample_transients(Step_index, Stop_index, df_formatted, st.session_state)    
    transient_removal_sample_plot   = transient_removal_plot(transient_sample, Step_index, Stop_index, df_formatted, st.session_state,  t_demanded, None, t_measured)

    df_formatted = df_formatted.drop(['Step_Change'], axis = 1)

    st.plotly_chart(transient_removal_sample_plot)

rem_trans_col1, rem_trans_col2, rem_trans_col3 = st.columns(3)

if rem_trans_col2.checkbox("Remove Transients", key = "Remove Transients") == True: 
    with st.spinner("Removing Transients from data"):
        df_formatted = transient_removal(df_formatted, Step_index, Stop_index)
        st.success(str(len(Stop_index)-1) + " Transients Removed")

st.markdown("---")

st.subheader("Power and Losses -*Optional*")

col_data_table, col_rows = st.columns(2)
col_data_table.checkbox("Display Data as Table", key = "Data as Table")
col_rows.selectbox("Number of Rows to Display", ["10","20","50","100","All"], key = "Number of Rows")
st.checkbox("Plot Powers", key = "Plot Powers")
st.checkbox("Plot Losses", key = "Plot Losses")

if st.session_state["Data as Table"] == True:
    if st.session_state["Number of Rows"] != "All":
        st.write(df_formatted.head(int(st.session_state["Number of Rows"])))
    else:
        st.write(df_formatted)

if st.session_state["Plot Powers"] == True:
    with st.spinner("Genearting Power Plot"):
        power_plot = plot_powers(df_formatted, pwr_mech, pwr_dc, pwr_ac)
        st.write(power_plot)

if st.session_state["Plot Losses"] == True:
    with st.spinner("Genearting Losses Plot"):
        losses_plot = plot_losses(df_formatted, loss_mtr, loss_mtr_comp, loss_inv, loss_inv_comp, loss_sys)
        st.write(losses_plot)

st.markdown("---")

st.subheader("Quadrant Determination")

col_spd_th, col_trq_th = st.columns(2)
col_spd_th.number_input("Zero Speed Threshold", min_value=0.0, max_value=500.0, value=0.0, step=0.5, key = "Speed Threshold")
col_trq_th.number_input("Zero Torque Threshold", min_value=0.0, max_value=500.0, value=0.0, step=0.5, key = "Torque Threshold")

# Determine operating quadrant
df_formatted[op_quad] = 'VEH_STP'
df_formatted[op_quad] = np.where( (df_formatted[speed_rpm] > st.session_state["Speed Threshold"]) & (df_formatted[t_measured] > st.session_state["Torque Threshold"]), 'DRV_FWD', df_formatted[op_quad] )
df_formatted[op_quad] = np.where( (df_formatted[speed_rpm] > st.session_state["Speed Threshold"]) & (df_formatted[t_measured] < st.session_state["Torque Threshold"]), 'BRK_FWD', df_formatted[op_quad] )
df_formatted[op_quad] = np.where( (df_formatted[speed_rpm] < st.session_state["Speed Threshold"]) & (df_formatted[t_measured] < st.session_state["Torque Threshold"]), 'DRV_REV', df_formatted[op_quad] )
df_formatted[op_quad] = np.where( (df_formatted[speed_rpm] < st.session_state["Speed Threshold"]) & (df_formatted[t_measured] > st.session_state["Torque Threshold"]), 'BRK_REV', df_formatted[op_quad] )

# Inverter Efficiency
df_formatted[eff_inv] = 0.0
DRV_Index = np.where( (df_formatted[op_quad] == 'DRV_FWD') | (df_formatted[op_quad] == 'DRV_REV') )
BRK_Index = np.where( (df_formatted[op_quad] == 'BRK_FWD') | (df_formatted[op_quad] == 'BRK_REV') )
df_formatted[eff_inv].iloc[DRV_Index] = eff_pc( df_formatted[pwr_ac].iloc[DRV_Index], df_formatted[pwr_dc].iloc[DRV_Index] )
df_formatted[eff_inv].iloc[BRK_Index] = eff_pc( df_formatted[pwr_dc].iloc[BRK_Index], df_formatted[pwr_ac].iloc[BRK_Index] )

# Motor Efficiency
df_formatted[eff_mtr] = 0.0
DRV_Index = np.where( (df_formatted[op_quad] == 'DRV_FWD') | (df_formatted[op_quad] == 'DRV_REV') )
BRK_Index = np.where( (df_formatted[op_quad] == 'BRK_FWD') | (df_formatted[op_quad] == 'BRK_REV') )
df_formatted[eff_mtr].iloc[DRV_Index] = eff_pc( df_formatted[pwr_mech].iloc[DRV_Index], df_formatted[pwr_ac].iloc[DRV_Index] )
df_formatted[eff_mtr].iloc[BRK_Index] = eff_pc( df_formatted[pwr_ac].iloc[BRK_Index], df_formatted[pwr_mech].iloc[BRK_Index] )

# System Efficiency
df_formatted[eff_sys] = 0.0
DRV_Index = np.where( (df_formatted[op_quad] == 'DRV_FWD') | (df_formatted[op_quad] == 'DRV_REV') )
BRK_Index = np.where( (df_formatted[op_quad] == 'BRK_FWD') | (df_formatted[op_quad] == 'BRK_REV') )
df_formatted[eff_sys].iloc[DRV_Index] = eff_pc( df_formatted[pwr_mech].iloc[DRV_Index], df_formatted[pwr_dc].iloc[DRV_Index] )
df_formatted[eff_sys].iloc[BRK_Index] = eff_pc( df_formatted[pwr_dc].iloc[BRK_Index], df_formatted[pwr_mech].iloc[BRK_Index] )

st.markdown("---") 

st.header("Round Speed")  

st.number_input("Base", min_value=1, max_value=5000, value=50, step=1, key = "Speed Base")

round_spd_col1, round_spd_col2, round_spd_col3 = st.columns(3)
if round_spd_col2.checkbox("Round Speed", key = "Round Speed") == True:
    df_formatted_avg = round_speeds(df_formatted, speed_rpm, t_demanded, st.session_state["Speed Base"])
    number_of_rounded_speeds = len((df_formatted_avg[speed_round]).unique())
    st.success(str(number_of_rounded_speeds) + " Unique Speed Points Found")
else:
    st.stop()

Meshgrid_Speed, Meshgrid_Torque, speed_bp, torque_bp = spd_trq_grid(df_formatted_avg, op_quad, speed_rpm, t_measured, st.session_state["Max Motor Speed"], st.session_state["Max Motor Torque"], speed_bp, torque_bp, st.session_state["Speed Threshold"], st.session_state["Torque Threshold"])
st.markdown("---") 

st.header("Losses")

fill_table_val, fill_table_method = st.columns(2)
fill_table_val.selectbox("Fill", ["NaN", "0"], key = "Fill Table Value" )
fill_table_method.selectbox("Method", ["linear", "nearest", "cubic"], key = "Fill Table Method" )
Loss_Inv_Table, Loss_Mtr_Table, Loss_Sys_Table = loss_tables(df_formatted_avg, speed_bp, torque_bp, Meshgrid_Speed, Meshgrid_Torque, speed_round, t_measured, loss_inv, loss_mtr_comp, loss_sys, st.session_state["Fill Table Method"], st.session_state["Fill Table Value"])

st.subheader("Tables")
st.write("Inverter Loss Table")
Loss_Inv_Table_display = pd.DataFrame(index=torque_bp, columns=speed_bp, data=Loss_Inv_Table)
st.write(Loss_Inv_Table_display)

st.write("Motor Loss Table")
Loss_Mtr_Table_display = pd.DataFrame(index=torque_bp, columns=speed_bp, data=Loss_Mtr_Table)
st.write(Loss_Mtr_Table_display)

st.write("System Loss Table")
Loss_Sys_Table_display = pd.DataFrame(index=torque_bp, columns=speed_bp, data=Loss_Sys_Table)
st.write(Loss_Sys_Table_display)

st.subheader("Plots")

plot_types, color_scales, color_maps, color_pre = st.columns(4)
plot_types.selectbox("Chart Type", ["Contour", "Surface","Heatmap","3D Scatter"], key = "Chart Type" )

color_scales.selectbox("Color Scale", ["Sequential", "Diverging"], key = "Color Scale" )

if st.session_state["Color Scale"] == 'Sequential':
    color_map = list(sequential_color_dict().keys())
else:
    color_map = list(diverging_color_dict().keys())

color_maps.selectbox("Color Map", color_map, key = "Color Map" )
if  st.session_state["Color Scale"] == 'Sequential':
    color_palette = sequential_color_dict().get(st.session_state["Color Map"])
else:
    color_palette = diverging_color_dict().get(st.session_state["Color Map"])

colormap_preview = plot_color_set(color_palette, st.session_state["Color Map"])
color_pre.image(colormap_preview, use_column_width = True)

st.subheader("Data Overlay")
if st.checkbox("Show Data Overlayed"):
    overlay = True
else:
    overlay = False

t_d_error_nm_ovr1, t_d_error_nm_ovr2 = st.columns(2)
t_d_error_nm_ovr1.slider("Opacity",value=0.5,min_value=0.0, max_value=1.0, step=0.01, key = "Overlay Alpha")
t_d_error_nm_ovr2.color_picker("Overlay Color", key = "Overlay Color")

st.checkbox("Plot Inverter Losses", key = "Plot Inverter Losses")
st.checkbox("Plot Motor Losses", key = "Plot Motor Losses")
st.checkbox("Plot System Losses", key = "Plot System Losses" )

if st.session_state["Plot Inverter Losses"] == True:
    loss_inv_plot = plot_3D(df_formatted_avg, speed_round, t_demanded, loss_inv, speed_bp, torque_bp, Loss_Inv_Table, st.session_state["Chart Type"], color_palette, overlay, st.session_state["Overlay Alpha"], st.session_state["Overlay Color"])
    st.plotly_chart(loss_inv_plot)
    loss_inv_html_string = '''<br><h4> Inverter Losses [W] ''' + str(st.session_state["Chart Type"]) + ''' </h4>'''
    loss_inv_html_plot = loss_inv_plot.to_html(default_width = "1200px",default_height = "720px")
else:
    loss_inv_html_string = ""
    loss_inv_html_plot = ""

if st.session_state["Plot Motor Losses"] == True:
    loss_mtr_plot = plot_3D(df_formatted_avg, speed_round, t_demanded, loss_mtr, speed_bp, torque_bp, Loss_Mtr_Table, st.session_state["Chart Type"], color_palette, overlay, st.session_state["Overlay Alpha"], st.session_state["Overlay Color"])
    st.plotly_chart(loss_mtr_plot)
    loss_mtr_html_string = '''<br><h4> Motor Losses [W] ''' + str(st.session_state["Chart Type"]) + ''' </h4>'''
    loss_mtr_html_plot = loss_mtr_plot.to_html(default_width = "1200px",default_height = "720px")
else:
    loss_mtr_html_string = ""
    loss_mtr_html_plot = ""

if st.session_state["Plot System Losses"] == True:
    loss_sys_plot = plot_3D(df_formatted_avg, speed_round, t_demanded, loss_sys, speed_bp, torque_bp, Loss_Sys_Table, st.session_state["Chart Type"], color_palette, overlay, st.session_state["Overlay Alpha"], st.session_state["Overlay Color"])
    st.plotly_chart(loss_sys_plot)
    loss_sys_html_string = '''<br><h4> System Losses [W] ''' + str(st.session_state["Chart Type"]) + ''' </h4>'''
    loss_sys_html_plot = loss_sys_plot.to_html(default_width = "1200px",default_height = "720px")
else:
    loss_sys_html_string = ""
    loss_sys_html_plot = ""


st.subheader("Code")

Loss_Mtr_Table_Code = mtr_loss_table_code(Loss_Mtr_Table)
with st.expander("Motor Loss Table [Code Formatted]"):
    st.text_area(label = "", value = Loss_Mtr_Table_Code, height = 720, help = "Ctrl+A in the text area and copy to the relevent location.")

st.header("Report")
test_dict = mtr_loss_report_details()

st.header("Report Appendix Items")
st.checkbox("Include non-averaged dataset", key = "Report Appendix Full Dataset")

if st.session_state["Report Appendix Full Dataset"] == True:
    report_appendix_full = '''
    <br><h4>Full Dataset Table</h4>
    <br><p>The below table contains all the data uploaded,selected and formatted.</p>
    <br>'''+ df_formatted.to_html().replace('<table border="1" class="dataframe">','<table class="table table-sm">') +'''
    '''
else: 
    report_appendix_full = ""

files = []
for file in uploaded_file:
    files.append(file.name)

if st.session_state["Remove Transients"] == True:
    transient_removal_html = ''' 
    <p>Dwell Period: '''+str(st.session_state["Dwell Period"])+'''</p>'''+'''
    <p>Torque Demanded Filter : '''+str(st.session_state["Torque Demanded Filter"])+''' Nm </p>'''

else:
    transient_removal_html = ''' 
    <p>Not applied</p>
    '''

if (st.session_state["Chart Type"] == "Contour") and ((st.session_state["Plot Inverter Losses"] == True) or (st.session_state["Plot Motor Losses"] == True) or (st.session_state["Plot Motor Losses"] == True)):
    plot_info = '''The below contour plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm) 
    <br>Data between measured data points have been interpolated between the nearest available data using the '''+ str(st.session_state["Chart Type"])+''' method.
    <br>Missing data has been filled with the following value: ''' + str(st.session_state["Fill Table Value"])+'''
    '''

elif (st.session_state["Chart Type"] == "Surface") and ((st.session_state["Plot Inverter Losses"] == True) or (st.session_state["Plot Motor Losses"] == True) or (st.session_state["Plot Motor Losses"] == True)):
    plot_info = '''The below surface plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm) and Torque error
    <br>Data between measured data points have been interpolated between the nearest available data using the '''+ str(st.session_state["Chart Type"])+''' method.
    <br>Missing data has been filled with the following value: ''' + str(st.session_state["Fill Table Value"])+'''
    '''

elif (st.session_state["Chart Type"] == "Heatmap") and ((st.session_state["Plot Inverter Losses"] == True) or (st.session_state["Plot Motor Losses"] == True) or (st.session_state["Plot Motor Losses"] == True)):
    plot_info = '''The below heatmap plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm)
    <br>Data between measured data points have been interpolated between the nearest available data using the '''+ str(st.session_state["Chart Type"])+''' method.
    <br>Missing data has been filled with the following value: ''' + str(st.session_state["Fill Table Value"])+'''
    '''

elif (st.session_state["Chart Type"] == "Scatter 3D") and ((st.session_state["Plot Inverter Losses"] == True) or (st.session_state["Plot Motor Losses"] == True) or (st.session_state["Plot Motor Losses"] == True)):
    plot_info = '''The below 3D Scatter plot(s) shows Torque against speed rounded (to the nearest: ''' + str(st.session_state["Speed Base"]) + ''' rpm) and Losses'''

else:
     plot_info = ""

input_files_table = pd.DataFrame(files)
input_files_table = input_files_table.to_html(header=False).replace('<table border="1" class="dataframe">','<table class="table table-borderless table-sm table-hover">')

test_detail = {
    "Test Name"                 : st.session_state["Test Name"],
    "User"                      : st.session_state["User"],
    "Test Date"                 : st.session_state["Test Date"],
    "Test Note"                 : st.session_state["Test Note"]
}

dyno_detail = {
    "Dyno"                      : st.session_state["Dyno"],
    "Torque Speed Sensor"       : st.session_state["Torque Speed Sensor"],
    "Sensor Calibration Date"   : st.session_state["Sensor Calibration Date"]
}

software_detail = {
    "Software Level"            : st.session_state["Software Level"],
    "Software Location"         : st.session_state["Software Location"],
    "Software Notes"            : st.session_state["Software Notes"]
}

controller_detail = {
    "Controller Manufacturer"   : st.session_state["Controller Manufacturer"],
    "Controller Model"          : st.session_state["Controller Model"],
    "Controller Sample"         : st.session_state["Controller Sample"],
    "Controller Notes"          : st.session_state["Controller Notes"]
}

motor_detail = {
    "Motor Manufacturer"        : st.session_state["Motor Manufacturer"],
    "Motor Model"               : st.session_state["Motor Model"],
    "Motor Sample"              : st.session_state["Motor Sample"],
    "Motor Notes"               : st.session_state["Motor Notes"]

}


test_detail_table = pd.DataFrame.from_dict(test_detail,orient='index')
test_detail_table = test_detail_table.to_html(header=False, classes='table text-left', justify='left', border="0")

dyno_detail_table = pd.DataFrame.from_dict(dyno_detail,orient='index')
dyno_detail_table = dyno_detail_table.to_html(header=False, classes='table text-left', justify='left', border="0")

software_detail_table = pd.DataFrame.from_dict(software_detail,orient='index')
software_detail_table = software_detail_table.to_html(header=False, classes='table text-left', justify='left', border="0")

controller_detail_table = pd.DataFrame.from_dict(controller_detail,orient='index')
controller_detail_table = controller_detail_table.to_html(header=False, classes='table text-left', justify='left', border="0")

motor_detail_table = pd.DataFrame.from_dict(motor_detail,orient='index')
motor_detail_table = motor_detail_table.to_html(header=False, classes='table text-left', justify='left', border="0")

html_string = '''
<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
        <style>body{ margin:100 100; background:white; }</style>
    </head>
    <body>
        <div class="container h-10">
            <div class="row h-10 justify-content-center align-items-center">
            <img src="https://turntide.com/wp-content/themes/turntide2021/theme/static/images/logo-color.svg" style="width: 400px" />
            <br>
            </div>
        </div>

        <h1 class="text-center">Motor Loss Results</h1>

        <br>

        <!-- *** Section 1 *** --->
        <h2>Report Details</h2>
        <br>
            <h4>Testing</h4>
                '''+ test_detail_table +'''
                <br>

            <h4>Software</h4>
                '''+ software_detail_table +'''
                <br>

            <h4>Motor</h4>
                '''+ motor_detail_table +'''
                <br>

            <h4>Controller</h4>
                '''+ controller_detail_table +'''
                <br>

            <h4>Dyno</h4>
                '''+ dyno_detail_table +'''
                <br>

            <!-- *** Section 2 *** --->
            <h2>Input Files</h2>
                '''+ input_files_table +'''
                <br>

            <h2>Transient Removal</h2> 
                '''+ transient_removal_html +'''
                '''+ transient_removal_sample_plot.to_html(default_width = "1200px",default_height = "720px") +'''
                <br>

            <h2>Unique Points</h2>
                <p>There are '''+ str(number_of_rounded_speeds)+''' unique speed points identified.</p>
                <br>
            <!-- *** Section 4 *** --->
            <h2>Loss Tables</h2>
            <h4>Inverter Loss Table</h4>
            '''+ Loss_Inv_Table_display.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped table-sm">') + '''
            <br>
            <h4>Motor Loss Table</h4>
            '''+ Loss_Mtr_Table_display.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped table-sm">') + '''
            <br>
            <h4>System Loss Table</h4>
            '''+ Loss_Sys_Table_display.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped table-sm">') + '''

        <!-- *** Section 4 *** --->
        <br>
        <h2>Plots</h2>
            <p>Selected plots will appear here.</p>          
            ''' + plot_info + '''
            ''' + loss_inv_html_string + '''
            ''' + loss_inv_html_plot + '''
            ''' + loss_mtr_html_string + '''
            ''' + loss_mtr_html_plot + '''
            ''' + loss_sys_html_string + '''
            ''' + loss_sys_html_plot + '''
        <!-- *** Section 4 *** --->
        <br>
        <h2>Appendix</h2>
            <br>
            <h4>Code C Formatted</h4>
            '''+ Loss_Mtr_Table_Code + '''
            <br>
            <h4>Data analysed as Table</h4> 
            ''' + df_formatted_avg.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped table-sm">') + '''
            <br>
            ''' + report_appendix_full + '''
    </body>
</html>
'''

bl, report_col ,br = st.columns(3)

report_col.download_button(
    label="Download Report",
    data=html_string,
    file_name="motor_loss.html",
    mime="application/octet-stream"
)