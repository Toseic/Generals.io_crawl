import requests
from multiprocessing import Pool
import time
from urllib import response
import requests,json,time,os
from bs4 import BeautifulSoup
import urllib.request
import lzstring,sys

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'   
}
file_id = sys.argv[1]
print("[json_{}] ".format(file_id))

def gior_crawl(replay_id):
    if (replay_id_map[replay_id] == False):
        print("[json_{}] ".format(file_id)+"begin downloading "+replay_id,end="... ")
        urllib.request.urlretrieve(
            f"https://generalsio-replays-na.s3.amazonaws.com/{replay_id}.gior",
            f"./gior/{replay_id}.gior"
        )

        print(" is done.")
        replay_id_map[replay_id] = True
    else:
        print("[json_{}] ".format(file_id)+replay_id+" is already downloaded. ")


replay_id_file = open("./apart_id/{}.json".format("json_"+file_id),"r",encoding='utf-8')
replay_id_map = json.load(replay_id_file)
replay_id_file.close()
replay_id_list = list(replay_id_map.keys())    
replay_id_list_len = len(replay_id_list)

crawl_num = 200
begin_place = 0
# while True:
#     if not replay_id_map[replay_id_list[begin_place]]:
#         break
#     if (begin_place == replay_id_list_len):
#         break
#     else: begin_place+=1

# for i in range(crawl_num):
#     if ((begin_place+i) == replay_id_list_len): break
#     gior_crawl(replay_id_list[i])
for i in range(replay_id_list_len):
    if replay_id_map[replay_id_list[i]]:
        begin_place+=1
        continue
    else :
        print("{} / {} is crawled.".format(begin_place,replay_id_list_len))
        break
for i in range(crawl_num):
    print("{} / {} | ".format(i+begin_place,replay_id_list_len),end="")
    time.sleep(0.3)
    gior_crawl(replay_id_list[begin_place+i])

replay_id_file = open("./apart_id/{}.json".format("json_"+file_id),"w",encoding='utf-8')
json.dump(replay_id_map,replay_id_file)
replay_id_file.close()
