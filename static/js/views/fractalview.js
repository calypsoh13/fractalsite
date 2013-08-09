define([
        'jquery',
        'underscore',
        'backbone',
        'app',
        'models/fractalmod',
        'html5slider'
], function($, _, Backbone, app, FractalMod, html5slider) {
    'use strict';

    // The Fractal View
    // ---------------

    app.FractalView = Backbone.View.extend({

        el: '#fractal',
        
        fractalTemplate: _.template( $('#fractal-template').html() ),
        
        events: {
            'change #sizeSetting': 'editSize',
            'change #roughnessSetting': 'editRoughness',
            'change #perturbanceSetting': 'editPerturbance'
        },

        initialize: function() {
            app.FractalMod = new FractalMod();
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
            this.$el.html( this.fractalTemplate( app.FractalMod.toJSON() ) );
            return this;
        },

        // update the size
        editSize: function() {
            var value = parseInt(this.$(sizeSetting).val());

            if (!isNaN(value)) {
                var newsize = Math.pow(2, value) + 1;
                app.FractalMod.save({ sizeSetting: value });
                app.FractalMod.save({ size : newsize });
                this.$(size).text(newsize);
            } 
        },

        // update the roughness
        editRoughness: function() {
            var value = parseInt(this.$(roughnessSetting).val());

            if (!isNaN(value)) {
                var newRoughness = value / 10;
                app.FractalMod.save({ roughnessSetting: value });
                app.FractalMod.save({ roughness: newRoughness});
                this.$(roughness).text(newRoughness);
            } 
        },
        
        // update the perturbance
        editPerturbance: function() {
            var value = parseInt(this.$(perturbanceSetting).val());

            if (!isNaN(value)) {
                var newperturbance = value / 10;
                app.FractalMod.save({ perturbanceSetting: value });
                app.FractalMod.save({ perturbance: newperturbance});
                this.$(perturbance).text(newperturbance);
            } 
        }
    });
    return app.FractalView;
});
