from datetime import datetime

from apiclient.discovery import build
from geopy.geocoders import Nominatim

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def youtube_search_video(query, max_results, loc, sday, smonth, syear, eday, emonth, eyear):
    geolocator = Nominatim(user_agent="Youtube Search")
    locatione = geolocator.geocode(loc)

    start_time = datetime(syear, smonth, sday).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime(eyear, emonth, eday).strftime('%Y-%m-%dT%H:%M:%SZ')

    search_keyword = youtube_object.search().list(q=query, part="id, snippet", type='video',
                                                  order = 'relevance',
                                                  # location=str(locatione.latitude) + ',' + str(locatione.longitude),
                                                  publishedAfter=start_time,
                                                  publishedBefore=end_time,
                                                  maxResults=max_results).execute()

    results = search_keyword.get("items", [])

    videos = []

    for result in results:
        if result['id']['kind'] == "youtube#video":
            videos.append("(% s),(% s),(% s),(% s),(% s)" % (
                result["snippet"]["title"], result["id"]["videoId"], result['snippet']['description'],
                result['snippet']['publishedAt'],
                result['snippet']['thumbnails']['default']['url']))

    print("Videos:\n\n", "\n\n".join(videos), "\n\n")


def youtube_search_playlist(query, max_results, loc):
    geolocator = Nominatim(user_agent="Youtube Search")
    locatione = geolocator.geocode(loc)

    search_keyword = youtube_object.search().list(q=query, part="id, snippet", type='playlist',
                                                  # location=locatione.latitude + ',' + locatione.longitude,
                                                  maxResults=max_results).execute()

    results = search_keyword.get("items", [])

    playlists = []

    for result in results:
        if result['id']['kind'] == "youtube#playlist":
            playlists.append("(% s),(% s),(% s),(% s)" % (
                result["snippet"]["title"],
                result["id"]["playlistId"],
                result['snippet']['description'],
                result['snippet']['thumbnails']['default']['url']))

    print("Playlists:\n", "\n".join(playlists), "\n")


def youtube_search_channel(query, max_results, loc):
    geolocator = Nominatim(user_agent="Youtube search")
    locatione = geolocator.geocode(loc)

    search_keyword = youtube_object.search().list(q=query, part="id, snippet", type='channel',
                                                  # location=locatione.latitude + ',' + locatione.longitude,
                                                  maxResults=max_results).execute()

    results = search_keyword.get("items", [])

    channels = []

    for result in results:
        if result['id']['kind'] == "youtube#channel":
            channels.append("(%s),(%s),(%s),(%s),(%s)" % (
                result["snippet"]["channelTitle"],
                result["snippet"]["title"],
                result["id"]["channelId"],
                result['snippet']['description'],
                result['snippet']['thumbnails']['default']['url']))

    print("Channels:\n", "\n".join(channels), "\n")


if __name__ == "__main__":
    youtube_search_video('coffin', 10, 'us', 14, 6, 2019, 16, 9, 2019)
    # youtube_search_playlist('ML', 10, 'USA')
    # youtube_search_channel('Bimo', 10, 'USA')