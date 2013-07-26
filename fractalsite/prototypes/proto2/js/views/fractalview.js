var app = app || {};

$(function( $ ) {
    'use strict';

    // The Fractal
    // ---------------

    app.fractalView = Backbone.View.extend({

        // Instead of generating a new element, bind to the existing skeleton of
        // the App already present in the HTML.
        el: '#fractal',
        
        fractalTemplate: _.template( $('#fractal-template').html() ),
        
        // Delegated events for creating new items, and clearing completed ones.
        events: {
            'change #sizeSetting': 'editSize',
            'change #roughnessSetting': 'editRoughness',
            'change #perturbanceSetting': 'editPerturbance'
        },

        // At initialization we bind to the relevant events on the `Todos`
        // collection, when items are added or changed. Kick things off by
        // loading any preexisting todos that might be saved in *localStorage*.
        initialize: function() {
            this.$size = this.$('#size');
            this.$sizeSetting = this.$('#sizeSetting');
            this.$roughness = this.$('#roughness');
            this.$roughnessSetting = this.$('#roughnessSetting');
            this.$perturbance = this.$('#perturbance');
            this.$perturbanceSetting = this.$('#perturbanceSetting');

            this.render();
        },

        // Re-render the fractal.
        render: function() {
            this.$el.html( this.fractalTemplate( app.fractalMod.toJSON() ) );
            return this;
        },

        // update the size
        editSize: function() {
            var value = parseInt(this.$(sizeSetting).val());

            if ( value ) {
                var newsize = Math.pow(2, value) + 1;
                app.fractalMod.save({ sizeSetting: value });
                app.fractalMod.save({ size : newsize });
                this.$(size).text(newsize);
            } 
        },

        // update the roughness
        editRoughness: function() {
            var value = parseFloat(this.$(roughnessSetting).val());

            if ( value ) {
                var newRoughness = value / 10;
                app.fractalMod.save({ roughnessSetting: value });
                app.fractalMod.save({ roughness: newRoughness});
                this.$(roughness).text(newRoughness);
            } 
        },
        
        // update the perturbance
        editPerturbance: function() {
            var value = parseFloat(this.$(perturbanceSetting).val());

            if ( value ) {
                var newperturbance = value / 10;
                app.fractalMod.save({ perturbanceSetting: value });
                app.fractalMod.save({ perturbance: newperturbance});
                this.$(perturbance).text(newperturbance);
            } 
        }
    });
});
