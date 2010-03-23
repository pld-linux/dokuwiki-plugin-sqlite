%include	/usr/lib/rpm/macros.php
%define		php_min_version 5.0.0
%define		plugin		sqlite
Summary:	DokuWiki helper plugin to easily access a SQLite database
Name:		dokuwiki-plugin-%{plugin}
Version:	20100203
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://download.github.com/cosmocode-sqlite-fb39468.zip
# Source0-md5:	cb14741dd492ae41022b5baa436c78e5
URL:		http://wiki.splitbrain.org/plugin:sqlite
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20091225
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-date
Requires:	php-pcre
Requires:	php-sqlite
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir	/usr/share/dokuwiki
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
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm -f $RPM_BUILD_ROOT%{plugindir}/{CREDITS,changelog}
rm -f $RPM_BUILD_ROOT%{plugindir}/{COPYING,README,VERSION}

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
%dir %{plugindir}
%{plugindir}/*.txt
%{plugindir}/*.php
%{plugindir}/db.sql
