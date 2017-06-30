"use strict";

;(
  function () {
    angular.module('BlackBook')
      .service(
        'contacts',
        [
          '$http',
          function ($http) {
            return {
              endpoint: '/api/contacts/',
              data: {},
              fetch (settings) {
                const self = this;
                return $http.get(self.endpoint, settings)
                  .success(
                    (data) => {
                      self.data = data;
                    }
                  )
              },
              get (href, settings) {
                return $http.get(href, settings);
              },
              post (data, settings) {
                const self = this,
                      contact_data = '';
                return $http.post(self.endpoint, contact_data, settings)
                  .success(
                    () => self.fetch()
                  )
              },
              patch (data, settings) {
                const self = this,
                      contact_data = '';
                return $http.patch(data.href, contact_data, settings)
                  .success(
                    () => self.fetch()
                  )
              },
              delete (data, settings) {
                const self = this;
                return $http.delete(data.href, settings)
                  .success(
                    () => self.fetch()
                  )
              }
            };
          }
        ]
      )
  }
)();