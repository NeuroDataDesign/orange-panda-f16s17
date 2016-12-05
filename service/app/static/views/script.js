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
        .when('/analyze', {
            templateUrl : 'static/views/pages/analyze.html',
            controller  : 'analyzeController'
        });
});

// create the controller and inject Angular's $scope
scotchApp.controller('mainController', function($scope) {
    // create a message to display in our view
    $scope.message = 'Welcome to PANDA';
});

scotchApp.controller('viewController', function($sce, $http, $scope) {
    $scope.message = 'View some analyses here!';
	$http.get('/getTable')
         .success(function(res){
            $scope.f_name_list = res
         })
});

scotchApp.controller('analyzeController', function($rootScope, $sce, $scope, $http) {
    $scope.message = '';
    $scope.set_bucket = true
    $scope.got_data = false
    $scope.args_set = false

    $scope.get = function(data) {
        $scope.data = data
        $scope.arguments = {}
        $scope.message = 'Trying to get data. This may take some time.';
		$http.post('/gets3', $scope.data)
             .success(function(path){
                $scope.message='Got Data!';
                $scope.set_bucket = false
                $scope.got_data = true
                $scope.args_set = false
                $scope.data_path = path
             })
             .error(function(){$scope.message='Something went wrong.'});
    }
    $scope.set_args = function(prep_args) {
        $scope.message='Preprocessing data... this will take some time!';
        prep_args['data_path'] = $scope.data_path
        prep_args['token'] = $scope.data.token
        prep_args['name'] = $scope.data.name
        $http.post('/prep', prep_args)
             .success(function(){
                $scope.message='Preprocessed Data!';
                $scope.set_bucket = false
                $scope.got_data = false
                $scope.args_set = true
             })
             .error(function(){$scope.message='Something went wrong.'});
    }
    $scope.analyze = function() {
        $rootScope.f_name_list = []
        $scope.message = 'Running Analysis. This should take no more than 2 minutes.';
		$http.post('/analyze_data', $scope.data)
             .success(function(res){
                 $scope.message='Analysis done! Look for ' + $scope.data.name + ' in the "Explore Analyses" section!';
                 $rootScope.f_name_list.push(res);
             })
             .error(function(){$scope.message='Something went wrong.'});
    }
    
});
