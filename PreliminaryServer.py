#main05

import csv, json, requests, os
from sanic import Sanic, Request, text
from sanic.response import json


def csv2dict(filename):
    """
    读取csv至进程中
    :param filename: csv 的文件名
    :return: 一个方便python处理的数据结构，例如设备的数组和字典 例如[{"device_id":"0001",...},xx,...]或{"0001":{...},"0002":{...},...}
    可以复用python与json相互转换的实验代码
    """
    with open(filename,"r",newline='') as f:
        device_dict = list(csv.DictReader(f))
    return device_dict

def dict2csv_save(filename, devices_dict):
    """
    python对象写入csv
    :param filename : csv的文件名
    :param devices_dict : python对象
    """
    csvfile = open(filename, 'w', newline = '')
    csv.writer(csvfile).writerow(devices_dict[0].keys())
    for i in range(len(devices_dict)):
        csv.writer(csvfile).writerow(devices_dict[i].values())
    
    csvfile.close()
    
app = Sanic("Sanic IoT Demo")

def get_data():
    return csv2dict("test01.csv")
    

# 最简单的方法是全局变量，但要避免多次初始化问题
#devoces_list用数组list存的 [{},{},{},...]
devices_list: list = get_data()
# 处理函数
@app.post("/v1/devices")
async def add_all_device(request):
    # request 包含了请求的所有信息

    # 首先检验请求体的JSON字符串是否符合规则
    if not validate_json_schema(request.json,device_schema):
        return json({"status":400,"message":"request json is not valid"}, status=400)

    # 判断设备是否已经存在（用device_id判断），device_dict用数组存储
    for device in devices_list:
        if request.json[device_id] == device["device_id"]:
            return json({"status":400,"message":"device json is already exist"}, status=400)

    # 添加并保存数据
    devices_list.append(request.json)
    dict2csv_save(devices_list)

    # 返回成功数据
    return json({"status":200,"message":"create device successfully"})



@app.get("/v1/devices")
async def get_all_device(request): 
    # 返回成功数据
    return json({"status":200,"message":"get all devices list successfully","data":devices_list})
    
@app.get("/v1/devices/<device_id:int>")
async def get_device(request,device_id:int):
    #计数
    n = str(device_id)
    s = n.zfill(5)
    flag1 = 0
    store = {}
    for device in devices_list:
        if s != device["device_id"]:
            flag1 += 1
        else:
            store = device
    if(flag1 == len(devices_list)):
        #错误信息
        return json({"status":404,"message":"device can not be found"}, status=400)
    else:
        return json({"status":200,"message":"get device successfully","data":store})
    
@app.delete("/v1/devices/<device_id:int>")
async def delete_device(request,device_id:int):
    n = str(device_id)
    s = n.zfill(5)
    #计数
    flag1 = 0
    flag2 = 0
    for device in devices_list:
        if s != device["device_id"]:
            flag1 += 1
        else:
            flag2 = flag1
    if(flag1 == len(devices_list)):
        #错误信息
        return json({"status":400,"message":"device can not be found"}, status=400)
    else:
        #把删了指定设备的数组存起来
        del devices_list[flag2]
        return json({"status":200,"message":"delete device successfully"})
    

@app.put("/v1/devices/<device_id:int>")
async def update_device(request,device_id:int):
    n = str(device_id)
    s = n.zfill(5)
    #计数
    flag1 = 0
    for device in devices_list:
        if s == device["device_id"]:
            device = request.json
            flag1 += 1
    if(flag1 == 0):
        #错误信息
        return json({"status":400,"message":"device can not be found"}, status=400)
    else:
        # 返回成功数据
        return json({"status":200,"message":"update device successfully"})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8001")
