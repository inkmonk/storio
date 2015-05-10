var story = {
    getStoryId : function(url) {
        var storyId = _.last(url.split("/"));
        return parseInt(storyId);
    }
};

var storifyApp = angular.module('storifyApp', ['btford.socket-io', 'cgNotify'])
    .factory('mySocket', function(socketFactory) {
        var myIoSocket = io.connect('http://' + serverName);


        var mySocket = socketFactory({
            ioSocket: myIoSocket
        });

        return mySocket;
    })
        .controller('storifyController', function($scope, mySocket,
                                                  $http, notify) {

            window.SCOPE = $scope;

            $scope.peopleWriting = [];
            $scope.userEmail = user;

            function updatePeopleWriting(elem) {
                // If elem.user is already present in
                // $scope.peopleWriting then just update the text.
                // If $scope.peopleWriting is empty, then return an
                // array with a single element.
                if (_.isEmpty($scope.peopleWriting)) {
                    return [elem];
                }
                var items = _.filter($scope.peopleWriting, function(item) {
                    return item.user === elem.user;
                });
                if (items.length > 0) {
                    var item = items[0];
                    item.text = elem.text;
                    var notItems = _.filter($scope.peopleWriting, function(elem) {
                        return item.user !== elem.user;
                    });
                    notItems.push(item);
                    return notItems;
                } 
                if (items.length === 0) {
                    $scope.peopleWriting.push(elem);
                    return $scope.peopleWriting;
                }
                console.log('should not reach here');
                return $scope.peopleWriting;
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
            console.log(data.user + "joined.");
        });    

        mySocket.on('welcome', function(data) {
            $scope.currentSegmentId = data.current_segment_id;
        });

            $scope.colorCount = "#C2C6CB";
        $scope.snippetChange = function(snippet) {
            var requestObj = { segment_id: $scope.currentSegmentId,
                               text: snippet,
                               story_id: story.getStoryId(window.location.href)
                             };
            console.log('hey its changing');
            $scope.colorCount = $scope.computeCountColor(snippet);
            mySocket.emit('modify_snippet_text', requestObj);
        };

            mySocket.on('user_modified_snippet_text', function(data) {
                console.log('user_modified_snippet_text handler');
                $scope.peopleWriting = updatePeopleWriting(data);
                console.log('server data', data);
            });

            $scope.computeCount = function(snippet) {
                if (snippet === null || snippet === undefined) {
                    return 40;
                }
                var remainingCount = 40 - snippet.length;
                return remainingCount;
            };

            $scope.computeCountColor = function(snippet) {
                if (snippet === null || snippet === undefined) {
                    return "#ec5959";
                }
                if (snippet.length < 20 || snippet.length > 40) {
                    return "#ec5959";
                }
                return "#C2C6CB";
            };
            
        $scope.snippetFinal = function(snippet) {
            if (snippet.length < 20 || snippet.length > 40) {
                return;
            }
            var requestObj = { story_id:
                               story.getStoryId(window.location.href),
                               segment_id: $scope.currentSegmentId,
                               text: snippet
                             };
            console.log('enter yo fool');
            mySocket.emit('submit_snippet', requestObj);
            $scope.snippet = "";
        };
            mySocket.on('handover_snippet_and_start_next_segment',
                        function(data) {
                            console.log('handover snippet and start'
                                        + ' next segemt');
                            $scope.peopleWriting = [];
                            $scope.currentSegmentId = data.next_segment_id;
                            $scope.alreadyWritten.push(data);
                        }) ;

            mySocket.on('append_snippet', function(data) {
                console.log('srya- append snippet ' , data);
            });

            $scope.computeColor = function(index) {
                var newIndex = index % 8;
                return colors[newIndex];
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

