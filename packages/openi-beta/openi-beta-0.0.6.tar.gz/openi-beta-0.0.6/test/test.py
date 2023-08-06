from openi.dataset import upload_file

upload_file(
    file = "./output/car_image.zip", # 必填，文件路径(包含文件名)
    username = "chenzh", # 必填，数据集所属项目用户名
    repository = "openi-api-test", # 必填，数据集所属项目名
    token = "c40d9f40d47078c33b431a3ac5156461ceaef95e", #必填，用户启智上获取的令牌token，并对该项目数据集有权限

    cluster = "GPU", # 选填，可填入GPU或NPU，不填写后台默认为NPU
    app_url = "http://192.168.207.34/api/v1/" #选填, 默认为平台地址，用户不用填写，开发测试用
)