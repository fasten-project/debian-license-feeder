# debian-license-feeder

This tool provides a Flask endpoint that takes a version of a package as input, and calling Debian APIs retrieves license information at the file level.

The REST API method provided uses SQL statements to augment the fasten knowledge base.

The `metadata` field of `package_versions` and `files` tables will be augmented with the license information retrieved.
