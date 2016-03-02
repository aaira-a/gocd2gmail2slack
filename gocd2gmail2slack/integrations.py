
import gmail as gm
import messages
import slack

from cfg.config import (
    WEBHOOK_URL,
    GOCD_DASHBOARD_URL,
)


def main():
    try:
        service = gm.get_service()
        labels = gm.get_labels(service)
        initial_messages = gm.get_messages(service, include_labels=['UNREAD'])
        messages_details = gm.get_messages_details(service, initial_messages)

        for message in messages_details:
            subject = messages.get_subject(message)
            if messages.is_gocd_pattern(subject):
                gocd_details = messages.get_gocd_details(subject)
                if slack.is_matching_send_rule(gocd_details):
                    body = messages.get_body(message)
                    revision_number = messages.get_revision_number(body)
                    changeset_url = messages.get_changeset_url(body)
                    slack.send_to_slack(gocd_details['pipeline'],
                                        gocd_details['stage'],
                                        gocd_details['status'],
                                        revision_number,
                                        changeset_url,
                                        WEBHOOK_URL, GOCD_DASHBOARD_URL)
                    gm.add_label(service, messages.get_id(message),
                                 'SENT_TO_SLACK', labels)

            gm.remove_label(service, messages.get_id(message),
                            'UNREAD', labels)
    except:
        pass


if __name__ == "__main__":
    main()
