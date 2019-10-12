# will return code for embedding the insights widget into your own application.
# https://api-portal.videoindexer.ai/docs/services/operations/operations/Get-Video-Insights-Widget?

import requests

##### CONFIGURE YOUR ACCOUNTS & ACCESS HERE 

# The video_id is assigned when the file is uploaded.  If you didn't catch it, use getListVideos.py to see all of your files.
video_indexer_video_id = 'REPLACE'  

# Configure access to Video Indexer
video_indexer_account_id = 'REPLACE'   # See account settings in Video Indexer Portal: https://www.videoindexer.ai/settings/account
video_indexer_region = 'REPLACE'       # At the top of the Video Indexer Portal (https://www.videoindexer.ai), you should see the region (may be trial, WestUS etc.)
video_indexer_key = 'REPLACE'          # See Profile in Video Indexer Developer Portal: https://api-portal.videoindexer.ai/developer

#configure the player size within an iframe.  Leave as is to begin with.
player_width = 580
player_height = 780

#######  END CONFIGURATION SECTION

# Get authorization token for Video Indexer API - to get the widget requires an access token for the individual video
auth_uri = 'https://api.videoindexer.ai/auth/{}/Accounts/{}/Videos/{}/AccessToken'.format(video_indexer_region,video_indexer_account_id, video_indexer_video_id)
auth_params = {'allowEdit':'true'}  #allows editing the transcripts/insights
auth_header = {'Ocp-Apim-Subscription-Key': video_indexer_key}
auth_token = requests.get(auth_uri,headers=auth_header,params=auth_params).text.replace('"','')

print('Getting widget embed code...')

# Get html snippet with widget script
getwidget_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos/{}/InsightsWidget'.format(video_indexer_region, video_indexer_account_id, video_indexer_video_id)

getwidget_headers = { 'x-ms-client-request-id': '', }
getwidget_params = {
    'accessToken':auth_token,
    #'widgetType': '{array}',  #Options: people, keywords, annotations, brands, sentiments, transcript, search
    'allowEdit': 'True',  #allowed to edit the timeline in the widget (note access token must also be set to 'allowEdit')
    }

try:
    response = requests.get(getwidget_uri, headers=getwidget_headers, params=getwidget_params)
    response_body = response.text  #The text returned is html that I believe worked in a previous version of Video Indexer
    widget_url = response.url #This will return the URI you can embed via an iframe in an html page.  Note the token will work for 1 hour.
   
    # Consider any status other than 2xx an error
    if not response.status_code // 100 == 2:
        print("Error: {} {}".format(response.status_code, response_body))
    else:
        #example code for using an iframe with embedded player
        widget_embed = '<html><iframe width='"'{}'"' height='"'{}'"' src='"'{}'"' frameborder='"'0'"' allowfullscreen></iframe></html>'.format(player_width, player_height, widget_url)
        print(widget_embed)

except requests.exceptions.RequestException as e:
    # A serious problem happened, like an SSLError or InvalidURL
    print("Error: {}".format(e))

