%define version {{VER}}
%define release {{SPI}}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Middleware that sends keystone stats so statsd
Name: keystone-probe
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{version}.tar.gz
License: Apache Software License 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Packager: Jasper Capel <jasper.capel@spilgames.com>
Url: https://github.com/spilgames/keystone-probe
Requires: python
BuildRequires: python python-setuptools

%description
Middleware that sends keystone stats to statsd

%prep
%setup -n %{name}-%{version}

%build
# add version file
echo %{version} > VERSION

python setup.py build

%install
python setup.py install --root=%{buildroot} 

%clean
rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/*

%files
%defattr(-,root,root)
/usr/lib/python2.6/site-packages/spil_keystone_auth_plugin/
/usr/lib/python2.6/site-packages/spil_keystone_auth_plugin-%{version}-py2.6.egg-info
