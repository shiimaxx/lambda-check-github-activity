#!/usr/bin/env python3

import datetime
import json
import os
import urllib

from github import Github


GITHUB_USER = os.environ["GITHUB_USER"]
GITHUB_LOGIN_USER = os.environ["GITHUB_LOGIN_USER"]
GITHUB_LOGIN_PASSWORD = os.environ["GITHUB_LOGIN_PASSWORD"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]


def to_slack(text):
    json_data = json.dumps({"text": text}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    requests = urllib.request.Request(
            SLACK_WEBHOOK_URL, data=json_data, headers=headers)

    response = urllib.request.urlopen(requests)

    return response


def lambda_handler(event, context):
    current_date = datetime.date.today()
    git = Github(GITHUB_LOGIN_USER, GITHUB_LOGIN_PASSWORD)

    for github_event in git.get_user(GITHUB_USER).get_events():
        if github_event.type == "PushEvent":
            recently_github_event = github_event
            break

    jst_created_at = \
        recently_github_event.created_at + datetime.timedelta(hours=9)
    recently_event_date = jst_created_at.date()

    if current_date == recently_event_date:
        response = to_slack("Shut the fuck up and write some code.")

    return response.status
