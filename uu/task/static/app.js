define("uutask-pattern-due-date-rule", [
  'jquery',
  'mockup-patterns-base'
], function($, Base, undefined) {
  'use strict';

  var DueDateRule = Base.extend({
    name: 'due-date-rule',
    trigger: '.pat-due-date-rule',
    defaults: {
    },
    init: function() {
      var self = this;
      self.$el.css({background: 'green'});
    }
  });

  return DueDateRule;

});


define("uutask-pattern-notification-rules", [
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
