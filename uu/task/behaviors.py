import json

from Products.CMFCore.utils import getToolByName
from plone.app.widgets.browser.vocabulary import _permissions
from plone.app.vocabularies import SlicableVocabulary
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from uu.task import _
from zope import schema
from zope.component.hooks import getSite
from zope.interface import implements
from zope.interface import provider, invariant, Invalid
from zope.schema.interfaces import IVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


def is_json(value):
    try:
        json.loads(value)
    except:
        raise Invalid(_(u"Not valid JSON."))
    return True


@provider(IFormFieldProvider)
class IAssignedTask(model.Schema):
    """adds Due date and notification_rules fields
    """

    model.fieldset(
        'assigned',
        label=_(u'Assigned'),
        fields=(
            'project_manager',
            'assigned_to',
            'due_date',
            'due_date_computed',
            'due_date_computed_relative_to_dow',
            'notification_rules',
        ),
    )

    project_manager = schema.Tuple(
        title=_(u"Project manager"),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )

    assigned_to = schema.Tuple(
        title=_(u"Assigned to"),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )

    due_date = schema.Datetime(
        title=u"Due date",
        required=False,
    )

    due_date_computed = schema.TextLine(
        title=_(u"Computed due date"),
        required=False,
        constraint=is_json,
    )

    due_date_computed_relative_to_dow = schema.TextLine(
        title=_(u"Computed due date relative to day of week"),
        required=False,
        constraint=is_json,
    )

    notification_rules = schema.TextLine(
        title=_(u"Notification rules"),
        required=False,
        constraint=is_json,
    )

    @invariant
    def due_date_validation(data):
        value = 0
        if data.due_date is not None:
            value += 1

        if data.due_date_computed is not None:
            value += 1

        if data.due_date_computed_relative_to_dow is not None:
            value += 1

        if value > 1:
            raise Invalid(_(u"'Due date', 'Computed due date' and "
                            u"'Computed due date relative to day of week' "
                            u"field can not be provided at the same time"))


class UsersGroupsVocabulary(SlicableVocabulary):

    implements(IVocabulary)

    def __init__(self, terms, context, *interfaces):
        super(UsersGroupsVocabulary, self).__init__(terms, *interfaces)
        self._users = getToolByName(context, "acl_users")
        self._groups = getToolByName(context, "portal_groups")

    @classmethod
    def fromItems(cls, items, context, *interfaces):
        def lazy(items):
            for item in items:
                yield cls.createTerm(item, context)
        return cls(lazy(items), context, *interfaces)
    fromValues = fromItems

    @classmethod
    def createTerm(cls, term_id, context):
        if term_id.startswith('user-'):
            title = term_id[len('user-'):]
            users = getToolByName(context, "acl_users")
            user = users.getUserById(term_id[len('user-'):], None)
            if user:
                title = user.getProperty('fullname', None) or title
            title = _(u'User: ') + title

        elif term_id.startswith('group-'):
            title = term_id[len('group-'):]
            groups = getToolByName(context, "portal_groups")
            group = groups.getGroupById(term_id[len('group-'):])
            if group:
                title = group.getProperty('title', None) or title
            title = _(u'Group: ') + title

        else:
            raise Exception("Term should start with `user-` or `group-` "
                            "instead is %s" % term_id)

        return SimpleTerm(term_id, term_id, title)

    def __contains__(self, term_id):
        if term_id.startswith('user-'):
            return self._users.getUserById(term_id, None) and True or False

        elif term_id.startswith('group-'):
            return self._groups.getGroupById(term_id) and True or False

        return False

    def getTerm(self, term_id):

        if term_id.startswith('user-'):
            title = term_id[len('user-'):]
            user = self._users.getUserById(term_id[len('user-'):], None)
            if user:
                title = user.getProperty('fullname', None) or title
            title = _(u'User: ') + title

        elif term_id.startswith('group-'):
            title = term_id[len('group-'):]
            group = self._groups.getGroupById(term_id[len('group-'):])
            if group:
                title = group.getProperty('title', None) or title
            title = _(u'Group: ') + title

        else:
            raise Exception("Term should start with `user-` or `group-` "
                            "instead is %s" % term_id)

        return SimpleTerm(term_id, term_id, title)

    getTermByToken = getTerm

    def __iter__(self):
        return self._terms


class UsersGroupsVocabularyFactory(object):
    """
    """

    implements(IVocabularyFactory)

    def __call__(self, context, query=''):
        if context is None:
            context = getSite()
        users = getToolByName(context, "acl_users")
        groups = getToolByName(context, "portal_groups")
        return UsersGroupsVocabulary.fromItems(
            ['user-' + i['userid'] for i in users.searchUsers(fullname=query)] +
            ['group-' + i.id for i in groups.searchForGroups(
                title_or_name=query)], context)


_permissions['uu.task.UsersAndGroups'] = 'Modify portal content'
