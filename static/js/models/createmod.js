define([
        'backbone',
        'app'
], function(Backbone, app) {
    'use strict';

    // Create Image Model
    // ----------

    app.CreateMod = Backbone.Model.extend({
        
        urlRoot: '../create',

        // Default attributes for the fractal
        defaults: {
            useHeat : true,
            currentFilter : 0,
            colorStops : 3,
            gaussFilters : []
        }, 
       
    });
    
    return new app.CreateMod();
});
