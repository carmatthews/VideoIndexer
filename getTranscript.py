# Parses the results from Get Video Index to extract the Transcript items.
# Use the Get Video Index API: https://api-portal.videoindexer.ai/docs/services/Operations/operations/Get-Video-Index?
# https://docs.microsoft.com/en-us/azure/media-services/video-indexer/video-indexer-output-json-v2

import requests


##### CONFIGURE YOUR ACCOUNTS & ACCESS HERE 

# The video_id is assigned when the file is uploaded.  If you didn't catch it, use getListVideos.py to see all of your files.
video_indexer_video_id = 'REPLACE'  

# Configure access to Video Indexer
video_indexer_account_id = 'REPLACE'   # See account settings in Video Indexer Portal: https://www.videoindexer.ai/settings/account
video_indexer_region = 'REPLACE'       # At the top of the Video Indexer Portal (https://www.videoindexer.ai), you should see the region (may be trial, WestUS etc.)
video_indexer_key = 'REPLACE'          # See Profile in Video Indexer Developer Portal: https://api-portal.videoindexer.ai/developer

#######  END CONFIGURATION SECTION

# Get authorization token for Video Indexer API
auth_uri = 'https://api.videoindexer.ai/auth/{}/Accounts/{}/AccessToken'.format(video_indexer_region,video_indexer_account_id)
auth_params = {'allowEdit':'true'}
auth_header = {'Ocp-Apim-Subscription-Key': video_indexer_key}
auth_token = requests.get(auth_uri,headers=auth_header,params=auth_params).text.replace('"','')

# Get indexed results for Video/Audio file
check_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos/{}/Index'.format(video_indexer_region,video_indexer_account_id,video_indexer_video_id)

check_header = { 'x-ms-client-request-id': '', }
check_params = {
    'accessToken':auth_token,
    #'language': '{string}',  #Note this could be used to translate a transcript into another language set to 'en-US' or 'es-ES'
    #'reTranslate': 'False',
    #'includeStreamingUrls': 'True'
    }

try:
    response = requests.get(check_uri, headers=check_header, params=check_params)
    response_body = response.json()
   
    # Consider any status other than 2xx an error
    if not response.status_code // 100 == 2:
        print("Error: {} {}".format(response.status_code, response_body))
    else:
        if response_body.get('state') == 'Processed':  #The video has been indexed and transcript should be available
            for video in response_body["videos"]:
                #print("Video id: {} insights are: {}".format(video.get('id'), video.get('insights')))
                for transcript in video["insights"]["transcript"]:
                    #print(transcript)  #use this to view all transcript data available
                    print("Line {}: {}-{} Speaker#{} in Language {} - {}".format(transcript.get('id'),transcript.get('instances')[0]["start"], transcript.get('instances')[0]["end"], transcript.get('speakerId'), transcript.get('language'), transcript.get('text')))         
        else:
            print('Video Id: {} has state: {}.'.format(response_body.get('id'), response_body.get('state'))) 

except requests.exceptions.RequestException as e:
    # A serious problem happened, like an SSLError or InvalidURL
    print("Error: {}".format(e))

