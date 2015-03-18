#
# spec file for package python-tomate
#
# Copyright (c) 2014 Elio Esteves Duarte <elio.esteves.duarte@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define real_name tomate
%define module_name %{real_name}_notify_plugin

Name: %{real_name}-notify-plugin
Version: 0.3.0
Release: 0
License: GPL-3.0+
Summary: Tomate notify plugin
Source: %{name}-upstream.tar.gz
Url: https://github.com/eliostvs/tomate-notify-plugin

BuildRoot: %{_tmppath}/%{name}-%{version}-build

BuildRequires: python-devel
BuildRequires: python-setuptools

Requires: tomate-gtk >= 0.3.0

%if 0%{?suse_version}
BuildArchitectures: noarch
Requires: typelib-1_0-Notify-0_7
%endif

%if 0%{?fedora}
BuildArch: noarch
Requires: notify-python
%endif

%description
Tomate plugin that shows screen notifications.

%prep
%setup -q -n %{name}-upstream

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_datadir}/%{real_name}/
%{_datadir}/%{real_name}/plugins/
%{python_sitelib}/%{module_name}-%{version}-*.egg-info/

%doc AUTHORS COPYING README.md

%changelog