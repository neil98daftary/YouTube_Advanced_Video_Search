#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:26:44 2020

@author: mana
"""
from apiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd


api_key = "AIzaSyBsHCndOUQMiB9YTobh-6Doh_Lt-WWHZOo"


def loop(keywords, order):
    final = []
    for keyword in keywords:
        days = 7
        results = search_keyword(keyword, order)
        results = results.sort_values(['Custom_Score'], ascending=[0])
#         print(results.head(1))
        final.append(results)
    final = pd.concat(final, axis = 0)
    final = final.sort_values(['Custom_Score'], ascending=[0])
    
    print("Top Videos are:")
    print(final.head(5))
    final.head(5).to_csv("videos.csv", index=False)
    return(final.head(5).to_dict())
    

    
def search_keyword(keyword, order1, days=365):
    api_key = "AIzaSyBsHCndOUQMiB9YTobh-6Doh_Lt-WWHZOo"
    youtube_api = build('youtube', 'v3', developerKey = api_key)
    
    search_start_date = datetime.today() - timedelta(days)
    date_string = datetime(year=search_start_date.year,month=search_start_date.month,
                               day=search_start_date.day).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    results = youtube_api.search().list(q=keyword, part="snippet", type="video",
                                    order=order1, maxResults=50, videoDuration="medium",
                                    relevanceLanguage="en", publishedAfter=date_string).execute()
    
    final_scores = results_scores(results, youtube_api)
    return final_scores


def results_scores(results, youtube_api):
    final_scores = pd.DataFrame(columns=('Title', 'Video URL', 'Custom_Score',
                            'Views', 'Channel Name','Num_subscribers',
                            'View-Subscriber Ratio'))
    for i,item in enumerate(results["items"]):
        days = days_live(item)
        stats = stats_query(item, youtube_api)
        if stats["views"]>5000:
            Subs = subs(item, youtube_api)
            Title = item["snippet"]["title"]
            Url = url(item)
            Score, Ratio = video_score(stats, Subs, days)
            C_Name = item["snippet"]["channelTitle"]
            Views = stats["views"]
            final_scores.loc[i+1] = [Title, Url, Score, Views, C_Name, Subs, Ratio]
#     print("THISSSSS", final_scores)
    return final_scores


def video_score(stat, sub, days):
    if sub != 0:
        ratio = stat["views"]/sub
    else:
        ratio = 0
    score = ratio/days + (stat["likes"]-stat["dislikes"])/(stat["views"] * 10)
    
    return score, ratio


def days_live(item):
    pub = item["snippet"]["publishTime"]
    pub = datetime.strptime(pub, '%Y-%m-%dT%H:%M:%SZ')
    today = datetime.today()
    diff = today-pub
    if int(diff.days) == 0:
        return 1
    else:
        return int(diff.days)
    
    
def subs(item, youtube_api):
    channelId = item["snippet"]["channelId"]
    stats = youtube_api.channels().list(id=channelId, part='statistics').execute()
    flag = stats['items'][0]['statistics']['hiddenSubscriberCount']
    if flag:
        return 10e6
    else:
        return (int(stats['items'][0]['statistics']['subscriberCount']))
    
    
def url(item):
    videoId = item['id']['videoId']
    return ("https://www.youtube.com/watch?v=" + videoId)


def stats_query(item, youtube_api):
    videoId = item['id']['videoId']
    stat = {}
    stats = youtube_api.videos().list(id=videoId, part="statistics").execute()
    if "likeCount" in stats['items'][0]['statistics']:
        stat["likes"] = int(stats['items'][0]['statistics']['likeCount'])
        stat["dislikes"] = int(stats['items'][0]['statistics']['dislikeCount'])
    else:
        stat["likes"] = 0
        stat["dislikes"] = 0
    stat["views"] = int(stats['items'][0]['statistics']['viewCount'])
    return (stat)


