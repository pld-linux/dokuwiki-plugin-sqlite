%define		subver	2016-08-10
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		sqlite
%define		php_min_version 5.3.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki helper plugin to easily access a SQLite database
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/cosmocode/sqlite/archive/da9a21e/%{plugin}-%{version}.tar.gz
# Source0-md5:	919e54158e1fa924d74dd6b7e17424e7
URL:		http://www.dokuwiki.org/plugin:sqlite
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	unzip
Requires:	dokuwiki >= 20140505
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(pcre)
# you should pick one:
Suggests:	php(pdo-sqlite)
Suggests:	php(sqlite)
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
mv %{plugin}-*/{.??*,*} .

rm .travis.yml

%build
version=$(awk '/date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} -r $RPM_BUILD_ROOT%{plugindir}/_test
%{__rm} $RPM_BUILD_ROOT%{plugindir}/README

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
%{plugindir}/classes
