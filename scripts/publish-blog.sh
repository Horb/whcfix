#!/bin/sh

echo "Publishing /blog to /dist";

rm ./dist/blog/*.html

find ./blog -name '*.md' -exec \
    bash -c \
        'python -m markdown -x extra "$1" > "./dist/blog/` basename "$1" ".md" `.html";' \
        "bash" {} ";"
