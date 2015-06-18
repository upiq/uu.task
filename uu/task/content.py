from plone.supermodel import model
from zope import schema


class IUUTask(model.Schema):
    """
    Assignable Task With Due Date; Contains Dependent Tasks
    """
    title = schema.TextLine(title=u"Name")


class IUUTaskPlanner(model.Schema):
    """
    Task Container; Shared Configuration For Contained Tasks
    """
    title = schema.TextLine(title=u"Name")
