var app = app || {};

(function() {
    'use strict';

    // Create Image Model
    // ----------

    app.CreateMod = Backbone.Model.extend({
        
        url : "create.html", 
        
        // Default attributes for the fractal
        defaults: {
            useHeat : true,
            currentFilter : 0,
            colorStops : 3,
            gaussFilters : []
        }, 
       
    });
    
    app.createMod = new app.CreateMod();
}());