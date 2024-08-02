%define check_tests 0

Summary:	Python library for symbolic mathematics
Name:		python-sympy
Version:	1.13.1
Release:	1
License:	BSD
Group:		Development/Python
Url:		https://github.com/sympy
#Source0:	https://github.com/sympy/sympy/releases/download/sympy-%{version}/sympy-%{version}.tar.gz
Source0:	https://pypi.io/packages/source/s/sympy/sympy-%{version}.tar.gz
#Patch0:i	doc-build.patch
BuildArch:	noarch
BuildRequires:  graphviz
BuildRequires:  python3dist(mpmath)
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

%files
%doc AUTHORS LICENSE
%{python_sitelib}/sympy/
%{python_sitelib}/isympy.*
%{python_sitelib}/__pycache__/
%{python_sitelib}/sympy-*.*info
%{_bindir}/isympy

#---------------------------------------------------------------------------

%package texmacs
Summary:        TeXmacs integration for sympy
Group:		Development/Python
Requires:       %{name} = %{version}-%{release}, 
Recommends: TeXmacs

%description texmacs
This package contains a TeXmacs plugin for sympy.

%files texmacs
%doc data/TeXmacs/LICENSE
%{_bindir}/tm_sympy
%{_datadir}/TeXmacs/plugins/sympy/

#---------------------------------------------------------------------------

%package examples
Summary:        Sympy examples
Group:		Development/Python
Requires:       %{name} = %{version}-%{release}

%description examples
This package contains example input for sympy.

%files examples
%doc examples

#---------------------------------------------------------------------------

%package doc
Summary:        Documentation for sympy
Group:		Development/Python

%description doc
man  and HTML documentation for sympy.

%files doc
#docdir %{_docdir}/%{name}-doc/html
#{_docdir}/%{name}-doc/html
%{_mandir}/man1/isympy.1*

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n sympy-%{version}

%build
%py_build

%install
%py_install

# Install the TeXmacs integration
cp -p data/TeXmacs/bin/tm_sympy %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/TeXmacs/plugins/sympy
cp -a data/TeXmacs/progs %{buildroot}%{_datadir}/TeXmacs/plugins/sympy

# Don't let an executable script go into the documentation
chmod a-x examples/all.py

%if 0%check_tests
%check
# The python3 tests fail with Unicode errors without this
export LC_ALL=en_US.UTF-8
let "dnum = $RANDOM % 90 + 10"
xvfb-run -n $dnum python3 setup.py test
%endif

