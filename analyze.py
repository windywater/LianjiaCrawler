#-*- coding: utf8 -*-
#from configparser import BasicInterpolation
import io  
import os
import sys  
import time
import json

def loadHouses(file):
    with open(file, mode='r', encoding='utf-8') as file_obj:
        content = file_obj.read()

    return json.loads(content)


if __name__ == '__main__':
    file1 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-08-27.json"
    file2 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-08-28.json"
    file3 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-08-29.json"
    file4 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-08-30.json"
    file5 = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\wuhan\\2022-08-31.json"
    
    houseMap = {}
    for file in [file3, file4, file5]:
        houses = loadHouses(file)
        date = houses["date"]
        for house in houses["houses"]:
            url = house["u"]
            title = house["t"]
            total = float(house["tp"])
            if not url in houseMap:
                houseMap[url] = {"dates": [], "title": "", "total_prices": []}
            
            houseMap[url]["dates"].append(date)
            houseMap[url]["title"] = title
            houseMap[url]["total_prices"].append(total)

    count = 0
    for url in houseMap:
        if len(houseMap[url]["dates"]) > 1:
            prices_set = set(houseMap[url]["total_prices"])
            if len(prices_set) > 1:
                print(url, houseMap[url])
                count += 1
                
    print(count)