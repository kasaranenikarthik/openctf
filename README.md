OpenCTF
=======

This repository houses the source code for the 2017 EasyCTF contest platform. Over time, this platform will be generalized to be easily adaptable to other CTF competitions. The platform itself contains a plethora of features, including:

* Easy-to-use setup interface.
* In-browser administration panel.
* Auto-generated challenges per team.
* Programming judge.

Project Structure
-----------------

This repository is like the control center of the entire platform. It contains a `docker-compose.yml` file that lists all of the components that are required by the platform. The components are listed here:

* [`easyctf/openctf-server:latest`](https://github.com/easyctf/openctf-server) - The main web application.
* [`easyctf/openctf-filestore:latest`](https://github.com/easyctf/openctf-filestore) - The static file server.
* [`easyctf/openctf-judge:latest`](https://github.com/easyctf/openctf-judge) - The programming judge manager.
* [`easyctf/openctf-jury:latest`](https://github.com/easyctf/openctf-jury) - The programming grader jury.

You don't need to pull these git repositories in order to use OpenCTF, since these images have been pushed to Docker Cloud for distribution. The `docker-compose.yml` file is already pulling from Docker Cloud by default.

Installation
------------

Since this platform runs using Docker, the easiest way to get started is installing Docker on your computer. In addition, install Docker Compose to take advantage of the easy project setup that Docker Compose provides.

Before we go ahead and start up the containers, we have to provide a `.env` file that contains important configuration options. Ideally, some of these options will be moved to the settings page, but this file is required to start the server. This `.env` file should be placed in the same directory as `docker-compose.yml`. An example .env file has been provided for you.

Once you've created this file, you're ready to start the Docker containers with the following command:

```bash
$ docker-compose up -d
```

This will automatically create and start all the containers, creating the necessary links and mounting the necessary volumes. At this point, navigate to `/setup` on wherever you are serving the platform to perform some basic configuration and set up the initial administrator account.

Contact
-------

Authors: Michael Zhang, David Hou, James Wang

Copyright: EasyCTF Team

License: TBD

Email: team@easyctf.com