define([  
        'backbone_tastypie' 
], function(Backbone) { 
   // We don't really use the router, yet. 
    var AppRouter = Backbone.Router.extend({ 
        routes: {  
            // Default 
            '*actions': 'defaultAction' 
        },
        defaultAction: function(param) {
            console.log('Default: ' + param); // Just an example action
        }
    });

    return AppRouter;
});
