Summary:	POP3 server
Summary(pl):	Serwer POP3
Name:		tpop3d
Version:	1.3.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.ex-parrot.com/~chris/tpop3d/%{name}-%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.init
Provides:	pop3daemon
Obsoletes:	pop3daemon
Obsoletes:	qpopper
Obsoletes:	qpopper6
Obsoletes:	imap-pop
Obsoletes:	solid-pop3d-ssl
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
POP3 server

%prep
%setup -q
%build
%configure2_13 \
	--with-mailspool-directory=/var/mail \
	--enable-auth-pam \
	--enable-auth-mysql \
	--enable-auth-perl \
	--enable-auth-other \
	--enable-mbox-maildir

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,security,rc.d/init.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT 

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/tpop3d
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/tpop3d

gzip -9nf README README.auth_mysql

touch $RPM_BUILD_ROOT%{_sysconfdir}/security/blacklist.pop3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz TPOP3D-AuthDriver scripts
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/tpop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.pop3
%attr(754,root,root) /etc/rc.d/init.d/tpop3d
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
