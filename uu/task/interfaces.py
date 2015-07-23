from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from z3c.form.interfaces import ITextWidget
from zope.interface import Interface, Attribute

from uu.task import _


TASK_STATE_KEY = "uu.task.state"

TASK_STATE_INITIAL = 'created'

TASK_STATES = dict(
    created=_(u'Created'),
    inprogress=_(u'In-progress'),
    completed=_(u'Completed'),
    discarded=_(u'Discarded'),
)

TASK_STATES_TRANSITIONS = dict(
    created=[
        ('inprogress', _(u'Start working')),
        ('discarded', _(u'Discard')),
    ],
    inprogress=[
        ('completed', _(u'Complete')),
        ('discarded', _(u'Discard')),
    ],
    completed=[
        ('created', _(u'Reopen')),
    ],
    discarded=[
        ('created', _(u'Reopen')),
    ],
)

TIME_UNITS = (
    ('hours', _(u'hour(s)'), lambda x: relativedelta(hour=x)),
    ('days', _(u'day(s)'), lambda x: relativedelta(day=x)),
)

TIME_RELATIONS = (
    ('after', _(u'after'), +1),
    ('before', _(u'before'), -1),
    ('on', _(u'on'), None),
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
    ('MO', _(u'Monday'), lambda x: relativedelta(weekday=MO(x))),
    ('TU', _(u'Tuesday'), lambda x: relativedelta(weekday=TU(x))),
    ('WE', _(u'Wednesday'), lambda x: relativedelta(weekday=WE(x))),
    ('TH', _(u'Thursday'), lambda x: relativedelta(weekday=TH(x))),
    ('FR', _(u'Friday'), lambda x: relativedelta(weekday=FR(x))),
    ('SA', _(u'Saturday'), lambda x: relativedelta(weekday=SA(x))),
    ('SU', _(u'Sunday'), lambda x: relativedelta(weekday=SU(x))),
)


class ITaskAccessor(Interface):
    """Task accessor adapter interface.
    """

    project_manager = Attribute(u"Responsible project manager(s) or group(s).")
    assignee = Attribute(u"Assign user(s) or/and group(s).")
    due = Attribute(u"Due date.")
    notifications = Attribute(u"Notifications.")


class IPatternWidget(ITextWidget):
    """Marker interface for the PatternWidget.
    """


class IInheritParentValue(Interface):
    """Marker interface to inherit parent value.
    """
