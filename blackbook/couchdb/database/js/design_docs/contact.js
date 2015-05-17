/**
 * Created by ievans3024 on 5/14/15.
 */

exports.design = {
    _id: "_design/contact",
    language: "javascript",
    validate_doc_update: function (new_rev, old_rev, context, security) {
        function require (field, message) {
            message = message || 'Document must have a field named ' + field;
            if (!new_rev[field]) {
                throw({forbidden: message});
            }
        }
        if (!(new_rev._deleted) && new_rev.type === 'contact') {
            require('name_first');
            require('name_last');
        }
    },
    views: {
        all: {
            map: function (doc) {
                if (doc.type === 'contact') {
                    emit(doc.id, doc);
                }
            }
        },
        by_address: {
            map: function (doc) {
                if (doc.type === 'contact') {

                }
            }
        },
        by_email: {
            map: function (doc) {
                if (doc.type === 'contact') {

                }
            }
        },
        by_name: {
            map: function (doc) {
                if (doc.type === 'contact') {

                }
            }
        },
        by_phone_number: {
            map: function (doc) {
                if (doc.type === 'contact') {

                }
            }
        },
        by_surname: {
            map: function (doc) {
                if (doc.type === 'contact') {

                }
            }
        },
        by_user: {
            map: function (doc) {
                if (doc.type === 'contact') {
                    emit(doc.user, doc);
                }
            }
        }
    }
};
