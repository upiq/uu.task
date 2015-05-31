from plone.directives import form
from zope import schema


class ITask(form.Schema):
    """
    Assignable Task With Due Date
    """
    title = schema.TextLine(title=u"Name")
