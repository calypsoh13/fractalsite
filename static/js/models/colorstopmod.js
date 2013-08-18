define([
        'underscore',
        'backbone_tastypie',
        'app'
], function(_, Backbone, app) {
    'use strict';

    // color stop Model
    // ----------

    app.ColorStopMod = Backbone.Model.extend({
       
        urlRoot: "../create/",
        
        // Default attributes for the color stop
        defaults: {
            fractal : "",
            color: '#777777',
            stop: 127,
            optional: true,
            useStop: false
        }
    });
    return app.ColorStopMod;
});
