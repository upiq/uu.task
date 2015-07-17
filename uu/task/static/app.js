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
            $.map(options.field2, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          ),
        field3: $('<select/>')
          .addClass('uutask-field3')
          .on('change', function(e) {
              if ($(this).val() === 'on') {
                items.field1.hide();
                items.field2.prev().hide();
              } else {
                items.field1.show();
                items.field2.prev().show();
              }
            })
          .append(
            $.map(options.field3, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          ),
        field4: $('<select/>')
          .addClass('uutask-field4')
          .append(
            $.map(options.field4, function(item) {
              return $('<option/>').val(item[0]).html(item[1]);
            })
          )
      };

      var $wrapper = $('<ul/>').addClass('uutask-rule');
      $el.append($wrapper.append(
        $.map(items, function(v) {
          return v.wrap($('<li/>')).parent();
        })
      ));

      items.field2.select2({ minimumResultsForSearch: -1, width: 100 });
      items.field3.select2({ minimumResultsForSearch: -1, width: 100 });
      items.field4.select2({ minimumResultsForSearch: -1, width: 150 });

      if (showTime === true) {
        items.field5 = $('<input type="text"/>')
          .addClass('uutask-field5');
        items.field5.patternPickadate({date:false});
      }

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


define('uutask-pattern-due', [
  'jquery',
  'mockup-patterns-base',
  'uutask-utils'
], function($, Base, Utils, undefined) {
  'use strict';

  var Due = Base.extend({
    name: 'uutask-due',
    trigger: '.pat-uutask-due',
    defaults: {
      date: {
      },
      computed: {
        field2: [],
        field3: [],
        field4: []
      },
      computed_dow: {
        field2: [],
        field3: [],
        field4: []
      },
      i18n: {
        label_1: "Exact date",
        label_2: "Computed",
        label_3: "Computed (raltive to day of the week)"
      }
    },
    init: function() {
      var self = this;

      self.uid = ("0000" + (Math.random()*Math.pow(36,4) << 0).toString(36)).slice(-4)

      self.$el.hide();

      self.$wrapper = $('<ul>')
        .addClass('uutask-due-wrapper')
        .insertAfter(self.$el);

      if (self.options.date !== false) {
        self.$due_date = $('<li>').appendTo(self.$wrapper);
      }
      self.$due_date_computed = $('<li>').appendTo(self.$wrapper);
      self.$due_date_computed_dow = $('<li>').appendTo(self.$wrapper);


      $.each([
        self.$due_date,
        self.$due_date_computed,
        self.$due_date_computed_dow
      ], function(i, $el) {
        if ($el !== undefined) {
          $('<input/>')
            .prop('type', 'radio')
            .prop('name', 'uutask-due-radio-' + self.uid)
            .prop('checked', i === 0 || (i === 1 && self.options.date === false))
            .appendTo($el)
            .on('change', function(e) {
              $('> li > div', self.$wrapper).hide();
              $('> div', $el).show();
            });
          $('<label/>')
            .html(self.options.i18n['label_' + (i + 1)])
            .appendTo($el);
          $('<div/>')
            .addClass('uutask-due-widget')
            .appendTo($el);
        }
      });


      if (self.options.date !== false) {
        self.$due_date_widget = $('<input/>')
          .prop('type', 'text')
          .appendTo($('> div', self.$due_date))
          .patternPickadate(self.options.date);
        self.$due_date_widget.data('pattern-pickadate').on('updated', function(e) {
          self.$el.val(JSON.stringify({type: "date", value: $(this).val()}));
        });
      }

      self.$due_date_computed_widget = Utils.appendRule(
        $('> div', self.$due_date_computed), self.options.computed, false,
        function(data) {
          self.$el.val(JSON.stringify({type: "computed", value: data}));
        });

      self.$due_date_computed_dow_widget = Utils.appendRule(
        $('> div', self.$due_date_computed_dow), self.options.computed_dow, false,
        function(data) {
          self.$el.val(JSON.stringify({type: "computed_dow", value: data}));
        });


      self.$due_date_computed_widget.field1.val('');
      self.$due_date_computed_widget.field2.select2("val", self.options.computed.field2[0][0]);
      self.$due_date_computed_widget.field3.select2("val", self.options.computed.field3[0][0]); 
      self.$due_date_computed_widget.field4.select2("val", self.options.computed.field4[0][0]); 

      self.$due_date_computed_dow_widget.field1.val('');
      self.$due_date_computed_dow_widget.field2.select2("val", self.options.computed_dow.field2[0][0]);
      self.$due_date_computed_dow_widget.field3.select2("val", self.options.computed_dow.field3[0][0]); 
      self.$due_date_computed_dow_widget.field4.select2("val", self.options.computed_dow.field4[0][0]); 

      var value;
      try {
        value = JSON.parse(self.$el.val());
      } catch (error) {
        value = {};
      }


      if (self.options.date !== false) {
        $('> div', self.$due_date).show();
        $('> div', self.$due_date_computed).hide();
        $('> div', self.$due_date_computed_dow).hide();
      } else {
        $('> div', self.$due_date_computed).show();
        $('> div', self.$due_date_computed_dow).hide();
      }

      if (value.type === 'date') {
        var pattern = self.$due_date_widget.data('pattern-pickadate')
        pattern.$date.pickadate('picker').set(
          'select', value.value.split(' ')[0],
          { format: pattern.options.date.formatSubmit });
        pattern.$time.pickatime('picker').set(
          'select', value.value.split(' ')[1],
          { format: pattern.options.time.formatSubmit });

        $('> input', self.$due_date).prop('checked', true);

        $('> div', self.$due_date).show();
        $('> div', self.$due_date_computed).hide();
        $('> div', self.$due_date_computed_dow).hide();

      } else if (value.type === 'computed') {
        self.$due_date_computed_widget.field1.val(value.value.field1);
        self.$due_date_computed_widget.field2.select2("val", value.value.field2);
        self.$due_date_computed_widget.field3.select2("val", value.value.field3); 
        self.$due_date_computed_widget.field4.select2("val", value.value.field4);

        $('> input', self.$due_date_computed).prop('checked', true);

        $('> div', self.$due_date).hide();
        $('> div', self.$due_date_computed).show();
        $('> div', self.$due_date_computed_dow).hide();

        if (value.value.field3 === 'on') {
          self.$due_date_computed_widget.field1.hide();
          self.$due_date_computed_widget.field2.prev().hide();
        } else {
          self.$due_date_computed_widget.field1.show();
          self.$due_date_computed_widget.field2.prev().show();
        }

      } else if (value.type === 'computed_dow') {
        self.$due_date_computed_dow_widget.field1.val(value.value.field1);
        self.$due_date_computed_dow_widget.field2.select2("val", value.value.field2);
        self.$due_date_computed_dow_widget.field3.select2("val", value.value.field3); 
        self.$due_date_computed_dow_widget.field4.select2("val", value.value.field4);

        $('> input', self.$due_date_computed_dow).prop('checked', true);

        $('> div', self.$due_date).hide();
        $('> div', self.$due_date_computed).hide();
        $('> div', self.$due_date_computed_dow).show();

        if (value.value.field3 === 'on') {
          self.$due_date_computed_dow_widget.field1.hide();
          self.$due_date_computed_dow_widget.field2.prev().hide();
        } else {
          self.$due_date_computed_dow_widget.field1.show();
          self.$due_date_computed_dow_widget.field2.prev().show();
        }
      }
    }
  });

  return Due;

});


define('uutask-pattern-notification-rules', [
  'jquery',
  'mockup-patterns-base',
  'uutask-utils'
], function($, Base, Utils, undefined) {
  'use strict';

  var NotificationRules = Base.extend({
    name: 'uutask-notification-rules',
    trigger: '.pat-uutask-notification-rules',
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
    setValue: function() {
      var self = this;
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
    },
    appendRule: function(value) {
      var self = this;
      var $rule = Utils.appendRule(self.$rules, self.options.rule, false, function() {
        self.setValue.call(self);
      });

      if (value !== undefined) {
        $rule.field1.val(value.field1);
        $rule.field2.select2("val", value.field2);
        $rule.field3.select2("val", value.field3); 
        $rule.field4.select2("val", value.field4); 
      }

      if (value && value.field3 === 'on') {
        $rule.field1.hide();
        $rule.field2.prev().hide();
      } else {
        $rule.field1.show();
        $rule.field2.prev().show();
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
        self.setValue.call(self);
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
    }
  });

  return NotificationRules;

});


require([
  'jquery',
  'uutask-pattern-due',
  'uutask-pattern-notification-rules'
], function($, DueDateRule, NotificationRules) {

  //$(document).ready(function() {
  //  // nothing
  //});

});
