from .interfaces import ITask
from .interfaces import ITaskPlanner
from plone.supermodel import model
from zope.interface import implementer


# UU Task

@implementer(ITask)
class Task(model.Schema):
    """Assignable task with due date
    """


# UU Task Planner

@implementer(ITaskPlanner)
class TaskPlanner(model.Schema):
    """Series of tasks with shared settings
    """
