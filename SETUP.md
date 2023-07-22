# Server Setup

This file details how to get this system going on the server/host side. If you are looking for how to set up the client side, see the README.md file.

## Config

First, you must create a config yml file, with this structure:
```yaml
modules:
  - path: 'kubejs' # Name of folder inside .minecraft folder
    zip_url: 'https://example.com/euclid/packs/kubejs.zip' # URL of zip. See SETUP.md
    version: 1 # Version of module. Should increment on each update.
    id: 'kubejs' # Unique ID for this module.
  - path: 'mods' # Name of folder inside .minecraft folder
    zip_url: 'https://example.com/euclid/packs/mods.zip' # URL of zip. See SETUP.md
    version: 1 # Version of module. Should increment on each update.
    id: 'mods' # Unique ID for this module.
  - path: 'config' # Name of folder inside .minecraft folder
    zip_url: 'https://example.com/euclid/packs/configs.zip' # URL of zip. See SETUP.md
    version: 1 # Version of module. Should increment on each update.
    id: 'config' # Unique ID for this module.
```

Each module has four important parts:

1. `path`: the path to the file within the user's `.minecraft` folder. For example if this is `mods` the zip file's contents will be placed in `.minecraft/mods/`

2. `zip_url`: the URL to download the zip file from. This zip file should be an archive of the CONTENTS of the folder, NOT THE FOLDER ITSELF.

3. `version`: the current version of this module. The client only updates when it's version is lower than this version-- so it must increment on every update.

4. `id`: a UNIQUE identifier for this module. The client uses this to see if it has this module installed, and stores the version based on this value. This ID should never be changed. *Additionally, this should be a valid YAML key

## Update Process

1. Client downloads your config file from a specified url (on your server)

2. Client checks each module and its version against it's local list of modules and versions

3. If the server has a module it does not have, it downloads the zip, creates a folder based on the `path:`, and unzips the zip file to there. It also adds that module and the module's version to its internal config.

4. If the server has a module with a higher `version:` than the client, it downloads the new version from the `zip_url:`, extracting the zip into the `path:`.

#### Update Notes

- Because the client re-downloads the config every time, the `zip_url` can be changed if necessary on each new version of a module.
- Because the client loops though the list of modules the server provides, you can remove a module from your config and not only will it not be a problem, it will not be touched by the client-side updater and you can create a new module in its place to update those files.