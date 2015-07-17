import pytz

from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from zope.i18nmessageid import MessageFactory


PKGNAME = 'uu.task'

_ = MessageFactory(PKGNAME)

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


def get_value(value, items):
    for item in items:
        if value == item[0]:
            return item


def get_due_date(context):
    _type = context.due.get('type')
    _value = context.due.get('value')

    if _type == 'date':
        return parse_datetime(_value)

    elif _type == 'computed':
        # TODO: temporary since we dont have start/end field
        #field4 = context.get(get_value(_value['field4'], SOURCE_DATE))
        field4 = datetime.now()
        field3 = get_value(_value['field3'], TIME_RELATIONS)[2]
        field2 = get_value(_value['field2'], TIME_UNITS)[2]
        field1 = int(_value['field1'])

        if field3 is None:
            return field4
        else:
            return field4 + field2(field3 * field1)

    elif _type == 'computed_dow':
        # TODO: temporary since we dont have start/end field
        #field4 = getattr(context, get_value(_value['field4'], SOURCE_DATE))
        field4 = datetime.now()
        field3 = get_value(_value['field3'], TIME_RELATIONS)[2]
        field2 = get_value(_value['field2'], DAYS_OF_WEEK)[2]
        field1 = int(_value['field1'])

        if field3 is None:
            return field4
        else:
            return field4 + field2(field3 * field1)


def parse_datetime(value, tz=None, missing_value=None):
    if not value:
        return missing_value

    tmp = value.split(' ')
    if not tmp[0]:
        return missing_value

    value = tmp[0].split('-')
    if len(tmp) == 2 and ':' in tmp[1]:
        value += tmp[1].split(':')
    else:
        value += ['00', '00']

    ret = datetime(*map(int, value))
    if tz:
        tzinfo = pytz.timezone(tz)
        ret = tzinfo.localize(ret)
    return ret
