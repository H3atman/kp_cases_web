import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config("KP Cases Detailed Entry")

# HIDE NAVBAR and stFormSubmitButton
css ='''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# Start the connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
users_db = st.connection("usersDB", type=GSheetsConnection)

# ===========  Start FUNCTIONS  ====================

def read_users_db(worksheet, usecols):
    user_data = users_db.read(worksheet=worksheet, usecols=usecols)
    user_data = user_data.dropna(how="all")
    return user_data

@st.cache_data(ttl=5)
def read_data(worksheet, usecols):
    data = conn.read(worksheet=worksheet, usecols=usecols)
    data = data.dropna(how="all")
    return data


def login():
    login_placeholder = st.empty()
    with login_placeholder.form(key="login",clear_on_submit=True):
        st.title("KP Cases Encoding Users Login")
        username = st.text_input("Username")
        passwd = st.text_input("Password",type="password")
        # Read the Users Database
        read_user = read_users_db("users_db",list(range(4)))
        ippo = None
        imps = None
        if username:  # Check if username is not empty
            user_exists = read_user['user'] == username
            if user_exists.any():
                correct_password = read_user.loc[user_exists, 'passwd'].values[0] == passwd
                if correct_password:
                    ippo = read_user.loc[user_exists,'ppo_cpo'].values[0]
                    imps = read_user.loc[user_exists,'mps_cps'].values[0]
                    st.session_state.logged_in = True
                    st.session_state.username = username
                else:
                    st.error('Incorrect password')
            else:
                st.error('User does not exist')
        if st.form_submit_button("Login",type="primary"):
            if 'logged_in' in st.session_state and st.session_state.logged_in:
                st.write(f'Logged in as {username}')
                st.switch_page("pages/entryCode.py")
                # login_placeholder.empty()  # Clear the login form
        return ippo, imps

# Initialize Login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    Appo, Amps = login()
else:
    st.session_state.Appo
    st.session_state.Amps

Abrgy = []

# # Get the Station Sequence
# entry_seq = read_data("station_seq", list(range(3)))

# def new_entry_page(entry_seq, Amps):
#     st.title('Katarungang Pambarangay Cases Detailed Report Encoding')
#     st.title(f":red[{Amps} - {Appo}]")
#     # Get the Blotter Sequence
#     entry_seq = entry_seq.loc[entry_seq['mps_cps'] == Amps, 'seq'].values[0]

#     entrySeq, dateMon, monthRep ,entryNum = st.columns(4)

#     entrySeq_value = entrySeq.text_input("Station Code", entry_seq, disabled=True, key="AentrySeq")

#     dateMon_value = dateMon.text_input("Year|Month",dateseq(), disabled=True)

#     monthRep_value = monthRep.number_input("Year|Month 'YYYYMM'",help="Enter the YEAR and MONTH the KP Incident is Reported (e.g 202105, 202212)",step=1,min_value=202101,max_value=202412)

#     entryNum_value = entryNum.number_input("Entry Number :red[#]",step=1,min_value=1)

#     combined_value = "{}-{}-{}-{}".format(entrySeq_value, dateMon_value, monthRep_value, entryNum_value)

#     return entryNum_value, combined_value

# if 'logged_in' in st.session_state and st.session_state.logged_in:
#     entryNum, combined_value = new_entry_page(entry_seq, Amps)

#     # Save combined_value in session state
#     if 'combined_value' not in st.session_state:
#         st.session_state.combined_value = combined_value
#     else:
#         st.session_state.combined_value = combined_value

#     if st.button("New Entry",type="primary",use_container_width=True):
#         st.switch_page("pages/entryForm.py")
