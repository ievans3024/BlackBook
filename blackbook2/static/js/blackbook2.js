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
            var headers = { 'Accept': 'application/vnd.collection+json' },
            get = $http.get('/api/entry/', { headers: headers });
            get.success(function(){
                console.log(this.data);
            });
        };

        contactAPI.getContact = function() {

        };

        return contactAPI;
    }
);