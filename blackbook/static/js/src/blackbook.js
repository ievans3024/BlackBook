/* TODO: js minifier automation w/ travis */

var black_book = angular.module('BlackBook', [
    'BlackBook.controllers',
    'BlackBook.filters',
    'BlackBook.services'
],
function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

black_book.filters = angular.module('BlackBook.filters', []);

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