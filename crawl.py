#-*- coding: utf8 -*-
import io  
import os
import sys  
import time
import requests
from bs4 import BeautifulSoup  
import sqlite3
import json

class HouseCrawler(object):
    def __init__(self):
        requests.adapters.DEFAULT_RETRIES = 5
        sess = requests.session()
        sess.keep_alive = False
        self.url_template = "https://{}.lianjia.com/ershoufang/{}/pg{}/" # (id, region, page)
        self.house_set = set()
        self.load_config()

    def load_config(self):
        cfg_file = os.path.split(os.path.realpath(__file__))[0] + "\\config.json"
        with open(cfg_file, mode='r', encoding='utf-8') as file_obj:
            content = file_obj.read()
        self.cfg = json.loads(content)

    def crawl(self):
        today = time.strftime("%Y-%m-%d", time.localtime())

        for city in self.cfg["cities"]:
            city_house_array = []
            city_name = city["name"]
            city_id = city["id"]
            if city_name == "" or city_id == "":
                continue

            self.house_set = set()
            for region in city["regions"]:
                city_house_array.extend(self.crawl_region(city_id, region))

            house_info = {}
            house_info["date"] = today
            house_info["houses"] = city_house_array

            print("Writing to file...")
            house_file = os.path.split(os.path.realpath(__file__))[0] + "\\houses\\" + city_name + "\\" + today + ".json"
            self.write_file(house_file, house_info) 

    def _parse_basic_info(self, text):
        basic_list = list(filter(None, text.split("|")))
        layout = basic_list[0].strip()
        area = basic_list[1].strip().replace("平米", "")
        return [layout, area]

    def crawl_region(self, city_id, region):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 'Cookie': self.cfg["cookie"]}

        house_array = []
        page = 1
        max_page = 100
        max_page_found = False

        while True:
            if page > max_page:
                break

            page_url = self.url_template.format(city_id, region, page)
            print(page_url)

            try:
                response = requests.get(page_url, headers=headers, timeout=8)
                page_content = response.content.decode("utf-8", "ignore")
            except Exception as e:
                print("exception:" + str(e))
                page += 1
                time.sleep(5)
                continue

            page_soup = BeautifulSoup(page_content, "html.parser")

            # find max page
            if not max_page_found:
                page_data = page_soup.find("div", "page-box house-lst-page-box")["page-data"]
                max_page = int(json.loads(page_data)["totalPage"])
                print("max page:", max_page)
                max_page_found = True

            ul_elt = page_soup.find("ul", "sellListContent")
            if len(ul_elt) == 0:
                print("No house, maybe the request has something problem. You can retry or stop(r/s):")
                next_action = input()
                if next_action == "r":
                    print("Retrying...")
                    continue
                else:
                    sys.exit(0)

            print("house count:", len(ul_elt))

            for house_elt in ul_elt:
                house_url = house_elt.find("a", "noresultRecommend img LOGCLICKDATA")["href"]
                if house_url in self.house_set:
                    continue

                try:
                    self.house_set.add(house_url)
                    title = house_elt.find("div", "title").find("a").get_text()
                    address = house_elt.find("div", "flood").get_text().replace(" ", "")
                    basic_info = house_elt.find("div", "houseInfo").get_text()
                    [layout, area] = self._parse_basic_info(basic_info)
                    
                    total_price = house_elt.find("div", "totalPrice totalPrice2").get_text().replace("万", "").replace("参考价:", "").strip()
                    average_price = house_elt.find("div", "unitPrice").get_text().replace("元/平", "").replace(",", "")
                    
                    house_dict = {}
                    house_dict["u"] = house_url
                    house_dict["t"] = title
                    house_dict["l"] = layout
                    house_dict["ar"] = float(area)
                    house_dict["ad"] = address
                    house_dict["r"] = region
                    house_dict["tp"] = float(total_price)
                    house_dict["ap"] = float(average_price)
                    house_array.append(house_dict)
                except Exception as e:
                     print("exception:" + str(e))
                
            print("Sleeping for a while...")
            time.sleep(float(self.cfg["page_interval"]))
            if page % int(self.cfg["pages_of_group"]) == 0:
                print("Sleeping more...")
                time.sleep(self.cfg["group_interval"])

            page += 1

        return house_array

    def write_file(self, file_name, house_info):
        dir = os.path.dirname(file_name)
        if not os.path.exists(dir):
            os.mkdir(dir)

        content = json.dumps(house_info, ensure_ascii=False)
        with open(file_name, mode='w', encoding='utf-8') as file_obj:
            file_obj.write(content)

if __name__ == '__main__':
    crawler = HouseCrawler()
    begin = time.time()
    crawler.crawl()
    end = time.time()
    m, s = divmod(int(end-begin), 60)
    h, m = divmod(m, 60)
    print("Elapsed: {} hours {} minutes {} secnods".format(h, m, s))
