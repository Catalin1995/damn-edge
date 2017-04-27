var carDamageApp = angular.module('carDamageApp', ['ngFileUpload', 'ui.bootstrap', 'ngImgCrop']);

carDamageApp.controller('mainController', ['$scope', '$http', 'Upload', '$sce', function($scope, $http, Upload, $sce) {
    $scope.classifiers = [];
    $scope.files = [];
    $scope.loading = false;
    $scope.Math = window.Math;

    $scope.dynamicPopover = {
        templateUrl: 'changeClassifierTemplate.html',
        title: 'Change the classifier'
    };

    $scope.fileSettings = {
        templateUrl: 'fileSettingsTemplate.html',
        title: 'Settings'
    }

    initialize();

    function initialize() {
        getClassifiers();
    }

    function getClassifiers() {
        $http.get('/classifiers').
        then(successGetClassifiers, errorGetClassifiers)
    }

    function successGetClassifiers(response) {
        $scope.classifiers = response.data.classifiers;
    }

    function errorGetClassifiers(error) {
        console.log('Error loading classifiers!');
        console.log(error);
    }

    $scope.onFileSelect = function($files) {
        angular.forEach($files, function(value) {
            value['loading'] = false;
            if ($scope.classifiers.length != 0)
                value['classifier'] = $scope.classifiers[0];
            else
                value['classifier'] = '';
            var reader = new FileReader();

            var reader = new FileReader();
            reader.onload = function(e) {
                var image = new Image();
                image.onload = function() {
                    value.content = reader.result;
                    $scope.$apply(function() {
                        $scope.files.push(value);
                    });
                };
                image.src = e.target.result;
            };
            reader.readAsDataURL(value);
        });
    }

    $scope.generateReports = function() {
        startLoadingItems()
        $scope.results = [];
        $scope.loading = true;
        doRequest(0);
    }

    function doRequest(i) {
        var test = new FormData();
        test.append('classifier', $scope.files[i].classifier);
        test.append('file', $scope.files[i]);

        var config = {
            headers: { 'Content-Type': undefined }
        }

        $http.post('/upload', test, config).then(
            function successCallback(response) {
                console.log(response);
                $scope.files[i]['result'] = response.data;
                $scope.files[i].loading = false;
                i = i + 1;
                if (i < $scope.files.length) {
                    doRequest(i);
                }
            },
            function errorCallback(error) {
                console.log("POST request error!");
                console.log(error);
            }
        );
    }

    function startLoadingItems() {
        angular.forEach($scope.files, function(file) {
            file.loading = true;
        })
    }

    var trustedHtml = {};

    $scope.getImgHtml = function(file) {
        return trustedHtml[file.name] || (trustedHtml[file.name] = $sce.trustAsHtml("<img src='" + file.content + "' width='200px' height='auto'/>"));
    }

    $scope.getClassifiersHtml = function(file) {
        return trustedClassifierHtml[file.name] || (trustedHtml[file.name] = $sce.trustAsHtml("<img src='" + file.content + "' width='200px' height='auto'/>"));
    }

    $scope.removeFile = function(file) {
        var index = $scope.files.indexOf(file);
        $scope.files.splice(index, 1);
    }

    $scope.addCropedImgToList = function() {
        // console.log($scope.myCroppedImage);
        // var image = new Image($scope.myCroppedImage);
        // console.log(image);
        // $scope.$apply(function() {
        //     $scope.files.push($scope.myCroppedImage);
        // });
    }

    // for croping an img
    $scope.myImage = '';
    $scope.myCroppedImage = '';

    var handleFileSelect = function(evt) {
        var file = evt.currentTarget.files[0];
        var reader = new FileReader();
        reader.onload = function(evt) {
            $scope.$apply(function($scope) {
                $scope.myImage = evt.target.result;
            });
        };
        reader.readAsDataURL(file);
    };
    angular.element(document.querySelector('#fileInput')).on('change', handleFileSelect);
}]);