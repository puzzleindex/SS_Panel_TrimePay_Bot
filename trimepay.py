import config
import sql
import hashlib
import urllib
import json
import base64
import uuid
import qrcode
import PIL
import requests

def params(tgid,totalFee,payType):
    #准备签名
    merchantTradeNo = ''.join(str(uuid.uuid1()).split('-'))[:8].upper()

    #创建paylist
    uid = sql.getUidByTgid(tgid)
    if uid is False:
        return False
    status = sql.newPaylist(uid,str(float(totalFee)/100),merchantTradeNo)
    if status == True:
        appId = config.trimepay_appid
        notifyUrl = config.baseUrl + '/payment/notify'
        returnUrl = config.baseUrl + '/user/payment/return'

        data = {}
        data['appId'] = appId
        data['payType'] = payType
        data['merchantTradeNo'] = merchantTradeNo
        data['totalFee'] = str(totalFee)
        data['notifyUrl'] = notifyUrl
        data['returnUrl'] = returnUrl

        return data


#签名
def sign(data):
    arrangeData = {}
    for key in sorted(data):
        arrangeData[key] = data[key]
    data = urllib.parse.urlencode(arrangeData)
    sign = hashlib.md5((hashlib.md5(data.encode()).hexdigest() + config.trimepay_secret).encode()).hexdigest()
    return sign

#支付宝post
def alipay_post(data,type='pay'):
    if type == 'pay':
        gatewayUri = config.gatewayUri + 'pay/go'
    else:
        gatewayUri = config.gatewayUri + 'refund/go'

    r = requests.post(url=gatewayUri,data=data)
    return r.json()

#微信post
def wechat_post(data):
    result = {}
    result['code'] = 0
    result['data'] = 'http://cashier.hlxpay.com/#/wepay/jsapi?payData=' + str(base64.b64encode(bytes(json.dumps(data), encoding="utf8")), encoding='utf8')
    result['pid'] = data['merchantTradeNo']
    return result

#获取微信二维码
def getQrcode(result):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    qr.add_data(result['data'])
    qr.make()
    img = qr.make_image()
    img.save('qr.png')
    return True
