0) Check if you have Python 2.6 or 2.7 installed on your machine. If you have a different version (i.e. Python 3.X), complete Steps A-D before moving to Step 1. If you do use system python of version 2.6 or 2.7, continue directly to Step 1

=====   Instructions for setting up python virtual env if using python version =/= 2.6 or 2.7   =====

A) Check /usr/bin/python* for the python executables available on your system. Hint, we want to use something like 2.7. If you don't have this, get it somehow

B) Create the virtual environment, e.g. $> virtualenv --python=/usr/bin/python2.7 <name of virtualenv>

C) Activate the environment, e.g. $> source <name of virtualenv>/bin/activate

======    Congratulations on your new virtual enviroment. You'll need to activate this every time you want to generate something in madgraph    ======

1) Get the most recent version of MG5 from https://launchpad.net/mg5amcnlo . Currently this is MG5_aMC_v2.6.5.tar.gz

2) Unpack tarball, e.g. $> tar -xzf MG5_aMC_v2.6.5.tar.gz

3) Move to MadGraph directory, e.g. $> cd MG5_aMC_v2_6_5/

4) Launch MadGraph, e.g. $> ./bin/mg5_aMC

5) Install pythia8 (this will take awhile) from mg command prompt, e.g. $> install pythia8

6) Install Delphes (this will take time but not as much as pythia) from mg command prompt, e.g. $> install Delphes
