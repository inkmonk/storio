var storifyApp = angular.module('storifyApp', ['btford.socket-io'])
    .factory('mySocket', function(socketFactory) {
        var myIoSocket = io.connect('http://localhost.com:5000');

        var mySocket = socketFactory({
            ioSocket: myIoSocket
        });

        return mySocket;
    })
    .controller('storifyController', function($scope, mySocket) {

        $scope.test = "hello world";

        mySocket.emit('connect', {'hi': 'dude'}, function(something) {
            console.log('some', something);
        });

        mySocket.on('welcome', function(data) {
            console.log('data', data);
        });

        $scope.segmentChange = function(segment) {
            console.log(segment);
        };
    });

storifyApp.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });
                event.preventDefault();
            }
        });
    };
});

