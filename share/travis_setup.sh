#!/bin/bash
set -evx

mkdir ~/.cspn

# safety check
if [ ! -f ~/.cspn/.cspn.conf ]; then
  cp share/cspn.conf.example ~/.cspn/cspn.conf
fi
