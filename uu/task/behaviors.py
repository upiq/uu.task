from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from uu.task import _
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IAssignedTask(model.Schema):
    """adds Due date and notification_rules fields
    """

    #model.fieldset(
    #    'assigned',
    #    label=_(u'Assigned'),
    #    fields=('due_date', 'due_date_rule', 'notification_rules'),
    #)

    due_date = schema.Datetime(
        title=u"Due date",
        required=False,
    )

    due_date_rule = schema.TextLine(
        title=_(u"Computed due date"),
        required=False,
    )

    notification_rules = schema.TextLine(
        title=_(u"Notification rules"),
        required=False,
    )

    # TODO: add invariant for due_date / due_date_rule
