#!/usr/bin/env bash

trap "" SIGHUP

doxygen_path=$(dirname $(readlink -f $0))

# Choose which libraries to recompile.  A handful of special keywords (shown 
# below) can be used to specify particular sets of libraries.  By default, 
# every library is recompiled.
#   
#   none: Just recompile the search index.
#   sandbox: Compile the sandbox projects.

all_libraries="utilities core protocols main"
pull_needed="false"

if [ $# -eq 0 ]; then
    chosen_libraries=$all_libraries
    pull_needed="true"
elif [ $1 = "none" ]; then
    chosen_libraries=""
elif [ $1 = "sandbox" ]; then
    all_libraries="sandbox/core sandbox/protocols"
    chosen_libraries=$all_libraries
else
    chosen_libraries=$*
    pull_needed="true"
fi

# Pull in new changes from the master repository if necessary.  Since this may 
# cause the contents of the local repository to change, care should be taken if 
# this script is not working with its own checkout of rosetta.  If the update 
# fails, the whole script will abort immediately.

if [ $pull_needed = "true" ]; then
    (cd "symlinks/rosetta"; git pull --ff-only)
    [ $? -ne 0 ] && exit
fi

# Invoke doxygen on each library that was selected.  Because the documentation 
# is configured to used tag files by default, the libraries with the fewest 
# dependencies should be recompiled first.

cd $doxygen_path

for library in $chosen_libraries; do
    html_directory="symlinks/html/$library"
    master_config="doxygen_config/Doxyfile"
    library_config="doxygen_config/$library/Doxyfile"
    version_config="PROJECT_NUMBER = $(cd symlinks/rosetta; git rev-parse --short HEAD)"

    mkdir -p $html_directory
    rm -rf $html_directory/*
    (cat $master_config $library_config; echo $version_config) | doxygen -
done

# Regenerate the search index.  This includes every library, even those that 
# were not recompiled just above.

search_data=""

for library in $all_libraries; do
    search_data="$search_data doxygen_config/$library/searchdata.xml"
done

search_engine/indexer.py -o symlinks/index $search_data

ln -sf $(readlink -f search_engine/search.py) symlinks/index
ln -sf $(readlink -f search_engine/helpers.py) symlinks/index
