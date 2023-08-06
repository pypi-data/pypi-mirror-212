#!/usr/bin/env bash

set -e

# Only do this if we aren't initializing the config or the db
# Safe to do even if the db exists already
if [[ "$@" != *"init-config"* && "$@" != *"init-db"* && "$@" != *"--help"* ]]; then
  echo "------------ Initializing config and database"
  qcfractal-server init-db
fi

if [ "$OPENFRACTAL_DO_RUN_MIGRATIONS" == "true" ]; then
  echo "------------ Upgrade database"
  qcfractal-server upgrade-db
fi

echo "------------ Create users if they don't exist already"
for i in {1..10}; do

  ROLE="OPENFRACTAL_USER_${i}_ROLE"
  NAME="OPENFRACTAL_USER_${i}_NAME"
  PASSWORD="OPENFRACTAL_USER_${i}_PASSWORD"

  ROLE_VALUE=${!ROLE}
  NAME_VALUE=${!NAME}
  PASSWORD_VALUE=${!PASSWORD}

  if [[ ! -z ${ROLE_VALUE} && ! -z ${NAME_VALUE} && ! -z ${PASSWORD_VALUE} ]]; then
    opfb create-user-if-not-exist \
      --role ${ROLE_VALUE} \
      --password ${PASSWORD_VALUE} \
      --username ${NAME_VALUE}
  fi

done

# Run with the rest of the arguments
# You can set QCF_DOCKER_COMMAND in an environment variable to specify the command,
# or just pass the arguments to "docker run"
echo "------------ Starting qcfractal-server"
qcfractal-server $@ ${QCF_DOCKER_COMMAND}
