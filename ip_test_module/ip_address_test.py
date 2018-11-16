import requests
from bs4 import BeautifulSoup

#检测当前ip
url = 'http://2018.ip138.com/ic.asp'
#把相应代理放入测试池
proxies = [
	{
	"http":"219.159.38.198:56210",
	#"https":"114.119.116.93:61066",
	},
	]
head = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', 
	'Connection': 'keep-alive'
	}
for proxy in proxies:
	req = requests.get(url,headers=head,proxies=proxy,timeout=10)
	print(req.status_code)
	req.encoding = 'GB2312'
	soup = BeautifulSoup(req.text, 'html.parser')
	ip = soup.select('body center')[0].get_text()
	print(ip)
