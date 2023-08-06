import openi
from threading import Thread, current_thread
from concurrent.futures import ThreadPoolExecutor

def upload(filename):
    print(filename)
    s = openi.dataset.upload_file(
        file = filename, # 必填，文件路径(包含文件名)
        username = "chenzh01", # 必填，用户名
        repository = "abcde", # 必填，项目名
        token = "4fc54cd1443f90bd09522cabd0bca981671bbc48", #必填，启智上获取的令牌token
        
        cluster = "NPU", # 选填，可填入GPU或NPU，不填写后台默认为NPU
        app_url = "http://192.168.207.34:8110/api/v1/" #选填, 默认为平台地址，用户不用填写，开发测试用
    )
    print(s)

filelist =["./output/data1.zip","./output/data2.zip","./output/data3.zip"]

executor = ThreadPoolExecutor(max_workers=3)

for i in range(3):
  future_a = executor.submit(upload, filelist[i])

print("something")