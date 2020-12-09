#!/bin/sh

find ./blog -name '*.md' -exec \
    bash -c \
        'python3 -m markdown -x extra "$1" > "./dist/blog/` basename "$1" ".md" `.html";' \
        "bash" {} ";"
