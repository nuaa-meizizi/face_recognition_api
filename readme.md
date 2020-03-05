# 人脸识别接口
美滋滋战队2018年软件杯车载APP赛题的人脸识别api，两年后运行还是能运行成功，挺惊喜的，哈哈哈。

* [美滋滋战队-软件杯2018-智能车载app演示视频](https://www.bilibili.com/video/av25826292/)
* [美滋滋战队-软件杯2018-智能车载app演示视频-2](https://www.bilibili.com/video/av25826292/?p=2)

功能主要有两个，一个是上传人脸图片，一个是识别人脸，可用于身份认证，人脸识别登陆。

## 环境
* Python 3.3+ or Python 2.7
* macOS or Linux (Windows not officially supported, but might work)
* dlib
    * dlib的安装可能会卡壳，可以参考[如何在macOS或者Ubuntu上安装dlib](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
* face_recognition
## 安装
* 安装参考[face_recognition](https://github.com/ageitgey/face_recognition)
* 安装成功的标志
    ```
        import dlib
        import face_recognition
    ```
    可以成功运行
* python的`bottle`框架
## 使用方式
命令行运行`python main.py`,bash显示
```
Bottle v0.13-dev server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:设置的端口号/
Hit Ctrl-C to quit.

```
打开浏览器`127.0.0.1:设置的端口号`,如果部署在云服务器则需要开通相应端口，由于云服务器的配置可能不能跑dlib和face_recognition，所以使用有GPU的机器，可以通过内网穿透来访问有GPU的机器，[内网穿透 frp 远程访问内网机器](https://blog.erestu.top/archives/200.html)。
### 细节
本项目有两个接口，
* `upload_know`,上传人脸，在核实图片中只有一个人脸且人脸ID不重复之后将提取的人脸特征加入到已知人脸库`upload/encoding`中，因为提取特征需要好一点时间，所以直接存储人脸特征。随后启动knn训练函数训练新的模型。
* `upload_unknown`,识别人脸，识别成功会返回相应的人脸ID。
## 待改进的地方
* 活体检测
    * 添加[眨眼识别](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
* knn模型的训练方式
    * 设置定期训练
* 还有一些写的不规范，希望大家提点建议，嘻嘻

## 接口
### 注册上传图片
* 127.0.0.1:设置的端口号/upload_know
* POST
* name="fileField"
#### 返回
* 上传成功
    ```
    {
        "code": 0,
        "data": "upload success"
    }
    ```
* 重复上传
    ```
    {
        "msg": "already_upload",
        "code": 2,
        "data":"upload success"
    }
    ```
* 上传失败
    * 检测不到人脸
        ```
            {
                "msg": "NO_FACE",
                "code": -2
            }
        ```
    * 超过一张脸
        ```
            {
                "msg": "E_MORE_THAN_ONE",
                "code": -1
            }
        ```
### 识别图片
* 127.0.0.1:设置的端口号/upload_unknown
* POST
* name="fileField"
#### 返回
* 检测不到人脸
    ```
        {
            "msg": "NO_FACE",
            "code": -2
        }
    ```
* 超过一张脸
    ```
        {
            "msg": "E_MORE_THAN_ONE",
            "code": -1
        }
    ```
* 没有这个人
    ```
        {
            "code": 0,
            "data": "unknown"
        }
    ```
* 有这个人
    ```
        {
            "code": 0,
            "data": "011010112"
        }
    ```
### 致谢
* 严重搬运 [face_recognition](https://github.com/ageitgey/face_recognition)
* face_recognition的更多用法 [Github开源人脸识别项目face_recognition](https://zhuanlan.zhihu.com/p/45827914)