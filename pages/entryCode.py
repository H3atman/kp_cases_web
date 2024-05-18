import streamlit as st
from app import db_conn
from datetime import date

st.set_page_config("KP Cases Detailed Entry")

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
           You can hover to question mark icons "❔" to know more.
           
           """)

# Check if Appo and Amps are initialized in st.session_state
if 'Appo' not in st.session_state or 'Amps' not in st.session_state:
    # If not, redirect to app.py
    st.switch_page("app.py")
else:
    # If they are, continue with your code
    Appo = st.session_state.Appo
    Amps = st.session_state.Amps

    # Fomat the dates
    def dateseq():
        # Get the current date
        current_date = date.today()

        # Format the date to 'YYYYMM'
        formatted_date = current_date.strftime('%Y%m')

        return formatted_date

    # Get the Station Sequence
    def entry_seq(Amps):
        cursor = conn.cursor()
        cursor.execute("SELECT seq FROM station_sequence WHERE mps_cps = %s ", ( Amps,))
        entry_seq = cursor.fetchone()
        if entry_seq is not None:
            return entry_seq[0]  # Return the first element of the tuple
        else:
            return None  # Or handle the case where no result is found as you see fit

    # Store the Entry Sequence to a variable
    seq = entry_seq(Amps)

    def new_entry():
        st.title('Katarungang Pambarangay Cases Detailed Report Encoding')
        st.title(f":red[{Amps} - {Appo}]")
        # # Get the Blotter Sequence
        # entry_seq = entry_seq.loc[entry_seq['mps_cps'] == Amps, 'seq'].values[0]

        entrySeq, dateMon, monthRep ,entryNum = st.columns(4)

        entrySeq_value = entrySeq.text_input("Station Code", seq, disabled=True)

        dateMon_value = dateMon.text_input("Year|Month",dateseq(), disabled=True)

        monthRep_value = monthRep.number_input("Year|Month 'YYYYMM'",help="Enter the YEAR and MONTH the KP Incident is Reported (e.g 202105, 202212)",step=1,min_value=202101,max_value=202412)

        # I want the entry number to auto suggest for the next entry based on the existing encoded number 
        entryNum_value = entryNum.number_input("Entry Number :red[#]",step=1,min_value=1)

        combined_value = "{}-{}-{}-{}".format(entrySeq_value, dateMon_value, monthRep_value, entryNum_value)

        

        return combined_value


    fullentryNum = new_entry()

    # Save combined_value in session state
    if 'combined_value' not in st.session_state:
        st.session_state.combined_value = fullentryNum
    else:
        st.session_state.combined_value = fullentryNum

    if st.button("New Entry",type="primary",use_container_width=True):
        # print(fullentryNum)
        st.switch_page("pages/entryForm.py")
