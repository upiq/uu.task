from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IAssignedTask(model.Schema):
    """Due date
    """

    due_on = schema.Datetime(title=u"Due Date", required=False)
