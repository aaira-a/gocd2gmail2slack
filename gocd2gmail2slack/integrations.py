
import gmail as Gm
import messages as Msg
import slack

from cfg.config import (
    WEBHOOK_URL,
    GOCD_DASHBOARD_URL,
)


def main():
    try:
        service, labels, messages_details = initialize()
        process(service, labels, messages_details)
    except:
        pass


def initialize():
    service = Gm.get_service()
    labels = Gm.get_labels(service)
    initial_messages = Gm.get_messages(service, include_labels=['UNREAD'])
    messages_details = Gm.get_messages_details(service, initial_messages)
    return (service, labels, messages_details)


def process(service, labels, messages_details):
    for item in messages_details:
        subject = Msg.get_subject(item)

        if Msg.is_gocd_pattern(subject):
            gocd_details = Msg.get_gocd_details(subject)

            if slack.is_matching_send_rule(gocd_details):
                body = Msg.get_body(item)
                changeset = Msg.get_changeset_info(body)
                text = (slack
                        .message_builder(gocd_details,
                                         changeset,
                                         GOCD_DASHBOARD_URL))

                slack.send_to_slack(text, WEBHOOK_URL)

                Gm.add_label(service, Msg.get_id(item),
                             'SENT_TO_SLACK', labels)

        Gm.remove_label(service, Msg.get_id(item),
                        'UNREAD', labels)


if __name__ == "__main__":
    main()
