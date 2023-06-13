import gspread
from oauth2client.service_account import ServiceAccountCredentials
from cfg import scope

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").worksheet("Успеваемость администрации")


async def get_admin_list():
    admin_nicks = sheet.col_values(2)[1:]
    return [nick for nick in admin_nicks if nick not in ['', 'Charlie_Marciano', 'Yaroslav_Belousov']]
