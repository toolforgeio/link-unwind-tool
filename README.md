# HELLO TOOLFORGE

## Introduction

This project is an example implementation of a
[ToolForge](https://app.toolforge.io/) tool in Python. It uses the
[toolforge](https://github.com/toolforgeio/toolforge4py) library for QOL.

This "Hello Toolforge" template is released FREE TO USE under the Apache 2.0
License for building ToolForge tools. Tool developers may choose their own
licenses for their tools, including closed source.

## Building

Simply running the following command will generate the required Docker image:

    make

Note that this example also includes GitHub actions for CI/CD.

## Creating Your Own Tool

To adapt this example into a real tool, the user should:

1. Create a [ToolForge](https://www.toolforge.io) account and create a new
   container. Call it whatever you like! Note the container's container location
   and ID.
2. Update the Dockerfile to reflect the container's name and environment.
3. Update the manifest to reflect the tool's inputs, outputs, and parameters.
4. Write the code to implement the tool.
5. Build, push, and run in ToolForge!