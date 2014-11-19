/**
 * AngularJS <-> Collection+JSON middleware
 */

/**
 * Collection Constructor
 * @param collection The Object or JSON string to construct this Collection from.
 * @throws {ValueError} If href or version properties are not present in collection.
 */
function Collection (collection) {

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

    this.collection = Collection.prototype.parse(collection);

}

/**
 * Collection properties with type requirements
 */
Collection.prototype.property_rules = {
    error: {constructor: CollectionError},
    // data: {constructor: Array, contents: {constructor: CollectionData}},
    href: {type: 'string', required: true},
    items: {constructor: Array, contents: {constructor: CollectionItem}},
    links: {constructor: Array, contents: {constructor: CollectionLink}},
    queries: {constructor: Array, contents: {constructor: CollectionQuery}},
    template: {constructor: CollectionTemplate},
    version: {type: 'string', required: true},
};

/**
 * Collection string method
 */
Collection.prototype.toString = function () {
    return JSON.stringify(this);
}

/**
 * Property validator and parser
 * @param {Object} object The object to parse.
 * @return {Object} The parsed form of the object
 */
Collection.prototype.parse = function (object) {
    var property,
        rule,
        collection = object;
        
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
                output.push(constructor(item));
            } else if (item instanceof constructor) {
                output.push(item);
            }
        }

        return output;
    }
    
    for (prop in this.property_rules) {
        property = object[prop];
        rule = this.property_rules[prop];
        
        for (r in rule) {
            if (r === 'required' && rule[r]) {
                if (!object.hasOwnProperty(prop)) {
                    throw ValueError(prop + ' is a required property.');
                }
            }
        
            if (r === 'constructor') {
                if (!property instanceof rule.constructor) {
                    throw TypeError(prop + ' must be an instance of ' + rule.constructor.name);
                }
                if (rule.constructor === Array) {
                    property = process_array(property, Object, rule.contents.constructor);
                } else {
                    property = rule.constructor(property);
                }
            }
            
            if (r === 'type') {
                if (typeof property !== rule.type) {
                    throw TypeError(prop + ' must be of type ' + rule.type);
                }
            }
        }
        
        collection[prop] = property;
    }
    
    return collection;
}



/**
 * CollectionData Constructor
 * @param {Object} opts The properties of this field
 */
function CollectionData (opts) {

    if (!this instanceof CollectionData) {
        return new CollectionData(name, opts);
    }

    if (!opts.hasOwnProperty('name')) {
        throw ValueError('name property is required.');
    }
    
    opts = CollectionData.prototype.parse(opts);

    for (opt in opts) {
        this[opt] = opts[opt];
    }
}

/**
 * CollectionData property rules
 */
CollectionData.prototype.property_rules = {
    'name': {type: 'string', required: true},
    'prompt': {type: 'string'}
};

/**
 * CollectionData string method
 */
CollectionData.prototype.toString = function () {
    return JSON.stringify(this);
}

CollectionData.prototype.parse = Collection.prototype.parse;



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