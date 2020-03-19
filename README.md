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

`https://hotel.lcworkroom.cn/api/ping`/

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

# Token

**用户许可类**

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

# User

**用户类**

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

+ `hash`生成规则： `hash = MD5(code+rand)`。`code`为短信验证码内容，`rand`为发送短信验证码请求时附带的随机字符串

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

## User Login - Password

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

+ `pass`为明文密码
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

| Status |     Message      |  Description   |
| :----: | :--------------: | :------------: |
|  100   |   No such user   |  无该账号记录  |
|  101   | Password not set | 用户密码未设置 |
|  102   |  Error password  |  用户密码错误  |
|  300   | Add token failed | 创建token失败  |

## User Login - Sms

> **API Description**

`POST`

​	此API用于以手机号作为登录凭证时的登录请求，成功返回token值以及登录状态`login_type`

> **URL**

`https://hotel.lcworkroom.cn/api/user/login/`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"login",
    "subtype":"sms",
    "data":{
        "username":"13750687010",
        "hash":"23jjf455...",
        "enduring":0,
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |              **Description**              |
| :------: | :----: | :----: | :--: | :-----: | :---------------------------------------: |
| username | string |   11   |      |         |                 账号名称                  |
|   hash   | String |        |      |         |                 校验文本                  |
| enduring |  int   |   1    |      |    √    | 是否长效登录，`0`为否，`1`为是。默认为`0` |

> **Notice**

+ `hash`生成规则： `hash = MD5(code+rand)`。`code`为短信验证码内容，`rand`为发送短信验证码请求时附带的随机字符串
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
        "token": "debc454ea24827b67178482fd73f37c3",
        "login_type":"create"
    }
}
```

> **Notice**

+ `login_type`取值有：`create`、`login`
  + `create`：用户原先不存在，自动创建
  + `login`：用户已存在，自动登录

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
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |      Message       |  Description  |
| :----: | :----------------: | :-----------: |
|  100   | Create User Failed | 创建用户失败  |
|  300   |  Add token failed  | 创建token失败 |

## User Info - Get（有修改）

> **API Description**

`GET`

​	通过`token`值获取对应用户信息

`POST`

​	通过`token`（url参数）或`username`值（POST字段）获取对应或指定的用户信息

**修改：**

**2020年1月26日12:11:01**

**1.更新信息返回**

**2.已修改请求返回值的错误**

**2020年2月19日23:53:05**

返回数据中新增`if_face`字段，类型为`boolean`，用于判断此用户是否已注册了人脸

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

+ `token`为必传字段，不论是否以`token`获取用户信息
+ 若`token`与`username`同时存在，则查询`username`对应用户信息
+ `username`缺省则自动获取`token`对应的用户信息，不缺省可查指定用户的信息
+ `POST`模式可查其他用户信息，`GET`模式只能查询自己的信息
+ **返回信息中，新增ID字段，用于查询实名认证与人脸认证（新增）**

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "id": 3, 
        "username": "13750687010", 
        "nickname": "FatBallFish", 
        "email": "893721708@qq.com", 
        "phone": "13750687010",
        "ID": "33108219991127089X", 
        "if_face":true
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

| Status |   Message    | Description  |
| :----: | :----------: | :----------: |
|  100   | No Such User | 无该账号记录 |

## User Info - Update

> **API Description**

`POST`

​	通过`token`或`username`值更新对应或指定的用户信息

**--修改日志--**

**2020年2月13日00:13:40**

+ 将`real_auth_id`和`face_id`字段改为Null字段，若将这两个字段设置null，表示解绑实名认证库与人脸认证库。且若实名认证库解绑，人脸认证库自动解绑，反之不会。

**2020年1月28日01:00:21**

+ 可更新字段中增加了`face_id`，`real_auth_id`两个字段

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
        "nickname":"FatBallFish",
        "email":"893721708@qq.com",
        "real_auth_id":"33108219991127089X"
    }
}
```

> **Data Param**

|    Field     |  Type  | Length | Null | Default |        **Description**         |
| :----------: | :----: | :----: | :--: | :-----: | :----------------------------: |
|   username   | string |        |      |    √    |            账号名称            |
|    phone     | string |   11   |      |    √    | 用户手机号，**暂不允许被修改** |
|   nickname   | string |   20   |  √   |    √    |            用户昵称            |
|    email     | string |   50   |  √   |    √    |            邮箱地址            |
| real_auth_id | string |   18   |  √   |    √    |    实名认证库id（身份证号）    |
|   face_id    | string |   18   |  √   |    √    |     人脸数据id（身份证号）     |

> **Notice**

+ `username`用作检验字段，不可被修改
+ `username`缺省则自动更新`token`对应的用户信息，不缺省可更新指定用户的信息，不过需要**拥有管理员权限**，无权限返回`status 102`
+ `phone`字段内容与`username`字段一致，暂不允许被修改
+ `email`字段在后端不会进行检验格式的正确与否，若需要请前端自行检验
+ `real_auth_id`若不存在返回`status 103`状态
+ `face_id`若不存在返回`status 104`状态
+ 建议不要自行修改`face_id`字段值，因为在注册人脸的时候，我会先判断是否已实名，若真则以实名的身份证号作为人脸数据的id值，若假则返回`此用户未实名`之类的错误

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
    "message": "No Such User", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |         Message         |   Description    |
| :----: | :---------------------: | :--------------: |
|  100   |      No Such User       |   无该账号记录   |
|  101   | Update UserInfo Failed  | 更新用户信息失败 |
|  102   | No Permission Operation |    无权限操作    |
|  103   |      No Such Face       |   无此人脸信息   |
|  104   |    No Such RealAuth     | 无此实名认证信息 |

## User Search

> **API Description**

`GET`

​	通过`keywords`或`user_id`值获取对应用户基本信息

​	通过`token`（url参数）或`username`值（POST字段）获取对应或指定的用户信息

> **URL**

`https://hotel.lcworkroom.cn/api/user/search/?param=`

> **URL Param**

|  Field   |  Type  | Length | Null | Default |                       **Description**                        |
| :------: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
| keywords | string |        |      |         | 查询关键字，可查询用户昵称与用户名<br />规则：模糊匹配用户昵称，精确匹配用户名，两者并集 |
| user_id  | string |        |      |         |     查询用户名，精确匹配。当传递此参数时`keywords`将失效     |

> **Response Success Example**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 2, 
        "list": [
            {
                "user_id": "13750687010", 
                "nickname": "FatBallFish"
            }, 
            {
                "user_id": "13858181317", 
                "nickname": "AmiKara"
            }
        ]
    }
}
```

> **Notice**

+ 总想说点什么但忘词了

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
| -100   | GET / POST |

> **Local Status**

null

## User Password - Forget

> **API Description**

`POST`

​	通过手机短信验证码形式找回用户密码**（仅限于用手机号注册的账号）**

> **URL**

`https://hotel.lcworkroom.cn/api/user/password/`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"password",
    "subtype":"forget",
    "data":{
        "username":"13750687010",
        "hash":"h2xf24rf..",
        "pass":"wanglingchao"
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default | **Description** |
| :------: | :----: | :----: | :--: | :-----: | :-------------: |
| username | string |   11   |      |         | 账号(即手机号)  |
|   hash   | string |   32   |      |         |    教研文本     |
|   pass   | string |        |      |         |     新密码      |

> **Notice**

+ `hash`生成规则： `hash = MD5(code,rand)`。`code`为短信验证码内容，`rand`为发送短信验证码请求时附带的随机字符串。**发送短信时需将短信接口中`command_type`设置为`2`**
+ `pass`为用户要设置的新密码，可与原密码相同且不会提示
+ 改密成功后该账户往期的所有`token`记录将被清空，即强制退出用户在所有设备的登录状态，包括长效登录

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
    "message": "No Such User", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -4     |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |   Message    | Description  |
| :----: | :----------: | :----------: |
|  100   | No Such User | 无该账号记录 |

## User Password - Change

> **API Description**

`POST`

​	通过验证用户名和原密码进行用户新密码修改

> **URL**

`https://hotel.lcworkroom.cn/api/user/password/`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"password",
    "subtype":"change",
    "data":{
        "username":"13750687010",
        "old_pass":"wanglingchao",
        "new_pass":"wanglingchao123"
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default | **Description** |
| :------: | :----: | :----: | :--: | :-----: | :-------------: |
| username | string |   11   |      |         | 账号(即手机号)  |
| old_pass | string |        |      |         |     原密码      |
| new_pass | string |        |      |         |     新密码      |

> **Notice**

+ `old_pass`为用户要设置的原密码，输入错误返回`status 100`状态码且改密失败
+ `new_pass`为用户要设置的新密码，可与原密码相同且不会提示
+ 改密成功后该账户往期的所有`token`记录将被清空，即强制退出用户在所有设备的登录状态，包括长效登录

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
    "message": "No Such User", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |                Message                 |    Description     |
| :----: | :------------------------------------: | :----------------: |
|  100   |              No such user              |     没有此用户     |
|  101   |            Password not set            |   用户密码未设置   |
|  102   |             Error password             |     错误的密码     |
|  103   | Password cannot be the same as account | 密码不能与账号一致 |

## User Portrait - Get（重要更新）

> **API Description**

`GET`

​	通过传递`username`参数获取指定用户头像，返回头像二进制数据

**修改**

**2020年2月19日23:49:20**

此API将全线重定向至`/api/pic/get/users/?name=`,详情请看[Pic - Get](#Pic - Get)API，此API将在后期版本不再维护，若出现bug请使用[Pic - Get](#Pic - Get)API

>  **URL**

`https://hotel.lcworkroom.cn/api/user/portrait/?username=`

此API将全线重定向至`/api/pic/get/users/?name=`,详情请看[Pic](#Pic - Get)API

> **URL Param**

|  Field   |  Type  | Length | Null | Default | **Description** |
| :------: | :----: | :----: | :--: | :-----: | :-------------: |
| username | string |   11   |      |         |      账号       |

> **Notice**

+ `username`字段不存在或者字段值错误将返回参数错误提示图片`error.jpg`
+ 访问此API的ip若非允许内的ip将被阻截（后期想改成返回禁止访问图片`ban.jpg`）
+ 若用户未上传过头像时将返回默认头像数据

## User Portrait - Upload（重要更新）

> **API Description**

`POST`

​	通过传递的`token`参数以及图片base64数据对指定用户进行图片更新

**修改**

**2020年2月19日23:54:34**

此API将与[Pic - Upload](#Pic - Upload)适配，新增`if_local`与`type`字段，并将所有请求转接至[Pic - Upload](#Pic - Upload)，后期建议使用新API，此API后期也许会被取消

> **URL**

`https://hotel.lcworkroom.cn/api/user/portrait/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"portrait",
    "subtype":"upload",
    "data":{
        "base64":"...",
    }
}
```

> **Data Param**

|  Field   |  Type   | Length | Null | Default |        **Description**        |
| :------: | :-----: | :----: | :--: | :-----: | :---------------------------: |
|  base64  | string  |        |      |         |        图片base64数据         |
| if_local | boolean |        |      |    √    | 图片是否存在本地，默认为flase |
|   type   | string  |        |      |    √    |   图片后缀名，默认为`user`    |

> **Notice**

+ API自动根据`token`值更新对应用户的头像
+ `base64`数据是否去除头信息都无所谓。（头信息例子：`image/jpg;base64,`)
+ 用户多次上传头像则之前的头像数据将被覆写，只保留最后一次上传的数据
+ `type`中不可包含点`.`，必须由英文字母组成
+ `if_local`用来指定图片上传位置，`false`则上传至COS储存服务器中，网速更快；`true`上传至服务器本地中。若传递的参数非`boolean`型，则默认值为`false`

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "url": "/api/user/portrait/?username=19857160634"
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

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message         |            Description             |
| :----: | :--------------------: | :--------------------------------: |
|  100   |   Error base64 data    |          错误的base64数据          |
|  101   | Upload portrait failed | 上传头像失败（服务器文件存储失败） |

# Captcha

**验证码类**

## Image Captcha - Generate

> **API Description**

`POST`

此API用于生成一个`5位字母数字混合`的图形验证码

成功则返回图片的`base64数据`和一个`5位rand`值。

> **URL**

`https://hotel.lcworkroom.cn/api/captcha/`

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

`https://hotel.lcworkroom.cn/api/captcha/`

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

`https://hotel.lcworkroom.cn/api/captcha/`

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
| command_type |  int   |  1-2   |      |    √    |   短信类型。`1`为注册账号;`2`为找回密码；`3`为账号短信登录   |
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

`https://hotel.lcworkroom.cn/api/captcha/`

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

# RealAuth

**实名认证类**

## RealAuth Create

> **API Description**

`POST`

此API用于创建一个实名认证信息，成功自动与用户绑定，暂不可解绑，并返回`real_auth_id`

> **URL**

`https://hotel.lcworkroom.cn/api/realauth/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"realauth",
    "subtype":"create",
    "data":{
        "id_type":"sfz",
        "id":"33108219991127089X",
        "name":"王凌超",
        "gender":"male",
        "birthday":1580140800.0,
    }
}
```

> **Data Param**

|    Field     |  Type  | Length | Null | Default |                       **Description**                        |
| :----------: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
|   id_type    | string |        |      |         |        身份证件种类，目前只有`sfz`，其他返回`200`错误        |
|      id      | string |   18   |      |         |                          身份证件号                          |
|     name     | string |   30   |      |         |                             姓名                             |
|    gender    | string |   6    |      |         |    年龄，只有`male`和`female`两个选项，其他返回`201`错误     |
|   birthday   | float  |        |      |         |           生日时间戳，精确到日，时分秒信息将被忽略           |
|    nation    | string |   10   |  √   |    √    |                             民族                             |
|   address    | string |  100   |  √   |    √    |                             住址                             |
| organization | string |   30   |  √   |    √    |                           签发机关                           |
|  date_start  | float  |        |  √   |    √    | 证件有效期·起始 时间戳，精确到日，时分秒信息将被忽略，失败返回`202`错误 |
|   date_end   | float  |        |  √   |    √    | 证件有效期·终止 时间戳，精确到日，时分秒信息将被忽略，失败返回`203`错误 |

> **Notice**

- `id`为不可重复字段，若创建的实名认证信息与已有的重复，将返回`100`状态码
- `id_type`、`id`、`name`、`gender`、`birthday`为必填字段，且不能为空，**且创建后无法修改更新**
- `nation`、`address`、`organization`、`date_start`、`date_end`为可选字段，且可为空（不过建议不要为空）
- 各字段的长度限制需由前端校验设置好后再传，否则若有异常会返回`100`状态码
- 后端不校验`date_start`与`date_end`之间的先后逻辑关系，请前端自行校验

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "real_auth_id":"3310821999..."
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -1, 
    "message": "Error JSON key", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |         Message         |   Description    |
| :----: | :---------------------: | :--------------: |
|  100   | Create RealAuth failed  | 创建实名认证失败 |
|  200   | Error id_type |  错误的证件类型  |
| 201 | Error gender | 错误的性别 |
| 202 | Error birthday | 错误的出生年月 |
| 203 | Error date_start | 错误的有效期开始 |
| 204 | Error date_end | 错误的有效期终止 |

## RealAuth Update

> **API Description**

`POST`

此API用于更新与用户绑定的实名认证信息，若用户未绑定实名认证信息，返回`100`状态码

> **URL**

`https://hotel.lcworkroom.cn/api/realauth/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"realauth",
    "subtype":"update",
    "data":{
        "nation":"汉",
        "address":"浙江省临海市...."
		"organization":"临海市公安局",
        "date_start":185551654...
        "date_end":15068956...
    }
}
```

> **Data Param**

|    Field     |  Type  | Length | Null | Default |                       **Description**                        |
| :----------: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
|    nation    | string |   10   |  √   |    √    |                             民族                             |
|   address    | string |  100   |  √   |    √    |                             住址                             |
| organization | string |   30   |  √   |    √    |                           签发机关                           |
|  date_start  | float  |        |  √   |    √    | 证件有效期·起始 时间戳，精确到日，时分秒信息将被忽略，失败返回`202`错误 |
|   date_end   | float  |        |  √   |    √    | 证件有效期·终止 时间戳，精确到日，时分秒信息将被忽略，失败返回`203`错误 |

> **Notice**

- 此API只能更新与用户自身绑定的实名认证信息，若无则返回`100`状态码
- 此API不能更新`id_type`、`id`、`name`、`gender`、`birthday`等字段
- `nation`、`address`、`organization`、`date_start`、`date_end`为可选字段，且可为空（不过建议不要为空）
- 各字段的长度限制需由前端校验设置好后再传，否则若有异常会返回`100`状态码
- 后端不校验`date_start`与`date_end`之间的先后逻辑关系，请前端自行校验

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
    "status": -1, 
    "message": "Error JSON key", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message         |   Description    |
| :----: | :--------------------: | :--------------: |
|  100   | RealAuth not certified |    实名未认证    |
|  200   |     Error date_start/date_end      |  错误的有效期开始/终止  |

## RealAuth - Get

> **API Description**

`POST`

此API用于获取用户绑定的实名认证信息

> **URL**

`https://hotel.lcworkroom.cn/api/realauth/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"realauth",
    "subtype":"get",
    "data":{}
}
```

> **Data Param**

null

> **Notice**

- 此API只能获取与用户自身绑定的实名认证信息，若无则返回`100`状态码

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "id_type": "sfz", 
        "id": "3310821999....", 
        "name": "王凌超", 
        "gender": "male", 
        "nation": "汉", 
        "birthday": 943632000.0, 
        "address": "浙江省临海市....", 
        "organization": "临海市公安局", 
        "date_start": 1467907200.0, 
        "date_end": 1783440000.0
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -1, 
    "message": "Error Json key", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message         | Description |
| :----: | :--------------------: | :---------: |
|  100   | RealAuth not certified | 实名未认证  |

# Face

**人脸数据类**

## Group - Create

> **API Description**

`POST`

此API用于创建一个人员库，成功返回人员库id

**此API有权限限制，仅管理员可用，其他人调用此API将返回`-103`状态码**

> **URL**

`https://hotel.lcworkroom.cn/api/face/group/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"group",
    "subtype":"create",
    "data":{
        "group_name": "西和5幢人员库",
        "group_content": "浙江科技学院西和公寓5幢人脸数据库"
    }
}
```

> **Data Param**

|     Field     |  Type  | Length | Null | Default | **Description** |
| :-----------: | :----: | :----: | :--: | :-----: | :-------------: |
|  group_name   | string |   20   |      |         |   人员库名称    |
| group_content | string |        |  √   |         |   人员库描述    |

> **Notice**

- `group_name`为不可重复字段，若创建的人员库名称与已有的重复，将返回`100`状态码

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "group_id":5
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -103, 
    "message": "No Permission Operate", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -103   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |          Message           |   Description    |
| :----: | :------------------------: | :--------------: |
|  100   | FaceGroup name has existed | 人员库名称已存在 |
|  101   |  Create FaceGroup Failed   |  创建人员库失败  |

## Group - Delete

> **API Description**

`POST`

此API用于以`group_id`或者`group_name`为检索条件删除一个人员库，并同步删除里面所有的人脸数据

**此API有权限限制，仅管理员可用，其他人调用此API将返回`-103`状态码**

> **URL**

`https://hotel.lcworkroom.cn/api/face/group/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"group",
    "subtype":"delete",
    "data":{
        "group_id":5,
        "group_name": "西和5幢人员库"
    }
}
```

> **Data Param**

|   Field    |  Type  | Length | Null | Default | **Description** |
| :--------: | :----: | :----: | :--: | :-----: | :-------------: |
|  group_id  |  int   |        |      |    √    |    人员库id     |
| group_name | string |   20   |      |    √    |   人员库名称    |

> **Notice**

- `group_id`与`group_name`二选一即可，若都传值过来，则选择`group_id`为检索条件。
- `group_id`字段类型为`int`型，但若传递了整型字符串过来，也会自动转为`int`类型，转换失败返回`100`状态码
- 若两个参数都没传过来，返回`101`状态码

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
    "status": -103, 
    "message": "No Permission Operate", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -103   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |           Message           |        Description         |
| :----: | :-------------------------: | :------------------------: |
|  100   |       Error Group ID        |       错误的人员库ID       |
|  101   | Need Group ID or Group name | 需要人员库ID或者人员库名称 |
|  102   |        No such Group        |         无此人员库         |
|  103   |     Delete Group Failed     |       删除人员库失败       |

## Group - Update

> **API Description**

`POST`

此API用于以`group_id`或者`group_name`为检索条件更新一个人员库描述（`group_content`）

**此API有权限限制，仅管理员可用，其他人调用此API将返回`-103`状态码**

> **URL**

`https://hotel.lcworkroom.cn/api/face/group/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"group",
    "subtype":"update",
    "data":{
        "group_id":5,
        "group_name": "西和5幢人员库",
        "group_content":"浙江科技学院西和公寓5幢人脸数据库123"
    }
}
```

> **Data Param**

|     Field     |  Type  | Length | Null | Default | **Description** |
| :-----------: | :----: | :----: | :--: | :-----: | :-------------: |
|   group_id    |  int   |        |      |    √    |    人员库id     |
|  group_name   | string |   20   |      |    √    |   人员库名称    |
| group_content | string |        |      |         |   人员库描述    |

> **Notice**

- `group_id`与`group_name`二选一即可，若都传值过来，则选择`group_id`为检索条件。
- `group_id`字段类型为`int`型，但若传递了整型字符串过来，也会自动转为`int`类型，转换失败返回`100`状态码
- 若两个参数都没传过来，返回`101`状态码
- 只能修改`group_content`的值，`group_name`与`group_id`只作为检索条件使用

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
    "status": -103, 
    "message": "No Permission Operate", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -103   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |           Message           |        Description         |
| :----: | :-------------------------: | :------------------------: |
|  100   |       Error Group ID        |       错误的人员库ID       |
|  101   | Need Group ID or Group name | 需要人员库ID或者人员库名称 |
|  102   |        No such Group        |         无此人员库         |

## Group - Get

> **API Description**

`POST`

此API用于以`group_id`或者`group_name`为检索条件获取一个人员库信息

> **URL**

`https://hotel.lcworkroom.cn/api/face/group/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"group",
    "subtype":"get",
    "data":{
        "group_id":5,
        "group_name": "西和5幢人员库"
    }
}
```

> **Data Param**

|     Field     |  Type  | Length | Null | Default | **Description** |
| :-----------: | :----: | :----: | :--: | :-----: | :-------------: |
|   group_id    |  int   |        |      |    √    |    人员库id     |
|  group_name   | string |   20   |      |    √    |   人员库名称    |
| group_content | string |        |      |         |   人员库描述    |

> **Notice**

- `group_id`与`group_name`二选一即可，若都传值过来，则选择`group_id`为检索条件。
- `group_id`字段类型为`int`型，但若传递了整型字符串过来，也会自动转为`int`类型，转换失败返回`100`状态码
- 若两个参数都没传过来，返回`101`状态码

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "group_id": 5, 
        "group_name": "西和5幢人员库", 
        "group_content": "浙江科技学院西和公寓5幢人脸数据库"
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -103, 
    "message": "No Permission Operate", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |           Message           |        Description         |
| :----: | :-------------------------: | :------------------------: |
|  100   |       Error Group ID        |       错误的人员库ID       |
|  101   | Need Group ID or Group name | 需要人员库ID或者人员库名称 |
|  102   |        No such Group        |         无此人员库         |

## Group - List

> **API Description**

`POST`

此API用于返回所有人员库信息

> **URL**

`https://hotel.lcworkroom.cn/api/face/group/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"group",
    "subtype":"list",
    "data":{}
}
```

> **Data Param**

null

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 2, 
        "list": [
            {
                "group_id": 5, 
                "group_name": "西和5幢人员库", 
                "group_content": "浙江科技学院西和公寓5幢人脸数据库"
            }, 
            {
                "group_id": 6, 
                "group_name": "西和6幢人员库", 
                "group_content": "浙江科技学院西和公寓6幢人脸数据库"
            }
        ]
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -103, 
    "message": "No Permission Operate", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

null

## Face - Register（新修改）

> **API Description**

`POST`

此API用于以`base64`为人脸数据注册用户的人脸信息，成功返回`face_id(身份证号)`

**调用此API前需保证用户已进行实名认证，否则将返回`100`状态码**



**修改**

**2020年3月12日21:04:08**

新增`104`状态码，出现条件为人脸上有遮罩物，例如口罩；

补充了`-101`和`-100`全局错误返回码，功能里已存在，只是忘记写进文档中

**2020年2月2日00:03:20**

新增注册时人脸个数判断，详情看api的局部返回值

> **URL**

`https://hotel.lcworkroom.cn/api/face/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"face",
    "subtype":"register",
    "data":{
        "base64":"sdfj32...",
        "db": 1,
        "content":"人脸数据描述"
    }
}
```

> **Data Param**

|  Field  |  Type  | Length | Null | Default |   **Description**   |
| :-----: | :----: | :----: | :--: | :-----: | :-----------------: |
| base64  | string |        |      |         |   图片base64文本    |
|   db    |  int   |        |      |    √    | 人员库id，默认为`1` |
| content | string |        |      |    √    |    人脸数据描述     |

> **Notice**

- 用户若未进行过**实名认证**，则返回`100`状态码
- 用户可重复调用此API对人脸数据进行覆盖注册，若图片中无人脸数据或人脸数据过多将返回下面状态码，原人脸数据不受影响。
- **确保人脸图像中只有一张人脸数据，无人脸返回`102`状态码，大于1张人脸返回`103`状态码**
- `db`为人员库id，可缺省，若有不可为`null`，默认为`1`(默认人员库)，详情人员库信息可通过[获取人员库列表API](#Group - List)获取
- `content`为人员描述信息，可缺省，若有不可为`null`，默认为空文本
- 若两个参数都没传过来，返回`101`状态码
- 只能修改`group_content`的值，`group_name`与`group_id`只作为检索条件使用

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "face_id":"3310821999..."
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "No Permission Operate", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |           Message            |    Description     |
| :----: | :--------------------------: | :----------------: |
|  100   |    Faces group not exist     |    人员库不存在    |
|  101   |     Register face failed     |  注册人员数据失败  |
|  102   |    No face data in base64    |  图片中无人脸数据  |
|  103   | Too much face data in base64 | 图片中人脸数据过多 |
|  104   |     No mask on the face      |  脸部不能有遮罩物  |

## Face - Find（新修改）

> **API Description**

`POST`

此API用于以`base64`为人脸数据查找指定人员库中的的人脸信息，成功返回人脸相关信息

**此API慎用，因为会返回用户的隐私信息**



**修改**

**2020年3月12日21:03:06**

在完整数据返回的部分新增`mask`字段，用来判断人脸是否有脸部遮罩物

补充了`-101`和`-100`全局错误返回码，功能里已存在，只是忘记写进文档中

**2020年2月2日00:05:55**

新增人脸数的判断，修复只能识别一张人脸的情况

更新返回的json文本格式

> **URL**

`https://hotel.lcworkroom.cn/api/face/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"face",
    "subtype":"find",
    "data":{
        "base64":"sdfj32...",
        "db": 1,
        "ret_type":0
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |                      **Description**                      |
| :------: | :----: | :----: | :--: | :-----: | :-------------------------------------------------------: |
|  base64  | string |        |      |         |                      图片base64文本                       |
|    db    |  int   |        |      |    √    |                   人员库id，默认为`-1`                    |
| ret_type |  int   |        |      |    √    | 数据返回模式：`0 精简返回`,`1 全部返回`，默认`0 精简返回` |

> **Notice**

- **没有人脸将返回`100`错误**
- `db`为人员库id，可缺省，若有不可为`null`，默认为`-1`(所有人员库)，详情人员库信息可通过[获取人员库列表API](#Group - List)获取
- `ret_type`为数据返回模式，`0`为精简返回，`1`为完全返回。**后期打算将`1 全部返回`限制为仅管理员可用，目前无限制**

> **Response Data Param**
>
> **0 精简返回**

|   Field   |  Type   | Length | Null | Default |               **Description**               |
| :-------: | :-----: | :----: | :--: | :-----: | :-----------------------------------------: |
|    ID     | string  |   18   |      |         |  人脸数据id（身份证号），若没找到默认为""   |
|   name    | string  |        |      |    √    |         人脸姓名，若没找到默认为""          |
| liveness  | boolean |        |      |         | 活体检测，`true`为真人，`false`为照片等假人 |
| threshold |  float  |        |      |         |       人脸相似度，若没找到默认为0.00        |

> **Notice**

1. 返回的`ID`为私密信息，请慎用
2. 若人员库中未找到此人信息，仍然会返回人脸数据信息，但`ID`,`name`将为空字符串，`threshold`为`0.00`，`liveness`仍然有效
3. `threshold`精确到小数点后两位，最高为`1(完全匹配)`，最低为`0(匹配失败时将会返回)`，一般匹配程度超过0.8才算匹配成功返回匹配值，否则一律返回`0.00`

> **Example**

```python
{
    "num": 2, 
    "list": [
        {
            "ID": "",
            "name": "", 
            "liveness": false, 
            "threshold": 0.0
        }, 
        {
            "ID": "", 
            "name": "", 
            "liveness": true, 
            "threshold": 0.0
        }
    ]
}
```

> **Notice**

+ 在简要返回中，若图片中的人脸数据有部分识别失败时，并不能准确判断。但在完全返回中可以进行判断
+ 若人脸数据有部分识别失败，`ID`为"",`name`为“”，`liveness`为false`threshold`为0.0
+ 识别失败与匹配失败不同，但在简单返回中返回值类似，唯一区别在于`liveness`，但若识别的为照片中人物且识别失败，两者返回值将无法分辨。
+ 识别失败属于程序算法中问题，暂无更优解，匹配失败是指人脸数据不在人员库中
+ 上面例子中，第一组数据为识别失败，第二组数据为匹配失败

> **Response Data Param**
>
> **1 完全返回**

|    Field     |    Type    | Length | Null | Default |                   **Description**                   |
| :----------: | :--------: | :----: | :--: | :-----: | :-------------------------------------------------: |
|      ID      |   string   |   18   |      |         |      人脸数据id（身份证号），若没找到默认为""       |
|     name     |   string   |        |      |    √    |             人脸姓名，若没找到默认为""              |
|     age      |    int     |        |      |         |           人脸预测年龄（非人脸真实年龄）            |
|   liveness   |  boolean   |        |      |         |     活体检测，`true`为真人，`false`为照片等假人     |
|  threshold   |   float    |        |      |         |           人脸相似度，若没找到默认为0.00            |
|    gender    |   string   |        |      |         |     用户性别，仅两种选择：`male`男，`female`女      |
|   top_left   | tuple/list |        |      |         |               人脸出现位置左上角坐标                |
|  top_right   | tuple/list |        |      |         |               人脸出现位置右上角坐标                |
| bottom_left  | tuple/list |        |      |         |               人脸出现位置左下角坐标                |
| bottom_right | tuple/list |        |      |         |               人脸出现位置右下角坐标                |
|     mask     |  boolean   |        |      |         | **新增字段**，脸部是否有遮罩物，true为有，false为无 |

> **Notice**

1. 完全返回中有很多私密信息，请慎用！
2. 若人员库中未找到此人信息，仍然会返回人脸数据信息，但`ID`,`name`将为空字符串，`threshold`为`0.00`，`liveness`仍然有效
3. `threshold`精确到小数点后两位，最高为`1(完全匹配)`，最低为`0(匹配失败时将会返回)`，一般匹配程度超过0.8才算匹配成功返回匹配值，否则一律返回`0.00`
4. **mask字段为新增检测信息，若识别失败此字段会返回null值**

> **Example**

```python
{
    "num": 2, 
    "list": [
        {
            "ID": "", 
            "age": null, 
            "threshold": 0.0, 
            "gender": "", 
            "liveness": false, 
            "top_left": [61, 94], 
            "top_right": [157, 94], 
            "bottom_left": [61, 189], 
            "bottom_right": [157, 189], 
            "name": "",
            "mask": true
        }, 
        {
            "ID": "", 
            "age": 26, 
            "threshold": 0.0,
            "gender": "male", 
            "liveness": true, 
            "top_left": [209, 60], 
            "top_right": [308, 60], 
            "bottom_left": [209, 159], 
            "bottom_right": [308, 159], 
            "name": "",
            "mask":false
        }
    ]
}
```

> **Notice**

+ 在完全返回中，若图片中的人脸数据有部分识别失败时，`age`字段将返回null值，但人脸矩阵依旧有数据
+ 若人脸数据有部分识别失败，`ID`为`""`，`age`为`null`，`gender`为`""`，`name`为`""`，`liveness`为`false`，`threshold`为`0.0`
+ 识别失败与匹配失败不同，识别失败属于程序算法中问题，暂无更优解，匹配失败是指人脸数据不在人员库中
+ 上面例子中，第一组数据为识别失败，第二组数据为匹配失败

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        返回数据见上方example
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "No face authentication", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message         |   Description    |
| :----: | :--------------------: | :--------------: |
|  100   | No face data in base64 | 图片中无人脸信息 |

## Face - Verify（新修改）

> **API Description**

`POST`

此API用于以`base64`为人脸数据核验是否与用户人脸认证信息匹配，成功返回相关信息

**没有人脸将返回`101`错误**



**修改**

**2020年3月12日21:05:08**

在完整数据返回的部分新增`mask`字段，用来判断人脸是否有脸部遮罩物

补充了`-101`和`-100`全局错误返回码，功能里已存在，只是忘记写进文档中

**2020年2月2日00:22:20**

新增多张人脸时返回`102`状态码

> **URL**

`https://hotel.lcworkroom.cn/api/face/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"face",
    "subtype":"verify",
    "data":{
        "base64":"sdfj32...",
        "ret_type":0
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |                      **Description**                      |
| :------: | :----: | :----: | :--: | :-----: | :-------------------------------------------------------: |
|  base64  | string |        |      |         |                      图片base64文本                       |
| ret_type |  int   |        |      |    √    | 数据返回模式：`0 精简返回`,`1 全部返回`，默认`0 精简返回` |

> **Notice**

- 若用户未进行过人脸认证，返回`100`状态码。
- **没有人脸将返回`101`错误，多张人脸返回`102`错误**
- `ret_type`为数据返回模式，`0`为精简返回，`1`为完全返回。**后期打算将`1 全部返回`限制为仅管理员可用，目前无限制**

> **Response Data Param**
>
> **0 精简返回**

|   Field   |  Type   | Length | Null | Default |                **Description**                |
| :-------: | :-----: | :----: | :--: | :-----: | :-------------------------------------------: |
|  result   | boolean |        |      |         | 匹配结果，`true`为匹配成功，`false`为匹配失败 |
| liveness  | boolean |        |      |         |  活体检测，`true`为真人，`false`为照片等假人  |
| threshold |  float  |        |      |         |        人脸相似度，若没找到默认为0.00         |

> **Notice**

1. 若人员库中未找到此人信息，`result`为`false`，`threshold`为`0.00`，`liveness`仍然有效
2. `result`为真时并不表示通过验证，请结合`liveness`字段进行判断
3. `threshold`精确到小数点后两位，最高为`1(完全匹配)`，最低为`0(匹配失败时将会返回)`，一般匹配程度超过0.8才算匹配成功返回匹配值，否则一律返回`0.00`
4. **mask字段为新增检测信息，若识别失败此字段会返回null值**

> **Example**

```python
{
    "result": true, 
    "liveness": true,
    "threshold": 0.98
}
```



> **Response Data Param**
>
> **1 完全返回**

|    Field     |    Type    | Length | Null | Default |                   **Description**                   |
| :----------: | :--------: | :----: | :--: | :-----: | :-------------------------------------------------: |
|    result    |  boolean   |        |      |         |    匹配结果，`true`为匹配成功，`false`为匹配失败    |
|      ID      |   string   |   18   |      |         |      人脸数据id（身份证号），若没找到默认为""       |
|     age      |    int     |        |      |         |           人脸预测年龄（非人脸真实年龄）            |
|   liveness   |  boolean   |        |      |         |     活体检测，`true`为真人，`false`为照片等假人     |
|  threshold   |   float    |        |      |         |           人脸相似度，若没找到默认为0.00            |
|    gender    |   string   |        |      |         |     用户性别，仅两种选择：`male`男，`female`女      |
|   top_left   | tuple/list |        |      |         |               人脸出现位置左上角坐标                |
|  top_right   | tuple/list |        |      |         |               人脸出现位置右上角坐标                |
| bottom_left  | tuple/list |        |      |         |               人脸出现位置左下角坐标                |
| bottom_right | tuple/list |        |      |         |               人脸出现位置右下角坐标                |
|     mask     |  boolean   |        |      |         | **新增字段**，脸部是否有遮罩物，true为有，false为无 |

> **Notice**

1. 若人员库中未找到此人信息，`result`为`false`，`threshold`为`0.00`，`liveness`仍然有效
2. `result`为真时并不表示通过验证，请结合`liveness`字段进行判断
3. `threshold`精确到小数点后两位，最高为`1(完全匹配)`，最低为`0(匹配失败时将会返回)`，一般匹配程度超过0.8才算匹配成功返回匹配值，否则一律返回`0.00`

> **Example**

```python
{
    "result": true,
    "ID": "33108219991127089X", 
    "age": 27, 
    "threshold": 0.98, 
    "gender": "male", 
    "liveness": true, 
    "top_left": [40, 88], 
    "top_right": [162, 88], 
    "bottom_left": [40, 210], 
    "bottom_right": [162, 210]
}
```

> **Notice**

+ 在完全返回中，若图片中的人脸数据有部分识别失败时，`age`字段将返回null值，但人脸矩阵依旧有数据
+ 若人脸数据有部分识别失败，`ID`为`""`，`age`为`null`，`gender`为`""`，`name`为`""`，`liveness`为`false`，`threshold`为`0.0`
+ 识别失败与匹配失败不同，识别失败属于程序算法中问题，暂无更优解，匹配失败是指人脸数据不在人员库中

> **Response Success Example**

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        返回数据见上方example
    }
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "No face authentication", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |           Message            |    Description     |
| :----: | :--------------------------: | :----------------: |
|  100   |    No face authentication    |   人脸信息未认证   |
|  101   |    No face data in base64    |  图片中无人脸信息  |
|  102   | Too much face data in base64 | 图片中人脸数据过多 |

## Face - Mask（新增）

> **API Description**

`POST`

此API用于以`base64`为人脸数据判断画面中的人脸是否有脸部遮罩物，成功返回相关信息

**注意**

此API不会判断人脸身份，仅判断脸部有无遮罩物

> **URL**

`https://hotel.lcworkroom.cn/api/face/mask/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"mask",
    "subtype":"check",
    "data":{
        "base64":"sdfj32...",
    }
}
```

> **Data Param**

| Field  |  Type  | Length | Null | Default | **Description** |
| :----: | :----: | :----: | :--: | :-----: | :-------------: |
| base64 | string |        |      |         | 图片base64文本  |

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 1, 
        "list": [
            {
                "top_left": [49, 84], 
                "top_right": [150, 84], 
                "bottom_left": [49, 208], 
                "bottom_right": [150, 208], 
                "result": false
            }
        ]
    }
}
```

> **Response Data Param**

|    Field     |    Type    | Length | Null | Default |                **Description**                |
| :----------: | :--------: | :----: | :--: | :-----: | :-------------------------------------------: |
|    result    |  boolean   |        |      |         | 匹配结果，`true`为有遮罩物，`false`为无遮罩物 |
|   top_left   | tuple/list |        |      |         |            人脸出现位置左上角坐标             |
|  top_right   | tuple/list |        |      |         |            人脸出现位置右上角坐标             |
| bottom_left  | tuple/list |        |      |         |            人脸出现位置左下角坐标             |
| bottom_right | tuple/list |        |      |         |            人脸出现位置右下角坐标             |

> **Notice**

+ 此API不会判断人脸身份，仅判断脸部有无遮罩物
+ 理论上不会判断失败，但有概率会错误识别，目前测试来看对小像素的物体容易识别失败
+ 识别错误是指将不是人脸的数据识别为人脸数据，且此API会将动漫的人脸也识别为人脸，很迷

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

null

# Map

**地图类**

## District - Get

> **API Description**

`GET`

​	转接高德地图行政区域查询API，精简返回结果

​	点击进入[高德行政区域查询API地址](https://lbs.amap.com/api/webservice/guide/api/district)

> **URL**

`https://hotel.lcworkroom.cn/api/map/district/?params`

> **URL Param**
>
> 所有参数与高德地图api一致，若传了非高德地图api的参数，将自动忽略。具体规则请查阅[高德行政区域查询API地址](https://lbs.amap.com/api/webservice/guide/api/district)

|    Field    |  Type  | Length | Null | Default |         **Description**          |
| :---------: | :----: | :----: | :--: | :-----: | :------------------------------: |
|     key     | string |   32   |      |    √    | 请求服务权限标识。**已内置初始值** |
|  keywords   | srting |        |      |    √    |            查询关键字            |
| subdistrict |  int   |        |      |    √    |            子级行政区            |
|    page     |  int   |        |      | √ |          需要第几页数据          |
|   offset    |  int   |        |      | √        |        最外层返回数据个数        |
| extensions  |   string    |        |      |   √      |           返回结果控制           |
|   filter    | int |        |      | √ |           根据区划过滤           |
|  callback   | function |        |      | √ |             回调函数。**请勿使用**             |
|   output    | string |        |      | √ |        返回数据格式类型。**已内置初始值，不可修改**        |

> **Notice**

+ 以上字段中`key`与`output`已二次封装内置，可忽略。
+ 其他字段若缺省则使用高德api默认字段值
+ `callback`字段请勿传值

> **Response Success Example**
>
> 已对高德api的返回值进行了精简，外层处理成与api相同样式，内层删除不必要的字段值

```python
{
    "id": -1, 
    "status": 0, 
    "message": "OK",
    "data": {
        "districts": [
            {
                "name": "\u6d59\u6c5f\u7701", 
                "districts": [
                    {
                        "name": "\u821f\u5c71\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u5b81\u6ce2\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u5609\u5174\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u53f0\u5dde\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u6e29\u5dde\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u4e3d\u6c34\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u7ecd\u5174\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u6e56\u5dde\u5e02", 
                        "districts": []
                    },
                    {
                        "name": "\u8862\u5dde\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u91d1\u534e\u5e02", 
                        "districts": []
                    }, 
                    {
                        "name": "\u676d\u5dde\u5e02", 
                        "districts": []
                    }
                ]
            }
        ]
    }
}


```

> **Response Failed Example**

```python
{
    "id": -1, 
    "status": 1000, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -100   |

> **Local Status**
>
> 二次封装时将高德中的`status`去除，将`infocode`改为`status`并从`string`转为了`int`型数据，将`info`改为`message`。并加入了`100`状态码

| Status |    Message     | Description |
| :----: | :------------: | :---------: |
|  100   | Get Json Error |     API请求失败     |

**其余状态码与状态信息请查阅[高德行政区域查询错误码](https://lbs.amap.com/api/webservice/guide/tools/info)**

# Pic（新增）

**图床类**

## Pic - Get（新增）

> **API Description**

`GET`

​	获取由此POST命令上传的图片，成功直接重定向至图片url，否则重定向至error提示图片

> **URL**

`https://hotel.lcworkroom.cn/api/pic/get/<path:upload_to>?name=`

> **URL Param**

|   Field   |  Type  | Length | Null | Default |       **Description**        |
| :-------: | :----: | :----: | :--: | :-----: | :--------------------------: |
| upload_to | string |        |      |         | 图片所处目录，由post请求决定 |
|   name    | srting |        |      |         |   图片名称，由post请求决定   |

> **Notice**

+ `upload_to`符合restful风格，可包含`/`，例如`test/fff`
+ `name`为url参数
+ 此api会自动重定向到图片所在url里，因此在调用此api时只要将其填入类似`src`的参数中即可
+ 若指定的图片不存在，自动重定向至参数error图片
+ `url`末尾是否有`/`都可

> **URL Example**

```
<img src="https://hotel.lcworkroom.cn/api/pic/get/abc?name=%E6%B5%8B%E8%AF%95%E5%9B%BE%E7%89%87" />
```

![测试图片](https://hotel.lcworkroom.cn/api/pic/get/abc?name=%E6%B5%8B%E8%AF%95%E5%9B%BE%E7%89%87)

> **Error图片**

![错误图片](https://hotel.lcworkroom.cn/media/default/error.jpg)

## Pic - Upload（新增）

> **API Description**

`POST`

​	获取由此POST命令上传的图片，成功直接重定向至图片url，否则重定向至error提示图片

后期打算增加身份验证，并扩充其api的用途

> **URL**

`https://hotel.lcworkroom.cn/api/pic/`

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"pic",
    "subtype":"upload",
    "data":{
        "name": "测试图片", 
        "content": "测试哒哒哒", 
        "type": "jpg", 
        "upload_to": "test/fff", 
        "if_local": False,
        "base64":"...",
    }
}
```

> **Data Param**

|   Field   |  Type   | Length | Null | Default |          **Description**           |
| :-------: | :-----: | :----: | :--: | :-----: | :--------------------------------: |
|   name    | string  |        |      |         |       图片名称，用于get请求        |
| upload_to | string  |        |      |         |   图片所上传的位置，用于get请求    |
|  base64   | string  |        |      |         |           图片base64数据           |
|  content  | string  |        |      |    √    | 图片描述，用于后台显示，默认空文本 |
|   type    | string  |        |      |    √    |       图片后缀名，默认`file`       |
| if_local  | boolean |        |      |    √    |     是否存储到本地，默认flase      |

> **Notice**

+ `name`与`upload_to`组成主键，若上传了已存在的主键将覆盖保存此记录对应的图片
+ 根据上一条规则，此API也可用于更新已存在的图片记录
+ `name`字段**不可包含**有点`.`和`/`等符号，建议使用中英文，若出现其他标点符号可能会出现未知错误
+ `upload_to`**只可包含**`/`或`_`标点符号，且`uoload_to`符合URL的组成规则，不可有中文字符，否则可能会出现未知错误
+ `base64`数据是否去除头信息都无所谓。（头信息例子：`image/jpg;base64,`)
+ `type`中不可包含点`.`，必须由英文字母组成
+ `if_local`用来指定图片上传位置，`false`则上传至COS储存服务器中，网速更快；`true`上传至服务器本地中。若传递的参数非`boolean`型，则默认值为`false`
+ 用此api可以实现对其他api的图片进行覆盖

> **Upload_to与name模式**
>
> 用以下特定的`upload_to`以及`name`可对其他的api图片进行覆盖操作
>
> 目前暂无法限制修改他人头像的行为，等后期增加权限验证后可解决此问题

| upload_to |     name     |  可覆盖  |                             备注                             |
| :-------: | :----------: | :------: | :----------------------------------------------------------: |
|   users   | 用户username | 用户头像 | 在此API上线之前的用户头像需重新用此API上传头像后才可用<br />使用此api后type不管传什么值固定为`user` |

> **不可用的upload_to值**
>
> 因为权限原因，若upload_to值指定为以下字段，将返回`200`无权操作返回码，因为这些值对应的数据为敏感数据，不能使用此API上传更新

| upload_to  |   对应数据   |
| :--------: | :----------: |
| faces_data | 人脸注册信息 |



> **Response Success Example**
>
> 根据请求时`if_local`的值，返回对应的图片url。
>
> 本地url为相对路径，例如`/media/test/fff/100ac4baafa990d6edc7810052d3e772.jpg`

```python
{
    "id": 1234, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "url": "https://hotel-1251848017.cos.ap-shanghai.myqcloud.com/test/fff/100ac4baafa990d6edc7810052d3e772.jpg"
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

| Status |
| ------ |
| -600   |
| -500   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |       Message       |   Description    |
| :----: | :-----------------: | :--------------: |
|  100   |  Error base64 data  | 错误的base64数据 |
|  200   | No right to operate |    无权限操作    |

# 

> **Notice**

+ `upload_to`符合restful风格，可包含`/`，例如`test/fff`
+ `name`为url参数
+ 此api会自动重定向到图片所在url里，因此在调用此api时只要将其填入类似`src`的参数中即可
+ 若指定的图片不存在，自动重定向至参数error图片

# Msg类

**站内信类**

后台地址：[酒店AI后台管理系统](https://hotel.lcworkroom.cn/admin)

客服账号：`server`

客服密码：`hotel2020`

已获得所有权限

## Msg - has_new

> **API Description**

`POST`

此API用于获取用户的新消息条数，成功返回系统新站内信条数，新私聊条数和私聊条数详情

这里的系统消息，是指由`hotel`用户或者空用户发出的消息，并非是指`消息type`值为`system`的消息。

这里的私聊消息，是指由非系统`hotel`用户或者空用户发出的，且有指定单一的接收者的消息，并非是指`消息type`值为`private`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"has_new",
    "data":{}
}
```

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "sys": 4, 
        "private": 3, 
        "private_detail": {
            "13750687010": 2, 
            "13735866541": 1
        }
    }
}
```

> **Response Data Param**

|     Field      | Type |  **Description**   |
| :------------: | :--: | :----------------: |
|      sys       | int  |   系统新消息条数   |
|    private     | int  |  新私聊站内信条数  |
| private_detail | json | 私聊站内信条数详情 |

> **Notice**

+ `private_detail`中的格式为：`私聊对象`:`新消息条数`，无`num`字段统计，需自行判断

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

**null**

## Msg - sys

> **API Description**

`POST`

此API用于获取发给用户的所有系统站内信，并自动**按发送时间降序排序**

这里的系统消息，是指由`hotel`用户或者空用户发出的消息，并非是指`消息type`值为`system`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"sys",
    "data":{
        "if_new":2
    }
}
```

> **Data Param**

| Field  | Type | Length | Null | Default |                       **Description**                        |
| :----: | :--: | :----: | :--: | :-----: | :----------------------------------------------------------: |
| if_new | int  |        |      |    √    | 消息过滤模式，可选值：`0`获取新消息;`1`获取已读消息;`2`获取全部消息。默认为`0` |

> **Notice**

+ 当`if_new`不为可选值范围时，将自动判定为获取新消息

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 1, 
        "list": [
            {
                "msg_id": 1, 
                "type":"system",
                "subtype":"notice",
                "title": "这是一条测试通知", 
                "content": "嗯？我就测试一下", 
                "add_time": 1582964040.0, 
                "status": false,
                "extra":""
            }
        ]
    }
}
```

> **Response Data Param**

|  Field   |  Type   |  **Description**   |
| :------: | :-----: | :----------------: |
|  msg_id  |   int   |   此消息的消息id   |
|   type   | string  |  消息类型，自定义  |
| subtype  | string  | 消息子类型，自定义 |
|  title   | string  |      消息标题      |
| content  | string  |      消息内容      |
| add_time |  float  |  站内信发送时间戳  |
|  status  | boolean |    消息已读状态    |
|  extra   | string  |  额外信息，自定义  |

> **Notice**
+ 消息已读状态变更请用[Msg - sign](#Msg - sign)或者[Msg - sign_batch](#Msg - sign_batch)API
+ 不论是系统群发还是单独发送的站内信，全部规整到此api
+ **一般的系统通知我打算如此设置：`type`值为`system`,`subtype`值为`notice`。其他可自定义**

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message        |   Description    |
| :----: | :-------------------: | :--------------: |
|  100   | Get admin user failed | 获取系统用户失败 |

## Msg - private

> **API Description**

`POST`

此API用于获取用户发送出去或者发送给用户的所有私聊站内信，并自动**按发送时间降序排序**

这里的私聊消息，是指由非系统`hotel`用户或者空用户发出的，且有指定单一的接收者的消息，并非是指`消息type`值为`private`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"private",
    "data":{
        "if_new":2,
        "people": "13750687010", 
        "start": 0, 
        "limit": -1
    }
}
```

> **Data Param**

| Field  |  Type  | Length | Null | Default |                       **Description**                        |
| :----: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
| if_new |  int   |        |      |    √    | 消息过滤模式，可选值：`0`获取新消息;`1`获取已读消息;`2`获取全部消息。默认为`0` |
| people | string |        |      |    √    | 聊天对象用户名，当不传递或传递为空文本时，返回所有聊天对象的消息，默认为空文本 |
| start  |  int   |        |      |    √    | 记录起始位置，设定后将从`start`的位置开始获取记录，初始值为`0` |
| limit  |  int   |        |      |    √    | 记录返回条数，设定后将从`start`位置开始，返回limit条记录，若记录不足有多少返回多少。当`limit`设置为-1时，将返回从`start`开始的全部记录，默认为`-1` |

> **Notice**

+ 当`if_new`为`0`的时候，用户发送且对方未读的消息将不返回，因为这类消息对于用户自己来说是已读消息
+ 当`if_new`不为可选值范围时，将自动判定为获取新消息
+ `people`传递的值不存在时将返回`101`错误码
+ 当`start`不传递或传递的值数据类型有误时，当做`0`处理
+ 当`limit`不传递或传递的值数据类型有误或值为负数时，当做`-1`处理
+ **`limit`与`if_new`同时存在时，将先执行`limit`再执行`if_new`，因此在使用`limit`取出指定数量消息时，建议将`if_new`设置为2，否则会出现什么问题我也没考虑清楚**

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "records_num": 4, 
        "unit_num": 2, 
        "list": [
            {
                "people": "13750687010", 
                "num": 3, 
                "records": [
                    {
                        "source": 0, 
                        "type":"private",
                        "subtype":"default",
                        "msg_id": 2, 
                        "title": "你好", 
                        "content": "你好鸭", 
                        "add_time": 1582964040.0, 
                        "status": false,
                        "extra":""
                    }, 
                    {
                        "source": 0, 
                        "type":"private",
                        "subtype":"default",
                        "msg_id": 4, 
                        "title": "你好", 
                        "content": "你好鸭", 
                        "add_time": 1582984020.0, 
                        "status": false,
                        "extra":""
                    }, 
                    {
                        "source": 1, 
                        "msg_id": 5, 
                        "type":"private",
                        "subtype":"default",
                        "title": "回复", 
                        "content": "你也好呀！", 
                        "add_time": 1582985310.489896, 
                        "status": false,
                        "extra":""
                    }
                ]
            }, 
            {
                "people": "13735866541", 
                "num": 1, 
                "records": [
                    {
                        "source": 0, 
                        "msg_id": 3, 
                        "type":"private",
                        "subtype":"default",
                        "title": "你好", 
                        "content": "你好鸭", 
                        "add_time": 1582983960.0, 
                        "status": false,
                        "extra":""
                    }
                ]
            }
        ]
    }
}
```

> **Response Data Param**

> **list结构**

|  Field  |  Type  | **Description** |
| :-----: | :----: | :-------------: |
| people  | string |   私聊对象id    |
|   num   |  int   |    私聊条数     |
| records |  list  |    消息列表     |

> **records结构**

| Field  | Type | **Description** |
| :----: | :--: | :-------------: |
| source | int  |  消息类型，可选值：`0`:其他人发来的消息；`1`:用户发送的消息  |
|  msg_id  |   int   | 此消息的消息id |
| type | string | 消息类型，暂不可自定义，默认为`private` |
| subtype | string | 消息子类型,暂不可自定义，默认为`default` |
|  title   | string  |              消息标题              |
| content  | string  |              消息内容              |
| add_time |  float  |          站内信发送时间戳          |
|  status  | boolean |            消息已读状态extra            |
| extra | string | 额外信息,暂不可自定义，默认为空文本 |

> **Notice**

+ 消息已读状态变更请用[Msg - sign](#Msg - sign)或者[Msg - sign_batch](#Msg - sign_batch)API
+ 在私聊中建议使用`content`字段传递聊天内容，保留`title`的原因是打算后期做成卡片式分享时用到。
+ 私聊消息之所以用消息列表式返回格式是为了前端更方便处理，同时也是借鉴了b站与其他论坛的格式
+ **私聊消息暂不使用`type`、`subtype`和`extra`的值**
+ **默认的私聊消息`type`值为`private`，`subtype`值为`default`，`extra`为空文本**

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message        |   Description    |
| :----: | :-------------------: | :--------------: |
|  100   | Get admin user failed | 获取系统用户失败 |
|  101   |   Get sender failed   |  获取发送者失败  |

## Msg - msg_list

> **API Description**

`POST`

此API用于获取用户的私聊过的聊天对象列表及最后一条消息，并自动**按最后一条消息发送时间降序排序**

这里的私聊消息，是指由非系统`hotel`用户或者空用户发出的，且有指定单一的接收者的消息，并非是指`消息type`值为`private`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"msg_list",
    "data":{}
}
```

> **Data Param**

**null**

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 1, 
        "list": [
            {
                "username": "13858181317", 
                "nickname": "AmiKara", 
                "msg_id": 7, 
                "status": false, 
                "add_time": 1583053260.0, 
                "title": "这是一条测试通知", 
                "content": "嗯？我就测试一下", 
                "type": "private", 
                "subtype": "default", 
                "extra": ""
            }
        ]
    }
}
```

> **Response Data Param**

|  Field   |  Type   |  **Description**   |
| :------: | :-----: | :----------------: |
| username | string  |       用户名       |
| nickname | string  |      用户昵称      |
|  msg_id  |   int   |   此消息的消息id   |
|   type   | string  |  消息类型，自定义  |
| subtype  | string  | 消息子类型，自定义 |
|  title   | string  |      消息标题      |
| content  | string  |      消息内容      |
| add_time |  float  |  站内信发送时间戳  |
|  status  | boolean |    消息已读状态    |
|  extra   | string  |  额外信息，自定义  |

> **Notice**

+ `list`列表已按照最后回复时间降序排序，最后回复包括用户发送给聊天对象的时间
+ **修改了list内部数据结构，新增与聊天对象的最后一条消息信息**

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message        |   Description    |
| :----: | :-------------------: | :--------------: |
|  100   | Get admin user failed | 获取系统用户失败 |

## Msg - sign

> **API Description**

`POST`

此API用于标记**站内信**为已读状态，不论系统站内信还是私聊站内信。

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`


> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"sign",
    "data":{
        "msg_id":1
    }
}
```

> **Data Param**

| Field  | Type | Length | Null | Default | **Description** |
| :----: | :--: | :----: | :--: | :-----: | :-------------: |
| msg_id | int  |        |      |         |     消息id      |

> **Notice**

+ 当`msg_id`数据类型错误或不存在时，返回`100`状态码

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
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |   Message    | Description  |
| :----: | :----------: | :----------: |
|  100   | Error msg_id | 错误的消息id |

## Msg - sign_batch

> **API Description**

`POST`

此API用于批量标记**站内信**为已读状态，不论系统站内信还是私聊站内信。

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`


> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"sign_batch",
    "data":{
        "sys":0,
        "private":1,
        "people":"13750687010"
    }
}
```

> **Data Param**

|  Field  |  Type  | Length | Null | Default |                       **Description**                        |
| :-----: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
|   sys   |  int   |        |      |    √    |  是否标记系统消息为已读：`0`为不标记，`1`为标记，默认为`0`   |
| private |  int   |        |      |    √    |  是否标记私聊消息为已读：`0`为不标记，`1`为标记，默认为`0`   |
| people  | string |        |      |    √    | 聊天对象id，仅在`private`设置时有效，设置后将仅标记与该聊天对象的未读消息为已读消息；不设置或设置为空文本表示标记所有未读私聊信息。 |

> **Notice**

+ 当`sys`数据类型错误或不存在时，默认使用`0`
+ 当`private`数据类型错误或不存在时，默认使用`0`
+ 当`people`数据类型错误或不存在时，默认使用空文本
+ 当同时标记系统消息与私聊消息时，若在标记系统消息过程中出现错误，将直接返回错误信息，不执行私聊消息的标记。
+ 私聊消息的标记仅针对于自身为接收者的未读信息，自己为发送者且对方未读的消息不会被标记

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
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message         |      Description       |
| :----: | :--------------------: | :--------------------: |
|  100   | Get system user failed |    获取系统用户失败    |
|  101   |   Get sender Failed    | 获取私聊发送者对象失败 |

## Msg - filter

> **API Description**

`POST`

此API用于通过`msg_type`、`msg_subtype`和`if_new`值进行筛选**用户收到的所有站内信消息**，并自动**按发送时间降序排序**

通过此接口获取的私聊消息结构会非常混乱，不建议私聊消息使用此API

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"filter",
    "data":{
        "type": "system", 
        "subtype": "", 
        "if_new": 1
    }
}
```

> **Data Param**

|  Field  |  Type  | Length | Null | Default |                       **Description**                        |
| :-----: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
|  type   | string |        |      |         |                           消息类型                           |
| subtype | string |        |      |    √    |  消息子类型，不传递或者传递空文本表示筛选`type`下所有的消息  |
| if_new  |  int   |        |      |    √    | 消息过滤模式，可选值：`0`获取新消息;`1`获取已读消息;`2`获取全部消息。默认为`0` |

> **Notice**

+ `type`值不可为空，否则可能发生不可知错误（没测试过）
+ 当`if_new`数据类型错误或不存在时，默认使用`0`，自动判定为获取新消息
+ `type`与`subtype`、`if_new`三者为交集检索条件

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 1, 
        "list": [
            {
                "msg_id": 1, 
                "type":"system",
                "subtype":"notice",
                "title": "这是一条测试通知", 
                "content": "嗯？我就测试一下", 
                "add_time": 1582964040.0, 
                "status": false,
                "extra":""
            }
        ]
    }
}
```

> **Response Data Param**

|  Field   |  Type   |          **Description**           |
| :------: | :-----: | :--------------------------------: |
|  msg_id  |   int   | 此消息的消息id，保留字段，暂无用处 |
|   type   | string  |              消息类型              |
| subtype  | string  |             消息子类型             |
|  title   | string  |              消息标题              |
| content  | string  |              消息内容              |
| add_time |  float  |          站内信发送时间戳          |
|  status  | boolean |            消息已读状态            |
|  extra   | string  |              额外信息              |

> **Notice**

+ 消息已读状态变更请用[Msg - sign](#Msg - sign)或者[Msg - sign_batch](#Msg - sign_batch)API
+ 不论是系统群发还是单独发送的站内信，全部规整到此api
+ 用此API获取的私聊消息返回结构非常混乱，不建议私聊消息使用此API

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

**null**

## Msg - send

> **API Description**

`POST`

此API用于发送私聊站内信给指定用户

> **URL**

`https://hotel.lcworkroom.cn/api/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"send",
    "data":{
        "receiver": "13750687010", 
        "title": "回复", 
        "content": "你也好呀！"
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |    **Description**     |
| :------: | :----: | :----: | :--: | :-----: | :--------------------: |
| receiver | string |   11   |      |         |      接收者用户名      |
|  title   | string |  100   |      |         | 消息标题，建议为空文本 |
| content  | string |        |      |         |        消息内容        |

> **Notice**

+ 在私聊中建议使用`content`字段传递聊天内容，`title`字段一般情况建议为空文本。
+ 保留`title`的原因是打算后期做成卡片式分享时用到。
+ **在私聊消息中，暂不支持自定义`type`、`subtype`和`extra`字段**
+ **默认的私聊消息`type`值为`private`，`subtype`值为`default`，`extra`为空文本**

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "msg_id": 5
    }
}
```

> **Response Data Param**

| Field  | Type |          **Description**           |
| :----: | :--: | :--------------------------------: |
| msg_id | int  | 此消息的消息id，保留字段，暂无用处 |

> **Notice**

+ 用户不存在返回`100`错误;消息正文创建失败返回`101`错误

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |          Message          |   Description    |
| :----: | :-----------------------: | :--------------: |
|  100   |      Error receiver       |   错误的接收者   |
|  101   | Create MessageText Failed | 创建消息内容失败 |

# Locker类

寄存柜类

## Locker - apply

> **API Description**

`POST`

此API用于预约酒店寄存柜，成功返回相关信息，并自动发送一条系统消息给用户

> **URL**

`https://hotel.lcworkroom.cn/api/locker/apply/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"locker",
    "subtype":"apply",
    "data":{
        "order_id":4
    }
}
```

> **Data Param**

|  Field   | Type | Length | Null | Default | **Description** |
| :------: | :--: | :----: | :--: | :-----: | :-------------: |
| order_id | int  |        |      |         |     订单id      |

> **Notice**

+ API通过订单，随机为用户分配订单对应酒店的寄存柜
+ 同一订单里用户只能拥有一个正在进行中的预约信息，且只能由订单中的`guest`申请
+ 若订单状态不对，返回`101`状态码。（状态不对指非预约中和入住中的其他状态）
+ 若操作用户与订单对应用户不一致，返回`300`状态码
+ 预约只能在入住时间前6h和入住时间后3h可进行预约，其他时间预约返回`102`错误码

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "apply_id": 3, 
        "status": "applying", 
        "locker_id": 1, 
        "index": 1, 
        "num": 1, 
        "expire_time": 1583852400.0}}

```

> **Response Data Param**

|    Field    |  Type  |                       **Description**                        |
| :---------: | :----: | :----------------------------------------------------------: |
|  apply_id   |  int   |                       寄存柜预约信息id                       |
|   status    | string | 寄存柜预约状态，可选值：<br />`applying`:预约中<br />`using`:使用中<br />`canceled`:被取消<br />`done`:使用完毕 |
|  locker_id  |  int   |                           寄存柜id                           |
|    index    |  int   |            寄存柜单元序列，通俗讲就是第`index`柜             |
|     num     |  int   |                 编号，通俗点将就是第`num`号                  |
| expire_time | float  |           过期时间时间戳，过期后预约信息自动被取消           |

> **Notice**

+ `index`和`num`字段一般连用，组成：`index`柜`num`号 的形式，这么设置的目的是为了适应多台寄存柜的场景

+ 寄存柜为随机分配，不可自主选择，若寄存柜已满返回`200`状态码

+ 寄存柜预约成功后会自动发送一条站内信，消息为系统单发消息，其中：

  + `type`值为`locker`

  + `subtype`值为`apply`

  + `title`值为`预约寄存柜成功`，

  + `content`值为`您成功预约了{酒店名称}的寄存柜，以下是详细信息,请注意过期时间，过时自动取消`

  + ``extra`为文本型的json数据，需自行二次解析，详细字段见下。

  + |    Field    |  Type  |                         Description                          |
    | :---------: | :----: | :----------------------------------------------------------: |
    |  hotel_id   |  int   |                       寄存柜所在酒店id                       |
    | hotel_name  | string |                      寄存柜所在酒店名称                      |
    |  apply_id   |  int   |                       寄存柜预约信息id                       |
    |   status    | string | 寄存柜预约状态，可选值：<br />`applying`:预约中<br />`using`:使用中<br />`canceled`:被取消<br />`done`:使用完毕 |
    |  locker_id  |  int   |                           寄存柜id                           |
    |    index    |  int   |            寄存柜单元序列，通俗讲就是第`index`柜             |
    |     num     |  int   |                 编号，通俗点将就是第`num`号                  |
    | expire_time | float  |           过期时间时间戳，过期后预约信息自动被取消           |

  + `extra`字段的想法是用来给卡片样式通知提供的字段

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |         Message          |                      Description                      |
| :----: | :----------------------: | :---------------------------------------------------: |
|  100   |      Error order_id      |                     错误的订单id                      |
|  101   |    Error order status    |       错误的订单状态(指非预约中或入住中的状态)        |
|  102   |     Error apply time     | 错误的预约时间（需在 入住时间-6h 与入住时间+3h 之间） |
|  103   | Already had application  |    已有未完成的预约或使用记录（指预约中与使用中）     |
|  200   |   No available locker    |       该酒店无可用寄存柜（已满或未设立寄存柜）        |
|  300   |      User mismatch       |               用户与订单的预订人不一致                |
|  301   | User don't has face data |                    用户无人脸数据                     |

## Locker - cancel

> **API Description**

`POST`

此API用于取消已预约的酒店寄存柜，取消成功后将自动发送一条系统消息给用户

> **URL**

`https://hotel.lcworkroom.cn/api/locker/apply/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"locker",
    "subtype":"cancel",
    "data":{
        "apply_id":3
    }
}
```

> **Data Param**

|  Field   | Type | Length | Null | Default | **Description**  |
| :------: | :--: | :----: | :--: | :-----: | :--------------: |
| apply_id | int  |        |      |         | 寄存柜预约信息id |

> **Notice**

+ `order_id`不存在返回`100`错误码

+ 只能取消处于预约中的寄存柜预约，否则返回`101`返回码

+ 若操作用户非预约者，返回`300`返回码，防止恶意取消他人预约信息

+ 预约超过入住时间3h后将自动取消。**（目前还没做自动取消机制，太耗性能没想好怎么弄，后期会增加）**

+ 寄存柜取消预约成功后会自动发送一条站内信，消息为系统单发消息，其中：

  + `type`值为`locker`

  + `subtype`值为`cancel`

  + `title`值为`取消寄存柜成功`，

  + `content`值为`您已成功取消预约{酒店名称}的寄存柜，以下是详细信息`

  + ``extra`为文本型的json数据，需自行二次解析，详细字段见下。

  + |    Field    |  Type  |                         Description                          |
    | :---------: | :----: | :----------------------------------------------------------: |
    |  hotel_id   |  int   |                       寄存柜所在酒店id                       |
    | hotel_name  | string |                      寄存柜所在酒店名称                      |
    |  apply_id   |  int   |                       寄存柜预约信息id                       |
    |   status    | string | 寄存柜预约状态，可选值：<br />`applying`:预约中<br />`using`:使用中<br />`canceled`:被取消<br />`done`:使用完毕 |
    |  locker_id  |  int   |                           寄存柜id                           |
    |    index    |  int   |            寄存柜单元序列，通俗讲就是第`index`柜             |
    |     num     |  int   |                 编号，通俗点将就是第`num`号                  |
    | expire_time | float  |           过期时间时间戳，过期后预约信息自动被取消           |

  + `extra`字段的想法是用来给卡片样式通知提供的字段

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {}

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |                  Message                  |       Description        |
| :----: | :---------------------------------------: | :----------------------: |
|  100   |              Error apply_id               |     错误的预约信息id     |
|  101   | Only with applying status can be canceled | 只有预约状态下可取消预约 |
|  300   |               User mismatch               |    用户与预约者不一致    |

## Locker - list

> **API Description**

`POST`

此API用于获取用户订单对应的寄存柜预约消息列表，之所以为列表是因为用户可能会有取消预约并重新预约的情况，如此会产生多条记录。成功返回相关信息

> **URL**

`https://hotel.lcworkroom.cn/api/locker/info/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"locker",
    "subtype":"list",
    "data":{
        "order_id":4
        "status":"applying"
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |                       **Description**                        |
| :------: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
| order_id |  int   |        |      |         |                            订单id                            |
|  status  | string |        |      |    √    | 寄存柜预约状态，可选值：<br />`applying`:预约中<br />`using`:使用中<br />`canceled`:被取消<br />`done`:使用完毕 |

> **Notice**

+ `order_id`错误返回`100`错误码
+ 不传递`status`字段时，默认返回全部预约消息，若传递了以上四个值之一，可进行状态筛选，不可传递多个值，若传递的值有误则自动返回全部预约消息。

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 2, 
        "list": [
            {
                "apply_id": 3, 
                "status": "applying", 
                "locker_id": 1, 
                "index": 1, 
                "num": 1, 
                "expire_time": 1583852400.0
            }, 
            {
                "apply_id": 4, 
                "status": 
                "canceled", 
                "locker_id": 2, 
                "index": 1, 
                "num": 2, 
                "expire_time": 1583852400.0
            }
        ]
    }
}
```

> **Response Data Param**

|    Field    |  Type  |                       **Description**                        |
| :---------: | :----: | :----------------------------------------------------------: |
|  apply_id   |  int   |                       寄存柜预约信息id                       |
|   status    | string | 寄存柜预约状态，可选值：<br />`applying`:预约中<br />`using`:使用中<br />`canceled`:被取消<br />`done`:使用完毕 |
|  locker_id  |  int   |                           寄存柜id                           |
|    index    |  int   |            寄存柜单元序列，通俗讲就是第`index`柜             |
|     num     |  int   |                 编号，通俗点将就是第`num`号                  |
| expire_time | float  |           过期时间时间戳，过期后预约信息自动被取消           |

> **Notice**

+ `index`和`num`字段一般连用，组成：`index`柜`num`号 的形式，这么设置的目的是为了适应多台寄存柜的场景

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |    Message     |       Description        |
| :----: | :------------: | :----------------------: |
|  100   | Error order_id |       错误的订单id       |
|  300   | User mismatch  | 用户与订单的预订人不一致 |

## Locker - get

> **API Description**

`POST`

此API用于通过`apply_id`获取用户单条寄存柜预约消息。成功返回相关信息

> **URL**

`https://hotel.lcworkroom.cn/api/locker/info/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"locker",
    "subtype":"get",
    "data":{
        "apply_id":4
    }
}
```

> **Data Param**

|  Field   | Type | Length | Null | Default | **Description**  |
| :------: | :--: | :----: | :--: | :-----: | :--------------: |
| apply_id | int  |        |      |         | 寄存柜预约消息id |

> **Notice**

+ `apply_id`错误返回`100`错误码

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "apply_id": 4, 
        "status": "canceled", 
        "locker_id": 2, 
        "index": 1, 
        "num": 2, 
        "expire_time": 1583852400.0
    }
}
```

> **Response Data Param**

|    Field    |  Type  |                       **Description**                        |
| :---------: | :----: | :----------------------------------------------------------: |
|  apply_id   |  int   |                       寄存柜预约信息id                       |
|   status    | string | 寄存柜预约状态，可选值：<br />`applying`:预约中<br />`using`:使用中<br />`canceled`:被取消<br />`done`:使用完毕 |
|  locker_id  |  int   |                           寄存柜id                           |
|    index    |  int   |            寄存柜单元序列，通俗讲就是第`index`柜             |
|     num     |  int   |                 编号，通俗点将就是第`num`号                  |
| expire_time | float  |           过期时间时间戳，过期后预约信息自动被取消           |

> **Notice**

+ `index`和`num`字段一般连用，组成：`index`柜`num`号 的形式，这么设置的目的是为了适应多台寄存柜的场景

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

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |    Message     |    Description     |
| :----: | :------------: | :----------------: |
|  100   | Error order_id |    错误的订单id    |
|  300   | User mismatch  | 用户与预约者不一致 |

# 硬件终端接口暂不写说明文档

**因为随时有可能会调整**

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
|  -100  |       Missing necessary args       |  api地址中缺少token或其他必需参数   | POST、GET |
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
|  -600  |         Local upload Error         |            本地上传失败             | POST      |

------

- `status`传递的错误码类型为整型。

- 手机验证码相关的错误码详见[短信错误码](http://cloud.tencent.com/document/product/382/3771 "腾讯短信API文档")