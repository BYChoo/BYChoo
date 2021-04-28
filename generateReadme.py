# -*- coding: utf-8 -*-
import urllib3
from lxml import etree
import html
import re
import sys

blogUrl = 'https://bychoo.github.io/categories/'
URL = "https://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day"

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'} 

def addStaticInfo(f):
	txt = '''  
<p>
  <img src="https://raw.githubusercontent.com/Vivekagent47/Vivekagent47/master/hello.svg">
</p>

# Hi, I'm Choo 👋

- 🔭 I’m currently working on ... Not working
- 🌱 I’m currently learning ...  React and nodejs
- 👯 I’m looking to collaborate on ... Any of project
- 🤔 I’m looking for help with ... Vuejs and React
- 💬 Ask me about ... What ever
- 😄 Pronouns: ... He
- ⚡ Fun fact: ... Play PUBG when get bored

### Languages and Tools:
<div display="flex">
  <img src="https://img.shields.io/badge/html5%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/css3%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white">
  <img src="https://img.shields.io/badge/javascript-%23F7DF1E.svg?&style=for-the-badge&logo=javascript&logoColor=black&labelColor=black">
  <img src="https://img.shields.io/badge/react%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Nodejs%20-%2300599C.svg?&style=for-the-badge&logo=node&logoColor=white">
  <img src="https://img.shields.io/badge/vuejs%20-%2335495e.svg?&style=for-the-badge&logo=vue.js&logoColor=%234FC08D">
  <img src="https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white"/>
  <img src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white"/>
  <img src="https://img.shields.io/badge/markdown-%23000000.svg?&style=for-the-badge&logo=markdown&logoColor=white" />
</div>

### Machine:
<div display="flex">
  <img src="https://img.shields.io/badge/windows-%20GL63%208RC-%23F50F0F.svg?&style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/linux-%20GL63%208RC-%23dd4814.svg?&style=for-the-badge&logo=linux&logoColor=white">
</div>
<br>

[![我的 GitHub 数据](https://github-readme-stats.vercel.app/api?username=BYChoo&show_icons=true&theme=graywhite)]()

## 我的博客

🔗   https://bychoo.github.io/

''' 
	f.write(txt)
	

def addBlogInfo(f):  
	http = urllib3.PoolManager(num_pools=5, headers = headers)
	resp = http.request('GET', blogUrl)
	resp_tree = etree.HTML(resp.data.decode("utf-8"))
	html_data = resp_tree.xpath(".//li[@class='category-list-item']")
	print(html_data)
# 	f.write("\n### 我的博客\n")
	for i in html_data: 
		category_title = i.xpath("./a/text()")[0].strip()
		print(category_title)
		f.write("\n### " + category_title + "\n")
		
		# 获取子节点列表
		url = i.xpath('./a/@href')[0] 
		list_url = "https://bychoo.github.io" + url
		print(list_url)
		resp2 = http.request('GET', list_url)
		resp_tree2 = etree.HTML(resp2.data.decode("utf-8"))
		html_data2 = resp_tree2.xpath(".//div[@class='post-title']")
		for i in html_data2: 
			title2 = i.xpath("./a/span/text()")[0].strip()
			print(title2)
			url2 = i.xpath('./a/@href')[0] 
			item2 = '- [%s](%s)\n' % (title2, "https://bychoo.github.io"+url2)
			f.write(item2)

def fetch_image(f):
	print("download image...")
	f.write("\n### 每日一图\n")
	http = urllib3.PoolManager(num_pools=5, headers = headers)
	resp = http.request('GET', URL)
	resp_tree = etree.HTML(resp.data.decode("utf-8"))
	presentation_table =  resp_tree.xpath("//table[@role='presentation']")[0]
	a_tag = presentation_table.xpath(".//a[@class='image']")[0]
	relative_link = a_tag.get("href")
	title = a_tag.get("title")
	image_src = a_tag.xpath("./img/@srcset")[0]
	best_image = image_src.split(" ")[0]
	print(f"{relative_link} {title}, image srcset:{image_src}")
	print(f"best image: {best_image}")
	item_url = "https://" + best_image[2:]
	item = "![House in Provence](" + item_url + ")"
	f.write(item)
# 	return relative_link, title, "https://" + best_image[2:]


if __name__=='__main__':
	f = open('README.md', 'w+')
	addStaticInfo(f)
	addBlogInfo(f)
	fetch_image(f)
	
