define([
        'jquery',
        'underscore',
        'backbone_tastypie',
        'app',
        'models/matrixmod',
        'html5slider',
        'text!templates/create/matrixtemplate.html'
], function($, _, Backbone, app, MatrixMod, html5slider, matrixTemplate) {
    'use strict';

    // The Matrix View
    // ---------------

    app.CreateMatrixView = Backbone.View.extend({

        el: '#matrixdiv',
        
        events: {
            'change #sizeSetting': 'editSize',
            'change #roughnessSetting': 'editRoughness',
            'change #perturbanceSetting': 'editPerturbance',
            'click #createMatrix': 'createMatrix'
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

        // Render the matrix inputs.
        render: function() {
            var compiledTemplate = _.template( matrixTemplate, app.MatrixMod.toJSON() );
            this.$el.html(compiledTemplate);
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
                this.clearMatrixImage();
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
                this.clearMatrixImage();
            } 
        },
        
        // update the perturbance
        editPerturbance: function() {
            var value = parseInt(this.$(perturbanceSetting).val());

            if (!isNaN(value)) {
                var newperturbance = value / 10;
                app.MatrixMod.set("perturbanceSetting", value);
                app.MatrixMod.set("perturbance", newperturbance);
                this.$(perturbance).text(newperturbance);
                this.clearMatrixImage();
            } 
        },
        
        // displays the matrix image if it is stored in the matrix model
        displayMatrixImage: function() {
            var image = app.MatrixMod.get("matrixImg");
            if (!image || /^\s*$/.test(image))
            {
                console.log("Setting image to blank");
                image = "";
            } 
            var url = 'url(/static/assets/' + image + ')';
            this.$("#matrixImage").css("background-image", url);
            this.$("#matrixImage").css("background-size", "100%");
        },
        
        // create the matrix
        createMatrix: function() {
            console.log("createMatrix");
            var that = this;
            var model = app.MatrixMod;
            console.log("size", model.get("size"));
            console.log("roughness", model.get("roughness"));
            console.log("perturbance", model.get("perturbance"));
            app.MatrixMod.save({
                size: model.get("size"),
                sizeSetting: model.get("sizeSetting"),
                roughness: model.get("roughness"),
                roughnessSetting: model.get("roughnessSetting"),
                perturbance: model.get("perturbance"),
                perturbanceSetting: model.get("perturbanceSetting")
            },
            {
                success: function(model, response) {
                    console.log("success!");
                    model.set("matrixImg", response.matrixImg);
                    that.displayMatrixImage();
                },
                error: function(model, response) {
                    console.log("error");
                    that.clearMatrixImage();
                }
            });
        },
        
        // clear matrix preview image
        clearMatrixImage: function() {
            app.MatrixMod.set("matrixImg", "");
            this.$("#matrixImage").css("background-image", "none");
        }
    });
    return app.CreateMatrixView;
});
