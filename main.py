from bs4 import BeautifulSoup
import requests
import json, os

def getSoup(website):
	r= requests.get(website)
	data = r.text
	soup = BeautifulSoup(data, "html5lib")
	return soup

def scrap(key, websites):
	soup= getSoup(websites[key])
	data= {}
	if websites[key]== "http://www.x6x.net/vb/":
		try:
			os.mkdir(key)
		except FileExistsError:
			pass
		os.chdir(key)
		data["Sections"]= []
		try:
			os.mkdir("Sections")
		except FileExistsError:
			pass
		os.chdir("Sections")
		for item in soup.find_all("td", {"class": "alt1Active"}):
			a_tag= item.find("a")
			a_text= a_tag.text.replace("/", " ")
			data["Sections"].append({"Name": a_text, "Link": a_tag["href"]})
			try:
				os.mkdir(a_text)
			except FileExistsError:
				pass
		for section in data["Sections"]:
			os.chdir(section["Name"])
			section["Posts"]= []
			try:
				os.mkdir("Posts")
			except FileExistsError:
				pass

			os.chdir("Posts")
			link= section["Link"]
			while True:
				section_soup= getSoup(link)
				for item in section_soup.select("a[id*= thread_title_]"):
					title= item.text.replace("/", " ")
					tmp= {"Title":title,"Link": item["href"]}
					if tmp not in section["Posts"]:
						section["Posts"].append(tmp)
						try:
							os.mkdir(title)
						except FileExistsError:
							pass
				next_page= section_soup.select("a[title*='الصفحة التالية -']")
				if len(next_page)> 0:
					link= next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				print(os.getcwd())
				os.chdir(post["Title"])
				link= post["Link"]
				post["Replies"]= []
				try:
					os.mkdir("Replies")
				except FileExistsError:
					pass
				os.chdir("Replies")
				while True:
					post_soup= getSoup(link)
					i= 0
					for item in post_soup.select("table[id*= post]"):
						infos1= item.find("a", {"class": "bigusername"})
						infos2= item.find("div", {"class": "smallfont hideonmobile"})
						content= item.select("div[id*=post_message_]")[0]
						try:
							itext1= infos1.text
						except Exception as e:
							print(e)
							itext1= ""
						try:
							itext2= infos2.text
						except Exception as e:
							print(e)
							itext2= ""
						try:
							ctext= content.text
						except Exception as e:
							print(e)
							ctext= ""
						if not os.path.isfile('{}.json'.format(i)):
							with open('{}.json'.format(i), 'w') as json_file:
								json.dump({"Infos":itext1+" "+ itext2, "Content": ctext}, json_file)
								# print('{}.json Created !'.format(key))
						i+= 1
					next_page= post_soup.select("a[title*='الصفحة التالية -']")
					if len(next_page)> 0:
						link= next_page[0]["href"]
					else:
						break
				os.chdir("../..")
			os.chdir("../..")
	elif websites[key]== "http://v4-team.com/cc/index.php":
		try:
			os.mkdir(key)
		except FileExistsError:
			pass
		os.chdir(key)
		data["Sections"]= []
		try:
			os.mkdir("Sections")
		except FileExistsError:
			pass
		os.chdir("Sections")
		for item in soup.find_all("td", {"class": "alt1Active"}):
			for a_tag in item.find_all("a"):
				link= a_tag["href"]
				name= a_tag.text.replace("/", " ").strip("\n")
				data["Sections"].append({"Name": name ,"Link": "http://v4-team.com/cc/"+link})
				try:
					os.mkdir(name)
				except FileExistsError:
					pass
		for section in data["Sections"]:
			os.chdir(section["Name"])
			section["Posts"]= []
			try:
				os.mkdir("Posts")
			except FileExistsError:
				pass
			os.chdir("Posts")
			link= section["Link"]
			while True:
				section_soup= getSoup(link)
				for item in section_soup.select("a[id*= thread_title_]"):
					title= item.text.replace("/", " ")
					tmp= {"Title": title,"Link": "http://v4-team.com/cc/"+item["href"]}
					if tmp not in section["Posts"]:
						section["Posts"].append(tmp)
						try:
							os.mkdir(title)
						except FileExistsError:
							pass
				next_page= section_soup.select("a[title*='الصفحة التالية -']")
				if len(next_page)> 0:
					link= "http://v4-team.com/cc/"+next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				os.chdir(post["Title"])
				link= post["Link"]
				post["Replies"]= []
				try:
					os.mkdir("Replies")
				except FileExistsError:
					pass
				os.chdir("Replies")
				while True:
					post_soup= getSoup(link)
					i= 0
					for item in post_soup.select("table[id*= post]"):
						infos= item.find("td", {"class": "alt2"})
						content= item.find("td", {"class": "alt1"})
						try:
							itext= infos.text
						except Exception:
							itext= ""
						try:
							ctext= content.text
						except Exception:
							ctext= ""
						if not os.path.isfile('{}.json'.format(i)):
							with open('{}.json'.format(i), 'w') as json_file:
								json.dump({"Infos":itext, "Content": ctext}, json_file)
						i+= 1
					next_page= post_soup.select("a[title*='الصفحة التالية -']")
					if len(next_page)> 0:
						link= "http://v4-team.com/cc/"+next_page[0]["href"]
					else:
						break
				os.chdir("../..")
			os.chdir("../..")
	elif websites[key]== "https://www.sqorebda3.com/vb/": 
		data["Sections"]= []
		for item in soup.find_all("h3", {"class": "node-title"}):
			a_tag =item.find("a")
			link= a_tag["href"]
			name= a_tag.text
			data["Sections"].append({"Name": name ,"Link": "https://www.sqorebda3.com"+link})
		for section in data["Sections"]:
			link= section["Link"]
			section["Posts"]= []
			while True:
				section_soup= getSoup(link)
				for item in section_soup.find_all("div", {"class": "structItem-title"}):
					a_tag =item.find("a")
					link= a_tag["href"]
					name= a_tag.text
					section["Posts"].append({"Title":name,"Link": "https://www.sqorebda3.com"+link})
				next_page= section_soup.find_all("a", {"class": "pageNav-jump pageNav-jump--next"})
				if len(next_page)> 0:
					link= "https://www.sqorebda3.com"+next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				post["Replies"]= []
				link= post["Link"]
				while True:
					print(link)
					post_soup= getSoup(link)
					for item in post_soup.find_all("div", {"class": "message-inner"}):
						try:
							itext= item.find("div", {"class": "message-userDetails"}).text
						except Exception:
							itext= ""
						try:
							ctext= item.find("div", {"class": "bbWrapper"}).text
						except Exception:
							ctext= ""
						post["Replies"].append({"Infos":itext, "Content": ctext})
					next_page= section_soup.find_all("a", {"class": "pageNav-jump pageNav-jump--next"})
					if len(next_page)> 0:
						link= "https://www.sqorebda3.com"+next_page[0]["href"]
					else:
						break
	elif websites[key]== "http://www.h4kurd.com/h4kurd/":
		try:
			os.mkdir(key)
		except FileExistsError:
			pass
		os.chdir(key)
		data["Sections"]= []
		try:
			os.mkdir("Sections")
		except FileExistsError:
			pass
		os.chdir("Sections")
		for item in soup.select("tbody[id*= cat_]"):
			for tbody in item.find_all("tr"):
				try:
					a_tag =tbody.find("a")
					link= a_tag["href"]
					name= a_tag.text.replace("/", " ")
					data["Sections"].append({"Name": name ,"Link": "http://www.h4kurd.com/h4kurd/"+link})	
					try:
						os.mkdir(name)
					except FileExistsError:
						pass
				except Exception:
					pass
		for section in data["Sections"]:
			os.chdir(section["Name"])
			section["Posts"]= []
			try:
				os.mkdir("Posts")
			except FileExistsError:
				pass
			os.chdir("Posts")
			link= section["Link"]
			while True:
				section_soup= getSoup(link)
				for item in section_soup.find_all("tr", {"class": "inline_row"}):
					try:
						a_tag =item.find("span", {"class": "subject_new"}).find("a")
						link= a_tag["href"]
						name= a_tag.text.replace("/", " ")
						tmp= {"Title":name,"Link": "http://www.h4kurd.com/h4kurd/"+link}
						if tmp not in section["Posts"]:
							section["Posts"].append(tmp)
							try:
								os.mkdir(name)
							except FileExistsError:
								pass
					except Exception:
						pass
				next_page= section_soup.find_all("a", {"class": "pagination_next"})
				if len(next_page)> 0:
					link= "http://www.h4kurd.com/h4kurd/"+next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				os.chdir(post["Title"])
				link= post["Link"]
				post["Replies"]= []
				try:
					os.mkdir("Replies")
				except FileExistsError:
					pass
				os.chdir("Replies")
				while True:
					post_soup= getSoup(link)
					i= 0
					for item in post_soup.find_all("div", {"class": "post classic"}):
						try:
							itext1= item.find("div", {"class": "author_information"}).find("span", {"class": "largetext"}).text
						except Exception as e:
							itext1= ""
						try:
							itext2= item.find("div", {"class": "author_statistics"}).text
						except Exception as e:
							itext2= ""
						try:
							ctext= item.find("div", {"class": "post_body scaleimages"}).text
						except Exception as e:
							ctext= ""
						if not os.path.isfile('{}.json'.format(i)):
							with open('{}.json'.format(i), 'w') as json_file:
								json.dump({"Infos":itext1+" "+itext2, "Content": ctext}, json_file)
								# print('{}.json Created !'.format(key))
						i+= 1
					next_page= section_soup.find_all("a", {"class": "pagination_next"})
					if len(next_page)> 0:
						link= "http://www.h4kurd.com/h4kurd/"+next_page[0]["href"]
						print(link)
					else:
						break
				os.chdir("../..")
			os.chdir("../..")
	elif websites[key]== "https://www.dev-point.com/vb/":
		try:
			os.mkdir(key)
		except FileExistsError:
			pass
		os.chdir(key)
		data["Sections"]= []
		try:
			os.mkdir("Sections")
		except FileExistsError:
			pass
		os.chdir("Sections")
		for item in soup.find_all("div", {"class": "node"}):
			a_tag =item.find("h3", {"class":"node-title"}).find("a")
			link= a_tag["href"]
			name= a_tag.text.replace("/", " ")
			data["Sections"].append({"Name": name ,"Link": "https://www.dev-point.com"+link})
			try:
				os.mkdir(name)
			except FileExistsError:
				pass
		for section in data["Sections"]:
			os.chdir(section["Name"])
			section["Posts"]= []
			try:
				os.mkdir("Posts")
			except FileExistsError:
				pass

			os.chdir("Posts")
			link= section["Link"]
			while True:
				section_soup= getSoup(link)
				for item in section_soup.find_all("div", {"class": "structItem-title"}):
					try:
						a_tag =item.find("a", {"class": ""})
						link= a_tag["href"]
						name= a_tag.text.replace("/", " ")
						section["Posts"].append({"Title":name,"Link": "https://www.dev-point.com"+link})
						try:
							os.mkdir(name)
						except FileExistsError:
							pass
					except Exception:
						pass
				next_page= section_soup.find_all("a", {"class": "pageNav-jump pageNav-jump--next"})
				if len(next_page)> 0:
					link= "https://www.dev-point.com"+next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				os.chdir(post["Title"])
				post["Replies"]= []
				link= post["Link"]
				try:
					os.mkdir("Replies")
				except FileExistsError:
					pass
				os.chdir("Replies")
				while True:
					i= 0
					post_soup= getSoup(link)
					for item in post_soup.select("article[data-content*= post-]"):
						try:	
							itext1= item.find("h4", {"class": "message-name"}).text
						except Exception as e:
							itext1= ""
						try:
							itext2= item.find("div", {"class":"message-userExtras"}).text
							itext2= ' '.join(itext2.split())
						except Exception as e:
							itext2= ""
						try:
							ctext= item.find("div", {"class": "bbWrapper"}).text
						except Exception as e:
							ctext= ""
						if not os.path.isfile('{}.json'.format(i)):
							with open('{}.json'.format(i), 'w') as json_file:
								json.dump({"Infos":itext1+" "+itext2, "Content": ctext}, json_file)
						i+= 1
					next_page= section_soup.find_all("a", {"class": "pagination_next"})
					if len(next_page)> 0:
						link= "https://www.dev-point.com"+next_page[0]["href"]
						print(link)
					else:
						break
				os.chdir("../..")
			os.chdir("../..")
	elif websites[key]== "http://mr11-11mr.7olm.org/":
		data["Sections"]= []
		for item in soup.find_all("a", {"class": "forumlink"}):
			link= item["href"]
			name= item.text
			data["Sections"].append({"Name": name ,"Link": "http://mr11-11mr.7olm.org"+link})
		
		for section in data["Sections"]:
			section_soup= getSoup(section["Link"])
			section["Posts"]= []
			for item in section_soup.find_all("a", {"class": "topictitle"}):
				try:
					link= item["href"]
					name= item.text
					section["Posts"].append({"Title":name,"Link": "http://mr11-11mr.7olm.org"+link})
				except Exception as e:
					pass

			for post in section["Posts"]:
				post_soup= getSoup(post["Link"])
				post["Replies"]= []
				for item in post_soup.select("tr[id*= p]"):
					try:	
						itext1= item.find("span", {"class": "name"}).text
					except Exception as e:
						itext1= ""
					try:
						itext2= item.find("span", {"class":"postdetails poster-profile"}).text
						itext2= ' '.join(itext2.split())
					except Exception as e:
						itext2= ""
					try:
						ctext= item.find("div", {"class": "postbody"}).text
					except Exception as e:
						ctext= ""
					post["Replies"].append({"Infos":itext1+" "+itext2, "Content": ctext})
	elif websites[key]== "http://www.alkrsan.net/forum/": #this is a weird website
		data["Sections"]= []
		for item in soup.find_all("td", {"class": "alt1Active"}):
			a_tag= item.find("a")
			link= a_tag["href"]
			name= a_tag.text
			data["Sections"].append({"Name": name ,"Link": link})
		for section in data["Sections"]:
			link= section["Link"]
			section["Posts"]= []
			while True:
				section_soup= getSoup(link)
				section["Posts"]= []
				for a_tag in section_soup.select("a[id*= thread_gotonew_]"):
					try:
						link= a_tag["href"]
						name= a_tag.text
						section["Posts"].append({"Title":name,"Link": link})
					except Exception:
						pass
				next_page= section_soup.select("a[title*='الصفحة التالية -']")
				if len(next_page)> 0:
					link= next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				post["Replies"]= []
				link= post["Link"]
				while True:
					post_soup= getSoup(link)
					for item in post_soup.find_all("table", {"class": "tborder"}):
						tmp= item.select("div[id*=postmenu_]")[0]
						try:
							itext1= tmp.find("a", {"class": "bigusername"}).text
						except Exception as e:
							itext1= ""
						try:
							itext2= tmp.find("div", {"class":"smallfont"}).text
						except Exception as e:
							itext2= ""
						try:
							ctext= item.select("div[id*=post_message_]")[0].text
						except Exception as e:
							ctext= ""
						post["Replies"].append({"Infos":itext1+" "+itext2, "Content": ctext})
						print({"Infos":itext1+" "+itext2, "Content": ctext})
					next_page= section_soup.select("a[title*='الصفحة التالية -']")
					if len(next_page)> 0:
						link= next_page[0]["href"]
					else:
						break
	elif websites[key]== "http://www.effecthacking.com/search/label/Android?&max-results=10":
		pages= ["http://www.effecthacking.com/search/label/Android?updated-max=2017-04-27T23%3A21%3A00-07%3A00&max-results=10#PageNo=2","http://www.effecthacking.com/search/label/Android?updated-max=2016-08-19T07%3A37%3A00-07%3A00&max-results=10#PageNo=3","http://www.effecthacking.com/search/label/Android?updated-max=2016-05-08T07%3A38%3A00-07%3A00&max-results=10#PageNo=4","http://www.effecthacking.com/search/label/Android?updated-max=2016-01-11T05%3A57%3A00-08%3A00&max-results=10#PageNo=5","http://www.effecthacking.com/search/label/Android?updated-max=2015-09-27T08%3A21%3A00-07%3A00&max-results=10#PageNo=6","http://www.effecthacking.com/search/label/Android?updated-max=2015-04-25T02%3A08%3A00-07%3A00&max-results=10#PageNo=7","http://www.effecthacking.com/search/label/Android?updated-max=2014-10-27T05%3A06%3A00-07%3A00&max-results=10#PageNo=8"]
		i= 0
		section= []
		while True:
			for item in soup.find_all("h2", {"class": "post-title entry-title"}):
				a_tag= item.find("a")
				link= a_tag["href"]
				name= a_tag.text
				section.append({"Name": name ,"Link": link})
			if i<len(pages):
				soup= getSoup(pages[i])
				i+= 1
			else:
				break
		data["Sections"]= section
		for section in data["Sections"]:
			soup= getSoup(section["Link"])
			section["Posts"]= soup.find("div", {"dir": "ltr"}).text
		return data
	elif websites[key]=="http://hker-arb.yoo7.com/":
		data["Sections"]= []
		for item in soup.find_all("a", {"class": "forumlink"}):
			# a_tag= item.find("a")
			link= item["href"]
			name= item.text
			data["Sections"].append({"Name": name ,"Link": "http://hker-arb.yoo7.com"+link})
		for section in data["Sections"]:
			section_soup= getSoup(section["Link"])
			section["Posts"]= []
			for item in section_soup.find_all("a", {"class": "topictitle"}):
				try:
					link= item["href"]
					name= item.text
					section["Posts"].append({"Title":name,"Link": "http://hker-arb.yoo7.com"+link})
				except Exception as e:
					pass

			for post in section["Posts"]:
				post_soup= getSoup(post["Link"])
				post["Replies"]= []
				for item in post_soup.select("tr[id*= p]"):
					try:	
						itext1= item.find("span", {"class": "name"}).text
					except Exception as e:
						itext1= ""
					try:
						itext2= item.find("span", {"class":"postdetails poster-profile"}).text
						itext2= ' '.join(itext2.split())
					except Exception as e:
						itext2= ""
					try:
						ctext= item.find("div", {"class": "postbody"}).text
					except Exception as e:
						ctext= ""
					post["Replies"].append({"Infos":itext1+" "+itext2, "Content": ctext})
	elif websites[key]== "http://hackerr.hooxs.com/forum":
		data["Sections"]= []
		for item in soup.find_all("a", {"class": "forumtitle"}):
			# a_tag= item.find("a")
			link= item["href"]
			name= item.text
			data["Sections"].append({"Name": name ,"Link": "http://hackerr.hooxs.com"+link})
		for section in data["Sections"]:
			section_soup= getSoup(section["Link"])
			section["Posts"]= []
			for item in section_soup.find_all("a", {"class": "topictitle"}):
				try:
					link= item["href"]
					name= item.text
					section["Posts"].append({"Title":name,"Link": "http://hackerr.hooxs.com"+link})
				except Exception as e:
					pass

			for post in section["Posts"]:
				post_soup= getSoup(post["Link"])
				post["Replies"]= []
				for item in post_soup.select("div[class*= post--]"):
					try:	
						itext1= item.find("div", {"class": "postprofile"}).text
					except Exception as e:
						itext1= ""
					try:
						ctext= item.find("div", {"class": "postbody"}).text
					except Exception as e:
						ctext= ""
					post["Replies"].append({"Infos":itext1, "Content": ctext})
	elif websites[key]=="http://www.igli5.com/": #this is a weird website
		data["Sections"]= []
		while True:
			for item in soup.find_all("h2", {"class": "mahdidra-title"}):
				a_tag= item.find("a")
				link= a_tag["href"]
				name= a_tag.text
				data["Sections"].append({"Name": name ,"Link": link})
			next_page= soup.find_all()

		for section in data["Sections"]:
			soup= getSoup(section["Link"])
			section["Posts"]= soup.find("div", {"dir": "rtl"}).text
		return data
	elif websites[key]=="https://www.sec4ever.com/home/index.php":
		data["Sections"]= []
		for item in soup.find_all("a", {"class": "main-txt"}):
			link= item["href"]
			name= item.text
			data["Sections"].append({"Name": name ,"Link": "https://www.sec4ever.com/home/"+link})
		for section in data["Sections"]:
			link= section["Link"]
			section["Posts"]= []
			while True:
				section_soup= getSoup(link)
				for item in section_soup.select("a[id*= thread_title_]"):
					link= item["href"]
					name= item.text
					section["Posts"].append({"Title":name,"Link": "https://www.sec4ever.com/home/"+link})
				next_page= section_soup.find_all("a", {"rel": "next"})
				if len(next_page)> 0:
					link= "https://www.sec4ever.com/home/"+next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				link= post["Link"]
				post["Replies"]= []
				while True:
					post_soup= getSoup(link)
					print(link)
					try:
						posts= post_soup.find("div", {"id": "posts"})
						for item in posts.find_all("div", {"class", "page"}):
							try:
								itext1= item.find("a", {"class": "bigusername"}).text
							except Exception as e:
								itext1= ""
							try:
								itext2= [x.text for x in item.find_all("div", {"class":"assila_profile"})]
								itext2= '\n'.join(itext2)
							except Exception as e:
								print(e)
								itext2= ""
							try:
								ctext= item.select("div[id*=post_message_]")[0].text
							except Exception as e:
								print(e)
								ctext= ""
							post["Replies"].append({"Infos":itext1+" "+itext2, "Content": ctext})
					except Exception:
						pass
					next_page= post_soup.find_all("a", {"rel": "next"})
					if len(next_page)> 0:
						link= "https://www.sec4ever.com/home/"+next_page[0]["href"]
					else:
						break
	elif websites[key]=="https://forums.soqor.net/":
		try:
			os.mkdir(key)
		except FileExistsError:
			pass
		os.chdir(key)
		data["Sections"]= []
		try:
			os.mkdir("Sections")
		except FileExistsError:
			pass
		os.chdir("Sections")
		for item in soup.find_all("a", {"class": "forum-title"}):
			link= item["href"]
			name= item.text
			data["Sections"].append({"Name": name ,"Link": link})
			try:
				os.mkdir(name)
			except FileExistsError:
				pass

		for section in data["Sections"]:
			os.chdir(section["Name"])
			section["Posts"]= []
			try:
				os.mkdir("Posts")
			except FileExistsError:
				pass
			os.chdir("Posts")
			link= section["Link"]
			while True:
				section_soup= getSoup(link)
				for item in section_soup.find_all("a", {"class": "topic-title js-topic-title"}):
					try:
						link= item["href"]
						s= item.text.replace("/", "")
						name= (s[:20]+".." if len(s)>20 else s)
						tmp= {"Title":name,"Link": link}
						if tmp not in section["Posts"]:
							section["Posts"].append(tmp)
							try:
								os.mkdir(name)
							except FileExistsError:
								pass
					except Exception as e:
						pass
				next_page= section_soup.find_all("a", {"class": "arrow right-arrow"})
				if len(next_page)> 0:
					link= next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				os.chdir(post["Title"])
				print("writing in {}".format(post["Title"]))
				link= post["Link"]
				post["Replies"]= []
				try:
					os.mkdir("Replies")
				except FileExistsError:
					pass
				os.chdir("Replies")
				while True:
					post_soup= getSoup(link)
					i= 0
					posts= post_soup.find("div", {"id": "content"})
					for item in posts.select("li[class~= b-post]"):
						try:
							itext1= item.find("div", {"class": "author h-text-size--14"}).text
						except Exception as e:
							itext1= ""
						try:
							itext2= [x.text for x in item.find_all("li", {"class":"b-userinfo__additional-info"})]
							itext2= '\n'.join(itext2)
						except Exception as e:
							itext2= ""
						try:
							ctext= item.select("div[class*=b-post__content]")[0].text
						except Exception as e:
							ctext= ""
						if not os.path.isfile('{}.json'.format(i)):
							with open('{}.json'.format(i), 'w') as json_file:
								json.dump({"Infos":itext1+" "+itext2, "Content": ctext}, json_file)
						i+= 1
					next_page= post_soup.find_all("a", {"class": "arrow right-arrow"})
					if len(next_page)> 0:
						link= next_page[0]["href"]
					else:
						break
				os.chdir("../..")
			os.chdir("../..")
	elif websites[key]=="http://ul-net.blogspot.com/": #this is a weird website
		section= []
		while True:
			for item in soup.find_all("a", {"class": "ptitle"}):
				link= item["href"]
				name= item.text
				section.append({"Name": name ,"Link": link})
			
			# nav= soup.find("div", {"class": "pagenavi"})
			# for item in nav.find_all("a"):
			# 	if item.text == "التالي":
			# 		print(item)
			next_page= []
			if len(next_page)> 0:
				link= "http://ul-net.blogspot.com"+ next_page[0]["href"]
				print(link)
				soup= getSoup(link)
			else:
				break
		data["Sections"]= section
		for section in data["Sections"]:
			soup= getSoup(section["Link"])
			section["Posts"]= soup.find("div", {"dir": "rtl"}).text
		return data
	elif websites[key]=="https://www.isecur1ty.org/": 
		data["Sections"]= []
		# print(soup.find_all("li"))
		for item in soup.find_all("ul", {"class": "sub-menu"}):
			for subitem in item.find_all("li"):
				a_tag= subitem.find("a")
				link= a_tag["href"]
				name= a_tag.text
				data["Sections"].append({"Name": name ,"Link": link})

		for section in data["Sections"]:
			link= section["Link"]
			section["Posts"]= []
			while True:
				section_soup= getSoup(link)
				for item in section_soup.find_all("h3", {"class": "post-title-link"}):
					a_tag= item.find("a")
					link= a_tag["href"]
					name= a_tag.text
					section["Posts"].append({"Title":name,"Link": link})
				next_page= ""
				try:
					nav= section_soup.find("div", {"class": "navigation"})
					for a_tag in nav.find_all("a"):
						if a_tag.text=="الصفحة التالية «":
							next_page= a_tag["href"]
				except Exception as e:
					pass
				if next_page != "":
					link=next_page
					print(link)
				else:
					break
			for post in section["Posts"]:
				post_soup= getSoup(post["Link"])
				post["Replies"]= []
				post_soup.find("section", {"class": "article-auther"})
				post["Replies"].append({"Infos":post_soup.text, "Content": post_soup.find_all("div", {"class": "the-content"})})
	elif websites[key]=="http://cjlab.memri.org/category/latest-reports/":
		data["Sections"]= []
		while True:
			for item in soup.select("li[class*= post-]"):
				a_tag= item.find("a")
				link= a_tag["href"]
				name= a_tag.text
				data["Sections"].append({"Name": name ,"Link": link})
			next_page= soup.find_all("a", {"class": "next page-numbers"})
			if len(next_page)>0:
				link= next_page[0]["href"]
				soup= getSoup(link)
			else:
				break
		for section in data["Sections"]:
			soup= getSoup(section["Link"])
			section["Posts"]= soup.find("div", {"class": "entry"}).text
	elif websites[key]=="http://www.aljyyosh.com/vb/":
		try:
			os.mkdir(key)
		except FileExistsError:
			pass
		os.chdir(key)
		data["Sections"]= []
		try:
			os.mkdir("Sections")
		except FileExistsError:
			pass
		os.chdir("Sections")
		for item in soup.find_all("h2", {"class": "forumtitle"}):
			a_tag =item.find("a")
			link= "http://www.aljyyosh.com/vb/" + a_tag["href"]
			name= a_tag.text.replace("/", " ")
			data["Sections"].append({"Name": name ,"Link": link})
			try:
				os.mkdir(name)
			except FileExistsError:
				pass
		for section in data["Sections"]:
			os.chdir(section["Name"])
			section["Posts"]= []
			try:
				os.mkdir("Posts")
			except FileExistsError:
				pass

			os.chdir("Posts")
			link= section["Link"]
			while True:
				section_soup= getSoup(link)
				section["Posts"]= []
				for item in section_soup.select("a[id*= thread_title_]"):
					link= "http://www.aljyyosh.com/vb/" + item["href"]
					name= item.text.replace("/", " ")
					tmp= {"Title":name,"Link": link}
					if tmp not in section["Posts"]:
						section["Posts"].append(tmp)
						try:
							os.mkdir(name)
						except FileExistsError:
							pass
				next_page= section_soup.select("a[title*='الصفحة التالية -']")
				if len(next_page)> 0:
					link= "http://www.aljyyosh.com/vb/" + next_page[0]["href"]
				else:
					break
			for post in section["Posts"]:
				os.chdir(post["Title"])
				link= post["Link"]
				post["Replies"]= []
				try:
					os.mkdir("Replies")
				except FileExistsError:
					pass
				os.chdir("Replies")
				while True:
					post_soup= getSoup(link)
					i= 0
					for item in post_soup.select("li[id*=post_]"):
						info= item.find("div", {"class": "userinfo"})
						try:
							itext1= item.find("div", {"class": "username_container"}).text
						except Exception as e:
							itext1= ""
						try:
							itext2= item.find("dl", {"class":"userinfo_extra"}).text
							itext2= ' '.join(itext2.split())
						except Exception as e:
							itext2= ""
						try:
							ctext= item.select("div[id*= post_message_]")[0].text
						except Exception as e:
							ctext= ""
						if not os.path.isfile('{}.json'.format(i)):
							with open('{}.json'.format(i), 'w') as json_file:
								json.dump({"Infos":itext1+" "+itext2, "Content": ctext}, json_file)
								# print('{}.json Created !'.format(i))
						i+= 1
					next_page= section_soup.select("a[title*='الصفحة التالية -']")
					if len(next_page)> 0:
						link= "http://www.aljyyosh.com/vb/" + next_page[0]["href"]
					else:
						print("Wrote {} !".format(post["Title"]))
						break
				os.chdir("../..")
			os.chdir("../..")

	return data

def main():
	websites= {"x6x":"http://www.x6x.net/vb/", "v4-team":"http://v4-team.com/cc/index.php",
	"sqebd":"https://www.sqorebda3.com/vb/", "h4kurd": "http://www.h4kurd.com/h4kurd/",
	"dev-point": "https://www.dev-point.com/vb/", "mr11":"http://mr11-11mr.7olm.org/",
	"alkrsan": "http://www.alkrsan.net/forum/", "effecthacking":"http://www.effecthacking.com/search/label/Android?&max-results=10",
	"hker": "http://hker-arb.yoo7.com/", "hackerr":"http://hackerr.hooxs.com/forum",
	"igli5":"http://www.igli5.com/", "sec4ever": "https://www.sec4ever.com/home/index.php",
	"soqor":"https://forums.soqor.net/", "ul-net": "http://ul-net.blogspot.com/",
	"isecur1ty":"https://www.isecur1ty.org/", "cjlab": "http://cjlab.memri.org/category/latest-reports/",
	"aljyyosh":"http://www.aljyyosh.com/vb/"}
	path= os.getcwd()
	# webkeys= ["x6x", "v4-team", "sqebd", "h4kurd", "dev-point", "mr11", 
	# "alkrsan", "effecthacking", "hker", "hackerr", "igli5", "sec4ever",
	# "soqor", "ul-net", "isecur1ty", "cjlab", aljyyosh]
	webkeys= ["dev-point"]
	# data= {"Websites": {}}
	for key in webkeys:
	# 	try:
		print("Scraping from {}".format(websites[key]))
		# data["Websites"][key]=({"Link": websites[key] ,"Content" :scrap(websites[key])})
		data= scrap(key, websites)
		os.chdir(path)
		with open('{}.json'.format(key), 'w') as json_file:
			json.dump(data, json_file)
			print('{}.json Created !'.format(key))
		# except Exception as e:
		# 	print('Could not create {}.json !\nExcpetion Raised:{}'.format(key, e))

if __name__ == '__main__':
	main()

'''

json

Website
	Sections
		Name
		Link
		Posts
			Title
			Link
			Replies
				Infos
				Content

'''
