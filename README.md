# Azure Video Indexer - Python API Usage Samples
Sample python code for using several Azure Video Indexer service APIs to upload and index files, then extract the transcript with speaker identification and multiple languages supported.

An overview of [Azure Video Indexer Service](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/video-indexer-overview) explains more about the service capabilities.

## Prerequisites ##
You need to install Python and setup an account with Azure Video Indexer.  

1. Download and install [Python](https://www.python.org/downloads/).  Use whatever IDE/Notebooks you prefer, I used VS.Code - these samples use API calls only, so no additional setup/SDK installation is required.

2. Setup a [Azure Video Indexer Account](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/video-indexer-get-started) note this will walk you through using the portal to upload a video, which is a great way to see how the service works and explore the widgets that are avaiable (and can be 

3. Subscribe to the [Video Indexer API](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/video-indexer-use-apis) through the Video Indexer Developer Portal.

4. Setup Azure Blob storage account and load your video/audio files.  Example instructions [here](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal).  

## Upload and Index a File, then Generate a Transcript ##
Example files are included in this repo, and are broken out by each API call, so you can use what you need.  The step by step process would be:

1. Load your Video/Audio file using [postUploadVideo.py](postUploadVideo.py).  Note the parameters in this example are for AudioOnly, and include multi-language.  Documentation on the [API Parameters](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/upload-index-videos) can help you decide what changes you should make for your scenario.

2. Because the indexing process will take several (to a lot) of minutes, you can use [getGetVideoIndex.py](getGetVideoIndex.py) to check the status of the upload and indexing process.

Once your file has been processed, a few options are:

3. To extract the audio transcript use [getTranscript.py](getTranscript.py) that leverages the getVideoIndex API again, but then parses the results to provide just the transcript.  To learn more about the data available see [Video Indexer Output](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/video-indexer-output-json-v2).

4. You can extract widgets and embed them into your own application to simulate the Video Indexer Portal.  For more information about using embedded objects see the [documentation](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/video-indexer-embed-widgets). The [getVideoInsightsWidget.py](getVideoInsightsWidget.py) shows using an API to get the code to embed an Insights widget - the part of the portal that shows all the insights extracted including sentiment, keywords, transcripts, etc. and lets you edit the transcript as well.

5. If you want to adjust the settings for your file you can just re-index it rather than upload again, use [putReIndex.py](putReIndex.py) and again, reference the [API Parameters](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/upload-index-videos) to see what adjustments are available.

6. If you forget your video id, you can use [getListVideos.py](getListVideos.py) to view what files have been indexed and find your id.


