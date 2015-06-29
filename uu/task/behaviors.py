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
        fields=(
            'project_manager',
            'assigned_to',
            'due_date',
            'due_date_computed',
            'due_date_computed_relative_to_dow',
            'notification_rules',
        ),
    )

    project_manager = schema.TextLine(
        title=_(u"Project manager"),
        required=False,
        constraint=is_json,
    )

    assigned_to = schema.TextLine(
        title=_(u"Assigned to"),
        required=False,
        constraint=is_json,
    )

    due_date = schema.Datetime(
        title=u"Due date",
        required=False,
    )

    due_date_computed = schema.TextLine(
        title=_(u"Computed due date"),
        required=False,
        constraint=is_json,
    )

    due_date_computed_relative_to_dow = schema.TextLine(
        title=_(u"Computed due date relative to day of week"),
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
        value = 0
        if data.due_date is not None:
            value += 1

        if data.due_date_computed is not None:
            value += 1

        if data.due_date_computed_relative_to_dow is not None:
            value += 1

        if value > 1:
            raise Invalid(_(u"'Due date', 'Computed due date' and "
                            u"'Computed due date relative to day of week' "
                            u"field can not be provided at the same time"))
