import streamlit as st
import getpass

def trq_report_details():

    controller_manfactures = [
        "Turntide",
        "Avid",
        "Cascadia",
        "BorgWarner",
        "Other",
    ]

    turntide_controllers = [
        "Gen 5 Oxford",
        "Gen 5",
        "Gen 4 Size 10",
        "Gen 4 Size 8"
    ]

    avid_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    cascadia_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    borgwarner_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    samples = [
        "A0",
        "A1",
        "A2",
        "A3",
        "A4",
        "B0",
        "B1",
        "B2",
        "B3",
        "B4",
        "C0",
        "C1",
        "C2",
        "C3",
        "C4",
        "D0",
        "D1",
        "D2",
        "D3",
        "D4",
    ]

    motor_manufactures = [
        "Turntide",
        "Yasa",
        "Intergral Powertrain",
        "Other"
    ]

    turntide_motors = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    yasa_motors = [
        "Oxford"
    ]

    ipt_motors = [
        "Bowfell",
    ]

    dynos = [
        "Dyno 1",
        "Dyno 2",
        "Dyno 3",
        "Dyno 4",
        "Dyno 5",
        "Dyno 6",
        "Other"
    ]

    sw_levels = [
        "Branch",
        "Tag",
        "Trunk",
        "Release Candidate",
        "Other"
    ]

    torque_speed_sensors =[
        "HBM T40 (SN:XX)",
        "HBM T20 (SN:XX)",
        "Sensor Technologies (SN:XX)"
    ]

    test_name, user, date               = st.columns(3)

    #Report Details
    test_name.text_input("Test Name", key = "Test Name")
    user.text_input("User", value = getpass.getuser(), key = "User")
    date.date_input("Date", key = "Test Date")
    st.text_area("Test Notes", key = "Test Note")

    dyno_fields, software_fields            = st.columns(2)

    #Dyno
    dyno_fields.subheader("Dyno")
    dyno_fields.selectbox("Dyno", dynos, key = "Dyno")
    dyno_fields.selectbox("Torque Speed Sensor",torque_speed_sensors, key = "Torque Speed Sensor")
    dyno_fields.date_input("Date", key = "Sensor Calibration Date")

    #Software
    software_fields.subheader("Software")
    software_fields.selectbox("Level", sw_levels, key = "Software Level")
    software_fields.text_input("Location", key = "Software Location")
    software_fields.text_area("Notes", key = "Software Notes")

    controller_field, motor_field   = st.columns(2)

    #Controllers
    controller_field.subheader("Controller")
    controller_field.selectbox("Manufacturer", controller_manfactures, key = "Controller Manufacturer")

    if st.session_state["Controller Manufacturer"] == 'Turntide':
        controller_field.selectbox("Model", turntide_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Avid':
        controller_field.selectbox("Model", avid_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Borgwarner':
        controller_field.selectbox("Model", borgwarner_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Cascadia':
        controller_field.selectbox("Model", cascadia_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Other':
        controller_field.text_input("Model")

    controller_field.selectbox("Sample", samples, key = "Controller Sample")
    controller_field.text_area("Notes", key = "Controller Notes")

    #Motors
    motor_field.subheader("Motor")
    motor_field.selectbox("Manufacturer", motor_manufactures, key = "Motor Manufacturer")

    if st.session_state["Motor Manufacturer"] == 'Turntide':
        motor_field.selectbox("Model", turntide_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Yasa':
        motor_field.selectbox("Model", yasa_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Intergral Powertrain':
        motor_field.selectbox("Model", ipt_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Other':
        motor_field.text_input("Model")

    motor_field.selectbox("Sample", samples, key = "Motor Sample")
    motor_field.text_area("Notes", key = "Motor Notes")

    return


def limits(analysis_toggle):

    if analysis_toggle == "Output":
        st.subheader("Output Limits")
        st.number_input("QM Limit [Nm]",      min_value = -100.0, max_value = 100.0, value = 5.0, step = 1.0, key = "Output Limit [Nm]")
        st.number_input("QM Limit [%]",       min_value = -100.0, max_value = 100.0, value = 5.0, step = 1.0, key = "Output Limit [%]")

    else:
        col_output, col_estimated = st.columns(2)
        col_output.subheader("Output Limits")
        col_output.number_input("Output Limit [Nm]",      min_value = -100.0, max_value = 100.0, value = 5.0, step = 1.0, key = "Output Limit [Nm]")
        col_output.number_input("Output Limit [%]",       min_value = -100.0, max_value = 100.0, value = 5.0, step = 1.0, key = "Output Limit [%]")
        col_estimated.subheader("Estimated Limits")
        col_estimated.number_input("Estimated Limit [Nm]",   min_value = -100.0, max_value = 100.0, value = 5.0, step = 1.0, key = "Estimated Limit [Nm]")
        col_estimated.number_input("Estimated Limit [%]",    min_value = -100.0, max_value = 100.0, value = 5.0, step = 1.0, key = "Estimated Limit [%]")
    return

def limit_format(flag, min, average, max, limit, unit):
    if min > st.session_state[limit + " Limit [" + unit + "]"] and flag == False:
        min_error_display = '<p style="font-family:sans-serif; color:Red; font-size: 24px;">'+str(round(min, 3)) + unit +'</p>'
    else:
        min_error_display = '<p style="font-family:sans-serif; color:Green; font-size: 24px;">'+str(round(min, 3))+ unit +'</p>'

    if average > st.session_state[limit + " Limit [" + unit + "]"] and flag == False:
        avg_error_display = '<p style="font-family:sans-serif; color:Red; font-size: 24px;">'+str(round(average, 3)) + unit +'</p>'
    else:
        avg_error_display = '<p style="font-family:sans-serif; color:Green; font-size: 24px;">'+str(round(average, 3))+ unit +'</p>'

    if max > st.session_state[limit + " Limit [" + unit + "]"] and flag == False:
        max_error_display = '<p style="font-family:sans-serif; color:Red; font-size: 24px;">'+str(round(max, 3)) + unit +'</p>'
    else:
        max_error_display = '<p style="font-family:sans-serif; color:Green; font-size: 24px;">'+str(round(max, 3))+ unit +'</p>'

    return min_error_display, avg_error_display, max_error_display

def mtr_loss_report_details():

    controller_manfactures = [
        "Turntide",
        "Avid",
        "Cascadia",
        "BorgWarner",
        "Other",
    ]

    turntide_controllers = [
        "Gen 5 Oxford",
        "Gen 5",
        "Gen 4 Size 10",
        "Gen 4 Size 8"
    ]

    avid_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    cascadia_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    borgwarner_controllers = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    samples = [
        "A0",
        "A1",
        "A2",
        "A3",
        "A4",
        "B0",
        "B1",
        "B2",
        "B3",
        "B4",
        "C0",
        "C1",
        "C2",
        "C3",
        "C4",
        "D0",
        "D1",
        "D2",
        "D3",
        "D4",
    ]

    motor_manufactures = [
        "Turntide",
        "Yasa",
        "Intergral Powertrain",
        "Other"
    ]

    turntide_motors = [
        "Placeholder A",
        "Placeholder B",
        "Placeholder C"
    ]

    yasa_motors = [
        "Oxford"
    ]

    ipt_motors = [
        "Bowfell",
    ]

    dynos = [
        "Dyno 1",
        "Dyno 2",
        "Dyno 3",
        "Dyno 4",
        "Dyno 5",
        "Dyno 6",
        "Other"
    ]

    sw_levels = [
        "Branch",
        "Tag",
        "Trunk",
        "Release Candidate",
        "Other"
    ]

    torque_speed_sensors =[
        "HBM T40 (SN:XX)",
        "HBM T20 (SN:XX)",
        "Sensor Technologies (SN:XX)"
    ]

    test_name, user, date               = st.columns(3)

    #Report Details
    test_name.text_input("Test Name", key = "Test Name")
    user.text_input("User", value = getpass.getuser(), key = "User")
    date.date_input("Date", key = "Test Date")
    st.text_area("Test Notes", key = "Test Note")

    dyno_fields, software_fields            = st.columns(2)

    #Dyno
    dyno_fields.subheader("Dyno")
    dyno_fields.selectbox("Dyno", dynos, key = "Dyno")
    dyno_fields.selectbox("Torque Speed Sensor",torque_speed_sensors, key = "Torque Speed Sensor")
    dyno_fields.date_input("Date", key = "Sensor Calibration Date")

    #Software
    software_fields.subheader("Software")
    software_fields.selectbox("Level", sw_levels, key = "Software Level")
    software_fields.text_input("Location", key = "Software Location")
    software_fields.text_area("Notes", key = "Software Notes")

    controller_field, motor_field   = st.columns(2)

    #Controllers
    controller_field.subheader("Controller")
    controller_field.selectbox("Manufacturer", controller_manfactures, key = "Controller Manufacturer")

    if st.session_state["Controller Manufacturer"] == 'Turntide':
        controller_field.selectbox("Model", turntide_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Avid':
        controller_field.selectbox("Model", avid_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Borgwarner':
        controller_field.selectbox("Model", borgwarner_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Cascadia':
        controller_field.selectbox("Model", cascadia_controllers, key = "Controller Model")

    elif st.session_state["Controller Manufacturer"] == 'Other':
        controller_field.text_input("Model")

    controller_field.selectbox("Sample", samples, key = "Controller Sample")
    controller_field.text_area("Notes", key = "Controller Notes")

    #Motors
    motor_field.subheader("Motor")
    motor_field.selectbox("Manufacturer", motor_manufactures, key = "Motor Manufacturer")

    if st.session_state["Motor Manufacturer"] == 'Turntide':
        motor_field.selectbox("Model", turntide_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Yasa':
        motor_field.selectbox("Model", yasa_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Intergral Powertrain':
        motor_field.selectbox("Model", ipt_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Other':
        motor_field.text_input("Model")

    motor_field.selectbox("Sample", samples, key = "Motor Sample")
    motor_field.text_area("Notes", key = "Motor Notes")

    #Motors
    motor_field.subheader("Motor")
    motor_field.selectbox("Manufacturer", motor_manufactures, key = "Motor Manufacturer")

    if st.session_state["Motor Manufacturer"] == 'Turntide':
        motor_field.selectbox("Model", turntide_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Yasa':
        motor_field.selectbox("Model", yasa_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Intergral Powertrain':
        motor_field.selectbox("Model", ipt_motors, key = "Motor Model")

    elif st.session_state["Motor Manufacturer"] == 'Other':
        motor_field.text_input("Model")

    motor_field.selectbox("Sample", samples, key = "Motor Sample")
    motor_field.text_area("Notes", key = "Motor Notes")

    return