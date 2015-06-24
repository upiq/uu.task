import json

from Products.Five.browser import BrowserView
from plone.app.widgets.base import InputWidget
from plone.app.widgets.dx import BaseWidget
from plone.app.widgets.dx import DatetimeWidget
from uu.task.behaviors import IAssignedTask
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
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


class IJSONWidget(ITextWidget):
    """Marker interface for the JSONWidget."""


class JSONWidgetConverter(BaseDataConverter):
    """Data converter for ICollection and IText."""

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: Query string.
        :type value: list

        :returns: Query string converted to JSON.
        :rtype: string
        """
        if not value:
            return ''
        return json.dumps(value)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Query string.
        :type value: string

        :returns: Query string.
        :rtype: list
        """
        try:
            value = json.loads(value)
        except ValueError:
            value = None
        if not value:
            return self.field.missing_value
        return value


class JSONWidget(BaseWidget, TextWidget):
    """
    """

    implementsOnly(IJSONWidget)

    _base = InputWidget

    pattern = None
    pattern_options = BaseWidget.pattern_options.copy()


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
