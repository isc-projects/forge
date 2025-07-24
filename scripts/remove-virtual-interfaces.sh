#!/bin/bash

set -eu

# Ensure that the script is run as root.
(( EUID != 0 )) && exec sudo -- "${0}" "${@}"

interface_count=${1}

# Default parameters
test -z "${show_only+x}" && show_only=false

# Show only?
if ${show_only}; then
  s='echo'
else
  s=
fi

# Namespaces
namespaces=( netns clientns serverns )

# Support only one set of namespaces for now.
m=

# Remove interfaces.
for i in '' $(seq 2 ${interface_count}); do
  for n in client server; do
    if ip link show "bveth${m}${n}${i}" &> /dev/null; then
      ${s} ip link delete "bveth${m}${n}${i}"
    fi
    if ip link show "veth${m}${n}${i}" &> /dev/null; then
      ${s} ip link delete "veth${m}${n}${i}"
    fi
    for ns in "${namespaces[@]}"; do
      if ip netns exec ${ns}${m} ip link show "veth${m}${n}${i}" &> /dev/null; then
        ${s} ip netns exec ${ns}${m} ip link delete "veth${m}${n}${i}"
      fi
    done
  done
done

# Remove bridge.
if ip link show bridge &> /dev/null; then
  ${s} ip link set bridge down
  ${s} ip link delete dev bridge type bridge
fi

# Remove namespaces.
for ns in "${namespaces[@]}"; do
  if test "$(ip netns list | grep -Ecw "${ns}")" = 1; then
    ${s} ip netns delete "${ns}${m}"
  fi
done
