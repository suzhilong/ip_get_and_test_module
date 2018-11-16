# -*- coding: utf-8 -*-

##############不加这段会报错
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
################

import random,requests,time,re

user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]

def get_random_header():
    headers={
        'User-Agent':random.choice(user_agent),
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding':'gzip'
        }
    return headers

def scraw_proxies(page_num,scraw_url="http://www.xicidaili.com/nt/"):
    #从西刺代理网站提取ip数据
    scraw_ip=list()
    available_ip=list()
    page_num = page_num + 1
    for page in range(1,page_num):
        print("抓取第%d页代理IP" %page)
        url=scraw_url+str(page)
        r=requests.get(url,headers=get_random_header())
        r.encoding='utf-8'
        pattern = re.compile(u'<tr class=".*?">.*?'
                           +u'<td class="country"><img.*?/></td>.*?'
                           +u'<td>(\d+\.\d+\.\d+\.\d+)</td>.*?'
                           +u'<td>(\d+)</td>.*?'
                           +u'<td>.*?'
                           +u'<a href=".*?">(.*?)</a>.*?'
                           +u'</td>.*?'
                           +u'<td class="country">(.*?)</td>.*?'
                           +u'<td>([A-Z]+)</td>.*?'
                           +'</tr>', re.S)
        scraw_ip= re.findall(pattern, r.text)
        
        #############清洗ip#############
        scraw_ip_htt = []
        for i in range(len(scraw_ip)):
            if scraw_ip[i][4] == "HTTP":
                scraw_ip_htt.append([scraw_ip[i][0],scraw_ip[i][1],'http',scraw_ip[i][3]])
            if scraw_ip[i][4] == "HTTPS":
                scraw_ip_htt.append([scraw_ip[i][0],scraw_ip[i][1],'https',scraw_ip[i][3]])
        #################################

        #测试ip
        for ip in scraw_ip_htt:
            if(test_ip(ip,5)==True):
                print('%s:%s %s 通过测试，添加进可用代理列表' %(ip[0],ip[1],ip[2]))
                print('--------------此IP测试通过-------------')
                available_ip.append(ip)
            else:
                pass    
        print("代理爬虫暂停10s")
        time.sleep(10)
        print("爬虫重启")
    print('抓取结束')
    #返回测试通过的ip
    return available_ip

#测试ip网站，前面年需要更新，改为当前年
def test_ip(ip,time_out,test_url='http://2018.ip138.com/ic.asp'):
    '''
    #http和https需要分开测试
    #透明的就不需要
    if ip[3] == '透明':
        proxies = {'http': ip[0] + ':' + ip[1]}
    else:
        if ip[2] == 'http':
            proxies={
                'http': ip[0] + ':' + ip[1],
                'https': ''
                }
        elif ip[2] == 'https':
            proxies={
                'http': '',
                'https': ip[0] + ':' + ip[1]
                }
    '''
    proxies = {'http': ip[0] + ':' + ip[1]}
    #print(proxies)
    try_ip=ip[0]
    #print(try_ip)
    #判断携带的ip与请求显示的ip是否一致，一致说明成功
    try:
        r=requests.get(test_url,headers=get_random_header(),proxies=proxies,timeout=time_out)
        #print(r.status_code)
        if r.status_code==200:
            #提取出当前ip
            r.encoding='gbk'
            result=re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',r.text)
            result=result.group()
            #比较两个测试ip和请求得到ip
            if result[:9]==try_ip[:9]:
                #print(r.text)
                print('--------------此IP测试通过-------------')
                return True
            else:
                print('%s:%s %s 携带代理失败,使用了本地IP' %(ip[0],ip[1],ip[2]))
                return False    
        else:
            print('%s:%s %s 请求码不是200,是%s' %(ip[0],ip[1],ip[2],str(r.status_code)))
            return False
    except:
        print('%s:%s %s 请求过程错误' %(ip[0],ip[1],ip[2]) )
        return False

#只取 http 的 ip
def get_http_ip(available_ip):
    http_ip = []
    for ip in available_ip:
        if ip[2] == 'http':
            proxy = 'http://' + ip[0] + ':' + ip[1]
            http_ip.append(proxy)
    return http_ip
#只取 https 的 ip
def get_https_ip(available_ip):
    https_ip = []
    for ip in available_ip:
        if ip[2] == 'https':
            proxy = 'https://' + ip[0] + ':' + ip[1]
            https_ip.append(proxy)
    return https_ip
    

if __name__=="__main__":
    #修改需要爬取的页数
    available_ip=scraw_proxies(1)
    #print(available_ip)
    http_ip = get_http_ip(available_ip)
    https_ip = get_https_ip(available_ip)
    print('http代理:')
    print(http_ip)
    print('---------------------')
    print('https代理:')
    print(https_ip)