import json

from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.metaconfigure import ViewMixinForTemplates
from plone.app.widgets.base import InputWidget
from plone.app.widgets.dx import AjaxSelectWidget, BaseWidget
from uu.task import _
from uu.task import (
    TIME_UNITS, TIME_RELATIONS, SOURCE_DATE, SOURCE_NOTIFY_DATE, DAYS_OF_WEEK
)
from uu.task.behaviors import IAssignedTask
from uu.task.interfaces import ITaskPlanner
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import IAddForm, IFieldWidget, IFormLayer, ITextWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapter, adapts
from zope.interface import implementer, alsoProvides, implementsOnly, Interface
from zope.schema.interfaces import IList, IDict


def get_taskplanner(item):
    if ITaskPlanner.providedBy(item):
        return item
    elif ISiteRoot.providedBy(item):
        return None
    else:
        return get_taskplanner(item.aq_parent)


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


class IPatternWidget(ITextWidget):
    """Marker interface for the PatternWidget.
    """


class IInheritParentValue(Interface):
    """Marker interface to inherit parent value.
    """


class BasePatternWidgetDataConverter(BaseDataConverter):

    _default_widget_value = None

    def toWidgetValue(self, value):
        if not value:
            value = self._default_widget_value
        return json.dumps(value)

    def toFieldValue(self, value):
        try:
            value = json.loads(value)
        except ValueError:
            value = None
        if not value:
            return self.field.missing_value
        return value


class PatternWidgetListDataConverter(BasePatternWidgetDataConverter):
    """Data converter for IList."""

    adapts(IList, IPatternWidget)

    _default_widget_value = list()


class PatternWidgetDictDataConverter(BasePatternWidgetDataConverter):
    """Data converter for IDict."""

    adapts(IDict, IPatternWidget)

    _default_widget_value = dict()


class PatternWidget(BaseWidget, TextWidget):
    """
    """

    implementsOnly(IPatternWidget)

    _base = InputWidget

    pattern = None
    pattern_options = BaseWidget.pattern_options.copy()

    def _base_args(self):
        """Method which will calculate _base class arguments.
        """
        args = super(PatternWidget, self)._base_args()
        args['name'] = self.name
        args['value'] = self.value

        if (IAddForm.providedBy(self.form._parent) and
                self.form._parent.portal_type == 'uu.taskplanner') or \
           (not IAddForm.providedBy(self.form._parent) and
                ITaskPlanner.providedBy(self.context) and
                'pattern_options' in args):
            args['pattern_options']['date'] = False

        return args

    def render_parent(self):
        if ISiteRoot.providedBy(self.context):
            return None

        taskplanner = get_taskplanner(self.context.aq_parent)

        if not taskplanner:
            return None

        return 'Parent: %s' % getattr(taskplanner, self.field.__name__)


@adapter(getSpecification(IAssignedTask['project_manager']), IFormLayer)
@implementer(IFieldWidget)
def ProjectManagerFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = 'uu.task.UsersAndGroups'
    widget.pattern_options['allowNewItems'] = False
    alsoProvides(widget, IInheritParentValue)
    return widget


@adapter(getSpecification(IAssignedTask['assigned_to']), IFormLayer)
@implementer(IFieldWidget)
def AssignedToFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = 'uu.task.UsersAndGroups'
    widget.pattern_options['allowNewItems'] = False
    alsoProvides(widget, IInheritParentValue)
    return widget


@adapter(getSpecification(IAssignedTask['due']), IFormLayer)
@implementer(IFieldWidget)
def DueFieldWidget(field, request):
    widget = FieldWidget(field, PatternWidget(request))
    widget.pattern = 'uutask-due'
    widget.pattern_options = dict()
    widget.pattern_options['date'] = dict()
    widget.pattern_options['computed'] = dict(
        field2=[i[:2] for i in TIME_UNITS],
        field3=[i[:2] for i in TIME_RELATIONS],
        field4=[i[:2] for i in SOURCE_DATE],
    )
    widget.pattern_options['computed_dow'] = dict(
        field2=[i[:2] for i in DAYS_OF_WEEK],
        field3=[i[:2] for i in TIME_RELATIONS],
        field4=[i[:2] for i in SOURCE_DATE],
    )
    alsoProvides(widget, IInheritParentValue)
    return widget


@adapter(getSpecification(IAssignedTask['notification_rules']), IFormLayer)
@implementer(IFieldWidget)
def NotificationRulesFieldWidget(field, request):
    widget = FieldWidget(field, PatternWidget(request))
    widget.pattern = 'uutask-notification-rules'
    widget.pattern_options = dict()
    widget.pattern_options['rule'] = dict(
        field2=[i[:2] for i in TIME_UNITS],
        field3=[i[:2] for i in TIME_RELATIONS],
        field4=[i[:2] for i in SOURCE_NOTIFY_DATE],
    )
    widget.pattern_options['i18n'] = dict(
        add_rule=_(u"Add rule"),
        remove=_(u"Remove"),
    )
    alsoProvides(widget, IInheritParentValue)
    return widget


class RenderWidget(ViewMixinForTemplates, BrowserView):
    index = ViewPageTemplateFile('templates/widget.pt')
