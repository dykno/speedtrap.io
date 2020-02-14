#!/bin/bash
# Script to initialize the MongoDB service
# in the event that the DB disappears

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
