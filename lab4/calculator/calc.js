// Angular application
var app = angular.module("CalculatorApp", []);
// controller
app.controller("CalculatorController", function($scope) {
        $scope.result = function() {
            if ($scope.operator == '+') {
                return "Result: " + ($scope.a + $scope.b);
            }
            if ($scope.operator == '-') {
                return "Result: " + ($scope.a - $scope.b);
            }
        };
});