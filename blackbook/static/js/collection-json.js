/**
 * AngularJS <-> Collection+JSON middleware
 */

/**
 * Collection Constructor
 * @param collection The Object or JSON string to construct this Collection from.
 * @throws {ValueError} If href or version properties are not present in collection.
 */
function Collection (collection) {

    /**
     * Iterate through an array, supplying parseables into a constructor,
     * passing instances of constructor into an output array.
     * @param {Array} array The array to process
     * @param {function} parseable The constructor for an acceptably parseable object
     * @param {function} constructor The constructor to pass parseable into, if necessary.
     * @return {Array}
     */
    function process_array (array, parseable, constructor) {
        var i = 0,
            output = [],
            length,
            item;

        for (i; i < length; i++) {
            item = array[i];
            if (item instanceof parseable) {
                try {
                    output.push(constructor(item));
                } catch (e) {
                    // Don't add item to the output, skip it.
                    console.warn('process_array: array[' + i + '] not added.', e);
                }
            } else if (item instanceof constructor) {
                output.push(item);
            }
        }

        return output;
    }

    var acceptable, acceptable_rules;

    if (!this instanceof Collection) {
        return new Collection(collection);
    }

    this.collection = {};

    // Parse from JSON, if necessary.
    if (typeof collection === 'string') {
        collection = JSON.parse(collection);
    }

    // Unwrap collection contents, if necessary.
    if (collection.hasOwnProperty('collection')) {
        collection = collection.collection;
    }

    // Check for most basic requirements in a Collection
    if (!collection.hasOwnProperty('href')) {
        throw ValueError('href property is required.');
    }
    if (!collection.hasOwnProperty('version')) {
        throw ValueError('version property is required.');
    }

    // Validate (and, if necessary, parse) values
    for (property in collection) {
        acceptable = collection[property];
        acceptable_rules = Collection.prototype.property_rules[property];
        try {
            Collection.prototype.validate({property: collection[property]}, true);
        } catch (e) {
            if (acceptable_rules.hasOwnProperty('constructor')) {
                if (acceptable_rules.constructor === Array) {
                    acceptable = process_array(acceptable, Object, acceptable_rules.contents.constructor);
                } else {
                    acceptable = acceptable_rules.constructor(acceptable);
                }
            }
        } finally {
            this.collection[property] = acceptable;
        }
    }

}

/**
 * Collection properties with type requirements
 */
Collection.prototype.property_rules = {
    error: {constructor: CollectionError},
    data: {constructor: Array, contents: {constructor: CollectionData}},
    href: {type: 'string'},
    items: {constructor: Array, contents: {constructor: CollectionItem}},
    links: {constructor: Array, contents: {constructor: CollectionLink}},
    queries: {constructor: Array, contents: {constructor: CollectionQuery}},
    template: {constructor: CollectionTemplate},
    version: {type: 'string'},
};

/**
 * Validate this collection OR validate a collection provided as an argument
 * @param collection Optional. A different collection to validate.
 * @param {bool} is_fragment Optional. If true, indicates that collection is not a complete Collection, but a segment.
 * @throws {TypeError} If collection is not a Collection and is_fragment is not true,
 * or if collection/fragment properties do not follow spec types.
 */
Collection.prototype.validate = function (collection, is_fragment) {

    var property_string,
        property;

    function validate_property (prop, property_string) {

        var i, rule,
        sub_properties = prop.getOwnPropertyNames();

        if (property_string in this.property_rules) {
            rule = this.property_rules[property_string];
            if (rule.hasOwnProperty('type')) {
                if (typeof prop !== rule.type) {
                    throw TypeError(property_string + ' must be of type ' + rule.type);
                }
            }

            if (rule.hasOwnProperty('constructor')) {
                if (!prop instanceof rule.constructor) {
                    throw TypeError(property_string + ' must be an instance of ' + rule.constructor);
                }
                if (rule.constructor === Array && rule.hasOwnProperty('contents')) {
                    for (i = 0; i < prop.length; i++) {
                        if (rule.contents.hasOwnProperty('constructor') {
                            if (!prop[i] instanceof rule.contents.constructor) {
                                throw TypeError(
                                    property_string + ' must only contain instances of ' + rule.contents.constructor.name
                                );
                            }
                        }
                    }
                }
            }
        }

        // Descend into child properties
        for (i = 0; i < sub_properties.length; i++) {
            validate_property(prop[sub_properties[i]], property_string + '.' + sub_properties[i]);
        }

    }

    if (!collection && this instanceof Collection) {
        collection = this;
    }

    if (!is_fragment) {
        if (!collection instanceof Collection) {
            throw TypeError('collection must be an instance of Collection');
        }

        if (!collection.hasOwnProperty('href') || !collection.hasOwnProperty('version')) {
            throw SyntaxError('collection must have at least "href" and "version" properties.');
        }
    }

    for (prop in collection) {
        validate_property(collection[prop], 'collection.' + prop);
    }
};


/**
 * CollectionData Constructor
 */
function CollectionData (opts) {

}

/**
 * CollectionError Constructor
 */
function CollectionError (opts) {

}

/**
 * CollectionItem Constructor
 */
function CollectionItem (opts) {

}

/**
 * CollectionLink Constructor
 */
function CollectionLink (opts) {

}

/**
 * CollectionQuery Constructor
 */
function CollectionQuery (opts) {

}

/**
 * CollectionTemplate Constructor
 */
function CollectionTemplate (opts) {

}