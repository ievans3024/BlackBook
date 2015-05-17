/**
 * Created by ievans3024 on 5/17/15.
 */


exports.spec = function (dbname) {
    var modelname = "contact";
    
    return {
        "_id": "_api/" + modelname,
        "endpoint": "/api/" + modelname + "/",
        "properties": [
            {
                "data": {"name": "user", "prompt": "Created by"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "user"].join(".")
                    ],
                    "update": []  // cannot be modified
                }
            },
            {
                "data": {"name": "name_first", "prompt": "First Name", "placeholder": "First Name"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "name_first"].join(".")
                    ],
                    "update": [
                        [dbname, "update", modelname, "name_first"].join(".")
                    ]
                }
            },
            {
                "data": {"name": "name_last", "prompt": "Last Name", "placeholder": "Last Name"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "name_last"].join(".")
                    ],
                    "update": [
                        [dbname, "update", modelname, "name_last"].join(".")
                    ]
                }
            },
            {
                "data": {"name": "date_created", "prompt": "Created on"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "date_created"].join(".")
                    ],
                    "update": []  // cannot be modified
                }
            },
            {
                "data": {"name": "date_modified", "prompt": "Modified on"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "date_modified"].join(".")
                    ],
                    "update": []  // cannot be modified
                }
            },
            {
                "data": {"name": "defaults", "prompt": "Default Information"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "defaults"].join(".")
                    ],
                    "update": [
                        [dbname, "update", modelname, "defaults"].join(".")
                    ]
                }
            },
            {
                "data": {"name": "addresses", "prompt": "Addresses"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "addresses"].join(".")
                    ],
                    "update": [
                        [dbname, "update", modelname, "addresses"].join(".")
                    ]
                }
            },
            {
                "data": {"name": "emails", "prompt": "Email Addresses"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "emails"].join(".")
                    ],
                    "update": [
                        [dbname, "update", modelname, "emails"].join(".")
                    ]
                }
            },
            {
                "data": {"name": "phone_numbers", "prompt": "Phone Numbers"},
                "permissions": {
                    "public": false,
                    "read": [
                        [dbname, "read", modelname, "phone_numbers"].join(".")
                    ],
                    "update": [
                        [dbname, "update", modelname, "phone_numbers"].join(".")
                    ]
                }
            }
        ],
        "template_data": {
            "create": [
                {"name": "name_first", "prompt": "First Name", "placeholder": "First Name", "value": ""},
                {"name": "name_last", "prompt": "Last Name", "placeholder": "Last Name", "value": ""},
                {
                    "name": "addresses",
                    "prompt": "Address(es)",
                    "value": [
                        [
                            {"name": "label", "prompt": "Label", "placeholder": "Label", "value": ""},
                            {"name": "line_1", "prompt": "Line 1", "placeholder": "Line 1", "value": ""},
                            {"name": "line_2", "prompt": "Line 2", "placeholder": "Line 2", "value": ""},
                            {"name": "city", "prompt": "City", "placeholder": "City", "value": ""},
                            {"name": "state", "prompt": "State", "placeholder": "State", "value": ""},
                            {"name": "zip", "prompt": "Zip", "placeholder": "Zip", "value": ""},
                            {"name": "country", "prompt": "Country", "placeholder": "Country", "value": ""}
                        ]
                     ]
                },
                {
                    "name": "emails",
                    "prompt": "Email(s)",
                    "value": [
                        [
                            {"name": "label", "prompt": "Label", "placeholder": "Label", "value": ""},
                            {"name": "email", "prompt": "Email", "placeholder": "Email", "value": ""}
                        ]
                    ]
                },
                {
                    "name": "phone_numbers",
                    "prompt": "Phone Number(s)",
                    "value": [
                        [
                            {"name": "label", "prompt": "Label", "placeholder": "Label", "value": ""},
                            {"name": "number", "prompt": "Phone Number", "placeholder": "Phone Number", "value": ""}
                        ]
                    ]
                }
            ],
            "update": []
        },
        "template_meta": {
            "create": {
                "permissions": {
                    "public": false,
                    "read": [],
                    "write": []
                },
                "validators": {}
            },
            "update": {
                "permissions": {
                    "public": false,
                    "read": [],
                    "write": []
                },
                "validators": {}
            }
        }
    }
};