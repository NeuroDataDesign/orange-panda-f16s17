// Declare app level module which depends on filters, and services
var app = angular.module('flashSPA', ['ngResource', 'ngAnimate', 'ngRoute', 'ui.bootstrap', 'ui.date', 'pageslide-directive'])
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'pages/mainPage/views/dashboard.html'
    })
    .otherwise({redirectTo: '/'});
}]);

app.controller('SiteArbiter', function($scope, $location , $rootScope, $http, $interval){
    $scope.location = $location.path();
    $scope.$on('$routeChangeSuccess', function(e) {
        $scope.location = $location.path();
    })
})

app.directive('keycatcher', function(){
    return {
        scope: false,
        link: function (scope, element, $rootScope) {
            element.on('keypress', function(e){
                if(e.keyCode == 8220){
                    scope.navigator = !scope.navigator;
                    if(!scope.$$phase) {
                        scope.$apply();
                    } 
                }
                else if(e.keyCode == 8216){
                    scope.settings = !scope.settings;
                    if(!scope.$$phase) {
                        scope.$apply();
                    } 
                }
            });
        }
    }
})