#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.3
%define		qtver		6.8.0
%define		kframever	6.13.0
%define		kaname		koko
Summary:	An image viewer
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	eb5cf326d0fdbebb9b4dc1bc73ed01f8
Source1:	http://download.geonames.org/export/dump/cities1000.zip
# Source1-md5:	17673c7d80586ac57a82f0f3adea4e31
Source2:	http://download.geonames.org/export/dump/admin1CodesASCII.txt
# Source2-md5:	5767124c80d81c3b9040ad592fcb56c5
Source3:	http://download.geonames.org/export/dump/admin2Codes.txt
# Source3-md5:	73307f36b6f26f50f2f09374d3940c3f
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	exiv2-devel >= 0.21
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdeclarative-devel >= %{kframever}
BuildRequires:	kf6-kfilemetadata-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kirigami-addons-devel
BuildRequires:	kf6-kirigami-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-purpose-devel >= %{kframever}
BuildRequires:	kquickimageeditor-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Koko is an image viewer designed for desktop and touch devices.

%prep
%setup -q -n %{kaname}-%{version}
cp -a %{SOURCE1} src/
cp -a %{SOURCE2} src/
cp -a %{SOURCE3} src/

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{sr,zh_CN}

# not supported by glibc yet
%{__rm} -rf $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/koko
%{_desktopdir}/org.kde.koko.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.koko.svg
%{_datadir}/knotifications6/koko.notifyrc
%dir %{_datadir}/koko
%{_datadir}/koko/admin1Codes.txt
%{_datadir}/koko/admin2Codes.txt
%{_datadir}/koko/cities1000.txt
%{_datadir}/koko/countries.csv
%{_datadir}/metainfo/org.kde.koko.appdata.xml
