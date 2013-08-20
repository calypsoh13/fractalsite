define([
        'underscore',
        'backbone_tastypie',
        'app'
], function(_, Backbone, app) {
    'use strict';

    // filter Model
    // ----------

    app.FilterMod = Backbone.Model.extend({
       
        urlRoot: "../create/",
        
        // Default attributes for the filter
        defaults: {
            fractal : "",
            X : 0,
            Y : 0,
            xSetting : 0,
            ySetting : 0,
            sigmaX : 1,
            sigmaY : 1,
            sigmaXSetting : 0,
            sigmaYSetting : 0
        }
    });
    return app.FilterMod;
});
