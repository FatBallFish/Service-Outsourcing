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

## User Login - Password（**有修改**）

> **API Description**

`POST`

​	此API用于以手机号作为登录凭证时的登录请求，成功返回token值

​	**修改：**

**1. 局部状态码全部有变，请仔细对照修改**

**2. 新增一条`Notice`中解释**

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

+ `pass`为明文密码**（新增）**
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

## User Login - Sms（**新增**）

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

**1.新增`100`局部状态码，用来处理用户不存在的情况**

**2.新增2条`Notice`解释**

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

+ `token`为必传字段，不论是否以`token`获取用户信息**（新增）**
+ 若`token`与`username`同时存在，则查询`username`对应用户信息**（新增）**
+ `username`缺省则自动获取`token`对应的用户信息，不缺省可查指定用户的信息
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

| Status |   Message    | Description  |
| :----: | :----------: | :----------: |
|  100   | No Such User | 无该账号记录 |

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

## User Password - Forget（有修改）

> **API Description**

`POST`

​	通过手机短信验证码形式找回用户密码**（仅限于用手机号注册的账号）**

**修改：**

**1.新增`101`局部状态码，拦截使用短信验证码注册且未设置过密码的账号进行忘记密码操作**

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

## User Password - Change（有修改）

> **API Description**

`POST`

​	通过验证用户名和原密码进行用户新密码修改

**修改：**

**局部状态码全部有变，请仔细对照修改**

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

## User Portrait - Get

> **API Description**

`GET`

​	通过传递`username`参数获取指定用户头像，返回头像二进制数据

**修改：**

****

> **URL**

`https://hotel.lcworkroom.cn/api/user/portrait/?username=`

> **URL Param**

|  Field   |  Type  | Length | Null | Default | **Description** |
| :------: | :----: | :----: | :--: | :-----: | :-------------: |
| username | string |   11   |      |         |      账号       |

> **Notice**

+ `username`字段不存在或者字段值错误将返回参数错误提示图片`error.jpg`
+ 访问此API的ip若非允许内的ip将被阻截（后期想改成返回禁止访问图片`ban.jpg`）
+ 若用户未上传过头像时将返回默认头像数据

## User Portrait - Upload

> **API Description**

`POST`

​	通过传递的`token`参数以及图片base64数据对指定用户进行图片更新

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

| Field  |  Type  | Length | Null | Default | **Description** |
| :----: | :----: | :----: | :--: | :-----: | :-------------: |
| base64 | string |        |      |         | 图片base64数据  |

> **Notice**

+ API自动根据`token`值更新对应用户的头像
+ `base64`数据是否去除头信息都无所谓。（头信息例子：`image/jpg;base64,`)
+ 用户多次上传头像则之前的头像数据将被覆写，只保留最后一次上传的数据

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

## Sms Captcha - Generate（**有修改**）

> **API Description**

`POST`

此API用于以手机号作为账号进行`注册`或`找回密码`时发送短信验证码

成功则向指定手机发送短信，并返回一个5位`rand`值

**修改：**

**新增一种`Data Param`中`command_type`的情况，用来处理用户短信登录**

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
| command_type |  int   |  1-2   |      |    √    | 短信类型。`1`为注册账号;`2`为找回密码；`3`为账号短信登录（**新增**） |
|     hash     | string |   32   |      |    √    | 图片验证码hash，**该字段目前不使用**<br />`hash = MD5(imgcode + rand` |

> **Notice**

- **`command_type`新增状态`3`用于处理短信登录的验证码发送**
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

# Face

## Group - Create

> **API Description**

`POST`

此API用于创建一个人员库，成功返回人员库id

**此API有权限限制，仅管理员可用，其他人调用此API将返回`-103`状态码**

> **URL**

`https://hotel.lcworkroom.cn/api/face/group`

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

`https://hotel.lcworkroom.cn/api/face/group`

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

`https://hotel.lcworkroom.cn/api/face/group`

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

`https://hotel.lcworkroom.cn/api/face/group`

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

## Group - List

> **API Description**

`POST`

此API用于返回所有人员库信息

> **URL**

`https://hotel.lcworkroom.cn/api/face/group`

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