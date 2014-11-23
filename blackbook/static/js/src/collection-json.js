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

    var i, collection_props;

    if (!(this instanceof Collection)) {
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

    collection = Collection.prototype.parse(collection);
    collection_props = Object.getOwnPropertyNames(collection);

    for (i = 0; i < collection_props.length; i++) {
        this[collection_props[i]] = collection[collection_props[i]];
    }

}

/**
 * Collection properties with type requirements
 */
Collection.prototype.property_rules = {
    error: {construct: CollectionError},
    href: {type: 'string', required: true},
    items: {construct: Array, contents: {construct: CollectionItem}},
    links: {construct: Array, contents: {construct: CollectionLink}},
    queries: {construct: Array, contents: {construct: CollectionQuery}},
    template: {construct: CollectionTemplate},
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
        return JSON.stringify({collection: this}, this.preJSON);
    }
}

/**
 * Property validator and parser
 * @param {Object} object The object to parse.
 * @return {Object} The parsed form of the object
 */
Collection.prototype.parse = function (object) {
    var i,
        i_2,
        prop,
        property,
        r,
        rule,
        rule_object,
        rules,
        collection = object;

    function process_array (array, contains) {

        var i,
            field,
            output = [];

        if (!(array instanceof Array)) {
            throw TypeError('array parameter must be an Array.');
        }

        if (typeof contains !== 'function') {
            throw TypeError('contains parameter must be a function.');
        }

        for (i = 0; i < array.length; i++) {
            if (array[i] instanceof contains) {
                output.push(array[i]);
            } else {
                output.push(new contains(array[i]));
            }
        }

        if (output.length > 0) {
            return output;
        }

    }

    if (typeof object === 'string') {
        object = JSON.parse(object);
    }

    rules = Object.getOwnPropertyNames(this.property_rules);
    
    for (i = 0; i < rules.length; i++) {
        prop = rules[i];
        if (object.hasOwnProperty(prop)) {
            property = object[prop];
            rule_object = this.property_rules[prop];
            rule = Object.getOwnPropertyNames(rule_object);
            for (i_2 = 0; i_2 < rule.length; i_2++) {
                r = rule[i_2];
                if (r === 'required' && rule_object.required) {
                    if (!object.hasOwnProperty(prop)) {
                        throw ValueError(prop + ' is a required property.');
                    }
                }

                if (r === 'construct') {
                    if (rule_object.construct === Array) {
                        property = process_array(property, rule_object.contents.construct);
                    } else {
                        if (!((property instanceof rule_object.construct))) {
                            property = new rule_object.construct(property);
                        }
                    }
                }

                if (r === 'type') {
                    if (typeof property !== rule_object.type) {
                        throw TypeError(prop + ' must be of type ' + rule_object.type);
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
Collection.hook = function (construct) {
    Collection.hooked.push(construct);
    construct.prototype.toString = Collection.prototype.toString;
    construct.prototype.parse = Collection.prototype.parse;
};

Collection.hooked = [Collection];


/**
 * CollectionData Constructor
 * @param {Array} fields The array containing the data fields for this data
 */
function CollectionData (fields) {

    var i,
        i_2,
        opts,
        value;

    if (!((this instanceof CollectionData))) {
        return new CollectionData(opts);
    }

    this.array = fields;

    for (i = 0; i < fields.length; i++) {
        opts = CollectionData.prototype.parse(fields[i]);
        opts_props = Object.getOwnPropertyNames(opts);
        value = {}
        for (i_2 = 0; i_2 < opts_props.length; i_2++) {
            if (opts_props[i_2] !== 'name') {
                value[opts_props[i_2]] = opts[opts_props[i_2]];
            }
        }
        this[opts.name] = value;
    }
}

/**
 * CollectionData property rules
 */
CollectionData.prototype.property_rules = {
    'name': {type: 'string', required: true},
    'prompt': {type: 'string'}
};

CollectionData.prototype.toArray = function () {
    if (this instanceof CollectionData) {
        return this.array;
    }
}

CollectionData.prototype.preJSON = CollectionData.prototype.toArray;

Collection.hook(CollectionData);


/**
 * CollectionError Constructor
 */
function CollectionError (opts) {

    var i;

    if (!(this instanceof CollectionError)) {
        return new CollectionError(opts);
    }
    
    opts = CollectionError.prototype.parse(opts);
    opts_props = Object.getOwnPropertyNames(opts);

    for (i = 0; i < opts_props.length; i++) {
        this[opts_props[i]] = opts[opts_props[i]];
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

    var i;

    if (!(this instanceof CollectionItem)) {
        return new CollectionItem(opts);
    }
    
    opts = CollectionItem.prototype.parse(opts);
    opts_props = Object.getOwnPropertyNames(opts);

    for (i = 0; i < opts_props.length; i++) {
        this[opts_props[i]] = opts[opts_props[i]];
    }
    
}

/**
 * CollectionItem property rules
 */
CollectionItem.prototype.property_rules = {
    href: Collection.prototype.property_rules.href,
    data: {construct: CollectionData},
    links: Collection.prototype.property_rules.links
};

Collection.hook(CollectionItem);


/**
 * CollectionLink Constructor
 */
function CollectionLink (opts) {

    var i;

    if (!(this instanceof CollectionLink)) {
        return new CollectionLink(opts);
    }
    
    opts = CollectionLink.prototype.parse(opts);
    opts_props = Object.getOwnPropertyNames(opts);

    for (i = 0; i < opts_props.length; i++) {
        this[opts_props[i]] = opts[opts_props[i]];
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

    var i;

    if (!(this instanceof CollectionQuery)) {
        return new CollectionQuery(opts);
    }
    
    opts = CollectionQuery.prototype.parse(opts);
    opts_props = Object.getOwnPropertyNames(opts);

    for (i = 0; i < opts_props.length; i++) {
        this[opts_props[i]] = opts[opts_props[i]];
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

    var i;

    if (!(this instanceof CollectionTemplate)) {
        return new CollectionTemplate(opts);
    }
    
    opts = CollectionTemplate.prototype.parse(opts);
    opts_props = Object.getOwnPropertyNames(opts);

    for (i = 0; i < opts_props.length; i++) {
        this[opts_props[i]] = opts[opts_props[i]];
    }
    
}

CollectionTemplate.prototype.property_rules = {
    data: CollectionItem.prototype.property_rules.data
}

Collection.hook(CollectionTemplate);