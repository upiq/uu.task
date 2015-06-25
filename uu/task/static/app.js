define('uutask-utils', [
  'jquery',
  'select2',
], function($, Base, Select2, undefined) {
  'use strict';

  return {
    appendRule: function($el, field2, field3, field4) {
      var items = {
        field1: $('<input type="text"/>')
          .css('width', '6em')
          .addClass('uutask-field-1'),
        field2: $('<select/>')
          .addClass('uutask-field-2')
          .append(
            $.map(field2, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          ),
        field3: $('<select/>')
          .addClass('uutask-field-3')
          .append(
            $.map(field3, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          ),
        field4: $('<select/>')
          .addClass('uutask-field-4')
          .append(
            $.map(field4, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          )
      };

      var wrapper = $('<ul/>');
      $el.append(wrapper..append(
        $.map(items, function(v) {
          return v.wrap($('<li/>'));
        })
      ));
      items.wrapper = wrapper;

      $('select', $el).select2({ minimumResultsForSearch: -1 });

      return items;
    }
  };

});


define('uutask-pattern-due-date-rule', [
  'jquery',
  'mockup-patterns-base',
  'uutask-utils'
], function($, Base, Utils, undefined) {
  'use strict';

  var DueDateRule = Base.extend({
    name: 'due-date-rule',
    trigger: '.pat-due-date-rule',
    defaults: {
      vocab: {
        time_units: [],
        time_relations: [],
        source_date: [],
        days_of_week: []
      },
      i18n: {
        select_relative_to_dow: "",
        time_of_day: "",
      }
    },
    init: function() {
      var self = this;

      self.$el.hide();

      self.$wrapper = $('<div>')
        .addClass('due-date-rule-wrapper')
        .insertAfter(self.$el);

      self.$rule1 = Utils.appendRule(
        self.$wrapper,
        self.options.time_units,
        self.options.time_relations,
        self.options.source_date
      );

      self.$dow = $('<div/>');
      self.$dow.append(
        $('<input type="checkbox"/>').on('click', function(e) {
          // TODO: disable/shadow self.$rule1.wrapper or self.$rule2.wrapper
        })
      );
      self.$dow.append($('<label/>').html(self.options.i18n.select_relative_to_dow));
      self.$wrapper.append(self.$dow);

      self.$rule2 = Utils.appendRule(
        self.$wrapper,
        self.options.days_of_week,
        self.options.time_relations,
        self.options.source_date
      );

      self.update();
    }
    update: function() {
      var value = JSON.parse(self.$el.val());
    }
  });

  return DueDateRule;

});


define('uutask-pattern-notification-rules', [
  'jquery',
  'mockup-patterns-base'
], function($, Base, undefined) {
  'use strict';

  var NotificationRules = Base.extend({
    name: 'notification-rules',
    trigger: '.pat-notification-rules',
    defaults: {
    },
    init: function() {
      var self = this;
      self.$el.css({background: 'blue'});
    }
  });

  return NotificationRules;

});


require([
  'jquery',
  'uutask-pattern-due-date-rule',
  'uutask-pattern-notification-rules'
], function($, DueDateRule, NotificationRules) {

  $(document).ready(function() {
  });

});
