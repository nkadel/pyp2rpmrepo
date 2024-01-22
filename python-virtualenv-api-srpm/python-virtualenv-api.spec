## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 27;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# Tests are disabled by default because they require network access.
# Try: fedpkg mockbuild --with tests --enable-network
#%%bcond tests 0
%global tests 0

Name:           python-virtualenv-api
Version:        2.1.18
Release:        %autorelease
Summary:        An API for virtualenv/pip

License:        BSD-2-Clause
URL:            https://github.com/sjkingo/virtualenv-api
# The GitHub tarball contains tests and LICENSE absent from the PyPI sdist.
Source:         %{url}/archive/%{version}/virtualenv-api-%{version}.tar.gz

# Fix --system-site-packages tests
# https://github.com/sjkingo/virtualenv-api/pull/52
Patch:          %{url}/pull/52.patch
# Remove search test cases
# https://github.com/sjkingo/virtualenv-api/pull/48
Patch:          %{url}/pull/48.patch
# Always use the current interpreter for test_python_version
# https://github.com/sjkingo/virtualenv-api/pull/56
Patch:          %{url}/pull/56.patch
# Taken together, the above three patches fix:
#   2.1.18: pytest is failing in four units
#   https://github.com/sjkingo/virtualenv-api/issues/55

BuildArch:      noarch

BuildRequires:  python3-devel

# Upstream does not name pip and virtualenv as dependencies, but they should
# be. See also:
#   Add virtualenv package to dependencies list
#   https://github.com/sjkingo/virtualenv-api/pull/49
BuildRequires:  /usr/bin/virtualenv
BuildRequires:  /usr/bin/pip

%global common_description %{expand:
virtualenv is a tool to create isolated Python environments. Unfortunately, it
does not expose a native Python API. This package aims to provide an API in the
form of a wrapper around virtualenv.

It can be used to create and delete environments and perform package management
inside the environment.}

%description %{common_description}


%package -n     python3-virtualenv-api
Summary:        An API for virtualenv/pip

Requires:       /usr/bin/virtualenv
Requires:       /usr/bin/pip

%description -n python3-virtualenv-api %{common_description}


%prep
%autosetup -n virtualenv-api-%{version} -p1
%py3_shebang_fix example.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files virtualenvapi


%check
%if %{with tests}
PYTHONPATH='%{buildroot}%{python3_sitelib}' \
    '%{python3}' -m unittest -v tests.py
%else
%pyproject_check_import
%endif


%files -n python3-virtualenv-api -f %{pyproject_files}
%doc CHANGES.md
%doc README.rst
%doc example.py


%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.18-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1.18-26
- Use new (rpm 4.17.1+) bcond style

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.1.18-25
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.18-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1.18-22
- Drop pytest BR; use unittest instead

* Mon Jan 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1.18-21
- Apply three upstream PR’s to fix failing tests

* Sun Jan 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1.18-9
- Drop EPEL7 compatibility
- Port to pyproject-rpm-macros

* Sun Jan 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1.18-8
- Switch to GitHub archive with LICENSE and tests
- Update License to SPDX
- Tidy up the spec file a bit; make tests a bcond conditional
- Unicode workaround for EPEL7
- Name the CLI tools in the virtualenv/pip dependencies added downstream
- Reduce macro indirection in the spec file
- Remove bogus BR on git-all
- Package additional documentation files
- Full EPEL7 compatibility with Python 2 and Python3 support
- Skip failing tests for now

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.1.18-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.18-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.1.18-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Charalampos Stratakis <cstratak@redhat.com> - 2.1.18-1
- Update to 2.1.18 (rhbz#1797387)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.1.16-12
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.16-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.16-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.16-7
- Subpackage python2-virtualenv-api has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.16-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 Michal Cyprian <mcyprian@redhat.com> - 2.1.16-1
- Update to 2.1.16

* Thu Feb 23 2017 Michal Cyprian <mcyprian@redhat.com> - 2.1.14-1
- Update to 2.1.14

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.9-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.9-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 06 2016 Michal Cyprian <mcyprian@redhat.com> - 2.1.8-4
- Update to 2.1.9

* Wed Apr 13 2016 Michal Cyprian <mcyprian@redhat.com> - 2.1.8-2
- Add requires, use test_suite enabling macro

* Wed Mar 30 2016 Michal Cyprian <mcyprian@redhat.com> - 2.1.8-1
- Initial package.

