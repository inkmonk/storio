var story = {
    getStoryId : function(url) {
        var storyId = _.last(url.split("/"));
        return parseInt(storyId);
    }

    
};

var storifyApp = angular.module('storifyApp', ['btford.socket-io', 'cgNotify'])
    .factory('mySocket', function(socketFactory) {
        var myIoSocket = io.connect('http://localhost.com:5000');

        var mySocket = socketFactory({
            ioSocket: myIoSocket
        });

        return mySocket;
    })
        .controller('storifyController', function($scope, mySocket,
                                                  $http, notify) {

        function getUser() {
            return "test_user";
        }

            notify('hey');

        $scope.test = "hello world";

        // mySocket.emit('connect', {'hi': 'dude'}, function(something) {
        //     console.log('some', something);
        // });

        // mySocket.on('welcome', function(data) {
        //     console.log('data', data);
        // });

        mySocket.emit('join', {story_id: story.getStoryId(window.location.href)});
        
        mySocket.on('user_joined', function(data) {
            console.log('user_joined ', data);
        });    

        $scope.snippetChange = function(snippet) {
            var requestObj = { user: getUser(),
                               snippet: snippet
                             };
            
            console.log('cha ' + snippet);
        };
            
        $scope.snippetFinal = function(snippet) {
            var requestObj = { user: getUser(),
                               snippet: snippet
                             };
            console.log('final' + snippet);
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

