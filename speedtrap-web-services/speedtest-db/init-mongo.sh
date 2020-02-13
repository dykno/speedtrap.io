#!/bin/bash

mongo <<EOF

db.createUser(
    {
        user    : '$MONGO_INITDB_USERNAME',
        pwd     : '$MONGO_INITDB_PASSWORD',
        roles   : [
            {
                role    : "readWrite",
                db      : "speedtest"
            }
        ]
    }
)

db.createCollection("results")
EOF
