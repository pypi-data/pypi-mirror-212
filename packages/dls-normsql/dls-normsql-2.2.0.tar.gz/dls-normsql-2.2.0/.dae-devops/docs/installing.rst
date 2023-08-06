.. # ********** Please don't edit this file!
.. # ********** It has been generated automatically by dae_devops version 0.5.3.
.. # ********** For repository_name dls-normsql

Installing
=======================================================================


You will need python 3.9 or later. 

On a Diamond Light Source internal computer, you can achieve Python 3.9 by::

    $ module load python/3.9

You can check your version of python by typing into a terminal::

    $ python3 --version

It is recommended that you install into a virtual environment so this
installation will not interfere with any existing Python software::

    $ python3 -m venv /scratch/$USER/myvenv
    $ source /scratch/$USER/myvenv/bin/activate
    $ pip install --upgrade pip


You can now use ``pip`` to install the library and its dependencies::

    $ python3 -m pip install dls-normsql

If you require a feature that is not currently released you can also install
from git::

    $ python3 -m pip install git+https://gitlab.diamond.ac.uk/kbp43231/dls-normsql.git

The library should now be installed and the commandline should be available.
You can check the version that has been installed by typing::

    $ dls-normsql --version
    $ dls-normsql --version-json

.. # dae_devops_fingerprint a2fe8dfbc79c151a5b899b244a529aa6
