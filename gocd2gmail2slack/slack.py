
import json
import requests

from gocd2gmail2slack.cfg.config import WEBHOOK_URL


def send_to_slack(pipeline, stage, status):

    if status == 'passed':
        icon = ':white_check_mark:'
    elif status == 'failed':
        icon = ':x:'
    else:
        return

    body = {'username': 'go build status - ' + status,
            'icon_emoji': icon,
            'text': 'Pipeline: ' + pipeline + '\n' + 'Stage: ' + stage}

    requests.post(WEBHOOK_URL, data=json.dumps(body))
