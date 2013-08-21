define([
        'jquery',
        'underscore',
        'backbone_tastypie',
        'app',
        'models/matrixmod',
        'html5slider'
], function($, _, Backbone, app, MatrixMod, html5slider) {
    'use strict';

    // The Matrix View
    // ---------------

    app.MatrixView = Backbone.View.extend({

        el: '#contentA',
        
        matrixTemplate: _.template( $('#matrix-template').html() ),
        
        events: {
            'change #sizeSetting': 'editSize',
            'change #roughnessSetting': 'editRoughness',
            'change #perturbanceSetting': 'editPerturbance',
            'click #createFractal': 'createFractal',
            'click #showFractal': 'displayFractalImage'
        },

        initialize: function() {
            app.MatrixMod = new MatrixMod();
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
            this.$el.html( this.matrixTemplate( app.MatrixMod.toJSON() ) );
            return this;
        },

        // update the size
        editSize: function() {
            var value = parseInt(this.$(sizeSetting).val());

            if (!isNaN(value)) {
                var newsize = Math.pow(2, value) + 1;
                app.MatrixMod.set("sizeSetting", value);
                app.MatrixMod.set("size", newsize);
                this.$(size).text(newsize);
                this.clearFractal();
            } 
        },

        // update the roughness
        editRoughness: function() {
            var value = parseInt(this.$(roughnessSetting).val());

            if (!isNaN(value)) {
                var newRoughness = value / 10;
                app.MatrixMod.set("roughnessSetting", value);
                app.MatrixMod.set("roughness", newRoughness);
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
            var image = app.MatrixMod.get("rawFractImg");
            if (!image || /^\s*$/.test(image))
            {
                console.log("Setting image to blank");
                image = "";
            } 
            var url = 'url(/static/assets/' + image + ')';
            this.$("#fractalImage").css("background-image", url);
            this.$("#fractalImage").css("background-size", "100%");
        },
        
        // create the fractal
        createFractal: function() {
            var that = this;
            var model = app.MatrixMod;
            app.MatrixMod.save({
                size: app.MatrixMod.get("size"),
                roughness: app.MatrixMod.get("roughness"),
                perturbance: app.MatrixMod.get("perturbance")
            },
            {
                success: function(model, response) {
                    model.set("rawFractImg", response.rawFractImg);
                    that.displayFractalImage();
                },
                error: function(model, response) {
                    that.clearFractal();
                }
            });
        },
        
        // clear fractal preview image
        clearFractal: function() {
            app.MatrixMod.set("rawFractImg", "");
            this.$("#fractalImage").css("background-image", "none");
        }
    });
    return app.MatrixView;
});
