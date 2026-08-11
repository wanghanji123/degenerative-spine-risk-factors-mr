# Repository file manifest

`REPOSITORY_FILE_MANIFEST.csv` records the relative path, byte size, and SHA-256 checksum for every public repository file present during packaging, excluding itself, Git metadata, and transient Python bytecode.

The manifest supports transfer and archival integrity checks. A changed checksum after an intentional revision is expected and should be followed by regenerating the manifest.
