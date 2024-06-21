import logging
from pytube import YouTube

class YoutubeDownloader:
    def __init__(self, ):
        self._logger = logging.getLogger(__name__)

    def execute(self, url):
        self._logger.info(f"Downloading video from {url}")
        video = YouTube(url)
        video.streams.filter(
            progressive=True, 
            file_extension='mp4')\
            .order_by('resolution')\
            .desc().first().download(output_path='videos/')
        self._logger.info(f"Done!")