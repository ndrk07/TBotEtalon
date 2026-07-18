from gspread import Client, Spreadsheet, Worksheet, service_account
from datetime import datetime
from services.calculation import calculatePrice
from config import prName, prPrice, tableID

LISTFOROST = "Склад (остатки)"
LISTFORORDERS = "Заказы покупателей"
STATUS = "Оформление"

def client_init_json() -> Client:
    return service_account(filename="services/botetalon-cc0fea78dbf5.json")

def get_table_by_id(client: Client, table_id):
    return client.open_by_key(table_id)
#get data
def get_data(table: Spreadsheet, title: str):
    worksheet = table.worksheet(title)
    return worksheet.get_all_records()

#return data ost
def google_sheet():
    client = client_init_json()
    table = get_table_by_id(client, tableID)
    data = get_data(table, LISTFOROST)
    return data
#new order
def new_order(user, order_id):
    client = client_init_json()
    table = get_table_by_id(client, tableID)
    worksheet = table.worksheet(LISTFORORDERS)
    current_date = datetime.now().strftime("%d.%m.%Y")
    worksheet.append_row([
        current_date, 
        user["name"], 
        user["phone"], 
        user["product"][prName],
        user["count"],
        user["product"][prPrice],
        calculatePrice(user["product"][prPrice], user["count"]),
        STATUS,
        order_id
    ])
#change status
def change_status_google_sheet(id, status):
    client = client_init_json()
    table = get_table_by_id(client, tableID)
    worksheet = table.worksheet(LISTFORORDERS)
    cell = worksheet.find(str(id))
    if cell:
        worksheet.update_cell(cell.row, 8, status)
        print("успешно изменен статус")

if __name__ == "__main__":
    print(google_sheet())