from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from datetime import datetime
from plone import api
from plone.app.layout.viewlets import ViewletBase

from uu.task import _
from uu.task.behaviors import ITask
from uu.task.interfaces import (
    TASK_STATES,
    TASK_STATES_TRANSITIONS,
    ITaskAccessor,
)
from uu.task.utils import ulocalized_time, DT


class TaskNotifications(BrowserView):
    """View that makes it possible for assignee to change notifications.
    """


class TaskStatus(ViewletBase):

    def update(self):
        super(TaskStatus, self).update()

        if 'uu.task-change-to' in self.request.form:
            self.change_task_state(self.request.form['uu.task-change-to'])

    @property
    def task(self):
        return ITaskAccessor(self.context)

    @property
    def computed_state(self):
        task = self.task
        state = task.state
        if state != 'completed' and task.due and datetime.now() > task.due:
            return 'overdue'
        return dict(id=state, title=TASK_STATES[state])

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

    def change_task_state(self, new_state):
        messages = IStatusMessage(self.request)
        response = self.request.response
        task = self.task
        state = task.state

        # are we allowed to change task state?
        #  - current user has 'Modify portal content' permission
        #  - current user is one of assigees
        if not api.user.has_permission("Modify portal content") and \
           not api.user.get_current().getId() in ITask(self.context).assignee:
            messages.add(u"Not allowed to change task state.", type=u"error")

        # is transition to new_state allowed?
        elif new_state not in [i[0] for i in TASK_STATES_TRANSITIONS[state]]:
            messages.add(u"Transition to '%s' state now allowed." % new_state,
                         type=u"error")

        # only allow to advance from created state to inprogress state if all
        # fields are set
        elif state == 'created' and new_state == 'inprogress' and \
                not task.due and not task.project_manager and \
                not task.assignee:
            messages.add(u"Transition to '%s' state now allowed due to "
                         u"missing entry in on of the fields: Due, "
                         u"Project manager, Assignee." % new_state,
                         type=u"error")

        # store new_state
        else:
            task.state = new_state
            messages.add(_(u"Task workflow changed sucessfully."), type=u"info")

        response.redirect(self.context.absolute_url())
