#!/bin/bash

get_connected_users() {
    users=$(who | cut -d' ' -f1 | sort | uniq)
    echo "{"
    echo -n "  \"users\": ["
    first=true
    for user in $users; do
        if $first; then
            first=false
        else
            echo -n ", "
        fi
        echo -n "\"$user\""
    done
    echo "]"
    echo "}"
}

get_connected_users