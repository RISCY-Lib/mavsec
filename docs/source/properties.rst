Built-In Properties
===================

The following properties are built-in and are always available on all MavSec projects:

SecureKeyProperty
-----------------

The `SecureKeyProperty` is a built-in property that is used to ensure a secure key is correctly stored. This means that the key is not accessible in anyway on a public bus.

Arguments
^^^^^^^^^

- `key_loc` (AnyRtlPath): The hardware location of the key.
- `key_size` (int | None): The size of the key in bits
- `public_bus` (AnyRtlPath): The public bus to which the key is connected.

SecureKeyIntegrityProperty
--------------------------

The `SecureKeyIntegrityProperty` is a built-in property that is used to ensure the integrity of a secure key. This means that the key is not able to be overwritten from the public bus.

Arguments
^^^^^^^^^

- `key_loc` (AnyRtlPath): The hardware location of the key.
- `key_size` (int | None): The size of the key in bits
- `public_bus` (AnyRtlPath): The public bus to which the key is connected.

SecureKeyGenProperty
--------------------

The `SecureKeyGenProperty` is a built-in property that is used to ensure that a secure key is generated in a secure manner. It ensures that the private key is not leaked except as minimally required by the public key. (In a moder secure key generation system, this doesn't reveal any actual information about the key)

Arguments
^^^^^^^^^

- `public_key_loc` (AnyRtlPath): The hardware location of the public key.
- `private_key_loc` (AnyRtlPath): The hardware location of the private key.
- `public_bus` (AnyRtlPath): The public bus to which the key is connected.

SecureExternalMemoryProperty
-----------------------------

Arguments
^^^^^^^^^

- `memory_loc` (AnyRtlPath): The hardware location of the memory.
- `public_bus_input` (AnyRtlPath): The public bus to which the memory is connected.
- `secure_output` (AnyRtlPath | None): The place in hardware where the output is ensured to be secure.

SecureInternalStorageProperty
-----------------------------

Arguments
^^^^^^^^^
- `storage_loc` (AnyRtlPath): The hardware location of the storage.
- `public_bus` (AnyRtlPath): The public bus to which the storage is connected.