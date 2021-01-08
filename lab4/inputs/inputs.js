// Angular application
var app = angular.module("PeselApp", []);
// Controller
app.controller("PeselController", function ($scope) {
    $scope.result = function () {
        if (typeof $scope.pesel !== "undefined") {
            var cutPesel = String($scope.pesel).substring(0, 6);

            var year = cutPesel.substring(0, 2);
            var month = cutPesel.substring(2, 4);
            var day = cutPesel.substring(4, 6);

            var dateUnparsed = day + "-" + month + "-" + year;
            if (year != "" && month != "" && day != "")
                return dateUnparsed;
            else
                return "";
        }
    };
});