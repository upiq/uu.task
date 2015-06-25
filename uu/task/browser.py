from Products.Five.browser import BrowserView
from plone.app.widgets.base import InputWidget
from plone.app.widgets.dx import BaseWidget
from plone.app.widgets.dx import DatetimeWidget
from uu.task import _
from uu.task.behaviors import IAssignedTask
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import ITextWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementsOnly


TIME_UNITS = (
    ('hours', _(u'hour(s)')),
    ('days', _(u'day(s)')),
)

TIME_RELATIONS = (
    ('after', _(u'after')),
    ('before', _(u'before')),
    ('on', _(u'on')),
)

SOURCE_DATE = (
    ('end', _(u'end date for task')),
    ('start', _(u'start date for task')),
    ('created', _(u'content creation date')),
)

SOURCE_NOTIFY_DATE = (
    [('due', _(u'due date'))] +
    list(SOURCE_DATE)
)

DAYS_OF_WEEK = (
    ('MO', _(u'Monday')),
    ('TU', _(u'Tuesday')),
    ('WE', _(u'Wednesday')),
    ('TH', _(u'Thursday')),
    ('FR', _(u'Friday')),
    ('SA', _(u'Saturday')),
    ('SU', _(u'Sunday')),
)


class TaskStatus(BrowserView):
    """
    View for assigned parties to see tasks assigned and when they are due

    Views should display task status to all parties viewing content treated
    as a task
    """


class TaskExtender(BrowserView):
    """
    View for add-ons to extend their own tasks with task behavior from uu.task
    """


class JSONWidget(BaseWidget, TextWidget):
    """
    """

    implementsOnly(ITextWidget)

    _base = InputWidget

    pattern = None
    pattern_options = BaseWidget.pattern_options.copy()

    def _base_args(self):
        """Method which will calculate _base class arguments.
        """
        args = super(JSONWidget, self)._base_args()
        args['name'] = self.name
        args['value'] = self.value
        return args


@adapter(getSpecification(IAssignedTask['due_date']), IFormLayer)
@implementer(IFieldWidget)
def DueDateFieldWidget(field, request):
    return FieldWidget(field, DatetimeWidget(request))


@adapter(getSpecification(IAssignedTask['due_date_rule']), IFormLayer)
@implementer(IFieldWidget)
def DueDateRuleFieldWidget(field, request):
    widget = JSONWidget(request)
    widget.pattern = 'due-date-rule'
    widget.pattern_options['vocab'] = dict(
        time_units=TIME_UNITS,
        time_relations=TIME_RELATIONS,
        source_date=SOURCE_DATE,
        days_of_week=DAYS_OF_WEEK,
    )
    widget.pattern_options['i18n'] = dict(
        select_relative_to_dow=_(u"Select relative to day of week"),
        time_of_day=_(u"Time of day"),
    )
    return FieldWidget(field, widget)


@adapter(getSpecification(IAssignedTask['notification_rules']), IFormLayer)
@implementer(IFieldWidget)
def NotificationRulesFieldWidget(field, request):
    widget = JSONWidget(request)
    widget.pattern = 'notification-rules'
    return FieldWidget(field, widget)
