/**
 * Created by ievans3024 on 5/13/15.
 */

exports.design = {
    _id: "_design/employee",
    language: "javascript",
    validate_doc_update: function (new_rev, old_rev, context, security) {
        function require (field, message) {
            message = message || 'Document must have a field named ' + field;
            if (!new_rev[field]) {
                throw({forbidden: message});
            }
        }
        if (!(new_rev._deleted) && new_rev.subtype === 'employee') {
            require('employee_id');
            require('employee_authorized');
            require('employee_discount');
            require('employee_department');
            require('permissions');
        }
    },
    views: {
        all: {
            map: function (doc) {
                if (doc.subtype === 'employee' || doc.subtype === 'admin') {
                    emit(doc.id, doc);
                }
            }
        },
        by_employee_id: {
            map: function (doc) {
                if (doc.subtype === 'employee' || doc.subtype === 'admin') {
                    emit(doc.employee_id, doc);
                }
            }
        },
        by_group: {
            map: function (doc) {
                var i;
                if (doc.subtype === 'employee' && doc.groups) {
                    for (i = 0; i < doc.groups.length; i++) {
                        emit(doc.groups[i], doc);
                    }
                }
            }
        }
    }
};