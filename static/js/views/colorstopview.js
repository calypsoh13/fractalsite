define([
        'jquery',
        'underscore',
        'backbone',
        'spectrum',
        'app'
], function($, _, Backbone, spectrum, app) {
    'use strict';

    // Todo Item View
    // --------------

    app.ColorStopView = Backbone.View.extend({

        tagName:  'tr',

        // Cache the template function for a single item.
        template: _.template( $('#colorstop-template').html() ),

        // The DOM events specific to an item.
        events: {
            'change .useStop': 'editCheckbox',
            'change .colorStop': 'editColorStop' 
        },

        // The TodoView listens for changes to its model, re-rendering. Since there's
        // a one-to-one correspondence between a **Todo** and a **TodoView** in this
        // app, we set a direct reference on the model for convenience.
        initialize: function() {
            this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function() {
            this.$el.html( this.template( this.model.toJSON() ) );
            this.$(".colorSelect").spectrum({
                color: this.model.get("color"),
                className: 'spectrum',
                showAlpha:true,
                showInitial:true,
                showInput:true,
                showPalette: true,
                palette: [
                    ['red', 'green', 'blue'], 
                    ['#ffff00', '#00ffff', '#ff00ff'],
                    ['black', '#777777', 'white']
                ],
                change: function(c) {
                    var id = parseInt($(this).attr("id").replace('color',''));
                    app.ColorStops.saveColor(id, c.toRgbString());
                }
            });
            return this;
        },

        // Remove the item, destroy the model from *localStorage* and delete its view.
        clear: function() {
            this.model.destroy();
        },
        
        editCheckbox: function() {
            var useStop = this.$(".useStop").is(":checked");
            this.model.save("useStop", useStop);
            if (useStop)
            {
                var color = new app.ColorStopMod();
                color.set("optional", true);
                color.set("useColor", false);
                color.set("order", app.ColorStops.nextOrder());
                app.ColorStops.add(color);
            }
            else
            {   
                if (app.ColorStops.length > 3)
                {
                    this.model.destroy();
                }
            }
        },
        
        editColorStop: function(c) {
            var stop = this.$(".colorStop").val();
            this.model.save("stop", stop);
        }
    });
    return app.ColorStopView;
});


