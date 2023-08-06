========================
NPM Release Instructions
========================

------------
Pre-Releases
------------

Based on https://survivejs.com/maintenance/packaging/publishing/#publishing-a-pre-release-version

    - Change version in package.json to corresponding version in setup.py
    - You can also use `npm version 3.0.0-beta1` - This will change the version in package.json and create a git tag.
    - `npm publish --tag beta` - Publish the package under beta tag.
    - Mark beta release as latest with `npm dist-tag add @plone/plonetheme-barceloneta-base@3.0.0-beta1 latest``

To consume the test version, users have to use `npm install @plone/plonetheme-barceloneta-base@beta`.
