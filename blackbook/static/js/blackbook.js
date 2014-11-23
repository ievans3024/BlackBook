var black_book = angular.module('BlackBook', [
    'BlackBook.controllers',
    'BlackBook.filters',
    'BlackBook.services'
],
function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

black_book.controllers = angular.module('BlackBook.controllers', []);
black_book.filters = angular.module('BlackBook.filters', []);
black_book.services = angular.module('BlackBook.services', []);

black_book.services.factory(
    'contacts_service', function($http) {

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

black_book.filters.filter(
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

black_book.controllers.controller(
    'selected_contact', function($scope, contacts_service) {

        $scope.selected = null;

        $scope.edit = function (href) {

        }

        $scope.delete = function (href) {
            contacts_service.delete(href).then(
                function () {
                    $scope.selected = null;
                }
            );
        }

        $scope.$on('select', function (event, href) {
            contacts_service.get(href).success(
                function (data) {
                    var collection = new Collection(data);
                    $scope.selected = collection.items[0];
                }
            );
        });
    }
);

black_book.controllers.controller(
    'contact_index', function($scope, contacts_service) {

        var navigation = {
            links: null,
            per_page: 5
        }

        $scope.index = null;
        $scope.navigation = navigation;

        $scope.get_contacts = function (href) {
            contacts_service.get(href).success(
                function (data) {
                    var collection = new Collection(data);
                    $scope.index = collection.items;
                    $scope.navigation.links = collection.links;
                }
            );
        }

        $scope.get_detail = function (href) {
            $scope.$broadcast('select', href);
        }

        $scope.refresh_index = function (href) {
            var uri;
            if ($scope.navigation.per_page !== 5) {
                uri = '/api/entry/?per_page=' + $scope.navigation.per_page;
            } else {
                uri = '/api/entry/';
            }
            $scope.get_contacts(uri);
        }

        $scope.refresh_index();
    }
);

// TODO: rewrite this using promises and expect()?
black_book.controllers.controller(
    'tests_controller', function ($scope, contacts_service) {

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

            contacts_service.get('/api/').then(
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