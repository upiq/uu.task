from plone.supermodel import model


class ITask(model.Schema):
    """Assignable task with due date
    """


class ITaskPlanner(model.Schema):
    """Series of tasks with shared settings
    """
