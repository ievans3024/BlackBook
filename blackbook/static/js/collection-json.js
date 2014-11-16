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

    // Parse from JSON, if necessary.
    if (typeof opts === 'string') {
        opts = JSON.parse(opts);
    }

    // Unwrap collection contents, if necessary.
    if (opts.hasOwnProperty('collection')) {
        opts = opts.collection;
    }

    this.collection = collection;
}

/**
 * Collection base properties with more complex requirements
 */
Collection.prototype.property_rules = {
    error: {constructor: Error},
    data: {constructor: Array, contents: {constructor: Data}},
    href: {type: 'string'},
    items: {constructor: Array, contents: {constructor: Item}},
    links: {constructor: Array, contents: {constructor: Link}},
    queries: {constructor: Array, contents: {constructor: Query}},
    template: {constructor: Template},
    version: {type: 'string'},
};

/**
 * Validate this collection OR validate a collection provided as an argument
 * @param collection Optional. A different collection to validate. Must be a Collection.
 * @throws {TypeError} If collection is not a Collection, or if collection properties do not follow spec types.
 */
Collection.prototype.validate = function (collection) {

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

    if (!collection instanceof Collection) {
        throw TypeError('collection must be an instance of Collection');
    }

    if (!collection.hasOwnProperty('href') || !collection.hasOwnProperty('version')) {
        throw SyntaxError('collection must have at least "href" and "version" properties.');
    }

    for (prop in collection) {
        validate_property(collection[prop], 'collection.' + prop);
    }
};