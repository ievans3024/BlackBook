angular.module('BlackBook', [
    'BlackBook.controllers',
    'BlackBook.services',
    'BlackBook.filters'
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

angular.module('BlackBook.filters', []).filter(
    'capitalize', function () {
        return function (input) {
            var string_array = input.split(' '),
                i;
            for (i = 0; i < string_array.length; i++) {
                string_array[i] = string_array[i][0].toUpperCase() + string_array[i].slice(1, string_array[i].length);
            }
            return string_array.join(' ');
        };
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
                    var contact_collection = new Collection(response.data)
                    $scope.selectedContact = contact_collection.items[0];
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
/*
angular.module('BlackBook.controllers', []).controller(
    'testsController', function ($scope, contactsService) {

        var status = {
            FAIL: { cssclass: 'label-danger', text: 'Failed!' },
            RUNNING: { cssclass: 'label-warning', text: 'Running...' },
            PASS: { cssclass: 'label-success', text: 'Passed!' }
        }

        $scope.tests = []
        $scope.current_test = null;

        $scope.test_basic = function () {

            $scope.current_test = {
                title: 'Basic GET',
                result: {text: 'Testing basic HTTP GET to /api/', status: status.RUNNING}
            }

            contactsService.get('/api/').then(
                function (response) {
                    if (
                        response.status === 200 &&
                        response.config.headers['Accept'] === 'application/vnd.collection+json' &&
                        response.data.hasOwnProperty('collection') &&
                        response.data.collection.hasOwnProperty('href') &&
                        response.data.collection.hasOwnProperty('version')
                        ) {

                        $scope.current_test.result.status = status.PASS;
                        $scope.current_test.result.text = 'HTTP GET /api/ successfully returned a Collection+JSON document'
                        $scope.tests.push($scope.current_test);
                        $scope.current_test = null;
                    }
                }
            )
        }

        $scope.test_basic();
    }
);
*/