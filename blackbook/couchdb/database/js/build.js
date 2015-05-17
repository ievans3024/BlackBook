/**
 * Created by ievans3024 on 5/13/15.
 */

var emit = function(){},  // so node doesn't bitch about emit not existing
    replacer = function (k, v) {
        if (typeof v === 'function') {
            return "" + v;  // cast function as a string to get string form
        }
        return v;
    },
    dbname = "blackbook",
    filesystem = require("fs"),
    schema = [
        // Design Docs
        // require("./design_docs/example.js").design

        // API Specs
        // require("./api_specs/example.js").spec(dbname)
    ];

schema_string = JSON.stringify(schema, replacer);

filesystem.writeFile(dbname + ".json", schema_string);