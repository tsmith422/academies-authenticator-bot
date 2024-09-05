import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


# LOGIC TO SAY WHETHER TO VERIFY A MEMBER
def get_verification(user_input: tuple[str, str, str]) -> str:
    """
    Returns a string saying whether the user should be verified or not.
    :param user_input: Message containing the information needed to verify the member
    :return: ``Verified!`` or ``NOT Verified!`` depending on whether the user meets the requirements to be verified
    """
    if check_verification(user_input[-1]):
        return "Verified!"
    else:
        return "NOT Verified!"


# CHECKS IF A MEMBER TRYING TO VERIFY IS A PART OF THE VERIFICATION LIST
def check_verification(student_uin: str) -> bool:
    """
    Reads through the data sheet containing information about verified users and returns whether
    the user is one of those verified people.
    :param student_uin: Number used to identify and differentiate users, this is what is checked against the data file
    :return: ``True`` if the user is one of those verified users, ``False`` otherwise
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(
        "Texas A&M Engineering Academies Ambassadors Discord Access Form (Responses)"
    ).sheet1
    student_uins = set(sheet.col_values(2)[1:])

    return student_uin in student_uins
