define([
        'underscore',
        'backbone',
        'app'
], function(_, Backbone, App) {
    'use strict';

    // Fractal Model
    // ----------
    var app = App.app;
    // the fractal model has a size, roughness, perturbance, server reference and image link attributes.
    app.FractalMod = Backbone.Model.extend({
        
        urlRoot: "../create",

        // Default attributes for the fractal
        defaults: {
            size: 257,
            sizeSetting: 8,
            roughness: .5,
            roughnessSetting: 5,
            perturbance: .5,
            perturbanceSetting: 5,
            serverRef: "",
            fractalImage: ""
        }
    });
    return new app.FractalMod();
});
