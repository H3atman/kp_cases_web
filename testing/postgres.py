import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config("KP Cases Login")

# HIDE NAVBAR and stFormSubmitButton
css ='''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# Initialize connection.
conn = st.connection("postgresql", type="sql")
# conn = st.connection("gsheets", type=GSheetsConnection)
# users_db = st.connection("usersDB", type=GSheetsConnection)

# Create a dataframe where we can query the username and passwords

# ===========  Start FUNCTIONS  ====================
@st.cache_data(ttl=60)
def read_users_db(worksheet, usecols):
    user_data = users_db.read(worksheet=worksheet, usecols=usecols)
    user_data = user_data.dropna(how="all")
    return user_data

@st.cache_data(ttl=60)
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
                    # Store Appo in session_state
                    st.session_state.Appo = ippo
                    # Store Amps in session_state
                    st.session_state.Amps = imps
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