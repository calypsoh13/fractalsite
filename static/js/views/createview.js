var app = app || {};

$(function( $ ) {
    'use strict';

    // The Create image view
    // ---------------

    app.createView = Backbone.View.extend({

        // Instead of generating a new element, bind to the existing skeleton of
        // the App already present in the HTML.
        el: '#create',

        colorViews: [],
        
        // Our template for the line of statistics at the bottom of the app.
        createTemplate: _.template( $('#create-template').html() ),

        // Delegated events for creating new items, and clearing completed ones.
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
            new app.fractalView();
            this.listenTo(app.fractalMod, 'change', this.updateGaussForSize);
            this.listenTo(app.colorStops, 'add', this.addAllColorStops);
            this.listenTo(app.colorStops, 'remove', this.addAllColorStops);
            this.listenTo(app.colorStops, 'change', this.updateGradient);
            this.render();
            // add views for the gradient stops
            if (app.createMod.get("useHeat"))
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
            app.createMod.save("numberColorStops", app.colorStops.length);
            this.$el.html( this.createTemplate( app.createMod.toJSON() ) );
            this.addAllColorStops();
            return this;
        },

        // add a filter
        addFilter: function() {
            var filters = app.createMod.get("gaussFilters");
            // limit the user to 5 filters
            if (filters.length > 4) return;
            var midsize = (app.fractalMod.get('size') -1) / 2 + 1;
            filters.push(
            {
                gaussXSetting : 0, 
                gaussYSetting : 0,
                gaussX : midsize,
                gaussY : midsize,
                sigmaXSetting : 0,
                sigmaYSetting : 0,
                sigmaX : 1,
                sigmaY : 1 
            });
            app.createMod.save(
            {
                gaussFilters : filters,
                currentFilter : filters.length - 1
            });
            this.setGaussElements();
            this.showGaussPreview();
        },

        // remove a filter
        removeFilter: function() {
            var filterIndex = app.createMod.get("currentFilter");
            var filters = app.createMod.get("gaussFilters");
            filters.splice(filterIndex,1);
            filterIndex = Math.max(0, Math.min(filters.length-1, filterIndex));
            app.createMod.save(
            {
                gaussFilters : filters,
                currentFilter : filterIndex
            });
            this.setGaussElements();
            this.showGaussPreview();
        },
        
        // go to previous filter
        previousFilter: function() {
            var filterIndex = app.createMod.get("currentFilter");
            filterIndex--;
            if (filterIndex < 0)
            {
                filterIndex = app.createMod.get("gaussFilters").length - 1;
            }
            app.createMod.save({currentFilter : filterIndex});
            this.setGaussElements();
            this.showGaussPreview();
        },
        
        // go to next filter
        nextFilter: function() {
            var filterIndex = app.createMod.get("currentFilter");
            var filters = app.createMod.get("gaussFilters");
            filterIndex++;
            if (filterIndex > filters.length - 1)
            {
                filterIndex = 0;
            }
            app.createMod.save({currentFilter : filterIndex});
            this.setGaussElements();
            this.showGaussPreview();
        },
        
        editXSetting: function() {
            var value = parseInt(this.$('#gaussXSetting').val());
            
            if (!isNaN(value)) {
                var size = app.fractalMod.get('size');
                var increment = (size-1)/128;
                var offset = increment * 64;
                var gx = increment * value + offset;
                var filterIndex = app.createMod.get("currentFilter");
                var filters = app.createMod.get('gaussFilters');
                filters[filterIndex].gaussXSetting = value;
                filters[filterIndex].gaussX = gx;
                app.createMod.save('gaussFilters', filters);
                this.$('#gaussX').val(gx);
            } 
            this.showGaussPreview();
        },
        
        editYSetting: function() {
            var value = parseInt(this.$('#gaussYSetting').val());
            
            if (!isNaN(value)) {
                var size = app.fractalMod.get('size');
                var increment = (size-1)/128;
                var offset = increment * 64;
                var gy = increment * value + offset;
                var filterIndex = app.createMod.get("currentFilter");
                var filters = app.createMod.get('gaussFilters');
                filters[filterIndex].gaussYSetting = value;
                filters[filterIndex].gaussY = gy;
                app.createMod.save('gaussFilters', filters);
                this.$('#gaussY').val(gy);
            } 
            this.showGaussPreview();
        },
        
        editSigmaXSetting: function() {
            var value = parseInt(this.$('#gaussSigmaXSetting').val());
            
            if (!isNaN(value)) {
                var sigmaX = Math.floor(Math.pow(2, value/2) * 100) / 100;
                var filterIndex = app.createMod.get("currentFilter");
                var filters = app.createMod.get('gaussFilters');
                filters[filterIndex].sigmaXSetting = value;
                filters[filterIndex].sigmaX = sigmaX;
                app.createMod.save('gaussFilters', filters);
                this.$('#gaussSigmaX').text(sigmaX);
            }
            this.showGaussPreview();

        },
        
        editSigmaYSetting: function() {
            var value = parseInt(this.$('#gaussSigmaYSetting').val());
            if (!isNaN(value)) {
                var sigmaY = Math.floor(Math.pow(2, value/2) * 100) / 100;
                var filterIndex = app.createMod.get("currentFilter");
                var filters = app.createMod.get('gaussFilters');
                filters[filterIndex].sigmaYSetting = value;
                filters[filterIndex].sigmaY = sigmaY;
                app.createMod.save('gaussFilters', filters);
                this.$('#gaussSigmaY').text(sigmaY);
            }
            this.showGaussPreview();
        },
        
        updateGaussForSize: function() {
            var size = app.fractalMod.get('size');
            var filterIndex = app.createMod.get("currentFilter");
            var filters = app.createMod.get('gaussFilters');
            
            for(var i = 0; i < filters.length; i++)
            {
                var filter = filters[i];
                var increment = (size-1)/128;
                var offset = increment * 64;
                filter.gaussX = increment * filter.gaussXSetting + offset;
                filter.gaussY = increment * filter.gaussYSetting + offset;
            }
            app.createMod.save('gaussFilters', filters);
            
            if (filters.length > 0)
            {
                this.$('#gaussX').val(filters[filterIndex].gaussX);
                this.$('#gaussY').val(filters[filterIndex].gaussY);
            
                this.showGaussPreview();
            }
        },
        
        editX: function() {
            var filterIndex = app.createMod.get("currentFilter");
            var filters = app.createMod.get('gaussFilters');
            var value = parseInt(this.$('#gaussX').val());
            
            if (!isNaN(value)) {
                var size = app.fractalMod.get('size');
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
                filters[filterIndex].gaussXSetting = gxSetting;
                filters[filterIndex].gaussX = value;
                app.createMod.save('gaussFilters', filters);
                this.$('#gaussX').val(value);
                this.$('#gaussXSetting').val(gxSetting);
            } 
            else
            {
                value = filters[filterIndex].gaussX;
                this.$('#gaussX').val(value);
            }
            this.showGaussPreview();
        },
        
        editY: function() {
            var filterIndex = app.createMod.get("currentFilter");
            var filters = app.createMod.get('gaussFilters');
            var value = parseInt(this.$('#gaussY').val());
            
            if (!isNaN(value) ) {
                var size = app.fractalMod.get('size');
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
                filters[filterIndex].gaussYSetting = gySetting;
                filters[filterIndex].gaussY = value;
                app.createMod.save('gaussFilters', filters);
                this.$('#gaussY').val(value);
                this.$('#gaussYSetting').val(gySetting);
            } 
            else
            {
                value = filters[filterIndex].gaussY;
                this.$('#gaussY').val(value);
            }
            this.showGaussPreview();
        },
        
        setGaussElements : function()
        {
            var filters = app.createMod.get('gaussFilters');
            var numberFilters = filters.length;
            $(".gaussInputs").toggleClass('hidden', numberFilters === 0);
            $("#filterMinus").toggleClass('hidden', numberFilters < 1);
            $("#filterPrevious").toggleClass('hidden', numberFilters < 2);
            $("#filterNext").toggleClass('hidden', numberFilters < 2);

            if (numberFilters > 0)
            {
                var index = app.createMod.get("currentFilter");
                var filter = filters[index];
                var filterLabel = index+1;
        
                $("#xLabel").text("X" + filterLabel);
                $("#yLabel").text("Y" + filterLabel);
                $("#sigmaXLabel").text("sigma X" + filterLabel);
                $("#sigmaYLabel").text("sigma Y" + filterLabel);
        
                $("#gaussXSetting").val(filter.gaussXSetting);
                $("#gaussYSetting").val(filter.gaussYSetting);
                $("#gaussSigmaXSetting").val(filter.sigmaXSetting);
                $("#gaussSigmaYSetting").val(filter.sigmaYSetting);

                $("#gaussX").val(filter.gaussX);
                $("#gaussY").val(filter.gaussY);
                $("#gaussSigmaX").text(filter.sigmaX);
                $("#gaussSigmaY").text(filter.sigmaY);
            }
        },
        
        showGaussPreview: function() 
        {
            var size = app.fractalMod.get('size');
            var filterIndex = app.createMod.get("currentFilter");
            var filter = app.createMod.get('gaussFilters')[filterIndex];
            var gsx = filter.sigmaX;
            var gsy = filter.sigmaY;
            var xSize = Math.floor(129 * gsx);
            var ySize = Math.floor(129 * gsy);
            $("#gaussPreview").css("background-size", xSize + "px " + ySize + "px"); 
            var gx = filter.gaussX;
            var gy = filter.gaussY;
            var tempx = 2 * (gx-1)/(size -1);
            var tempy = 2 * (gy-1)/(size -1);
            var locX = (tempx - gsx) * 65;
            var locY = (tempy - gsy) * 65;
            $("#gaussPreview").css("background-position-x", locX);
            $("#gaussPreview").css("background-position-y", locY);
        },
        
        useHeat: function() {
            app.createMod.save(
            { 
                useHeat: true
            });
            $("#heatPreview").toggleClass("hidden", false);
            $("#gradientPreview").toggleClass("hidden", true);
            $(".gradientInputs").toggleClass("hidden", true);
        },
        
        useGradient: function() {
            app.createMod.save(
            { 
                useHeat: false
            });
            $("#heatPreview").toggleClass("hidden", true);
            $("#gradientPreview").toggleClass("hidden", false);
            $(".gradientInputs").toggleClass("hidden", false);
        },
        
        newColorAttributes: function() {
            return {
                order: app.Todos.nextOrder()
            };
        },
        
        addColorStop: function( color ) {
            var view = new app.ColorStopView({ model: color });
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
            app.colorStops.each(this.addColorStop, this);
            this.updateGradient();
        },

        
        updateGradient: function()
        {
            var stopA = "";
            var stopB = "";
            var first = true;
            
            app.colorStops.forEach(function(model) {
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
});


