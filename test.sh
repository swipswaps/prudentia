#!/bin/bash

python -c 'import sys; print sys.real_prefix' 2>/dev/null && INVENV=1 || INVENV=0

if [ ${INVENV} == 0 ]; then
  echo -e "No active Virtual Environment.\n"
  if [ ! -d "./p-env/" ]; then
    virtualenv p-env
  fi

  source ./p-env/bin/activate

  pip install -q -r ./requirements-dev.txt
else
  echo -e "Virtual Env active.\n"
fi

export PRUDENTIA_USER_DIR=.
export PRUDENTIA_LOG=

rm -rf tests/envs tests/cover

nosetests -c nose.cfg $@
