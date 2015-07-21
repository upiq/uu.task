from zope.interface import Interface, Attribute
from plone.supermodel import model


class ITaskAccessor(Interface):
    """Task accessor adapter interface.
    """

    project_manager = Attribute(u"Responsible project manager(s) or group(s).")
    assignee = Attribute(u"Assign user(s) or/and group(s).")
    due = Attribute(u"Due date.")
    notifications = Attribute(u"Notifications.")


class ITask(model.Schema):
    """Assignable task with due date
    """


class ITaskPlanner(model.Schema):
    """Series of tasks with shared settings
    """
