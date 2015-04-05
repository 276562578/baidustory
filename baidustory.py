#!/usr/bin/python
#coding:utf-8
print '这是一个抓取百度贴吧小说的爬虫，将某部小说贴吧的精品贴进行抓取并合并在一起'+'\n'

import urllib2
import re
#url=raw_input('请输入精品连载贴地址')
url='http://tieba.baidu.com/f/good?kw=%E5%A4%A7%E4%B8%BB%E5%AE%B0&ie=utf-8&cid=2'

#找到每一章节帖子的地址，并以page_address列表形式存储
def get_page_address():
	
	#这里的函数可以连起来写
	#像这样  html=urllib2.urlopen('www.com').read()
	html=urllib2.urlopen(url).read().decode("utf-8")
        print "正在请求网页......"
	#正则寻找每个帖子的地址 
	find_page_string=re.compile(r'<a href="/p/.*?" title=.*?\" target="_blank"')
	page_string=find_page_string.findall(html)
        print "正在分析网页......"
        all_page_string=""
	for i in page_string:
		all_page_string=all_page_string+i
	find_page_number=re.compile(r'\d{10}')
	page_number=find_page_number.findall(all_page_string)
	page_address=[]
	for p in range(len(page_number)):
		page_address.append("http://tieba.baidu.com/p/"+str(page_number[p]))
        print "已得到网页列表"
        return(page_address)

def get_article(page_address):
        article_html=[]
        crude_article=[]
        article=[]
	for p in range(2):        
                article_html.append(urllib2.urlopen(page_address[p]).read().decode("utf-8"))
                print "正在添加第"+str(p+1)+"篇文章"
                find_crude_article=re.compile(r'd_post_content j_d_post_content.*?share_thread share_thread_wrapper')
                crude_article.append(find_crude_article.findall(article_html[p]))
                
                article_begin_dropped=re.compile(r'd_post_content j_d_post_content ">')
                crude_article[p]=article_begin_dropped.sub(r'',crude_article[p][0])
                article_end_dropped=re.compile(r'</div>.*share_thread_wrapper')
                crude_article[p]=article_end_dropped.sub(r'',crude_article[p])
                article_br_replace=re.compile(r'<br>.*?<br>')
                article.append(article_br_replace.sub(r'\n',crude_article[p]))
                
                print article[p]
get_article(get_page_address())
