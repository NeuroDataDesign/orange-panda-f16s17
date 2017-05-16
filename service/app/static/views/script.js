// create the module and name it scotchApp
var scotchApp = angular.module('eegApp', ['ngRoute']);

// configure our routes
scotchApp.config(function($routeProvider) {
    $routeProvider

        // route for the home page
        .when('/', {
            templateUrl : 'static/views/pages/home.html',
            controller  : 'mainController'
        })

        // route for the about page
        .when('/view', {
            templateUrl : 'static/views/pages/view.html',
            controller  : 'viewController'
        })

        // route for the contact page
        .when('/process', {
            templateUrl : 'static/views/pages/process.html',
            controller  : 'processController'
        })

        .when('/flow', {
            templateUrl : 'static/views/pages/flow.html',
            controller  : 'flowController'
        });
});

scotchApp.controller('viewController', function($scope) {
    // create a message to display in our view
    $scope.message = 'View Results';
});

// create the controller and inject Angular's $scope
scotchApp.controller('mainController', function($scope) {
    // create a message to display in our view
    $scope.message = 'Welcome to PANDA';
});


scotchApp.controller('processController', function($rootScope, $sce, $scope, $http) {
    $scope.message = '';
    $scope.set_bucket = true

    $scope.get = function(data) {
        $scope.data = data
        $scope.arguments = {}
        $scope.message = 'Trying to get data. This may take some time.';
		$http.post('/gets3', $scope.data)
             .success(function(path){
                $scope.message=path ;
                //$scope.data_path = path
             })
             .error(function(){$scope.message='Something went wrong.'});
    }
});
