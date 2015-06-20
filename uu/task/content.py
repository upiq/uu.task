from plone.supermodel import model
from zope import schema


class UUTask(model.Schema):
    """Assignable task with due date; may contain dependent tasks"""

    title = schema.TextLine(title=u"Name")


class UUTaskPlanner(model.Schema):
    """Task container; shared configuration for contained tasks"""

    title = schema.TextLine(title=u"Name")
