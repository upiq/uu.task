import pytz

from Products.CMFCore.utils import getToolByName
from datetime import datetime
from plone.event.utils import default_timezone as fallback_default_timezone
from plone.event.utils import validated_timezone
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import Invalid

from uu.task import _
from uu.task.interfaces import (
    TIME_UNITS,
    TIME_RELATIONS,
    SOURCE_DATE,
    SOURCE_NOTIFY_DATE,
    DAYS_OF_WEEK,
)


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


def validate_notifications(
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


def validate_due(value):
    _type = value.get('type')
    _value = value.get('value')

    if not _type or not _value:
        raise Invalid(_(u"Not valid Due date."))

    if _type == 'date':
        timezone = default_timezone()
        try:
            parse_datetime(_value, tz=timezone)
        except:
            raise Invalid(_(u"Not valid Due date."))
        return True

    elif _type == 'computed':
        return validate_notifications(
            _value,
            field4_values=[i[0] for i in SOURCE_DATE])

    elif _type == 'computed_dow':
        return validate_notifications(
            _value,
            field2_values=[i[0] for i in DAYS_OF_WEEK],
            field4_values=[i[0] for i in SOURCE_DATE])

    raise Invalid(_(u"Not valid Due date."))


# -- below is copy/pasted from plone.app.event --


replacement_zones = {
    'CET': 'Europe/Vienna',    # Central European Time
    'MET': 'Europe/Vienna',    # Middle European Time
    'EET': 'Europe/Helsinki',  # East European Time
    'WET': 'Europe/Lisbon',    # West European Time
}

FALLBACK_TIMEZONE = 'UTC'


def default_timezone(context=None, as_tzinfo=False):
    """Return the timezone from the portal or user.
    :param context: Optional context. If not given, the current Site is used.
    :type context: Content object
    :param as_tzinfo: Return the default timezone as tzinfo object.
    :type as_tzinfo: boolean
    :returns: Timezone identifier or tzinfo object.
    :rtype: string or tzinfo object
    """
    # TODO: test member timezone
    if not context:
        context = getSite()

    membership = getToolByName(context, 'portal_membership', None)
    if membership and not membership.isAnonymousUser():  # user not logged in
        member = membership.getAuthenticatedMember()
        member_timezone = member.getProperty('timezone', None)
        if member_timezone:
            info = pytz.timezone(member_timezone)
            return info if as_tzinfo else info.zone

    reg_key = 'plone.portal_timezone'
    registry = getUtility(IRegistry)
    portal_timezone = registry.get(reg_key, None)

    # fallback to what plone.event is doing
    if not portal_timezone:
        portal_timezone = fallback_default_timezone()

    # Change any ambiguous timezone abbreviations to their most common
    # non-ambigious timezone name.
    if portal_timezone in replacement_zones.keys():
        portal_timezone = replacement_zones[portal_timezone]
    portal_timezone = validated_timezone(portal_timezone, FALLBACK_TIMEZONE)

    if as_tzinfo:
        return pytz.timezone(portal_timezone)

    return portal_timezone
