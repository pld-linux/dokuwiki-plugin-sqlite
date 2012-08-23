# $Revision: 1.4 $, $Date: 2012/06/24 21:00:53 $
%define		plugin		sqlite
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki helper plugin to easily access a SQLite database
Name:		dokuwiki-plugin-%{plugin}
Version:	20120704
Release:	6
License:	GPL v2
Group:		Applications/WWW
#Source0:	https://github.com/cosmocode/sqlite/tarball/pdo/%{plugin}-pdo-%{version}.tgz
Source0:	https://github.com/Klap-in/sqlite/tarball/pdo/%{plugin}-pdo-%{version}.tgz
# Source0-md5:	8aae9339ea785655d7c4340b8eb8de37
URL:		http://www.dokuwiki.org/plugin:sqlite
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	unzip
Requires:	dokuwiki >= 20091225
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
Requires:	php-date
# you should pick one:
Suggests:	php-pdo-sqlite
Suggests:	php-sqlite
Conflicts:	dokuwiki-plugin-data < 20120624
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
DokuWiki helper plugin to easily access a SQLite database for other
DokuWiki plugins.

The plugin comes with a simple admin interface where you can run your
own SQL queries against any of the available databases.

%prep
%setup -qc
mv *-%{plugin}-*/* .
version=$(awk '/date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
#	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm $RPM_BUILD_ROOT%{plugindir}/README

# find locales
%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.txt
%{plugindir}/*.css
%{plugindir}/*.php
%{plugindir}/db.sql
