define([
        'backbone_tastypie',
        'app'
], function(Backbone, app) {
    'use strict';

    // Fractal Image Model
    // ----------

    app.FractalMod = Backbone.Model.extend({
        
        urlRoot: '../create',

        // Default attributes for the fractal
        defaults: {
            author : "",
            pubDate : "",
            fractalImg : "",
            title : "",
            rawFractal : "", 
            useHeat : true, 
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
    app.CurrentFilter = 0;
    return new app.FractalMod();
});
