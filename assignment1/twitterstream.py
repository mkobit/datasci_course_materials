import argparse
import oauth2 as oauth
import urllib2 as urllib

# See assignment1.html instructions or README for how to get credentials

_debug = 0

'''
Construct, sign, and open a twitter request.
'''
def twitterreq(url, method, parameters, **kwargs):
  oauth_token = oauth.Token(key=kwargs.get('access_token_key'),
    secret=kwargs.get('access_token_secret'))
  oauth_consumer = oauth.Consumer(key=kwargs.get('api_key'),
    secret=kwargs.get('api_secret'))
  signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
  http_handler = urllib.HTTPHandler(debuglevel=_debug)
  https_handler = urllib.HTTPSHandler(debuglevel=_debug)
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
    token=oauth_token,
    http_method=method,
    http_url=url,
    parameters=parameters)
  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
  headers = req.to_header()

  if method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples(apiKey, apiSecret, accessTokenKey, accessTokenSecret):
  url = "https://api.twitter.com/1.1/search/tweets.json"
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = {}
  response = twitterreq(url=url, method="GET", parameters=parameters,
    access_token_key=accessTokenKey,
    access_token_secret=accessTokenSecret,
    api_key=apiKey,
    api_secret=apiSecret)
  for line in response:
    print(line.strip())

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Fetch data from Twitter')
  parser.add_argument('--apiKey',
    help="Twitter API key",
    required=True,
    type=str)
  parser.add_argument('--apiSecret',
    help="Twitter API secret",
    required=True,
    type=str)
  parser.add_argument('--accessTokenKey',
    help="Twitter User Access Token Key",
    required=True,
    type=str)
  parser.add_argument('--accessTokenSecret',
    help="Twitter User Access token secret",
    required=True,
    type=str)
  arguments = parser.parse_args()
  fetchsamples(arguments.apiKey,
    arguments.apiSecret,
    arguments.accessTokenKey,
    arguments.accessTokenSecret)
