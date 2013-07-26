var app = app || {};

$(function( $ ) {
    'use strict';

    // The Create image view
    // ---------------

    app.createView = Backbone.View.extend({

        // Instead of generating a new element, bind to the existing skeleton of
        // the App already present in the HTML.
        el: '#create',

        // Our template for the line of statistics at the bottom of the app.
        createTemplate: _.template( $('#create-template').html() ),

        // Delegated events for creating new items, and clearing completed ones.
        events: {
            'click #filterPlus': 'addFilter',
            'click #filterMinus': 'removeFilter',
            'click #filterPrevious': 'previousFilter',
            'click #filterNext': 'nextFilter',
            'click #useHeat': 'useHeat',
            'click #useGradient': 'useGradient'
        },

        // At initialization we bind to the relevant events on the `Todos`
        // collection, when items are added or changed. Kick things off by
        // loading any preexisting todos that might be saved in *localStorage*.
        initialize: function() {
            new app.fractalView();
            //this.$size = this.$('#size');
            //this.$sizeSetting = this.$('#sizeSetting');

            //this.listenTo(app.fractalMod, 'sizeSetting', this.render);
            this.render();
        },

        // Re-render the fractal.
        render: function() {
            this.$el.html( this.createTemplate( app.createMod.toJSON() ) );
            return this;
        },

        // add a filter
        addFilter: function() {
            console.log("add filter");
        },

        // remove a filter
        removeFilter: function() {
            console.log("remove filter");
        },
        
        // go to previous filter
        previousFilter: function() {
            console.log("go to previous filter");
        },
        
        // go to next filter
        nextFilter: function() {
            console.log("go to next filter");
        },
        
        useHeat: function() {
            console.log("use heat");
            app.createMod.save(
            { 
                useHeat: true,
                heatPreview : "heatPreview",
                gradientPreview : "noPreview",
                heatChecked: "checked",
                gradientChecked: "" 
            });
            this.render();
        },
        
        useGradient: function() {
            console.log("use gradient");
            app.createMod.save(
            { 
                useHeat: false,
                heatPreview : "noPreview",
                gradientPreview : "gradientPreview",
                heatChecked: "",
                gradientChecked: "checked"
            });
            this.render();
            console.log("done rendering");
            var i = 0;
            app.createMod.get('colorStops').forEach(function(color) {
                var itemName = "#color" + i;
                console.log(itemName + " " + color);
                $(itemName).spectrum({
                    color: color.color,
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
                        updateGradient();
                        }
                });
                i++;
            });
            
        }
    });
});
