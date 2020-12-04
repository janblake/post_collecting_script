import requests
from bs4 import BeautifulSoup as soup
import re
import math


def getLocation(c,url):



	req=c.get(url)
	
	page_html=req.content

	page_soup=soup(page_html,"html.parser")

	profile_list=page_soup.findAll('li',{'class':'grid--cell ow-break-word'})

	loc_exists=profile_list[0].findAll('svg',{'class':'svg-icon iconLocation'})
	if loc_exists:
		location=profile_list[0].div.text.strip()
		locations.append(location)
	else:
		locations.append("No Location")
	



url=[
	"https://stackoverflow.com/search?q=coronavirus+created%3A2020-10-28..2020-11-30&s=6165b23c-e20d-47bc-a765-4abc3fe83400&page=",
	"https://stackoverflow.com/search?q=corona-virus+created%3A2020-10-28..2020-11-30&s=12558bda-75f7-4c15-91d0-76df4d403655&page=",
	"https://stackoverflow.com/search?q=covid*+created%3A2020-10-28..2020-11-30&page=",
	"https://stackoverflow.com/search?q=sars-cov+created%3A2020-10-28..2020-11-30&page=",
	"https://stackoverflow.com/search?q=2019-ncov+created%3A2020-10-28..2020-11-30&page="
	]

headers={
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
	'Referer':'https://stackoverflow.com/'
	}



question_id=[]
question_title=[]
question_body=[]
timestamp=[]
views=[]
votes=[]
tags=[]
owner_id=[]
locations=[]



with requests.Session() as c:
	login_url='https://stackoverflow.com/users/login'
	USERNAME='testuser'
	PASSWORD='paok1998'
	c.get(login_url)
	login_data=dict(username=USERNAME,password=PASSWORD,next='/')
	c.post(login_url,data=login_data,headers=headers)
	for j in range(len(url)):
		page=c.get(url[j])
		print()
		print(url[j])
		print()
		page_soup=soup(page.content,'html.parser')
		numberOfResults_div=page_soup.find('div',{'class':'grid--cell fl1 fs-body3 mr12'})
		numberOfResults=float(re.sub("[^0-9]", "",numberOfResults_div.text))
		numberOfPages=math.ceil(numberOfResults/15)
		for i in range(numberOfPages):
			paginated_page=c.get(url[j]+str(i+1))
			paginated_page_soup=soup(paginated_page.content,'html.parser')
			results=paginated_page_soup.findAll('div',{'class':'question-summary search-result'})
			for result in results:
				if result['id'].startswith('question-summary-'):
					question=result.find('a',{'class':'question-hyperlink'})

					q_id='https://stackoverflow.com'+question['href']
					question_id.append(q_id)#id

					question_page=c.get(q_id)
					question_soup=soup(question_page.content,'html.parser')

					title_div=question_soup.find('div',{'id':'question-header'})
					question_title.append(title_div.h1.a.text)#title
					print(title_div.h1.a.text)

					time_div=question_soup.find('div',{'class':'grid--cell ws-nowrap mr16 mb8'})
					timestamp.append(time_div['title'])#timestamp

					views_div=question_soup.find('div',{'class':'grid--cell ws-nowrap mb8'})
					views.append(re.sub("[^0-9]", "",views_div.text))#views

					votes_div=question_soup.find('div',{'class':'js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center'})
					votes.append(votes_div.text)#votes

					string=""
					tags_a=result.findAll('a',{'class':'post-tag'})
					for a in tags_a:
						string=string+a.text+" "
					tags.append(string)#tags

					post_div=question_soup.find('div',{'class':'post-layout'})
					body_div=post_div.find('div',{'class':'s-prose js-post-body'})
					question_body.append(body_div.text)#body

					user_div=question_soup.find('div',{'class':'user-details'})
					if user_div.a is not None:
						u_id='https://stackoverflow.com'+user_div.a['href']
						owner_id.append(u_id)#owner
						print(u_id)
						print()
						getLocation(c,u_id)#location
					else:
						owner_id.append('No Owner ID')
						locations.append('No Location')
				


for i in range(len(votes)):
	print(question_id[i])
	print(question_title[i])
	print(question_body[i])
	print(votes[i])
	print(views[i])
	print(tags[i])
	print(owner_id[i])
	print(locations[i])
	print(timestamp[i])
	print("----------------------------------------------------")


	

