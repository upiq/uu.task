from zope import schema
from zope.interface import Interface


class IAssignedParties(Interface):
    """Assigned party -- principal(s) who have been assigned a task. Often a
        user who has ability, permission, and expectation to view a monthly
        form, enter data (custom view), and submit the form.
    """

    principals = schema.List(value_type=schema.Choice([]))


class IStartEnd(Interface):
    """
    Task rule dependency on start, end date is a loose coupling
    that is presumed duck-typed, as start and end may be either
    Python date or datetime objects. This dependency is only
    for calculation and not for storage of configuration
    state.

    Note: start/end for a task should have two supported
    meanings:

    (1) start, end bracker period for when task should be
    permitted.

    (2) start, end bracket some (often retrospective) period
    of time related to the task to be performed.
    """
    start = schema.Datetime()
    end = schema.Datetime()


class ITask(Interface):
    """Explicit marker interface for UU Task
    """


class ITaskPlanner(Interface):
    """Explicit marker interface for UU Task Planner
    """
