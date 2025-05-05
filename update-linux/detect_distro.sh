#!/bin/bash

# Set everything to "false" and "unknown"
DISTRO_ID="unknown"
DISTRO_NAME="unknown"
DISTRO_VERSION="unknown"
HAS_APT="false"
HAS_DNF="false"
HAS_ZYPPER_LEAP="false"
HAS_ZYPPER_TUMBLEWEED="false"
HAS_PACMAN="false"
HAS_YAY="false"
HAS_SNAP="false"
HAS_FLATPAK="false"

# Try to read /etc/os-release
if [ -f /etc/os-release ]; then
    # Load the variables from /etc/os-release
    . /etc/os-release
    # Set the detected values
    DISTRO_ID=${ID:-"unknown"}
    DISTRO_NAME=${NAME:-"unknown"}
    DISTRO_VERSION=${VERSION_ID:-"unknown"}
# Fallback if /etc/os-release does not exist
elif [ -f /etc/lsb-release ]; then
     . /etc/lsb-release
     DISTRO_ID=${DISTRIB_ID:-"unknown"}
     DISTRO_NAME=${DISTRIB_DESCRIPTION:-"unknown"}
     DISTRO_VERSION=${DISTRIB_RELEASE:-"unknown"}
fi

# Check which package managers are available by checking if the commands are available

# APT (Debian, Ubuntu, Mint, ...)
if command -v apt > /dev/null 2>&1; then
    HAS_APT="true"
fi

# DNF (Fedora, RHEL, CentOS, ...)
if command -v dnf > /dev/null 2>&1; then
    HAS_DNF="true"
fi

# Zypper (openSUSE)
if command -v zypper > /dev/null 2>&1; then
    # Differ Leap and Tumbleweed based on DISTRO_ID
    if [[ "$DISTRO_ID" == "opensuse-leap" ]]; then
        HAS_ZYPPER_LEAP="true"
    elif [[ "$DISTRO_ID" == "opensuse-tumbleweed" ]]; then
        HAS_ZYPPER_TUMBLEWEED="true"
    else
        HAS_ZYPPER_LEAP="true"
    fi
fi

# Pacman (Arch, Manjaro, ...)
if command -v pacman > /dev/null 2>&1; then
    HAS_PACMAN="true"
fi

# Yay (AUR Helper)
if command -v yay > /dev/null 2>&1; then
    HAS_YAY="true"
fi

# Snap (Snapcraft)
if command -v snap > /dev/null 2>&1; then
    HAS_SNAP="true"
fi

# Flatpak
if command -v flatpak > /dev/null 2>&1; then
    HAS_FLATPAK="true"
fi

# Output the results
echo "DISTRO_ID=${DISTRO_ID}"
echo "DISTRO_NAME=${DISTRO_NAME}"
echo "DISTRO_VERSION=${DISTRO_VERSION}"
echo "HAS_APT=${HAS_APT}"
echo "HAS_DNF=${HAS_DNF}"
echo "HAS_ZYPPER_LEAP=${HAS_ZYPPER_LEAP}"
echo "HAS_ZYPPER_TUMBLEWEED=${HAS_ZYPPER_TUMBLEWEED}"
echo "HAS_PACMAN=${HAS_PACMAN}"
echo "HAS_YAY=${HAS_YAY}"
echo "HAS_SNAP=${HAS_SNAP}"
echo "HAS_FLATPAK=${HAS_FLATPAK}"

exit 0