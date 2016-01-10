
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


def is_matching_send_rule(gocd_details):
    if gocd_details['status'] == 'failed':
        return True
    if gocd_details['status'] == 'passed':
        if gocd_details['stage'] in ['Package', 'Deploy',
                                     'Default', 'defaultStage']:
            return True
    else:
        return False
