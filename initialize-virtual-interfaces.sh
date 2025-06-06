#!/bin/bash

# Ensure that the script is run as root.
(( EUID != 0 )) && exec sudo -- "${0}" "${@}"

script_path=$(cd "$(dirname "${0}")" && pwd)
cd "${script_path}"

interface_count="${1}"

# Default parameters
test -z "${bridged_namespaces+x}" && bridged_namespaces=false
test -z "${interface_count+x}" && interface_count=1
test -z "${namespace_count+x}" && namespace_count=0
test -z "${show_only+x}" && show_only=false

# Sanity checks
if test "${namespace_count}" != 0 && \
   test "${namespace_count}" != 0.5 && \
   test "${namespace_count}" != 1 && \
   test "${namespace_count}" != 2; then
  printf "${RED}%s${RESET}\\n" 'ERROR: namespace_count limited to 0, 0.5, 1 or 2' >&2
  print-usage
  exit 1
fi
if ${bridged_namespaces} && test "${namespace_count}" != 2; then
  printf "${RED}%s${RESET}\\n" 'ERROR: bridged_namespaces is only available with namespace_count 2' >&2
  exit 1
fi

# Remove any previously installed virtual interfaces for idempotency.
./remove-virtual-interfaces.sh "${interface_count}"

# Show only?
if ${show_only}; then
  s='echo'
else
  s=
fi

# Prefixed commands for adding to namespaces
if test "${namespace_count}" = 0 || test "${namespace_count}" = 0.5; then
  ip=
  netns=
  exec=
else
  ip='ip'
  netns='netns'
  exec='exec'
fi

# Namespaces
namespaces=()
if test "${namespace_count}" = 0.5; then
  namespaces=( clientns )
elif test "${namespace_count}" = 1; then
  namespaces=( netns )
elif test "${namespace_count}" = 2; then
  namespaces=( clientns serverns )
fi

# Support only one set of namespaces for now.
m=

# Add namespaces.
for ns in "${namespaces[@]}"; do
  ${s} ip netns add "${ns}${m}"
done

ip link set lo down

# Add and start interfaces.
j=1
k=1
l=$((k + 100))
for i in '' $(seq 2 ${interface_count}); do
  if test "${namespace_count}" = 0 || test "${namespace_count}" = 0.5; then
    ns=
  elif test "${namespace_count}" = 1; then
    ns='netns'
  fi
  if ${bridged_namespaces}; then
    for n in client server; do
      binterface="bveth${m}${n}${i}"
      interface="veth${m}${n}${i}"
      ${s} ip link add "${interface}" type veth peer name "${binterface}"
      ${s} ip link set "${interface}" netns "${n}ns"
      ${s} ip link set "${binterface}" up
      l=$((l + 1))
    done
  else
    ${s} ip link add "veth${m}client${i}" type veth peer name "veth${m}server${i}"
    if test "${namespace_count}" = 0.5; then
      ${s} ip link set "veth${m}client${i}" netns clientns
    elif test "${namespace_count}" = 1; then
      ${s} ip link set "veth${m}client${i}" netns netns
      ${s} ip link set "veth${m}server${i}" netns netns
    elif test "${namespace_count}" = 2; then
      ${s} ip link set "veth${m}client${i}" netns clientns
      ${s} ip link set "veth${m}server${i}" netns serverns
    fi
  fi
  for n in client server; do
    if test "${namespace_count}" = 0 || \
      test "${namespace_count}" = 0.5; then
      ip=
      netns=
      exec=
      ns=
    else
      ip='ip'
      netns='netns'
      exec='exec'
    fi
    if test "${namespace_count}" = 0.5 && test "${n}" = 'client'; then
      ip='ip'
      netns='netns'
      exec='exec'
      ns='clientns'
    elif test "${namespace_count}" = 1; then
      ns='netns'
    elif test "${namespace_count}" = 2; then
      ns="${n}ns"
    fi
    interface="veth${m}${n}${i}"
    ${s} ${ip} ${netns} ${exec} ${ns} ip -4 addr add "192.${j}.2.${k}/24" dev "${interface}"
    ${s} ${ip} ${netns} ${exec} ${ns} ip -6 addr add "2001:db8:${j}::${k}/64" dev "${interface}"
    ${s} ${ip} ${netns} ${exec} ${ns} ip link set dev "${interface}" up
    ${s} ${ip} ${netns} ${exec} ${ns} ip link set lo up
    k=$((k + 1))
  done
  # j=$((j + 1))
done

# Add bridge.
if ${bridged_namespaces}; then
  ${s} ip link add name bridge type bridge
  ${s} ip link set bridge up
  ${s} ip addr add 10.0.0.254/24 broadcast + dev bridge
  ${s} ip addr add 2001:db8:1::ffff/64 dev bridge
  ${s} iptables -t nat -A POSTROUTING -s 10.0.0.254/24 -j MASQUERADE
  for i in '' $(seq 2 ${interface_count}); do
    if ${bridged_namespaces}; then
      for n in client server; do
        ${s} ip link set "bveth${m}${n}${i}" master bridge
      done
    fi
  done
  ${s} ip -all netns exec ip route add default via 10.0.0.254
fi

# Wait for interfaces to be ready.
if ! ${show_only}; then
  sleep 1
fi
