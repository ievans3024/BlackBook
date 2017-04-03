"use strict";

;(
  function () {
    angular.module('BlackBook')
      .service(
        'contacts',
        [
          '$http',
          function ($http) {
            this.endpoint = '/api/contacts/';
            this.data = {};
            this.fetch = function (http_settings) {
              var self = this;
              return $http.get(this.endpoint, http_settings)
                .success(
                  function (data) {
                    self.data = data;
                  }
                );
            };
            this.get = function (href, http_settings) {
              return $http.get(href, http_settings);
            };
            this.post = function (contact, http_settings) {
              var self = this,
                  contact_data = '';
              return $http.post(this.endpoint, contact_data, http_settings)
                .success(
                  function () {
                    self.fetch();
                  }
                );
            };
            this.patch = function (contact, http_settings) {
              var self = this,
                  contact_data = '';
              return $http.patch(contact.href, contact_data, http_settings)
                .success(
                  function () {
                    self.fetch();
                  }
                )
            };
            this.delete = function (contact, http_settings) {
              var self = this;
              return $http.delete(contact.href, http_settings)
                .success(
                  function () {
                    self.fetch();
                  }
                );
            };
          }
        ]
      )
  }
)();