'use strict';
define([
        'jquery',
        'underscore',
        'backbone'
], function($, _, Backbone) {
    var app = {
        eventBus: _.extend( {}, Backbone.Events)
    };

    return app;
});
