var scotchApp = angular.module('scotchApp', ['ngFileUpload', 'ui.bootstrap']);

scotchApp.controller('mainController', ['$scope', '$http', 'Upload', '$sce', function($scope, $http, Upload, $sce) {
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
        var data = new FormData();
        data.append('classifier', $scope.files[i].classifier);
        data.append('file', $scope.files[i]);

        $.ajax({
            url: "/upload",
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: "POST"
        }).done(function(data) {
            console.log(data);
            $scope.$apply(function() {
                $scope.files[i]['result'] = data;
                $scope.files[i].loading = false;
            });
            i = i + 1;
            if (i < $scope.files.length) {
                doRequest(i);
            }
        });
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

}]);