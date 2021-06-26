# Custom error handling

class VideoNotYoutubeLink(Exception):
    """Custom error handling for when a video entered was not a youtube video."""

    def __init__(self, video_link: str, message: str = "The video entered was not a youtube video"):
        self.video_link = video_link
        self.message = message
        super().__init__(self.message)
