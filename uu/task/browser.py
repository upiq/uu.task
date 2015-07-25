import json

from Products.Five.browser import BrowserView
from Products.Five.browser.metaconfigure import ViewMixinForTemplates
from Products.statusmessages.interfaces import IStatusMessage
from datetime import datetime
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.event.utils import utc
from zope.interface import Invalid

from uu.task import _
from uu.task.behaviors import ITask, ITaskPlanner
from uu.task.interfaces import (
    TASK_STATES,
    TASK_STATES_TRANSITIONS,
    TIME_UNITS,
    TIME_RELATIONS,
    SOURCE_NOTIFY_DATE,
    ITaskAccessor,
)
from uu.task.utils import ulocalized_time, DT, validate_notifications


class TaskCommon(object):

    @property
    def task(self):
        return ITaskAccessor(self.context)

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
            extra=utc(datetime.now()) > utc(item) and ' (past-due)' or '',
        )

    def has_permission(self):
        if api.user.has_permission("Modify portal content") or \
                api.user.get_current().getId() in ITask(self.context).assignee:
            return True
        return False


class TaskNotifications(BrowserView, TaskCommon):
    """View that makes it possible for assignee to change notifications.
    """

    def __init__(self, context, request):
        super(TaskNotifications, self).__init__(context, request)
        self.error = None

    def __call__(self):
        if 'form.widgets.submit' in self.request.form:
            self.save_notifications(
                self.request.form['form.widget.notifications'])
        return super(TaskNotifications, self).__call__()

    def save_notifications(self, new_notifications):
        messages = IStatusMessage(self.request)
        response = self.request.response
        task = self.task

        # are we allowed to save notificationschange task state?
        #  - current user has 'Modify portal content' permission
        #  - current user is one of assigees
        if not self.has_permission():
            messages.add(
                u"Not allowed to customize notifications.", type=u"error")

        # save notification in to context
        else:
            try:
                self.error = None
                new_notifications = json.loads(new_notifications)
                for item in new_notifications:
                    validate_notifications(item)
                task.notifications = new_notifications
                messages.add(
                    _(u"Notifications saved sucessfully."), type=u"info")
            except Invalid, e:
                self.error = e.message

        if not self.error:
            response.redirect(
                self.context.absolute_url() + '/@@task_notifications')

    def notifications_pattern(self):
        options = dict()
        options['rule'] = dict(
            field2=[i[:2] for i in TIME_UNITS],
            field3=[i[:2] for i in TIME_RELATIONS],
            field4=[i[:2] for i in SOURCE_NOTIFY_DATE],
        )
        options['i18n'] = dict(
            add_rule=_(u"Add rule"),
            remove=_(u"Remove"),
        )
        return json.dumps(options)

    def notifications_value(self):
        value = self.context.notifications
        if not value:
            taskplanner = self.task._get_taskplanner(self.context)
            if taskplanner:
                value = getattr(taskplanner, 'notifications', None)
        return json.dumps(value)


class TaskStatus(ViewletBase, TaskCommon):

    def update(self):
        super(TaskStatus, self).update()

        if 'uu.task-change-to' in self.request.form:
            self.change_task_state(self.request.form['uu.task-change-to'])

    def user_url(self, user):
        return '%s/author/%s' % (
            api.portal.get().absolute_url(),
            user.getUserName())

    @property
    def computed_state(self):
        task = self.task
        state = task.state
        if state != 'completed' and task.due and \
                utc(datetime.now()) > utc(task.due):
            return 'overdue'
        return dict(id=state, title=TASK_STATES[state])

    def change_task_state(self, new_state):
        messages = IStatusMessage(self.request)
        response = self.request.response
        task = self.task
        state = task.state

        # are we allowed to change task state?
        #  - current user has 'Modify portal content' permission
        #  - current user is one of assigees
        if not self.has_permission():
            messages.add(u"Not allowed to change task state.", type=u"error")

        # is transition to new_state allowed?
        elif new_state not in [i[0] for i in TASK_STATES_TRANSITIONS[state]]:
            messages.add(u"Transition to '%s' state now allowed." % new_state,
                         type=u"error")

        # only allow to advance from created state to inprogress state if all
        # fields are set
        elif state == 'created' and new_state == 'inprogress' and (
                not task.due or not task.project_manager or not task.assignee):
            messages.add(u"Transition to '%s' state now allowed due to "
                         u"missing entry in on of the fields: Due, "
                         u"Project manager, Assignee." % new_state,
                         type=u"error")

        # store new_state
        else:
            task.state = new_state
            messages.add(_(u"Task workflow changed sucessfully."), type=u"info")

        response.redirect(self.context.absolute_url())


class TaskWidget(ViewMixinForTemplates, BrowserView):
    """
    """

    @property
    def task(self):
        return ITaskAccessor(self.context.context)

    def formatted_date(self, item):
        DT_item = DT(item)
        return '%s %s' % (
            ulocalized_time(
                DT_item,
                long_format=False,
                time_only=None,
                context=self.context.context),
            ulocalized_time(
                DT_item,
                long_format=False,
                time_only=True,
                context=self.context.context),
        )

    def inherited(self, field_name):
        if not ITask.providedBy(self.context.context):
            return None

        value = getattr(self.task, field_name, None)
        if value:
            if field_name in ['project_manager', 'assignee']:
                return ', '.join([
                    item.getProperty('fullname') for item in value])
                
            elif field_name == 'due':
                return self.formatted_date(value)

            elif field_name == 'notifications':
                return ', '.join([
                    self.formatted_date(item) for item in value])


class TaskSendNotifications(BrowserView, TaskCommon):
    """
    """

    def __init__(self, context, request):
        super(TaskSendNotifications, self).__init__(context, request)
