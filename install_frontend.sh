#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "#### CLEANING UP ####"
rm -rf hangman/static/*
rm hangman/templates/index.html
cd frontend_src

echo "#### BUILDING FRONTEND ####"
npm install
npm run build

echo "#### MOVING FILES ####"
cd ..
mv frontend_src/build/index.html hangman/templates/index.html
mv frontend_src/build/static/* hangman/static/
mv frontend_src/build/* hangman/static/

echo "#### DONE ####"
