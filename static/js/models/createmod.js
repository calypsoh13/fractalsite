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
            author : "",
            pubDate : "",
            fractalImg : "",
            title : "",
            rawFractal : ""
            
        }, 
       
    });
    
    app.CurrentFilter = 0;
    return new app.CreateMod();
});
