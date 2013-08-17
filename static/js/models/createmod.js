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
            author : "",
            pubDate : "",
            fractalImg : "",
            title : "",
            rawFractal : "", 
            useHeat : true,
            
        }, 
       
    });
    
    app.CurrentFilter = 0;
    return new app.CreateMod();
});
