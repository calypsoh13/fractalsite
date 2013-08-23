define([
        'jquery',
        'underscore',
        'backbone_tastypie',
        'spectrum',
        'app',
        'text!templates/colorstoptemplate.html'
], function($, _, Backbone, spectrum, app, colorStopTemplate) {
    'use strict';

    // ColorStop View
    // --------------

    app.ColorStopView = Backbone.View.extend({

        tagName:  'tr',

        events: {
            'change .useStop': 'editCheckbox',
            'change .colorStop': 'editColorStop' 
        },

        initialize: function() {
            this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function() {
            var compiledTemplate = _.template( colorStopTemplate, app.FractalMod.toJSON() );
            this.$el.html(compiledTemplate);
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
                    app.ColorStops.setColor(id, c.toRgbString());
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
            this.model.set("useStop", useStop);
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
            this.model.set("stop", stop);
        }
    });
    return app.ColorStopView;
});


