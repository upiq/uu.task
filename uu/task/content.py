from DateTime import DateTime
from Products.CMFPlone.utils import safe_callable
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone.utils import safe_unicode
from plone.autoform.interfaces import IFormFieldProvider
from plone.event.utils import pydt
from plone.indexer import indexer
from plone.supermodel import model
from zope import schema
from zope.component import adapter, getUtility
from zope.interface import provider, implementer
from zope.schema.interfaces import IVocabularyFactory

from uu.task import _
from uu.task.interfaces import (
    TIME_RELATIONS,
    TIME_UNITS,
    DAYS_OF_WEEK,
    ITaskAccessor,
    ITaskPlannerMarker,
    ITaskMarker,
)
from uu.task.utils import (
    validate_due,
    validate_notifications,
    parse_datetime,
)


class ITaskCommon(model.Schema):

    project_manager = schema.Tuple(
        title=_(u"Project manager"),
        value_type=schema.TextLine(),
        required=False,
    )

    assignee = schema.Tuple(
        title=_(u"Assigned to"),
        value_type=schema.TextLine(),
        required=False,
    )


@provider(IFormFieldProvider)
class ITaskPlanner(ITaskCommon):

    model.fieldset(
        'assigned',
        label=_(u'Assign'),
        fields=(
            'project_manager',
            'assignee',
        ),
    )


@provider(IFormFieldProvider)
class ITask(ITaskCommon):

    model.fieldset(
        'assigned',
        label=_(u'Assign'),
        fields=(
            'start',
            'end',
            'project_manager',
            'assignee',
            'due',
            'notifications',
        ),
    )

    start = schema.Datetime(
        title=_(u'Task Starts'),
        required=False,
        #defaultFactory=default_start
    )

    end = schema.Datetime(
        title=_(u'TaskEnds'),
        required=False,
        #defaultFactory=default_end
    )

    due = schema.Dict(
        title=u"Due date",
        required=False,
        constraint=validate_due,
    )

    notifications = schema.List(
        title=_(u"Notification rules"),
        required=False,
        value_type=schema.Dict(
            constraint=validate_notifications,
        ),
    )


@adapter(ITaskPlannerMarker)
@implementer(ITaskAccessor)
class TaskPlannerAccessor(object):

    def __init__(self, context):
        self.context = context

    def _get_taskplanner(self, obj):
        """Look into parent object (recursively) until TaskPlanner content type
           is found. Or until we reach Plone site root object.
        """

        # we found TaskPlanner object
        if ITaskPlannerMarker.providedBy(obj):
            return obj

        # return None once we reach Plone site root object
        elif ISiteRoot.providedBy(obj):
            return None

        # recurse call until one of the above conditions is met
        else:
            return self._get_taskplanner(obj.aq_parent)

    def _get_user_or_group(self, field_name, default=tuple()):
        value = getattr(self.context, field_name, None)

        if value is None:
            taskplanner = self._get_taskplanner(self.context)
            if taskplanner:
                value = getattr(taskplanner, field_name, None)

        if value is None:
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


@adapter(ITaskMarker)
@implementer(ITaskAccessor)
class TaskAccessor(TaskPlannerAccessor):

    def _get_value(self, value, items):
        for item in items:
            if value == item[0]:
                return item

    def _get_due(self, value=None):
        if value is None:
            value = getattr(self.context, 'due', None)

        _type = value.get('type')
        _value = value.get('value')

        if _type == 'date':
            return parse_datetime(_value)

        elif _type == 'computed':
            field4 = getattr(self.context, _value['field4'])
            field3 = self._get_value(_value['field3'], TIME_RELATIONS)[2]

            if safe_callable(field4):
                field4 = field4()
            if isinstance(field4, DateTime):
                field4 = pydt(field4)

            if field3 is None:
                return field4
            else:
                field2 = self._get_value(_value['field2'], TIME_UNITS)[2]
                field1 = int(_value['field1'])
                return field4 + field2(field3 * field1)

        elif _type == 'computed_dow':
            field4 = getattr(self.context, _value['field4'])
            field3 = self._get_value(_value['field3'], TIME_RELATIONS)[2]

            if safe_callable(field4):
                field4 = field4()
            if isinstance(field4, DateTime):
                field4 = pydt(field4)

            if field3 is None:
                return field4
            else:
                field2 = self._get_value(_value['field2'], DAYS_OF_WEEK)[2]
                field1 = int(_value['field1'])
                return field4 + field2(field3 * field1)

    @property
    def due(self):
        return self._get_due()

    @due.setter
    def due(self, value):
        setattr(self.context, 'due', safe_unicode(value))

    @property
    def notifications(self):
        dates = []
        rules = getattr(self.context, 'notifications', None)

        if rules:
            for rule in rules:
                if rule['field4'] == 'due':
                    field4 = self._get_due(
                        getattr(self.context, rule['field4']))
                else:
                    field4 = getattr(self.context, rule['field4'])
                field3 = self._get_value(rule['field3'], TIME_RELATIONS)[2]

                if safe_callable(field4):
                    field4 = field4()
                if isinstance(field4, DateTime):
                    field4 = pydt(field4)

                if field3 is None:
                    dates.append(field4)
                else:
                    field2 = self._get_value(rule['field2'], TIME_UNITS)[2]
                    field1 = int(rule['field1'])
                    dates.append(field4 + field2(field3 * field1))

        return dates

    @notifications.setter
    def notifications(self, value):
        setattr(self.context, 'notifications', safe_unicode(value))


@indexer(ITask)
def start_indexer(context):
    return ITaskAccessor(context).start


@indexer(ITask)
def end_indexer(context):
    return ITaskAccessor(context).end


@indexer(ITask)
def notifications_start_indexer(context):
    dates = ITaskAccessor(context).notificatios
    if len(dates) == 0 or dates is None:
        return
    dates.sort()
    return dates[0]


@indexer(ITask)
def notifications_end_indexer(context):
    dates = ITaskAccessor(context).notificatios
    if len(dates) == 0 or dates is None:
        return
    dates.sort()
    return dates[-1]


@indexer(ITask)
def due_indexer(context):
    return ITask(context).due
