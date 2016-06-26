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
        logging.info('HELLOOO')
        project_id = 'rics-woven-code-test-2016'
        credentials = GoogleCredentials.get_application_default()

        bigquery_service = build('bigquery', 'v2', credentials=credentials)
        query_request = bigquery_service.jobs()
        query_data = {
            'query': (
                'SELECT *, '
                'FROM [beacon_sample_Data.json_block],'

                'LIMIT 100;')
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
                logging.info(date)
                #models.insertWebRecords(website, day)
                #models.insertWebDayRecords(website, date)

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
            data = "<h1>Hello welcome to Ric's Woven Code Test 2016</h1>"
            self.response.write(data)


class AnalyticsWebsite(BaseHandler):
    def get(self):
        #website : all = find all website based on date arg, {name} = find exact website by name and by date   
        #date : recent = past 7 days , week
        try:
            website = self.request.get('website')
            date = self.request.get('date')
            data = models.queryWebsite(website, date)
            logging.info('website: ' + website + ' date: ' + date)
            logging.info(data)
            if data == False:
                raise Exception
            self.response.write(data)
        except Exception as e:
            logging.error(e)
            self.response.set_status(400)
            self.response.write(e)




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