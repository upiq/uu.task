from .interfaces import ITask
from .interfaces import ITaskPlanner
from plone.dexterity.browser import add 
from plone.dexterity.browser import edit 
from plone.supermodel import model
from zope.interface import implementer


class TaskAddForm(add.DefaultAddForm):
    """Custom add form for ``UU Task`` content type
    """


class TaskEditForm(edit.DefaultEditForm):
    """Custom edit form for ``UU Task`` content type
    """


class TaskPlannerAddForm(add.DefaultAddForm):
    """Custom add form for ``UU Task Planner`` content type
    """


class TaskPlannerEditForm(edit.DefaultEditForm):
    """Custom edit form for ``UU Task Planner`` content type
    """


@implementer(ITask)
class Task(model.Schema):
    """Convenience subclass for ``UU Task`` content type
    """


@implementer(ITaskPlanner)
class TaskPlanner(model.Schema):
    """Convenience subclass for ``UU Task Planner`` content type
    """
