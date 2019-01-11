%define module	sympy

Summary:	Python library for symbolic mathematics

Name:		python-%{module}
Version:	1.3
Release:	1
Source0:	https://github.com/sympy/sympy/releases/download/sympy-1.3/sympy-%{version}.tar.gz
License:	BSD
Group:		Development/Python
Url:		http://sympy.googlecode.com/
Requires: 	python-numpy
BuildArch:	noarch
BuildRequires:	python-sphinx
BuildRequires:	python-docutils
BuildRequires:  python3-devel
BuildRequires:  librsvg
BuildRequires:  imagemagick
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	python2-setuptools

%description
SymPy is a Python library for symbolic mathematics. It aims to become
a full-featured computer algebra system (CAS) while keeping the code
as simple as possible in order to be comprehensible and easily
extensible. SymPy is written entirely in Python and does not require
any external libraries, except optionally for plotting support.

%package -n python2-sympy
Requires:	python2-numpy

%prep
%setup -q -n %{module}-%{version}

cp -a . %py2dir

%install

pushd %py2dir
python2 setup.py install --root=%{buildroot}
mv %{buildroot}%{_bindir}/isympy %{buildroot}%{_bindir}/python2-isympy
mv %{buildroot}%{_mandir}/man1/isympy.1 \
   %{buildroot}%{_mandir}/man1/python2-isympy.1
popd

%__%py_install
#make -C doc html
rm -f %{buildroot}%{_bindir}/test %{buildroot}%{_bindir}/doctest %{buildroot}%{_bindir}/py.bench

%clean

%files 
%doc AUTHORS LICENSE examples/
%{_bindir}/isympy
%{_mandir}/man1/isympy.*
%dir %{py_puresitedir}/%{module}
%{py_puresitedir}/%{module}/*
%{py_puresitedir}/%{module}-*.egg-info


%files -n python2-sympy
%doc AUTHORS LICENSE
%{_bindir}/python2-isympy
%{_mandir}/man1/python2-isympy.*
%dir %{py2_puresitedir}/%{module}
%{py2_puresitedir}/%{module}/*
%{py2_puresitedir}/%{module}-*.egg-info
