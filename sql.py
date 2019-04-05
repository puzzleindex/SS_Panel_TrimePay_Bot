import config
import pymysql
import time

#数据库链接信息
def getConnect():
	db = pymysql.connect(config.db_host,config.db_username,config.db_password,config.db_database)
	return db

#通过tg id 获取user id
def getUidByTgid(tgid):
    db = getConnect()
    cursor = db.cursor()
    sql = 'SELECT id FROM user WHERE telegram_id = ' + tgid
    try:
        cursor.execute(sql)
        data = str(cursor.fetchone()[0])
    except:
        data = False
        print('获取uid失败')
    finally:
        db.close()
    return data


#创建paylist
def newPaylist(userid,total,tradeno):
    status = False
    db = getConnect()
    cursor = db.cursor()
    sql = "INSERT INTO `paylist` (`id`, `userid`, `total`, `status`, `tradeno`, `datetime`, `type`, `url`) VALUES (NULL, '%s', '%s', '0', '%s', '0', '0', NULL)"%(userid,total,tradeno)
    try:
        cursor.execute(sql)
        db.commit()
        status = True
    except:
        print('创建paylist失败')
    finally:
        db.close()
    return status

#查询余额
def getMoney(tgid):
	db = getConnect()
	cursor = db.cursor()
	sql = 'SELECT money FROM user WHERE telegram_id = ' + str(tgid)
	try:
		cursor.execute(sql)
		data = str(cursor.fetchone()[0])
	except:
		data = False
		print('查询余额失败')
	finally:
		db.close()
	return data

#获取套餐列表
def getGoods():
	db = getConnect()
	cursor = db.cursor()
	sql = 'SELECT * FROM shop WHERE status = 1'
	try:
		cursor.execute(sql)
		data = cursor.fetchall()
	except:
		data = False
		print('查询套餐列表失败')
	finally:
		db.close()
	return data

#获取coupon
def getCoupon(coupon):
	db = getConnect()
	cursor = db.cursor()
	sql = 'SELECT * FROM coupon WHERE code = ' + coupon
	try:
		cursor.execute(sql)
		data = cursor.fetchone()
	except:
		data = False
		print('获取coupon失败')
	finally:
		db.close()
	return data

#创建Bought记录
def Bought(userid,shopid,t,coupon,price):
	status = False
	db = getConnect()
	cursor = db.cursor()

	sql = "INSERT INTO `bought` (`id`, `userid`, `shopid`, `datetime`, `renew`, `coupon`, `price`) VALUES (NULL, '%s', '%s', '%s', '0', '%s', %s)"%(userid,shopid,t,coupon,price)
	try:
		cursor.execute(sql)
		db.commit()
		status = True
	except:
		print('创建bought失败')
	finally:
		db.close()
	return status

#购买套餐修改user表
def UpdateUser(userid,price,t,details):
	status = False
	db = getConnect()
	cursor = db.cursor()
	details = eval(details)
	transfer_enable = int(details['bandwidth']) * 1024 * 1024 * 1024
	node_connector = int(details['connector'])
	_class = int(details['class'])
	class_expire = int(t) + int(details['class_expire']) * 24 * 60 * 60
	class_expire = time.localtime(class_expire)
	class_expire = time.strftime("%Y-%m-%d %H:%M:%S",class_expire)

	sql = "UPDATE `user` SET `u` = 0, `d` = 0, `transfer_enable` = %d, `money` = `money` - %f, `node_connector` = %d, `last_day_t` = 0, `class` = %d, `class_expire` = str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s') WHERE id = %s"%(transfer_enable,price,node_connector,_class,class_expire,userid)
	
	try:
		cursor.execute(sql)
		db.commit()
		status = True
	except:
		print('更新user失败')
	finally:
		db.close()
	return status