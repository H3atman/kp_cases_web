import streamlit as st
from app import read_data, Appo, Amps
from datetime import date

# Fomat the dates
def dateseq():
    # Get the current date
    current_date = date.today()

    # Format the date to 'YYYYMM'
    formatted_date = current_date.strftime('%Y%m')

    return formatted_date

# Get the Station Sequence
entry_seq = read_data("station_seq", list(range(3)))

def new_entry_page(entry_seq, Amps):
    st.title('Katarungang Pambarangay Cases Detailed Report Encoding')
    st.title(f":red[{Amps} - {Appo}]")
    # Get the Blotter Sequence
    entry_seq = entry_seq.loc[entry_seq['mps_cps'] == Amps, 'seq'].values[0]

    entrySeq, dateMon, monthRep ,entryNum = st.columns(4)

    entrySeq_value = entrySeq.text_input("Station Code", entry_seq, disabled=True, key="AentrySeq")

    dateMon_value = dateMon.text_input("Year|Month",dateseq(), disabled=True)

    monthRep_value = monthRep.number_input("Year|Month 'YYYYMM'",help="Enter the YEAR and MONTH the KP Incident is Reported (e.g 202105, 202212)",step=1,min_value=202101,max_value=202412)

    entryNum_value = entryNum.number_input("Entry Number :red[#]",step=1,min_value=1)

    combined_value = "{}-{}-{}-{}".format(entrySeq_value, dateMon_value, monthRep_value, entryNum_value)

    return entryNum_value, combined_value

if 'logged_in' in st.session_state and st.session_state.logged_in:
    entryNum, combined_value = new_entry_page(entry_seq, Amps)

    # Save combined_value in session state
    if 'combined_value' not in st.session_state:
        st.session_state.combined_value = combined_value
    else:
        st.session_state.combined_value = combined_value

    if st.button("New Entry",type="primary",use_container_width=True):
        st.switch_page("pages/entryForm.py")