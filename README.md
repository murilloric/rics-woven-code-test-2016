# RIC'S WOVEN CODE TEST 6-25-2016



#About this API 

This API will give you historical data on website visits for the 7 most recent days.  For a given website, you can get the total page views for each day of the week.( Mon. - Sun.)

#How to use API

There is one end-point with a GET method that takes two params. The return data will be in JSON format.  


------
HOST: https://rics-woven-code-test-2016.appspot.com/
PATH: /analytics/website
FULL_URL: https://rics-woven-code-test-2016.appspot.com/analytics/website?website={{PARAM}}&date={{PARAM}}
METHOD: GET
PARAMS REQUIRED KEYS:  website and date 
HEADERS: N/A (PUBLIC API)
BODY: N/A
RESPONSE: {"status":200, "message":"message", 'data":{}}
------



OPTION 1:
total page views on each website for the past 7 days.  Website with a value of all will look for all websites recorded.  Date 
recent will look at todays date and count back seven days to get most recent page view count. 

params
website: all 
date: recent

curl call:  

```curl -X GET -H "website: all" -H "date: recent" "https://rics-woven-code-test-2016.appspot.com/analytics/website?website=all&date=recent" ```


OPTION 2:
for a chosen website.  Total page views for each day of the week (Mon. - Sun). For the website key please type brobible.com or uproxx.com. For Date please type week.  The value are strict.

params
website: 'brobible.com' or 'uproxx.com'
date: week


```curl -X GET -H "website: all" -H "date: recent" "https://rics-woven-code-test-2016.appspot.com/analytics/website?website=uproxx.com&date=week" ```














