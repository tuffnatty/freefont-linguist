fontforge -script $@
# fontforge as a script interpreter.
# Exists because Linux /usr/bin/env won't allow arguments such as -script
# on the command line, and it was desirable to launch fontforge scripts
# as executables.
