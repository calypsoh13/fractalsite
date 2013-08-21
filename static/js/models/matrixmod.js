define([
        'underscore',
        'backbone_tastypie',
        'app'
], function(_, Backbone, app) {
    'use strict';

    // Matrix Model
    // ----------
    // the matrix model has a size, roughness, perturbance, server reference and image link attributes.
    app.MatrixMod = Backbone.Model.extend({
        
        url: MATRIX_API,
        
        initialize: function() {
            this.serverAttrs=['size', 'roughness', 'perturbance'];
        },

        // Default attributes for the fractal
        defaults: {
            author: "",
            matrixFile: "",
            matrixImg: "",
            size: 257,
            sizeSetting: 8,
            roughness: .5,
            roughnessSetting: 5,
            perturbance: .5,
            perturbanceSetting: 5
        },
        isNew: function() {
            return true;
        },
        save: function (attrs, options) { 
            attrs = attrs || this.toJSON();
            options = options || {};

            // If model defines serverAttrs, replace attrs with trimmed version
            if (this.serverAttrs) attrs = _.pick(attrs, this.serverAttrs);

            // Move attrs to options
            options.attrs = attrs;

            // Call super with attrs moved to options
            Backbone.Model.prototype.save.call(this, attrs, options);
        }
    });
    return app.MatrixMod;
});
