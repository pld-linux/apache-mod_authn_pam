%define		mod_name	authn_pam
%define 	apxs		/usr/sbin/apxs
Summary:	This is the PAM authentication module for Apache 2.2
Summary(es):	Este m�dulo proporciona autenticaci�n PAM para Apache 2.2
Summary(pl):	Modu� uwierzytelnienia PAM dla Apache
Summary(pt_BR):	Este m�dulo prov� autentica��o PAM para o Apache
Name:		apache-mod_%{mod_name}
Version:	0.0.1
Release:	1
Epoch:		1
License:	Apache Group License
Group:		Networking/Daemons
Source0:	mod_%{mod_name}.tar.gz
# Source0-md5:	d7e2601f226c0319e3178f00406537b7
Source1:	apache-mod_authn_pam.conf
Source2:	httpd.pam
Patch0:		apache-mod_authn_pam-AuthnPAMService.patch
URL:		http://cvs.sourceforge.net/viewcvs.py/mod-auth/mod_authn_pam/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache >= 2.2
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	apache-mod_auth_pam

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using PAM (pluggable authentication module).

%description -l es
Este m�dulo permite autenticar clientes HTTP usando el directorio PAM.

%description -l pl
To jest modu� uwierzytelnienia dla Apache pozwalaj�cy na
uwierzytelnianie klient�w HTTP przez PAM.

%description -l pt_BR
Este m�dulo permite que voc� autentique clientes HTTP usando o
diret�rio PAM.

%prep
%setup -q -n mod_%{mod_name}
%patch0 -p1

%build
cd src
%{apxs} -c mod_%{mod_name}.c	-o mod_%{mod_name}.la	 -lpam

%install
cd src
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},/etc/pam.d,%{_sysconfdir}/httpd.conf}

install .libs/mod_*.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/52_mod_authn_pam.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_authn_pam.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%config(noreplace) /etc/pam.d/httpd
