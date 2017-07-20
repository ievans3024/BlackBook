"use strict";

;(
  function () {
    angular.module('BlackBook')
      .controller(
        'selected_contact',
        [
          'contacts',
          '$scope',
          function (contacts, $scope) {
            $scope.selected = {};
            $scope.delete = function () {
              contacts.delete(selected)
                .success(
                  function () {
                    $scope.selected = {};
                  }
                )
            };
            $scope.edit = function () {
              contacts.patch(selected);
            };
            $scope.$on(
              'blackbook.contact.select', function (event, href) {
                contacts.get(href)
                  .success(
                    function (data) {
                      let collection = new Collection(data);
                      $scope.selected = collection.items[0];
                    }
                  );
              }
            );
          }
        ]
      )
      .controller(
        'contact_list',
        [
          'contacts',
          '$scope',
          function (contacts, $scope) {
            $scope.contacts = contacts.data;
            $scope.delete = function (contact) {
              contacts.delete(contact);
            };
            $scope.edit = function (contact) {
              contacts.patch(contact);
            };
            $scope.select = function (contact) {
              $scope.$broadcast('blackbook.contact.select', contact.href);
            };
            contacts.fetch();
          }
        ]
      )
      .controller(
        'new_contact',
        [
          'contacts',
          '$scope',
          function (contacts, $scope) {
            $scope.contact = {};
            $scope.create = function () {
              contacts.post($scope.contact);
            };
          }
        ]
      )
  }
)();