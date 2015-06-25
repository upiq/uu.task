define('uutask-utils', [
  'jquery',
  'select2',
  'mockup-patterns-pickadate'
], function($, Base, Select2, PickADate, undefined) {
  'use strict';

  return {
    appendRule: function($el, options, showTime) {
      var items = {
        field1: $('<input type="text"/>')
          .addClass('uutask-field1'),
        field2: $('<select/>')
          .addClass('uutask-field2')
          .append(
            $.map(options.rule.field2, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          ),
        field3: $('<select/>')
          .addClass('uutask-field3')
          .append(
            $.map(options.rule.field3, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          ),
        field4: $('<select/>')
          .addClass('uutask-field4')
          .append(
            $.map(options.rule.field4, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          )
      };

      if (showTime === true) {
        items.field5 = $('<input type="text"/>')
          .addClass('uutask-field5');
      }

      var $wrapper = $('<ul/>').addClass('uutask-rule');
      $el.append($wrapper.append(
        $.map(items, function(v) {
          return v.wrap($('<li/>')).parent();
        })
      ));
      items.wrapper = $wrapper;

      $('select.uutask-field2', $el).select2({ minimumResultsForSearch: -1, width: 100 });
      $('select.uutask-field3', $el).select2({ minimumResultsForSearch: -1, width: 100 });
      $('select.uutask-field4', $el).select2({ minimumResultsForSearch: -1, width: 150 });
      $('.uutask-field5', $el).patternPickadate({date:false});

      return items;
    }
  };

});


define('uutask-pattern-due-date-computed', [
  'jquery',
  'mockup-patterns-base',
  'uutask-utils'
], function($, Base, Utils, undefined) {
  'use strict';

  var DueDateRule = Base.extend({
    name: 'due-date-computed',
    trigger: '.pat-due-date-computed',
    defaults: {
      rule: {
        field2: [],
        field3: [],
        field4: []
      },
      i18n: {
        time_of_day: "Time of day",
      }
    },
    init: function() {
      var self = this;

      self.$el.hide();

      self.$wrapper = $('<div>')
        .addClass('due-date-computed-wrapper')
        .insertAfter(self.$el);

      self.$rule = Utils.appendRule(self.$wrapper, self.options, true);

      self.update();
    },
    extract: function() {
    },
    update: function() {
      //var value = JSON.parse(self.$el.val());
    }
  });

  return DueDateRule;

});


define('uutask-pattern-notification-rules', [
  'jquery',
  'mockup-patterns-base',
  'uutask-utils'
], function($, Base, Utils, undefined) {
  'use strict';

  var NotificationRules = Base.extend({
    name: 'notification-rules',
    trigger: '.pat-notification-rules',
    defaults: {
      rule: {
        field2: [],
        field3: [],
        field4: [],
      },
      i18n: {
        add_rule: "Add rule",
        remove: "Remove"
      }
    },
    init: function() {
      var self = this;

      self.$el.hide();

      self.$wrapper = $('<div>')
        .addClass('notification-rules-wrapper')
        .insertAfter(self.$el);

      self.$rules = $('<div>')
        .addClass('notification-rules-wrapper-inner')
        .appendTo(self.$wrapper);

      self.$addRule = $('<a href="#"/>')
        .addClass('notification-rules-add')
        .html(self.options.i18n.add_rule)
        .appendTo(self.$wrapper)
        .on('click', function(e) {
          e.stopPropagation();
          e.preventDefault();

          var $rule = Utils.appendRule(self.$rules, self.options, false);
          
          var $remove = $('<a href="#"/>')
            .addClass('notification-rules-remove')
            .html(self.options.i18n.remove)

          $remove.wrap($('<li/>'))
            .parent()
            .appendTo($rule.wrapper);

          $remove.on('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).parents('ul').remove()
          });
        });

        self.update();
    },
    extract: function() {
    },
    update: function() {
      //var value = JSON.parse(self.$el.attr('val'));
    }
  });

  return NotificationRules;

});


require([
  'jquery',
  'uutask-pattern-due-date-computed',
  'uutask-pattern-notification-rules'
], function($, DueDateRule, NotificationRules) {

  $(document).ready(function() {
    var options = [
      $('#formfield-form-widgets-IAssignedTask-due_date'),
      $('#formfield-form-widgets-IAssignedTask-due_date_computed'),
      $('#formfield-form-widgets-IAssignedTask-due_date_computed_relative_to_dow')
    ];
    $.each(options, function(i, $el) {
      $input = $('<input/>')
        .prop('type', 'radio')
        .prop('name', 'formfield-form-widgets-IAssignedTask-due_date-radio')
        .on('change', function(e) {
          $.each(options, function(i, $el_) {
            if ($el === $el_) {
              $('.pattern-pickadate-wrapper', $el_).show();
              $('.due-date-computed-wrapper', $el_).show();
            } else {
              $('.pattern-pickadate-wrapper', $el_).hide();
              $('.due-date-computed-wrapper', $el_).hide();
            }
          });
        });

      if (i == 0) {
        $input.prop("checked", true);
      } else {
        $('.pattern-pickadate-wrapper', $el).hide();
        $('.due-date-computed-wrapper', $el).hide();
      }

      $('label', $el).first().before($input);
    });
  });

});
