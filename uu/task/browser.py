import json

from Products.Five.browser import BrowserView
from Products.Five.browser.metaconfigure import ViewMixinForTemplates
from plone.app.widgets.base import InputWidget
from plone.app.widgets.dx import AjaxSelectWidget, BaseWidget, DatetimeWidget
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import (
    IAddForm,
    IFieldWidget,
    IFormLayer,
    ITextWidget,
    INPUT_MODE,
)
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapter, adapts, getUtility
from zope.interface import (
    implementer,
    alsoProvides,
    implementsOnly,
    Interface,
    providedBy,
)
from zope.schema.interfaces import IList, IDict, IVocabularyFactory

from uu.task import _
from uu.task.utils import default_timezone
from uu.task.content import ITask, ITaskCommon, ITaskPlanner
from uu.task.interfaces import (
    TIME_UNITS,
    TIME_RELATIONS,
    SOURCE_DATE,
    SOURCE_NOTIFY_DATE,
    DAYS_OF_WEEK,
    ITaskAccessor,
    ITaskPlannerMarker,
)


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
                ITaskPlannerMarker.providedBy(self.context) and
                'pattern_options' in args):
            args['pattern_options']['date'] = False

        return args


def render_parent(widget):
    if widget.form.mode != INPUT_MODE:
        return

    context = widget.context
    if not IAddForm.providedBy(widget.form._parent):
        context = widget.context.aq_parent

    if ITask in providedBy(context) or ITaskPlanner in providedBy(context):
        task = ITaskAccessor(context)
        users_groups = getUtility(
            IVocabularyFactory, name=u"uu.task.UsersAndGroups")(context)
        value = getattr(task, widget.field.__name__, None)
        if value:
            return 'Parent: %s' % (', '.join(
                [i.title for i in users_groups.fromValues(value)]))


@adapter(getSpecification(ITaskCommon['project_manager']), IFormLayer)
@implementer(IFieldWidget)
def ProjectManagerFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = 'uu.task.UsersAndGroups'
    widget.pattern_options['allowNewItems'] = False
    widget.render_parent = lambda: render_parent(widget)
    alsoProvides(widget, IInheritParentValue)
    return widget


@adapter(getSpecification(ITaskCommon['assignee']), IFormLayer)
@implementer(IFieldWidget)
def AssigneeFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = 'uu.task.UsersAndGroups'
    widget.pattern_options['allowNewItems'] = False
    widget.render_parent = lambda: render_parent(widget)
    alsoProvides(widget, IInheritParentValue)
    return widget


@adapter(getSpecification(ITask['start']), IFormLayer)
@implementer(IFieldWidget)
def StartDateFieldWidget(field, request):
    widget = FieldWidget(field, DatetimeWidget(request))
    widget.default_timezone = default_timezone
    return widget


@adapter(getSpecification(ITask['end']), IFormLayer)
@implementer(IFieldWidget)
def EndDateFieldWidget(field, request):
    widget = FieldWidget(field, DatetimeWidget(request))
    widget.default_timezone = default_timezone
    return widget


@adapter(getSpecification(ITask['due']), IFormLayer)
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
    widget.render_parent = lambda: render_parent(widget)
    alsoProvides(widget, IInheritParentValue)
    return widget


@adapter(getSpecification(ITask['notifications']), IFormLayer)
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
    widget.render_parent = lambda: render_parent(widget)
    alsoProvides(widget, IInheritParentValue)
    return widget


class RenderWidget(ViewMixinForTemplates, BrowserView):
    index = ViewPageTemplateFile('templates/widget.pt')
