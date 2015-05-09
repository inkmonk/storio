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

            $scope.peopleWriting = [];

            function updatePeopleWriting(elem) {
                var items = _.filter($scope.peopleWriting, function(item) {
                    return item.user === elem.user;
                });
                var notItems = _.filter($scope.peopleWriting, function(elem) {
                    return item.user !== elem.user;
                });
                if (items.length === 0) {
                    return $scope.peopleWriting;
                } else {
                    var item = items[0];
                    item.text = elem.text;
                    return notItems.append(item);
                }
            };
            $scope.alreadyWritten = [];

        function initializeStoryDetails(storyId)   {
            $http.get('/json/stories/' + storyId).
                success(function(data, status, headers, config) {
                    function mapObject(elem) {
                        var snippet = elem.snippets;
                        var firstSnippet = _.first(_.filter(snippet, function(elem)
                                                            {
                                                                return elem.is_first === true;
                                                            }));
                        return { current_segment_id: elem.id,
                                 first_snippet: firstSnippet,
                                 next_segment_id: null
                        };
                    }
                    data = data.result;
                    var segments = data.segments;
                    $scope.alreadyWritten = _.map(segments,
                                                  function(elem) {
                                                      return mapObject(elem);
                                                  });
                    console.log('stories', $scope.alreadyWritten);
                }).
                error(function(data, status, headers, config) {
                    console.log('story get error');
                });
        }  

        initializeStoryDetails(story.getStoryId(window.location.href));    

        mySocket.emit('join', {story_id: story.getStoryId(window.location.href)});
        
        mySocket.on('user_joined', function(data) {
            notify(data.user + " joined.");
        });    

        mySocket.on('welcome', function(data) {
            $scope.currentSegmentId = data.current_segment_id;
        });

        $scope.snippetChange = function(snippet) {
            var requestObj = { segment_id: $scope.currentSegmentId,
                               text: snippet,
                               story_id: story.getStoryId(window.location.href)
                             };
            mySocket.emit('modified_snippet_text', requestObj);
        };

            mySocket.on('user_modified_snippet_text', function(data) {
                console.log('hey coming');
                updatePeopleWriting(data);
            });

            
            
        $scope.snippetFinal = function(snippet) {
            var requestObj = { story_id:
                               story.getStoryId(window.location.href),
                               segment_id: $scope.currentSegmentId,
                               text: snippet
                             };
            mySocket.emit('submit_snippet', requestObj);
            $scope.snippet = "";
        };
            mySocket.on('handover_snippet_and_start_next_segment',
                        function(data) {
                            console.log('hey im dth');
                            $scope.currentSegmentId = data.next_segment_id;
                            $scope.alreadyWritten.push(data);
                        }) ;

            mySocket.on('append_snippet', function(data) {
                console.log('srya ' , data);
            });
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

