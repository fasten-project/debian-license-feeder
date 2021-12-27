# debian-license-feeder

This tool provide a Flask endpoint that takes as input a version of a package, and calling Debian APIs retrieves license information at file level.

The REST API method provided makes use of SQL statements to augment the fasten knowledge base.

The `metadata` field of `package_versions` and `files` tables will be augmented with the license information retrieved.
