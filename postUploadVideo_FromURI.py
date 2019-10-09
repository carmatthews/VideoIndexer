# Uploads a file to Video Indexer using API, which initiates the indexing process, which will usually take several minutes (to many minutes depending on size of video and available resources)
# This example sends the video file as a byte array in the request body.  NOTE: the recommendation is to use a URI (see postUploadVideo_FromURI.py)

# Video Upload API Definition: https://api-portal.videoindexer.ai/docs/services/Operations/operations/Upload-Video?
# Parameter Definition: https://docs.microsoft.com/en-us/azure/media-services/video-indexer/upload-index-videos

import requests

##### CONFIGURE YOUR ACCOUNTS & ACCESS HERE 

# Used Blob Account/SAS Token to Access the file to upload (video_url) and provided a file_name just for identifying/naming on Video Indexer.
video_uri = 'REPLACE WITH YOUR URI'
file_name = 'REPLACE WITH YOUR FILENAME'

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

print('Authorization Token Obtained.')

# Upload file to Video Indexer API  (video or audio)
upload_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos'.format(video_indexer_region,video_indexer_account_id)
upload_params = {
    'name':file_name,
    'accessToken':auth_token,
    'streamingPreset':'NoStreaming', #we will not encode the file, change to Default to encode first
    'indexingPreset': 'AudioOnly', #leave as Default if you want both audio and video.
    'fileName':file_name, #identifies the file on Video Indexer
    'privacy': 'Private',
    #'priority': '{string}',
    'description': 'Sample audio file with multiple languages',
    #'partition': '{string}',
    #'externalId': '{string}',
    #'externalUrl': '{string}',
    #'callbackUrl': '{string}',
    #'metadata': '{string}',
    'language': 'multi',  #multi will automatically detect multiple languages in file
    'videoUrl': video_uri,
    #'linguisticModelId': '{string}',
    #'personModelId': '{string}',
    #'animationModelId': '{string}',
    #'sendSuccessEmail': 'False',
    #'assetId': '{string}',
    #'brandsCategories': '{string}',
    }

print('Start uploading file: ',file_name)

try:
    response = requests.post(upload_uri,params=upload_params)
    response_body = response.json()
   
    # Consider any status other than 2xx an error
    if not response.status_code // 100 == 2:
        print("Error: {} {}".format(response.status_code, response_body))
    else:
        print('File upload Completed with status_code: {}'.format(response.status_code))
        print('Assigned Video Id: {} is in state: {}.'.format(response_body.get('id'), response_body.get('state')))
        print('Video Indexer API: Upload Completed, Indexing file started.')
        #print(response_body)

except requests.exceptions.RequestException as e:
    # A serious problem happened, like an SSLError or InvalidURL
    print("Error: {}".format(e))



