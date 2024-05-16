import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
# from datetime import date
import hashlib

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

# Hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Start the connection to Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)
users_db = st.connection("usersDB", type=GSheetsConnection)
@st.cache_data(ttl=60)
def read_data(worksheet, usecols):
    data = users_db.read(worksheet=worksheet, usecols=usecols)
    data = data.dropna(how="all")
    return data

users = read_data("users_db", list(range(5)))

# # Initialize an empty dictionary to store the data
# user_dict = {}

# # user_dict = users.set_index('user')[['passwd', 'mps_cps']].T.to_dict()
# # Iterate over the DataFrame rows as (index, Series) pairs
# for index, row in users.iterrows():
#     # Use the 'user' field as the dictionary key and the other fields as values in another dictionary
#     # Hash the password before storing it in the dictionary
#     user_dict[row['user']] = {'password': hash_password(row['passwd']), 'mps': row['mps_cps']}

# Apply the hash_password function to the 'passwd' column
users['hashed_passwords'] = users['passwd'].apply(hash_password)

# Now you can use 'hashed_passwords' as a column name
user_dict = users.set_index('user')[['hashed_passwords', 'mps_cps']].T.to_dict()

# # Iterate over the DataFrame rows as (index, Series) pairs
# for index, row in users.iterrows():
#     # Use the 'user' field as the dictionary key and the other fields as values in another dictionary
#     user_dict[row['user']] = {'password': row['passwd'], 'mps': row['mps_cps']}

# Now, user_dict contains the username, password, and mps for each user

# Convert the user_dict to the format expected by Streamlit-Authenticator
credentials = {
    'usernames': user_dict
}
print(credentials)
# Initialize Authenticator
authenticator = stauth.Authenticate(credentials, "kp_cases_data_entry","123", cookie_expiry_days=30)


authenticator.login()
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
