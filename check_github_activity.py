#!/usr/bin/env python

import datetime
import json
import os
import urllib2

import lamvery

from github import Github


GITHUB_USER = os.environ["GITHUB_USER"]
GITHUB_LOGIN_USER = os.environ["GITHUB_LOGIN_USER"]
GITHUB_LOGIN_PASSWORD = lamvery.secret.get('GITHUB_LOGIN_PASSWORD')
SLACK_WEBHOOK_URL = lamvery.secret.get('SLACK_WEBHOOK_URL')


def to_slack(text):
    json_data = json.dumps({"text": text}).encode("utf-8")
    req = urllib2.Request(SLACK_WEBHOOK_URL)
    req.add_data(json_data)
    req.add_header("Content-Type", "application/json")
    urllib2.urlopen(req)

    return


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

    if current_date > recently_event_date:
        to_slack("Shut the fuck up and write some code.")

    return
