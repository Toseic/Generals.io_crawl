from base64 import encode
import json
from logging import exception
import os,sys
import lzstring
# from multiprocessing import Pool
import multiprocessing as mp

id = sys.argv[1]
base_path = "E:\CodePalace\cpp code\AI-game\Generals.io_crawl\dataset\gior{}".format(id)
json_path = "E:\CodePalace\cpp code\AI-game\Generals.io_crawl\dataset\json\json{}".format(id)

if not os.path.exists(json_path):
    os.makedirs(json_path)

def add_info(list_data : list) -> map:
    # print(list_data)
    info_map = {}
    if (not list_data[0]): return {}
    info_map["version"] = int(list_data[0])
    info_map["id"] = str(list_data[1])
    info_map["mapWidth"] = int(list_data[2])
    info_map["mapHeight"] = int(list_data[3])
    info_map["usernames"] = list_data[4]   # data check TODO:
    info_map["stars"] = list_data[5]
    info_map["cities"] = list_data[6]
    info_map["cityArmies"] = list_data[7]
    info_map["generals"] = list_data[8]
    info_map["mountains"] = list_data[9]
    info_map["moves"] = list_data[10]
    
    return info_map

def decode( path: str ):
    lz = lzstring.LZString()
    if not os.path.exists(path):
        print("{} does not exist !".format(path))
        return 
    with open(path, mode="rb") as compressed_rep:
        compressed_arr = compressed_rep.read()
        compressed_str = ""
        for i in range(int(len(compressed_arr) / 2)):
            compressed_str += chr(compressed_arr[2 * i] * 256 + compressed_arr[2 * i + 1])
        rep = json.loads(lz.decompress(compressed_str))
        rep_map = add_info(rep)
        return rep_map
        # print(rep_map)


def file_check( myid : str):
    print("check {}... ".format(myid), end=" ")
    path = "{}\{}.gior".format(base_path,myid)
    map_path = "{}\{}.json".format(json_path,myid)

    datamap = decode(path)
    if datamap == None: 
        return  

    with open(map_path, mode="w") as mapfile:
        json.dump(datamap, mapfile)
    print("  isdone.")

    # print(datamap)
# file_check(replay_id)
# def decode( path ):
#     # user_id = "bucknuggets21"
#     # id_file_path = f"./dataset/json/json1/{user_id}.json" 
#     with open(path, "r") as id_file:
#         id_list = json.load(id_file)
#         # print(id_list)
#         for id in id_list:
#             file_check(id)

# base_path = f"E:\CodePalace\cpp code\AI-game\Generals.io_crawl\dataset\gior1"
if __name__ == '__main__':
    id_list = [filename[:-5] for filename in os.listdir(base_path)]
    print(len(id_list),id_list[0])
    # file_check(id_list[0])
    pool=mp.Pool(processes=mp.cpu_count())#设置进程数目
    pool.map(file_check,id_list)