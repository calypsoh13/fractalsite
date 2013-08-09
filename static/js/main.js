'use strict';

require.config({
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
            exports: 'spectrum',
        }
    },
    paths: {
        jquery: 'lib/jquery.min',
        underscore: 'lib/lodash.min',
        backbone: 'lib/backbone',
        backboneLocalStorage: 'lib/backbone.localStorage',
        spectrum: 'spectrum/spectrum' 
    }
});

require([
    'backbone',
    'app',
    'views/createview',
    'router'
], function(Backbone, App, CreateView, AppRouter){
    new AppRouter();
    Backbone.history.start();
    new CreateView();
});
