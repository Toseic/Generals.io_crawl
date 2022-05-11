from urllib import response
import requests,json,time,os
from bs4 import BeautifulSoup
import urllib.request
import lzstring

# 选择爬取榜上前多少的人
people_top_num = 100
# 选取爬取的赛季
crawl_season = 22
people_list = []


requests.packages.urllib3.disable_warnings()

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}
my_proxies={"http": "http://127.0.0.1:7890","https": "http://127.0.0.1:7890"}


def people_id_crawl(season):
    
    people_url = "https://generals.io/rankings/{}".format(season)
    response = requests.get(url=people_url, headers=headers,
    proxies=my_proxies
    )
    html = response.text
    soup=BeautifulSoup(html,'lxml')
    people_res = soup.find_all(attrs={'target':'_blank'})

    for i in range(people_top_num):

        people_list.append(people_res[i].get_text())

    return people_list

def replay_crawl(people_id):
 
    offset, count = 0,150
    people_url = "https://generals.io/api/replaysForUsername?u={}&offset={}&count={}"
    path = "./replay_id/{}.json".format(people_id)
    if os.path.exists(path):
        print(people_id+" already crawled.")
        return False
    json_data_select = {}
    while True:
        time.sleep(5)
        print("crawling url="+people_url.format(people_id,offset,count))
        for i in range(5):
            response = requests.get(url=people_url.format(people_id,offset,count), 
                headers=headers, 
                proxies=my_proxies,
                 verify=False)
            if (response.status_code != 200): print("try again",end=" ")
            else: break
        json_data = response.json()
        
        len_json_data = len(json_data)
        if len_json_data == 0: 
            print("person id:{} all over".format(people_id))
            break
  
        for i in range(len_json_data):
            if json_data[i]["type"] == '1v1' and\
            json_data[i]["ranking"][0]["stars"] >= 50 and\
            json_data[i]["ranking"][1]["stars"] >= 50 :
                json_data_select[json_data[i]["id"]] = False

        offset += count

    with open("./replay_id/{}.json".format(people_id),"w") as a:
        json.dump(json_data_select, a)
    return True;

if __name__ == '__main__':
    people_list = people_id_crawl(22)
    game_map = {}
    for i in people_list:

        if (replay_crawl(i)): time.sleep(60)

