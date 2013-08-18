define([
        'underscore',
        'backbone_tastypie',
        'app'
], function(_, Backbone, app) {
    'use strict';

    // Fractal Model
    // ----------
    // the fractal model has a size, roughness, perturbance, server reference and image link attributes.
    app.FractalMod = Backbone.Model.extend({
        
        url: RAWFRAC_API,

        // Default attributes for the fractal
        defaults: {
            author: "",
            rawFractImg: "",
            rawFractFile: "",
            size: 257,
            sizeSetting: 8,
            roughness: .5,
            roughnessSetting: 5,
            perturbance: .5,
            perturbanceSetting: 5
        }
    });
    return app.FractalMod;
});
