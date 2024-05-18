from datetime import datetime

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

