from Products.CMFPlone.utils import safe_unicode
from plone.autoform.interfaces import IFormFieldProvider
from plone.indexer import indexer
from plone.supermodel import model
from uu.task import (
    TIME_UNITS, TIME_RELATIONS, SOURCE_DATE, SOURCE_NOTIFY_DATE, DAYS_OF_WEEK,
    EMPTY_VALUE, _, parse_datetime, get_notification_dates, get_due_date,
)
from uu.task.utils import get_parent_taskplanner
from uu.task.interfaces import ITaskAccessor
from zope import schema
from zope.component import adapter, getUtility
from zope.interface import implementer, provider, Invalid
from zope.schema.interfaces import IVocabularyFactory


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
        missing_value=EMPTY_VALUE,
    )

    assigned_to = schema.Tuple(
        title=_(u"Assigned to"),
        value_type=schema.TextLine(),
        required=False,
        missing_value=EMPTY_VALUE,
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


@adapter(IAssignedTask)
@implementer(ITaskAccessor)
class TaskAccessor(object):
    """Task accessor adapter implementation for Dexterity content objects.
    """

    def __init__(self, context):
        self.context = context

    def _get_user_or_group(self, field_name, default=tuple()):
        value = getattr(self.context, field_name, EMPTY_VALUE)

        if value is EMPTY_VALUE:
            taskplanner = get_parent_taskplanner(self.context)
            if taskplanner:
                value = getattr(taskplanner, field_name, EMPTY_VALUE)

        if value is EMPTY_VALUE:
            return default

        users_groups = getUtility(
            IVocabularyFactory, name=u"uu.task.UsersAndGroups")(self.context)

        return [users_groups.getTermByToken(i).value for i in value]

    @property
    def project_manager(self):
        return self._get_user_or_group('project_manager')

    @project_manager.setter
    def project_manager(self, value):
        setattr(self.context, 'project_manager', safe_unicode(value))

    @property
    def assignee(self):
        return self._get_user_or_group('assignee')

    @assignee.setter
    def assignee(self, value):
        setattr(self.context, 'assignee', safe_unicode(value))


@indexer(IAssignedTask)
def notifications_start_indexer(context):
    return
    dates = get_notification_dates(
        IAssignedTask(context).notification_rules, context)
    dates.sort()
    return dates[0]


@indexer(IAssignedTask)
def notifications_end_indexer(context):
    return
    dates = get_notification_dates(
        IAssignedTask(context).notification_rules, context)
    dates.sort()
    return dates[-1]


@indexer(IAssignedTask)
def due_indexer(context):
    return get_due_date(IAssignedTask(context).due, context)
