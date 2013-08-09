define([ 
        'jquery', 
        'backbone' 
], function($, Backbone) { 
    
    var AppRouter = Backbone.Router.extend({ 
        routes: {  
            // Default 
            '*actions': 'defaultAction' 
        },
        defaultAction: function(param) {
            console.log('Default: ' + param);
        }
    });

    return AppRouter;
});
