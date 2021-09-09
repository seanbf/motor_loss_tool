import numpy as np
import streamlit as st
import pandas as pd

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

# Round to nearest base input
def custom_round(x, base):
    return int(base * round(float(x)/base))

@st.cache
def load_dataframe(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
    except:
        df = pd.read_excel(uploaded_file)

    columns = list(df.columns)
    columns.append(None)

    return df, columns