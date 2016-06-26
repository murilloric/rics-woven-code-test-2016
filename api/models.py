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

def getDateList():
	numdays = 7
	base = datetime.datetime.today()
	date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
	return [str(x.strftime('%m/%d/%Y')) for x in date_list]


def queryWebsite(website, date):
	#website must be in DataStore if True check if date args are equal to 'recent' or 'week' if not False
	is_website = WebsiteModel.query(WebsiteModel.name == website).get()
	if is_website == None and website != 'all':
		return False
	else:
		if date != 'recent' and date != 'week':
			return False
		else:
			#query for data
			data = {}
			if date == 'recent' and website == 'all':
				#query for past 7 days
				# date.now() + minus past 7 days
				# fiter by date range
				#data structure to return
				# [{'uproxx.com':[{'6/20/2016':26}...]},
				#  {'brobile.com':[{'6/20/2016':21}...]}
				# ]

				seven_days = ['06/06/2016', '06/07/2016', '06/08/2016', '06/09/2016', '06/10/2016']
				#seven_days = getDateList()
				websites = {'uproxx.com':0, 'brobible.com':0}
				for d in seven_days:
					day = WebDayModel.query(WebDayModel.date == d).fetch()
					for w in day:
						websites[w.name] += w.page_views
				data = websites
			elif date == 'week':
				#query by website return days of the week
				if is_website != None:
					data = {website:is_website.day_of_week}
				else:
					return False
			else:
				return False
			return data
		return True


