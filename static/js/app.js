'use strict';
define([
        'jquery',
        'underscore',
        'backbone'
], function($, _, Backbone) {
    
    new CreateView();
    
    return {
        app: _.extend({}, Backbone.Events)
    };
});
