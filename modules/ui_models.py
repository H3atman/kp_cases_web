import streamlit as st
from datetime import datetime

@st.experimental_dialog("Input the time",width="medium")
def input_time_reported():
    hr, min , ampm = st.columns(3)
    hour = hr.number_input("Hour",step=1,min_value=1,max_value=12)
    minutes = min.number_input("Minutes",step=1,min_value=1,max_value=59,format="%02d")
    time_class = ampm.selectbox("AM/PM",options=("AM","PM"))
    timevalue = "{}:{} {}".format(hour,minutes,time_class)
    if st.button("Submit",type="primary"):
        # Convert the timevalue to a datetime object
        dt = datetime.strptime(timevalue, "%I:%M %p")
        st.session_state.input_time_reported = {"timevalue":dt}
        st.rerun()


@st.experimental_dialog("Input the time",width="medium")
def input_time_committed():
    hr, min , ampm = st.columns(3)
    hour = hr.number_input("Hour",step=1,min_value=1,max_value=12)
    minutes = min.number_input("Minutes",step=1,min_value=1,max_value=59,format="%02d")
    time_class = ampm.selectbox("AM/PM",options=("AM","PM"))
    timevalue = "{}:{} {}".format(hour,minutes,time_class)
    if st.button("Submit",type="primary"):
        # Convert the timevalue to a datetime object
        dt = datetime.strptime(timevalue, "%I:%M %p")
        st.session_state.input_time_committed = {"timevalue":dt}
        st.rerun()

# if "input_time" not in st.session_state:
#     st.write("Test")
# else:
#     st.write("Test 2")



# if "input_time" not in st.session_state:
#     DTreported, DTcommitted = st.columns(2)
#     with DTreported:
#         st.date_input("Date Reported")
#         col1 , col2 = st.columns(2)
#         col1.text_input("Time Reported")
#         col2.write("\n")
#         col2.write("\n")
#         if col2.button("Enter Time",use_container_width=True):
#             input_time()
# else:
#     DTreported, DTcommitted = st.columns(2)
#     with DTreported:
#         st.date_input("Date Reported")
#         col1 , col2 = st.columns(2)
#         # Format the datetime object to a string representing time in the "%I:%M %p" format
#         time_str = st.session_state.input_time["timevalue"].strftime("%I:%M %p")
#         col1.text_input("Time Reported",value=time_str,disabled=True)
#         col2.write("\n")
#         col2.write("\n")
#         if col2.button("Enter Time",use_container_width=True):
#             input_time()
