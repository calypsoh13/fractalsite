'use strict';

require.config({
    // Shim lets us use require.js with non-AMD modules-
    // Some modules must be loaded before others.
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        backboneLocalStorage: {
            deps: ['backbone'],
            exports: 'Store'
        },
        spectrum: {
            deps: ['jquery'],
            exports: 'spectrum'
        }
    },
    paths: {
        jquery: 'lib/jquery.min',
        underscore: 'lib/lodash.min', //lo-dash is an extension of underscore.
        backbone: 'lib/backbone',
        backboneLocalStorage: 'lib/backbone.localStorage',
        spectrum: 'spectrum/spectrum'
        // When we get into RESTful API, we might consider using backbone-tastypie.js 
    }
});

require([
    'backbone',
    'views/createview',
    'router'
], function(Backbone, CreateView, AppRouter){
    // Initialize router
    new AppRouter();
    // Start Backbone History
    Backbone.history.start();
    // Kick things off with CreateView. We may want to do this in the router, later.
    new CreateView();
});
