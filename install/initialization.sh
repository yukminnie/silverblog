#!/usr/bin/env bash

if [ -f "initialization.sh" ]; then
    cd ..
fi

echo "Setup directories..."

mkdir ./document
mkdir -p ./config/unix_socks
mkdir -p ./templates/static
mkdir ./templates/include

touch ./templates/include/comment.html
touch ./templates/include/head.html
touch ./templates/include/foot.html

echo "Setup missing configuration files..."

if [ ! -f "./config/menu.json" ]; then
    echo "[]" > ./config/menu.json
fi

if [ ! -f "./config/page.json" ]; then
    echo "[]" > ./config/page.json
fi

if [ ! -f "./uwsgi.json" ]; then
    cp -i ./example/uwsgi.json ./uwsgi.json
fi

echo "Installation complete! "
echo -e "Note: \e[31;1;4mDO NOT\e[0m use \`git clean\` to reset your git repository. This command could potentially cause data loss!"