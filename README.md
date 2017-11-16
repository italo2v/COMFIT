COMFIT (Cloud and Model based IDE for the Internet of Things) joins Eclipse FLUX and Web2Compile projects in one tool.

The Web2Compile project can be found in https://github.com/italo2v/web2compile.

The [Eclipse Flux](https://wiki.eclipse.org/Flux) development tool messaging server.
For more details, see the [Flux Repository Readme](https://github.com/eclipse/flux).

COMFIT is a development environment for the Internet of Things and supports code generation, simulations, and code compilation of applications for TinyOS and ContikiOS applications.

COMFIT uses GitHub authentication to provide users access, so you will need a GitHub Client ID, Secret and Redirect URI to comply with OAuth (you must change the files github-secret.js and web2compile/webserver.py).

Tutorial to create github secret: https://auth0.com/docs/connections/social/github

You will also need a MongoDB database, NodeJS and RabbitMQ Connector installed to run FLUX.

Download and install RabbitMQ from: https://www.rabbitmq.com/

Rename the folder web2compile/projects/italo2v to your GitHub account login to see some examples of a Hello Word in ContikiOS and a Blink in TinyOS.

Run mongod and rabbitmq-server to start the database and the message broker.

Just run startup-all-in-one.js to provide FLUX platform, Orion Editor (http://localhost:3000).
Run web2compile/webserver.py to provide TinyOS and ContikiOS simulations (http://localhost:8080/).

Enjoy :)
