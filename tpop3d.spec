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
Patch0:		%{name}-ac_am_fixes.patch
URL:		http://www.ex-parrot.com/~chris/tpop3d/
Provides:	pop3daemon
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	pop3daemon
Obsoletes:	qpopper
Obsoletes:	qpopper6
Obsoletes:	imap-pop
Obsoletes:	solid-pop3d-ssl

%define		_sysconfdir	/etc

%description
tpop3d is yet-another-pop3-server. The intention has been to write a
server which is fast, extensible, and secure. `Extensible' is used
specifically in the context of new authentication mechanisms and
mailbox formats. Presently the distribution supports the following
authentication mechanisms:
- auth_pam - uses Pluggable Authentication Modules
- auth_passwd - /etc/passwd (and optionally /etc/shadow)
- auth_mysql - a vmail-sql style MySQL database; see
  http://www.ex-parrot.com/~chris/vmail-sql/
- auth_other - an external program
- auth_perl - embedded perl subroutines

The latter three options provide virtual domain support; the first two
are designed to authenticate local (Unix) users.

The following mailbox formats are supported:
- bsd - for BSD (`Unix') mailspools
- maildir - Qmail-style maildirs
- empty - null driver

tpop3d implements an optional metadata caching scheme for BSD
mailspools, which offers improved performance in cases where many
users leave large numbers of messages on the server between sessions.

%prep
%setup -q
%patch0 -p1

%build
aclocal
autoconf
automake -a -c
autoheader
%configure \
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
