# SS_Panel_TrimePay_Bot

# 魔改Trimepay充值以及购买套餐


1.tg国内被墙,所以tgbot运行环境必须是国外ip的机器


2.去bot father那申请一个充值用的bot


```
git clone -b master https://github.com/number018/SS_Panel_TrimePay_Bot.git
```

```
cd SS_Panel_TrimePay_Bot && vi config.py
```
在config中填好相关信息

```
nohup python main.py &
```

### 注:
本程序不支持套餐renew

套餐也别设置多少天重置多少流量那种(因为我直接对sql进行修改的,没改到这里)



## 使用教程

充值:

对bot发送  
支付宝充值+金额,比如支付宝充值10

微信充值+金额,比如微信充值10(trimepay微信已改为WEPAY_QR,没有WEPAY_JSAPI感觉微信充值废了)

查询余额:
对bot发送查询余额,即可查看账户余额

购买套餐:
对bot发送套餐列表,bot会返回套餐id,名称,价格

然后发送购买套餐+套餐id,例如购买套餐1,即可购买成功

若使用优惠码,则发送 购买套餐+套餐id 优惠码,中间有个空格,例如   购买套餐1 HAPPY_NEW_YEAR

优惠码默认全套餐可用...只通过过期时间来判断是否可用(懒)

余额不足肯定购买不成功啦


不管啦...使用本程序自行承担一定风险...代码写的比较烂,凑活着用吧...
