Choose your own confession server
=================================

Create a virtual env:

  $ python virtualenv.py cyoc

Clone the repo

  $ cd cyoc
  $ git clone git@github.com:latteier/cyoc.git

Setup:

  $ bin/python cyoc/setup.py develop

Run the server:

  $ bin/pserve develop.ini

Notes
-----

- very incomplete
- no persistence
