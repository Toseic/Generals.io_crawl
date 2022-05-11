import os,json
import functools 

base_path="E:/CodePalace/cpp code/AI-game/Generals.io_crawl/dataset/json/"
begin_list = [base_path+filename for filename in os.listdir(base_path)]
replay_list = []
# print(begin_list)
for base in begin_list:
    base += "/"
    path_list =  [base+filename for filename in os.listdir(base)]
    # print(path_list)

    for path_ in path_list:
        with open(path_,mode="r",encoding="utf-8") as file:
            print("open{}".format(path_),end="   ")
            file_json = json.load(file)
            if (
                len(file_json) < 1 or \
                len(file_json["moves"]) < 0 
            ):
                print("\r",end="")
                continue
            else:
                replay_list.append(file_json)
                print(len(replay_list),end="\r")

# replay_list = []
print("\nlen = ",len(replay_list))
# print("begin unique")
# unique_list = functools.reduce(lambda x, y: y in x and x or x + [y], replay_list, [])
# print(len(replay_list))
with open(base_path+"data.json","w",encoding="utf-8") as file:
    json.dump(replay_list,file)
# print(replay_list)
