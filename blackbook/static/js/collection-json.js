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
    items: {constructor: CollectionArray, contents: {constructor: CollectionItem}},
    links: {constructor: CollectionArray, contents: {constructor: CollectionLink}},
    queries: {constructor: CollectionArray, contents: {constructor: CollectionQuery}},
    template: {constructor: CollectionTemplate},
    version: {type: 'string', required: true},
};

/**
 * Collection string method
 */
Collection.prototype.toString = function () {

    var i
        acceptable_instance = false;

    for (i = 0; i < Collection.hooked.length; i++) {
        if (this instanceof Collection.hooked[i]) {
            acceptable_instance = true;
            break;
        }
    }

    if (acceptable_instance) {
        return JSON.stringify(this, this.preJSON);
    }
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

    if (typeof object === 'string') {
        object = JSON.parse(object);
    }
    
    for (prop in this.property_rules) {
        if (object.hasOwnProperty(prop)) {
            property = object[prop];
            rule = this.property_rules[prop];
            for (r in rule) {
                if (r === 'required' && rule[r]) {
                    if (!object.hasOwnProperty(prop)) {
                        throw ValueError(prop + ' is a required property.');
                    }
                }

                if (r === 'constructor') {
                    if (rule.constructor === CollectionArray) {
                        property = new CollectionArray(property, rule.contents.constructor);
                    } else {
                        if (!property instanceof rule.constructor) {
                            property = new rule.constructor(property);
                        }
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
    }
    
    return collection;
}

/**
 * Hook some Collection functions into a collection data constructor's prototype
 * @param {function} constructor The constructor whose prototype should receive these functions
 */
Collection.hook = function (constructor) {
    Collection.hooked.push(constructor);
    constructor.prototype.toString = Collection.prototype.toString;
    constructor.prototype.parse = Collection.prototype.parse;
};

Collection.hooked = [Collection];


/**
 * CollectionArray constructor
 * @param {Array} array The array to make into an object
 * @param {function} contains The constructor for the type of data this CollectionArray should contain
 * @throws TypeError If params are not the correct type.
 */
function CollectionArray (array, contains) {

    var i,
        field;

    if (!this instanceof CollectionArray) {
        return new CollectionArray(opts);
    }

    if (!array instanceof Array) {
        throw TypeError('array parameter must be an Array.');
    }

    if (typeof contains !== 'function') {
        throw TypeError('contains parameter must be a function.');
    }

    for (i = 0; i < array.length; i++) {
        if (array[i] instanceof contains) {
            field = array[i];
        } else {
            field = new contains(array[i]);
        }
        this[field.name] = {};
        for (prop in field) {
            this[field.name][prop] = field[prop];
        }
    }

}

/**
 * Turn CollectionArray's data into a Collection+JSON-friendly array
 */
CollectionArray.prototype.toArray = function () {

    var i,
        properties,
        array = []
        field_object;

    if (this instanceof CollectionArray) {
        fields = this.getOwnPropertyNames();
        for (i = 0; i < fields.length; i++) {
            field_object = {name: fields[i]};
            for (prop in this[fields[i]]) {
                field_object[prop] = this[fields[i]][prop];
            }
            array.push(field_object);
        }
    }

    return array;
}

CollectionArray.prototype.preJSON = CollectionArray.prototype.toArray;


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
    data: {constructor: CollectionArray, contents: {constructor: CollectionData}},
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