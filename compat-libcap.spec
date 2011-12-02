Name: compat-libcap1
Version: 1.10
Release: 1
Summary: Library for getting and setting POSIX.1e capabilities
Source: ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/libcap-1.10.tar.bz2
Source1: http://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/capfaq-0.2.txt
License: BSD-like and LGPL
Patch: libcap-1.10-ia64.patch
Patch1: libcap-1.10-userland.patch
Patch2: libcap-1.10-shared.patch
Patch3: libcap-1.10-alpha.patch
Patch4: libcap-1.10-useCFLAGSwithCC.patch
Patch5: libcap-1.10-types.patch
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%prep
%setup -q -n libcap-1.10
# FIXME: Is this really required still?
%patch -p1 -b .ia64
%ifarch alpha
# FIXME: Is this really required still?
%patch3 -p1 -b .alpha
%endif
%patch1 -p1 -b .userland
%patch2 -p1 -b .shared
%patch4 -p1
%patch5 -p1

%build
make PREFIX=%{_prefix} LIBDIR=%{_libdir} 

%install
rm -rf ${RPM_BUILD_ROOT}
make install FAKEROOT=${RPM_BUILD_ROOT} \
             LIBDIR=${RPM_BUILD_ROOT}/%{_lib} \
             SBINDIR=${RPM_BUILD_ROOT}/%{_sbindir} \
             INCDIR=${RPM_BUILD_ROOT}/%{_includedir} \
             MANDIR=${RPM_BUILD_ROOT}/%{_mandir}/ \
             COPTFLAG="$RPM_OPT_FLAGS"
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man{2,3,8}
rm -f doc/cap_set_fd* doc/cap_set_file*
#mv -f doc/*.2 ${RPM_BUILD_ROOT}/%{_mandir}/man2/
#mv -f doc/*.3 ${RPM_BUILD_ROOT}/%{_mandir}/man3/
cp %{SOURCE1} doc/

chmod +x ${RPM_BUILD_ROOT}/%{_lib}/*.so.*
rm -rf ${RPM_BUILD_ROOT}/%{_sbindir}/
rm -rf ${RPM_BUILD_ROOT}/%{_includedir}/
rm -rf ${RPM_BUILD_ROOT}/%{_lib}/*.so
rm -rf ${RPM_BUILD_ROOT}/%{_mandir}/man2/*
rm -rf ${RPM_BUILD_ROOT}/%{_mandir}/man3/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/%{_lib}/*.so.*
%doc doc/capability.notes  doc/capfaq-0.2.txt

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
* Tue Aug 24 2010 Karsten Hopp <karsten@redhat.com> 1.10-1
- package as compat-libcap1

* Tue Aug 17 2010 Karsten Hopp <karsten@redhat.com> 1.10-26.kh
- include linux/types.h in capability.h

* Tue Nov 14 2006 Karsten Hopp <karsten@redhat.com> 1.10-26
- remove obsolete manpages (#215402)

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
