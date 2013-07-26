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
            colorStops : new Array()
            
        }
        
        
       
    });
    
    app.createMod = new app.CreateMod();
    console.log("creating colorstop collection");
    var collection = new Backbone.Collection();
    app.createMod.set("colorStops", collection);
    var color = new app.ColorStopMod();
    color.color = "#000000";
    color.optional = false;
    color.useColor = true
    color.stop = 0.0;
    collection.add(color);
    color = new app.ColorStopMod();
    color.color = "#ffffff";
    color.optional = false;
    color.useColor = true;
    color.stop = 1.0;
    collection.add(color);
    color = new app.ColorStopMod();
    color.optional = true;
    color.useColor = false;
    collection.add(color);
    console.log(app.createMod.get("colorStops").length);
}());