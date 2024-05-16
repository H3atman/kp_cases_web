import streamlit as st
from streamlit_gsheets import GSheetsConnection


conn = st.connection("usersDB", type=GSheetsConnection)

df = conn.read(usecols = list(range(4)))
df = df.dropna(how="all")

st.dataframe(df)


