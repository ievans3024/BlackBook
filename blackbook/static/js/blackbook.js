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

        var extractCollectionItems = function (response) {
            console.log(response.data);
            var data = [],
            data_items = response.data.collection.items,
            data_count = data_items.length;
            i = 0,
            data_object = null,
            data_object_item = null,
            data_object_item_length = 0,
            j = 0;

            for (i; i<data_count; i++) {
                data_object = {};
                data_object.href = data_items[i].href;
                data_object_item = data_items[i].data;
                data_object_item_length = data_object_item.length;
                j = 0;
                for (j; j<data_object_item_length; j++) {
                    data_object[data_object_item[j].name] = data_object_item[j].value;
                }
                data.push(data_object);
            }
            if (data.length === 1) {
                return data[0];
            }
            return data;
        };

        $scope.selectedContact = null;
        $scope.contactList = null;
        $scope.listNavigation = null;
        $scope.listPerPage = 5;
        $scope.deletedContact = null;

        $scope.getContact = function(href) {
            contactsService.get(href).then(
                function(response) {
                    $scope.selectedContact = extractCollectionItems(response);
                }
            );
        };

        $scope.getContactList = function (href) {
            contactsService.get(href).then(
                function(response) {
                    $scope.contactList = extractCollectionItems(response);
                    $scope.listNavigation = response.data.collection.links;
                }
            );
        }

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