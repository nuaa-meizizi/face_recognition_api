#人脸识别接口
## 注册上传图片
* upload 172.31.218.230:8080/upload_know
* POST
* name="fileField"
### 返回
* 上传成功 1
* 重复上传 2
* 上传失败 -1
## 识别图片
* upload 172.31.218.230:8080/upload_unknown
* POST
* name="fileField"
### 返回
* 没有这个人 -1
* 有这个人 userid 
