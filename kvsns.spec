#
# Conditional build:
%bcond_without	ceph		# RADOS support
#
Summary:	Library to access to a namespace inside a KVS
Summary(pl.UTF-8):	Biblioteka dostępu do przestrzeni nazw wewnątrz KVS
Name:		kvsns
Version:	1.2.9
Release:	1
License:	LGPL v3+
Group:		Libraries
#Source0Download: https://github.com/phdeniel/kvsns/tags
Source0:	https://github.com/phdeniel/kvsns/archive/V%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	dce3a8c06a08420d86da007d990f7e8d
Patch0:		%{name}-overflow.patch
Patch1:		%{name}-format.patch
Patch2:		%{name}-cmake.patch
Patch3:		%{name}-types.patch
URL:		https://github.com/phdeniel/kvsns
%{?with_ceph:BuildRequires:	ceph-devel}
BuildRequires:	cmake >= 2.6.4
BuildRequires:	hiredis-devel
BuildRequires:	libini_config-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libkvsns library allows of a POSIX namespace built on top of a
Key-Value Store.

%description -l pl.UTF-8
Biblioteka libkvsns pozwala zbudować przestrzeń nazw POSIX ponad
systemem KVS (Key-Value Store).

%package ceph
Summary:	RADOS object store for KVSNS library
Summary(pl.UTF-8):	Biblioteka przechowywania danych RADOS dla biblioteki KVSNS
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ceph
RADOS object store for KVSNS library.

%description ceph -l pl.UTF-8
Biblioteka przechowywania danych RADOS dla biblioteki KVSNS.

%package devel
Summary:	Header files for KVSNS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki KVSNS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	hiredis-devel
Requires:	libini_config-devel

%description devel
Header files for KVSNS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki KVSNS.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
# meson support is incomplete (no required include directories, no install), so use cmake
install -d build
cd build
# possible snprint or strncpy truncations
CFLAGS="%{rpmcflags} -Wno-error=format-truncation -Wno-error=stringop-truncation -D_FILE_OFFSET_BITS=64"
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	ceph -p /sbin/ldconfig
%postun	ceph -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/kvsns_*.txt
%attr(755,root,root) %{_libdir}/libextstore_crud_cache.so
%attr(755,root,root) %{_libdir}/libextstore_posix.so
%attr(755,root,root) %{_libdir}/libkvsal_redis.so
%attr(755,root,root) %{_libdir}/libkvsns.so
%attr(755,root,root) %{_libdir}/libobjstore_cmd.so

%if %{with ceph}
%files ceph
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libextstore_rados.so
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/kvsns
%{_pkgconfigdir}/libkvsns.pc
