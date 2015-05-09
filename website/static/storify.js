angular.module('storifyApp', ['btford.socket-io'])
    .factory('mySocket', function(socketFactory) {
        var myIoSocket = io.connect('http://localhost.com:5000');

        var mySocket = socketFactory({
            ioSocket: myIoSocket
        });

        return mySocket;
    })
    .controller('storifyController', function($scope, mySocket) {
        console.log('hell world');
        $scope.test = "hello world";

        mySocket.emit('connect', function(something) {
            console.log('some', something);
        });
    });

