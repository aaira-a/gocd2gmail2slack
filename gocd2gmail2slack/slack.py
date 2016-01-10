
import json
import requests


def send_to_slack(pipeline, stage, status, webhook_url):

    if status == 'passed':
        icon = ':white_check_mark:'
    elif status == 'failed':
        icon = ':x:'
    else:
        return

    body = {'username': 'go build status - ' + status,
            'icon_emoji': icon,
            'text': 'Pipeline: ' + pipeline + '\n' + 'Stage: ' + stage}

    requests.post(webhook_url, data=json.dumps(body))
