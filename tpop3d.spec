Summary:	POP3 server
Summary(pl):	Serwer POP3
Name:		tpop3d
Version:	1.3.5
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.ex-parrot.com/~chris/tpop3d/%{name}-%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.init
Patch0:		%{name}-ac_am_fixes.patch
URL:		http://www.ex-parrot.com/~chris/tpop3d/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
Prereq:		rc-scripts
Provides:	pop3daemon
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
aclocal
autoconf
automake -a -c
autoheader
%configure \
	--with-mailspool-directory=/var/mail \
	--enable-shadow-passwords \
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
%doc *.gz TPOP3D-AuthDriver scripts
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/tpop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.pop3
%attr(754,root,root) /etc/rc.d/init.d/tpop3d
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
