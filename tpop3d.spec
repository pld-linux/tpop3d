#
# Conditional build:
# _without_authother	- without auth other support
# _without_mysql	- without MySQL support
# _without_ldap		- without LDAP support
# _without_perl		- without perl support
# _without_pam		- without pam support
# _without_ssl		- without ssl support
# _without_whoson	- without WHOSON protocol support
#
Summary:	POP3 server
Summary(pl):	Serwer POP3
Name:		tpop3d
Version:	1.5.1
Release:	0.030718.1
License:	GPL
Group:		Networking/Daemons
#Source0:	http://www.ex-parrot.com/~chris/tpop3d/%{name}-%{version}.tar.gz
Source0:	tpop3d-1.5.1.030718.tar.bz2
# Source0-md5:	e9e5f9abef3626a2c6c26059db733695
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.conf
Patch0:		%{name}-ac_am_fixes.patch
URL:		http://www.ex-parrot.com/~chris/tpop3d/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_mysql:BuildRequires:	mysql-devel}
%{!?_without_ldap:BuildRequires:	openldap-devel}
%{!?_without_pam:BuildRequires:		pam-devel}
%{!?_without_perl:BuildRequires:	perl-devel}
%{!?_without_whoson:BuildRequires:	whoson-devel}
%{!?_without_ssl:BuildRequires:		openssl-devel}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	pop3daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	courier-imap-pop3
Obsoletes:	imap-pop
Obsoletes:	imap-pop3
Obsoletes:	pop3daemon
Obsoletes:	qpopper
Obsoletes:	qpopper6
Obsoletes:	solid-pop3d
Obsoletes:	solid-pop3d-ssl

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

%description -l pl
tpop3d to jeszcze-jeden-serwer-pop3. Intencj± by³o napisanie serwera,
który jest szybki, rozszerzalny i bezpieczny. `Rozszerzalny' jest tu
u¿yte w kontek¶cie formatów skrzynek. Obecnie pakiet dystrybucyjny
wspiera nastêpuj±ce mechanizmy autentykacji:

- auth_pam - u¿ywa Wymiennych Modu³ów Autentykacji (PAM)
- auth_passwd - /etc/passwd (i opcjonalnie /etc/shadow)
- auth_mysql - baza MySQL w stylu vmail-sql ; obejrzyj
  http://www.ex-parrot.com/~chris/vmail-sql/
- auth_other - zewnêtrzny program
- auth_perl - zakorzenione podprogramy Perla

Ostatnie trzy opcje pozwalaj± wspieraæ wirtualne domeny; pierwsze dwie
za¶ s± stworzone by autentykowaæ lokalnych (Unixowych) u¿ytkowników.

Wspierane s± nastêpuj±ce formaty skrzynek:
- bsd - dla kolejkowych skrzynek w stylu BSD (`Unix')
- maildir - format maildir znany z Qmail
- empty - pusty sterownik

tpop3d implementuje opcjonalne zapamiêtywanie (caching) meta-danych
dla skrzynek BSD, które znacznie poprawia wydajno¶æ w przypadku, gdy
wielu u¿ytkowników zostawia du¿± liczbê wiadomo¶ci na serwerze
pomiêdzy sesjami.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-mailspool-directory=/var/mail \
	--enable-shadow-passwords \
%{?_without_pam:	--disable-auth-pam} \
%{!?_without_ldap:	--enable-auth-ldap} \
%{!?_without_mysql:	--enable-auth-mysql} \
%{!?_without_whoson:	--enable-whoson} \
%{!?_without_perl:	--enable-auth-perl} \
%{!?_without_authother:	--enable-auth-other} \
	--enable-mbox-maildir \
%{!?_without_ssl:	--enable-tls} \
	--enable-auth-flatfile

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{pam.d,security,rc.d/init.d},%{_sysconfdir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/tpop3d
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/tpop3d
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}

touch $RPM_BUILD_ROOT/etc/security/blacklist.pop3

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README* TPOP3D-AuthDriver scripts FAQ CHANGES CREDITS TODO PORTABILITY
%{!?_without_pam:%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/tpop3d}
%{!?_without_pam:%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.pop3}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/tpop3d.conf
%attr(754,root,root) /etc/rc.d/init.d/tpop3d
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
