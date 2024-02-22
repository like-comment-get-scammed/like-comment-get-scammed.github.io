import utils_youtube

'''
Example script to use youtube utils
Please note the API limitation.
'''

def crawl_channel(channel_id=None, username=None, video_id=None):
    service2 = utils_youtube.load_service_var_balance()
    if (channel_id is None
            and username is None
            and video_id is None):
        print("Channel ID, User Name and Video ID cannot be all None.")
        return
    if (channel_id is not None):
        # use it
        pass
    elif (username is not None):
        # get channel ID from user name
        channel_id = utils_youtube.channel_id_by_username(
            service=service2, username=username)
    elif (video_id is not None):
        # get channel ID from sample video ID
        channel_id, _ = utils_youtube.channel_id_by_video_id(
            service=service2, video_id=video_id)
    print(f"Crawling channel ID: {channel_id}")
    utils_youtube.dump_comment_reply_data_by_channel(
        service=service2, channel_id=channel_id)
    return

if __name__ == '__main__':
    video_id = 'NreJ_VEcuYE'  # Pokemon
    crawl_channel(video_id=video_id)
