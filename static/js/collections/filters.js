define([
        'underscore',
        'backbone',
        'app',
        'models/filtermod'
], function(_, Backbone, app, FilterMod) {
    'use strict';

    // Filters Collection
    // ---------------

    app.Filters = Backbone.Collection.extend({

        // Reference to this collection's model.
        model: app.FilterMod,

        // We keep the filters in sequential order, despite being saved by unordered
        // GUID in the database. This generates the next order number for new items.
        nextOrder: function() {
            if ( !this.length ) {
                return 1;
            }
            return this.last().get('order') + 1;
        },

        // Todos are sorted by their original insertion order.
        comparator: function( filter ) {
            return filter.get('order');
        }
    });

    // Create our global collection of **Filter models**
    return new app.Filters();

});
