#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.3
%define		qtver		6.8.0
%define		kframever	6.13.0
%define		kaname		koko
Summary:	An image viewer
Name:		ka6-%{kaname}
Version:	25.04.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	7731795d44b64a9a86bbcc8870df28e9
Source1:	http://download.geonames.org/export/dump/cities1000.zip
# Source1-md5:	6187b6d345528d78e072a75b50c06e89
Source2:	http://download.geonames.org/export/dump/admin1CodesASCII.txt
# Source2-md5:	ea209c170a34ded1105649a014a086df
Source3:	http://download.geonames.org/export/dump/admin2Codes.txt
# Source3-md5:	6a9a5dce5bcf0d2c04e7591719b0fa3c
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
