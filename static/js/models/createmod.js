define([
        'underscore',
        'backbone',
        'app'
], function(_, Backbone, app) {
    'use strict';

    // Create Image Model
    // ----------

    app.CreateMod = Backbone.Model.extend({
        
        url : "../create/",
        
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
