var app = app || {};

(function() {
    'use strict';

    // color stop Model
    // ----------

    app.ColorStopMod = Backbone.Model.extend({
        
        url : "create.html", 
        
        // Default attributes for the color stop
        defaults: {
            color: '#777777',
            stop: 127,
            optional: true,
            useStop: false
        }
    });
    
}());