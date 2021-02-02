# python_svelte_serverless_stack

This is a minimal example of a full-stack serverless web architecture. Every
part of this application stack can be developed locally and then pushed to AWS.

The example being used is a grocery store app.


##  Getting started

1.  Install the dependencies for your OS:

Ubuntu:

```
sudo apt install python3.8
sudo apt install python3-pip
sudo apt install node
sudo apt install npm
```

2.  Clone and initialize the repo:

```
git clone git://github.com/samhaaf/python_svelte_serverless_stack.git ./stack
cd stack
make init
```

3.  Fill out each of the `private.json` configuration files in `./config`


##  Local development

To run the flask backend framework in debug mode:

```
make run-flask
```

To run the svelte frontend framework in dev mode:
```
make run-svelte
```


##  Serverless deployment

1.  Build the app

```
make build
```


2.  Deploy the entire stack to a specific infrastructure:

```
make deploy stage={dev,stage,prod}
```
