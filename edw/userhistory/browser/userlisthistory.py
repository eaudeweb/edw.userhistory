from itertools import chain

from persistent.list import PersistentList
from zope.component import getUtilitiesFor, getMultiAdapter
from zope.annotation.interfaces import IAnnotations

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner, aq_parent, aq_base
from AccessControl import Unauthorized
from zExceptions import Forbidden

from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.ATContentTypes.utils import DT2dt


class UserListHistoryView(BrowserView):
    template = ViewPageTemplateFile('templates/userlisthistory.pt')

    def __call__(self):
        return self.template()

    def getMemberList(self):
        return get_member_list(self.context)

def get_member_list(context):
    membership_tool = getToolByName(context, 'portal_membership')
    for member in membership_tool.listMembers():
        member_history = IAnnotations(member).get('login_history', None)
        date, ip = DT2dt(member.getProperty('login_time')), None
        if member_history:
            date = member_history[-1]['date']
            ip = member_history[-1]['ip']
        yield dict(member=member, date=date, ip=ip)
