import streamlit as st

# Initialize connection.
conn = st.connection("postgresql", type="sql")


Appo = "GENERAL SANTOS CPO"
Amps = "PS 03"

df_brgy = conn.query(f"SELECT brgy FROM regionxii_brgy WHERE ppo_cpo = '{Appo}' AND mps_cps = '{Amps}'",show_spinner=True)

st.dataframe(df_brgy,hide_index=True)