require.config({
  paths: {
    jquery: 'lib/jquery.min',
    lodash: 'lib/lodash.min',
    backbone: 'lib/backbone',
    underscore: 'lib/underscore',
    base: 'base',
    backbone-localStorage: 'lib/backbone.localStorage',
    
    
  }

});

require([
  // Load our app module and pass it to our definition function
  'app',

], function(App){
  // The "app" dependency is passed in as "App"
  // Again, the other dependencies passed in are not "AMD" therefore don't pass a parameter to this function
  App.initialize();
});
