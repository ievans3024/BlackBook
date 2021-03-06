black_book.controllers = black_book.controllers || angular.module('BlackBook.controllers', []);

black_book.controllers.controller(
    'selected_contact', function ($scope, contacts_service) {

        $scope.selected = null;

        $scope.edit = function (href) {

        };

        $scope.delete = function (href) {
            contacts_service.delete(href).then(
                function () {
                    $scope.selected = null;
                }
            );
        };

        $scope.$on('select', function (event, href) {
            contacts_service.read(href).success(
                function (data) {
                    var collection = new Collection(data);
                    $scope.selected = collection.items[0];
                }
            );
        });
    }
);

black_book.controllers.controller(
    'new_contact', function ($scope, contacts_service) {
        var status_messages = {
            201: {cssclass: 'bg-success', text: 'Contact created!'},
            400: {cssclass: 'bg-danger', text: 'Bad form data. Please double-check each field.'}
        };

        $scope.template = {};
        $scope.defaults = {};
        $scope.statuses = [];

        $scope.add_fieldset = function (fieldset) {
            if (fieldset === 'emails' || fieldset === 'phone_numbers') {
                $scope.template.data[fieldset].value.unshift(angular.copy($scope.defaults[fieldset]));
            }
        };

        $scope.remove_fieldset = function (fieldset, index) {
            if (fieldset === 'emails' || fieldset === 'phone_numbers') {
                $scope.template.data[fieldset].value.splice(index, 1);
            }
        };

        $scope.create_new = function () {
            var promise = contacts_service.create({ data: $scope.template.data.array });
            promise.success(
                function (data, status) {
                    $scope.statuses.push(status_messages[status]);
                }
            );
            promise.error(
                function (data, status) {
                    $scope.statuses.push(status_messages[status]);
                }
            );
        };

        $scope.$watch(
            function () { return contacts_service.collection; },
            function (newValue) {
                if (
                    newValue instanceof Collection &&
                        newValue.hasOwnProperty('template')
                ) {
                    $scope.template = angular.copy(newValue.template);
                    $scope.defaults.emails = angular.copy(newValue.template.data.emails.value[0]);
                    $scope.defaults.phone_numbers = angular.copy(newValue.template.data.phone_numbers.value[0]);
                }
            },
            true
        );
    }
);

black_book.controllers.controller(
    'contact_index', function ($scope, contacts_service) {

        var navigation = {
            links: null,
            per_page: 5
        };

        $scope.index = null;
        $scope.navigation = navigation;

        $scope.get_contacts = function (href) {
            contacts_service.read(href).success(
                function (data) {
                    var collection = new Collection(data);
                    contacts_service.collection = collection;
                    $scope.index = collection.items;
                    $scope.navigation.links = collection.links;
                }
            );
        };

        $scope.get_detail = function (href) {
            $scope.$broadcast('select', href);
        };

        $scope.refresh_index = function (href) {
            var uri;
            if (href) {
                uri = href;
            } else if ($scope.navigation.per_page !== 5) {
                uri = '/api/entry/?per_page=' + $scope.navigation.per_page;
            } else {
                uri = '/api/entry/';
            }
            $scope.get_contacts(uri);
        };

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
        };

        $scope.tests = [];
        $scope.current_test = null;

        $scope.test_basic = function () {

            $scope.current_test = {
                title: 'Basic GET',
                result: {text: 'Testing basic HTTP GET to /api/', status: status.RUNNING}
            };

            contacts_service.read('/api/').then(
                function (response) {
                    if (
                        response.status === 200 &&
                        response.config.headers['Accept'] === 'application/vnd.collection+json' &&
                        response.data.hasOwnProperty('collection') &&
                        response.data.collection.hasOwnProperty('href') &&
                        response.data.collection.hasOwnProperty('version')
                        ) {

                        $scope.current_test.result.status = status.PASS;
                        $scope.current_test.result.text = 'HTTP GET /api/ successfully returned a Collection+JSON document';
                        $scope.tests.push($scope.current_test);
                        $scope.current_test = null;
                    }
                }
            )
        };

        $scope.test_basic();
    }
);