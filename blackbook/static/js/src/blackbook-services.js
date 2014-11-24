black_book.services = black_book.services || angular.module('BlackBook.services', []);

black_book.services.factory(
    'contacts_service', function($http) {
        var collection = {};

        return {
            create: function (data, href) {
                var request = {
                    method: 'POST',
                    url: '/api/entry/',
                    headers: {'Content-Type': 'application/vnd.collection+json'},
                    data: data
                };

                if (href) {
                    request.url = '/api/entry/';
                }

                return $http(request);
            },
            read: function(href) {
                var headers = { 'Accept': 'application/vnd.collection+json' };
                return $http.get(href, { headers: headers }); // please note how this might be insecure
            },
            update: function (href, data) {

            },
            delete: function(href) {
                return $http.delete(href);
            },
            collection: collection
        }

    }
);