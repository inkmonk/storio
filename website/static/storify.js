angular.module('storifyApp', ['btford.socket-io'])
    .factory('mySocket', function(socketFactory) {
        return socketFactory();
    })
    .controller('storifyController', function($scope) {
        console.log('hell world');
        $scope.test = "hello world";
    });

