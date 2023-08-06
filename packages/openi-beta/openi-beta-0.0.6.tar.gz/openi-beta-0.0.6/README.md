# OpenI PyPi

> PYPI package for 启智AI协作平台。

启智平台提供的Python工具包，使用户能在本地上传数据集。

## 安装

*适配python3.6及以上版本*
```bash
pip install openi
```

## 使用说明

- 确保您拥有此数据集（项目）的权限，`username`参数为数据集的创建者，即项目所属用户/组织的名称
- 使用前请在平台个人设置中获取token：[点击跳转token获取界面](https://openi.pcl.ac.cn/user/settings/applications)
- 当前版本为了方便用户本地上传数据集，建议在本地使用，后续版本将适配隐藏token参数、代码仓配置及云脑任务

## 本地上传数据集示例

```python
from openi.dataset import upload_file

upload_file(
    file = "", # 必填，文件路径(包含文件名，支持windows文件路径如d:\\xxx)
    username = "", # 必填，数据集所属项目owner用户名
    repository = "", # 必填，数据集所属项目名称
    token = "", #必填，用户启智上获取的令牌token，并对该项目数据集有权限
    
    cluster = "" # 选填，可填入GPU或NPU，不填写后台默认为NPU
    )
```
![alt](./media/4.png)