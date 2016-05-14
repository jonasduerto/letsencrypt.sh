Summary:	letsencrypt/acme client implemented as a shell-script
Name:		letsencrypt.sh
Version:	0.1.0
Release:	0.2
License:	MIT
Group:		Applications/Networking
Source0:	https://github.com/lukas2511/letsencrypt.sh/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	eadd134cc5365753c03929dd70db341d
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		https://github.com/lukas2511/letsencrypt.sh
BuildRequires:	rpmbuild(macros) >= 1.713
Requires:	curl
Requires:	grep
Requires:	mktemp
Requires:	openssl
Requires:	sed
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
This is a client for signing certificates with an ACME-server
(currently only provided by letsencrypt) implemented as a relatively
simple bash-script.

Current features:
- Signing of a list of domains
- Signing of a CSR
- Renewal if a certificate is about to expire or SAN (subdomains)
  changed
- Certificate revocation

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/acme-challenges}

install -p letsencrypt.sh $RPM_BUILD_ROOT%{_sbindir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG LICENSE
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
# challenges written here from letsencrypt.sh, need to be readable by webserver
%dir %attr(751,root,root) %{_sysconfdir}/acme-challenges

%attr(755,root,root) %{_sbindir}/letsencrypt.sh