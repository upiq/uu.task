import types

from Products.CMFCore.interfaces._tools import IMemberData
from Products.CMFPlone.utils import safe_unicode
from Products.PlonePAS.interfaces.group import IGroupData
from plone import api
from plone.app.vocabularies import SlicableVocabulary
from plone.app.widgets.browser.vocabulary import _permissions
from uu.task import _
from zope.interface import implements, providedBy
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


class UsersGroupsVocabulary(SlicableVocabulary):

    implements(IVocabulary)

    @classmethod
    def createTerm(cls, term):
        if isinstance(term, basestring):
            term_id = term
            if term.startswith('user-'):
                username = term_id[len('user-'):]
                term_value = api.user.get(username=username)
                if not term_value:
                    raise Exception(u"User with username '%s' does not "
                                    u"exists." % username)
                term_title = term_value.getProperty('fullname') or username
                term_title = _(u'User: ') + safe_unicode(term_title)

            elif term_id.startswith('group-'):
                groupname = term_id[len('group-'):]
                term_value = api.group.get(groupname=groupname)
                if not term_value:
                    raise Exception(u"Group with groupname '%s' does not "
                                    u"exists." % groupname)
                term_title = term_value.getProperty('title') or groupname
                term_title = _(u'Group: ') + safe_unicode(term_title)

            else:
                raise Exception(u"Term should start with `user-` or `group-` "
                                u"instead is '%s'." % term_id)

        elif IMemberData in providedBy(term):
            term_id = 'user-' + term.getUserName()
            term_title = term.getProperty('fullname')
            term_title = _(u'User: ') + safe_unicode(term_title)
            term_value = term

        elif IGroupData in providedBy(term):
            term_id = 'group-' + term.getGroupName()
            term_title = term.getProperty('title')
            term_title = _(u'Group: ') + safe_unicode(term_title)
            term_value = term

        else:
            raise Exception(u"Term is something we can not recognize as a "
                            u"user or group.")

        return SimpleTerm(term_value, term_id, term_title)

    @classmethod
    def fromItems(cls, items, *interfaces):
        def lazy(items):
            terms = []
            for item in items:
                term = cls.createTerm(item)
                terms.append(term)
                yield term
            self._terms = terms
        self = cls(lazy(items), *interfaces)
        return self

    fromValues = fromItems

    def getTerm(self, term_id):
        return self.createTerm(term_id)

    getTermByToken = getTerm

    def __contains__(self, term):
        if isinstance(term, basestring):
            if term.startswith('user-'):
                return api.user.get(
                    username=term[len('user-'):]) and True or False

            elif term.startswith('group-'):
                return api.group.get(
                    groupname=term[len('group-'):]) and True or False

        elif IMemberData in providedBy(term):
            return api.user.get(
                username=term.getUserName()) and True or False

        elif IGroupData in providedBy(term):
            return api.group.get(
                groupname=term.getGroupName()) and True or False

        return False

    def __iter__(self):
        for term in self._terms:
            yield term

    def __len__(self):
        if isinstance(self._terms, types.GeneratorType):
            return len([i for i in self._terms])
        return len(self._terms)


class UsersGroupsVocabularyFactory(object):

    implements(IVocabularyFactory)

    def __call__(self, context, query=''):
        users = api.portal.get_tool(name='portal_membership')
        groups = api.portal.get_tool(name='portal_groups')
        return UsersGroupsVocabulary.fromItems(
            ['user-' + i.getUserName() for i in users.searchForMembers(
                fullname=query)] +
            ['group-' + i.id for i in groups.searchForGroups(
                title_or_name=query)])


_permissions['uu.task.UsersAndGroups'] = 'Modify portal content'
