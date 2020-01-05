%define module	sympy
%define check_tests 0

Summary:	Python library for symbolic mathematics
Name:		python-%{module}
Version:	1.5.1
Release:	1
License:	BSD
Group:		Development/Python
Url:		http://sympy.googlecode.com/
Source0:	https://github.com/%{module}/%{module}/releases/download/%{module}-%{version}/%{module}-%{version}.tar.gz
Patch0:		doc-build.patch
BuildArch:	noarch
BuildRequires:  graphviz
# For docs
BuildRequires:  python-sphinx
BuildRequires:  python-matplotlib
BuildRequires:  librsvg
BuildRequires:  imagemagick
# for tests
BuildRequires:  x11-font-type1
BuildRequires:  x11-server-xvfb

%description
SymPy is a Python library for symbolic mathematics. It aims to become
a full-featured computer algebra system (CAS) while keeping the code
as simple as possible in order to be comprehensible and easily
extensible. SymPy is written entirely in Python and does not require
any external libraries, except optionally for plotting support.

%package texmacs
Summary:        TeXmacs integration for sympy
Group:		Development/Python
Requires:       %{name} = %{version}-%{release}, TeXmacs

%description texmacs
This package contains a TeXmacs plugin for sympy.

%package examples
Summary:        Sympy examples
Group:		Development/Python
Requires:       %{name} = %{version}-%{release}

%description examples
This package contains example input for sympy.

%package doc
Summary:        Documentation for sympy
Group:		Development/Python

%description doc
man  and HTML documentation for sympy.

%package -n python-%{module}
Summary:        Python 3 library for symbolic mathematics
Group:		Development/Python
BuildRequires:	python-devel
BuildRequires:	python-mpmath
Requires: 	python-numpy
Requires:	python-mpmath
Requires:	python-matplotlib
%{?python_provide:%python_provide python-%{module}}

%description -n python-%{module}
SymPy is a Python 3 library for symbolic mathematics. It aims to become
a full-featured computer algebra system (CAS) while keeping the code
as simple as possible in order to be comprehensible and easily
extensible. SymPy is written entirely in Python 3 and does not require
any external libraries, except optionally for plotting support.

%prep
%setup -q -n sympy-%{name}-%{version}
%autopatch -p1

%build
%py3_build

# docs
PYTHONPATH=$(pwd) make -C doc html
# leftovers
rm -rf doc/_build/html/.buildinfo

%install
%py_install

# Remove extra files
rm -f %{buildroot}%{_bindir}/{,doc}test

# Install the TeXmacs integration
cp -p data/TeXmacs/bin/tm_sympy %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/TeXmacs/plugins/sympy
cp -a data/TeXmacs/progs %{buildroot}%{_datadir}/TeXmacs/plugins/sympy

# Don't let an executable script go into the documentation
chmod a-x examples/all.py

# Install the HTML documentation
mkdir -p %{buildroot}%{_docdir}/%{name}-doc
cp -a doc/_build/html %{buildroot}%{_docdir}/%{name}-doc
rm -fr %{buildroot}%{_docdir}/%{name}-doc/i18n

%if 0%check_tests
%check
# The python3 tests fail with Unicode errors without this
export LC_ALL=en_US.UTF-8
let "dnum = $RANDOM % 90 + 10"
xvfb-run -n $dnum python3 setup.py test
%endif

%files texmacs
%doc data/TeXmacs/LICENSE
%{_bindir}/tm_sympy
%{_datadir}/TeXmacs/plugins/sympy/

%files examples
%doc examples

%files doc
%docdir %{_docdir}/%{name}-doc/html
%{_docdir}/%{name}-doc/html
%{_mandir}/man1/isympy.1*

%files -n python3-%{module}
%doc AUTHORS LICENSE PKG-INFO 
%{python_sitelib}/sympy/
%{python_sitelib}/isympy.*
%{python_sitelib}/__pycache__/*.pyc
%{python_sitelib}/sympy-%{version}-*.egg-info
%{_bindir}/isympy
