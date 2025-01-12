Summary:	Network traffic analyzer
Name:		nta
Version:	1.0
Release:	12
License:	GPLv2+
Group:		Monitoring
Url:		https://www.kyberdigi.cz/projects/nta
Source0:	%{name}-%{version}.tar.bz2
Source1:	nta-cron-sample
Patch0:		nta-mandriva_apache_integration.bz2
Patch1:		nta-config_location.bz2
Requires:	webserver
BuildArch:	noarch

%description
Sometimes it is good to know, how the network is used, how many
bytes were received and how many bytes were sent. Therefore, here
is Network Traffic Analyzer, that creates nice graphical network
usage statistics accessible using a webbrowser.

NTA runs as a cron job as any unprivileged (non root) user.

%files
%doc README COPYING README.urpmi
%config(noreplace) %{webappconfdir}/nta.conf
%config(noreplace) %{_sysconfdir}/nta/config.pl
%{_sysconfdir}/cron.d/nta
%{_sbindir}/*
%{perl_vendorlib}/*
%attr(0755,apache,apache) %dir /var/www/nta
/var/www/nta/*
%attr(0755,apache,apache) %dir /var/run/nta
%attr(0755,apache,apache) %dir %{_localstatedir}/lib/nta/data
%{_localstatedir}/lib/nta/templates/*

#----------------------------------------------------------------------------

%prep
%setup
%patch0 -p0
%patch1 -p0

%build

%install
# nta has no make install or similar, so we do it manually

install -d %{buildroot}%{_sbindir}
install nta.pl %{buildroot}%{_sbindir}

install -d %{buildroot}%{_sysconfdir}/nta
install -m0644 config.pl %{buildroot}%{_sysconfdir}/nta

install -d %{buildroot}%{_sysconfdir}/cron.d
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.d/nta

install -d -m 755 %{buildroot}%{webappconfdir}
cat > %{buildroot}%{webappconfdir}/%{name}.conf <<EOF
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

