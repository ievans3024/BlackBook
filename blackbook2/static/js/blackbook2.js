angular.module('BlackBook', [
    'BlackBook.controllers',
    'BlackBook.services'
],
function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

angular.module('BlackBook.controllers', []).controller(
    'contactsController', function($scope, contactsService) {
        $scope.selectedContact = null;
        $scope.contactList = [];

        contactsService.getContactList().success(function (response) {
            $scope.contactList = response;
        });
    }
);

angular.module('BlackBook.services', []).factory(
    'contactsService', function($http) {

        var contactAPI = {};

        contactAPI.getContactList = function() {
            return $http.get('/api/entry/');
        };

        contactAPI.getContact = function() {

        };

        return contactAPI;
    }
);