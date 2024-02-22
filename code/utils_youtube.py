import os
import sys
import pickle
import requests
import datetime
import utils_db
import time
import random

# import google.oauth2.credentials

from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import utils_db

############# Global variables #############

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.


# for multiple use
CLIENT_SECRETS_FILE_LIST = [
    # "./cred/your_credential.json",
]
SERVICE_VAR_FILE_LIST = [
    f"./cred/service_var{i}.pickle" for i in range(len(CLIENT_SECRETS_FILE_LIST))
]

# List of videos used for test API availability
TEST_VIDEOS = []
with open("test_video_quota.txt", "r") as fp1:
    for line in fp1:
        TEST_VIDEOS.append(line.strip().strip('\n'))

# global service var
CURR_SERVICE_IDX = 0
SVC_VAR = None

# counter for API in each run
API_USAGE_COUNTER = 0

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# video created after this date will be monitored every hour for 10 days
MONITOR_NEW_VIDEO_DATE = '2022-09-09 00:00:01'


MAX_REPLIES_PER_THREAD = 500
MAX_THREAD_PER_VIDEO = 50000


fmt = "%Y-%m-%d %H:%M:%S"
fmt_T = "%Y-%m-%dT%H:%M:%S"
fmt_date_fn = "%Y_%m_%d"  # for date str in folder name
############# Helper Functions #############

# def refresh_service_var(secret_fn,service_var_fn):
#   # this will refresh service variable in case its expired
#   # need user interaction
#   service = get_authenticated_service(secret_fn=secret_fn)
#   save_service_var(service_var_fn,service)
#   return service


def get_authenticated_service(secret_fn):
    flow = InstalledAppFlow.from_client_secrets_file(secret_fn, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# def save_service_var(service_var_fn,service):
#   with open(service_var_fn,'wb') as fp1:
#     pickle.dump(service,fp1)
#   print("dumped to {}".format(service_var_fn))
#   return

# def load_service_var(service_var_fn):
#   with open(service_var_fn,'rb') as fp1:
#     service = pickle.load(fp1)
#   print("Loaded from {}".format(service_var_fn))
#   return service


def refresh_service_var_balance(start_index=0):
    # this will refresh service variable in case its expired
    # need user interaction
    for i in range(start_index, len(CLIENT_SECRETS_FILE_LIST)):
        secret_file_fn = CLIENT_SECRETS_FILE_LIST[i]
        print(f"refreshing for secret {secret_file_fn}")
        flow = InstalledAppFlow.from_client_secrets_file(secret_file_fn, SCOPES)
        credentials = flow.run_console()
        service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        service_fn = SERVICE_VAR_FILE_LIST[i]
        with open(service_fn, 'wb') as fp1:
            pickle.dump(service, fp1)
        print("dumped to {}".format(service_fn))
    return service


def load_service_var_balance():
    # load one service var that is not used up
    global CURR_SERVICE_IDX
    ts_now_str = datetime.datetime.now().strftime(fmt)
    for i, fn in enumerate(SERVICE_VAR_FILE_LIST):
        if (i < CURR_SERVICE_IDX):
            continue
        service_fn = fn
        secret_file_fn = CLIENT_SECRETS_FILE_LIST[i]  # only for display
        with open(service_fn, 'rb') as fp1:
            service = pickle.load(fp1)
        FoundAPI = False
        # check if API is used up
        try:
            # make a 1-call API
            video_id = random.choice(TEST_VIDEOS)
            #video_list = video_list_top_by_channel_id(service=service,channel_id='UCQkw-wkyzTZH9nfkmATQ7dQ')
            videoInfoItem = test_quota_get_video_info(
                service=service, video_id=video_id)
            print(
                f"Test:videoid={video_id},info={videoInfoItem['snippet']['channelId']}")
            # channel_id_by_video_id(service=service,video_id='RfEMpIthy9s')
        except Exception as e:
            # API used up
            print(f"[{ts_now_str}]API {service_fn} used up, use next, err={str(e)}")
            continue
        print(f"[{ts_now_str}]API {service_fn} OK")
        # update current working service var index
        CURR_SERVICE_IDX = i

        FoundAPI = True
        break
    # if all used up, return the last one

    print(f"[{ts_now_str}]Loaded from {service_fn}({secret_file_fn})")
    if (FoundAPI == False):
        print(f"[Warning] All API used up, increase API num")
        sys.exit(0)
    return service, service_fn


def get_channel_img_info(channelId):
    thumbnails_url = None
    channel_img_bytes = None
    channelInfo = get_channel_info(channelId)
    # TODO return channel profile image / URL
    # https://developers.google.com/youtube/v3/docs/channels/list
    if (channelInfo is not None):
        if ("default" in channelInfo["snippet"]["thumbnails"]):
            thumbnails_url = channelInfo["snippet"]["thumbnails"]["default"]["url"]
            # usually 176x176
        channel_img_bytes = get_author_profile_img(thumbnails_url)
    print(
        f"[channelImg] Channel img url = {thumbnails_url}, bytes={len(channel_img_bytes)}")
    return thumbnails_url, channel_img_bytes


def get_channel_info(channelId):
    global SVC_VAR
    global API_USAGE_COUNTER
    results = SVC_VAR.channels().list(
        part="snippet,contentDetails,statistics",
        id=channelId
    ).execute()
    API_USAGE_COUNTER += 1
    if ('items' in results and len(results['items']) > 0):
        channelInfo = results['items'][0]

        return channelInfo
    else:
        return None


def get_author_profile_img(img_url):
    # try to retrieve author profile image, does not have API quota restriction
    # if success, return raw binary data, else return None
    myheader = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"}
    try:
        resp = requests.get(img_url)
        if (resp.status_code % 100 >= 4):
            print(f"Cannot get URL as response is {resp.status_code}")
            return None
        return resp.content
    except Exception as e:
        print(f"Exception in getting img {img_url}")
        return None


def test_quota_get_video_info(service, video_id):
    # video ID: ID of youtube video
    # get first 10 videos
    # will throw exception if Quota Exceeded
    global API_USAGE_COUNTER
    videoInfo = service.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id,
    ).execute()
    API_USAGE_COUNTER += 1
    videoInfoItem = videoInfo['items'][0]
    return videoInfoItem
# Call the API's commentThreads.list method to list the existing comments.
# Use pageToken to retrieve paginated results


def get_all_comment_threads(video_id, max_results=100):
    # video ID: ID of youtube video,
    # max_results: max results returned, can be infinite,
    #     the result set will be min(max_results, actual_comment_threads)
    global SVC_VAR
    global API_USAGE_COUNTER
    next_page_token = None
    comment_threads_list = []
    results = SVC_VAR.commentThreads().list(
        part="snippet,replies",
        videoId=video_id,
        pageToken=next_page_token,
        textFormat="plainText",
        maxResults=100,
    ).execute()
    API_USAGE_COUNTER += 1
    while (len(results["items"]) > 0):
        comment_threads_list.extend(results["items"])
        if (len(comment_threads_list) > max_results):
            break
        if ("nextPageToken" not in results):
            # end of list
            break
        next_page_token = results["nextPageToken"]
        results = SVC_VAR.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            pageToken=next_page_token,
            textFormat="plainText",
            maxResults=100,
        ).execute()
        API_USAGE_COUNTER += 1
    if (len(comment_threads_list) <= max_results):
        return comment_threads_list
    else:  # slightly greater due to 100 per page, cut it out
        return comment_threads_list[:max_results]


# Call the API's commentThreads.list method to list the existing comments.
# def get_comment_threads(service, video_id, channel_id, next_page_token=None):
#   results = SVC_VAR.commentThreads().list(
#     part="snippet,replies",
#     videoId=video_id,
#     # channelId=channel_id,
#     pageToken=next_page_token,
#     textFormat="plainText"
#   ).execute()

#   for item in results["items"]:
#     commentId = item["id"]
#     comment = item["snippet"]["topLevelComment"]
#     author = comment["snippet"]["authorDisplayName"]
#     authorChannelId = comment["snippet"]["authorChannelId"]['value']
#     text = comment["snippet"]["textDisplay"]
#     print(f"Comment by {author}: {text}, comment id=({commentId}, authorChannelId={authorChannelId}")

#   return results

# Call the API's comments.list method to list the existing comment replies.
# use pageToken to retrieve paginated results
def get_all_comment_replies(parent_id, max_results=100):
    # parent_id: comment thread ID
    # max_results: max results returned, can be infinite,
    #     the result set will be min(max_results, actual_comment_replies)
    global SVC_VAR
    global API_USAGE_COUNTER
    next_page_token = None
    comment_replies_list = []
    results = SVC_VAR.comments().list(
        part="snippet",
        parentId=parent_id,
        textFormat="plainText",
        pageToken=next_page_token,
        maxResults=100,
    ).execute()
    API_USAGE_COUNTER += 1
    while (len(results["items"]) > 0):
        comment_replies_list.extend(results["items"])

        if (len(comment_replies_list) > max_results):
            break
        if ("nextPageToken" not in results):
            # end of list
            break
        next_page_token = results["nextPageToken"]
        results = SVC_VAR.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            pageToken=next_page_token,
            maxResults=100,
        ).execute()
        API_USAGE_COUNTER += 1
    if (len(comment_replies_list) <= max_results):
        return comment_replies_list
    else:  # slightly greater due to 100 per page, cut it out
        return comment_replies_list[:max_results]

# # Call the API's comments.list method to list the existing comment replies.
# def get_comment_replies(service, parent_id):
#   # parent_id: comment thread ID
#   #
#   results = SVC_VAR.comments().list(
#     part="snippet",
#     parentId=parent_id,
#     textFormat="plainText"
#   ).execute()

#   for item in results["items"]:
#     commentId = item["id"]
#     authorChannelId = item["snippet"]["authorChannelId"]['value']
#     author = item["snippet"]["authorDisplayName"]
#     text = item["snippet"]["textDisplay"]

#   return results["items"]


def channel_id_by_username(username):
    global SVC_VAR
    global API_USAGE_COUNTER
    results = SVC_VAR.channels().list(
        part='snippet,contentDetails,statistics',
        forUsername=username,
    ).execute()
    API_USAGE_COUNTER += 1
    channelId = None
    for i in range(len(results['items'])):
        channelItem = results['items'][i]
        channelId = channelItem['id']
        break
    return channelId


def channel_id_by_video_id(video_id):
    # get channel ID by any video ID in that channel
    # cost 1 API
    global SVC_VAR
    global API_USAGE_COUNTER
    try:
        result = SVC_VAR.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id,
        ).execute()
        API_USAGE_COUNTER += 1
        channel_id = result['items'][0]['snippet']['channelId']
        channel_title = result['items'][0]['snippet']['channelTitle']
    except Exception as e:
        print(f"Exception in getting channel ID, err={str(e)}")
        return "---", "---"
    # print(result['items'][0]['snippet']['channelId'])
    return channel_id, channel_title


def channels_list_by_username(**kwargs):
    global SVC_VAR
    results = SVC_VAR.channels().list(
        **kwargs
    ).execute()
    API_USAGE_COUNTER += 1
    for i in range(len(results['items'])):
        channelItem = results['items'][i]
        print('This channel\'s ID is %s. Its title is %s, and it has %s views.' %
              (channelItem['id'],
               channelItem['snippet']['title'],
               channelItem['statistics']['viewCount']))
        # we only consider first channel for now
        break
    return


'''
Random sampling of channels have too much videos:
For random sampling of the videos, if we do it as a "true random" way, 
we won't be able to capture the content same video at every hour, 
which lost our initial goal. 
It is also a bad practice to make each capture "stateful" by remembering 
the last captured content, so I took this strategy to make our capture 
stable and fair:
1. if videos in last 10 days < 10, collect everything;
2. if more than 10 videos in the last 10 days, capture earliest published 
   video everyday; in the end there are 10 videos.

For example, if a channel publish a lot and have 2 videos at 3am and 6am today, 
we'll always capture that 3am video. 
'''


def video_list_all_by_channel_id(channel_id: str, before_date: datetime = None, max_results: int = 1000):
    # get all videos, API returns newest first
    global SVC_VAR
    global API_USAGE_COUNTER
    new_video_date = datetime.datetime.strptime('2001-01-01 00:00:01', fmt)

    if (before_date is not None):
        new_video_date = before_date

    next_page_token = None
    video_id_time_list = []
    activities = SVC_VAR.activities().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        pageToken=next_page_token,
        maxResults=100
    ).execute()
    API_USAGE_COUNTER += 1
    counter = 0
    while (len(activities["items"]) > 0):

        if (len(video_id_time_list) > max_results):
            #print("max results reached")
            break

        # process video IDs
        shouldStop = False
        for i in range(len(activities["items"])):
            activityItem = activities["items"][i]
            counter += 1
            activityType = activityItem["snippet"]["type"]
            if (activityType == 'upload'):
                title = activityItem["snippet"]["title"]
                description = activityItem["snippet"]["description"]
                contentDetails = activityItem["contentDetails"]
                publishedAt = activityItem["snippet"]["publishedAt"][:19]
                publishedAt_date = datetime.datetime.strptime(
                    publishedAt, fmt_T)
                if (publishedAt_date >= new_video_date):
                    print(f"[{counter}] New Video:{title[:10]},date={publishedAt}")
                    pass
                else:
                    # not new enough, no need next pages
                    print(
                        f"[{counter}]video published={publishedAt}, older than {before_date},stopped")
                    shouldStop = True
                    break
                videoId = contentDetails["upload"]["videoId"]
                video_id_time_list.append([publishedAt_date, videoId])
            else:
                pass
        # get next page batch
        if ("nextPageToken" not in activities):
            # end of list
            print("End of List")
            break
        if (shouldStop == True):
            # no need to get next page
            break
        next_page_token = activities["nextPageToken"]
        activities = SVC_VAR.activities().list(
            part="snippet,contentDetails",
            channelId=channel_id,
            pageToken=next_page_token,
            maxResults=100
        ).execute()
        print(f"next page: {len(activities['items'])} results")
        API_USAGE_COUNTER += 1
        # print(f"[{i}][{activityType}],title={title[:10]},description={description[:10]}")
    '''
  add all qualified video into video_id_list_ret
  '''
    video_id_time_list.sort()
    video_id_list = []
    prev_date = None
    if (len(video_id_time_list) > 10):
        for i, (publishedAt_date, videoId) in enumerate(video_id_time_list):
            # add 1 video per day (earliest published)
            if (prev_date is None or prev_date != publishedAt_date.date()):
                # first video of this day
                print(f"Added {videoId} at {publishedAt_date}")
                video_id_list.append(videoId)
                prev_date = publishedAt_date.date()
        # then select last 10 videos
        if (len(video_id_list) > 10):
            video_id_list = video_id_list[-10:]
    else:
        for i, (publishedAt_date, videoId) in enumerate(video_id_time_list):
            # add everything if list < 10
            print(f"Added {videoId} at {publishedAt_date}")
            video_id_list.append(videoId)
    print(
        f"Channel={channel_id}, Total videos:{len(video_id_time_list)}; selected videos:{len(video_id_list)}")
    return video_id_list


def video_list_top_by_channel_id(channel_id):
    # get first 100 videos, API returns newest first
    global SVC_VAR
    global API_USAGE_COUNTER
    activities = SVC_VAR.activities().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=100
    ).execute()
    API_USAGE_COUNTER += 1
    video_id_list = []
    for i in range(len(activities["items"])):
        activityItem = activities["items"][i]
        activityType = activityItem["snippet"]["type"]
        if (activityType == 'upload'):
            title = activityItem["snippet"]["title"]
            description = activityItem["snippet"]["description"]
            contentDetails = activityItem["contentDetails"]
            videoId = contentDetails["upload"]["videoId"]
            video_id_list.append(videoId)
        else:
            pass
        # print(f"[{i}][{activityType}],title={title[:10]},description={description[:10]}")
    return video_id_list


def process_reply(reply):
    replyId = reply["id"]
    replyAuthorChannelId = reply["snippet"]["authorChannelId"]['value']
    replyAuthor = reply["snippet"]["authorDisplayName"]
    replyText = reply["snippet"]["textDisplay"]
    replyAuthorChannelURL = reply["snippet"]["authorChannelUrl"]

    return [replyId, replyAuthorChannelId, replyAuthor, replyText, replyAuthorChannelURL]


def process_thread(commentThreadItem):
    commentThreadId = commentThreadItem["id"]
    commentThread = commentThreadItem["snippet"]["topLevelComment"]
    threadAuthorName = commentThread["snippet"]["authorDisplayName"]
    threadAuthorChannelId = commentThread["snippet"]["authorChannelId"]['value']
    threadText = commentThread["snippet"]["textDisplay"]
    totalReplyCount = commentThreadItem["snippet"]['totalReplyCount']
    return [commentThreadId, threadAuthorName, threadAuthorChannelId, threadText, totalReplyCount]


def dump_video_item(videoInfoItem):
    video_id = videoInfoItem['id']
    channel_id = videoInfoItem['snippet']['channelId']
    fn = f"data/{channel_id}__{video_id}__{utils_db.SNAPSHOT_ID}.pickle"
    with open(fn, 'wb') as fp1:
        pickle.dump(videoInfoItem, fp1)
    return


def dump_recent_video_item(videoInfoItem):
    # no upload to DB, just dump it with a unique TS
    video_id = videoInfoItem['id']
    channel_id = videoInfoItem['snippet']['channelId']
    capture_ts = int(time.time())  # seconds since epoch
    # data path
    date_str = datetime.datetime.now().strftime(fmt_date_fn)
    data_path = f"data_monitor/{date_str}"
    if (not os.path.exists(data_path)):  # create if not exist
        os.makedirs(data_path)
    fn = f"{data_path}/{channel_id}__{video_id}__{capture_ts}.pickle"
    with open(fn, 'wb') as fp1:
        pickle.dump(videoInfoItem, fp1)
    return


def load_video_comment_threads(channel_id, video_id):
    fn = f"data/{channel_id}__{video_id}.pickle"
    with open(fn, 'rb') as fp1:
        video_comment_threads = pickle.load(fp1)
    return video_comment_threads


def load_video_item_byfile(filename):
    fn = filename
    with open(fn, 'rb') as fp1:
        video_item = pickle.load(fp1)
    return video_item


def get_all_comments_replies_by_videoID(videoID):
    # get all threads, replies by video ID
    # return a list of commentThreadItem
    #print(f"getting threads for video ID {videoID}...")
    global SVC_VAR
    global API_USAGE_COUNTER
    video_comment_threads = []
    # try 3 times before give up
    for i in range(3):
        try:
            video_comment_threads = get_all_comment_threads(
                video_id=videoID,
                max_results=MAX_THREAD_PER_VIDEO)
            if (i != 0):
                print(f"Success getting theads from video{videoID} after error")
            break
        except Exception as e:
            # Maybe API used up, retry
            print(
                f"[{i}] Error getting threads from video {videoID}, error: {str(e)}")
            SVC_VAR, _ = load_service_var_balance()
            continue
    #print(f"getting replies for video ID {videoID}...")
    for i in range(len(video_comment_threads)):
        commentThreadItem = video_comment_threads[i]
        commentThreadId = commentThreadItem["id"]
        totalReplyCount = commentThreadItem["snippet"]['totalReplyCount']
        commentThreadItem['authorProfileImage'] = None
        try:
            authorProfileImageUrl = commentThreadItem["snippet"][
                'topLevelComment']['snippet']['authorProfileImageUrl']
            commentThreadItem['authorProfileImage'] = get_author_profile_img(
                authorProfileImageUrl)
        except Exception as e:
            # no action if HTTP request fail
            pass
        commentThreadItem['replies_scrape'] = []
        if (totalReplyCount > 0):
            video_comment_replies = []
            # try 3 times before give up
            for i in range(3):
                try:
                    video_comment_replies = get_all_comment_replies(
                        parent_id=commentThreadId,
                        max_results=MAX_REPLIES_PER_THREAD)
                    if (i != 0):
                        print(
                            f"Success getting replies from thread {commentThreadId},video{videoID} after error")
                    break
                except Exception as e:
                    # Maybe API used up, retry
                    print(
                        f"[{i}] Error getting replies from thread {commentThreadId},video{videoID} error: {str(e)}")
                    SVC_VAR, _ = load_service_var_balance()
                    continue
            for replyItem in video_comment_replies:
                replyItem['authorProfileImage'] = None
                try:
                    authorProfileImageUrl = replyItem['snippet']['authorProfileImageUrl']
                    replyItem['authorProfileImage'] = get_author_profile_img(
                        authorProfileImageUrl)
                except Exception as e:
                    # no action if HTTP request fail
                    pass
            commentThreadItem['replies_scrape'] = video_comment_replies

    return video_comment_threads


def get_video_info(videoID):
    # this one usually success
    global SVC_VAR
    global API_USAGE_COUNTER
    try:
        videoInfo = SVC_VAR.videos().list(
            part="snippet,contentDetails,statistics",
            id=videoID,
        ).execute()
        API_USAGE_COUNTER += 1
        videoInfoItem = videoInfo['items'][0]
        return videoInfoItem
    except Exception as e:
        print(f"Error in getting video Info:{videoID},error={str(e)}")
    return None


def dump_comment_reply_data_by_video_nodatabase(video_id: str, channel_img_url=None, channel_img_bytes=None):
    # single-call function for getting info for one video
    # for continuous monitoring, not inserting to DB
    # channel_img_url and channel_img_bytes are channel profile image

    video_info_item = get_video_info(videoID=video_id)
    video_comment_threads = get_all_comments_replies_by_videoID(
        videoID=video_id)

    if (video_info_item is not None):
        video_info_item['video_comment_threads'] = video_comment_threads
        video_info_item['channel_img_url'] = channel_img_url
        video_info_item['channel_img_bytes'] = channel_img_bytes
        dump_recent_video_item(videoInfoItem=video_info_item)
    print(f"vid={video_id},threads={len(video_comment_threads)}")
    return


def dump_comment_reply_data_by_channel(channel_id: str):
    # try:
    video_id_list = video_list_top_by_channel_id(channel_id=channel_id)
    # except Exception as e:
    #   print(f"Cannot List Videos for channel {channel_id}, error={str(e)}")
    #   return
    current_videos = utils_db.do_query(utils_db.load_video_list)
    err_count = 0
    for i, video_id in enumerate(video_id_list):
        if (video_id in current_videos):
            print(f"[{i}] Video ID {video_id} existed, SKIPPED API query")
            continue
        print(f"[{i}] getting info for video ID {video_id}...")
        video_info_item = get_video_info(videoID=video_id)
        if (video_info_item is not None):

            print(f"[{i}] getting comments/replies for video ID {video_id}...")
            video_comment_threads = []
            video_comment_threads = get_all_comments_replies_by_videoID(
                videoID=video_id)
            video_info_item['video_comment_threads'] = video_comment_threads
            dump_video_item(videoInfoItem=video_info_item)
            # log video, to database
            utils_db.insert_video_to_database(video_info_item)

            err_count = 0  # reset
        else:
            err_count += 1
            if (err_count > 10):
                print("ERROR: error count in multiple videos in a channel, stopping")
                break
    # end of for loop

    return


# Example usage
if __name__ == '__main__':
    pass
