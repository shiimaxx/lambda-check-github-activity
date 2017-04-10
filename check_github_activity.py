#!/usr/bin/env python3

import datetime
import os

from pytz import timezone

from github import Github


GITHUB_USER = os.environ["GITHUB_USER"]
GITHUB_PASSWORD = os.environ["GITHUB_PASSWORD"]


if __name__ == "__main__":
    current_date = datetime.date.today()
    git = Github(GITHUB_USER, GITHUB_PASSWORD)

    for event in git.get_user("shiimaxx").get_events():
        if event.type == "PushEvent":
            recently_event = event
            break

    jst_created_at = timezone("Asia/Tokyo").localize(event.created_at)
    recently_event_date = jst_created_at.date()

    if current_date > recently_event_date:
        print("Shut the fuck up and write some code.")
