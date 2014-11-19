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

        contactAPI.get = function(href) {
            var headers = { 'Accept': 'application/vnd.collection+json' };
            return $http.get(href, { headers: headers }); // please note how this might be insecure
        };

        contactAPI.delete = function(href) {
            return $http.delete(href);
        }

        return contactAPI;
    }
);

angular.module('BlackBook.controllers', []).controller(
    'contactsController', function($scope, contactsService) {

    // TODO: Create separate controllers for featured contact, pagination, contact list, and create/edit/delete

        $scope.collection = null;
        $scope.selectedContact = null;
        $scope.contactList = null;
        $scope.listNavigation = null;
        $scope.listPerPage = 5;
        $scope.deletedContact = null;

        $scope.getContactList = function (href) {
            contactsService.get(href).then(
                function(response) {
                    $scope.collection = new Collection(response.data);
                    $scope.contactList = $scope.collection.items;
                    $scope.listNavigation = $scope.collection.links;
                }
            );
        };

        $scope.getContact = function(href) {
            contactsService.get(href).then(
                function(response) {
                    $scope.selectedContact = extractCollectionItems(response);
                }
            );
        };

        $scope.refreshList = function () {
            $scope.getContactList('/api/entry/?page=1&per_page=' + $scope.listPerPage);
        }

        $scope.deleteContact = function (href) {
            contactsService.delete(href).then(
                function (response) {
                    $scope.selectedContact = null;
                    $scope.deletedContact = null;
                    $scope.refreshList();
                }
            );
        }

        $scope.getContactList('/api/entry/');
    }
);