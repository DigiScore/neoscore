#!/bin/bash

# Script for Travis to automatically build and deploy
# the website to the brown-site repository
# Based on https://gist.github.com/domenic/ec8b0fc8ab45f39403dd

set -e # Exit with nonzero exit code if anything fails

SOURCE_BRANCH="master"
TARGET_BRANCH="master"

# Pull requests and commits to other branches shouldn't try to deploy site.
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping site deploy."
    exit 0
fi

echo "Beginning site deploy."

# Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
echo "Decrypting site ssh key"
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in doc/site_deploy_key.enc -out deploy_key -d
echo "Adding decrypted ssh key"
chmod 600 deploy_key
eval `ssh-agent -s`
ssh-add deploy_key

TARGET_REPO_SSH='git@github.com:ajyoon/brown-site.git'
git clone $TARGET_REPO_SSH ../target
cd ../target

find . -not -path "\./\.git/*" -type f \
     -not -path "\./README.md" \
     -not -path "\./LICENSE" \
     -not -path "\./CNAME" \
     -print0 | xargs -0 rm --
cd ../brown

echo "Installing doc generator dependencies"
pip3 install -r doc/doc_requirements.txt
echo "Generating site."
python3 doc/generator.py site
echo "Moving site to target"
cp -r site/* ../target/

cd ../target
git config user.name "travis-ci-doc-build-robot"
git config user.email "$COMMIT_AUTHOR_EMAIL"

# If there are no changes to the compiled out (e.g. this is a README update) then just bail.
git add -N --all .
if [ -z `git diff HEAD --exit-code` ]; then
    echo "No changes to the output on this push; exiting."
    exit 0
fi

# Commit the "changes", i.e. the new version.
# The delta will show diffs between new and old versions.
echo "Committing site changes"
git add .
git commit -m "Deploy site"

echo "Pushing site changes"
# Now that we're all set up, we can push.
git push $TARGET_REPO_SSH $TARGET_BRANCH

echo "Site deployed successfully."
