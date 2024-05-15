from datetime import datetime

def profile(fname, midname, lname, qlfr, alias, age, sex):
    if not fname:
        fname = "Unidentified"
    if not midname:
        midname = "Unidentified"
    if not lname:
        lname = "Unidentified"
    if not qlfr:
        qlfr = "Unidentified"
    if not alias:
        alias = "Unidentified"
    if not sex:
        sex = "Unidentified"
    if not age:
        age = "Unidentified"
    name = f"{fname} {midname} {lname} {qlfr} alias {alias} ({age}/{sex})"
    return name

def process_offense(offenseType, otherOffense, offenseClass):
    if not offenseType and not offenseClass:
        offenseType = otherOffense
        offenseClass = 'Other Cases'
    return offenseType, offenseClass

def datetimeEncoded():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


