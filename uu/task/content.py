import json

from BTrees.OOBTree import OOBTree
from DateTime import DateTime
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone.utils import safe_callable
from Products.CMFPlone.utils import safe_unicode
from datetime import datetime
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from plone import api
from plone.app.textfield import RichText as RichTextField
from plone.app.widgets.dx import RichTextWidget
from plone.event.utils import pydt
from plone.indexer import indexer
from plone.supermodel import model
from time import mktime
from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter, getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory

from uu.task import _
from uu.task.behaviors import ITask, ITaskPlanner, ITaskCommon
from uu.task.interfaces import (
    TASK_NOTIFICATIONS_KEY,
    TASK_STATE_KEY,
    TASK_STATE_INITIAL,
    TASK_STATES,
    TASK_STATES_TRANSITIONS,
    TIME_RELATIONS,
    TIME_UNITS,
    DAYS_OF_WEEK,
    ITaskAccessor,
)
from uu.task.utils import parse_datetime


class ITaskPlannerSchema(model.Schema):
    """TaskPlanner content type schema.
    """

    model.primary('text')

    text = RichTextField(
        title=_(u'Text'),
        description=u"",
        required=False,
    )


class ITaskSchema(model.Schema):
    """Task content type schema.
    """

    model.primary('text')

    text = RichTextField(
        title=_(u'Text'),
        description=u"",
        required=False,
    )


@adapter(ITaskCommon)
@implementer(ITaskAccessor)
class TaskAccessor(object):

    def __init__(self, context):
        self.context = context

    def _get_taskplanner(self, obj):
        """Look into parent object (recursively) until TaskPlanner content type
           is found. Or until we reach Plone site root object.
        """

        if not obj:
            return None

        # we found TaskPlanner object
        elif ITaskPlanner.providedBy(obj):
            return obj

        # return None once we reach Plone site root object
        elif ISiteRoot.providedBy(obj):
            return None

        # recurse call until one of the above conditions is met
        else:
            return self._get_taskplanner(obj.__parent__)

    def _get_users(self, field_name, default=tuple()):
        value = getattr(self.context, field_name, None)

        if value is None:
            taskplanner = self._get_taskplanner(self.context)
            if taskplanner:
                value = getattr(taskplanner, field_name, None)

        if value is None:
            return default

        users = getUtility(IVocabularyFactory,
                           name=u"uu.task.Users")(self.context)

        return [users.getTermByToken(i).value for i in value]

    @property
    def project_manager(self):
        return self._get_users('project_manager')

    @project_manager.setter
    def project_manager(self, value):
        setattr(self.context, 'project_manager', safe_unicode(value))
        self.context.reindexObject()

    @property
    def assignee(self):
        return self._get_users('assignee')

    @assignee.setter
    def assignee(self, value):
        setattr(self.context, 'assignee', safe_unicode(value))
        self.context.reindexObject()

    def _get_value(self, value, items):
        for item in items:
            if value == item[0]:
                return item

    def _get_due(self, value=None):
        if value is None:
            value = getattr(self.context, 'due', None)
            if not value:
                taskplanner = self._get_taskplanner(self.context)
                if taskplanner:
                    value = getattr(taskplanner, 'due', None)

        if not value:
            return

        _type = value.get('type')
        _value = value.get('value')

        if _type == 'date':
            return parse_datetime(_value)

        elif _type == 'computed':
            field4 = getattr(self.context, _value['field4'])

            if not field4:
                return

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

            if not field4:
                return

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
        self.context.reindexObject()

    @property
    def notifications(self):
        dates = []
        rules = None

        # if assignee is asking for notifications look first if there are
        # customezed ones
        current = api.user.get_current().getId()
        annotations = self._setup_annotations()
        assignee = getattr(self.context, 'assignee', None)
        if assignee and current in assignee and \
                current in annotations[TASK_NOTIFICATIONS_KEY]:
            rules = annotations[TASK_NOTIFICATIONS_KEY][current]

        # in all other cases just return notifications
        else:
            rules = getattr(self.context, 'notifications', None)
            if not rules:
                taskplanner = self._get_taskplanner(self.context)
                if taskplanner:
                    rules = getattr(taskplanner, 'notifications', None)

        if rules:
            for rule in rules:
                if rule['field4'] == 'due':
                    field4 = self._get_due(
                        getattr(self.context, rule['field4']))
                else:
                    field4 = getattr(self.context, rule['field4'])

                if not field4:
                    continue

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

        # check that value is list
        if not isinstance(value, list):
            raise Exception("Notifcations should be list of dictionaries, "
                            "that can be dumped using json module.")

        # check that all list items are dictionaries
        for item in value:
            if not isinstance(item, dict):
                raise Exception("Notifcations should be list of dictionaries, "
                                "that can be dumped using json module.")

        # check that we can dump value using json module
        try:
            json.dumps(value)
        except:
            raise Exception("Notifcations should be list of dictionaries, "
                            "that can be dumped using json module.")

        # if assignee is storing notifications then we store to annotations
        current = api.user.get_current().getId()
        assignee = getattr(self.context, 'assignee', None)
        if assignee and current in assignee:
            annotations = self._setup_annotations()
            rules = PersistentList()
            for item in value:
                rules.append(PersistentDict(item))
            annotations[TASK_NOTIFICATIONS_KEY][current] = rules

        # otherwise we store
        else:
            setattr(self.context, 'notifications', value)

        self.context.reindexObject()

    def _timestamp(self):
        return int(mktime(datetime.now().timetuple()))

    def _setup_annotations(self):
        annotations = IAnnotations(self.context)

        if TASK_STATE_KEY not in annotations:
            annotations[TASK_STATE_KEY] = OOBTree()
            annotations[TASK_STATE_KEY][self._timestamp()] = TASK_STATE_INITIAL

        if TASK_NOTIFICATIONS_KEY not in annotations:
            annotations[TASK_NOTIFICATIONS_KEY] = OOBTree()

        return annotations
    
    @property
    def state(self):
        annotations = self._setup_annotations()
        if len(annotations[TASK_STATE_KEY].keys()) == 0:
            return None
        return annotations[TASK_STATE_KEY][
            sorted(annotations[TASK_STATE_KEY].keys())[-1]]

    @state.setter
    def state(self, value):
        if value not in TASK_STATES.keys():
            raise Exception("State must be one of %s, but it is '%s'" % (
                TASK_STATES, value))
        annotations = self._setup_annotations()
        annotations[TASK_STATE_KEY][self._timestamp()] = value
        self.context.reindexObject()

    @property
    def state_transitions(self):
        return TASK_STATES_TRANSITIONS[self.state]

    @property
    def state_title(self):
        return TASK_STATES[self.state] or self.state


@indexer(ITask)
def index_start(context):
    return ITaskAccessor(context).start


@indexer(ITask)
def index_end(context):
    return ITaskAccessor(context).end


@indexer(ITask)
def index_notifications_day(context):
    index = []
    for item in ITaskAccessor(context).notifications:
        index.append(int(mktime(datetime(
            item.year, item.month, item.day).timetuple())))
    return index


@indexer(ITask)
def index_notifications_hour(context):
    index = []
    for item in ITaskAccessor(context).notifications:
        index.append(int(mktime(datetime(
            item.year, item.month, item.day, item.hour).timetuple())))
    return index


@indexer(ITask)
def index_project_manager(context):
    return [i.getId() for i in ITaskAccessor(context).project_manager]


@indexer(ITask)
def index_assignee(context):
    return [i.getId() for i in ITaskAccessor(context).assignee]


@indexer(ITask)
def index_state(context):
    return ITaskAccessor(context).state


@indexer(ITask)
def index_due(context):
    return ITaskAccessor(context).due


@adapter(getSpecification(ITaskPlannerSchema['text']), IFormLayer)
@implementer(IFieldWidget)
def TaskPlannerTextFieldWidget(field, request):
    return FieldWidget(field, RichTextWidget(request))


@adapter(getSpecification(ITaskSchema['text']), IFormLayer)
@implementer(IFieldWidget)
def TaskTextFieldWidget(field, request):
    return FieldWidget(field, RichTextWidget(request))
