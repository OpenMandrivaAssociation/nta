Summary:	Network traffic analyzer
Name:		nta
Version:	1.0
Release:	12
License:	GPL
Group:		Monitoring
URL:		http://www.kyberdigi.cz/projects/nta
Source0:	%{name}-%{version}.tar.bz2
Source1:	nta-cron-sample
Patch0:		nta-mandriva_apache_integration.bz2
Patch1:		nta-config_location.bz2
Requires:	webserver
BuildArch:  noarch

%description
Sometimes it is good to know, how the network is used, how many
bytes were received and how many bytes were sent. Therefore, here
is Network Traffic Analyzer, that creates nice graphical network 
usage statistics accessible using a webbrowser.

NTA runs as a cron job as any unprivileged (non root) user.

%prep
%setup
%patch0 -p0
%patch1 -p0

%build

%install
# nta has no make install or similar, so we do it manually
install -d  %{buildroot}%{_sbindir}
install nta.pl %{buildroot}%{_sbindir}

install -d %{buildroot}%{_sysconfdir}/nta
install -m0644 config.pl %{buildroot}%{_sysconfdir}/nta

install -d %{buildroot}%{_sysconfdir}/cron.d
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.d/nta

install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# configuration for NTA

Alias /nta /var/www/nta
<Directory /var/www/nta>
    Require all granted
</Directory>
EOF

install -d %{buildroot}%{perl_vendorlib}
install -m0644 *.pm %{buildroot}%{perl_vendorlib}

install -d %{buildroot}/var/www/nta
install -d %{buildroot}/var/www/nta/images
install -m0644 images/* %{buildroot}/var/www/nta
install -d %{buildroot}/var/run/nta

install -d %{buildroot}%{_localstatedir}/lib/nta/data
install -d %{buildroot}%{_localstatedir}/lib/nta/templates
install -m0644 templates/* %{buildroot}%{_localstatedir}/lib/nta/templates

cat > README.urpmi <<EOF
NTA is installed as a cronjob that runs every five minutes.

You can check the results by accessing http://localhost/nta with any 
browser.
EOF

%files
%doc README COPYING README.urpmi
%config(noreplace) %{_webappconfdir}/nta.conf
%config(noreplace) %{_sysconfdir}/nta/config.pl

%{_sysconfdir}/cron.d/nta

%{_sbindir}/*
%{perl_vendorlib}/*

%attr(0755,apache,apache) %dir /var/www/nta
/var/www/nta/*
%attr(0755,apache,apache) %dir /var/run/nta

%attr(0755,apache,apache) %dir %{_localstatedir}/lib/nta/data
%{_localstatedir}/lib/nta/templates/*


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-7mdv2011.0
+ Revision: 613109
- the mass rebuild of 2010.1 packages

* Wed Feb 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0-6mdv2010.1
+ Revision: 507259
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.0-5mdv2010.0
+ Revision: 430187
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.0-4mdv2009.0
+ Revision: 254106
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 1.0-2mdv2008.1
+ Revision: 133089
- fix installing
- kill re-definition of %%buildroot on Pixel's request

  + Emmanuel Andry <eandry@mandriva.org>
    - Import nta



* Sun May 21 2006 Emmanuel Andry <eandry@mandriva.org> 1.0-2mdk
  Package from Udo Rader <udo.rader@bestsolution.at> 
    - bugfix for wrong lockfile location

* Sat May 20 2006 Udo Rader <udo.rader@bestsolution.at> 1.0-1mdk
- initial release on Mandriva
