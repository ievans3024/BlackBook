/**
 * Created by ian on 5/13/15.
 */

exports.spec = function (dbname) {
    return {
        "_id": "_api/employee",
        "endpoint": "/api/users/employee/",
        "properties": [
            {
                "prompt": "Employee ID",
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", "employee", "employee_id"].join("."),
                        [dbname, "read", "employee", "employee_id", "self"].join(".")
                    ],
                    "update": [
                        [dbname, "update", "employee", "employee_id"].join(".")
                    ]
                }
            },
            {
                "prompt": "Authorized Employee",
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", "employee", "employee_authorized"].join(".")
                    ],
                    "update": [
                        [dbname, "update", "employee", "employee_authorized"].join(".")
                    ]
                }
            },
            {
                "prompt": "Employee Discount",
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", "employee", "employee_discount"].join("."),
                        [dbname, "read", "employee", "employee_discount", "self"].join("."),
                    ],
                    "update": [
                        [dbname, "update", "employee", "employee_discount"].join(".")
                    ]
                }
            },
            {
                "data": {"name": "employee_department", "prompt": "Department", "placeholder": "Department"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", "employee", "employee_department"].join("."),
                        [dbname, "read", "employee", "employee_department", "self"].join(".")
                    ],
                    "update": [
                        [dbname, "update", "employee", "employee_department"].join(".")
                    ]
                }
            }
        ],
        "templates": {
            "create": {
                "permissions": {
                    "public": true,
                    "read": [],
                    "write": []
                },
                "validators": {}
            },
            "update": {
                "permissions": {},
                "data": [],
                "validators": {}
            }
        }
    }
};