/**
 * AngularJS <-> Collection+JSON middleware
 */

// TODO: write property constructors to accept JSON as an argument

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

    this.collection = Collection.prototype.parse(collection);

}

/**
 * Collection properties with type requirements
 */
Collection.prototype.property_rules = {
    error: {constructor: CollectionError},
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

        if (output.length > 0) {
            return output;
        }
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
                if (rule.constructor === Array) {
                    property = process_array(property, Object, rule.contents.constructor);
                } else {
                    if (!property instanceof rule.constructor) {
                        property = rule.constructor(property);
                    }
                }
            }
            
            if (r === 'type') {
                if (typeof property !== rule.type) {
                    throw TypeError(prop + ' must be of type ' + rule.type);
                }
            }
        }

        if (property !== undefined) {
            collection[prop] = property;
        }

    }
    
    return collection;
}

/**
 * Hook collection data constructors to use some Collection functions
 * @param {function} constructor The constructor whose prototype should receive these functions
 */
Collection.hook = function (constructor) {
    constructor.prototype.toString = Collection.prototype.toString;
    constructor.prototype.parse = Collection.prototype.parse;
};



/**
 * CollectionData Constructor
 * @param {Object} opts The properties of this field
 */
function CollectionData (opts) {

    if (!this instanceof CollectionData) {
        return new CollectionData(opts);
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

Collection.hook(CollectionData);



/**
 * CollectionError Constructor
 */
function CollectionError (opts) {

    if (!this instanceof CollectionError) {
        return new CollectionError(opts);
    }

    opts = CollectionError.prototype.parse(opts);

    for (opt in opts) {
        this[opt] = opts[opt];
    }
}

/**
 * CollectionError property rules
 */
CollectionError.prototype.property_rules = {
    title: {type: 'string'},
    code: {type: 'string'},
    message: {type: 'string'}
};

Collection.hook(CollectionError);


/**
 * CollectionItem Constructor
 */
function CollectionItem (opts) {
    if (!this instanceof CollectionItem) {
        return new CollectionItem(opts);
    }

    opts = CollectionItem.prototype.parse(opts);

    for (opt in opts) {
        this[opt] = opts[opt];
    }
}

/**
 * CollectionItem property rules
 */
CollectionItem.prototype.property_rules = {
    href: Collection.prototype.property_rules.href,
    data: {constructor: Array, contents: {constructor: CollectionData}},
    links: Collection.prototype.property_rules.links
};

Collection.hook(CollectionItem);


/**
 * CollectionLink Constructor
 */
function CollectionLink (opts) {
    if (!this instanceof CollectionLink) {
        return new CollectionLink(opts);
    }

    opts = CollectionLink.prototype.parse(opts);

    for (opt in opts) {
        this[opt] = opts[opt];
    }
}

CollectionLink.prototype.property_rules = {
    href: Collection.prototype.property_rules.href,
    rel: {type: 'string', required: true},
    prompt: {type: 'string'},
    name: {type: 'string'},
    render: {type: 'string'}
}

Collection.hook(CollectionLink);


/**
 * CollectionQuery Constructor
 */
function CollectionQuery (opts) {
    if (!this instanceof CollectionQuery) {
        return new CollectionQuery(opts);
    }

    opts = CollectionQuery.prototype.parse(opts);

    for (opt in opts) {
        this[opt] = opts[opt];
    }
}

CollectionQuery.prototype.property_rules = CollectionLink.prototype.property_rules;
delete CollectionQuery.prototype.property_rules.render;
CollectionQuery.prototype.property_rules.data = CollectionItem.prototype.property_rules.data

Collection.hook(CollectionQuery);


/**
 * CollectionTemplate Constructor
 */
function CollectionTemplate (opts) {
    if (!this instanceof CollectionTemplate) {
        return new CollectionTemplate(opts);
    }

    opts = CollectionTemplate.prototype.parse(opts);

    for (opt in opts) {
        this[opt] = opts[opt];
    }
}

CollectionTemplate.prototype.property_rules = {
    data: CollectionItem.prototype.property_rules.data
}

Collection.hook(CollectionTemplate);