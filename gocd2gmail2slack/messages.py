
import re

GOCD_PATTERN = r"Stage\s*\[(\S*)\/\d*\/(\S*)\/\d*\]\s*(passed|failed)"


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
