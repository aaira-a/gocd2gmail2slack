
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'cfg/client_secret.json'
APPLICATION_NAME = 'gocd2gmail2slack'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credential_dir = os.path.join(current_dir, 'cfg', 'cred')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'saved_credentials.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_service():
    """Creates a Gmail API service object.

    Returns:
        Service
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service


def get_labels(service):
    labels = service.users().labels().list(userId='me').execute()
    return labels


def get_label_id(label_name, labels):
    for label in labels['labels']:
        if label['name'] == label_name:
            return label['id']


def query_builder(include_labels=None, exclude_labels=None):
    query = None
    if include_labels:
        prefix = 'label:'
        query = ' label:'.join(include_labels)
        query = prefix + query

    if exclude_labels:
        prefix = '-label:'
        query = ' -label:'.join(exclude_labels)
        query = prefix + query

    return query
