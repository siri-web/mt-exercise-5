#! /bin/bash

scripts=$(dirname "$0")
base=$scripts/..

tools=$base/tools
mkdir -p $tools

# install Moses scripts for postprocessing

git clone https://github.com/bricksdont/moses-scripts $tools/moses-scripts
