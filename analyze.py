#-*- coding: utf8 -*-
#from configparser import BasicInterpolation
import io  
import os
import sys  
import time
import json
import numpy as np

def loadHouses(file):
    with open(file, mode='r', encoding='utf-8') as file_obj:
        content = file_obj.read()

    return json.loads(content)


if __name__ == '__main__':
    file1 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-08-27.json"
    file2 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-09-02.json"
    file6 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-09-05.json"

    file7 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\shenzhen\\2022-08-31.json"
    file8 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\shenzhen\\2022-09-01.json"
    file88 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\shenzhen\\2022-09-07.json"

    file9 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\beijing\\2022-08-31.json"
    file10 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\beijing\\2022-09-07.json"

    file11 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\hangzhou\\2022-08-31.json"
    file12 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\hangzhou\\2022-09-01.json"
    file13 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\hangzhou\\2022-09-07.json"

    file100 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\shanghai\\2022-09-02.json"
    file101 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\shanghai\\2022-09-07.json"
    
    house_total = 0
    houseMap = {}
    for file in [file100, file101]:
        houses = loadHouses(file)
        date = houses["date"]
        house_total = len(houses["houses"])
        for house in houses["houses"]:
            url = house["u"]
            title = house["t"]
            total = float(house["tp"])
            if not url in houseMap:
                houseMap[url] = {"dates": [], "title": "", "total_prices": []}
            
            houseMap[url]["dates"].append(date)
            houseMap[url]["title"] = title
            houseMap[url]["total_prices"].append(total)

    change_count = 0
    dec_count = 0

    for url in houseMap:
        if len(houseMap[url]["dates"]) > 1:
            tps = houseMap[url]["total_prices"]
            prices_set = set(tps)
            if len(prices_set) > 1:
                print(url, houseMap[url])
                change_count += 1

            aver_tp = np.mean(tps)
            if tps[-1] < aver_tp:
                dec_count += 1

    print("house_total", house_total)                
    print("change count", change_count)
    print("dec count", dec_count)