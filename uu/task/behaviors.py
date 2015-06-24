import json

from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from uu.task import _
from zope import schema
from zope.interface import provider, invariant, Invalid


def is_json(value):
    try:
        json.loads(value)
    except:
        raise Invalid(_(u"Not valid JSON."))
    return True


@provider(IFormFieldProvider)
class IAssignedTask(model.Schema):
    """adds Due date and notification_rules fields
    """

    model.fieldset(
        'assigned',
        label=_(u'Assigned'),
        fields=('due_date', 'due_date_rule', 'notification_rules'),
    )

    due_date = schema.Datetime(
        title=u"Due date",
        required=False,
    )

    due_date_rule = schema.TextLine(
        title=_(u"Computed due date"),
        required=False,
        constraint=is_json,
    )

    notification_rules = schema.TextLine(
        title=_(u"Notification rules"),
        required=False,
        constraint=is_json,
    )

    @invariant
    def due_date_validation(data):
        if data.due_date is not None and data.due_date_rule is not None:
            raise Invalid(_(u"'Due date' and 'Computed due date' field can "
                            u"not be provided at the same time"))
