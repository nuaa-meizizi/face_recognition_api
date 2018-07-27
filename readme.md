#人脸识别接口
## 注册上传图片
* 192.168.1.45:8080/upload_know
* POST
* name="fileField"
### 返回
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
        "code": 2, "data":"upload success"
        }
    ```
* 上传失败
    * 检测不到人脸
        ```
            {
                "msg": "NO_FACE", "code": -2
            }
        ```
    * 超过一张脸
        ```
            {
                "msg": "E_MORE_THAN_ONE",
                "code": -1
            }
        ```
## 识别图片
* 192.168.1.45:8080/upload_unknown
* POST
* name="fileField"
### 返回
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
