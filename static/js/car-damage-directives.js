carDamageApp.directive('popoverClose', function($timeout) {
    return {
        scope: {
            excludeClass: '@'
        },
        link: function(scope, element, attrs) {
            var trigger = document.getElementsByClassName('trigger');

            function closeTrigger(i) {
                $timeout(function() {
                    angular.element(trigger[0]).triggerHandler('click').removeClass('trigger');
                });
            }

            element.on('click', function(event) {
                var etarget = angular.element(event.target);
                var tlength = trigger.length;
                if (!etarget.hasClass('trigger') && !etarget.hasClass(scope.excludeClass)) {
                    for (var i = 0; i < tlength; i++) {
                        closeTrigger(i)
                    }
                }
            });
        }
    };
});

carDamageApp.directive('popoverElem', function() {
    return {
        link: function(scope, element, attrs) {
            element.on('click', function() {
                element.addClass('trigger');
            });
        }
    };
});