import json

from plone import api
from plone.app.widgets.base import InputWidget
from plone.app.widgets.dx import AjaxSelectWidget, DatetimeWidget, BaseWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import (
    IAddForm,
    IFieldWidget,
    IFormLayer,
    INPUT_MODE,
)
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope import schema
from zope.component import adapter, getUtility, adapts
from zope.interface import (
    implementer,
    implementsOnly,
    alsoProvides,
    providedBy,
    provider,
)
from zope.schema.interfaces import IVocabularyFactory, IList, IDict

from uu.task import _
from uu.task.interfaces import (
    TIME_UNITS,
    TIME_RELATIONS,
    SOURCE_DATE,
    SOURCE_NOTIFY_DATE,
    DAYS_OF_WEEK,
    ITaskAccessor,
    IInheritParentValue,
    IPatternWidget,
)
from uu.task.utils import (
    validate_due,
    validate_notifications,
    default_timezone,
)


class ITaskCommon(model.Schema):

    project_manager = schema.Tuple(
        title=_(u"Project manager"),
        value_type=schema.TextLine(),
        required=False,
    )

    assignee = schema.Tuple(
        title=_(u"Assigned to"),
        value_type=schema.TextLine(),
        required=False,
    )

    due = schema.Dict(
        title=u"Due date",
        required=False,
        constraint=validate_due,
    )

    notifications = schema.List(
        title=_(u"Notification rules"),
        required=False,
        value_type=schema.Dict(
            constraint=validate_notifications,
        ),
    )


class ITaskStartEnd(model.Schema):

    start = schema.Datetime(
        title=_(u'Task Starts'),
        required=False,
        # TODO: defaultFactory=default_start
    )

    end = schema.Datetime(
        title=_(u'TaskEnds'),
        required=False,
        # TODO: defaultFactory=default_end
    )


@provider(IFormFieldProvider)
class ITaskPlanner(ITaskCommon):
    """
    """


@provider(IFormFieldProvider)
class ITask(ITaskCommon, ITaskStartEnd):
    """
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

        if (IAddForm.providedBy(self.form) and
                self.form.portal_type == 'uu.taskplanner') or \
           (not IAddForm.providedBy(self.form) and
                ITaskPlanner.providedBy(self.context) and
                'pattern_options' in args):
            args['pattern_options']['date'] = False

        return args


@adapter(getSpecification(ITaskCommon['project_manager']), IFormLayer)
@implementer(IFieldWidget)
def ProjectManagerFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = 'uu.task.Users'
    widget.pattern_options['allowNewItems'] = False
    alsoProvides(widget, IInheritParentValue)
    return widget


@adapter(getSpecification(ITaskCommon['assignee']), IFormLayer)
@implementer(IFieldWidget)
def AssigneeFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = 'uu.task.Users'
    widget.pattern_options['allowNewItems'] = False
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
    alsoProvides(widget, IInheritParentValue)
    return widget


def set_localroles(obj, event):
    users = ITaskAccessor(obj).assignee

    # revoke roles
    for userid, roles in obj.get_local_roles():
        user = api.user.get(userid=userid)
        if user in users and 'Reader' in roles:
            api.user.revoke_roles(
                user=user,
                roles=['Reader'],
                obj=obj,
            )

    # grant roles
    for user in users:
        if user in users and 'Reader' in roles:
            continue
        api.user.grant_roles(
            user=user,
            roles=['Reader'],
            obj=obj,
        )
