%define debug_package %{nil}
%define gcc_version 4.5.4
%define pkg_suffix 454
%define moz_release 0moz1
%define mpc_version 0.8.1
%define mpfr_version 2.4.2
%define gmp_version 5.0.1
%define gcc_prefix /tools/gcc-%{gcc_version}-%{moz_release}

Name: gcc%{pkg_suffix}_%{moz_release}
Summary: An interpreted, interactive, object-oriented programming language.
Version: %{gcc_version}
Release: %{moz_release}
License: GPL
Group: Development/Languages
Source: http://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Source1: http://www.mpfr.org/mpfr-%{mpfr_version}/mpfr-%{mpfr_version}.tar.bz2
Source2: http://ftp.gnu.org/gnu/gmp/gmp-%{gmp_version}.tar.bz2
Source3: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
# https://bugzilla.mozilla.org/attachment.cgi?id=457606
Patch0: plugin_finish_decl.diff
Patch1: pr49911.diff
Patch2: r159628-r163231-r171807.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Autoprov: 0
Autoreq: 0

BuildRequires: m4
%ifarch x86_64
BuildRequires: glibc-devel(x86-32)
%endif

# manually specify 'Requires' so we don't require package-internal libs.
%ifarch x86_64
Requires: /bin/sh
Requires: ld-linux-x86-64.so.2()(64bit)
Requires: ld-linux-x86-64.so.2(GLIBC_2.3)(64bit)
Requires: ld-linux.so.2
Requires: ld-linux.so.2(GLIBC_2.3)
Requires: libc.so.6
Requires: libc.so.6()(64bit)
Requires: libc.so.6(GLIBC_2.0)
Requires: libc.so.6(GLIBC_2.1)
Requires: libc.so.6(GLIBC_2.1.3)
Requires: libc.so.6(GLIBC_2.11)(64bit)
Requires: libc.so.6(GLIBC_2.2)
Requires: libc.so.6(GLIBC_2.2.5)(64bit)
Requires: libc.so.6(GLIBC_2.3)
Requires: libc.so.6(GLIBC_2.3)(64bit)
Requires: libc.so.6(GLIBC_2.3.2)
Requires: libc.so.6(GLIBC_2.3.2)(64bit)
Requires: libc.so.6(GLIBC_2.6)
Requires: libc.so.6(GLIBC_2.6)(64bit)
Requires: libc.so.6(GLIBC_2.7)
Requires: libc.so.6(GLIBC_2.7)(64bit)
Requires: libdl.so.2
Requires: libdl.so.2()(64bit)
Requires: libdl.so.2(GLIBC_2.0)
Requires: libdl.so.2(GLIBC_2.1)
Requires: libdl.so.2(GLIBC_2.2.5)(64bit)
Requires: libm.so.6
Requires: libm.so.6()(64bit)
Requires: libm.so.6(GLIBC_2.0)
Requires: libm.so.6(GLIBC_2.2.5)(64bit)
Requires: libpthread.so.0
Requires: libpthread.so.0()(64bit)
Requires: libpthread.so.0(GLIBC_2.0)
Requires: libpthread.so.0(GLIBC_2.1)
Requires: libpthread.so.0(GLIBC_2.2.5)(64bit)
Requires: libpthread.so.0(GLIBC_2.3.4)
Requires: libpthread.so.0(GLIBC_2.3.4)(64bit)
Requires: librt.so.1
Requires: librt.so.1()(64bit)
Requires: librt.so.1(GLIBC_2.2)
Requires: librt.so.1(GLIBC_2.2.5)(64bit)
Requires: rpmlib(CompressedFileNames) <= 3.0.4-1
Requires: rpmlib(PartialHardlinkSets) <= 4.0.4-1
Requires: rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires: rtld(GNU_HASH)
%else
Requires: /bin/sh
Requires: ld-linux.so.2
Requires: ld-linux.so.2(GLIBC_2.3)
Requires: libc.so.6
Requires: libc.so.6(GLIBC_2.0)
Requires: libc.so.6(GLIBC_2.1)
Requires: libc.so.6(GLIBC_2.1.3)
Requires: libc.so.6(GLIBC_2.11)
Requires: libc.so.6(GLIBC_2.2)
Requires: libc.so.6(GLIBC_2.2.3)
Requires: libc.so.6(GLIBC_2.3)
Requires: libc.so.6(GLIBC_2.3.2)
Requires: libc.so.6(GLIBC_2.6)
Requires: libc.so.6(GLIBC_2.7)
Requires: libdl.so.2
Requires: libdl.so.2(GLIBC_2.0)
Requires: libdl.so.2(GLIBC_2.1)
Requires: libm.so.6
Requires: libm.so.6(GLIBC_2.0)
Requires: libpthread.so.0
Requires: libpthread.so.0(GLIBC_2.0)
Requires: libpthread.so.0(GLIBC_2.1)
Requires: libpthread.so.0(GLIBC_2.3.4)
Requires: librt.so.1
Requires: librt.so.1(GLIBC_2.2)
Requires: rpmlib(CompressedFileNames) <= 3.0.4-1
Requires: rpmlib(PartialHardlinkSets) <= 4.0.4-1
Requires: rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires: rtld(GNU_HASH)
%endif

%description
Mozilla specific GCC 4.5 version. Includes GMP, MPC and MPFR libraries.
Compiled with CXXFLAGS set to "-fPIC"

%prep
%setup -q -b 1 -b 2 -b 3 -n gcc-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
cd ../gmp-%{gmp_version}
./configure --prefix=%{gcc_prefix}
make
make install

#fix la
sed -i "s,libdir='/tools/gcc-%{version}/lib',libdir='%{gcc_prefix}/lib',g" \
  %{gcc_prefix}/lib/libgmp.la

cd ../mpfr-%{mpfr_version}
./configure --prefix=%{gcc_prefix} --with-gmp=%{gcc_prefix}
make
make install

cd ../mpc-%{mpc_version}
./configure --prefix=%{gcc_prefix} --with-gmp=%{gcc_prefix} --with-mpfr=%{gcc_prefix}
make
make install

cd ../gcc-%{version}
export LDFLAGS="-L%{gcc_prefix}/lib -Wl,-rpath,%{gcc_prefix}/lib"
export BOOT_LDFLAGS="$LDFLAGS"
export CXXFLAGS="-fPIC"
./configure --prefix=%{gcc_prefix} \
    --disable-gnu-unique-object \
    --enable-__cxa_atexit \
    --enable-languages=c,c++ \
    --with-gmp=%{gcc_prefix} \
    --with-mpfr=%{gcc_prefix} \
    --with-mpc=%{gcc_prefix}
make BOOT_LDFLAGS="$BOOT_LDFLAGS" LDFLAGS="$LDFLAGS" bootstrap
make install

%install
# fake install, make files section happy
mkdir -p $RPM_BUILD_ROOT/%{gcc_prefix}
cp -a %{gcc_prefix}/* $RPM_BUILD_ROOT/%{gcc_prefix}/

%clean
echo rm -fr $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{gcc_prefix}

%changelog
* Thu Apr 04 2013 Rail Aliiev <rail@mozilla.com>
 - New upstream version

* Wed Jan 30 2013 John Hopkins <jhopkins@mozilla.com>
- Build gcc with --disable-gnu-unique-object
- Manually specify Requires, remove all Provides.

* Tue Jun 01 2010 Rail Aliev <rail@mozilla.com>
- Initial spec
