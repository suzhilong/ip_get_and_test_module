# coding: utf-8

import telnetlib

def single_ip_test(test_ips):
	for test_ip in test_ips:
		ip = test_ip.split(':')[0]
		port = test_ip.split(':')[1]
		# 连接Telnet服务器
		try:
		    tn = telnetlib.Telnet(ip,port=port,timeout=10)
		except:
		    print(test_ip + '--该代理IP  无效')
		else:
		    print(test_ip + '--该代理IP  有效')
def main():
	#放入待测ip
	test_ips = [
		'219.159.38.198:56210',
		]
	single_ip_test(test_ips)
   
if __name__ == '__main__':
	main()


