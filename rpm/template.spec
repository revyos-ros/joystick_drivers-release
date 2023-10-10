%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-wiimote
Version:        3.2.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS wiimote package

License:        GPL
URL:            http://www.ros.org/wiki/wiimote
Source0:        %{name}-%{version}.tar.gz

Requires:       bluez-libs
Requires:       ros-iron-geometry-msgs
Requires:       ros-iron-rclcpp
Requires:       ros-iron-rclcpp-components
Requires:       ros-iron-rclcpp-lifecycle
Requires:       ros-iron-sensor-msgs
Requires:       ros-iron-std-msgs
Requires:       ros-iron-std-srvs
Requires:       ros-iron-wiimote-msgs
Requires:       ros-iron-ros-workspace
BuildRequires:  bluez-libs-devel
BuildRequires:  ros-iron-ament-cmake
BuildRequires:  ros-iron-ament-cmake-auto
BuildRequires:  ros-iron-geometry-msgs
BuildRequires:  ros-iron-rclcpp
BuildRequires:  ros-iron-rclcpp-components
BuildRequires:  ros-iron-rclcpp-lifecycle
BuildRequires:  ros-iron-sensor-msgs
BuildRequires:  ros-iron-std-msgs
BuildRequires:  ros-iron-std-srvs
BuildRequires:  ros-iron-wiimote-msgs
BuildRequires:  ros-iron-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-iron-ament-cmake-gtest
BuildRequires:  ros-iron-ament-lint-auto
BuildRequires:  ros-iron-ament-lint-common
%endif

%description
The wiimote package allows ROS nodes to communicate with a Nintendo Wiimote and
its related peripherals, including the Nunchuk, Motion Plus, and
(experimentally) the Classic. The package implements a ROS node that uses
Bluetooth to communicate with the Wiimote device, obtaining accelerometer and
gyro data, the state of LEDs, the IR camera, rumble (vibrator), buttons,
joystick, and battery state. The node additionally enables ROS nodes to control
the Wiimote's LEDs and vibration for feedback to the human Wiimote operator.
LEDs and vibration may be switched on and off, or made to operate according to a
timed pattern.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Tue Oct 10 2023 Jonathan Bohren <jbo@jhu.edu> - 3.2.0-1
- Autogenerated by Bloom

* Thu Apr 20 2023 Jonathan Bohren <jbo@jhu.edu> - 3.1.0-4
- Autogenerated by Bloom

* Tue Mar 21 2023 Jonathan Bohren <jbo@jhu.edu> - 3.1.0-3
- Autogenerated by Bloom

