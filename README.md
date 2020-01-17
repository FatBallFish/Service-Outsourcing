# Service-Outsourcing API Document
Service outsourcing competition - Hotel visual AI solution

[TOC]

# Common Request Json Format

```python
{
  "id":1234,
  "type":"xxx",
  "subtype":"xxxx",
  "data":{
      "key":"value"
  }
}
```

# Common Response Json Format

```python
{
  "id":1234,
  "status":0,
  "message":"successful",
  "data":{
      "key":"value"
  }
}
```

# Param Description

|  Field  |  Type  |                         Description                          |   Caller   |             Example              |
| :-----: | :----: | :----------------------------------------------------------: | :--------: | :------------------------------: |
|   id    |  int   |      事件处理id，整型，请求端发送，接收端返回时原样返回      | 请求、返回 |           "id":123456            |
| status  |  int   | 返回请求处理状态，请求时status填写0。默认返回0时为请求处理成功，若失败返回错误码 |    返回    |            "status":0            |
| message | string | 状态简略信息，若成功调用则返回"successful"，失败返回错误信息 |    返回    |      "message":"successful"      |
|  type   | string |                           请求类型                           |    请求    |          "type":"user"           |
| subtype | string |                          请求子类型                          |    请求    |        "subtype":"login"         |
|  data   |  json  |                   包含附加或返回的请求数据                   | 请求、返回 | "data":{"token":"xxxxxxxxxxxxx"} |

# Start

## Ping - Pong

> **API Description**

`GET`&`POST`

​	此API用于检验是否能够成功连接上服务器，事实上然并卵。

> **URL**

`https://hotel.lcworkroom.cn/api/ping`

> **GET Response Success**

```html
pong
```

> **POST Response Success**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "pong", 
    "data": {}
}
```

> **Notice**

+ 不同的访问方式会获得不同的返回结果
+ 这个API没有实际用处，仅用于让使用者熟悉此文档中API的请求与返回格式
+ 顺便可以判断能不能API有没有部署成功？

# User

## User Register

> **API Description**

`POST`

​	以手机号为字段注册一个新账号

> **URL**

`https://hotel.lcworkroom.cn/api/user/register/`

> **Request Json Text Example**

```python
{
    "id":0,
    "status":0,
    "type":"register",
    "subtype":"phone",
    "data":{
        "username":"13750687010",
        "hash":"cffb7f1eb316fd45bbfbd43082e36f9c",
        "pass":"wlc570Q0"
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default | **Description** |
| :------: | :----: | :----: | :--: | :-----: | :-------------: |
| username | string |   11   |      |         |    账号名称     |
|   hash   | String |   32   |      |         |    校验文本     |
|   pass   | String |        |      |         |    用户密码     |

> **Notice**

+ `hash`生成规则： `hash = MD5(code,rand)`。`code`为短信验证码内容，`rand`为发送短信验证码请求时附带的随机字符串

+ `pass`为用户设置的明文密码，长度由前端决定限制，后端只取其加密结果

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {}
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "Create User Failed", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -200   |
| -4     |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |      Message       | Description  |
| :----: | :----------------: | :----------: |
|  100   | Create User Failed | 创建账号失败 |

## User Login

> **API Description**

`POST`

​	此API用于以手机号作为登录凭证时的登录请求，成功返回token值

> **URL**

`https://hotel.lcworkroom.cn/api/user/login/`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"login",
    "subtype":"pass",
    "data":{
        "username":"13750687010",
        "pass":"wlc570Q0",
        "enduring":0,
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |              **Description**              |
| :------: | :----: | :----: | :--: | :-----: | :---------------------------------------: |
| username | string |   11   |      |         |                 账号名称                  |
|   pass   | String |        |      |         |                 用户密码                  |
| enduring |  int   |   1    |      |    √    | 是否长效登录，`0`为否，`1`为是。默认为`0` |

> **Notice**

+ `enduring`为`0`时，当用户无操作(未使用token向服务器发送任何请求)10min时自动取消其登录状态；为`1`时则保持token不失效(目前设置为永久有效)

+ 若想保持token有效，可使用`Doki`刷新token有效时间
+ 获取的`token`用于后期所有需要用户验证的请求操作。  
+ 账号每登录一次即可获得一个`token`
+ 一个账号同时获得10个以上的`token`时，自动删除早期的`token`，维持`token`数在10以内
+ 获得的`token`未被用于任何操作超过`10min`后将被自动删除（设置为长效token的除外）
+ 若`enduring`传递了非`int`类型数据，则自动为`0`

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "token": "debc454ea24827b67178482fd73f37c3"
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "Incorrect user", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -200   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |          Message           |  Description  |
| :----: | :------------------------: | :-----------: |
|  100   | Error username or password | 无该账号记录  |
|  300   |      Add token failed      | 创建token失败 |

## User Info - Get

> **API Description**

`GET`

​	通过`token`值获取对应用户信息

`POST`

​	通过`token`或`username`值获取对应或指定的用户信息

> **URL**

`https://hotel.lcworkroom.cn/api/user/info/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"info",
    "subtype":"get",
    "data":{
        "username":"13750687010",
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default | **Description** |
| :------: | :----: | :----: | :--: | :-----: | :-------------: |
| username | string |   11   |      |    √    |    账号名称     |

> **Notice**

+ `username`缺省则自动获取`token`对应的用户信息，不缺省可查指定用户的信息

+ 若想保持token有效，可使用`Doki`刷新token有效时间
+ 获取的`token`用于后期所有需要用户验证的请求操作。  
+ 账号每登录一次即可获得一个`token`
+ 一个账号同时获得10个以上的`token`时，自动删除早期的`token`，维持`token`数在10以内
+ 获得的`token`未被用于任何操作超过`10min`后将被自动删除（设置为长效token的除外）
+ `POST`模式可查其他用户信息，`GET`模式只能查询自己的信息

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "token": "debc454ea24827b67178482fd73f37c3"
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status | Method     |
| ------ | ---------- |
| -101   | GET / POST |
| -100   | GET / POST |
| -3     | POST       |
| -2     | POST       |
| -1     | POST       |

> **Local Status**

Null



## User Info - Update

> **API Description**

`POST`

​	通过`token`或`username`值更新对应或指定的用户信息

> **URL**

`https://hotel.lcworkroom.cn/api/user/info/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"info",
    "subtype":"update",
    "data":{
        "username":"13750687010",
        "name":"王凌超",
        "nickname":"FatBallFish",
        "email":"893721708@qq.com",
        "gender":"male"
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |           **Description**            |
| :------: | :----: | :----: | :--: | :-----: | :----------------------------------: |
| username | string |        |      |    √    |               账号名称               |
|  phone   | string |   11   |      |    √    |    用户手机号，**暂不允许被修改**    |
|   name   | string |   20   |  √   |    √    |                王凌超                |
| nickname | string |   20   |  √   |    √    |               用户昵称               |
|  email   | string |   50   |  √   |    √    |               邮箱地址               |
|  gender  | string |   6    |      |    √    | 性别，只有两个选项：`male`、`female` |

> **Notice**

+ `username`用作检验字段，不可被修改
+ `username`缺省则自动更新`token`对应的用户信息，不缺省可更新指定用户的信息，不过需要**拥有管理员权限**，无权限返回`status 102`

+ `phone`字段内容与`username`字段一致，暂不允许被修改
+ `name`字段实质为`first_name`与`last_name`两字段组成，默认将`name`第一个字符给`last_name`，其余都给`first name`（不想考虑复姓与英文名)，不过输出时显示正常
+ `gender`字段若接收了`male`、`female`之外的值，则`gender`字段被忽略，不会对性别信息进行更新

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "token": "debc454ea24827b67178482fd73f37c3"
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "No Such User", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status | Method     |
| ------ | ---------- |
| -101   | GET / POST |
| -100   | GET / POST |
| -3     | POST       |
| -2     | POST       |
| -1     | POST       |

> **Local Status**

| Status |         Message         |   Description    |
| :----: | :---------------------: | :--------------: |
|  100   |      No Such User       |   无该账号记录   |
|  101   | Update UserInfo Failed  | 更新用户信息失败 |
|  102   | No Permission Operation |    无权限操作    |

# Captcha

## Image Captcha - Generate

> **API Description**

`POST`

此API用于生成一个`5位字母数字混合`的图形验证码

成功则返回图片的`base64数据`和一个`5位rand`值。

> **URL**

`https://hotel.lcworkroom.cn/api/captcha`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"img",
    "subtype":"generate",
    "data":{}
}
```

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "imgdata":"iVBORw0yrfmx5m7975n32/23Y+cdf1Rv9oA6.....(以下省略)",
        "rand":"CST43"  # 随机文本
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "No Such User", 
    "data": {}
}
```

> **Notice**

+ `imgdata`为验证码base64图片数据，前端获得数据后进行转码再显示;  

+ `rand`为随机字符串，前端获得验证码后需要将验证码和`rand`文本MD5加密后传给后端进行验证，`hash = MD5(code+rand)`。  
+ 验证码**不区分大小写**，请自行将验证码转换成`全部小写`再进行hash操作。

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -404   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |      Message       |    Description     |
| :----: | :----------------: | :----------------: |
|  100   | Error captcha hash | 错误的验证码`hash` |

## Image Captcha - Validate

> **API Description**

`POST`

此API用于校验用户输入的验证码是否正确，**在目前版本中，此API可以暂时不用**

> **URL**

`https://hotel.lcworkroom.cn/api/captcha`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"img",
    "subtype":"validate",
    "data":{
        "hash":"asddwfw……"
    }
}
```

> **Data Param**

| Field |  Type  | Length | Null | Default |                 **Description**                 |
| :---: | :----: | :----: | :--: | :-----: | :---------------------------------------------: |
| hash  | string |   32   |      |    √    | 图片验证码hash<br />`hash = MD5(imgcode + rand` |

> **Notice**

- `hash`字段的数据要求是用户填写的验证码内容与`rand`文本进行MD5加密获得。即`hash = MD5(code + rand)`

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {}
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "Error captcha hash", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -404   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |      Message       |   Description    |
| :----: | :----------------: | :--------------: |
|  100   | Error captcha hash | 错误的验证码hash |

## Sms Captcha - Generate

> **API Description**

`POST`

此API用于以手机号作为账号进行`注册`或`找回密码`时发送短信验证码

成功则向指定手机发送短信，并返回一个5位`rand`值

> **URL**

`https://hotel.lcworkroom.cn/api/captcha`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"sms",
    "subtype":"generate",
    "data":{
        "phone":"137xxxxxxxx",
        "command_type":1
    }
}
```

> **Data Param**

|    Field     |  Type  | Length | Null | Default |                       **Description**                        |
| :----------: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
|    phone     | string |   11   |      |         |                            手机号                            |
| command_type |  int   |  1-2   |      |    √    |            短信类型。`1`为注册账号;`2`为找回密码             |
|     hash     | string |   32   |      |    √    | 图片验证码hash，**该字段目前不使用**<br />`hash = MD5(imgcode + rand` |

> **Notice**

- `phone`字段需用文本型传递，且只能为中国大陆手机号，不支持国外手机号
- `hash`字段的数据要求是用户填写的验证码内容与`rand`文本进行MD5加密获得。即`hash = MD5(code + rand)`

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "imgdata":"iVBORw0yrfmx5m7975n32/23Y+cdf1Rv9oA6.....(以下省略)",
        "rand":"CST43"  # 随机文本
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 1016, 
    "message": "手机号格式错误", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -404   |
| -204   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status                                                       |
| ------------------------------------------------------------ |
| 具体错误码请看腾讯云[短信错误码](http://cloud.tencent.com/document/product/382/3771 "腾讯短信API文档") |

> **Notice**

+ 腾讯云[短信错误码](http://cloud.tencent.com/document/product/382/3771 "腾讯短信API文档")中的`message`皆为中文字符

## Sms Captcha - Validate

> **API Description**

`POST`

此API用于校验用户输入的验证码是否正确，**在目前版本中，此API可以暂时不用**

> **URL**

`https://hotel.lcworkroom.cn/api/captcha`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"sms",
    "subtype":"validate",
    "data":{
        "hash":"asddwfw……"
    }
}
```

> **Data Param**

| Field |  Type  | Length | Null | Default |                 **Description**                 |
| :---: | :----: | :----: | :--: | :-----: | :---------------------------------------------: |
| hash  | string |   32   |      |    √    | 短信验证码hash<br />`hash = MD5(imgcode + rand` |

> **Notice**

- `hash`字段的数据要求是用户填写的验证码内容与`rand`文本进行MD5加密获得。即`hash = MD5(code + rand)`

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {}
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "Error captcha hash", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -404   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |      Message       |   Description    |
| :----: | :----------------: | :--------------: |
|  100   | Error captcha hash | 错误的验证码hash |

# Token

## Token Doki

> **API Description**

`GET`&`POST`

​	此API用于检验`token`是否有效，若有效并刷新`token`有效时间。

> **URL**

`https://hotel.lcworkroom.cn/api/user/doki/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Response Success Example**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "Successful", 
    "data": {}
}
```

> **Response Failed Example**

```python
{
    "id": -1, 
    "status": -101, 
    "message": "Error token", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status | Method     |
| ------ | ---------- |
| -101   | GET / POST |
| -100   | GET / POST |

> **Local Status**

Null

# Global Status Table

**所有的全局status值皆小于0**

**大于 0 的status值皆为请求局部status值**

| Status |              Message               |             Description             | Method    |
| :----: | :--------------------------------: | :---------------------------------: | --------- |
|   0    |             successful             |            函数处理正确             | POST、GET |
|   -1   |           Error JSON key           |         json文本必需key缺失         | POST      |
|   -2   |          Error JSON value          |          json文本value错误          | POST      |
|   -3   |           Error data key           |      data中有非预料中的key字段      | POST      |
|   -4   |             Error Hash             |          Hash校验文本错误           | POST      |
|  -100  |       Missing necessary args       |       api地址中缺少token参数        | POST、GET |
|  -101  |            Error token             |             token不正确             | POST、GET |
|  -102  |  Get userid failed for the token   |       使用token获取userid失败       | POST、GET |
|  -103  |      No permission to operate      |            用户无权操作             | POST      |
|  -104  |       Error device_id token        |         错误的设备id token          | POST      |
|  -200  |    Failure to operate database     | 数据库操作失败，检查SQL语句是否正确 | POST、GET |
|  -201  | Necessary key-value can't be empty |        关键键值对值不可为空         | POST      |
|  -202  |  Missing necessary data key-value  |          缺少关键的键值对           | POST      |
|  -203  |       Arg's value type error       |         键值对数据类型错误          | POST      |
|  -204  |         Arg's value error          |           键值对数据错误            | POST      |
|  -404  |           Unknown Error            |           未知的Redis错误           | POST      |
|  -500  |          COS upload Error          |           COS储存上传失败           | POST      |

------

- `status`传递的错误码类型为整型。

- 手机验证码相关的错误码详见[短信错误码](http://cloud.tencent.com/document/product/382/3771 "腾讯短信API文档")