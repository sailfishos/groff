#specfile originally created for Fedora, modified for Moblin Linux
%{!?with_x:%define with_x 0}

Summary: A document formatting system
Name:	groff
Version: 1.18.1.4+git1
Release: 0
License: GPLv2 and GFDL
Group: Applications/Publishing
URL: http://groff.ffii.org
Source0: ftp://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz
Source3: mandocj.tar.gz
Source4: man-pages-ja-GNU_groff-20000115.tar.gz
Source6: hyphen.cs
Source7: nroff
Patch1: groff-1.16-safer.patch
Patch3: groff_1.18.1-15.diff
Patch4: groff-1.18-info.patch
Patch5: groff-1.18-nohtml.patch
Patch6: groff-1.18-pfbtops_cpp.patch
Patch7: groff-1.18-gzip.patch
Patch9: groff-1.18.1-fixminus.patch
Patch11: groff-1.18.1-8bit.patch
Patch12: groff-1.18.1-korean.patch
Patch13: groff-1.18.1-gzext.patch
#Patch14: groff-xlibs.patch
Patch15: groff-1.18.1-fix15.patch
Patch16: groff-1.18.1-devutf8.patch
#Patch17: groff-1.18.1.3-revision.patch
Patch18: groff-1.18.1.1-do_char.patch
#Patch19: groff-1.18.1.1-grn.patch
#Patch20: groff-1.18.1.1-tempfile.patch
#Patch21: groff-1.18.1.1-gcc41.patch
#Patch22: groff-1.18.1.1-bigendian.patch
Patch23: groff-1.18.1.1-spacefix.patch
Patch24: groff-1.18.1.4-sectmp.patch
Patch25: groff-1.18.1.4-grofferpath.patch
Patch26: groff-1.18.1.4-gcc4.3.0.patch
Patch27: stamp.patch
Patch28: groff-1.18.1.4-gcc6.patch
Patch29: groff-1.18.1.4-fix_build_with_glibc228.patch

Requires: /bin/mktemp
Requires: /sbin/install-info
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: bison zlib-devel texinfo

%description
Groff is a document formatting system. Groff takes standard text and
formatting commands as input and produces formatted output. The
created documents can be shown on a display or printed on a printer.
Groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

Groff can also be used to format man pages. If you are going to use
groff with the X Window System, you will also need to install the
groff-gxditview package.

%package perl
Summary: Parts of the groff formatting system that require Perl
Group: Applications/Publishing

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit font processor
for creating PostScript font files, the grog utility that can be used
to automatically determine groff command-line options, and the
troff-to-ps print filter.

%if %{with_x}
%package gxditview
Summary: An X previewer for groff text processor output
Group: Applications/Publishing
BuildRequires: imake xorg-x11-proto-devel libX11-devel libXaw-devel
BuildRequires: libXt-devel libXpm-devel libXext-devel

%description gxditview
Gxditview displays the groff text processor's output on an X Window
System display.
%endif

%prep
%setup -q -a 4
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1 -b .gzext
#%patch14 -p1
%patch15 -p1 -b .fix9
%patch16 -p1 -b .devutf8
#%patch17 -p1 -b .revision
%patch18 -p1 -b .do_char
#%patch19 -p1 -b .grn
#%patch20 -p1 -b .tempfile
#%patch21 -p1 -b .gcc41
#%patch22 -p1 -b .bigendian
%patch23 -p1 -b .spacefix
%patch24 -p1 -b .sectmp
%patch25 -p1 -b .grofferpath
%patch26 -p1 -b .gcc43
%patch27 -p1
%patch28 -p1
%patch29 -p1

for i in contrib/mm/{groff_mm,groff_mmse,mmroff}.man \
		src/devices/grolbp/grolbp.man; do
	iconv -f iso-8859-1 -t utf-8 < "$i" > "${i}_"
	mv "${i}_" "$i"
done

%build
#PATH=$PATH:%{_prefix}/X11R6/bin
#autoconf
%configure --enable-multibyte
make
(cd doc && makeinfo groff.texinfo)
%if %{with_x}
cd src/xditview
xmkmf && make %{?_smp_mflags}
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
#PATH=$PATH:%{_prefix}/X11R6/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix} ${RPM_BUILD_ROOT}%{_infodir}
make install manroot=${RPM_BUILD_ROOT}%{_mandir} \
			bindir=%{buildroot}%{_bindir} \
			mandir=%{buildroot}%{_mandir} \
			prefix=%{buildroot}/usr \
			exec_prefix=%{buildroot}/usr \
			sbindir=%{buildroot}%{_exec_prefix}/sbin \
			sysconfdir=%{buildroot}/etc \
			datadir=%{buildroot}/usr/share \
			infodir=%{buildroot}/%{_prefix}/info \
			sysconfdir=%{buildroot}/etc \
			includedir=%{buildroot}/usr/include \
			libdir=%{buildroot}/%{_libdir} \
			libexecdir=%{buildroot}/usr/libexec \
			localstatedir=%{buildroot}/var \
			sharedstatedir=%{buildroot}/usr/com \
			infodir=%{buildroot}/usr/share/info
			
#install -m 644 doc/groff.info* ${RPM_BUILD_ROOT}/%{_infodir}
%if %{with_x}
cd src/xditview
make install DESTDIR=${RPM_BUILD_ROOT}
cd ../..
%endif
#mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_prefix}/share
ln -s s.tmac ${RPM_BUILD_ROOT}%{_datadir}/groff/%version/tmac/gs.tmac
ln -s mse.tmac ${RPM_BUILD_ROOT}%{_datadir}/groff/%version/tmac/gmse.tmac
ln -s m.tmac ${RPM_BUILD_ROOT}%{_datadir}/groff/%version/tmac/gm.tmac
ln -s troff	${RPM_BUILD_ROOT}%{_bindir}/gtroff
ln -s tbl ${RPM_BUILD_ROOT}%{_bindir}/gtbl
ln -s pic ${RPM_BUILD_ROOT}%{_bindir}/gpic
ln -s eqn ${RPM_BUILD_ROOT}%{_bindir}/geqn
ln -s neqn ${RPM_BUILD_ROOT}%{_bindir}/gneqn
ln -s refer ${RPM_BUILD_ROOT}%{_bindir}/grefer
ln -s lookbib ${RPM_BUILD_ROOT}%{_bindir}/glookbib
ln -s indxbib ${RPM_BUILD_ROOT}%{_bindir}/gindxbib
ln -s soelim ${RPM_BUILD_ROOT}%{_bindir}/gsoelim
ln -s soelim ${RPM_BUILD_ROOT}%{_bindir}/zsoelim
ln -s nroff	${RPM_BUILD_ROOT}%{_bindir}/gnroff

# Build system is compressing man-pages
ln -s eqn.1.gz		${RPM_BUILD_ROOT}%{_mandir}/man1/geqn.1.gz
ln -s indxbib.1.gz	${RPM_BUILD_ROOT}%{_mandir}/man1/gindxbib.1.gz
ln -s lookbib.1.gz	${RPM_BUILD_ROOT}%{_mandir}/man1/glookbib.1.gz
ln -s nroff.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/gnroff.1.gz
ln -s pic.1.gz		${RPM_BUILD_ROOT}%{_mandir}/man1/gpic.1.gz
ln -s refer.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/grefer.1.gz
ln -s soelim.1.gz	${RPM_BUILD_ROOT}%{_mandir}/man1/gsoelim.1.gz
ln -s soelim.1.gz	${RPM_BUILD_ROOT}%{_mandir}/man1/zsoelim.1.gz
ln -s tbl.1.gz		${RPM_BUILD_ROOT}%{_mandir}/man1/gtbl.1.gz
ln -s troff.1.gz 	${RPM_BUILD_ROOT}%{_mandir}/man1/gtroff.1.gz

ln -s devnippon ${RPM_BUILD_ROOT}%{_datadir}/groff/%{version}/font/devkorean

cat debian/mandoc.local >> ${RPM_BUILD_ROOT}%{_datadir}/groff/site-tmac/mdoc.local
cat debian/mandoc.local >> ${RPM_BUILD_ROOT}%{_datadir}/groff/site-tmac/man.local

find ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_mandir} -type f -o -type l | \
	grep -v afmtodit | grep -v grog | grep -v mdoc.samples |\
	grep -v mmroff |\
	grep -v gxditview |\
	sed "s|${RPM_BUILD_ROOT}||g" | sed "s|\.[0-9]|\.*|g" > groff-files

install -pm 644 %SOURCE6 $RPM_BUILD_ROOT%{_datadir}/groff/%version/tmac/hyphen.cs

install -pm 755 %SOURCE7 $RPM_BUILD_ROOT%{_bindir}/nroff

ln -sf doc.tmac $RPM_BUILD_ROOT%{_datadir}/groff/%version/tmac/docj.tmac
# installed, but not packaged in rpm
mkdir -p $RPM_BUILD_ROOT%{_datadir}/groff/%{version}/groffer/
chmod 755 $RPM_BUILD_ROOT%{_datadir}/groff/1.18.1.4/font/devps/generate/symbol.sed
chmod 755 $RPM_BUILD_ROOT%{_datadir}/groff/1.18.1.4/font/devdvi/generate/CompileFonts
chmod 755 $RPM_BUILD_ROOT%{_datadir}/groff/1.18.1.4/font/devps/generate/afmname
chmod 755 $RPM_BUILD_ROOT%{_libdir}/groff/groffer/version.sh
mv $RPM_BUILD_ROOT%{_libdir}/groff/groffer/* $RPM_BUILD_ROOT/%{_datadir}/groff/%{version}/groffer/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/groff $RPM_BUILD_ROOT%{_infodir}/dir $RPM_BUILD_ROOT/%{_prefix}/lib/X11/app-defaults
rm -rf $RPM_BUILD_ROOT%{_libdir}/groff/groffer
rm -rf $RPM_BUILD_ROOT%{_libdir}/groff/site-tmac
rm -rf $RPM_BUILD_ROOT%{_libdir}/groff

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
[ -e %{_infodir}/groff.gz ] && /sbin/install-info %{_infodir}/groff.gz %{_infodir}/dir;
exit 0

%preun
if [ $1 = 0 ]; then
	[ -e %{_infodir}/groff.gz ] && /sbin/install-info --delete %{_infodir}/groff.gz %{_infodir}/dir
fi
exit 0

%files -f groff-files
%defattr(-,root,root,-)
%doc	BUG-REPORT NEWS PROBLEMS README TODO VERSION
%doc	doc/meintro.me doc/meref.me doc/pic.ms
%{_datadir}/groff
%doc %{_infodir}/groff*

%files perl
%defattr(-,root,root,-)
%{_bindir}/grog
%{_bindir}/mmroff
%{_bindir}/afmtodit
%doc %{_mandir}/man1/afmtodit.*
%doc %{_mandir}/man1/grog.*
%doc %{_mandir}/man1/mmroff*

%if %{with_x}
%files gxditview
%defattr(-,root,root,-)
%{_bindir}/gxditview
%{_datadir}/X11/app-defaults/GXditview
%endif

