from plone.directives import form
from zope import schema


class IUUTask(form.Schema):
    """
    Assignable Task With Due Date; Contains Dependent Tasks
    """
    title = schema.TextLine(title=u"Name")


class IUUTaskPlanner(form.Schema):
    """
    Task Container; Shared Configuration For Contained Tasks
    """
    title = schema.TextLine(title=u"Name")
