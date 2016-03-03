
import json
import requests


def send_to_slack(body, webhook_url):
    requests.post(webhook_url, data=json.dumps(body))


def message_builder(gocd_details, changeset, dashboard_url):

    pipeline = gocd_details['pipeline']
    stage = gocd_details['stage']
    status = gocd_details['status']

    pipeline_url = get_pipeline_url(dashboard_url, pipeline)

    if status in ['passed', 'is fixed']:
        icon = ':white_check_mark:'
    elif status == 'failed':
        icon = ':x:'
    else:
        return

    body = {'username': 'go build status - ' + status,
            'icon_emoji': icon,
            'text': '<' + pipeline_url + '|' + pipeline + '>'}

    if stage not in ['Deploy', 'defaultStage', 'Default', 'DeployAll']:
        body['text'] += '\nChangeset: <' + changeset['url'] + '|'
        '' + changeset['id'] + '>'

    if status == 'failed':
        body['text'] += '\nStage: ' + stage

    return body


def is_matching_send_rule(gocd_details):
    if gocd_details['status'] == 'failed':
        return True
    if gocd_details['status'] in ['passed', 'is fixed']:
        if gocd_details['stage'] in ['Package', 'Deploy',
                                     'Default', 'defaultStage',
                                     'DeployAll']:
            return True
    else:
        return False


def get_pipeline_url(gocd_dash_root_url, pipeline):
    return gocd_dash_root_url + '/tab/pipeline/history/' + pipeline
