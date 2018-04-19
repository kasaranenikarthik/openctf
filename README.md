OpenCTF
=======

[![Build Status](https://travis-ci.org/easyctf/openctf.svg?branch=master)](https://travis-ci.org/easyctf/openctf)

Under construction.

Find the old version in the `old` branch.

Installation
------------

Binaries will be shipped when the project reaches a working state. Follow the steps in "Building from Source" for now.

Building from Source
--------------------

Make sure you have the following dependencies installed:

* **Go** (the main server will be delivered as a Go-compiled binary)
* **Node/NPM** (this is used to build the user-facing site)
* list may expand

```bash
npm install
```

This will install all of the dev dependencies that are required to compile the source files.

```bash
npm run build
```

This will build the entire project into a binary called `openctf` in the current folder.

```bash
./openctf --help
```

You're good to go! This single binary is responsible for everything, so run it with `--help` to figure out how to use it.

Contact
-------

Authors: Michael Zhang, David Hou, James Wang

Copyright: EasyCTF Team

License: TBD
