import streamlit as st
from datetime import datetime, date
import datetime
import traceback
from modules.helper import profile, process_offense, local_address, vic_name_process, db_conn, get_prov_data, get_muncity_data, get_brgy_data, get_crime_incidentName_data, get_crime_classification_data, store_data, convert_to_proper_time

st.set_page_config("New Entry")

# Initialize Connection to the database
conn = db_conn()

# HIDE NAVBAR and stFormSubmitButton
css ='''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

st.warning("""
           
           Please dont refresh the website to avoid resetting your encoded data \n 
           You can hover to question mark icons "❔" to learn more.
           
           """)

# Check if Appo and Amps are initialized in st.session_state
if 'Appo' not in st.session_state or 'Amps' not in st.session_state:
    # If not, redirect to app.py
    st.switch_page("app.py")
else:
    # If they are, continue with your code
    Appo = st.session_state.Appo
    Amps = st.session_state.Amps


    def validate_name(name):
        return name is not None and name != ""

    def validate_gender(gender):
        return gender is not None

    def validate_brgy(brgy):
        return brgy is not None

    def validate_date_reported(date):
        return date != datetime.date.today()

    def validate_offense(check, offenseType, otherOffense):
        if check:
            return otherOffense is not None and otherOffense != ""
        else:
            return offenseType is not None

    def validate_case_status(case_status):
        return case_status is not None



    def convert_time(time_str):
        try:
            return datetime.strptime(time_str, '%I:%M %p').time()
        except ValueError:
            st.error('Invalid time format. Please enter time in the format "HH\\:MM AM/PM".')
            return None
        
    # Get the Name of Barangays for Respective Mun/City with the Corresponding Provinces
    data = get_brgy_data(Appo, Amps)

    # Get the Offense Type with the Offense Classification
    offense = get_crime_incidentName_data()
    offenseKP = [item[0] for item in offense]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # vic_prof = read_data(str(Amps) + " - vic_prof", list(range(28)))
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Get the Province Value
    province_value = get_prov_data(Appo)

    # Get the Municipality Value and Barangay Value
    if Appo == "GENERAL SANTOS CPO":
        muncity_value = get_muncity_data(Appo)[0][0]  # Assuming the first value is the required one
        Abrgy = [item[0] for item in get_brgy_data(Appo, Amps)]  # Convert the result to a list

    else:
        muncity_value = get_muncity_data(Appo)[0][0]  # Assuming the first value is the required one
        Abrgy = [item[0] for item in get_brgy_data(Appo, Amps)]  # Convert the result to a list



    st.title('Katarungang Pambarangay Cases Detailed Report Encoding')
    st.title(f":red[{Amps} - {Appo}]")



    # Entry Number
    def entry_number():
        if 'combined_value' in st.session_state:
            entryNumber = st.text_input("Entry Number", str(st.session_state.combined_value), disabled=True)
            # Entry Form
            complainant, suspect, caseDetail, offense = st.tabs(["Complainant / Victim's Profile", "Suspect/s Profile", "Case Detail", "Offense"])

            with complainant:
                st.subheader("Victims's Profile")

                # First, Middle, and Last Name Portion
                fname, mname = st.columns(2)
                vic_fname = fname.text_input("First Name :red[#]",key="vic_fname")
                vic_midname = mname.text_input("Middle Name",key="vic_mname")
                vic_lname = st.text_input("Last Name :red[#]",key="vic_lname")

                if not vic_fname:
                    fname.warning('Please enter a first name.')
                if not vic_lname:
                    st.warning('Please enter a last name.')

                # Qualifier, Alias and Gender
                qlfr, alias, gndr= st.columns(3)
                vic_qlfr = qlfr.text_input("Qualifier",key="vic_qlfr")
                vic_alias = alias.text_input("Alias",key="vic_alias")
                with gndr:
                    vic_gndr = st.radio("Gender :red[#]",("Male", "Female"),index=None,horizontal=True,key="vic_gndr")

                if not vic_gndr:
                    gndr.warning('Please select a gender.')


                # Age Group
                ageGrp, age = st.columns(2)
                ageGrp.selectbox("Age Group",index=None,placeholder="Select Victims Age Group",options=("Infant (0-12 months)","Toddler (1-3 y/o)","Kid (4-9 y/o)","Preteen (10-12 y/o)","Teenager (13-18 y/o)","Young Adult (19-39 y/o)","Middle age Adult (40-64 y/o)","Old Age Adult (65 y/o-up)"),key="vic_ageGrp")
                vic_age = age.number_input("Estimated or Exact Age",step=1,min_value=0,key="vic_age")

                # Address - Region and Disttict/Province
                st.subheader("Victim's Address")
                region, distprov = st.columns(2)
                region.text_input("Region",value="Region XII",disabled=True,key="vic_region")
                vic_distprov = distprov.selectbox("District/Province",([province_value]),disabled=True,key="vic_distprov")

                # Address - RCity/Municipality, Barangay and House No/Street Name
                citymun, brgy = st.columns(2)
                vic_cityMun = citymun.selectbox("City/Municipality",([muncity_value]),disabled=True,key="vic_citymun")
                vic_brgy = brgy.selectbox("Barangay :red[#]",Abrgy,placeholder="Please select a Barangay",key="vic_abrgy",index=None)


                # Check if a Barangay was selected
                if vic_brgy == None:
                    st.warning("Please select a Barangay.")
                else:
                    vic_add_street = st.text_input("House No./Street Name",key="vic_strName")

                st.write("---")


            with suspect:
                st.subheader("Suspect's Profile")

                # First, Middle, and Last Name Portion
                fname, mname = st.columns(2)
                sus_fname = fname.text_input("First Name",key="sus_fname")
                sus_midname = mname.text_input("Middle Name",key="sus_mname")
                sus_lname = st.text_input("Last Name",key="sus_lname")

                # Qualifier, Alias and Gender
                qlfr, alias, gndr= st.columns(3)
                sus_qlfr = qlfr.text_input("Qualifier",key="sus_qlfr")
                sus_alias = alias.text_input("Alias",key="sus_alias")
                with gndr:
                    sus_gndr = st.radio("Gender",("Male", "Female"),index=None,horizontal=True,key="sus_gndr")

                # Age Group
                ageGrp, age = st.columns(2)
                ageGrp.selectbox("Age Group",index=None,placeholder="Select Victims Age Group",options=("Infant (0-12 months)","Toddler (1-3 y/o)","Kid (4-9 y/o)","Preteen (10-12 y/o)","Teenager (13-18 y/o)","Young Adult (19-39 y/o)","Middle age Adult (40-64 y/o)","Old Age Adult (65 y/o-up)"),key="sus_ageGrp")
                sus_age = age.number_input("Estimated or Exact Age",step=1,min_value=0,key="sus_age")

                # Address - Region and Disttict/Province
                st.subheader("Suspect's Address")
                region, distprov = st.columns(2)
                region.text_input("Region",value="Region XII",disabled=True,key="sus_region")
                sus_distprov = distprov.selectbox("District/Province",([province_value]),disabled=True,key="sus_distprov")

                # Address - RCity/Municipality, Barangay and House No/Street Name
                citymun, brgy = st.columns(2)
                sus_cityMun = citymun.selectbox("City/Municipality",([muncity_value]),disabled=True,key="sus_citymun")
                sus_brgy = brgy.selectbox("Barangay",Abrgy,placeholder="Please select a Barangay",key="sus_abrgy",index=None)
                sus_add_street = st.text_input("House No./Street Name",key="sus_strName")


                st.write("---")


            with caseDetail:

                det_narrative = st.text_area("Narrative")

                st.write("---")

                DTreported, DTcommitted = st.columns(2)
                with DTreported:
                    st.subheader("Date & Time Reported")
                    dt_reported = st.date_input("Date Reported :red[#]",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month", format="YYYY/MM/DD")
                    if dt_reported == datetime.date.today():
                        st.warning("Please change the Date Reported")
                    time_reported_str = st.text_input("Time Reported", placeholder='Time format 12:00 AM')
                    # Validate the time input
                    try:
                        valid_time = datetime.datetime.strptime(time_reported_str, '%I:%M %p')
                        st.success("Time input is valid.")
                    except ValueError:
                        st.error("Time input is not valid. Please enter time in the format 12:00 AM.")




                with DTcommitted:
                    st.subheader("Date & Time Committed")
                    dt_committed = st.date_input("Date Committed",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month",value=None, format="YYYY/MM/DD")
                    time_committed_str = st.text_input("Time Committed", placeholder='Time format 12:00 AM')
                    # time_committed = convert_time(time_committed_str)

                st.write("---")

                st.subheader("Place of Commission")
                region, distprov = st.columns(2)
                region.text_input("Region",value="Region XII",disabled=True,key="region")
                pi_distprov = distprov.selectbox("District/Province",([province_value]),disabled=True,key="distprov")

                # Address - RCity/Municipality, Barangay and House No/Street Name
                citymun, brgy = st.columns(2)
                pi_citymun = citymun.selectbox("City/Municipality",([muncity_value]),disabled=True,key="citymun")
                incident_selected_brgy = brgy.selectbox("Barangay :red[#]",Abrgy,placeholder="Please select a Barangay",key="abrgy",index=None)
                if incident_selected_brgy == None:
                    st.warning("Please select a Barangay.")

                # Check if a Barangay was selected
                pi_street = st.text_input("House No./Street Name",key="strName")

                st.write("---")


            with offense:
                generate_offense = offenseKP
                st.subheader("Offense :red[#]")
                offenseType_placeholder = st.empty()
                offenseType = offenseType_placeholder.selectbox("Select Offense :red[#]",generate_offense,index=None,placeholder="Please select an Offense")

                # Get the Incident Classification
                offClassification = ""
                offClassification_placeholder = st.empty()
                if offenseType != None:
                    offClassification = get_crime_classification_data(offenseType)
                    offClassification_placeholder.text_input("Offense Classification",offClassification,disabled=True)
                if offenseType == None:
                    offClassification_placeholder.warning("Please Select Offense")

                # Check if the Offense is not in the option
                check = st.checkbox("Tick the checkbox for Other Cases not found in Select Offense Dropdown above")
                otherOffense = ""
                if check:
                    offenseType_placeholder.empty()
                    offClassification_placeholder.empty()
                    otherOffense = st.text_input("Others, Please Specify :red[#]",help="Press Enter to confirm the Other KP Incident")

                    if not otherOffense:
                        st.warning("Please Type the Other Offense")

                st.subheader("Case Status")
                case_status = st.selectbox("Status of the Case :red[#]",("For Conciliation","Settled","For Record Purposes","With Certificate to File Action"),index=None)
                if case_status == None:
                    st.error("Please select Case Status.")
                st.write("---")
                
        else:
            st.error("No Entry Number Please click Home.")


        try:
            if not validate_name(vic_fname):
                st.error('Victim\'s First name is required.')
            if not validate_name(vic_lname):
                st.error('Victim\'s Last name is required.')
            if not validate_gender(vic_gndr):
                st.error('Victim\'s Gender is required.')
            if not validate_brgy(vic_brgy):
                st.error('Victim\'s Barangay address is required.')
            if not validate_date_reported(dt_reported):
                st.error("Please change the Date Reported")
            if not validate_brgy(incident_selected_brgy):
                st.error("Barangay in Place of Incident is Required.")
            if not validate_offense(check, offenseType, otherOffense):
                st.error('Please select an Offense')
            if not validate_case_status(case_status):
                st.error('Case status is required.')
            # Add time validation here
            if time_reported_str:
                try:
                    valid_time = datetime.datetime.strptime(time_reported_str, '%I:%M %p')
                except ValueError:
                    st.error("Time input is not valid. Please enter time in the format 12:00 AM.")

            if validate_name(vic_fname) and validate_name(vic_lname) and validate_gender(vic_gndr) and validate_brgy(vic_brgy) and validate_date_reported(dt_reported) and validate_brgy(incident_selected_brgy) and validate_offense(check, offenseType, otherOffense) and validate_case_status(case_status) and (not time_reported_str or valid_time):

                sub_Entry = st.button("Submit Entry",use_container_width=True, type="primary")
                if sub_Entry:
                    # Fuction to encode data google sheet
                    print(f"{entryNumber} Entry Successfuly Submitted")
                    # print(dt_reported)

                    # Process Victims profile
                    vic_name = profile(vic_fname,vic_midname,vic_lname,vic_qlfr, vic_alias,vic_age,vic_gndr)
                    # Process Victim's Address
                    vic_address = local_address(vic_add_street, vic_brgy, vic_cityMun, vic_distprov)


                    # Process Suspects profile
                    sus_name = profile(sus_fname,sus_midname,sus_lname,sus_qlfr, sus_alias,sus_age,sus_gndr)
                    # Process Suspect's Address
                    sus_address = local_address(sus_add_street, sus_brgy, sus_cityMun, sus_distprov)

                    # Process Offense
                    offense_Type, offenseClass = process_offense(offenseType,otherOffense,offClassification)

                    # Process Victims profile
                    vic_fname,vic_midname,vic_lname,vic_qlfr, vic_alias,vic_age,vic_gndr = vic_name_process(vic_fname,vic_midname,vic_lname,vic_qlfr, vic_alias,vic_age,vic_gndr)

                    # Process Offense
                    offense_Type, offenseClass = process_offense(offenseType,otherOffense,offClassification)

                    time_reported, time_committed = convert_to_proper_time(time_reported_str,time_committed_str)


                    # Start adding the newEntry data on the on the existing data
                    store_data(entryNumber, pi_distprov, pi_citymun, incident_selected_brgy, pi_street,dt_reported,time_reported_str,dt_committed,time_committed_str,vic_name,vic_fname,vic_midname,vic_lname,vic_qlfr,vic_alias,vic_age,vic_gndr,vic_distprov,vic_cityMun,vic_add_street, vic_address, sus_name, sus_address, offense_Type, offenseClass, det_narrative,case_status)


                    # store_data(entryNumber, pi_distprov)

                    st.success('Entry Successfuly Submitted')
                    # time.sleep(3)
                    # st.balloons
                    # st.cache_data.clear()
                    # st.switch_page("pages/entryCode.py")
                    

        except Exception as e:

            st.error(f"An error occurred: Error Details: {str(e)}\n{traceback.format_exc()}")


    # This line of code handles the entry form and I don't know why 😂
    entry_number()


footer_html = """
<style>
.sticky-footer {
    position="fixed",
    bottom=0,
    width: 100%;
    color="black",
    text_align="center",
    opacity=1
}
.center-div {
    display: grid;
    place-items: center;
}
</style>
<div class='sticky-footer center-div'>
    <p>Developed by Rafael Villanueva 🤙🏻🤘🏻🎉</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

