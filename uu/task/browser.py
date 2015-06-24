from Products.Five.browser import BrowserView
from plone.app.widgets.base import InputWidget
from plone.app.widgets.dx import BaseWidget
from plone.app.widgets.dx import DatetimeWidget
from uu.task.behaviors import IAssignedTask
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import ITextWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementsOnly


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


class JSONWidget(BaseWidget, TextWidget):
    """
    """

    implementsOnly(ITextWidget)

    _base = InputWidget

    pattern = None
    pattern_options = BaseWidget.pattern_options.copy()

    def _base_args(self):
        """Method which will calculate _base class arguments.
        """
        args = super(JSONWidget, self)._base_args()
        args['name'] = self.name
        args['value'] = self.value
        return args


@adapter(getSpecification(IAssignedTask['due_date']), IFormLayer)
@implementer(IFieldWidget)
def DueDateFieldWidget(field, request):
    return FieldWidget(field, DatetimeWidget(request))


@adapter(getSpecification(IAssignedTask['due_date_rule']), IFormLayer)
@implementer(IFieldWidget)
def DueDateRuleFieldWidget(field, request):
    widget = JSONWidget(request)
    widget.pattern = 'due-date-rule'
    return FieldWidget(field, widget)


@adapter(getSpecification(IAssignedTask['notification_rules']), IFormLayer)
@implementer(IFieldWidget)
def NotificationRulesFieldWidget(field, request):
    widget = JSONWidget(request)
    widget.pattern = 'notification-rules'
    return FieldWidget(field, widget)
