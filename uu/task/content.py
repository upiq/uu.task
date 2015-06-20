from plone.supermodel import model
from zope import schema


class Task(model.Schema):
    """Assignable task with due date; may contain dependent tasks"""

    title = schema.TextLine(title=u"Name")


class TaskPlanner(model.Schema):
    """Task container; shared configuration for contained tasks"""

    title = schema.TextLine(title=u"Name")
