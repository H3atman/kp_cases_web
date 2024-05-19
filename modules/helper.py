import streamlit as st
from datetime import datetime
import psycopg2
from psycopg2.errors import UniqueViolation

def profile(fname, midname, lname, qlfr, alias, age, sex):
    if not fname:
        fname = "Unidentified"
    if not midname:
        midname = "Unidentified"
    if not lname:
        lname = "Unidentified"
    if not qlfr:
        qlfr = ""
    if not alias:
        alias = "Unknown"
    if not sex:
        sex = "Unidentified"
    if not age:
        age = "Unidentified"
    name = f"{fname} {midname} {lname} {qlfr} alias {alias} ({age}/{sex})"
    return name

def vic_name_process(fname, midname, lname, qlfr, alias, age, sex):
    if not fname:
        fname = "Unidentified"
    if not midname:
        midname = "Unidentified"
    if not lname:
        lname = "Unidentified"
    if not qlfr:
        qlfr = ""
    if not alias:
        alias = "Unknown"
    if not sex:
        sex = "Unidentified"
    if not age:
        age = "Unidentified"

    return fname, midname, lname, qlfr, alias, age, sex

def process_offense(offenseType, otherOffense, offenseClass):
    if not offenseType and not offenseClass:
        offenseType = otherOffense
        offenseClass = 'Other Cases'
    return offenseType, offenseClass

def datetimeEncoded():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def local_address(street, brgy, cityMun, province):
    if not street:
        address = f"{brgy}, {cityMun} {province}"
    else:
        address = f"{street} {brgy}, {cityMun} {province}"
    return address


# Connect to your PostgreSQL database
def db_conn():
    # Get the PostgreSQL connection details from the secrets
    pg_conn = st.secrets["connections"]["postgresql"]
    conn = psycopg2.connect(
        dbname=pg_conn["database"],
        user=pg_conn["username"],
        password=pg_conn["password"],
        host=pg_conn["host"],
        port=pg_conn["port"]
    )
    return conn


# Function to check the latest entryNumber
# @st.cache_data(ttl="60m")
def get_next_entry_number(Amps, Appo):
    conn = db_conn()
    cursor = conn.cursor()
    # Fetch the last encoded entry for the given Amps and Appo
    cursor.execute("SELECT entry_number FROM crime_incidents WHERE ppo = %s AND station = %s ORDER BY date_encoded DESC LIMIT 1", (Appo, Amps))
    result = cursor.fetchone()
    cursor.close()
    if result is not None:
        # Extract the last value before the "-" and increment it by 1
        last_value = int(result[0].split("-")[-1])
        next_value = last_value + 1
        return next_value
    else:
        # Return 1 if no entry was found
        return 1
    

# Function to retrieve BARANGAY from the database
@st.cache_data(ttl="60m")
def get_brgy_data(Appo, Amps):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT brgy FROM regionxii_brgy WHERE ppo_cpo = %s AND mps_cps = %s", (Appo, Amps))
    data = cursor.fetchall()
    cursor.close()
    return data

# Function to retrieve MUN/CITY from the database
@st.cache_data(ttl="60m")
def get_muncity_data(Appo):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT mun_city FROM regionxii_brgy WHERE ppo_cpo = %s", (Appo,))
    data = cursor.fetchall()
    cursor.close()
    return data


# Function to retrieve PROVINCE from the database
@st.cache_data(ttl="60m")
def get_prov_data(Appo):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT province FROM regionxii_brgy WHERE ppo_cpo = %s", (Appo,))
    data = cursor.fetchone()
    cursor.close()
    return data[0]

# Function to retrieve Offenses from the database
@st.cache_data(ttl="60m")
def get_crime_incidentName_data():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT incidents FROM crime_class")
    incidents = cursor.fetchall()

    cursor.close()
    return incidents


# Function to identify the  Offense Classification from the database
@st.cache_data(ttl="60m")
def get_crime_classification_data(offense):
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT classification FROM crime_class WHERE incidents = %s", (offense,))
    classification = cursor.fetchone()

    cursor.close()
    return classification[0]

# Function to store entryNumber - OLD
def store_entryNumber(newEntry, Appo, Amps):
    try:
        pro = "PRO 12"
        date_encoded = datetimeEncoded()
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO crime_incidents (entry_number, date_encoded, pro, ppo, station) VALUES (%s, %s, %s, %s, %s)", (newEntry, date_encoded, pro, Appo, Amps))
        cursor.execute("INSERT INTO victim_details (entry_number, date_encoded, pro, ppo, station) VALUES (%s, %s, %s, %s, %s)", (newEntry, date_encoded, pro, Appo, Amps))
        conn.commit()
        cursor.close()

    except UniqueViolation as e:
        st.error(f"Entry number {newEntry} already exists in the database.")
        st.stop()

# Function to store the encoded data to the database
def store_data(newEntry, pi_distprov, pi_citymun, incident_selected_brgy, pi_street,dt_reported,time_reported_str,dt_committed,time_committed_str,vic_name,vic_fname,vic_midname,vic_lname,vic_qlfr,vic_alias,vic_age,vic_gndr,vic_distprov,vic_cityMun,vic_add_street, vic_address, sus_name, sus_address, offense_Type, offenseClass, det_narrative,case_status):
    conn = db_conn()
    cursor = conn.cursor()
    # Enter data to the crime_incidents db
    cursor.execute("UPDATE crime_incidents SET province = %s, city = %s, barangay = %s, street = %s, date_reported = %s, time_reported = %s, date_committed = %s, time_committed = %s, offense = %s, offense_type = %s, victims_name_age_sex = %s, victims_local_address = %s, suspects_name_age_sex = %s, suspects_local_address = %s, narrative = %s, case_status = %s WHERE entry_number = %s", (pi_distprov, pi_citymun, incident_selected_brgy, pi_street, dt_reported, time_reported_str, dt_committed, time_committed_str, offense_Type, offenseClass,vic_name, vic_address, sus_name, sus_address, det_narrative, case_status, newEntry))

    # Enter data to the victim_details db
    cursor.execute("UPDATE victim_details SET province = %s, city = %s, barangay = %s, street = %s, date_reported = %s, time_reported = %s, date_committed = %s, time_committed = %s, offense = %s, offense_type = %s, suspects_name_age_sex = %s, narrative = %s, case_status = %s, victim_first_name = %s, victim_middle_name = %s, victim_last_name = %s, victim_qualifier = %s, victim_alias = %s, victim_age = %s, victim_sex = %s, victim_province_address = %s, victim_city_address = %s, victim_street_house_number_address = %s WHERE entry_number = %s", (pi_distprov, pi_citymun, incident_selected_brgy, pi_street, dt_reported, time_reported_str, dt_committed, time_committed_str, offense_Type, offenseClass, sus_name, det_narrative, case_status,vic_fname,vic_midname,vic_lname,vic_qlfr, vic_alias, vic_age, vic_gndr, vic_distprov, vic_cityMun,vic_add_street,newEntry))

    conn.commit()
    cursor.close()
    return "The data has been successfuly submitted"


def convert_to_proper_time(time_reported_str, time_committed_str):
    # Convert the strings into datetime objects
    time_reported = datetime.strptime(time_reported_str, "%I:%M %p").time()

    # Check if time_committed_str is not blank
    if time_committed_str.strip():
        time_committed = datetime.strptime(time_committed_str, "%I:%M %p").time()
    else:
        time_committed = "NULL"

    # Return the time objects
    return time_reported, time_committed


def query_encoded_data(Appo, Amps):
    conn = st.connection("postgresql", type="sql")

    df = conn.query(f"SELECT * FROM crime_incidents WHERE ppo = '{Appo}' AND station = '{Amps}';", ttl="100m",show_spinner=True, index_col="entry_number")

    return df

    