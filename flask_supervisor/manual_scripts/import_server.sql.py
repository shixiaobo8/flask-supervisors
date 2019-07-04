#!/usr/bin/env python3
# -*- coding:utf8 -*-
# 导入server 主机列表服务器
# 打开数据库连接
import pymysql
import traceback


try:
	db = pymysql.connect("localhost","root","123456","xj_omsa" ) 
	# 使用 cursor() 方法创建一个游标对象 cursor
	cursor = db.cursor()
	with open("./server1.txt","r",encoding="UTF-8") as f:
		for line in f.readlines():
			line_data = line.split("\t")
			ali_instance_id = line_data[0]
			hostname = line_data[1]
			host_info = line_data[2] + "/" + line_data[7] + "c/" + line_data[8] + "M" 
			host_inner_ip = line_data[5]
			host_public_ip = line_data[4]
			sv_port = 22
			sv_node_id = 2 
			cursor.execute("SELECT * from sv_hosts where ali_instance_id='"+ali_instance_id+"';")
			data = cursor.fetchall()
			sql = "insert into sv_hosts(`ali_instance_id`,`hostname`,`host_info`,`host_inner_ip`,`host_public_ip`,`sv_port`,`sv_node_id`,`is_del`) values('%s','%s','%s','%s','%s','%d','%d','%d');"%(ali_instance_id,hostname,host_info,host_inner_ip,host_public_ip,sv_port,sv_node_id,0)
			if data:
				sql = "update sv_hosts set ali_instance_id='"+ali_instance_id+"',hostname='"+hostname+"',host_info='"+host_info+"',host_inner_ip='"+host_inner_ip+"',host_public_ip='"+host_public_ip+"',sv_port=22,sv_node_id=2,is_del=0 where ali_instance_id='"+ali_instance_id+"';"
			print(sql)
			rs=cursor.execute(sql)
			print(rs)
			db.commit()
except Exception as e:
	print(e)
	traceback.print_exc()
finally:
	db.close()