'use strict';
define([
        'underscore',
        'backbone'
], function(_, Backbone) {
    // Provide namespace 'app' for instances of our models, views and collections.
    var app = {
        // In case we want to use this.
        eventBus: _.extend( {}, Backbone.Events)
    };

    return app;
});
