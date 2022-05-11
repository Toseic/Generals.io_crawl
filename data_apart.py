import json,os

base_path = f"./replay_id/"
id_map = {}
path_list = [base_path+filename for filename in os.listdir(base_path)]
num = 0
for path in path_list:
    print("open "+path)
    replay_id_file = open(path,"r",encoding='utf-8')
    replay_id_map = json.load(replay_id_file)
    replay_id_file.close()
    num += len(replay_id_map)
    id_map = {**id_map,**replay_id_map}
print(len(id_map),num)

num = 0
map_temp = {}
for i in list(id_map.keys()):
    map_temp[i] = id_map[i]
    if (num % 10000 == 0 and num!=0):
        replay_id_file = open("./apart_id/{}.json".format("json_"+str(int(num/10000))),"w",encoding='utf-8')
        json.dump(map_temp,replay_id_file)
        replay_id_file.close()
        map_temp = {}
    num += 1
replay_id_file = open("./apart_id/{}.json".format("json_"+str(int(num/10000) + 1)),"w",encoding='utf-8')
json.dump(map_temp,replay_id_file)
replay_id_file.close()
