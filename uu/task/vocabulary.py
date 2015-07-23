import types

from Products.CMFCore.interfaces._tools import IMemberData
from Products.CMFPlone.utils import safe_unicode
from plone import api
from plone.app.vocabularies import SlicableVocabulary
from plone.app.widgets.browser.vocabulary import _permissions
from zope.interface import implements, providedBy
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


class UsersVocabulary(SlicableVocabulary):

    implements(IVocabulary)

    @classmethod
    def createTerm(cls, term):
        if isinstance(term, basestring):
            term_id = term
            term_value = api.user.get(userid=term)

        elif IMemberData in providedBy(term):
            term_id = term.getUserId()
            term_value = term

        else:
            raise Exception(u"Term is something we can not recognize as a "
                            u"user.")

        if not term_value:
            raise Exception(u"User with id '%s' does not "
                            u"exists." % term_id)

        term_title = safe_unicode(
            term_value.getProperty('fullname') or term_value.getUserName())

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

    def getTerm(self, term):
        return self.createTerm(term)

    getTermByToken = getTerm

    def __contains__(self, term):
        if isinstance(term, basestring):
            return api.user.get(userid=term) and True or False

        elif IMemberData in providedBy(term):
            return api.user.get(userid=term.getUserId()) and True or False

        return False

    def __iter__(self):
        for term in self._terms:
            yield term

    def __len__(self):
        if isinstance(self._terms, types.GeneratorType):
            return len([i for i in self._terms])
        return len(self._terms)


class UsersFactory(object):

    implements(IVocabularyFactory)

    def __call__(self, context, query=''):
        users = api.portal.get_tool(name='portal_membership')
        return UsersVocabulary.fromItems(
            [i.getUserId() for i in users.searchForMembers(fullname=query)])


_permissions['uu.task.Users'] = 'Modify portal content'
