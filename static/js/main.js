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
        backboneLocalstorage: {
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
], function(Backbone, App, Workspace){
    new Workspace();
    Backbone.history.start();
    App.initialize();
});
