from .interfaces import ITask
from .interfaces import ITaskPlanner
from plone.supermodel import model
from zope.interface import implementer


@implementer(ITask)
class Task(model.Schema):
    """Convenience subclass for ``UU Task`` portal type
    """


@implementer(ITaskPlanner)
class TaskPlanner(model.Schema):
    """Convenience subclass for ``UU Task Planner`` portal type
    """
