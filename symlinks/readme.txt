This directory should contain three symlinks.  These links are used by doxygen 
to easily adapt to different directory layouts on different servers.

The first symlink should be called 'rosetta'.  It should link to the 'source' 
directory within some rosetta installation.  In other words, 'rosetta/src/core' 
should exist.

The second symlink should be called 'html'.  It should link to a directory that 
is readable by the web server.  Inside this directory, a subdirectory will be 
created for each library in rosetta (e.g. core, protocols, etc.).

The third symlink should be called 'index'.  The search index and the search 
script will be placed in this directory, so the web server must be able to read 
it and must allow CGI scripts to be executed from within it.  Usually it is 
considered good practice to place this directory outside the website root.  The 
SEARCHENGINE_URL option in 'doxygen_config/Doxyfile' must be set to be 
compatible with this symlink.
