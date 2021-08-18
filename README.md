# Chalice, Svelte and Postgres Webstack

This is a minimal example of a full-stack serverless web architecture. Every
part of this application stack can be developed locally and then pushed to AWS.

Poetry is used as the python package manager.


## Root directory

```
$ make install
```

* Installs project-wide dependecies.
* Installs python modules via poetry.

```
$ make build-all [stage=<stage>]
```

* Goes into each of the subdirectories and runs `$ make build stage=<stage>`.
* If <stage> is not provided, it uses 'local'.


## /config

A custom python system is used
to centralize the config files across the components. Throughout project you'll find `abc.gen.xyz` files that are used to generate corresponding `abc.xyz` files. They do so by accessing a centralized `config` object generated at build time in the `/config` directory, and using a custom syntax to access values in that object. The centralized `config` object also has syntactic sugar that can reach into the other directories and load in their locally generated files, like build information.

```
$ make print [stage=<stage>]
```

* Prints the config object to stdout.
* If <stage> is provided, it uses the config object for that stage, otherwise all stages.

```
$ make apply path=<path> [stage=<stage>]
```

* Generates the config object and uses it to generate all of the `abc.xyz` files from the  `abc.gen.xyz` files in the directory specified with `<path>`. Generally used with a `<stage>` argument.


## /db

The database and database management module. Supports local development.

```
$ make install
```

* Installs docker and pulls the `postgres` image.

```
$ make build [stage=<stage>]
```

* if `stage=local`, builds a `postgres` docker instance for local development.
* if `stage={dev,beta,prod}`, builds a `postgres` RDS instance and a database with the name specified in `/config`.

```
$ make start
```

* starts the local docker instance.

```
$ make stop
```

* stops the local docker instance.

```
$ make clear
```

* deletes the local docker image.

```
$ make update
```

* applies all of the updates in `/db/updates` to the target stage database. Keeps track of last update and only applies the newest updates.
* if `stage=local`, applies updates to the docker instance.
* if `stage={dev,beta,prod}`, applies updates to the corresponding RDS instance.
* The update file name follows the syntax: `<update_#>[.<stage,...>].{sql,json}`. Stages can be listed as the middle argument and the update will only apply to those stages. SQL files will run as expected. JSON files will perform a data upload.

```
$ make rebuild
```

* Clears and rebuilds the docker instance.
* Is the equivalent of `make stop; make clear; make build; make start; make update;`.
* Currently only used in the `local` stage.


## /api

A module to deploy and manage a serverless python API, using the chalice software. Supports local development.


```
$ make install
```

* Installs python modules via poetry.

```
$ make build stage=<stage>
```

* Prepares the module to be deployed.
* Applies the config module to the `/api` directory.
* Exports the poetry dependencies in the format expected by chalice.

```
$ make deploy stage=<stage>
```

* Deploys the API to AWS using Chalice.

```
$ make local
```

* Runs the API with hot reloading on localhost for local dev.

```
$ make clean stage=<stage)
```

* Destroys that stage of the API in AWS.


## /ui

A svelte SPA deployable serverless to the AWS cloud. Supports local development.

```
$ make install
```

* installs dependencies, currently just `npm`.

```
$ make build
```

* applies the configuration module to `/ui`.
* If `stage=local`, installs the `npm` packages.
* If `stage={dev,beta,prod}`, compiles the svelte code into bundles for deployment.

```
$ make local
```

* runs the svelte code with hot reloading on localhost for local dev.

```
$ make serve
```

* runs the svelte code without hot reloading on localhost.

```
$ make deploy
```

* Pushes the bundles to S3
* Builds the CloudFront Distribution (with Route53 etc. integration) to serve the bundles.
