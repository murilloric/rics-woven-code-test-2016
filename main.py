import logging
import urllib
import webapp2
import json
import os
import cloudstorage as gcs
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import time
import datetime

from google.appengine.api import app_identity
from api import hooks

from google.appengine.ext import deferred

from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

from api import models


def populateRecords():
    try:
        project_id = 'rics-woven-code-test-2016'
        credentials = GoogleCredentials.get_application_default()

        bigquery_service = build('bigquery', 'v2', credentials=credentials)
        query_request = bigquery_service.jobs()
        query_data = {
            'query': (
                'SELECT *, '
                'FROM [beacon_sample_Data.json_block],'

                'LIMIT 5000;')
        }

        query_response = query_request.query(
            projectId=project_id,
            body=query_data).execute()

        for row in query_response['rows']:
            rowVal = []
            for cell in row['f']:
                cell = json.loads(cell['v'])
                website =  cell['url'].split("/")[2]
                day = time.strftime("%A", time.localtime(int(cell['ctime'])))
                currentutc = int(cell['currentutc']) / 1000
                date = datetime.datetime.utcfromtimestamp(currentutc).strftime('%m/%d/%Y') 
                #models.insertWebRecords(website, day)
                models.insertWebDayRecords(website, date)

    except Exception as e:
        logging.error(e)





class BaseHandler(webapp2.RequestHandler):
    def server_resp(self, status, message, data):
        message = json.dumps({'status':status, 'message':message, 'data':data})
        self.response.write(message)


class HomeHandler(BaseHandler):
    def get(self):
        populate_records = self.request.get('populate')
        logging.info(populate_records)
        if populate_records == 'true':
            self.response.write('populating records...')
            #deferred.defer(populateRecords)
            self.redirect('/')
        else:  
            html = """
                <h1>Hello welcome to Ric's Woven Code Test 2016</h1>
                <a target="_blank" href="https://github.com/murilloric/rics-woven-code-test-2016">View code on Github</a>

                <h2>About this API</h2>

<p>This API will give you historical data on website visits for the 7 most recent days.  For a given website, you can get the total page views for each day of the week.( Mon. - Sun.)</p>

<h2>#How to use API</h2>

<p>There is one end-point with a GET method that takes two params. The return data will be in JSON format.</p> 


------
<h5>HOST: https://rics-woven-code-test-2016.appspot.com/</h5>
<h5>PATH: /analytics/website</h5>
<h5>FULL_URL: https://rics-woven-code-test-2016.appspot.com/analytics/website?website={{PARAM}}&date={{PARAM}}</h5>
<h5>METHOD: GET</h5>
<h5>PARAMS REQUIRED KEYS:  website and date </h5>
<h5>HEADERS: N/A (PUBLIC API)</h5>
<h5>BODY: N/A</h5>
<h5>RESPONSE: {"status":200, "message":"message", 'data":{}}</h5>
------



<h5>OPTION 1:</h5>
<p>total page views on each website for the past 7 days.  Website with a value of all will look for all websites recorded.  Date 
recent will look at todays date and count back seven days to get most recent page view count. </p>
----
<h5>params</h5>
----
<p>website: all </p>
<p>date: recent</p>
-----
<h5>curl call: </h5> 
-----
<p>curl -X GET -H "website: all" -H "date: recent" "https://rics-woven-code-test-2016.appspot.com/analytics/website?website=all&date=recent"</p>


<h5>OPTION 2:</h5>
for a chosen website.  Total page views for each day of the week (Mon. - Sun). For the website key please type brobible.com or uproxx.com. For Date please type week.  The value are strict.
----
<h5>params</h5>
----
<p>website: 'brobible.com' or 'uproxx.com'</p>
<p>date: week</p>
-----
<h5> curl call:</h5>
-----
<p>curl -X GET -H "website: all" -H "date: recent" "https://rics-woven-code-test-2016.appspot.com/analytics/website?website=uproxx.com&date=week"</p>


            """
            self.response.write(html)


class AnalyticsWebsite(BaseHandler):
    def get(self):
        #website : all = find all website based on date arg, {name} = find exact website by name and by date   
        #date : recent = past 7 days , week
        try:
            website = self.request.get('website')
            date = self.request.get('date')
            data = models.queryWebsite(website, date)
            if data == False:
                raise Exception
            self.response.write(json.dumps({'status':200, 'message': 'data results', 'data':data}))
        except Exception as e:
            logging.info('ERROR')
            logging.info(e)
            self.response.set_status(400)
            self.response.write(json.dumps({'status':400, 'message':'Bad Request, please read documentation', 'data':{}}))




#ERROR HANDLERS

def handle_404(request, response, exception):
    response.write('Oops! I could swear this page was here! <a href="/">go back</a>')
    response.set_status(404)

def handle_500(request, response, exception):
    response.write('A server error occurred!')
    response.set_status(500)


app = webapp2.WSGIApplication([
    ('/analytics/website', AnalyticsWebsite),
    ('/', HomeHandler)
], debug=True)


app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500