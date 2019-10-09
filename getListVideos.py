# Get a list of all videos in your account in video indexer - returns the VideoId you need for other operations

#List Videos API: https://api-portal.videoindexer.ai/docs/services/Operations/operations/List-Videos?

import requests


##### CONFIGURE YOUR ACCOUNTS & ACCESS HERE 

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

print('Getting list...')

# Get list of videos available on Video Indexer API
listvideo_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos'.format(video_indexer_region,video_indexer_account_id)

listvideo_headers = { 'x-ms-client-request-id': '', }
listvideo_params = {
    'accessToken':auth_token
    }

try:
    response = requests.get(listvideo_uri, headers=listvideo_headers, params=listvideo_params)
    response_body = response.json()

    # Consider any status other than 2xx an error
    if not response.status_code // 100 == 2:
        print("Error: {} {}".format(response.status_code, response_body))
    else:
        #DEBUG print(response_body)
        for result in response_body["results"]:
            print("Video id: {} is for file {} and is {}.".format(result.get('id'), result.get('name'), result.get('state')))

except requests.exceptions.RequestException as e:
    # A serious problem happened, like an SSLError or InvalidURL
    print("Error: {}".format(e))

