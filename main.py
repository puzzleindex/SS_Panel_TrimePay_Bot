import config
import trimepay
import sql
import re

import qrcode
import PIL
import os
import time
import telebot
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'使用本机器人需先绑定\n在网站-菜单-资料编辑页面找到二维码发送给 @%s\n绑定后发送关键字(支付宝充值或微信充值)+金额,按照提示充值即可\n例如发送支付宝充值10'%config.bindBot)

@bot.message_handler(func=lambda message:True)
def code(message):
    if message.chat.type == 'private':
        if message.text.startswith('支付宝充值'):
            price = message.text[5:].strip()
            try:
                price = float(price)
            except:
                bot.send_message(message.chat.id,'非法金额')
                return
            if isinstance(price, float) == True and price > 0:

                tgid = str(message.chat.id)

                totalFee = int(float(price) * 100)
                payType = 'ALIPAY_WAP'

                data = trimepay.params(tgid,totalFee,payType)
                if data is False:
                    bot.send_message(message.chat.id,'您的网站账户没有绑定tg账户,无法充值')
                else:
                    data['sign'] = trimepay.sign(data)
                    result = trimepay.alipay_post(data)
                    #print()
                    markup = types.InlineKeyboardMarkup()
                    alipay_btn = types.InlineKeyboardButton('点击充值', url=result['data'])
                    markup.add(alipay_btn)
                    bot.send_message(message.chat.id,'支付宝充值%.2f元'%price,reply_markup=markup)

            else:
                bot.send_message(message.chat.id,'非法金额')

        elif message.text.startswith('微信充值'):
            price = message.text[5:].strip()
            try:
                price = float(price)
            except:
                bot.send_message(message.chat.id,'非法金额')
                return
            if isinstance(price, float) == True and price > 0:

                tgid = str(message.chat.id)
                totalFee = int(float(price) * 100)
                payType = 'WEPAY_QR'

                data = trimepay.params(tgid,totalFee,payType)
                if data is False:
                    bot.send_message(message.chat.id,'您的网站账户没有绑定tg账户,无法充值')
                else:
                    data['sign'] = trimepay.sign(data)
                    result = trimepay.wechat_post(data)

                    status = trimepay.getQrcode(result)

                    if status is True:
                        qr = open('qr.png', 'rb')
                        bot.send_message(message.chat.id,'微信充值%.2f元'%price)
                        bot.send_photo(message.chat.id,qr)
                        qr.close()
                        if os.path.exists('qr.png'):
                            os.remove('qr.png')
                        else:
                            print('qrcode删除失败')
                    else:
                        print('qrcode生成失败')

            else:
                bot.send_message(message.chat.id,'非法金额')

        elif message.text == '查询余额':
            money = sql.getMoney(message.chat.id)
            bot.send_message(message.chat.id,'账户余额为%s'%money)

        elif message.text == '套餐列表':
            msg = ''
            goods = sql.getGoods()
            for good in goods:
                msg = msg + 'id:' + str(good[0]) + '\t名称:' + good[1] + '\t价格:' + str(good[2]) + '\n'
            bot.send_message(message.chat.id,msg)

        elif message.text.startswith('购买套餐'):
            t = int(time.time())
            shopid = str(message.text[4:7].strip())
            credit = 1.0
            coupon = ''
            try:
                coupon = message.text.split()[1]
                data = sql.getCoupon(coupon)
                credit = 1 - float(data[5])/100
                if t > int(data[3]):
                    bot.send_message(message.chat.id,'优惠码已过期')
                    return
            except Exception:
                pass
            
            goods = sql.getGoods()
            shopids = {}
            details = {}
            for good in goods:
                shopids[str(good[0])] = str(good[2])
            for good in goods:
                details[str(good[0])] = str(good[3])

            if shopid not in shopids.keys():
                bot.send_message(message.chat.id,'非法shopid')
            else:
                price = float(shopids[shopid])
                totalPrice = round(credit * price,2)
                money = float(sql.getMoney(message.chat.id))
                if totalPrice <= money:
                    status_1 = sql.Bought(sql.getUidByTgid(str(message.chat.id)),shopid,str(t),coupon,totalPrice)
                    status_2 = sql.UpdateUser(sql.getUidByTgid(str(message.chat.id)),totalPrice,str(t),details[shopid])
                    if status_1 and status_2 is True:
                        bot.send_message(message.chat.id,'购买成功,当前余额为%s'%sql.getMoney(message.chat.id))

                else:
                    bot.send_message(message.chat.id,'余额不足请充值')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(10)
