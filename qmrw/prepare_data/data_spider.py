import urllib.request
import urllib.parse
from lxml import etree
import pymongo
import json
'''爬虫类'''
class KaoyanSpider:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['kaoyan']
        self.col = self.db['data']

    '''根据url，请求html'''
    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk','ignore')
        return html

    '''找到哪个省'''
    def province_spider(self,url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        u1_list = selector.xpath('/html/body/div[3]/div/div/div[2]/div[2]/div/div[2]/div[3]/ul')
        for u1 in u1_list:
            li_list = u1.xpath('./li')
        province = []
        for li in li_list:
            info = li.xpath('./a/text()')[0]
            province.append(info)
            # 保存数据为txt格式
        with open('./dict/' + 'province.txt', 'w',encoding='utf-8') as fp:
            for xx in province:
                fp.write(str(xx))
                fp.write('\n')

        return province#返回列表
    '''链接:这里返回的是各省的招生单位'''
    def school_spider(self,url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        li_list = selector.xpath('/html/body/div[3]/div/div/div[2]/div[2]/div/div[2]/div[3]/ul/li')
        link = []
        for li in li_list:
            info2 = li.xpath('./a/@href')
            info = 'http://www.chinakaoyan.com' + info2[0]
            link.append(info)

        return link
    '''所有学校名和链接：这里返回的是所有的学校的名字和学校的链接'''
    def school_all_spider(self,url):
        informa = self.school_spider(url)
        school_data = {}
        link_ = []
        school = []
        for url in informa:
            html = self.get_html(url)
            selector = etree.HTML(html)
            li_list = selector.xpath('/html/body/div[3]/div[1]/div/div[3]/div[3]/div/ul/li')
            for li in li_list:
                info = li.xpath('./a/text()')[0]
                link = li.xpath('./a/@href')
                linkk = 'http://www.chinakaoyan.com' + link[0]
                link_.append(linkk)
                school.append(info)
            school_data['name'] = school
            school_data['link'] = link_
            js_sd = json.dumps(school_data,ensure_ascii=False)
        with open('./dict/' + 'school.txt', 'w',encoding='utf-8') as fp:
            for xx in school:
                fp.write(str(xx))
                fp.write('\n')
        return school
    '''各个学校的基本信息：这里返回的是学校内部页面直接可获取的信息：地址，电话，官网'''
    def school_info_spider(self,url):
        infomat = self.school_all_spider(url)
        locate = []
        guanwang = []
        desc = []
        num = []
        xxxx = {}
        for url in infomat:
            html = self.get_html(url)
            selector = etree.HTML(html)
            loca = selector.xpath('/html/body/div[8]/div[3]/p[1]/text()')
            locate.append(loca)
            phone_num = selector.xpath('/html/body/div[8]/div[3]/p[2]/text()')
            num.append(phone_num)
            guan = selector.xpath('/html/body/div[8]/div[3]/p[3]/a/@href')
            guanwang.append(guan)
        xxxx['学校地址'] = locate
        xxxx['学校官网'] = guanwang
        xxxx['联系电话'] = num
        with open('./dict/' + 'locate.txt', 'w',encoding='utf-8') as fp:
            for xx in locate:
                fp.write(str(xx))
                fp.write('\n')
        with open('./dict/' + 'guanwang.txt', 'w', encoding='utf-8') as fp:
            for xx in guanwang:
                fp.write(str(xx))
                fp.write('\n')
        with open('./dict/' + 'phonenum.txt', 'w', encoding='utf-8') as fp:
            for xx in num:
                fp.write(str(xx))
                fp.write('\n')
        js_xx = json.dumps(xxxx,ensure_ascii=False)
        return js_xx
    '''学校批次'''
    def pici_spider(self,url):
        pp = ['985','211','zhx']
        pici = {}
        i = 0
        for ii in pp:
            urlp = url + pp[i] + '/shtml'
            htmlp = self.get_html(urlp)
            selectorp = etree.HTML(htmlp)
            li_list = selectorp.xpath('/html/body/div[3]/div[1]/div/div[3]/div[3]/div/ul/li')
            for li in li_list:
                info = li.xpath('./a/text()')
                pici[ii] = info
        i+=1
        js_pc = json.dumps(pici,ensure_ascii=False)
        return js_pc
    '''学校简介：这里返回的是学校所有简介'''
    def jbxx_spider(self,url):
        #首先先将学校的链接使用从而得到新链接
        infomat = self.school_all_spider(url)
        desc = []
        for url in infomat:
            html = self.get_html(url)
            selector = etree.HTML(html)
            #新连接
            new_link = selector.xpath('/html/body/div[4]/ul/li[2]/a/@href')
            new_linkk = 'http://www.chinakaoyan.com' + new_link[0]
            new_html = self.get_html(new_linkk)
            new_selector = etree.HTML(new_html)
            #新建一个列表保存其所有的简介
            descc = new_selector.xpath('/html/body/div[7]/div[1]/div[1]/p[1]/text()')[0]
            desc.append(descc)
        with open('./dict/' + 'desc.txt', 'w', encoding='utf-8') as fp:
            for xx in desc:
                fp.write(str(xx))
                fp.write('\n')
        return desc
    '''学校的院系设置'''

    '''学校各院系的专业有哪些'''
    def major_spider(self,url):
        infomat = self.school_all_spider(url)
        major = []
        academy = []
        yuanxi = {}
        for url in infomat:
            html = self.get_html(url)
            selector = etree.HTML(html)
            # 新连接
            new_link = selector.xpath('/html/body/div[4]/ul/li[3]/a/@href')
            new_linkk = 'http://www.chinakaoyan.com' + new_link[0]
            #print(new_linkk)
            new_html = self.get_html(new_linkk)
            new_selector = etree.HTML(new_html)
            # 新建一个列表保存其所有的专业
            div_list = new_selector.xpath('/html/body/div[7]/div[1]/div[3]/div')
            for div in div_list:
                info1 = div.xpath('./h3/text()')
                academy.append(str(info1).replace('/r/n','').replace('[]',''))
                data = div.xpath('./ul/li/a/text()')
                major.append(str(data).replace('[]',''))
        yuanxi['学院'] = academy
        yuanxi['专业'] = major
        with open('./dict/' + 'major.txt', 'w',encoding='utf-8') as fp:
            for xx in major:
                fp.write(str(xx))
                fp.write('\n')
        return yuanxi

if __name__ == '__main__':
    handl = KaoyanSpider()
    url = 'http://www.chinakaoyan.com/graduate/'
    #filename = 'data'
    Yuanxi = handl.major_spider(url)
    sc_name = handl.school_spider(url)
    sc_provin = handl.province_spider(url)
    Sc_addr = handl.school_info_spider(url)
    sc_desc = handl.jbxx_spider(url)
    School = {}
    School['学校名称'] = sc_name
    #School['省份'] = sc_provin
    School['简介'] = sc_desc
    School.update(Sc_addr)
    js = json.dumps(School,ensure_ascii=False)
    js1 = json.dumps(Yuanxi,ensure_ascii=False)
    with open('./data/' + 'school.json','w',encoding='UTF-8') as fp:
        fp.write(School)
#学校名称: 学校办学：学校省份：学校具体地址：联系电话：学校官网：院系：简介：
