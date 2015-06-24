define("uutask-pattern-duedate-rule", [
  'jquery',
  'mockup-patterns-base'
], function($, Base, undefined) {
  'use strict';

  var DueDateRule = Base.extend({
    name: 'duedate-rule',
    trigger: '.pat-duedate-rule',
    defaults: {
    },
    init: function() {
      var self = this;
      self.$el.css({background: 'green'});
    }
  });

  return DueDateRule;

});


define("uutask-pattern-duedate-notificationrules", [
  'jquery',
  'mockup-patterns-base'
], function($, Base, undefined) {
  'use strict';

  var DueDateNotificationRules = Base.extend({
    name: 'duedate-notificationrules',
    trigger: '.pat-duedate-notificationrules',
    defaults: {
    },
    init: function() {
      var self = this;
      self.$el.css({background: 'blue'});
    }
  });

  return DueDateNotificationRules;

});


require([
  'jquery',
  'uutask-pattern-duedate-rule',
  'uutask-pattern-duedate-notificationrulesrule'
], function($, DueDateRule, DueDateNotificationRules) {

  $(document).ready(function() {
  });

});
