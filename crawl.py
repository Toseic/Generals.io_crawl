from urllib import response
import requests,json,time
from bs4 import BeautifulSoup
import urllib.request
import lzstring

# 选择爬取榜上前多少的人
people_top_num = 1
# 选取爬取的赛季
crawl_season = 21

requests.packages.urllib3.disable_warnings()

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}
# my_proxies={"http": "http://127.0.0.1:7890","https": "http://127.0.0.1:7890"}


# url = "https://generals.io/rankings/{}"

def people_id_crawl(season):
    people_list = []
    people_url = "https://generals.io/rankings/{}".format(season)
    response = requests.get(url=people_url, headers=headers,
    # proxies=my_proxies
    )
    html = response.text
    soup=BeautifulSoup(html,'lxml')
    people_res = soup.find_all(attrs={'target':'_blank'})

    for i in range(100):
        # print(people.get_text())
        people_list.append(people_res[i].get_text())
        # print(people_res[i].get_text())
    # print(html)
    return people_list

def replay_crawl(people_id, crawl_now = False):
    # people_url = "https://generals.io/profiles/{}".format(people_id)
    offset, count = 0,100
    people_url = "https://generals.io/api/replaysForUsername?u={}&offset={}&count={}"
        
    
    json_data_select = []
    while True:
        time.sleep(1)
        print("crawling url="+people_url.format(people_id,offset,count))
        for i in range(5):
            response = requests.get(url=people_url.format(people_id,offset,count), 
                headers=headers, 
                # proxies=my_proxies,
                 verify=False)
            if (response.status_code != 200): print("try again",end=" ")
            else: break
        json_data = response.json()
        
        len_json_data = len(json_data)
        if len_json_data == 0: 
            print("person id:{} all over".format(people_id))
            break
        # if offset > 200: break
        for i in range(len_json_data):
            if json_data[i]["type"] == '1v1':
                json_data_select.append(json_data[i]["id"])
                if (crawl_now == True):
                    gior_crawl(json_data[i]["id"])
        offset += count
    with open("./replay_id/{}.json".format(people_id),"w") as a:
        json.dump(json_data_select, a)
    
        # print(json_data_select)

def gior_crawl(replay_id):
    urllib.request.urlretrieve(f"https://generalsio-replays-na.s3.amazonaws.com/{replay_id}.gior",
         f"./gior/{replay_id}.gior")
    lz = lzstring.LZString()
        
    with open(f"./gior/{replay_id}.gior", mode="rb") as compressed_rep:
        compressed_arr = compressed_rep.read()
        compressed_str = ""
        for i in range(int(len(compressed_arr) / 2)):
            compressed_str += chr(compressed_arr[2 * i] * 256 + compressed_arr[2 * i + 1])
        rep = json.loads(lz.decompress(compressed_str))
        # print(rep)
    
# people_id_crawl(21)
# replay_crawl('bucknuggets21')
# gior_crawl("rc4Yr3lC_")
def main():

    people_list = people_id_crawl(crawl_season)
    people_list_len = len(people_list)
    for i in range(people_top_num):
        person_id = people_list[i]
        replay_crawl(person_id, True)


    pass


if __name__ == '__main__':
    main()