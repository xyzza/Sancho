# coding: utf-8
_USERS_STORAGE = {
    'default_id': None, # current issue
}


def set_user_issues(user_id, issue=None):
    if not issue:
        issue = Issue('', '')
    _USERS_STORAGE[user_id] = issue
    return _USERS_STORAGE[user_id]


def get_user_issue(user_id):
    return _USERS_STORAGE[user_id]


class Issue(object):
    __slots__ = 'text', 'summary', 'date'

    def __init__(self, text, summary, date=None):
        self.text = text
        self.summary = summary
        self.date = date
