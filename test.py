import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'gkey.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

sheet = client.open_by_key('1-EEmcUjINw-mqsp76bYiYPJwkYngOa1MeQ1KWTUO6Xk').worksheet("Updates")
data = sheet.get_all_values()
curr = 1
while(data[curr][0] != ''):
    # print(data[curr])
    curr += 1


with open("data/money.csv", 'r') as file:
    csvreader = csv.reader(file)
    for line in csvreader:
        print(line)