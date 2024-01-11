Name: libcap
Version: 2.48
Release: 9%{?dist}
Summary: Library for getting and setting POSIX.1e capabilities
URL: https://sites.google.com/site/fullycapable/
License: BSD or GPLv2

Source: https://git.kernel.org/pub/scm/libs/libcap/libcap.git/snapshot/%{name}-%{version}.tar.gz
Patch0: libcap-use-compiler-flag-options.patch
Patch1: libcap-static-analysis-fix.patch
Patch2: libcap-static-analysis-fix-2.patch
Patch3: libcap-static-analysis-fix-3.patch
Patch4: libcap-disable-golang.patch
Patch5: libcap-fix-ambient-caps.patch
Patch6: libcap-cve-2023-2603.patch
Patch7: libcap-cve-2023-2602.patch

BuildRequires: libattr-devel pam-devel perl-interpreter gcc
BuildRequires: make

%description
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package static
Summary: Static libraries for libcap development
Requires: %{name} = %{version}-%{release}

%description static
The libcap-static package contains static libraries needed to develop programs
that use libcap and need to be statically linked. 

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package devel
Summary: Development files for libcap
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, etc) for libcap.

libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install libcap-devel if you want to develop or compile applications using
libcap.

%prep
%autosetup -p1

%build
# libcap can not be build with _smp_mflags:
make prefix=%{_prefix} lib=%{_lib} LIBDIR=%{_libdir} SBINDIR=%{_sbindir} \
     INCDIR=%{_includedir} MANDIR=%{_mandir} PKGCONFIGDIR=%{_libdir}/pkgconfig/

%install
make install RAISE_SETFCAP=no \
             DESTDIR=%{buildroot} \
             LIBDIR=%{_libdir} \
             SBINDIR=%{_sbindir} \
             PKGCONFIGDIR=%{_libdir}/pkgconfig/

mkdir -p %{buildroot}/%{_mandir}/man{2,3,8}
mv -f doc/*.3 %{buildroot}/%{_mandir}/man3/

chmod +x %{buildroot}/%{_libdir}/*.so.*

%ldconfig_scriptlets

%files
%license License
%doc doc/capability.notes
%{_libdir}/*.so.*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_libdir}/security/pam_cap.so

%files static
%{_libdir}/libcap.a
%{_libdir}/libpsx.a

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*
%{_libdir}/pkgconfig/libcap.pc
%{_libdir}/pkgconfig/libpsx.pc


%changelog
* Wed Jul 12 2023 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 2.48-9
- Fix integer overflow in _libcap_strdup() (CVE-2023-2603)
  Resolves: rhbz#2210638
- Correctly check pthread_create() return value to avoid memory leak (CVE-2023-2602)
  Resolves: rhbz#2222198

* Fri Jan 28 2022 Zoltan Fridrich <zfridric@redhat.com> - 2.48-8
- Fix ambient capabilities for non-root users
  Related: rhbz#2037215

* Fri Aug 27 2021 Zoltan Fridrich <zfridric@redhat.com> - 2.48-7
- Fix issues detected by static analyzers
  Related: rhbz#1985346

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2.48-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Jun 18 2021 Zoltan Fridrich <zfridric@redhat.com> - 2.48-5
- Remove deprecated tests
  Resolves: rhbz#1938758

* Tue Jun 15 2021 Zoltan Fridrich <zfridric@redhat.com> - 2.48-4
- Fix issues detected by static analyzers (rhbz#1938758)

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.48-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Sun Feb 14 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2.48-2
- Rebase distro flags patch

* Wed Feb 10 2021 Giuseppe Scrivano <gscrivan@redhat.com> - 2.48-1
- Update to 0.2.48

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 17 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2.46-1
- Update to 0.2.46

* Wed Oct 21 2020 Karsten Hopp <karsten@fedoraproject.org> - 2.44-1
- update to 2.44
- remove additional getpcaps manpage as it now included in the sources

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Karsten Hopp <karsten@redhat.com> - 2.26-5
- enable gating

* Mon Feb 04 2019 Karsten Hopp <karsten@redhat.com> - 2.26-4
- bump release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Karsten Hopp <karsten@redhat.com> - 2.26-2
- add CI tests using the standard test interface (astepano)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Karsten Hopp <karsten@redhat.com> - 2.25-11
- rebuild

* Wed Feb 21 2018 Karsten Hopp <karsten@redhat.com> - 2.25-10
- buildrequire gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.25-8
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Karsten Hopp <karsten@redhat.com> - 2.25-4
- add -static subpackage (rhbz#1380251)

* Sun Nov 27 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.25-3
- Add perl BR to fix FTBFS

* Mon Apr 25 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.25-2
- Fix pkgconfig install location on aarch64
- Spec file cleanups

* Mon Apr 11 2016 Karsten Hopp <karsten@redhat.com> - 2.25-1
- libcap-2.25

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 2.24-6
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Karsten Hopp <karsten@redhat.com> 2.24-4
- fix libdir in libcap.pc

* Wed Apr 23 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.24-3
- set pkg-config dir to proper value to get it built on AArch64

* Wed Apr 16 2014 Karsten Hopp <karsten@redhat.com> 2.24-2
- fix URL and license

* Wed Apr 16 2014 Karsten Hopp <karsten@redhat.com> 2.24-1
- update to 2.24
- dropped patch for rhbz#911878, it is upstream now

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Karsten Hopp <karsten@redhat.com> 2.22-6
- mv libraries to /usr/lib*
- add getpcaps man page 
- spec file cleanup
- fix URL of tarball

* Tue May 14 2013 Karsten Hopp <karsten@redhat.com> 2.22-5
- add patch from Mark Wielaard to fix use of uninitialized memory in _fcaps_load
  rhbz #911878

* Sun Feb 24 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.22-5
- Build with $RPM_OPT_FLAGS and $RPM_LD_FLAGS.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Karsten Hopp <karsten@redhat.com> 2.22-1
- update to 2.22 (#689752)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 10 2009 Karsten Hopp <karsten@redhat.com> 2.17-1
- update to 2.17

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Karsten Hopp <karsten@redhat.com> 2.16-4
- fix build problems with p.e. cdrkit

* Sun Mar 22 2009 Karsten Hopp <karsten@redhat.com> 2.16-1
- update, with a fix for rebuild problems

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 06 2008 Karsten Hopp <karsten@redhat.com> 2.10-2
- drop libcap.so.1
- fix buildrequires and path to pam security module

* Thu Jun 05 2008 Karsten Hopp <karsten@redhat.com> 2.10-1
- libcap-2.10

* Thu Feb 21 2008 Karsten Hopp <karsten@redhat.com> 2.06-4
- don't build static binaries (#433808)

* Wed Feb 20 2008 Karsten Hopp <karsten@redhat.com> 2.06-3
- temporarily add libcap-1 libraries to bootstrap some packages

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.06-2
- Autorebuild for GCC 4.3

* Fri Feb 15 2008 Karsten Hopp <karsten@redhat.com> 2.06-1
- upate to 2.06 (#432983)

* Wed Jan 16 2008 Karsten Hopp <karsten@redhat.com> 1.10-33
- drop post,postun requirements on ldconfig as find-requires can handle this

* Tue Jan 15 2008 Karsten Hopp <karsten@redhat.com> 1.10-32
- add disttag
- fix changelog
- fix defattr

* Mon Jan 14 2008 Karsten Hopp <karsten@redhat.com> 1.10-31
- use cp -p in spec file to preserve file attributes (#225992)
- add license file

* Fri Aug 24 2007 Karsten Hopp <karsten@redhat.com> 1.10-30
- rebuild

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 1.10-29
- add CAP_AUDIT_WRITE and CAP_AUDIT_CONTROL (#229833)

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.10-28
- drop obsolete ia64 patch
- rpmlint fixes

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.10-27
- misc. review fixes
- add debian patch to make it build with a recent glibc
- remove static lib

* Wed Jul 19 2006 Karsten Hopp <karsten@redhat.de> 1.10-25
- add patch to support COPTFLAG (#199365)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.10-24.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.10-24.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.10-24.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Karsten Hopp <karsten@redhat.de> 1.10-24
- added development manpages
- as there are no manpages for the executables available, added at least
  a FAQ (#172324)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 31 2005 Steve Grubb <sgrubb@redhat.com> 1.10-23
- rebuild to pick up audit capabilities

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.10-22
- build with gcc-4

* Wed Feb 09 2005 Karsten Hopp <karsten@redhat.de> 1.10-21
- rebuilt

* Tue Aug 31 2004 Phil Knirsch <pknirsch@redhat.com> 1.10-20
- Fix wrong typedef in userland patch (#98801)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Karsten Hopp <karsten@redhat.de> 1.10-17
- use _manpath

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 1.10-14
- set execute bits on library so that requires are generated.

* Thu Nov 21 2002 Mike A. Harris <mharris@redhat.com> 1.10-13
- Removed %%name macro sillyness from package Summary, description text, etc.
- Removed archaic Prefix: tag
- lib64 fixes everywhere to use _lib, _libdir, etc
- Removed deletion of RPM_BUILD_DIR from %%clean section
- Added -q flag to setup macro
- Severely cleaned up spec file, and removed usage of perl

* Fri Jul 19 2002 Jakub Jelinek <jakub@redhat.com> 1.10-12
- CFLAGS was using COPTFLAG variable, not COPTFLAGS
- build with -fpic
- apply the IA-64 patch everywhere, use capget/capset from glibc,
  not directly as _syscall (as it is broken on IA-32 with -fpic)
- reenable alpha

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.10-10
- Exclude alpha for now, apparent gcc bug.

* Fri Nov  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.10-6
- Fix sys/capabilities.h header (#55727)
- Move to /lib, some applications seem to be using this rather early
  (#55733)

* Mon Jul 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add post,postun scripts

* Tue Jul 10 2001 Jakub Jelinek <jakub@redhat.com>
- don't build libcap.so.1 with ld -shared, but gcc -shared

* Wed Jun 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Rebuild - it was missing for alpha

* Wed Jun 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390/s390x support

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.10-1
- initial RPM
- fix build on ia64
