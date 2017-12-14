#-*-encoding:utf-8-*-
import json
import requests
import execjs
from bs4 import BeautifulSoup

class anyew():

	session = requests.Session()
	home_url = "http://m.anyew.cn"

	def __init__(self):

		print("######## 暗夜小说网spider ########")
		print("功能如下：1、搜索 2、小说详情")
		while(True):
			operation = input("输入操作：")
			if(int(operation) == 1):
				keyword = input("输入搜索关键词：")
				search_list = self.search(keyword)
				print(search_list)

			elif(int(operation) == 2):
				book_id = input("输入小说id：")
				book_info = self.getBookInfo(book_id)
				print(book_info)
			
			else:
				break

	### 解密，参数为章节页面返回的class为data-trda和data-trdkk的input的value值 ###
	def descrypt(self, trda, trdkk):

		fp = open("./解密.js")
		js = fp.read()
		fp.close()
		ctx = execjs.compile(js)
		return_data = (ctx.call("test", data_trda, data_trdkk))
		return return_data	

	### 搜索，参数为搜索关键词 ###
	def search(self, keyword):

		# result_list = []
		
		# search_url = self.home_url + "/search-index"
		# page = 1
		# params = {
		# 	"word" : keyword,
		# 	"page" : page
		# }
		# req = self.session.get(url=search_url, params=params)
		# html = BeautifulSoup(req.text, "html.parser")
		# dls = html.select(".search_box .search_result .pictxtbox")
		# for dl in dls:
		# 	book_info = {}
		# 	book_info["head"] = dl.select("dt img")[0]["src"]
		# 	book_info["name"] = dl.select("dd h3")[0].text
		# 	book_info["author"] = dl.select("dd span")[0].text
		# 	book_info["desc"] = dl.select("dd p")[0].text
		# 	result_list.append(book_info)		

		# return result_list

		result_dict = {}
		search_url = self.home_url + "/search-search_json"
		page = 1
		params = {
			'page':page,
			'word':keyword
		}
		req = self.session.get(url=search_url, params=params)
		json_data = json.loads(req.text)
		count = json_data["count"]
		page_count = int(count/10) + 1
		result_dict["count"] = count
		for i in range(1,page_count+1):
			params = {
				'page':page,
				'word':keyword
			}
			req = self.session.get(url=search_url, params=params)
			json_data = json.loads(req.text)
			result_dict["books"] = []
			for book in json_data["books"]:
				result_dict["books"].append(book)

		return result_dict

	### 获取书籍信息，参数为书籍id，返回dict ###
	def getBookInfo(self, book_id):

		book_info = {} 

		## 获取小说作者、简介等信息 ##
		book_url = self.home_url + "/book/" + book_id
		req = self.session.get(book_url)
		html = BeautifulSoup(req.text, "html.parser")
		dl = html.select(".detail_head dl")[0]
		book_info["head"] = dl.select("dt img")[0]["src"]
		book_info["name"] = dl.select("dd h2")[0].text.strip()
		book_info["author"] = {
			"name" : dl.select("dd p a")[0].text,
			"href" : self.home_url + dl.select("dd p a")[0]["href"]
		}
		book_info["type"] = dl.select("dd p")[1].text
		book_info["words"] = dl.select("dd p")[2].text

		## 获取小说章节信息 ##
		chapter_url = self.home_url + "/chapters/" + book_id
		req = self.session.get(chapter_url)
		req.encoding = "utf-8"
		html = BeautifulSoup(req.text,"html.parser")
		chap_li_as = html.select(".chapter-list .bd .list li a")
		chapter_list = []
		for chap_li_a in chap_li_as[:-1]:
			chapter_info = {}
			chapter_info["title"] = chap_li_a.text.strip()
			chapter_info["href"] = self.home_url + chap_li_a['href']
			chapter_list.append(chapter_info)
		book_info["chapter_info"] = chapter_list

		return book_info

	### 获取小说章节内容，参数为章节url，返回章节内容 ###
	def getChapterContent(self, chapter_url):

		req = session.get(chap_href)
		html = BeautifulSoup(req.text,"html.parser")
		data_trda = html.select(".data-trda")[0]["value"]
		data_trdkk = html.select(".data-trdkk")[0]["value"]
		data_trdkk = data_trdkk.split("=")[1]
		## 数据解密
		return_data = descrypt(trda,trdkk)
		return return_data

def main():

	anyew_obj = anyew()

if __name__ == '__main__':
	main()