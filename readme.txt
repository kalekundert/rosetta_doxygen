This is a collection of scripts meant to quickly compile the API documentation 
for Rosetta.  Because Rosetta is such a large project, simply running doxygen 
on the entire thing can take days (or weeks) to finish.  It is much faster to 
run doxygen of several subsets of Rosetta and to link together the resulting 
documentation.

These scripts are configured to run doxygen independently on the core library, 
the protocols library, and all the other libraries.  There is also a main 
pseudo-library that serves to link the other three libraries together.  The 
main library contains no code, just formatted text to explain how the 
documentation can be used.

The documentation can be built by running the build_doxygen.sh command.  Prior 
to commit a2cd38, however, this script will choke on a comment in the Mersenne 
Twister code which contains unicode.  This script also expects that you have 
manually filled in the symlinks directory, which should contain links to a 
rosetta installation, an HTML directory, and a CGI-BIN directory.  Consult the 
readme file in the symlinks directory for more information.

If your web server is setup to execute CGI-BIN scripts, a reasonably 
sophisticated search engine will be installed when build_doxygen.sh is run.  
You can view these scripts in the search_engine directory.  These scripts 
require that the python binding to the xapian library be installed.

Note that these scripts haven't been written to be especially general or easy 
to use.  So expect that you'll have to read some code and figure out what's 
going on, to an extent.  I was personally interested in serving the API 
documentation on the web, so everything is kinda geared towards doing that.  If 
you find a way to generalize things, please let me know about them (via a pull 
request) so I can improve the code.
