define([
        'jquery',
        'underscore',
        'backbone',
        'app',
        'views/fractalview',
        'views/colorstopview',
        'models/createmod',
        'collections/colorstops',
        'collections/filters',
        'html5slider'
], function($, _, Backbone, app, FractalView, ColorStopView, CreateMod, ColorStops, Filters, html5slider) {
    'use strict';

    // The Create image view
    // ---------------

    app.CreateView = Backbone.View.extend({

        el: '#create',

        colorViews: [],
        
        createTemplate: _.template( $('#create-template').html() ),

        events: {
            'click #filterPlus': 'addFilter',
            'click #filterMinus': 'removeFilter',
            'click #filterPrevious': 'previousFilter',
            'click #filterNext': 'nextFilter',
            'click #useHeat': 'useHeat',
            'click #useGradient': 'useGradient',
            'change #gaussXSetting' : 'editXSetting',
            'change #gaussYSetting' : 'editYSetting',
            'change #gaussSigmaXSetting' : 'editSigmaXSetting',
            'change #gaussSigmaYSetting' : 'editSigmaYSetting',
            'change #gaussX' : 'editX',
            'change #gaussY' : 'editY'
        },

        initialize: function() {
            new FractalView();
            app.ColorStops = ColorStops;
            app.Filters = Filters;
            app.CreateMod = CreateMod;
            this.listenTo(app.FractalMod, 'change', this.updateGaussForSize);
            this.listenTo(app.ColorStops, 'add', this.addAllColorStops);
            this.listenTo(app.ColorStops, 'remove', this.addAllColorStops);
            this.listenTo(app.ColorStops, 'change', this.updateGradient);
            this.render();
            // add views for the gradient stops
            if (app.CreateMod.get("useHeat"))
            {
                this.useHeat();
            }
            else
            {
                this.useGradient();
            }
        },

        // Render the create template.
        render: function() {
            this.$el.html( this.createTemplate( app.CreateMod.toJSON() ) );
            this.addAllColorStops();
            return this;
        },

        // add a filter
        addFilter: function() {
            // limit the user to 5 filters
            if (app.Filters.length > 4) return;
            var midsize = (app.FractalMod.get('size') -1) / 2 + 1;
            var filter = new app.FilterMod()
            filter.set("X", midsize);
            filter.set("Y", midsize);
            app.Filters.add(filter);
            app.CurrentFilter = app.Filters.length - 1;
            this.setGaussElements();
            this.showGaussPreview();
        },

        // remove a filter
        removeFilter: function() {
            app.Filters.remove(app.Filters.at(app.CurrentFilter));
            app.CurrentFilter = Math.max(0, Math.min(app.Filters.length-1, app.CurrentFilter));
            this.setGaussElements();
            this.showGaussPreview();
        },
        
        // go to previous filter
        previousFilter: function() {
            app.CurrentFilter--;
            if (app.CurrentFilter < 0)
            {
                app.CurrentFilter = app.Filters.length - 1;
            }
            this.setGaussElements();
            this.showGaussPreview();
        },
        
        // go to next filter
        nextFilter: function() {
            app.CurrentFilter++;
            if (app.CurrentFilter > app.Filters.length - 1)
            {
                app.CurrentFilter = 0;
            }
            this.setGaussElements();
            this.showGaussPreview();
        },
        
        editXSetting: function() {
            var value = parseInt(this.$('#gaussXSetting').val());
            
            if (!isNaN(value)) {
                var size = app.FractalMod.get('size');
                var increment = (size-1)/128;
                var offset = increment * 64;
                var gx = increment * value + offset;
                app.Filters.at(app.CurrentFilter).set("xSetting", value);
                app.Filters.at(app.CurrentFilter).set("X", gx);
                this.$('#gaussX').val(gx);
            } 
            this.showGaussPreview();
        },
        
        editYSetting: function() {
            var value = parseInt(this.$('#gaussYSetting').val());
            
            if (!isNaN(value)) {
                var size = app.FractalMod.get('size');
                var increment = (size-1)/128;
                var offset = increment * 64;
                var gy = increment * value + offset;
                app.Filters.at(app.CurrentFilter).set("ySetting", value);
                app.Filters.at(app.CurrentFilter).set("Y", gy);
                this.$('#gaussY').val(gy);
            } 
            this.showGaussPreview();
        },
        
        editSigmaXSetting: function() {
            var value = parseInt(this.$('#gaussSigmaXSetting').val());
            
            if (!isNaN(value)) {
                var sigmaX = Math.floor(Math.pow(2, value/2) * 100) / 100;
                app.Filters.at(app.CurrentFilter).set("sigmaXSetting", value);
                app.Filters.at(app.CurrentFilter).set("sigmaX", sigmaX);
                this.$('#gaussSigmaX').text(sigmaX);
            }
            this.showGaussPreview();

        },
        
        editSigmaYSetting: function() {
            var value = parseInt(this.$('#gaussSigmaYSetting').val());
            if (!isNaN(value)) {
                var sigmaY = Math.floor(Math.pow(2, value/2) * 100) / 100;
                app.Filters.at(app.CurrentFilter).set("sigmaYSetting", value);
                app.Filters.at(app.CurrentFilter).set("sigmaY", sigmaY);
                this.$('#gaussSigmaY').text(sigmaY);
            }
            this.showGaussPreview();
        },
        
        updateGaussForSize: function() {
            var size = app.FractalMod.get('size');
            
            for(var i = 0; i < app.Filters.length; i++)
            {
                var filter = app.Filters.at(i);
                var increment = (size-1)/128;
                var offset = increment * 64;
                filter.set("X", increment * filter.get("gaussXSetting") + offset);
                filter.set("Y", increment * filter.get("gaussYSetting") + offset);
            }
            
            if (app.Filters.length > 0)
            {
                this.$('#gaussX').val(app.Filters.at(app.CurrentFilter).get("X"));
                this.$('#gaussY').val(app.Filters.at(app.CurrentFilter).get("Y"));
            
                this.showGaussPreview();
            }
        },
        
        editX: function() {
            var value = parseInt(this.$('#gaussX').val());
            
            if (!isNaN(value)) {
                var size = app.FractalMod.get('size');
                var increment = (size-1)/128;
                var offset = increment * 64;
                var gxSetting = (value - offset) / increment;
                var sign = 1;
                if (gxSetting < 0) sign = -1;
                gxSetting = Math.floor(Math.abs(gxSetting)) *  sign;
                // limit the setting to -80 to 80
                if (gxSetting < -80 || gxSetting > 80)
                {
                    gxSetting = Math.max(-80, Math.min(80, gxSetting));
                    value = increment * gxSetting + offset;
                }
                app.Filters.at(app.CurrentFilter).set("xSetting", gxSetting);
                app.Filters.at(app.CurrentFilter).set("X", value);
                this.$('#gaussX').val(value);
                this.$('#gaussXSetting').val(gxSetting);
            } 
            else
            {
                value = app.Filters.at(app.CurrentFilter).get("X");
                this.$('#gaussX').val(value);
            }
            this.showGaussPreview();
        },
        
        editY: function() {
            var value = parseInt(this.$('#gaussY').val());
            
            if (!isNaN(value) ) {
                var size = app.FractalMod.get('size');
                var increment = (size-1)/128;
                var offset = increment * 64;
                var gySetting = (value - offset) / increment;
                var sign = 1;
                if (gySetting < 0) sign = -1;
                gySetting = Math.floor(Math.abs(gySetting)) *  sign;
                // limit the setting to -80 to 80
                if (gySetting < -80 || gySetting > 80)
                {
                    gySetting = Math.max(-80, Math.min(80, gySetting));
                    value = increment * gySetting + offset;
                }
                app.Filters.at(app.CurrentFilter).set("ySetting", gySetting);
                app.Filters.at(app.CurrentFilter).set("Y", value);
                this.$('#gaussY').val(value);
                this.$('#gaussYSetting').val(gySetting);
            } 
            else
            {
                value = app.Filters.at(app.CurrentFilter).get("Y");
                this.$('#gaussY').val(value);
            }
            this.showGaussPreview();
        },
        
        setGaussElements : function()
        {
            var numberFilters = app.Filters.length;
            
            $(".gaussInputs").toggleClass('hidden', numberFilters === 0);
            $("#filterMinus").toggleClass('hidden', numberFilters < 1);
            $("#filterPrevious").toggleClass('hidden', numberFilters < 2);
            $("#filterNext").toggleClass('hidden', numberFilters < 2);

            if (numberFilters > 0)
            {
                var filter = app.Filters.at(app.CurrentFilter);
                var filterLabel = app.CurrentFilter+1;
                
                $("#xLabel").text("X" + filterLabel);
                $("#yLabel").text("Y" + filterLabel);
                $("#sigmaXLabel").text("sigma X" + filterLabel);
                $("#sigmaYLabel").text("sigma Y" + filterLabel);
                
                $("#gaussXSetting").val(filter.get("xSetting"));
                $("#gaussYSetting").val(filter.get("ySetting"));
                $("#gaussSigmaXSetting").val(filter.get("sigmaXSetting"));
                $("#gaussSigmaYSetting").val(filter.get("sigmaYSetting"));
                
                $("#gaussX").val(filter.get("X"));
                $("#gaussY").val(filter.get("Y"));
                $("#gaussSigmaX").text(filter.get("sigmaX"));
                $("#gaussSigmaY").text(filter.get("sigmaY"));
            }
        },
        
        showGaussPreview: function() 
        {
            var size = app.FractalMod.get('size');
            var filter = app.Filters.at(app.CurrentFilter);
            var gsx = filter.get("sigmaX");
            var gsy = filter.get("sigmaY");
            var xSize = Math.floor(129 * gsx);
            var ySize = Math.floor(129 * gsy);
            $("#gaussPreview").css("background-size", xSize + "px " + ySize + "px"); 
            var gx = filter.get("X");
            var gy = filter.get("Y");
            var tempx = 2 * (gx-1)/(size -1);
            var tempy = 2 * (gy-1)/(size -1);
            var locX = (tempx - gsx) * 65;
            var locY = (tempy - gsy) * 65;
            var locXY = locX.toString() + 'px ' + locY.toString() + 'px';
            $("#gaussPreview").css("background-position", locXY);
        },
        
        useHeat: function() {
            app.CreateMod.set("useHeat", true);
            $("#heatPreview").toggleClass("hidden", false);
            $("#gradientPreview").toggleClass("hidden", true);
            $(".gradientInputs").toggleClass("hidden", true);
        },
        
        useGradient: function() {
            app.CreateMod.set("useHeat", false);
            $("#heatPreview").toggleClass("hidden", true);
            $("#gradientPreview").toggleClass("hidden", false);
            $(".gradientInputs").toggleClass("hidden", false);
        },
        
        addColorStop: function( color ) {
            var view = new ColorStopView({ model: color });
            $('#colorStopTable').append( view.render().el );
            this.colorViews.push(view);
        },

        addAllColorStops: function() {
            for(var i = this.colorViews.length - 1; i >=0; i--)
            {
                this.colorViews[i].remove;
            }
            this.colorViews = [];
            $('#colorStopTable').empty();
            app.ColorStops.each(this.addColorStop, this);
            this.updateGradient();
        },

        
        updateGradient: function()
        {
            var stopA = "";
            var stopB = "";
            var first = true;
            
            app.ColorStops.forEach(function(model) {
                if (model.get("useStop"))
                {
                    if (!first)
                    {
                        stopA = stopA + ", ";
                        stopB = stopB + ", ";
                    }
                    first = false;
                    
                    var stop = Math.round(model.get("stop")/ 2.55)/100;
                    stopA = stopA + model.get("color") + " " + stop*100 + "%";
                    stopB = stopB + "color-stop(" + stop + ", " + model.get("color") + ")";
                }
            });
    
            var bgi = "background-image: ";
            var lingrad = "linear-gradient(left, ";

            var gradElement = document.getElementById("gradientPreview");
            
            gradElement.style.background=lingrad + stopA  + ")";
            gradElement.style.background="-o-" + lingrad + stopA +")";
            gradElement.style.background="-moz-" + lingrad + stopA +")";
            gradElement.style.background="-webkit-" + lingrad + stopA +")";
            gradElement.style.background="-ms-" + lingrad + stopA +")";
            gradElement.style.background="-webkit-gradient(linear, left top, right top," + stopB + ")";
        }
        
    });
    return app.CreateView;
});


