/**
 * Created by ievans3024 on 5/13/15.
 */

exports.spec = function (dbname) {
    var modelname = "example";

    return {
        "_id": "_api/" + modelname,
        "endpoint": "/api/" + modelname + "/",
        "properties": [
            {
                "data": {"name": "", "prompt": ""},
                "permissions": {
                    "public": false,
                    "read": [
                        /*
                        list of permission strings user must have to
                        read this property. if this list is empty,
                        nobody has permission, except special root user
                         */
                    ],
                    "update": [
                        /*
                        list of permission strings user must have to
                        change or delete the value of this property.
                        if this list is empty, nobody has permission,
                        except special root user.
                         */
                    ]
                }
            }
        ],
        "template_data": {
            "create": [],
            "update": []
        },
        "template_meta": {
            "create": {
                "permissions": {
                    "public": true,
                    "read": [],
                    "write": []
                },
                "validators": {}
            },
            "update": {
                "permissions": {
                    "public": true,
                    "read": [],
                    "write": []
                },
                "validators": {}
            }
        }
    }
};