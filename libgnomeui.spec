Summary:	GNOME base GUI library
Summary(pl):	Podstawowa biblioteka GUI GNOME
Name:		libgnomeui
Version:	2.8.0
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.8/%{name}-%{version}.tar.bz2
# Source0-md5:	ef0df128e3c0b2047ce440bbbe481390
Patch0:		%{name}-threads.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.7.92
BuildRequires:	audiofile-devel >= 1:0.2.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel >= 1:0.2.31
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-keyring-devel >= 0.4.0
BuildRequires:	gnome-vfs2-devel >= 2.8.0
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	gtk+2-devel >= 2:2.4.4
BuildRequires:	libbonoboui-devel >= 2.6.1
BuildRequires:	libglade2-devel >= 1:2.4.0
BuildRequires:	libgnome-devel >= 2.8.0
BuildRequires:	libgnomecanvas-devel >= 2.8.0
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	pango-devel >= 1:1.4.1
BuildRequires:	perl-base
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpm-build >= 4.1-10
Requires:	gtk+2 >= 2:2.4.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
GUI applications and desktop tools to be used in conjunction with a
window manager for the X Window System. The libgnomeui package
includes GUI-related libraries that are needed to run GNOME. (The
libgnome package includes the library features that don't use the X
Window System.)

%description -l pl
GNOME (GNU Network Object Model Environment) jest przyjaznym dla
użytkownika zestawem aplikacji i narzędzi z graficznym interfejsem do
używania w połączeniu z zarządcą okien X Window System. Pakiet
libgnomeui zawiera biblioteki związane z graficznym interfejsem
użytkownika potrzebne do uruchomienia GNOME (pakiet libgnome zawiera
biblioteki nie używające X Window System).

%package devel
Summary:	Headers for libgnomeui
Summary(pl):	Pliki nagłówkowe libgnomeui
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	GConf2-devel >= 2.7.92
Requires:	esound-devel >= 1:0.2.31
Requires:	gnome-vfs2-devel >= 2.8.0
Requires:	gnome-keyring-devel >= 0.4.0
Requires:	gtk-doc-common
Requires:	gtk+2-devel >= 2:2.4.4
Requires:	libbonoboui-devel >= 2.6.1
Requires:	libglade2-devel >= 1:2.4.0
Requires:	libgnome-devel >= 2.8.0
Requires:	libgnomecanvas-devel >= 2.8.0
Requires:	libjpeg-devel

%description devel
GNOME (GNU Network Object Model Environment) is a user-friendly set of
GUI applications and desktop tools to be used in conjunction with a
window manager for the X Window System. The libgnomeui-devel package
includes the libraries and include files that you will need to use
libgnomeui.

%description devel -l pl
Ten pakiet zawiera pliki nagłówkowe potrzebne do kompilacji programów
używających libgnomeui.

%package static
Summary:	Static libgnomeui libraries
Summary(pl):	Statyczne biblioteki libgnomeui
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libgnomeui libraries.

%description static -l pl
Statyczna wersja bibliotek libgnomeui.

%prep
%setup -q
%patch -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/help

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

# no static modules and *.la for libglade or vfs modules
rm -f $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/2.*/filesystems/libgnome-vfs.{la,a}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/gnome_segv2
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/libglade/2.0/*.so
%attr(755,root,root) %{_libdir}/gtk-2.0/2.*/filesystems/libgnome-vfs.so
%{_pixmapsdir}/*
# it seems that every package that uses %{_datadir}/gnome tree requires
# libgnomeui - so added these directories to this package
%dir %{_datadir}/gnome
%dir %{_datadir}/gnome/help

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_pkgconfigdir}/*.pc
%{_includedir}/libgnomeui-2.0
%{_gtkdocdir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
