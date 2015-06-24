from .interfaces import ITask
from .interfaces import ITaskPlanner
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.supermodel import model
from zope.interface import implementer


# UU Task

class TaskAddForm(add.DefaultAddForm):
    """Custom add form for Task
    """
    # XXX: removes all plone styles and also does not show other fieldsets then
    # default
    #template = ViewPageTemplateFile('templates/task_add.pt')


class TaskAddView(add.DefaultAddView):
    """Custom add view for Task
    """
    form = TaskAddForm


class TaskEditForm(edit.DefaultEditForm):
    """Custom edit form for Task
    """
    # XXX: removes all plone styles and also does not show other fieldsets then
    # default
    #template = ViewPageTemplateFile('templates/task_edit.pt')


@implementer(ITask)
class Task(model.Schema):
    """Assignable task with due date
    """


# UU Task Planner

class TaskPlannerAddForm(add.DefaultAddForm):
    """Custom add form for Task Planner
    """

    # XXX: taskplanner_add.pt removes all plone styles and also does not show
    # other fieldsets then default
    #template = ViewPageTemplateFile('templates/taskplanner_add.pt')


class TaskPlannerAddView(add.DefaultAddView):
    """Custom add view for Task Planner
    """
    form = TaskPlannerAddForm


class TaskPlannerEditForm(edit.DefaultEditForm):
    """Custom edit form for Task
    """
    # XXX: removes all plone styles and also does not show other fieldsets then
    # default
    #template = ViewPageTemplateFile('templates/taskplanner_edit.pt')


@implementer(ITaskPlanner)
class TaskPlanner(model.Schema):
    """Series of tasks with shared settings
    """
