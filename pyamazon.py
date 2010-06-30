#!/usr/bin/env python

# Jon Vlachoyiannis
# jon@socialcaddy.com

# First version here: http://cloudcarpenters.com/blog/amazon_products_api_request_signing/
# 29/06/2010

import base64,hashlib,hmac,time
from urllib import urlencode, urlopen

# check here for your keys https://aws-portal.amazon.com/gp/aws/developer
AWS_ACCESS_KEY_ID = "ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "SECRET_KEY"

base_url = "http://ecs.amazonaws.com/onca/xml"

# for more options check here http://docs.amazonwebservices.com/AWSECommerceService/latest/DG/index.html?SummaryofA2SOperations.html
url_params = {'AWSAccessKeyId':AWS_ACCESS_KEY_ID, 'Keywords':"harry",
			  'Operation':"ItemSearch", 'SearchIndex': 'Books',
			  'Service':"AWSECommerceService",
			  'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()), 
			  'Version':"2009-03-31",
			  'Availability':"Available",'Condition':"All",'ItemPage':"1",'ResponseGroup':"Images,ItemAttributes,EditorialReview",
}

# Sort the URL parameters by key
keys = url_params.keys()
keys.sort()

# Get the values in the same order of the sorted keys
values = map(url_params.get, keys)
 
# Reconstruct the URL paramters and encode them
url_string = urlencode(zip(keys,values))
url_string = url_string.replace('+',"%20") 
url_string = url_string.replace(':',"%3A") 

#Construct the string to sign
string_to_sign = """GET
ecs.amazonaws.com
/onca/xml
%s""" % url_string

# Sign the request
signature = hmac.new(
	key=AWS_SECRET_ACCESS_KEY,
	msg=string_to_sign,
	digestmod=hashlib.sha256).digest()
 
# Base64 encode the signature
signature = base64.encodestring(signature)

# Make the signature URL safe
#signature = urlencode({'Signature': signature})

signature = signature.replace('+','%2B')
signature = signature.replace('=',"%3D")

params = signature
url_string += "&Signature=" + params

print urlopen("%s?%s" % (base_url,url_string)).read()

