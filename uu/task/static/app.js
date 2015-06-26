define('uutask-utils', [
  'jquery',
  'select2',
  'mockup-patterns-pickadate'
], function($, Base, Select2, PickADate, undefined) {
  'use strict';

  return {
    appendRule: function($el, options, showTime, callback) {
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

      $('select.uutask-field2', $el).select2({ minimumResultsForSearch: -1, width: 100 });
      $('select.uutask-field3', $el).select2({ minimumResultsForSearch: -1, width: 100 });
      $('select.uutask-field4', $el).select2({ minimumResultsForSearch: -1, width: 150 });
      $('.uutask-field5', $el).patternPickadate({date:false});

      $.map(items, function($el) {
        $el.on('change', function(e) {
          callback({
            field1: items.field1.val(),
            field2: items.field2.val(),
            field3: items.field3.val(),
            field4: items.field4.val()
          });
        });
      });

      items.wrapper = $wrapper;
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

      self.$rule = Utils.appendRule(self.$wrapper, self.options, true, function(data) {
        self.$el.val(JSON.stringify(data));
      });

      self.update();
    },
    extract: function() {
    },
    update: function() {
      var self = this;
      if (self.$el.val() === "") {
          self.$rule.field1.val('');
          self.$rule.field2.select2("val", self.options.rule.field2[0][0]);
          self.$rule.field3.select2("val", self.options.rule.field3[0][0]); 
          self.$rule.field4.select2("val", self.options.rule.field4[0][0]); 
      } else {
        try {
          var value = JSON.parse(self.$el.val());
          self.$rule.field1.val(value.field1);
          self.$rule.field2.select2("val", value.field2);
          self.$rule.field3.select2("val", value.field3); 
          self.$rule.field4.select2("val", value.field4); 
        } catch (error) {
        }
      }
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
          self.appendRule.call(self);
        });

      self.update();
    },
    appendRule: function(value) {
      var self = this;
      var $rule = Utils.appendRule(self.$rules, self.options, false, function() {
        var data = [];
        $('ul.uutask-rule', self.$rules).each(function(i, $ul) {
          data.push({
            field1: $('input.uutask-field1', $ul).val(),
            field2: $('select.uutask-field2', $ul).val(),
            field3: $('select.uutask-field3', $ul).val(),
            field4: $('select.uutask-field4', $ul).val()
          });
        });
        self.$el.val(JSON.stringify(data));
      });

      if (value !== undefined) {
        $rule.field1.val(value.field1);
        $rule.field2.select2("val", value.field2);
        $rule.field3.select2("val", value.field3); 
        $rule.field4.select2("val", value.field4); 
      }
      
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
    },
    update: function() {
      var self = this;
      if (self.$el.val() !== "") {
        try {
          var values = JSON.parse(self.$el.val());
          $.each(values, function(i, value) {
            self.appendRule(value)
          });
        } catch (error) {
        }
      }
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
    var id = 'formfield-form-widgets-IAssignedTask-due_date';

    var options = [
      $('form #' + id),
      $('form #' + id + '_computed'),
      $('form #' + id + '_computed_relative_to_dow')
    ];

    $.each(options, function(i, $el) {
      $input = $('<input/>')
        .prop('type', 'radio')
        .prop('name', id + '-radio')
        .on('change', function(e) {
          $.each(options, function(i, $el_) {
            if ($el === $el_) {
              $el_.removeClass('uutask-hidden');
            } else {
              $el_.addClass('uutask-hidden');
            }
          });
        });

      if ($('input', $el).first().val() !== '') {
        $input.prop("checked", true);
      } else {
        $el.addClass('uutask-hidden');
      }

      $('label', $el).first().before($input);
    });

    if ($('input[name=' + id + '-radio]:checked').size() == 0) {
      $('input[name=' + id + '-radio]:checked').first().prop("checked", true);
    }

    $('body.portaltype-uu-task form').on('submit', function() {
      $.each(options, function(i, $el) {
        if ($('input', $el).first().prop('checked') === false) {
        $($('input', $el)[1]).val('');
        }
      });
    });

  });

});
