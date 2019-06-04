from itsdangerous import TimedJSONWebSignatureSerializer as TJSWServer

#加密
def generate_sign_openid(openid):
    #1.创建TJSWServer对象
    serializer=TJSWServer(secret_key="oauth",expires_in=300)
    #2.加密openid
    sign_openid =serializer.dumps({"openid":openid})
    #3.返回结果 同时对二进制解密
    return sign_openid.decode()

#解密
def decode_sign_openid(data):
    # 1.创建TJSWServer对象
    serializer = TJSWServer(secret_key="oauth", expires_in=300)
    # 2.解密openid
    try:
        data_dict=serializer.loads(data)
    except Exception as e:
        return None
    #3.返回结果
    return data_dict.get("openid")
