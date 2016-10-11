#!/bin/bash

for TARGET in $(find stages -mindepth 1 -maxdepth 1 -type d | xargs -n1 basename | sort -n | uniq); do
  echo "${TARGET}:"
  echo -e '\t$(FABRIC)\n'
done
