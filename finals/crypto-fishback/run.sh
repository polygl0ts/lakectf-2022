#!/bin/sh

set -e

if [ ! -e secret.asc ]; then
	gpg --batch --passphrase '' --quick-gen-key epfl-ctf-bot@protonmail.com
	gpg --batch --passphrase '' --armor --export epfl-ctf-bot@protonmail.com > public.asc
	gpg --batch --passphrase '' --armor --export-secret-key epfl-ctf-bot@protonmail.com > secret.asc
fi
if [ ! -e flag.asc ]; then
	echo -n $FLAG | gpg --batch --rfc2440 --compression-algo none --armor -ef public.asc > flag.asc
fi
unset FLAG

poetry run python3 server.py
