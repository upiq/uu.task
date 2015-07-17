from zope.i18nmessageid import MessageFactory


PKGNAME = 'uu.task'

_ = MessageFactory(PKGNAME)

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
