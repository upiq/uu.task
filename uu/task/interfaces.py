from zope import schema
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.interface import Interface

from uu.task import _

# convenience functions for static vocabularies:
mkterm = lambda value, title: SimpleTerm(value, title=title)
mkvocab = lambda s: SimpleVocabulary([mkterm(t, title) for (t, title) in s])


TIME_UNITS = mkvocab((
    ('hours', _(u'hour(s)')),
    ('days', _(u'day(s)')),
))

TEMPORAL_REL_TYPE = mkvocab((
    ('after', _(u'after')),
    ('before', _(u'before')),
    ('on', _(u'on')),
))

SOURCE_DATE = mkvocab(
    ('end', _(u'end date for task')),
    ('start', _(u'start date for task')),
    ('created', _(u'content creation date')),
)

SOURCE_NOTIFY_DATE = mkvocab(
    [('due', _(u'due date'))] +
    [(t.value, t.title) for t in SOURCE_DATE]
)


# Day of week corresponds to vocabulary from RFC5545:
DOW = mkvocab((
    ('MO', _(u'Monday')),
    ('TU', _(u'Tuesday')),
    ('WE', _(u'Wednesday')),
    ('TH', _(u'Thursday')),
    ('FR', _(u'Friday')),
    ('SA', _(u'Saturday')),
    ('SU', _(u'Sunday')),
))


class IAssignedParties(Interface):
    """Assigned party -- principal(s) who have been assigned a task. Often a
        user who has ability, permission, and expectation to view a monthly
        form, enter data (custom view), and submit the form.
    """

    principals = schema.List(value_type=schema.Choice([]))


class INotificationRule(Interface):
    """
    """

    notify_for = schema.Float()
    units = schema.Choice(
        title=_(u'time units'),
        vocabulary=TIME_UNITS,
        default='days',
        )
    notify_rel = schema.Choice(
        title=_(u'Time relationship'),
        vocabulary=TEMPORAL_REL_TYPE,
        default='before',
    )
    source = schema.Choice(
        title=_(u'Source date'),
        vocabulary=SOURCE_NOTIFY_DATE,
        default='due',
    )


class IStartEnd(Interface):
    """
    Task rule dependency on start, end date is a loose coupling
    that is presumed duck-typed, as start and end may be either
    Python date or datetime objects. This dependency is only
    for calculation and not for storage of configuration
    state.

    Note: start/end for a task should have two supported
    meanings:

    (1) start, end bracker period for when task should be
    permitted.

    (2) start, end bracket some (often retrospective) period
    of time related to the task to be performed.
    """
    start = schema.Datetime()
    end = schema.Datetime()


class ITask(Interface):
    """Explicit marker interface for UU Task
    """


class ITaskPlanner(Interface):
    """Explicit marker interface for UU Task Planner
    """


class ITaskRules(Interface):
    """Computed due date
    """

    due_in = schema.Int()
    due_units = schema.Choice(
        title=_(u'Time units due'),
        vocabulary=TIME_UNITS,
        default='hours',
        )
    due_rel = schema.Choice(
        title=_(u'Due relationship'),
        vocabulary=TEMPORAL_REL_TYPE,
        default='after',
        )
    source = schema.Choice(
        title=_(u'Source date'),
        vocabulary=SOURCE_DATE,
        )
    use_dow = schema.Bool(
        title=_(u'Select due relative to the day of the week?'),
        required=False,
        default=True,
        )
    dow_n = schema.Int()
    dow = schema.Choice(
        title=_(u'Day of week'),
        vocabulary=DOW,
        default='MO',
        )
    time_due = schema.Time()
    notification_rules = schema.List()
    timezone = schema.Choice([])
