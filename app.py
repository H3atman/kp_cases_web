import streamlit as st
from modules.helper import db_conn

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


# Initialize Connection to the database
conn = db_conn()
# conn = st.connection("postgresql", type="sql")



# Verify user credentials - OLD
def authenticate_user(username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT username, passwd FROM userbase WHERE username = %s AND passwd = %s", (username, password))
    cursor.fetchone()
    cursor.execute("SELECT ppo_cpo, mps_cps FROM userbase WHERE username = %s AND passwd = %s", (username, password))
    details = cursor.fetchone()
    cursor.close()
    if details:
        Appo, Amps = details
        return Appo, Amps
    else:
        return None, None


def login_form():
    st.title("KP Cases Encoding Users Login", anchor=False)
    with st.form(key="login", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password",type="password")
        if st.form_submit_button("Submit"):
            Appo, Amps = authenticate_user(username, password)
            if Appo and Amps:
                st.success("You've successfuly logged-in!")
                st.session_state['Amps'] = Amps
                st.session_state['Appo'] = Appo
                # st.write(st.session_state['Amps'], st.session_state['Appo'])
                st.switch_page("pages/entryCode.py")
            else:
                st.error("Invalid username or password. Please try again.")

# Initiate login form
login_form()



