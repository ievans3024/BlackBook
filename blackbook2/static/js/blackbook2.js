angular.module('BlackBook', [
    'BlackBook.controllers',
    'BlackBook.services'
],
function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

angular.module('BlackBook.services', []).factory(
    'contactsService', function($http) {

        var contactAPI = {};

        contactAPI.getContactList = function() {
            var headers = { 'Accept': 'application/vnd.collection+json' };
            return $http.get('/api/entry/', { headers: headers });
        };

        contactAPI.getContact = function() {

        };

        return contactAPI;
    }
);

angular.module('BlackBook.controllers', []).controller(
    'contactsController', function($scope, contactsService) {
        $scope.selectedContact = null;
        $scope.contactList = [];

        contactsService.getContactList().then(
            function (response) {
                // Success callback. Extract information and set it in $scope.
                console.log(response.data);
                //$scope.contactList = response;
            }
        );
    }
);