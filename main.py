import crawl_data
import hbase_api
import time

FILE_PATH = "latest_row_key.txt"

def main():
    crawl = crawl_data.Crawl()
    hbase = hbase_api.HBase()
    

    data = crawl.main()
    hbase.create_table()
    the_latest_row_key = hbase.read_latest_row_key_from_file(FILE_PATH)
    while True:
        hbase.create_connection()
        the_latest_row_key = hbase.put_data_from_data(data, the_latest_row_key)
        hbase.write_latest_row_key_to_file(FILE_PATH, the_latest_row_key)
        print("Done")
        time.sleep(120)

if __name__ == "__main__":
    main()
    # hbase_api.HBase().delete_all_data(FILE_PATH)