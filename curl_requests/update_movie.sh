#!/bin/sh

curl -X PUT -d '{"id": 1, "title":"Sharknado", "director":"you", "release_year": 2000}' -H "Content-Type: application/json" http://localhost:3000/movies
