"use strict";

;(
  function () {
    angular.module('BlackBook', ['ngRoute'])
      .filter(
        'capitalize', function () {
          return function (input) {
            let string_array = input.split(' '),
                i;
            for (i = 0; i < string_array.length; i++) {
              string_array[i] = string_array[i][0].toUpperCase() + string_array[i].slice(1);
            }
            return string_array.join(' ');
          };
        }
      );
  }
)();