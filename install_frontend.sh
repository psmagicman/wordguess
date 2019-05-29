#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "#### CLEANING UP ####"
rm -rf wordguess/static/*
rm wordguess/templates/index.html
cd frontend_src

echo "#### BUILDING FRONTEND ####"
npm install
npm run build

echo "#### MOVING FILES ####"
cd ..
mv frontend_src/build/index.html wordguess/templates/index.html
mv frontend_src/build/static/* wordguess/static/
mv frontend_src/build/* wordguess/static/

echo "#### DONE ####"