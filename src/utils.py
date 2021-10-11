import numpy as np
from scipy.interpolate import griddata
import pandas as pd
import streamlit as st

@st.cache
def load_dataframe(uploaded_files):
    with st.spinner("Generating Dataframe"):
        try:
            df = pd.concat( (pd.read_csv(f) for f in uploaded_files), ignore_index=True)
        except:
            df = pd.concat( (pd.read_excel(f) for f in uploaded_files), ignore_index=True)

        columns = list(df.columns)
        columns.append(None)

        return df, columns

def determine_transients(df, t_demanded, torque_demanded_filter, dwell_period):
    df["Step_Change"] = '0'
    df["Step_Change"] = df[t_demanded].diff()
    
    Step_index          = ( df.index[abs(df['Step_Change']) >= torque_demanded_filter] - 1 )
    Stop_index          = Step_index + dwell_period

    return Step_index, Stop_index

def sample_transients(Step_index, Stop_index, df, test_dict):

    transient_sample = df.iloc[ Step_index[test_dict["Sample"]]-250 : Stop_index[test_dict["Sample"]]+250 ]
    
    return transient_sample

def col_removal(data, list_to_keep):
    selected_data = pd.DataFrame
    selected_data = data.columns.intersection(list_to_keep)
    data = data[selected_data]

    return data

def transient_removal(df, Step_index, Stop_index):
    
#Transient Removal
    delete_slice = np.array(0)

    for x in range( len(Step_index) ):
        temp_slice = np.arange(Step_index[x], Stop_index[x])
        delete_slice = np.append(delete_slice, temp_slice)

    delete_slice = abs(delete_slice)
    df = df.drop(index = delete_slice)
    return df

def myround(x, base):
    return base * round(x/base)

def round_speeds(df, speed_signal, torque_demanded_signal, base):
    # Round measured speed to the nearest 50rpm.
    
    df[speed_signal + " Rounded"] = myround(df[speed_signal], base)

    # Group the data in the dataframe by the measured speed (rounded) and torque demanded.
    # Get average of all data within those subgroups and create new dataframe, df.
    df = df.groupby([speed_signal + " Rounded", torque_demanded_signal], as_index=False).agg("mean")

    return df

def torque_error_calc(df, t_demanded, t_estimated, t_measured, t_demanded_error_nm, t_demanded_error_pc, t_estimated_error_nm, t_estimated_error_pc):
    df[t_demanded_error_nm]    = 0
    df[t_demanded_error_nm]    = df[t_demanded_error_nm].where(df[t_demanded] >= 0, df[t_demanded] - df[t_measured])
    df[t_demanded_error_nm]    = df[t_demanded_error_nm].where(df[t_demanded] < 0, df[t_measured] - df[t_demanded])
    df[t_demanded_error_pc]    = ( (df[t_demanded] - df[t_measured]) / df[t_measured]) * 100

    df[t_estimated_error_nm]   = 0
    df[t_estimated_error_nm]   = df[t_estimated_error_nm].where(df[t_estimated] >= 0, df[t_measured] - df[t_estimated])
    df[t_estimated_error_nm]   = df[t_estimated_error_nm].where(df[t_estimated] < 0, df[t_estimated] - df[t_measured])
    df[t_estimated_error_pc]   =  ( (df[t_measured] - df[t_estimated]) / df[t_estimated]) * 100

    return df

def error_nm_analysis(df, limit_nm, limit_pc, t_to_analyse ,t_demanded, t_estimated, t_measured, speed_round, vdc, idc, error_nm, error_pc):

    if ( abs(df[error_nm]) > limit_nm ).any():
    
        error_table_nm = df[abs(df[error_nm]) > limit_nm].copy()
    
        if ( abs(error_table_nm[t_to_analyse]) <= (limit_nm/(limit_pc/100)) ).any():
            
            error_table_nm = error_table_nm[abs(error_table_nm[t_to_analyse]) <= (limit_nm/(limit_pc/100))].copy()
            error_table_nm.sort_values(by=error_nm, key = abs, ascending = False, inplace = True)
            error_table_nm = error_table_nm.filter([error_nm, error_pc, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])
            
            flag = False

        else:
            
            error_table_nm = df[abs(df[t_to_analyse]) <= (limit_nm/(limit_pc/100))].copy()
            error_table_nm.sort_values(by=error_nm,key = abs, ascending = False, inplace = True)
            error_table_nm = error_table_nm[0:5]
            error_table_nm = error_table_nm.filter([error_nm, error_pc, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])
            
            flag = True

    else:
        error_table_nm = df.copy()
        error_table_nm.sort_values(by=[error_nm, error_pc],key = abs, ascending = False, inplace = True)
        error_table_nm = error_table_nm[0:5]
        error_table_nm = error_table_nm.filter([error_nm, error_pc, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])
        
        flag = True

    min_error       = min(abs(error_table_nm[error_nm]))
    average_error   = np.mean(abs(error_table_nm[error_nm]))
    max_error       = max(abs(error_table_nm[error_nm]))

    return error_table_nm, min_error, average_error, max_error, flag

def error_pc_analysis(df, limit_nm, limit_pc, t_to_analyse, t_demanded, t_estimated, t_measured, speed_round, vdc, idc, error_nm, error_pc):

    if ( abs(df[error_pc]) > limit_pc ).any():
    
        error_table_pc = df[abs(df[error_pc]) > limit_pc].copy()
        
        if ( abs(error_table_pc[t_to_analyse]) > (limit_nm/(limit_pc/100)) ).any():
        
            error_table_pc = error_table_pc[abs(error_table_pc[t_to_analyse]) > (limit_nm/(limit_pc/100))].copy()
            error_table_pc.sort_values(by=error_pc, key = abs, ascending = False, inplace = True)
            error_table_pc = error_table_pc.filter([error_pc, error_nm, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])

            flag = False
            
        else:

            error_table_pc.sort_values(by=error_pc,key = abs, ascending = False, inplace = True)
            error_table_pc = error_table_pc[0:5]
            error_table_pc = error_table_pc.filter([error_pc, error_nm, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])

            flag = True
    else:


        error_table_pc = df.copy()
        error_table_pc.sort_values(by=[error_pc, error_nm],key = abs, ascending = False, inplace = True)
        error_table_pc = error_table_pc[0:5]
        error_table_pc = error_table_pc.filter([error_pc, error_nm, t_measured, t_demanded, t_estimated, speed_round, vdc, idc])

        flag = True

    min_error       = min(abs(error_table_pc[error_pc]))
    average_error   = np.mean(abs(error_table_pc[error_pc]))
    max_error       = max(abs(error_table_pc[error_pc]))
    
    return error_table_pc, min_error, average_error, max_error, flag

def z_col_or_grid(chart_type, fill, method, grid_res, x_in, y_in, z_in):
    '''
    Depending on graph wanted, format data as grid or columns
    '''
    x = x_in
    y = y_in
    z = z_in

    if chart_type != '3D Scatter':

        xi = np.linspace( float(min(x)), float(max(x)), int(grid_res) )
        yi = np.linspace( float(min(y)), float(max(y)), int(grid_res) )

        X,Y = np.meshgrid(xi,yi)

        z = griddata( (x,y),z,(X,Y), fill_value=fill, method=method)  
        x = xi
        y = yi

    return x, y, z

def spd_trq_grid(df, op_quad, speed_rpm, t_measured, max_mtr_spd, max_mtr_trq, speed_bp, torque_bp, spd_th, trq_th):
    Meshgrid_Speed_Array  = np.linspace(0, int(max_mtr_spd)+1, int(max_mtr_spd)+1)
    Meshgrid_Torque_Array = np.linspace(0, int(max_mtr_trq)+1, int(max_mtr_trq)+1)

    Meshgrid_Speed, Meshgrid_Torque = np.meshgrid(Meshgrid_Speed_Array, Meshgrid_Torque_Array)

    # Determine operating quadrant
    df[op_quad] = 'VEH_STP'
    df[op_quad] = np.where((df[speed_rpm] > spd_th) & (df[t_measured] > trq_th), 'DRV_FWD', df[op_quad])
    df[op_quad] = np.where((df[speed_rpm] > spd_th) & (df[t_measured] < trq_th), 'BRK_FWD', df[op_quad])
    df[op_quad] = np.where((df[speed_rpm] < spd_th) & (df[t_measured] < trq_th), 'DRV_REV', df[op_quad])
    df[op_quad] = np.where((df[speed_rpm] < spd_th) & (df[t_measured] > trq_th), 'BRK_REV', df[op_quad])

    # Rearrange data depending on quadrant.
    if (df[op_quad].any() == 'BRK_REV'):
        Meshgrid_Speed  = Meshgrid_Speed    *-1
        speed_bp        = speed_bp          *-1

    elif (df[op_quad].any() == 'BRK_FWD'):
        Meshgrid_Torque = Meshgrid_Torque   *-1
        torque_bp       = torque_bp         *-1
    elif (df[op_quad].any() == 'DRV_REV'):
        Meshgrid_Torque = Meshgrid_Torque   *-1
        torque_bp       = torque_bp         *-1
        Meshgrid_Speed  = Meshgrid_Speed    *-1
        speed_bp        = speed_bp          *-1

    else:
        pass

    return Meshgrid_Speed, Meshgrid_Torque, speed_bp, torque_bp

def loss_tables(df, speed_bp, torque_bp, Meshgrid_Speed, Meshgrid_Torque, speed_round, t_measured, loss_inv, loss_mtr_comp, loss_sys, method, fill):
    # Inverter losses
    Loss_Inv_Grid       = griddata( df.loc[ :, [speed_round,t_measured] ], df[loss_inv], (Meshgrid_Speed, Meshgrid_Torque), method=method,fill_value=fill)
    Loss_Inv_Table      = Loss_Inv_Grid[:, speed_bp]
    Loss_Inv_Table      = Loss_Inv_Table[torque_bp, :]

    # Motor losses
    Loss_Mtr_Grid       = griddata( df.loc[ :, [speed_round,t_measured] ], df[loss_mtr_comp], (Meshgrid_Speed, Meshgrid_Torque), method=method,fill_value=fill )
    Loss_Mtr_Table      = Loss_Mtr_Grid[:, speed_bp]
    Loss_Mtr_Table      = Loss_Mtr_Table[torque_bp, :]

    # System losses
    Loss_Sys_Grid       = griddata( df.loc[ :, [speed_round,t_measured] ], df[loss_sys], (Meshgrid_Speed, Meshgrid_Torque), method=method,fill_value=fill )
    Loss_Sys_Table      = Loss_Sys_Grid[:, speed_bp]
    Loss_Sys_Table      = Loss_Sys_Table[torque_bp, :]

    return Loss_Inv_Table, Loss_Mtr_Table, Loss_Sys_Table

def eff_tables():
    return

def mtr_loss_table_code(Loss_Mtr_Table):
    Loss_Mtr_Table_Code = pd.DataFrame(Loss_Mtr_Table)

    Loss_Mtr_Table_Code_Open = Loss_Mtr_Table_Code[0]
    Loss_Mtr_Table_Code_Open = '{'

    Loss_Mtr_Table_Code_Close = Loss_Mtr_Table_Code_Open
    Loss_Mtr_Table_Code_Close = '},'

    Loss_Mtr_Table_Code.loc[:,0:Loss_Mtr_Table_Code.shape[1]-2] = Loss_Mtr_Table_Code.applymap("{0:.2f},".format)

    Loss_Mtr_Table_Code.insert(0, 0, Loss_Mtr_Table_Code_Open, allow_duplicates = True)

    Loss_Mtr_Table_Code.columns = range(Loss_Mtr_Table_Code.shape[1])

    Loss_Mtr_Table_Code.insert(Loss_Mtr_Table_Code.shape[1], Loss_Mtr_Table_Code.shape[1], Loss_Mtr_Table_Code_Close, allow_duplicates=True)

    Loss_Mtr_Table_Code.loc[Loss_Mtr_Table_Code.shape[0]-1,Loss_Mtr_Table_Code.shape[1]-1] = '} '

    Loss_Mtr_Table_Code = Loss_Mtr_Table_Code.to_string( index = False, header = False, justify = "right" )

    return Loss_Mtr_Table_Code

# Convert Peak value to RMS value
def peak_2_rms(value_peak):
    value_rms = value_peak / np.sqrt(2)
    return value_rms

# Convert RMS value to Peak value
def rms_2_peak(value_rms):
    value_peak = value_rms * np.sqrt(2)
    return value_peak

# Convert rpm value to rad/s
def rpm_2_rads(speed_rpm):
    speed_rads = (speed_rpm / 60) * (2 * np.pi)
    return speed_rads

# Compute efficinecy in percentage
def eff_pc(output_value, input_value):
    eff_pc = (output_value/input_value) * 100
    return eff_pc

# Compute efficinecy in percentage
def error_pc(experimental_value, theoretical_value):
    error_pc = ( (experimental_value - theoretical_value) / theoretical_value )*100
    return error_pc

# Inverse Clarke's transformation.
def inverse_clarke(i_alpha, i_beta):
    i_a = i_alpha
    i_b = (-i_alpha + np.sqrt(3) * i_beta) / 2
    i_c = (-i_alpha - np.sqrt(3) * i_beta) / 2
    return i_a, i_b, i_c