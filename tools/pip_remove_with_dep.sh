#!/bin/bash

# IMPORTANT - only works with SINGLE DEEP dependency packages

printf "name of package? "
read PACKAGE

for dep in $(pip show $PACKAGE | grep Requires | sed 's/Requires: //g; s/,//g') ; do 
	pip uninstall -y $dep
done
pip uninstall -y $PACKAGE