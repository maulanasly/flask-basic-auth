import requests
import json
import xlwt

app_key = 'x73z3SCZz9RJpOW8JYogyvfuYMBV62N5'
session_id = 'bb0f9bdc5e40152b260c289bf1a8850e'

coaching_url = "https://coaching-api.sense-os.nl/v2"
auth_url = "https://auth-api.sense-os.nl/v1"


def get_session_id():
    headers = {'APPLICATION-KEY': app_key, 'Content-Type': 'application/json'}
    body = {"username": "gilang+helpdesk@sense-os.nl", "password": "12341234"}
    results = requests.post(auth_url + '/login', headers=headers, data=json.dumps(body))
    return json.loads(results.content)


def get_users():
    session_id = get_session_id().get('session_id', None)
    headers = {'APPLICATION-KEY': app_key, 'SESSION-ID': session_id, 'Content-Type': 'application/json'}
    results = requests.get(coaching_url + '/users?user_type=USER', headers=headers)
    if results.status_code == 200:
        return json.loads(results.content)
    return None


def generate_to_excell():
    TITLE_STYLE = xlwt.easyxf("font: name Calibri, bold on, height 240; align: horiz center")
    TEXT_STYLE = xlwt.easyxf("font: name Calibri,height 240;")
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("4DKL")
    sheet.write(0, 0, "No", style=TITLE_STYLE)
    sheet.write(0, 1, "Firstname", style=TITLE_STYLE)
    sheet.write(0, 2, "Lastname", style=TITLE_STYLE)
    sheet.write(0, 3, "Email", style=TITLE_STYLE)
    users = get_users()
    i = 1
    for value in users:
        sheet.write(i, 0, i, style=TEXT_STYLE)
        sheet.write(i, 1, value['user_info'].get('first_name', None), style=TEXT_STYLE)
        sheet.write(i, 2, value['user_info'].get('last_name', None), style=TEXT_STYLE)
        sheet.write(i, 3, value['email'], style=TEXT_STYLE)
        i += 1
    book.save('Mentors.xls')


if __name__ == '__main__':
    generate_to_excell()
