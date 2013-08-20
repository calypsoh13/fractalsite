define([  
        'backbone_tastypie',
        'views/createview'
], function(Backbone, CreateView) { 

    var AppRouter = Backbone.Router.extend({ 
        routes: {  
            // Default 
            '': 'defaultRoute',
            'create': 'create' 
        },
        defaultRoute: function(){
            console.log("beep boop");
        },
        create: function() {
            console.log('Create View');
            new CreateView();
        }
    });

    return AppRouter;
});
