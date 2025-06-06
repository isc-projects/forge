#!/bin/sh

# Ensure that the script is run as root.
(( EUID != 0 )) && exec sudo -- "${0}" "${@}"

configure() {
  local key=${1}
  local value=${2}

  if grep -E "^${key} =" "${init_all_py}" &> /dev/null; then
    sed -i'' "s%^${key} = .*$%${key} = ${value}%g" "${init_all_py}"
  elif grep -E "^[# ]*${key} =" "${init_all_py}" &> /dev/null; then
    sed -i'' "s%^[# ]*${key} = .*$%${key} = ${value}%g" "${init_all_py}"
  else
    printf '%s\n' "${key} = ${value}" >> "${init_all_py}"
  fi
}

get_address_from_interface() {
  ip a s dev "${1}" | grep -E "${2}" | tr -s ' ' | cut -d ' ' -f 3 | cut -d '/' -f 1
}

root_path=$(cd "$(dirname "${0}")" && pwd)
cd "${root_path}"

./initialize-virtual-interfaces.sh 3

client_interface='vethclient'
init_all_py='init_all.py'
server_interface='vethserver'
server2_interface='vethserver2'
server3_interface='vethserver3'
server_management_address='127.0.0.1'

client_address=$(get_address_from_interface "${client_interface}" 'inet\b.*\bscope global\b')
client_v6_address=$(get_address_from_interface "${client_interface}" 'inet6\b.*\bscope global\b')
cli_link_local=$(get_address_from_interface "${client_interface}" 'inet6\b.*\bscope link\b')
server_address=$(get_address_from_interface "${server_interface}" 'inet\b.*\bscope global\b')
server_v6_address=$(get_address_from_interface "${server_interface}" 'inet6\b.*\bscope global\b')
server_v6_address_link_local=$(get_address_from_interface "${server_interface}" 'inet6\b.*\bscope link\b')
server2_address=$(get_address_from_interface "${server2_interface}" 'inet\b.*\bscope global\b')
server3_address=$(get_address_from_interface "${server3_interface}" 'inet\b.*\bscope global\b')

# Virtual environment
if ! test -d ./venv; then
  python3 -m venv ./venv
  ./venv/bin/pip install --upgrade pip
  ./venv/bin/pip install -r requirements.txt
fi

# init_all.py
if ! test -f "${init_all_py}"; then
  cp "${init_all_py}_default" "${init_all_py}"
  sed -i'' 's/^\([a-zA-Z]\)/# \1/g' "${init_all_py}"
  configure 'CIADDR' "'${client_address}'"
  configure 'CLI_LINK_LOCAL' "'${cli_link_local}'"
  configure 'CLIENT_IPV6_ADDR_GLOBAL' "'${client_v6_address}'"
  configure 'DNS_IFACE' "'${client_interface}'"
  configure 'DNS4_ADDR' "'${server_address}'"
  configure 'DNS6_ADDR' "'${server_v6_address}'"
  configure 'GIADDR4' "'${client_address}'"
  configure 'IFACE' "'${client_interface}'"
  configure 'MGMT_ADDRESS' "'${server_management_address}'"
  configure 'MGMT_USERNAME' "'andrei'"
  configure 'MGMT_PASSWORD_CMD' "'pass show andrei@localhost'"
  configure 'MGMT_ADDRESS_2' "'${server_management_address}'"
  configure 'MGMT_ADDRESS_3' "'${server_management_address}'"
  configure 'MGMT_USERNAME_2' "'andrei'"
  configure 'MGMT_USERNAME_3' "'andrei'"
  configure 'SERVER_IFACE' "'${server_interface}'"
  configure 'SERVER2_IFACE' "'${server2_interface}'"
  configure 'SERVER3_IFACE' "'${server3_interface}'"
  configure 'SERVER_IFACE2' "'${server2_interface}'"
  configure 'SERVER_IFACE3' "'${server3_interface}'"
  configure 'SHOW_PACKETS_FROM' "'server'"
  if printf '%s' "${v-}" | grep -F 'isc_dhcp'; then
    configure 'SOFTWARE_INSTALL_PATH' "'/opt/dhcp'"
  else
    configure 'SOFTWARE_INSTALL_PATH' "'/opt/kea'"
  fi
  if printf '%s' "${v-}" | grep -F 'isc_dhcp'; then
    configure 'SOFTWARE_UNDER_TEST' "('bind9_server', '${v}'),"
  elif test "${v-}" = '4'; then
    configure 'SOFTWARE_UNDER_TEST' "('bind9_server', 'kea${v}_server'),"
  elif test "${v-}" = '6'; then
    configure 'SOFTWARE_UNDER_TEST' "('bind9_server', 'kea${v}_server'),"
  fi
  configure 'SRV_IPV6_ADDR_GLOBAL' "'${server_v6_address}'"
  configure 'SRV_IPV6_ADDR_LINK_LOCAL' "'${server_v6_address_link_local}'"
  configure 'SRV4_ADDR' "'${server_address}'"
  configure 'SRV4_ADDR_2' "'${server2_address}'"
  configure 'SRV4_ADDR_3' "'${server3_address}'"
  remove-comments "${init_all_py}"
  cat "${init_all_py}" | sort -uV > "${init_all_py}.tmp"
  mv "${init_all_py}.tmp" "${init_all_py}"
  sed -i '/^$/d' "${init_all_py}"
  cp "${init_all_py}" "src/${init_all_py}"
fi

# Validate configuration.
./venv/bin/python src/forge_cfg.py -T

./venv/bin/pytest --junitxml "forge-junit-${timestamp}.xml" "${@}"
