#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library for writing RADIUS clients
Summary(pl.UTF-8):	Biblioteka do tworzenia klientów usługi RADIUS
Name:		radcli
Version:	1.2.7
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/radcli/radcli/releases
Source0:	https://github.com/radcli/radcli/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	79c80174ceb31ce0698c760fd16f1216
URL:		http://radcli.github.io/radcli/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11.3
BuildRequires:	gnutls-devel >= 3.1.0
BuildRequires:	libtool >= 2:2
BuildRequires:	nettle-devel >= 2.4
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The radcli library is a library for writing RADIUS Clients. The
library's approach is to allow writing RADIUS-aware application in
less than 50 lines of C code. It was based originally on
freeradius-client and radiusclient-ng and is source compatible with
them.

%description -l pl.UTF-8
Biblioteka radcli to biblioteka do tworzenia klientów usługi RADIUS.
Ideą jest umożliwienie pisania aplikacji obsługujących RADIUS o
rozmiarze poniżej 50 linii kodu w języku C. Biblioteka jest oparta na
kodzie bibliotek freeradius-client oraz radiusclient-ng i jest z nimi
zgodna na poziomie źródeł.

%package devel
Summary:	Header files for radcli library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki radcli
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gnutls-devel >= 3.1.0
Requires:	nettle-devel >= 2.4

%description devel
Header files for radcli library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki radcli.

%package compat-devel
Summary:	Legacy header files for radcli library
Summary(pl.UTF-8):	Tradycyjne pliki nagłówkowe dla biblioteki radcli
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	freeradius-client-devel = %{version}
Provides:	radiusclient-ng-devel = %{version}
Obsoletes:	freeradius-client-devel < 1.2.0
Obsoletes:	radiusclient-ng-devel < 1.2.0

%description compat-devel
Legacy header files for radcli library (compatible with
freeradius-client and radiusclient-ng).

%description compat-devel -l pl.UTF-8
Tradycyjne pliki nagłówkowe dla biblioteki radcli (zgodne z
freeradius-client i radiusclient-ng).

%package static
Summary:	Static radcli library
Summary(pl.UTF-8):	Statyczna biblioteka radcli
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static radcli library.

%description static -l pl.UTF-8
Statyczna biblioteka radcli.

%prep
%setup -q

%build
touch config.rpath
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-legacy-compat \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libradcli.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT NEWS README.rst
%attr(755,root,root) %{_libdir}/libradcli.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libradcli.so.4
%dir %{_sysconfdir}/radcli
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radcli/radiusclient.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radcli/radiusclient-tls.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radcli/servers
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radcli/servers-tls
%{_datadir}/radcli

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libradcli.so
%{_includedir}/radcli
%{_pkgconfigdir}/radcli.pc
%{_mandir}/man3/radcli.h.3*
%{_mandir}/man3/rc_*.3*

%files compat-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeradius-client.so
%attr(755,root,root) %{_libdir}/libradiusclient-ng.so
%{_includedir}/freeradius-client.h
%{_includedir}/radiusclient-ng.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libradcli.a
%endif
