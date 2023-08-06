.. contents:: Table of Contents:


About
-----

sbo-create, it's a tool that creates easy, fast and safe SlackBuilds files scripts.

This tool is for everyone, but maintainers will be going to love it!

Enjoy!


Features
________

- Preloaded SlackBuilds templates.
- Checking for already SlackBuilds in the repository and the distribution.
- Autocorrect the quote marks for the .info file.
- Auto-importing the SlackBuild script name.
- Auto-importing the text from the slack-desc file into the README.
- Auto-importing the maintainer data to the .SlackBuild script.
- Auto-importing the version to the .SlackBuild script.
- Auto-importing and checking the checksum signature to the .info file.
- Auto-create all the necessary files for your SlackBuild package.


Screenshot
__________

.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-create/img_menu.png
    :target: https://gitlab.com/dslackw/sbo-create

.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-create/img_info.png
    :target: https://gitlab.com/dslackw/sbo-create

.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-create/img_slack_desc.png
    :target: https://gitlab.com/dslackw/sbo-create



Install
-------

.. code-block:: bash

    $ tar xvf sbo-create-2.0.6.tar.gz
    $ cd sbo-create-2.0.6
    $ ./install.sh

    or

    $ slpkg install sbo-create


Requirements
------------

- python3-pythondialog >= 3.5.3


Usage
-----

.. code-block:: bash

    Usage: sbo-create [OPTIONS]

    Optional arguments:
      -n, --prgnam NAME          Set the name of the SlackBuild.
      -e, --prg-version VERSION  Set the version of the SlackBuild.
      -t, --template TEMPLATE    Set the SlackBuild template:
                                 templates={autotools, cmake, perl, python,
                                            rubygem, haskell, meson}
      -f, --create-files         Creates the necessary files and exit:
                                 files={<prgnam>.SlackBuild, <prgnam>.info,
                                        README, slack-desc}.
      -m, --maintainer           Edit the maintainer file.
      -d, --download             Download source files listed in the .info file.
      -c, --check NAME           Check if the SBo exist in the repository.
      -h, --help                 Display this message and exit.
      -v, --version              Show version and exit.

The first step is to create your profile, be entering the maintainer data:

.. code-block:: bash

    $ sbo-create --maintainer

For a new project, you should create at first a new folder with the same name as
the project.
For an existing project, come into the folder and start to edit, just run `sbo-create`.

Alternative you can run the below command to create all the necessary files:

.. code-block:: bash

    $ sbo-create --prgnam sboname --prg-version 1.0.0 --template python --create-files
    Files created:

      > slack-desc
      > sboname.info
      > README
      > sboname.slackbuild


It's good you know before you start, please visit here: `HOWTO <https://slackbuilds.org/howto/>`_


Note
----
The :code:`sbo-create` tool, checks for installed SlackBuilds.


Donate
------

If you feel satisfied with this project and want to thank me, treat me to a coffee ☕ !

.. image:: https://gitlab.com/dslackw/images/raw/master/donate/paypaldonate.png
   :target: https://www.paypal.me/dslackw


Copyright 
---------

- Copyright © 2015-2023 Dimitris Zlatanidis
- Slackware ® is a Registered Trademark of Patrick Volkerding.
- Linux is a Registered Trademark of Linus Torvalds.
