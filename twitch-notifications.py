#!/usr/bin/env python

from apprise import Apprise
from collections import namedtuple
from datetime import datetime, timedelta
from json import dump, load
from os import path
from requests import get
from sys import exit
from yaml import safe_load

config_data = safe_load(open("config-example.yml"))

rewrite_twitch_category_ids = False
twitch_category_id_file = "twitch_category_ids.json"

api_url = "https://api.twitch.tv/helix/"
headers = {
    "Client-ID": config_data["clientid"],
    "Authorization": "Bearer {}".format(config_data["oauth"]),
}


def twitchTime(time):
    # Twitch api uses a time format that datetime can not parse by default
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")


def rewriteTwitchCategoryIds():
    global rewrite_twitch_category_ids
    rewrite_twitch_category_ids = True


def categoryName(id):
    if id in twitch_category_ids:
        return twitch_category_ids[id]
    else:
        # https://dev.twitch.tv/docs/api/reference#get-games
        r = get(
            "{}games?id={}".format(api_url, str(id)),
            headers=headers,
            timeout=(3.05, 27),
        )
        category_data = r.json()["data"]
        if not category_data:
            return "Unknown"
        else:
            category_name = category_data[0]["name"]
            twitch_category_ids[id] = category_name
            # only need to set the global once
            if rewrite_twitch_category_ids is False:
                rewriteTwitchCategoryIds()
            return category_name


def liveStreams(channels):
    # the api allows for up to look up 100 within one call
    # error out if there are over 100 channels
    # todo: add support for more than 100 channels, via paganation
    if len(channels) > 100:
        print("ERROR: More than 100 channels currently not supported.")
        exit(1)
    # build string of channels to feed to api call
    channel_list = ""
    for channel in channels:
        channel_list += "user_login={}&".format(channel)
    # make api call
    # https://dev.twitch.tv/docs/api/reference#get-streams
    r = get(
        "{}streams?{}".format(api_url, channel_list),
        headers=headers,
        timeout=(3.05, 27),
    )
    if r.status_code != 200:
        print("ERROR: {} when attempting to connect to the Twitch API.".format(r.text))
        exit(1)
    data = r.json()["data"]
    channel_info = {}
    # add game title from game id
    # covert from list of dicts to dicts of dicts
    for item in data:
        item["category_name"] = categoryName(item["game_id"])
        channel_info[item["user_name"]] = item
    return channel_info


def buildMessage(channel_info):
    middle = " is now streaming "
    if len(channel_info) == 1:
        items = channel_info.pop(0)
        return "{}{}{}.".format(items.channel, middle, items.category)
    else:
        message = ""
        while len(channel_info) > 0:
            if len(channel_info) == 1:
                items = channel_info.pop(0)
                message += "and {}{}{}.".format(items.channel, middle, items.category)
            else:
                items = channel_info.pop(0)
                message += "{}{}{}, ".format(items.channel, middle, items.category)
        return message


# load twitch_category_id_file if it exist
if path.isfile(twitch_category_id_file) is True:
    with open(twitch_category_id_file) as json_file:
        twitch_category_ids = load(json_file)
else:
    twitch_category_ids = {}

# get data on which channels are currently streaming
live_data = liveStreams(config_data["channels"])

# find streams that have started within the threshold.
time_offset = datetime.utcnow() - timedelta(minutes=config_data["offset"])
new_stream = namedtuple("data", "channel category")
new_streams = []

for x in (x for x in live_data if time_offset < twitchTime(live_data[x]["started_at"])):
    new_streams.append(
        new_stream(live_data[x]["user_name"], live_data[x]["category_name"])
    )

# send notifications if new streams have started
if new_streams:
    apobj = Apprise()
    for notification in config_data["noticiations"]:
        apobj.add(notification)
    message = buildMessage(new_streams)
    apobj.notify(title="Twitch", body=message)

# save twitch_category_id_file only if new game has been added
if rewrite_twitch_category_ids is True:
    with open(twitch_category_id_file, "w") as f:
        dump(twitch_category_ids, f, ensure_ascii=False)
