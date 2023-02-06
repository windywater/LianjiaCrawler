#-*- coding: utf8 -*-
import sqlite3
import json
import sys
import os

def load_json_house(file):
    with open(file, mode='r', encoding='utf-8') as file_obj:
        content = file_obj.read()

    return json.loads(content)

def json_to_sqlite(json_file, db_file):
    if not os.path.exists(json_file):
        return

    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()
    sql = "CREATE TABLE houses(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, url VARCHAR(100), title VARCHAR(50), layout VARCHAR(10), " \
        "area DECIMAL, address VARCHAR(30), region VARCHAR(16), total_price DECIMAL, avg_price DECIMAL)"

    cursor.execute(sql)
    connect.commit()

    houses_obj = load_json_house(json_file)
    houses_array = houses_obj["houses"]
    item_count = len(houses_array)
    index = 1
    for house_obj in houses_array:
        region = house_obj["r"] if "r" in house_obj else ""

        sql = "INSERT INTO houses(url, title, layout, area, address, region, total_price, avg_price) " \
            "VALUES ('{}', '{}', '{}', {}, '{}', '{}', {}, {})" \
            .format(house_obj["u"], house_obj["t"], house_obj["l"], house_obj["ar"], house_obj["ad"], region, house_obj["tp"], house_obj["ap"])

        cursor.execute(sql)

        if index % 300 == 0:
            print("{}/{}".format(index, item_count))
            connect.commit()

        index = index + 1

    connect.commit()
    connect.close()
    print("Done.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Arguments error.")
        exit(1)

    file_or_dir = sys.argv[1]
    (prefix, suffix) = os.path.splitext(file_or_dir)
    db_file = prefix + ".db"
    if not os.path.exists(db_file):
        json_to_sqlite(file_or_dir, db_file)
