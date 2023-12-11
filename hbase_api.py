import pandas as pd
import happybase
import csv
import crawl_data

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
                'Name': {},
                'Price': {},
                'Date': {},
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
                    price_column = f"Price:"
                    row_key = i.to_bytes(4, byteorder='big')
                    i += 1
                    data = {
                        date_column: row[0],
                        price_column: row[4]
                    }
                    table.put(row_key, data)
        except Exception as e:
            print("Error put_data_from_csv: ", e)
    
    def put_data_from_data(self, list_data, the_latest_row_key):
        try:
            conn = self.conn
            table = conn.table(self.TABLE_NAME)
            if the_latest_row_key != 0:
                i = the_latest_row_key
            else:
                i = 0                
            for row in list_data:
                    name_column = "Name:"
                    price_column = "Price:"
                    date_column = "Date:"
                    row_key = f"{i}"
                    i += 1
                    data = {
                        name_column: row["name"],
                        price_column: row["price"],
                        date_column: row["datetime"]
                    }
                    table.put(row_key.encode("utf-8"), data)
            return i
        except Exception as e:
            print("Error put_data_from_data: ", e)
    
    def show_data_from_table(self):
        try:
            conn = self.conn
            table = conn.table(self.TABLE_NAME)
            temp = {
                "id": dict(),
                "date": dict(),
                "price": dict()
            }
            result = []
            for x, y in table.scan():
                temp = []
                temp.append(int.from_bytes(x, byteorder="big"))
                for value1, value2 in y.items():
                    temp.append(value2)
                for i in range(1, 3):
                    temp[i] = temp[i].decode("utf-8")
                result.append(temp)
            return result
        except Exception as e:
            print("Error show_data_from_table: ", e)
    
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
    def read_latest_row_key_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return int(file.read())
        except (IOError, ValueError):
            return 0


    def write_latest_row_key_to_file(self, file_path, the_latest_row_key):
        try:
            with open(file_path, 'w') as file:
                file.write(str(the_latest_row_key))
        except Exception as e:
            print("Error: " + e)

if __name__ == "__main__":
    crawl = crawl_data.Crawl()
    data = crawl.main()
    print(data)
    hbase = HBase()
    hbase.create_connection()
    hbase.put_data_from_data(data)
    print("Done")