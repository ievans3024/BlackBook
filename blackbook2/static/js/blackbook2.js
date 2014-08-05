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

        contactAPI.getContact = function(href) {
            var headers = { 'Accept': 'application/vnd.collection+json' };
            return $http.get(href, { headers: headers }); // please note how this might be insecure
        };

        return contactAPI;
    }
);

angular.module('BlackBook.controllers', []).controller(
    'contactsController', function($scope, contactsService) {
        $scope.selectedContact = null;
        $scope.contactList = [];

        $scope.processCollection = function (response) {
            var contacts = [],
            contact_items = response.data.collection.items,
            contact_count = contact_items.length;
            i = 0,
            contact = null,
            contact_item = null,
            contact_item_length = 0,
            j = 0;

            for (i; i<contact_count; i++) {
                contact = {};
                contact.href = contact_items[i].href;
                contact_item = contact_items[i].data;
                contact_item_length = contact_item.length;
                j = 0;
                for (j; j<contact_item.length; j++) {
                    contact[contact_item[j].name] = contact_item[j].value;
                }
                contacts.push(contact);
            }
            if (contacts.length === 1) {
                return contacts[0];
            }
            return contacts;
        };

        $scope.getContact = function(href) {
            contactsService.getContact(href).then(
            function(response) {
                $scope.selectedContact = $scope.processCollection(response);
            }
            );
        };

        contactsService.getContactList().then(
            function (response) {
                $scope.contactList = $scope.processCollection(response);
            }
        );
    }
);