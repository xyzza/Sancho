#coding: utf-8
from jira import JIRA

# define JIRA instance
jac = JIRA('jira url')

authed_jira = JIRA(basic_auth=('user', 'pass'))
