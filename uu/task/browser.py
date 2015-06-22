from Products.Five.browser import BrowserView


class TaskStatus(BrowserView):
    """
    View for assigned parties to see tasks assigned and when they are due

    Views should display task status to all parties viewing content treated
    as a task
    """


class TaskExtender(BrowserView):
    """
    View for add-ons to extend their own tasks with task behavior from uu.task
    """
