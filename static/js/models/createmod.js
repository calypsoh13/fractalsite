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
            author : "",
            pubDate : "",
            fractalImg : "",
            title : "",
            rawFractal : ""
            
        }, 
       
    });
    
    return new app.CreateMod();
});
