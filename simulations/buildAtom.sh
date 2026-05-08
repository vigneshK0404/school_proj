#!/bin/bash

set -e  # stop on error

echo "Compiling..."

g++ testGL.cxx glad.c -o testGL \
-I/usr/local/include \
/usr/local/lib/libglfw3.a \
-lGL -ldl -lpthread \
-lX11 -lXrandr -lXi -lXxf86vm -lXcursor -lm

echo "Running..."

./testGL
