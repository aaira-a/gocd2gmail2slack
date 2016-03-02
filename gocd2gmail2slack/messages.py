
import base64
import re

GOCD_PATTERN = r"Stage\s*\[(\S*)\/\d*\/(\S*)\/\d*\]\s*(passed|failed|is fixed)"
BASE_TFS_URL_PATTERN = r"Tfs: (https:\/\/.*?)\\r"
REVISION_PATTERN = r"revision: (\d+)"


def get_subject(message):
    for header in message['payload']['headers']:
        if header['name'] == 'Subject':
            return header['value']


def is_gocd_pattern(subject):
    match = re.search(GOCD_PATTERN, subject)
    if match:
        return True
    else:
        return False


def get_gocd_details(subject):
    match = re.search(GOCD_PATTERN, subject)
    result = {'pipeline': match.group(1),
              'stage': match.group(2),
              'status': match.group(3),
              }
    return result


def get_timestamp(message):
    return message['internalDate']


def get_id(message):
    return message['id']


def get_body(message):
    encoded = message['payload']['body']['data']
    return str(base64.urlsafe_b64decode(encoded))


def get_changeset_url(body):
    match = re.search(BASE_TFS_URL_PATTERN, body)
    if match:
        base_url = match.group(1)
        return base_url + "/_versionControl/changeset/" + get_revision_number(body)


def get_revision_number(body):
    match = re.search(REVISION_PATTERN, body)
    if match:
        return match.group(1)
