# -*- coding: utf-8 -*-

import os
import time
import sys
sys.path.append('..')
from jntemplate import Template,engine,BaseLoader,FileLoader 


class Article(object):
    def ___init___(self):
        self.basis_id = 0
        self.category_id = 0
        self.content = ""
        self.create_date = time.localtime(time.time())
        self.default_picture = ""
        self.description = ""
        self.edit_date = time.localtime(time.time())
        self.english_name = ""
        self.module_id = 0
        self.title = ""


class Product(object):
    def ___init___(self):
        self.basis_id = 0
        self.category_id = 0
        self.content = ""
        self.create_date = time.localtime(time.time())
        self.date_price = 0
        self.default_picture = ""
        self.description = ""
        self.download_url = ""
        self.edit_date = time.localtime(time.time())
        self.english_name = ""
        self.exampleUrl = ""
        self.file_size = ""
        self.gateway = ""
        self.module_id = 0
        self.title = ""


class Category(object):
    def ___init___(self):
        self.category_id = 1
        self.category_name = "栏目1"
        self.create_date = time.localtime(time.time())
        self.deph = 1
        self.english_name = "001"
        self.module_id = 1


class ProductModule(object):
    def ___init___(self):
        self.basis_id = 0
        self.module_name = ""
        self.product_module_id = 0


class Help(object):
    def ___init___(self):
        self.basis_id = 0
        self.category_id = 0
        self.content = ""
        self.create_date = time.localtime(time.time())
        self.default_picture = ""
        self.description = ""
        self.edit_date = time.localtime(time.time())
        self.english_name = ""
        self.module_id = 0
        self.title = ""


class DbRead(object):
    def test(self,message,  id,  result):
        return "您输入的参数是有：%s %d %s" % message % id % str(result)

    def get_help_list(self,category,  product,  module,  type_id):
        arr = []
        arr.append(Help())
        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "下单后可以修改订单吗？"

        arr.append(Help())

        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "无货商品几天可以到货？"

        arr.append(Help())

        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "合约机资费如何计算？"

        arr.append(Help())

        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "可以开发票吗？"

        return arr

    def get_article_list(self,id):
        arr = []
        arr.append(Article())
        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "购物流程"
        arr.append(Article())

        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "会员介绍"

        arr.append(Article())

        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "生活旅行/团购"

        arr.append(Article())

        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "常见问题"

        arr.append(Article())
        arr[-1].basis_id = 301
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "art001"
        arr[-1].module_id = 1
        arr[-1].title = "联系客服"

        return arr

    def get_product_list(self):
        arr = []
        arr.append(Product())

        arr[-1].basis_id = 201
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].date_price = 245
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].download_url = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "pro001"
        arr[-1].example_url = ""
        arr[-1].file_size = "564kb"
        arr[-1].gateway = ""
        arr[-1].module_id = 2
        arr[-1].title = "产品1"

        arr.append(Product())

        arr[-1].basis_id = 202
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].date_price = 245
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].download_url = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "pro001"
        arr[-1].example_url = ""
        arr[-1].file_size = "564kb"
        arr[-1].gateway = ""
        arr[-1].module_id = 2
        arr[-1].title = "产品2"

        arr.append(Product())

        arr[-1].basis_id = 203
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].date_price = 245
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].download_url = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "pro001"
        arr[-1].example_url = ""
        arr[-1].file_size = "564kb"
        arr[-1].gateway = ""
        arr[-1].module_id = 2
        arr[-1].title = "产品3"

        arr.append(Product())

        arr[-1].basis_id = 204
        arr[-1].category_id = 1
        arr[-1].content = ""
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].date_price = 245
        arr[-1].default_picture = ""
        arr[-1].description = ""
        arr[-1].download_url = ""
        arr[-1].edit_date = time.localtime(time.time())
        arr[-1].english_name = "pro001"
        arr[-1].example_url = ""
        arr[-1].file_size = "564kb"
        arr[-1].gateway = ""
        arr[-1].module_id = 2
        arr[-1].title = "产品4"
        return arr

    def get_category_list(self,mode):
        arr = []
        arr.append(Category())
        arr[-1].category_id = 1
        arr[-1].category_name = "栏目1"
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].deph = 1
        arr[-1].english_name = "001"
        arr[-1].module_id = 1

        arr.append(Category())
        arr[-1].category_id = 2
        arr[-1].category_name = "栏目2"
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].deph = 1
        arr[-1].english_name = "002"
        arr[-1].module_id = 1
        arr.append(Category())
        arr[-1].category_id = 3
        arr[-1].category_name = "栏目3"
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].deph = 1
        arr[-1].english_name = "003"
        arr[-1].module_id = 1

        arr.append(Category())
        arr[-1].category_id = 4
        arr[-1].category_name = "栏目4"
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].deph = 1
        arr[-1].english_name = "004"
        arr[-1].module_id = 1

        arr.append(Category())
        arr[-1].category_id = 5
        arr[-1].category_name = "栏目5"
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].deph = 1
        arr[-1].english_name = "005"
        arr[-1].module_id = 1

        arr.append(Category())
        arr[-1].category_id = 6
        arr[-1].category_name = "栏目6"
        arr[-1].create_date = time.localtime(time.time())
        arr[-1].deph = 1
        arr[-1].english_name = "006"
        arr[-1].module_id = 1
        return arr

    def get_product_url(self,model):
        if model.english_name != None and model.english_name != "":
            return "/Product/%s" % model.english_name
        else:
            return "/Product?id=%s" % model.english_name

    def get_article_url(self,model):
        if model.english_name != None and model.english_name != "":
            return "/Article/%s" % model.english_name
        else:
            return "/Article?id=%s" % model.english_name

    def get_help_url(self,model):
        if model.english_name != None and model.english_name != "":
            return "/Help/%s" % model.english_name
        else:
            return "/Help?id=%s" % model.english_name

    def get_product_item(self,key):
        model = Product()
        model.basis_id = 1
        model.category_id = 1
        model.content = """<p style="text-align: center text-indent: 0"><img src="http://upload.chinaz.com/2015/0624/1435111490722.jpg" border="0" alt="视频网站 付费会员"></p>
<p>6月24日报道&nbsp文/肖芳</p>
<p>近日，爱奇艺高调宣布其月度付费VIP会员数已达501.7万，并称视频付费业务台风已经到来。而阿里巴巴宣布进入视频付费市场，将推出付费视频服务TBO(Tmall&nbspBox&nbspOffice)，它的模式将更接近美国在线影片租赁提供商Netflix，其中90%的TBO内容都将采用付费观看模式。</p>
<p>这不是业界首次探讨视频网站收费的可能性了。早在2008年，激动网就正式推出了付费点播品牌“激动派”，虽然2011年激动网声称80%的收入来自付费用户，如今却已转型淡出视频行业。其他的也基本都是“雷声大，雨点小”，付费没有形成足够的阵势。当时有说法称“谁第一个收费谁就第一个倒下”。</p>
<p>时隔5年视频网站再次呼唤用户付费。业内人士透露，目前视频网站或片方都已经在酝酿网络付费看剧，试图在网络付费领域上分一杯羹，最快明年就会试水。这一次的底气在哪？谈论这个问题之前不妨先从5年前的收费为何没有成气候说起。</p>
<p><strong>早年内容不成熟&nbsp付费1~2元也无人问津</strong></p>
<p>2010年，迅雷看看推出向用户收费的“红宝石影院”业务，一期推广高清下载，二期将推广高清在线观看，一部电影收费大约1元-2元钱，高清在线观看的收费项目将成为现实。</p>
<p>由迅雷看看当时的宣传页面可以窥见“红宝石影院”的初衷：“买一张盗版碟至少要花5元钱，而在红宝石上下载一部正版高清电影最低只花2元钱。正版比盗版还便宜。”虽然在业务推出前期，迅雷看看展开声势浩大的宣传，但“红宝石影院”后来也销声匿迹，迅雷看看的营收依然是以传统的广告为主。今年年初，迅雷把一直处于亏损状态下的看看出售，免于拖累上市公司。</p>
<p>花2元看正版，比5元买盗版碟还便宜，这个初衷是好的，但也要考虑收费实施的基础。一方面是用户付费意愿，另一方面是视频网站的服务能否达到收费的水平。</p>
<p>在用户付费意愿上，2010年某门户网站曾经做过一项调查。结果显示，愿意为视频点播付费的网友只有383名，而不愿意的则达到6095名，后者是前者的15倍。由此可见，只有6%的网友愿意付费，没有用户的支持视频网站畅想的再美好都无济于事。</p>
<p>另一方面，2010年前后，在线视频的品质还不够好。由于带宽等因素的限制，视频很难达到高清的效果。同时，视频网站购买版权的意识也不如现在强，很多内容都来自网友上传，体验很差。</p>
<p>当时，另一家坚持免费观看的视频网站负责人道出了视频收费不宜大规模推广的原委。她指出，要想让用户掏钱看视频，首先要满足两个条件：一是网站要有独家的、不可替代的内容，否则网友不会“买账”；二是用户的使用习惯。对于前者，可以靠投入重金买版权来实现；但对于后者，她并不乐观地表示，让习惯了免费看视频的用户掏钱买收视权，短期内是不太现实的。</p>
<p><strong>服务升级后&nbsp视频网站亟需付费扭转巨亏</strong></p>
<p>可以看到，2010年之后视频网站在朝着正版化、高清化发展。视频网站在不断砸钱购买内容，同时也在改善视频播放技术，让网友获得更好的观看体验。</p>
<p>对比2010年优酷网和如今优酷土豆的财报便可以发现端倪。2010年第四季度，优酷的内容成本为1250万美元，比2009年增长11%，净亏损为570万美元。2014年第四季度，优酷土豆的内容成本为9,720万美元，是2010年同期的8倍，净亏损为5130万美元，接近2010年同期的10倍。</p>
<p>越是投入越是亏得厉害，不只是优酷，这是近5年来视频行业发展的缩影。可以看到多家视频网站因资金问题“卖身”，而现在留下的视频网站背后都背靠大树。没有巨头的支持，视频“烧钱”的游戏很难再持续下去。</p>
<p style="text-align: center text-indent: 0"><img src="http://upload.chinaz.com/2015/0624/1435111500344.jpg" border="0" alt="视频网站 付费会员"></p>
<p>视频网站付费会员增长超700% 苦熬7年再度掀付费潮</p>
<p>归根到底，这是由于广告收入的增速远远不及内容成本的增速（图为2014年优酷土豆内容成本和广告收入成本的同比增长），依靠内容投入拉动营收就如同一个无底洞，只会将自己陷得越来越深。</p>
"""
        model.create_date = time.localtime(time.time())
        model.date_price = 940
        model.default_picture = "http://upload.chinaz.com/2015/0624/1435111500344.jpg"
        model.description = "近日，爱奇艺高调宣布其月度付费VIP会员数已达501.7万，并称视频付费业务台风已经到来。而阿里巴巴宣布进入视频付费市场，将推出付费视频服务TBO(Tmall&nbspBox&nbspOffice)，它的模式将更接近美国在线影片租赁提供商Netflix，其中90%的TBO内容都将采用付费观看模式。"
        model.edit_date = time.localtime(time.time())
        model.english_name = "001"
        model.example_url = "http://www.baidu.com"
        model.file_size = "54KB"
        model.title = "视频网站付费会员增长超700% 苦熬7年再度掀付费潮"
        return model

    def get_default_int(self,key,  defaultValue):
        return defaultValue

    def get_product_module(self,product):
        arr = []
        arr.append(ProductModule())
        arr[-1].basis_id = 101
        arr[-1].module_name = "测试模块"
        arr[-1].product_module_id = product

        arr.append(ProductModule())
        arr[-1].basis_id = 102
        arr[-1].module_name = "订单模块"
        arr[-1].product_module_id = product

        arr.append(ProductModule())
        arr[-1].basis_id = 103
        arr[-1].module_name = "产品模块"
        arr[-1].product_module_id = product
        arr.append(ProductModule())
        arr[-1].basis_id = 104
        arr[-1].module_name = "新闻模块"
        arr[-1].product_module_id = product
        return arr

    def get_page_index(self):
        return 1

    def get_pager(self):
        return '<span>首页</span> <span>上一页</span> <a href=\"?page=1\">1/a> <span>下上一页</span> <span>末页</span>'

if __name__ == '__main__':
    loader = FileLoader()
    db = DbRead()
    loader.directories.append(os.getcwd()+'\\templets\\')
    loader.directories.append(os.getcwd()+'\\templets\\public\\')
 
    engine.configure(loader=loader) 
    template = engine.load("questionlist.html")
    template.set("func", db)
    html = template.render()
    print(html)