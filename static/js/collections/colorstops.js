define([
        'underscore',
        'backbone',
        'backboneLocalStorage',
        'app',
        'models/colorstopmod'
], function(_, Backbone, Store, app, ColorStopMod) {
    'use strict';

    // ColorStops Collection
    // ---------------

    app.ColorStopsColl = Backbone.Collection.extend({

        // Reference to this collection's model.
        model: app.colorStop,

        // Save all of the items under the given namespace.
        //localStorage: new Store('colorstops-backbone'),

        // We keep the color stops in sequential order, despite being saved by unordered
        // GUID in the database. This generates the next order number for new items.
        nextOrder: function() {
            if ( !this.length ) {
                return 1;
            }
            return this.last().get('order') + 1;
        },

        // Todos are sorted by their original insertion order.
        comparator: function( colorStop ) {
            return colorStop.get('order');
        },
        
        saveColor: function(id, color) {
            this.forEach(function (model) {
                if (model.get("order") === id)
                {
                    model.save('color', color);
                }
            });
        }
    });

    // Create our global collection of **ColorStop models**.
    app.ColorStops = new app.ColorStopsColl();
    
    // add the default stops - black to white with an unused stop in the middle
    var color = new ColorStopMod();
    color.set("color", "#000000");
    color.set("optional", false);
    color.set("useStop", true);
    color.set("stop", 0);
    color.set("order", app.ColorStops.nextOrder());
    app.ColorStops.add(color);
    color = new ColorStopMod();
    color.set("color", "#ffffff");
    color.set("optional", false);
    color.set("useStop", true);
    color.set("stop", 255);
    color.set("order", app.ColorStops.nextOrder());
    app.ColorStops.add(color);
    color = new ColorStopMod();
    color.set("optional", true);
    color.set("useColor", false);
    color.set("order", app.ColorStops.nextOrder());
    app.ColorStops.add(color);

    return app.ColorStops;

});
