from downloader import YoutubeDownloader


if __name__ == "__main__":
    yt_downloader = YoutubeDownloader()
    yt_downloader.execute(url="https://www.youtube.com/watch?v=EAjQNcH9ug0")
    print("Finish!")