/**
 * AngularJS <-> Collection+JSON middleware
 */

/**
 * Collection Constructor
 * @param opts The Object or JSON string to construct this Collection from.
 * Automatically validated with Collection.prototype.validate
 */
function Collection (opts) {

    if (!this instanceof Collection) {
        return new Collection(opts);
    }

    // Unwrap collection contents, if necessary.
    if (opts.hasOwnProperty('collection')) {
        opts = opts.collection;
    }

    this.collection = Collection.prototype.validate(opts);
}

/**
 * Collection base properties with more complex requirements
 */
Collection.prototype.property_rules = {
    error: {constructor: Object},
    data: {constructor: Array, required: [{name: 'name', type: 'string'}]},
    href: {type: 'string'},
    items: {constructor: Array, required: [{name: 'href', type: 'string'}]},
    links: {constructor: Array, required: [{name: 'href', type: 'string'}, {name: 'rel', type: 'string'}]},
    queries: {constructor: Array, required: [{name: 'href', type: 'string'}, {name: 'rel', type: 'string'}]},
    template: {constructor: Object, required: [{name: 'data', constructor: Array}]},
    version: {type: 'string'},
};

/**
 * Validate this collection OR validate a collection provided as an argument
 * @param collection Optional. A different collection to validate. May be an object, JSON-parseable string, or Collection.
 * @throws {TypeError} If collection is not object or string, or if collection properties do not follow spec types.
 * @throws {SyntaxError} If collection is a string and not parseable by JSON.parse
 * @throws {SyntaxError} If collection (or collection.collection) does not have at least "href" and "version" properties.
 * @throws {ValueError} If collection properties do not have required properties
 * @return {Object} The collection, if valid.
 */
Collection.prototype.validate = function (collection) {

    var property_string,
        property;

    function validate_property (prop, property_string) {
        var i = 0,
            i_2 = 0,
            i_3 = 0,
            properties = Object.getOwnPropertyNames(prop),
            property_rules,
            required;

        // Validate the current property
        if (property_string in this.property_rules) {
            if (this.property_rules[property_string].hasOwnProperty('constructor') {
                object_type = this.property_rules[property_string].constructor;
                if (!prop instanceof object_type) {
                    throw TypeError(
                        property_string + ' must be an instance of ' object_type.name
                    );
                }
            }
            if (this.property_rules[property_string].hasOwnProperty('type') {
                object_type = this.property_rules[property_string].type;
                if (typeof prop !== object_type) {
                    throw TypeError(
                        property_string + ' must be of type ' + object_type
                    )
                }
            }
            if (this.property_rules[property_string].hasOwnProperty('required')) {
                required = this.property_rules[property_string].required;
                if (object_type === Array) {
                    for (i_2 < prop.length; i_2++) {
                        for (i_3 < required.length; i_3++) {
                            if (!prop[i_2].hasOwnProperty(required[i_3].name)) {
                                throw ValueError(
                                    property_string + ' must have property ' + required[i_3].name
                                );
                            }
                            if (required[i_3].hasOwnProperty('type')) {
                                if (typeof prop[i_2][required[i_3].name] !== required[i_3].type) {
                                    throw TypeError(
                                        property_string + '.' + required[i_3].name + ' must be of type ' + required[i_3].type
                                    );
                                }
                            }
                            if (required[i_3].hasOwnProperty('constructor)) {
                                if (!prop[i_2][required[i_3].name] instanceof required[i_3].constructor) {
                                    throw TypeError(
                                        property_string + '.' + required[i_3].name + ' must be an instance of ' + required[i_3].constructor.name
                                    );
                                }
                            }
                        }
                    }
                } else if (object_type === Object) {
                    for (i_2 < required.length; i_2++) {
                        if (!prop.hasOwnProperty(required[i_2].name) {
                            throw ValueError(
                                property_string + ' must have property ' + required[i_2].name
                            );
                        }
                        if (required[i_2].hasOwnProperty('type')) {
                            if (typeof prop[required[i_2].name] !== required[i_2].type) {
                                throw TypeError(
                                    property_string + '.' + required[i_2].name + ' must be of type ' + required[i_2].type
                                );
                            }
                        }
                        if (required[i_2].hasOwnProperty('constructor')) {
                            if (!prop[required[i_2].name instanceof required[i_2].constructor) {
                                throw TypeError(
                                    property_string + '.' + required[i_2].name + ' must be an instance of ' + required[i_2].constructor.name
                                );
                            }
                        }
                    }
                }
            }
        }

        // Descend to validate child properties
        for (i < properties.length; i++) {
            validate_property(prop[properties[i]], property_string + properties[i]);
        }
    }

    if (!collection && this instanceof Collection) {
        collection = this;
    }

    if (typeof colleciton === 'string') {
        collection = JSON.parse(collection);
    } else if (!collection instanceof Object) {
        throw TypeError('collection must be an object or string.');
    }

    if (!collection.hasOwnProperty('href') || !collection.hasOwnProperty('version')) {
        throw SyntaxError('collection must have at least "href" and "version" properties.');
    }

    for (prop in collection) {
        validate_property(collection[prop], 'collection.' + prop);
    }

    return collection;
};