
import json
import requests

from cfg.config import (
    CI_STAGES,
    DEPLOY_STAGES,
)


def send_to_slack(body, webhook_url):
    requests.post(webhook_url, data=json.dumps(body))


def message_builder(gocd_details, changeset, dashboard_url):

    pipeline = gocd_details['pipeline']
    stage = gocd_details['stage']
    status = gocd_details['status']

    pipeline_url = get_pipeline_url(dashboard_url, pipeline)

    if status in ['passed', 'is fixed']:
        icon = ':white_check_mark:'
    elif status in ['failed', 'is broken']:
        icon = ':x:'
    else:
        return

    body = {'username': 'go build status - {0}'.format(status),
            'icon_emoji': icon,
            'text': '<{0}|{1}>'.format(pipeline_url, pipeline)}

    if stage in CI_STAGES:
        body['text'] += ('\nChangeset: <{0}|{1}> - {2}: {3}'
                         ''.format(changeset['url'],
                                   changeset['id'],
                                   changeset['author'],
                                   changeset['comment']))

    if status in ['failed', 'is broken']:
        body['text'] += '\nStage: ' + stage

    return body


def is_matching_send_rule(gocd_details):
    if gocd_details['status'] in ['failed', 'is broken']:
        return True
    if gocd_details['status'] in ['passed', 'is fixed']:
        if gocd_details['stage'] in ['Package', 'package'] + DEPLOY_STAGES:
            return True
    else:
        return False


def get_pipeline_url(gocd_dash_root_url, pipeline):
    return gocd_dash_root_url + '/tab/pipeline/history/' + pipeline
