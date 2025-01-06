from langchain_community.document_loaders import YoutubeLoader
def load_vid_transript(youtube_url):
    loader = YoutubeLoader.from_youtube_url(youtube_url=youtube_url, add_video_info=False)
    docs = loader.load()
    return docs
