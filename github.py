'''Interacts with the GitHub API'''
import os
import json
import textwrap
import ConfigParser

import requests

BASEURL = "https://api.github.com/notifications"

def get_unique_ids():
    try:
        with open("updated_at.txt", "r") as record:
            unique_id = record.read().split('\n')
            unique_id = list(filter(None, unique_id))
    except FileNotFoundError:
        unique_id = []

    return unique_id


def build_notification_message(notifcation, config):
    repo = notifcation['repository']
    repoName = repo['name']
    repoURL = repo['html_url']

    repoOwner = repo['owner']['login']
    repoOwnerURL = repo['owner']['html_url']

    subjectTitle = notification['subject']['title']
    subjectURL = notification['subject']['latest_comment_url']

    html_req = requests.get(url=subjectURL, headers={'Authorization' : config.GITTOKEN})
    subject_resp = json.loads(html_req.text)
    subjectURL2 = subject_resp['html_url']
    subjectType = notification['subject']['type']

    message_template = textwrap.dedent("""
    From: [{repoOwner}]({repoOwnerURL})
    Repository: [{repoName}]({repoURL})
    Subject: [{subjectTitle}]({subjectURL})
    Type: {subjectType}
    """)

    messageContent = message_template.format(repoOwner=repoOwner, repoOwnerURL=repoOwnerURL,
                                             repoName=repoName, repoURL=repoURL, subjectTitle=subjectTitle, subjectURL=subjectURL2,
                                             subjectType=subjectType)
    return messageContent


def notifications():
    """Check GitHub for Notifications"""
    req = requests.get(url=BASEURL, headers={'Authorization' : config.GITTOKEN})
    notifications = json.loads(req.text)
    unique_id = get_unique_ids()

    messageContent = None
    for notification in notifications:
        if str(notifcation['updated_at']) not in unique_id:
            unique_id = str(notification['updated_at'])
            messageContent = build_notification_message(notification)
            with open('updated_at.txt', 'a') as record:
                record.write (unique_id + '\n')

    return messageContent

if __name__ == '__main__':
    notifications()
