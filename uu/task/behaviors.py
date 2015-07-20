from Products.CMFCore.utils import getToolByName
from plone.app.vocabularies import SlicableVocabulary
from plone.app.widgets.browser.vocabulary import _permissions
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from uu.task import _, parse_datetime
from uu.task import (
    TIME_UNITS, TIME_RELATIONS, SOURCE_DATE, SOURCE_NOTIFY_DATE, DAYS_OF_WEEK
)
from zope import schema
from zope.component.hooks import getSite
from zope.interface import implements
from zope.interface import provider, Invalid
from zope.schema.interfaces import IVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


def is_notification_rule(
        value,
        field2_values=[i[0] for i in TIME_UNITS],
        field3_values=[i[0] for i in TIME_RELATIONS],
        field4_values=[i[0] for i in SOURCE_NOTIFY_DATE],
        ):

    field1 = value.get('field1')
    field2 = value.get('field2')
    field3 = value.get('field3')
    field4 = value.get('field4')

    # when field3 value is "on" then dont validate field1 and field2
    if field3 == "on" and field4 in field4_values:
        return True

    if not field1 or not field2 or not field3 or not field4:
        raise Invalid(_(u"Not valid Rule."))

    try:
        int(field1)
    except:
        raise Invalid(_(u"Not valid Rule."))

    if field2 in field2_values and \
            field3 in field3_values and \
            field4 in field4_values:
        return True

    raise Invalid(_(u"Not valid Rule."))


def is_due_date(value):
    _type = value.get('type')
    _value = value.get('value')

    if not _type or not _value:
        raise Invalid(_(u"Not valid Due date."))

    if _type == 'date':
        ## TODO: respect the selected zone from the widget and just fall back
        ## to default_zone
        #default_zone = self.widget.default_timezone
        #timezone = default_zone(self.widget.context)\
        #    if safe_callable(default_zone) else default_zone
        timezone = None
        try:
            parse_datetime(_value, tz=timezone)
        except:
            raise Invalid(_(u"Not valid Due date."))
        return True

    elif _type == 'computed':
        return is_notification_rule(
            _value,
            field4_values=[i[0] for i in SOURCE_DATE])

    elif _type == 'computed_dow':
        return is_notification_rule(
            _value,
            field2_values=[i[0] for i in DAYS_OF_WEEK],
            field4_values=[i[0] for i in SOURCE_DATE])

    raise Invalid(_(u"Not valid Due date."))


@provider(IFormFieldProvider)
class IAssignedTask(model.Schema):

    model.fieldset(
        'assigned',
        label=_(u'Assign'),
        fields=(
            'project_manager',
            'assigned_to',
            'due',
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

    due = schema.Dict(
        title=u"Due date",
        required=False,
        constraint=is_due_date,
    )

    notification_rules = schema.List(
        title=_(u"Notification rules"),
        required=False,
        value_type=schema.Dict(
            constraint=is_notification_rule,
        ),
    )


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
            title = _(u'User: ') + title.decode('utf8')

        elif term_id.startswith('group-'):
            title = term_id[len('group-'):]
            groups = getToolByName(context, "portal_groups")
            group = groups.getGroupById(term_id[len('group-'):])
            if group:
                title = group.getProperty('title', None) or title
            title = _(u'Group: ') + title.decode('utf8')

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
