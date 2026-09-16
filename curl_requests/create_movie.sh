#!/bin/sh

curl -X POST -d '{"title":"Harry Potter", "director":"me", "release_year": 2026}' -H "Content-Type: application/json" http://localhost:3000/movies
