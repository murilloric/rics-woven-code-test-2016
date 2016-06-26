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

                'LIMIT 5;')
        }

        query_response = query_request.query(
            projectId=project_id,
            body=query_data).execute()

        for row in query_response['rows']:
            rowVal = []
            for cell in row['f']:
                cell = json.loads(cell['v'])
                website =  cell['url'].split("/")[2]
                logging.info("website: " + website)
                day = time.strftime("%A", time.localtime(int(cell['ctime'])))
                date = time.strftime("%x", time.localtime(int(cell['ctime'])))
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
        populateRecords()
        #deferred.defer(populateRecords)

        
        data = "hello"
        self.response.write(data)



#ERROR HANDLERS

def handle_404(request, response, exception):
    response.write('Oops! I could swear this page was here! <a href="/">go back</a>')
    response.set_status(404)

def handle_500(request, response, exception):
    response.write('A server error occurred!')
    response.set_status(500)


app = webapp2.WSGIApplication([
    ('/', HomeHandler)
], debug=True)


app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500