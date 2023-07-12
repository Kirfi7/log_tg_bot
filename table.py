import gspread
from oauth2client.service_account import ServiceAccountCredentials
from cfg import scope

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
admin_sheet = client.open("ADMINS RED1").worksheet("Успеваемость администрации")
helper_sheet = client.open("HELPERS RED").worksheet("Успеваемость агентов поддержки")


async def get_admin_list():
    admin_nicks = admin_sheet.col_values(2)[1:]
    return [nick for nick in admin_nicks if nick not in ['', 'Mikhail_Mendeleev', 'Yaroslav_Belousov']]


async def get_helpers_dict():
    nicks, dates = helper_sheet.col_values(2)[10:], helper_sheet.col_values(4)[10:]
    return zip([nick for nick in nicks if nick != ''], [date for date in dates if date != ''])
