/**
 * AngularJS <-> Collection+JSON middleware
 * @author ievans3024
 * @preserve true
 */

"use strict";

class CollectionArray {

  constructor (contains, ...array) {
    let i = 0;

    if (typeof contains !== 'function') {
      throw new Error(
        'First argument "contains" must be a function.'
      );
    }

    for (i; i < array.length; i++) {
      if (!(array[i] instanceof contains)) {
        try {
          array[i] = contains(array[i]);
        } catch (e) {
          throw new Error(
            'CollectionArray[' + contains.name + '] may only contain instances of ' + contains.name + '.'
          );
        }
      }
    }

    this.data = array;
    this.contains = contains;

  }

  get (search_property, search_value) {

    if (typeof search_property === 'number') {
      return this.data[search_property];
    } else {
      return this.data.reduce(
        function (accumulator, currentValue) {

          if (accumulator !== null) {
            return accumulator;
          }

          if (currentValue.hasOwnProperty(search_property)) {
            if (
              typeof search_value === 'undefined' ||
                currentValue[search_property] === search_value
            ) {
              return currentValue;
            }
          }

          return accumulator;

        },
        null
      );
    }

  }

  set (search_property, search_value, set_property, set_value) {

    let i = 0;

    for (i; i < this.data.length; i++) {
      if (this.data[i][search_property] === search_value) {
        this.data[i][set_property] = set_value;
        return this.data[i];
      }
    }

  }

  indexOf(property, property_value) {

    let i = 0;

    for (i; i < this.data.length; i++) {
      if (this.data[i][property] === property_value) {
        return i
      }
    }

  }

  push (...values) {

    let i = 0;

    for (i; i < values.length; i++) {
      if (!(values[i] instanceof this.contains)) {
        try {
          values[i] = new this.contains(values[i]);
        } catch (e) {
          console.log(e);
          throw new Error(
            'CollectionArray[' + this.contains.name + '] may only contain instances of ' + this.contains.name + '.'
          )
        }
      }
    }

    return this.data.push(...values);

  }

  splice (start, deleteCount, ...values) {

    let i = 0;

    for (i; i < values.length; i++) {
      if (!(values[i] instanceof this.contains)) {
        console.log(values[i]);
        try {
          values[i] = new this.contains(values[i]);
        } catch (e) {
          console.log(e);
          throw new Error(
            'CollectionArray[' + this.contains.name + '] may only contain instances of ' + this.contains.name + '.'
          );
        }
      }
    }

    return this.data.splice(start, deleteCount, ...values);

  }

  toString () {
    return this.data.toString();
  }

  unshift (...values) {

    let i = 0;

    for (i; i < values.length; i++) {
      if (!(values[i] instanceof this.contains)) {
        try {
          values[i] = new this.contains(values[i]);
        } catch (e) {
          console.log(e);
          throw new Error(
            'CollectionArray[' + this.contains.name + '] may only contain instances of ' + this.contains.name + '.'
          )
        }
      }
    }

    return this.data.unshift(...values);

  }

}

class CollectionData {

  constructor (data) {

    let property;

    if (!data.hasOwnProperty('name')) {
      throw new Error('CollectionData must have a "name" property');
    }
    this.name = data.name;
    delete data.name;

    if (data.hasOwnProperty('prompt')) {
      this.prompt = data.prompt;
      delete data.prompt;
    }

    if (data.hasOwnProperty('value')) {
      this.value = data.value;
      delete data.value;
    }

    // allow extensions
    for (property in data) {
      if (data.hasOwnProperty(property)) {
        this[property] = data[property];
      }
    }

  }

}

class CollectionError {

  constructor (error) {

    let property;

    // a bit wild-westy, but allows extensions and covers spec properties (which are all optional.)
    for (property in error) {
      if (error.hasOwnProperty(property)) {
        this[property] = error[property];
      }
    }

  }

}

class CollectionLink {

  constructor (link) {

    let property;

    if (!link.hasOwnProperty('href')) {
      throw new Error('CollectionLink must have "href" property.');
    }

    if (!link.hasOwnProperty('rel')) {
      throw new Error('CollectionLink must have "rel" property.');
    }

    this.href = link.href;
    delete link.href;

    this.rel = link.rel;
    delete link.rel;

    for (property in link) {
      if (link.hasOwnProperty(property)) {
        this[property] = link[property];
      }
    }

  }
}

class CollectionItem {

  constructor (item) {

    let property;

    if (!item.hasOwnProperty('href')) {
      throw new Error('CollectionItem must have "href" property.');
    }
    this.href = item.href;
    delete item.href;

    if (item.hasOwnProperty('data')) {
      this.data = item.data;
      delete item.data;
    }

    if (item.hasOwnProperty('links')) {
      this.links = item.links;
      delete item.links;
    }

    // support extensions
    for (property in item) {
      if (item.hasOwnProperty(property)) {
        this[property] = item[property];
      }
    }

  }

  get data () {
    return super.data;
  }

  set data (value) {
    if (!(value instanceof CollectionArray)) {
      value = new CollectionArray(CollectionData, ...value);
    }
    super.data = value;
  }

  get links () {
    return super.links;
  }

  set links (value) {
    if (!(value instanceof CollectionArray)) {
      value = new CollectionArray(CollectionLink, ...value);
    }
    super.links = value;
  }

}

class CollectionQuery {

  constructor (query) {

    let property;

    if (!query.hasOwnProperty('href')) {
      throw new Error(
        'CollectionQuery must have "href" property.'
      );
    }

    if (!query.hasOwnProperty('rel')) {
      throw new Error(
        'CollectionQuery must have "rel" property.'
      );
    }

    this.href = query.href;
    delete query.href;

    this.rel = query.rel;
    delete query.rel;

    for (property in query) {
      if (query.hasOwnProperty(property)) {
        this[property] = query[property];
      }
    }
  }

  get data () {
    return super.data;
  }

  set data (value) {
    if (!(value instanceof CollectionArray)) {
      value = new CollectionArray(CollectionData);
    }
    super.data = value;
  }
}

class CollectionTemplate {

  constructor (template) {

    if (!template.hasOwnProperty('data')) {
      throw new Error(
        'CollectionTemplate must have "data" property.'
      )
    }

    this.data = template.data;
  }

  get data () {
    return super.data;
  }

  set data (value) {
    if (!(value instanceof CollectionArray)) {
      value = new CollectionArray(CollectionData);
    }
    super.data = value;
  }

}

class Collection {

  constructor (collection) {

    let property;

    if (typeof collection === 'string') {
      collection = JSON.parse(collection);
    }

    if (collection.hasOwnProperty('collection')) {
      collection = collection.collection;
    }

    if (!collection.hasOwnProperty('href')) {
      throw new Error('Invalid collection: missing "href" property.');
    }

    if (!collection.hasOwnProperty('version')) {
      throw new Error('Invalid collection: missing "version" property.');
    }

    for (property in collection) {
      if (collection.hasOwnProperty(property)) {
        this[property] = collection[property];
      }
    }

  }

  toString () {
    return JSON.stringify({collection: this});
  }

  get error () {
    return super.error;
  }

  set error (value) {
    if (!(value instanceof CollectionError)) {
      value = new CollectionError(value);
    }
    super.error = value;
  }

  get items () {
    return super.items;
  }

  set items (value) {
    if (!(value instanceof CollectionArray)) {
      value = new CollectionArray(CollectionItem, ...value);
    }
    super.items = value;
  }

  get links () {
    return super.links;
  }

  set links (value) {
    if (!(value instanceof CollectionArray)) {
      value = new CollectionArray(CollectionLink, ...value);
    }
    super.links = value;
  }

  get queries () {
    return super.queries;
  }

  set queries (value) {
    if (!(value instanceof CollectionArray)) {
      value = new CollectionArray(CollectionQuery, ...value);
    }
    super.queries = value;
  }

  get template () {
    return super.template;
  }

  set template (value) {
    if (!(value instanceof CollectionTemplate)) {
      value = new CollectionTemplate(value);
    }
    super.template = value;
  }

  get version () {
    return super.version;
  }

  set version (value) {
    if (typeof value !== 'string') {
      throw new Error('Collection version must be a string.');
    }
    super.version = value;
  }

}