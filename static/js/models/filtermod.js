define([
        'underscore',
        'backbone',
        'app'
], function(_, Backbone, app) {
    'use strict';

    // filter Model
    // ----------

    app.FilterMod = Backbone.Model.extend({
       
        urlRoot: "../create/",
        
        // Default attributes for the filter
        defaults: {
            X: 0,
            Y: 0,
            sigX: 1.0,
            sigY: 1.0
        }
    });
    return app.FilterMod;
});
