import logging
import time
import datetime
from google.appengine.ext import ndb


class WebsiteModel(ndb.Model):
	name = ndb.StringProperty()
	total_page_views = ndb.IntegerProperty()
	day_of_week = ndb.JsonProperty()


class PageModel(ndb.Model):
	name = ndb.StringProperty()
	total_page_views = ndb.IntegerProperty()

class UserModel(ndb.Model):
	name = ndb.StringProperty()
	visits = ndb.IntegerProperty()


class WebDayModel(ndb.Model):
	date = ndb.StringProperty()
	name = ndb.StringProperty()
	page_views = ndb.IntegerProperty()

class PageDayModel(ndb.Model):
	date = ndb.DateTimeProperty()
	page = ndb.StringProperty()
	page_views = ndb.IntegerProperty()

class PageReferModel(ndb.Model):
	page = ndb.StringProperty()
	refer = ndb.StringProperty()
	total_refer = ndb.IntegerProperty()


class UserReadingModel(ndb.Model):
	name = ndb.StringProperty()
	page = ndb.StringProperty()


def insertWebRecords(website, day):
	day = day.lower()
	time.sleep(1)
	web_model = WebsiteModel.query(WebsiteModel.name == website).get()
	logging.info(web_model)
	if web_model == None:
		day_of_week = {'monday':0, 'tuesday':0, 'wednesday':0, 'thursday':0, 'friday':0, 'saturday':0, 'sunday':0}
		day_of_week[day] = 1
		WebsiteModel(name=website, total_page_views=1, day_of_week=day_of_week).put()
	else:
		web_model.day_of_week[day] = web_model.day_of_week[day] + 1
		web_model.total_page_views = web_model.total_page_views + 1
		web_model.put()

def insertWebDayRecords(website, date):
	time.sleep(1)
	web_day_model = WebDayModel.query(ndb.AND(WebDayModel.date == date, WebDayModel.name == website)).get()
	logging.info(web_day_model)
	if web_day_model == None:
		WebDayModel(name=website, date=date, page_views=1).put()
	else:
		web_day_model.page_views = web_day_model.page_views + 1
		web_day_model.put()

def queryWebsite(website, date):
	#website must be in DataStore if True check if date args are equal to 'recent' or 'week' if not False
	if website == 'all':
		is_website = True
	else:
		is_website = WebsiteModel.query(WebsiteModel.name == website).get()

	logging.info(is_website)
	if is_website == None:
		return False
	else:
		if date != 'recent' and date != 'week':
			return False
		else:
			#query for data
			if date == 'recent':
				#query for past 7 days
				#query

				data = {}
			elif date == 'week':
				#query by website return days of the week
				data = {}
			return data
		return True


