import streamlit as st
import streamlit_authenticator as stauth
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
# conn = st.connection("gsheets", type=GSheetsConnection)
users_db = st.connection("usersDB", type=GSheetsConnection)
users_db = users_db.read(worksheet="users_db",usecols=list(range(4)))
users_db = users_db.dropna(how="all")

username = [users_db['user']for user in users_db]
password = [users_db['passwd'] for user in users_db]
mps = [users_db['mps_cps'] for user in users_db]


# Initialize Authenticator
authenticator = stauth.Authenticate(username, password, mps, "kp_cases_data_entry","123")

# ===========  Start FUNCTIONS  ====================

# def read_users_db(worksheet, usecols):
#     user_data = users_db.read(worksheet=worksheet, usecols=usecols)
#     user_data = user_data.dropna(how="all")
#     return user_data

# @st.cache_data(ttl=5)
# def read_data(worksheet, usecols):
#     data = conn.read(worksheet=worksheet, usecols=usecols)
#     data = data.dropna(how="all")
#     return data



# # Initialize Login
# if not authenticator.is_authenticated():
#     username, password = authenticator.login()
#     # Read the Users Database
#     read_user = read_users_db("users_db",list(range(4)))
#     user_exists = read_user['user'] == username
#     if user_exists.any():
#         correct_password = read_user.loc[user_exists, 'passwd'].values[0] == password
#         if correct_password:
#             ippo = read_user.loc[user_exists,'ppo_cpo'].values[0]
#             imps = read_user.loc[user_exists,'mps_cps'].values[0]
#             st.session_state.logged_in = True
#             st.session_state.username = username
#             st.write(f'Logged in as {username}')
#             st.switch_page("pages/entryCode.py")
#         else:
#             st.error('Incorrect password')
#     else:
#         st.error('User does not exist')
# else:
#     st.session_state.Appo
#     st.session_state.Amps

# Abrgy = []
