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
        return new Collection(href, version, from_object);
    }

    // Unwrap collection contents, if necessary.
    if (opts.hasOwnProperty('collection')) {
        opts = opts.collection;
    }

    Collection.prototype.validate(opts);

    // Assuming validator did it's job properly
    this.collection = opts;
}

/**
 * Collection base properties where typeof should be checked.
 */
Collection.prototype.property_types = {
    href: 'string',
    version: 'string'
};

/**
 * Collection base properties with more complex requirements
 */
Collection.prototype.property_rules = {
    error: {constructor: Object},
    data: {constructor: Array, required: [{name: 'name', type: 'string'}]},
    items: {constructor: Array, required: [{name: 'href', type: 'string'}]},
    links: {constructor: Array, required: [{name: 'href', type: 'string'}, {name: 'rel', type: 'string'}]},
    queries: {constructor: Array, required: [{name: 'href', type: 'string'}, {name: 'rel', type: 'string'}]},
    template: {constructor: Object, required: [{name: 'data', type: Array}]}
};

/**
 * Validate this collection OR validate a collection provided as an argument
 * @param collection Optional. A different collection to validate. May be an object, JSON-parseable string, or Collection.
 * @throws {TypeError} If collection is not object or string.
 * @throws {SyntaxError} If collection is a string and not parseable by JSON.parse
 * @throws {SyntaxError} If collection (or collection.collection) does not have at least "href" and "version" properties.
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
        if (property_string in this.property_types) {
            if (typeof prop !== this.property_types[property_string]) {
                throw TypeError(
                    property_string + ' must be of type ' + this.property_types[property_string]
                );
            }
        }
        if (property_string in this.property_rules) {
            object_type = this.property_rules[property_string].constructor;
            if (this.property_rules[property_string].hasOwnProperty('required')) {
                required = this.property_rules[property_string].required;
                if (object_type === Array) {
                    for (i_2 < prop.length; i_2++) {
                        for (i_3 < required.length; i_3++) {
                            // TODO:
                            // Check prop[i_2].hasOwnProperty(required[i_3].name);
                            // Check prop[i_2][required[i_3].name] isinstance required[i_3].type
                            // -OR-
                            // Check typeof prop[i_2][required[i_3].name] === required[i_3].type
                        }
                    }
                } else if (object_type === Object) {
                    for (i_2 < required.length; i_2++) {
                        // TODO:
                        // Check prop.hasOwnProperty(required[i_2].name);
                        // Check prop[required[i_2].name] isinstance required[i_2].type
                        // -OR-
                        // Check typeof prop[required[i_2].name] === required[i_2].type
                    }
                }
            }
            if (!prop instanceof this.property_object_types[property_string].constructor) {
                throw TypeError(
                    property_string + ' must be an instance of ' + this.property_object_types[property_string].name
                );
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

    if (typeof opts === 'string') {
        collection = JSON.parse(opts);
    } else if (!opts instanceof Object) {
        throw TypeError('collection must be an object or string.');
    }

    if (!collection.hasOwnProperty('href') || !collection.hasOwnProperty('version')) {
        throw SyntaxError('collection must have at least "href" and "version" properties.');
    }

    for (prop in collection) {
        validate_property(collection[prop], 'collection.' + prop);
    }

};