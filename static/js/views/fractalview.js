define([
        'jquery',
        'underscore',
        'backbone_tastypie',
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
            'change #perturbanceSetting': 'editPerturbance',
            'click #createFractal' : 'createFractal'
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
                app.FractalMod.set("sizeSetting", value);
                app.FractalMod.set("size", newsize);
                this.$(size).text(newsize);
                this.clearFractal();
            } 
        },

        // update the roughness
        editRoughness: function() {
            var value = parseInt(this.$(roughnessSetting).val());

            if (!isNaN(value)) {
                var newRoughness = value / 10;
                app.FractalMod.set("roughnessSetting", value);
                app.FractalMod.set("roughness", newRoughness);
                this.$(roughness).text(newRoughness);
                this.clearFractal();
            } 
        },
        
        // update the perturbance
        editPerturbance: function() {
            var value = parseInt(this.$(perturbanceSetting).val());

            if (!isNaN(value)) {
                var newperturbance = value / 10;
                app.FractalMod.set("perturbanceSetting", value);
                app.FractalMod.set("perturbance", newperturbance);
                this.$(perturbance).text(newperturbance);
                this.clearFractal();
            } 
        },
        
        // displays the fractal image if it is stored in the fractal model
        displayFractalImage: function() {
            var image = app.FractalMod.get("rawFractalImg");
            if (!image || /^\s*$/.test(image))
            {
                console.log("Setting image to blank");
                image = "";
            }
            
            this.$("#fractalImage").css("background-image", 'url(' + image + ')');
            this.$("#fractalImage").css("background-size", "100%");
        },
        
        // create the fractal
        // FOR TESTING: This just shows an example image
        createFractal: function() {
            app.FractalMod.save();
            console.log("FractalMod saved: " + app.FractalMod.get("size") + " : " + app.FractalMod.get("roughness") + " : " + app.FractalMod.get("perturbance"));
            console.log("Using example image to work visibility issues");
            app.FractalMod.set("rawFractalImg", "/static/assets/img/preview.png");
            
            this.displayFractalImage();
        },
        
        // clear fractal preview image
        clearFractal: function() {
            app.FractalMod.set("rawFractalImg", "");
            app.FractalMod.set("rawFractFile", "");
            this.displayFractalImage();
        }
    });
    return app.FractalView;
});
