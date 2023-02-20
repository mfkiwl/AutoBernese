
Documentation for our internal developers.

## Development environment

We use MambaForge to create a development environment.

With the mamba command, you can create the needed tools by building an
environment from the environment-dev.yml file in the root of the Git archive.


## Documentation

The documentation is built using MkDocs with the Material extension. The
lightbox feature is installed using PIP from the mamba environment.

### Visualise and Build the Diagrams

The architecture and overall functionality is viaualised using the C4-model tool
Structurizr.

A single [workspace][STRUCTURIZR-WORKSPACE-DSL] contains a collection of
software systems, the main system's container and their components.

[STRUCTURIZR-WORKSPACE-DSL]:
    https://github.com/sdfidk/autobernese/workspace/structurizr/workspace.dsl

The diagrams are produced using the docker container for [Structurizr
Lite][STRUCTURIZR-LITE], and the generated images are manually created from the
web application accessing the workspace file.

[STRUCTURIZR-LITE]: https://structurizr.com/help/lite

Command for running it in development:

```sh
docker run -d -it --rm -p 8080:8080 -v /path/to/git/AutoBernese/workspace/structurizr:/usr/local/structurizr structurizr/lite
```

For VS Code, there is a syntax extension called **Structurizr DSL syntax
highlighting** from publisher *ciarant* that is useful, when editing the
workspace file.

!!! note "Note"

    Running the docker container above for the first in a directory which does not
    already have a `workspace.dsl` file, a new file is created with root ownership.

    In this case, change the permissions on the `workspace.dsl` to give yourself
    write permissions for the file.