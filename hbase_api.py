import pandas as pd
import happybase
import csv
from datetime import datetime as dt
class HBase:
    TABLE_NAME = "crypto_table"
    def __init__(self):
        self.create_connection()


    def create_connection(self):
        try:
            conn = happybase.Connection('localhost', 9090, autoconnect=False, timeout=None)
            conn.open()
            self.conn = conn
        except Exception as e:
            print("Error create_connection: ", e)
    

    def create_table(self):
        try:
            conn = self.conn
            column_families = {
                'Date': {},
                'Price:': {}
            }
            conn.create_table(self.TABLE_NAME,column_families)
        except Exception as e:
            print("Already exist table")


    def put_data_from_csv(self, csv_filename):
        try:
            conn = self.conn
            df = pd.read_csv(csv_filename)
            table = conn.table(self.TABLE_NAME)

            with open(csv_filename, "r") as csv_filename:
                csv_reader = csv.reader(csv_filename)
                i = 0
                data = {}
                next(csv_reader, None)
                for row in csv_reader:
                    date_column = f"Date:"
                    open_price_column = f"Price:Open"
                    high_price_column = f"Price:High"
                    low_price_column = f"Price:Low"
                    close_price_column = f"Price:Close"
                    row_key = i.to_bytes(4, byteorder='big')
                    i += 1
                    data = {
                        date_column: row[0],
                        open_price_column: row[1],
                        high_price_column: row[2],
                        low_price_column: row[3],
                        close_price_column: row[4]
                    }
                    table.put(row_key, data)
        except Exception as e:
            print("Error put_data_from_csv: ", e)
    

    def put_data_from_crawler(self, data_input, the_latest_row_key):
        try:
            conn = self.conn
            table = conn.table(self.TABLE_NAME)
            if the_latest_row_key != 0:
                i = the_latest_row_key
            else:
                i = 0
            date_column = f"Date:"
            open_price_column = f"Price:Open"
            high_price_column = f"Price:High"
            low_price_column = f"Price:Low"
            close_price_column = f"Price:Close"
            row_key = i.to_bytes(4, byteorder='big')
            i += 1
            data = {
                date_column: str(dt.now().strftime("%Y-%m-%d %H:%M:%S")),
                open_price_column: str(data_input[0]),
                high_price_column: str(data_input[1]),
                low_price_column: str(data_input[2]),
                close_price_column: str(data_input[3])
            }
            table.put(row_key, data)
        except Exception as e:
            print("Error put_data_from_crawler: ", e)

    
    def show_data_from_table(self):
        try:
            conn = self.conn
            table = conn.table(self.TABLE_NAME)
            result = []
            for x, y in table.scan():
                temp = {
                    "Date:": y[b'Date:'].decode('utf-8'),
                    "Open Price:": float(y[b'Price:Open'].decode('utf-8').replace(",","")),
                    "High Price:": float(y[b'Price:High'].decode('utf-8').replace(",","")),
                    "Low Price:": float(y[b'Price:Low'].decode('utf-8').replace(",","")),
                    "Close Price:": float(y[b'Price:Close'].decode('utf-8').replace(",","")),
                }
                result.append(temp)
            return result
        except Exception as e:
            print("Error show_data_from_table: ", e)

    # def show_data_from_table_cdc(self, limit_row):
    #     try:
    #         conn = self.conn
    #         table = conn.table(self.TABLE_NAME)
    #         result = []
    #         for x, y in table.scan(reverse=True, limit=limit_row):
    #             temp = {
    #                 "Updated_At": y[b'Updated_At:'].decode('utf-8'),
    #                 "price": float(y[b'Price:'].decode('utf-8').replace(",","")),
    #                 "name": y[b'Name:'].decode('utf-8')
    #             }
    #             result.append(temp)
    #         return result
    #     except Exception as e:
    #         print("Error show_data_from_table: ", e)

    def delete_all_data(self, file_path):
        try:
            conn = self.conn
            table_name = self.TABLE_NAME
            conn.disable_table(table_name)
            conn.delete_table(table_name)
            print(table_name + " deleted")
            try:
                with open(file_path, 'w') as file:
                    file.write(str(0))
            except Exception as e:
                print("Error: " + e)
        except Exception as e:
            print("Error delete_all_data: ", e)

    def read_oldest_row_key_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                result = int(file.readline())
                if result == None:
                    result = 0
                else:
                    return result
        except (IOError, ValueError):
            return 0

    def write_oldest_row_key_to_file(self, file_path, the_latest_row_key):
        try:
            with open(file_path, 'w') as file:
                file.write(str(the_latest_row_key))
        except Exception as e:
            print("Error write_oldest_row_key_to_file: " + e)

    def get_the_latest_timestamp(self, row_key):
        try:
            conn = self.conn
            conn.open()
            table = conn.table(self.TABLE_NAME)
            latest_row_key = f'{row_key - 1}'
            latest_row_key = str(latest_row_key).encode('utf-8')
            row_data = table.row(row=latest_row_key, columns=['Price:'], include_timestamp=True)
            if row_data.items():
                ts = list(row_data.items())[0][1][1] / 1000
                return ts
            else:
                print("Khong ton tai row")
        except Exception as e:
            print("Error in get_the_latest_timestamp:", str(e))
            return None

    def get_the_latest_row(self, row_key):
        try:
            conn = self.conn
            conn.open()
            table = conn.table(self.TABLE_NAME)
            latest_row_key = row_key - 1
            latest_row_key = latest_row_key.to_bytes(4, byteorder='big')
            row_data = table.row(row=latest_row_key)
            return row_data
        except Exception as e:
            print("Error in get_the_latest_row:", str(e))
            return None
if __name__ == "__main__":
    hbase = HBase()
    hbase.create_connection()
    # hbase.delete_all_data('latest_row_key.txt')
    # hbase.create_table()
    # hbase.put_data_from_csv('BTC-USD.csv')
    # latest_row_key = hbase.read_oldest_row_key_from_file('latest_row_key.txt')
    hbase.write_oldest_row_key_to_file('latest_row_key.txt', len(hbase.show_data_from_table()))
    index = hbase.read_oldest_row_key_from_file('latest_row_key.txt')
    x = hbase.get_the_latest_row(index)
    print(x)