from Products.Five.browser import BrowserView
from datetime import datetime
from plone.app.layout.viewlets import ViewletBase

from uu.task.interfaces import ITaskAccessor
from uu.task.utils import ulocalized_time, DT


class TaskNotifications(BrowserView):
    """View that makes it possible for assignee to change notifications.
    """


class TaskStatus(ViewletBase):

    #def update(self):
    #    super(TaskStatus, self).update()

    @property
    def task(self):
        return ITaskAccessor(self.context)

    @property
    def computed_state(self):
        task = self.task
        state = task.state['id']
        if state != 'completed' and task.due and datetime.now() > task.due:
            return 'overdue'
        return state

    def formatted_date(self, item):
        DT_item = DT(item)
        return dict(
            date=ulocalized_time(
                DT_item,
                long_format=False,
                time_only=None,
                context=self.context),
            time=ulocalized_time(
                DT_item,
                long_format=False,
                time_only=True,
                context=self.context),
            iso=item.isoformat(),
            extra=datetime.now() > item and ' (past-due)' or '',
        )
