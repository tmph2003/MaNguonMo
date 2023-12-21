import crawl_data, hbase_api
import time
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta

FILE_PATH = "latest_row_key.txt"
FILE_CSV = "BTC-USD.csv"

class Main:
    def __init__(self):
        self.crawl = crawl_data.Crawl()
        self.hbase = hbase_api.HBase()
        self.hbase.create_table()
        self.stop_import_flag = False

    def ImportData(self):
        self.stop_import_flag = False
        self.hbase.write_oldest_row_key_to_file(FILE_PATH, len(self.hbase.show_data_from_table()))
        the_latest_row_key = self.hbase.read_oldest_row_key_from_file(FILE_PATH)
        while not self.stop_import_flag:
            self.hbase.create_connection()
            the_latest_row = self.hbase.get_the_latest_row(the_latest_row_key)
            data = self.crawl.main(the_latest_row)
            print('------------------Writing data into HBase------------------')
            self.hbase.put_data_from_crawler(data, the_latest_row_key)
            self.hbase.write_oldest_row_key_to_file(FILE_PATH, the_latest_row_key+1)
            the_latest_row_key = self.hbase.read_oldest_row_key_from_file(FILE_PATH)
            print('------------------Finished------------------')
            time.sleep(5)
    
    def display_dataframe(self):
        self.hbase.create_connection()
        result = self.hbase.show_data_from_table()
        df = pd.DataFrame(result)
        root = tk.Tk()
        root.title("DataFrame Viewer")

        tree = ttk.Treeview(root)
        scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")

        tree["columns"] = tuple(df.columns)
        for col in df.columns:
            tree.column(col, anchor="center", width=150)
            tree.heading(col, text=col)

        for i, row in df.iterrows():
            tree.insert("", i, values=tuple(row))

        tree.configure(yscrollcommand=scrollbar_y.set)
        tree.pack(expand=True, fill="both")

        root.mainloop()

    def BuildChart(self):
        self.hbase.create_connection()
        result = self.hbase.show_data_from_table()
        df = pd.DataFrame(result)
        df['Date:'] = pd.to_datetime(df['Date:'])
        plt.plot(df['Date:'], df['Close Price:'], label='Bitcoin Price', color='blue')
        plt.show()

    def Predict(self, open_price):
        self.hbase.create_connection()
        result = self.hbase.show_data_from_table()
        df = pd.DataFrame(result)
        current_date = datetime.now()
        date_60_days_ago = current_date - timedelta(days=720)
        df['Date:'] = pd.to_datetime(df['Date:'])
        df = df[df['Date:'] > date_60_days_ago]
        X = df[['Open Price:']]
        y = df['Close Price:']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict([[open_price]])
        messagebox.showinfo("Thông báo", f"Bitcoin close price predict: {round(y_pred[0],2)}")

if __name__ == "__main__":
    main = Main()
    # hbase_api.HBase().delete_all_data(FILE_PATH)
    hbase_api.HBase().put_data_from_csv(FILE_CSV)