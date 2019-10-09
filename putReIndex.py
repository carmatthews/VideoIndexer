#Allows you to re-index a file that already exists on Video Indexer - you could change settings

# Video Re-Index API Definition: https://api-portal.videoindexer.ai/docs/services/operations/operations/Re-Index-Video?
# Parameter Definition: https://docs.microsoft.com/en-us/azure/media-services/video-indexer/upload-index-videos

import requests

##### CONFIGURE YOUR ACCOUNTS & ACCESS HERE 

# The video_id is assigned when the file is uploaded.  If you didn't catch it, use getListVideos.py to see all of your files.
video_indexer_video_id = 'REPLACE'  
file_name = 'REPLACE'  #informational only, helpful for finding your files.

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

print('Start Re-indexing ',file_name)

# Setup to re-index a file already uploaded to Video Indexer
reindex_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos/{}/ReIndex'.format(video_indexer_region,video_indexer_account_id,video_indexer_video_id)
reindex_header = { 'x-ms-client-request-id': '', }
reindex_params = {
    'accessToken':auth_token,
    # Request parameters
    'indexingPreset': 'AudioOnly',
    'streamingPreset': 'NoStreaming',  #the video/audio won't be encoded
    #'callbackUrl': '{string}',
    'sourceLanguage': 'multi',
    #'sendSuccessEmail': 'False',
    #'linguisticModelId': '{string}',
    #'personModelId': '{string}',
    #'animationModelId': '{string}',
    #'priority': '{string}',
    #'brandsCategories': '{string}',
    }

try:
    response = requests.put(reindex_uri, headers=reindex_header, params=reindex_params)

    if response.status_code == 204: #Status of 204 means the index has started.
        print('Re-indexing Started...')  
    elif response.status_code == 400:
        print('Re-indexing already in progress...')   
    else:
        response_body = response.json()
        print("Error: {} {}".format(response.status_code, response_body))

except requests.exceptions.RequestException as e:
    # A serious problem happened, like an SSLError or InvalidURL
    print("Error: {}".format(e))

# Check Status of Job
# You can sleep and loop hitting the Get Video Index API to view the status as it processes
