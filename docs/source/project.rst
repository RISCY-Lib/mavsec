MavSec Projects
================

MavSec projects consist of the following properties:
- `name` (string): The name of the project.
- `description` (string): A description of the project.
- `version` (string): The version of the project.
- `properties` (list[Properties]): A list of properties that the project has.

MavSec Projects can be created two ways:
- Through the GUI
- Through a Markup Language (TOML, YAML, JSON, etc.)

Markup Language Creation
------------------------

.. code-block:: toml

    [project]
    name = "example_project_toml"
    version = "0.1.2"
    description = "An example project using toml"

    [properties]
        [properties.example_property_1]
        description = ""
        ptype = "SecureKeyProperty"
        preconditions = ""
        metadata = {key_loc: "dut.key", public_bus: "$OUTPUTS"}

        [properties.example_property_2]
        description = ""
        ptype = "SecureKeyGenProperty"
        preconditions = ""
        metadata = {public_key_loc: "dut.key", public_bus: "$OUTPUTS"}

.. code-block:: yaml

    project:
        name: "example_project_toml"
        version: "0.1.2"
        description: "An example project using toml"

    properties:
        example_property_1:
            description: ""
            ptype: "SecureKeyProperty"
            preconditions: ""
            metadata:
            key_loc: "dut.key"
            public_bus: "$OUTPUTS"
        example_property_2:
            description: ""
            ptype: "SecureKeyGenProperty"
            preconditions: ""
            metadata:
            public_key_loc: "dut.key"
            public_bus: "$OUTPUTS"



GUI Creation
------------
