import streamlit as st
from datetime import datetime, date
import datetime
from app import read_data

st.set_page_config("New Entry")

# HIDE NAVBAR and stFormSubmitButton
css ='''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

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

def dateseq():
    # Get the current date
    current_date = date.today()

    # Format the date to 'YYYYMM'
    formatted_date = current_date.strftime('%Y%m')

    return formatted_date


Appo = "GENERAL SANTOS CPO"
Amps = "PS 03"
Abrgy = []


data = read_data("RXII_Barangay", list(range(5)))
offenseKP = read_data("offense", list(range(2)))


# Get the Province Value
province_value = data.loc[data['PPO'] == Appo, 'Province'].values[0]

# Get the Municipality Value and Barangay Value
if Appo == "GENERAL SANTOS CPO":
    muncity_value = data.loc[data['MPS_CPS'] == Amps, 'MPS_CPS'].values[0]
    Abrgy = data.loc[data['MPS_CPS'] == muncity_value, 'Barangay'].tolist()

else:
    muncity_value = data.loc[data['MPS_CPS'] == Amps, 'Municipality_City'].values[0]
    Abrgy = data.loc[data['Municipality_City'] == muncity_value, 'Barangay'].tolist()


st.title('Katarungang Pambarangay Cases Detailed Report Encoding')
st.title(f":red[{Amps} - {Appo}]")



# Entry Number
def entry_number():
    if 'combined_value' in st.session_state:
        st.text_input("Entry Number", str(st.session_state.combined_value), disabled=True)
        # Entry Form
        complainant, suspect, caseDetail, offense = st.tabs(["Complainant / Victim's Profile", "Suspect/s Profile", "Case Detail", "Offense"])

        with complainant:
            st.subheader("Victims's Profile")

            # First, Middle, and Last Name Portion
            fname, mname = st.columns(2)
            vic_fname = fname.text_input("First Name :red[#]",key="vic_fname")
            mname.text_input("Middle Name",key="vic_mname")
            vic_lname = st.text_input("Last Name :red[#]",key="vic_lname")

            if not vic_fname:
                fname.warning('Please enter a first name.')
            if not vic_lname:
                st.warning('Please enter a last name.')

            # Qualifier, Alias and Gender
            qlfr, alias, gndr= st.columns(3)
            qlfr.text_input("Qualifier",key="vic_qlfr")
            alias.text_input("Alias",key="vic_alias")
            with gndr:
                vic_gndr = st.radio("Gender :red[#]",("Male", "Female"),index=None,horizontal=True,key="vic_gndr")

            if not vic_gndr:
                gndr.warning('Please select a gender.')


            # Age Group
            ageGrp, age = st.columns(2)
            ageGrp.selectbox("Age Group",index=None,placeholder="Select Victims Age Group",options=("Infant (0-12 months)","Toddler (1-3 y/o)","Kid (4-9 y/o)","Preteen (10-12 y/o)","Teenager (13-18 y/o)","Young Adult (19-39 y/o)","Middle age Adult (40-64 y/o)","Old Age Adult (65 y/o-up)"),key="vic_ageGrp")
            age.number_input("Estimated or Exact Age",step=1,min_value=0,key="vic_age")

            # Address - Region and Disttict/Province
            st.subheader("Victim's Address")
            region, distprov = st.columns(2)
            region.text_input("Region",value="Region XII",disabled=True,key="vic_region")
            distprov.selectbox("District/Province",([province_value]),disabled=True,key="vic_distprov")

            # Address - RCity/Municipality, Barangay and House No/Street Name
            citymun, brgy = st.columns(2)
            citymun.selectbox("City/Municipality",([muncity_value]),disabled=True,key="vic_citymun")
            Vselected_brgy = brgy.selectbox("Barangay :red[#]",Abrgy,placeholder="Please select a Barangay",key="vic_abrgy",index=None)


            # Check if a Barangay was selected
            if Vselected_brgy == None:
                st.warning("Please select a Barangay.")
            else:
                st.text_input("House No./Street Name",key="vic_strName")

            st.write("---")


        with suspect:
            st.subheader("Suspect's Profile")

            # First, Middle, and Last Name Portion
            fname, mname = st.columns(2)
            fname.text_input("First Name",key="sus_fname")
            mname.text_input("Middle Name",key="sus_mname")
            st.text_input("Last Name",key="sus_lname")

            # Qualifier, Alias and Gender
            qlfr, alias, gndr= st.columns(3)
            qlfr.text_input("Qualifier",key="sus_qlfr")
            alias.text_input("Alias",key="sus_alias")
            with gndr:
                st.radio("Gender",("Male", "Female"),index=None,horizontal=True,key="sus_gndr")

            # Age Group
            ageGrp, age = st.columns(2)
            ageGrp.selectbox("Age Group",index=None,placeholder="Select Victims Age Group",options=("Infant (0-12 months)","Toddler (1-3 y/o)","Kid (4-9 y/o)","Preteen (10-12 y/o)","Teenager (13-18 y/o)","Young Adult (19-39 y/o)","Middle age Adult (40-64 y/o)","Old Age Adult (65 y/o-up)"),key="sus_ageGrp")
            age.number_input("Estimated or Exact Age",step=1,min_value=0,key="sus_age")

            # Address - Region and Disttict/Province
            st.subheader("Suspect's Address")
            region, distprov = st.columns(2)
            region.text_input("Region",value="Region XII",disabled=True,key="sus_region")
            distprov.selectbox("District/Province",([province_value]),disabled=True,key="sus_distprov")

            # Address - RCity/Municipality, Barangay and House No/Street Name
            citymun, brgy = st.columns(2)
            citymun.selectbox("City/Municipality",([muncity_value]),disabled=True,key="sus_citymun")
            brgy.selectbox("Barangay",Abrgy,placeholder="Please select a Barangay",key="sus_abrgy",index=None)
            st.text_input("House No./Street Name",key="sus_strName")


            st.write("---")


        with caseDetail:

            st.text_area("Narrative")

            st.write("---")

            DTreported, DTcommitted = st.columns(2)
            with DTreported:
                st.subheader("Date & Time Reported")
                dt_reported = st.date_input("Date Reported :red[#]",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month")
                if dt_reported == datetime.date.today():
                    st.warning("Please change the Date Reported")
                time_reported_str = st.text_input("Time Reported", placeholder='Time format 12:00 AM')




            with DTcommitted:
                st.subheader("Date & Time Committed")
                st.date_input("Date Committed",help="If di po available sa data ang exact date reported paki pili nalang po ang 1st day of the month",value=None)
                time_committed_str = st.text_input("Time Committed", placeholder='Time format 12:00 AM')
                # time_committed = convert_time(time_committed_str)

            st.write("---")

            st.subheader("Place of Commission")
            region, distprov = st.columns(2)
            region.text_input("Region",value="Region XII",disabled=True,key="region")
            distprov.selectbox("District/Province",([province_value]),disabled=True,key="distprov")

            # Address - RCity/Municipality, Barangay and House No/Street Name
            citymun, brgy = st.columns(2)
            citymun.selectbox("City/Municipality",([muncity_value]),disabled=True,key="citymun")
            incident_selected_brgy = brgy.selectbox("Barangay :red[#]",Abrgy,placeholder="Please select a Barangay",key="abrgy",index=None)
            if incident_selected_brgy == None:
                st.warning("Please select a Barangay.")

            # Check if a Barangay was selected
            st.text_input("House No./Street Name",key="strName")

            st.write("---")


        with offense:
            generate_offense = offenseKP['incidents'].values
            st.subheader("Offense :red[#]")
            offenseType_placeholder = st.empty()
            offenseType = offenseType_placeholder.selectbox("Select Offense :red[#]",generate_offense,index=None,placeholder="Please select an Offense")

            # Get the Incident Classification
            offClassification_placeholder = st.empty()
            if offenseType != None:
                offClassification = offenseKP.loc[offenseKP['incidents'] == offenseType, 'classification'].values[0]
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
            


            # otherOffense = ""
            try:
                if not validate_name(vic_fname):
                    st.error('Victim\'s First name is required.')
                if not validate_name(vic_lname):
                    st.error('Victim\'s Last name is required.')
                if not validate_gender(vic_gndr):
                    st.error('Victim\'s Gender is required.')
                if not validate_brgy(Vselected_brgy):
                    st.error('Victim\'s Barangay address is required.')
                if not validate_date_reported(dt_reported):
                    st.error("Please change the Date Reported")
                if not validate_brgy(incident_selected_brgy):
                    st.error("Barangay in Place of Incident is Required.")
                if not validate_offense(check, offenseType, otherOffense):
                    st.error('Please select an Offense')
                if not validate_case_status(case_status):
                    st.error('Case status is required.')

                if validate_name(vic_fname) and validate_name(vic_lname) and validate_gender(vic_gndr) and validate_brgy(Vselected_brgy) and validate_date_reported(dt_reported) and validate_brgy(incident_selected_brgy) and validate_offense(check, offenseType, otherOffense) and validate_case_status(case_status):
                    sub_Entry = st.button("Submit Entry",use_container_width=True, type="primary")
                    if sub_Entry:
                        print("Entry Successfuly Submitted")


            except Exception as e:

                st.error(f"An error occurred: Please select and Offense in the Dropdown Menu. Error Details: {str(e)}")

            # otherOffense = ""
            # try:
            #     if not vic_fname:
            #         st.error('First name is required.')
            #     if not vic_lname:
            #         st.error('Last name is required.')
            #     if vic_gndr is None:
            #         st.error('Gender is required.')
            #     if Vselected_brgy is None:
            #         st.error('Victim\'s Barangay address is required.')
            #     if dt_reported == datetime.date.today():
            #         st.error("Please change the Date Reported")
            #     if incident_selected_brgy == None:
            #         st.error("Place of Incident Barangay is Required.")
            #     if not check and offenseType is None:
            #         st.error('Please select an Offense')
            #     if check and  otherOffense is not "":
            #         st.error('Please type the Other Case Type.')
            #     if case_status is None:
            #         st.error('Case status is required.')

            #     if vic_fname is not None and vic_lname is not None and vic_gndr is not None and Vselected_brgy is not None and ((not check and offenseType is not None) or (check and otherOffense is not "" )) and case_status is not None:
            #         sub_Entry = st.button("Submit Entry",use_container_width=True, type="primary")
            #         if sub_Entry:
            #             print("Entry Successfuly Submitted")

            # except Exception as e:

            #     st.error(f"An error occurred: Please select and Offense in the Dropdown Menu. Error Details: {str(e)}")

    else:
        st.error("No Entry Number Please click Home.")


# This line of code handles the entry form and I don't know why 😂
entry_number()

