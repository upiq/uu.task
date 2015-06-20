from zope import schema
from zope.interface import Interface


class ITask(Interface):
    """Explicit marker interface for UU Task
    """


class ITaskPlanner(Interface):
    """Explicit marker interface for UU Task Planner
    """


class ITaskRules(Interface):
    """Computed due date
    """

    due_in = schema.Int()
    due_units = schema.Choice([])
    due_rel = schema.Choice([])
    source = schema.Choice([])
    use_dow = schema.Bool()
    dow_n = schema.Int()
    dow = schema.Choice([])
    time_due = schema.Time()
    notification_rules = schema.List()
    timezone = schema.Choice([])
