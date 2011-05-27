#
# Conditional build:
%bcond_without	authother	# without auth other support
%bcond_without	mysql		# without MySQL support
%bcond_without	ldap		# without LDAP support
%bcond_without	perl		# without perl support
%bcond_without	pam		# without pam support
%bcond_without	pgsql		# without PostgreSQL support
%bcond_without	ssl		# without ssl support
%bcond_without	whoson		# without WHOSON protocol support
%bcond_without	gdbm		# without gdbm auth db
%bcond_without	snide		# without snide server responses
%bcond_with	skipgetpwcheck	# with getpwuid returned struct check ommited (see patch for details)
#
Summary:	POP3 server
Summary(pl.UTF-8):	Serwer POP3
Name:		tpop3d
Version:	1.5.5
Release:	10
License:	GPL
Group:		Networking/Daemons/POP3
Source0:	http://download.savannah.nongnu.org/releases/tpop3d/%{name}-%{version}.tar.gz
# Source0-md5:	febe9ca46b575fcf99fd410caff98f47
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.conf
Source4:	%{name}.sysconfig
Patch1:		%{name}-pam-vdomain.patch
Patch2:		%{name}-sql-getpwuid-optional.patch
Patch3:		%{name}-lib.patch
Patch4:		%{name}-ssl-chain.patch
URL:		https://savannah.nongnu.org/projects/tpop3d
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_gdbm:BuildRequires:	gdbm-devel}
%{?with_libevent:BuildRequires:	libevent-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.4.6}
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_pam:BuildRequires:		pam-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_whoson:BuildRequires:	whoson-devel}
Requires(post,preun):	/sbin/chkconfig
Requires:	pam >= 0.79.0
Requires:	rc-scripts
%if %{with perl}
BuildRequires:	perl-devel
%endif
Provides:	pop3daemon
Obsoletes:	courier-imap-pop3
Obsoletes:	imap-pop
Obsoletes:	imap-pop3
Obsoletes:	pop3daemon
Obsoletes:	qpopper
Obsoletes:	qpopper6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
- auth_pgsql - uses PostgreSQL database
- auth_other - an external program
- auth_perl - embedded perl subroutines

The latter four options provide virtual domain support; the first two
are designed to authenticate local (Unix) users.

The following mailbox formats are supported:
- bsd - for BSD (`Unix') mailspools
- maildir - Qmail-style maildirs
- empty - null driver

tpop3d implements an optional metadata caching scheme for BSD
mailspools, which offers improved performance in cases where many
users leave large numbers of messages on the server between sessions.

%description -l pl.UTF-8
tpop3d to jeszcze-jeden-serwer-pop3. Intencją było napisanie serwera,
który jest szybki, rozszerzalny i bezpieczny. `Rozszerzalny' jest tu
użyte w kontekście formatów skrzynek. Obecnie pakiet dystrybucyjny
wspiera następujące mechanizmy autentykacji:

- auth_pam - używa Wymiennych Modułów Autentykacji (PAM)
- auth_passwd - /etc/passwd (i opcjonalnie /etc/shadow)
- auth_mysql - baza MySQL w stylu vmail-sql ; obejrzyj
  http://www.ex-parrot.com/~chris/vmail-sql/
- auth_pgsql - baza PostgreSQL
- auth_other - zewnętrzny program
- auth_perl - zakorzenione podprogramy Perla

Ostatnie cztery opcje pozwalają wspierać wirtualne domeny; pierwsze
dwie zaś są stworzone by autentykować lokalnych (uniksowych)
użytkowników.

Wspierane są następujące formaty skrzynek:
- bsd - dla kolejkowych skrzynek w stylu BSD (`Unix')
- maildir - format maildir znany z Qmail
- empty - pusty sterownik

tpop3d implementuje opcjonalne zapamiętywanie (caching) meta-danych
dla skrzynek BSD, które znacznie poprawia wydajność w przypadku, gdy
wielu użytkowników zostawia dużą liczbę wiadomości na serwerze
pomiędzy sesjami.

%prep
%setup -q
%patch1 -p1
%if %{with skipgetpwcheck}
%patch2 -p0
%endif
%patch3 -p1
%patch4 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-mbox-bsd-save-indices \
	--with-mailspool-directory=/var/mail \
	--enable-shadow-passwords \
%{!?with_pam:	--disable-auth-pam} \
%{?with_ldap:	--enable-auth-ldap} \
%{?with_mysql:	--enable-auth-mysql} \
%{?with_whoson:	--enable-whoson} \
%{?with_perl:	--enable-auth-perl} \
%{?with_pgsql:	--enable-auth-pgsql} \
%{?with_gdbm:	--enable-gdbm} \
%{?with_authother:	--enable-auth-other} \
	--enable-mbox-maildir \
%{?with_ssl:	--enable-tls} \
%{!?with_snide:	--disable-snide-comments} \
	--enable-auth-flatfile

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{pam.d,security,rc.d/init.d,sysconfig},%{_sysconfdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

touch $RPM_BUILD_ROOT/etc/security/blacklist.pop3

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "%{name} daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README* TPOP3D-AuthDriver scripts FAQ CHANGES CREDITS TODO PORTABILITY
%{?with_pam:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/%{name}}
%{?with_pam:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.pop3}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tpop3d.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
