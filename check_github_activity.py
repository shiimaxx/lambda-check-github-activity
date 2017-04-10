import datetime
from pytz import timezone

from github import Github


if __name__ == "__main__":
    current_date = datetime.date.today()
    git = Github("", "")

    for event in git.get_user("shiimaxx").get_events():
        if event.type == "PushEvent":
            recently_event = event
            break

    jst_created_at = timezone("Asia/Tokyo").localize(event.created_at)

    recently_event_time \
        = datetime.datetime.strftime(jst_created_at, "%Y-%m-%d")
