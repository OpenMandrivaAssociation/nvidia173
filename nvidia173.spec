
# I love OpenSource :-(

%define name		nvidia173
%define version		173.14.17
%define rel		3

%define priority	9620

# pkg0: plain archive
# pkg1: + precompiled modules
# pkg2: + 32bit compatibility libraries
%define pkgname32	NVIDIA-Linux-x86-%{version}-pkg0
%define pkgname64	NVIDIA-Linux-x86_64-%{version}-pkg2

# For now, backportability is kept for 2006.0 / CS4 forwards.

%define nameprefix		x11-driver-video-
%define drivername		nvidia173
%define driverpkgname		%{nameprefix}%{drivername}
%define modulename		%{drivername}
%define cards			GeForce FX based cards
%define xorg_libdir		%{_libdir}/xorg
%define xorg_extra_modules	%{_libdir}/xorg/extra-modules
%define nvidia_driversdir	%{xorg_libdir}/modules/drivers/%{drivername}
%define nvidia_extensionsdir	%{_libdir}/%{drivername}/xorg
%define nvidia_libdir		%{_libdir}/%{drivername}
%define nvidia_libdir32		%{_prefix}/lib/%{drivername}
%define nvidia_bindir		%{nvidia_libdir}/bin
%define nvidia_deskdir		%{_datadir}/%{drivername}
%define nvidia_xvmcconfdir	%{_sysconfdir}/%{drivername}
%define ld_so_conf_dir		%{_sysconfdir}/%{drivername}
%define ld_so_conf_file		ld.so.conf

%if %{mdkversion} <= 200900
%define nvidia_extensionsdir	%{xorg_libdir}/modules/extensions/%{drivername}
%endif

%if %{mdkversion} <= 200810
%define drivername		nvidia-current
%define cards			GeForce FX and later cards
%endif

%if %{mdkversion} <= 200710
%define nameprefix		%{nil}
%define drivername		nvidia97xx
%endif

%if %{mdkversion} <= 200700
%define drivername		nvidia
%define ld_so_conf_dir		%{_sysconfdir}/ld.so.conf.d/GL
%define ld_so_conf_file		%{drivername}.conf
%endif

%if %{mdkversion} <= 200600
%define xorg_libdir		%{_prefix}/X11R6/%{_lib}
%define ld_so_conf_dir		%{_sysconfdir}/ld.so.conf.d
%define nvidia_driversdir	%{xorg_libdir}/modules/drivers
%define nvidia_extensionsdir	%{xorg_libdir}/modules/extensions/nvidia
%define nvidia_bindir		%{_bindir}
%define nvidia_xvmcconfdir	%{_sysconfdir}/X11
%define nvidia_deskdir		%{_datadir}/applications
%endif

%define biarches x86_64
%ifarch %{ix86}
%define nsource %{SOURCE0}
%define pkgname %{pkgname32}
%endif
%ifarch x86_64
%define nsource %{SOURCE1}
%define pkgname %{pkgname64}
%endif

# Other packages should not require any NVIDIA libraries, and this package
# should not be pulled in when libGL.so.1 is required
%define _provides_exceptions \\.so
%define common_requires_exceptions libGLcore\\.so\\|libnvidia-tls\\.so

%ifarch %{biarches}
# (anssi) Allow installing of 64-bit package if the runtime dependencies
# of 32-bit libraries are not satisfied. If a 32-bit package that requires
# libGL.so.1 is installed, the 32-bit mesa libs are pulled in and that will
# pull the dependencies of 32-bit nvidia libraries in as well.
%define _requires_exceptions %common_requires_exceptions\\|lib.*so\\.[^(]\\+\\(([^)]\\+)\\)\\?$
%else
%define _requires_exceptions %common_requires_exceptions
%endif

Summary:	NVIDIA proprietary X.org driver and libraries, 173.14.xx series
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
Source0:	ftp://download.nvidia.com/XFree86/Linux-x86/%{version}/%{pkgname32}.run
Source1:	ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/%{pkgname64}.run
License:	Proprietary
BuildRoot:	%{_tmppath}/%{name}-buildroot
URL:		http://www.nvidia.com/object/unix.html
Group: 		System/Kernel and hardware
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	ImageMagick
%if "%{driverpkgname}" == "nvidia"
# old nvidia package had different versioning
Epoch:		1
%endif

%description
Source package of the 173.14.xx series NVIDIA proprietary driver.
Binary packages are named x11-driver-video-nvidia173 on 2009,
x11-driver-video-nvidia-current on 2008, nvidia97xx on 2007.1, and
nvidia on 2007.0 and earlier.

%package -n %{driverpkgname}
Summary:	NVIDIA proprietary X.org driver and libraries for %cards
Group: 		System/Kernel and hardware
%if %{mdkversion} >= 200700
# Older alternatives implementations were buggy in various ways:
Requires(post): update-alternatives >= 1.9.0
Requires(postun): update-alternatives >= 1.9.0
%endif
%if %{mdkversion} >= 200910
Conflicts:	x11-server-common < 1.6.0-3
%endif
%if %{mdkversion} >= 200800
# Proprietary driver handling rework:
Conflicts:	harddrake < 10.4.163
Conflicts:	drakx-kbd-mouse-x11 < 0.21
Conflicts:	x11-server-common < 1.3.0.0-17
# Suggests supported as of 2008.0, pull the rest of docs:
Suggests:	%{drivername}-doc-html
%endif
%if %{mdkversion} >= 200810
# for missing libwfb.so
Conflicts:	x11-server-common < 1.4
# Proper support for versioned kmod() was added in 2008.1:
Requires:	kmod(%{modulename}) = %{version}
%endif

%description -n %{driverpkgname}
NVIDIA proprietary X.org graphics driver, related libraries and
configuration tools for %cards,
including the associated Quadro cards.

NOTE: You should use XFdrake to configure your NVIDIA card. The
correct packages will be automatically installed and configured.

If you do not want to use XFdrake, see README.manual-setup.

This NVIDIA driver should be used with %cards,
including the associated Quadro cards.
For older cards, the packages %{nameprefix}nvidia96xx and
%{nameprefix}nvidia71xx should be used instead.

%package -n dkms-%{drivername}
Summary:	NVIDIA kernel module for %cards
Group:		System/Kernel and hardware
Requires:	dkms
Requires(post):	dkms
Requires(preun): dkms
Requires:	%{driverpkgname} = %{version}

%description -n dkms-%{drivername}
NVIDIA kernel module for %cards. This
is to be used with the %{driverpkgname} package.

%package -n %{drivername}-devel
Summary:	NVIDIA XvMC development library and OpenGL headers
Group:		Development/C
Requires:	%{driverpkgname} = %{version}-%{release}

%description -n %{drivername}-devel
NVIDIA XvMC static development library and OpenGL headers for
%cards. This package is not required for
normal use.

# HTML doc splitted off because of size, for Mandriva One:
%package -n %{drivername}-doc-html
Summary:	NVIDIA html documentation (%{drivername})
Group:		System/Kernel and hardware
Requires:	%{driverpkgname} = %{version}-%{release}

%description -n %{drivername}-doc-html
HTML version of the README.txt file provided in package
%{driverpkgname}.

%prep
%setup -c -T
sh %{nsource} --extract-only
rm -rf %{pkgname}/usr/src/nv/precompiled

# Now works properly on xen, as reported by guillomovitch, so remove the xen
# check:
perl -pi -e 's/^module:(.*) xen-sanity-check (.*)$/module:$1 $2/' \
    %{pkgname}/usr/src/nv/Makefile.kbuild

cat > README.install.urpmi <<EOF
This driver is for %cards.

Use XFdrake to configure X to use the correct NVIDIA driver. Any needed
packages will be automatically installed if not already present.
1. Run XFdrake as root.
2. Go to the Graphics Card list.
3. Select your card (it is usually already autoselected).
4. Answer any questions asked and then quit.

If you do not want to use XFdrake, see README.manual-setup.
EOF

cat > README.manual-setup <<EOF
This file describes the procedure for the manual installation of this NVIDIA
driver package. You can find the instructions for the recommended automatic
installation in the file 'README.install.urpmi' in this directory.

- Open %{_sysconfdir}/X11/xorg.conf and make the following changes:
  o Change the Driver to "nvidia" in the Device section
  o Make the line below the only 'glx' related line in the Module section:
%if %{mdkversion} >= 200710
      Load "glx"
%if %{mdkversion} >= 200800
  o Remove any 'ModulePath' lines from the Files section
%else
  o Make the lines below the only 'ModulePath' lines in the Files section:
      ModulePath "%{nvidia_extensionsdir}"
      ModulePath "%{xorg_libdir}/modules"
%endif
%else
      Load "%{nvidia_extensionsdir}/libglx.so"
%endif
%if %{mdkversion} >= 200700
- Run "update-alternatives --set gl_conf %{ld_so_conf_dir}/%{ld_so_conf_file}" as root.
- Run "ldconfig" as root.
%endif
EOF

mv %{pkgname}/usr/share/doc/html html-doc

%install
rm -rf %{buildroot}
cd %{pkgname}/usr

# dkms
install -d -m755 %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}
install -m644 src/nv/* %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}
chmod 0755 %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/conftest.sh

install -d -m755 %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/patches
#install -m644 %{SOURCE3} %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/patches
# -p1 for dkms:
#sed -i 's,usr/src/nv,nv,g' %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/patches/*.diff.txt

cat > %{buildroot}%{_usrsrc}/%{drivername}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME="%{drivername}"
PACKAGE_VERSION="%{version}-%{release}"
BUILT_MODULE_NAME[0]="nvidia"
DEST_MODULE_LOCATION[0]="/kernel/drivers/char/drm"
%if %{mdkversion} >= 200710
DEST_MODULE_NAME[0]="%{modulename}"
%endif
MAKE[0]="make SYSSRC=\${kernel_source_dir} module"
CLEAN="make -f Makefile.kbuild clean"
AUTOINSTALL="yes"
EOF

# OpenGL and CUDA headers
install -d -m755	%{buildroot}%{_includedir}/%{drivername}
cp -a include/*		%{buildroot}%{_includedir}/%{drivername}

# install binaries
install -d -m755			%{buildroot}%{nvidia_bindir}
install -m755 bin/nvidia-settings	%{buildroot}%{nvidia_bindir}
install -m755 bin/nvidia-smi		%{buildroot}%{nvidia_bindir}
install -m755 bin/nvidia-xconfig	%{buildroot}%{nvidia_bindir}
install -m755 bin/nvidia-bug-report.sh	%{buildroot}%{nvidia_bindir}
%if %{mdkversion} >= 200700
install -d -m755			%{buildroot}%{_bindir}
touch					%{buildroot}%{_bindir}/nvidia-settings
touch					%{buildroot}%{_bindir}/nvidia-smi
touch					%{buildroot}%{_bindir}/nvidia-xconfig
touch					%{buildroot}%{_bindir}/nvidia-bug-report.sh
# rpmlint:
chmod 0755				%{buildroot}%{_bindir}/*
%endif

# install man pages
install -d -m755				%{buildroot}%{_mandir}/man1
install -m644 share/man/man1/nvidia-xconfig*	%{buildroot}%{_mandir}/man1
install -m644 share/man/man1/nvidia-settings*	%{buildroot}%{_mandir}/man1
%if %{mdkversion} >= 200700
cd %{buildroot}%{_mandir}/man1
rename nvidia .%{drivername} *
cd -
touch %{buildroot}%{_mandir}/man1/nvidia-xconfig.1%{_extension}
touch %{buildroot}%{_mandir}/man1/nvidia-settings.1%{_extension}
%endif

# menu entry
%if %{mdkversion} <= 200600
install -d -m755 %{buildroot}/%{_menudir}
cat <<EOF >%{buildroot}/%{_menudir}/%{driverpkgname}
?package(%{driverpkgname}):command="%{nvidia_bindir}/nvidia-settings" \
                  icon=%{drivername}-settings.png \
                  needs="x11" \
                  section="System/Configuration/Hardware" \
                  title="NVIDIA Display Settings" \
                  longtitle="Configure NVIDIA X driver" \
                  xdg="true"
EOF
%endif

install -d -m755 %{buildroot}%{nvidia_deskdir}
cat > %{buildroot}%{nvidia_deskdir}/mandriva-nvidia-settings.desktop <<EOF
[Desktop Entry]
Name=NVIDIA Display Settings
Comment=Configure NVIDIA X driver
Exec=%{_bindir}/nvidia-settings
Icon=%{drivername}-settings
Terminal=false
Type=Application
Categories=GTK;Settings;HardwareSettings;X-MandrivaLinux-System-Configuration;
EOF

install -d -m755	%{buildroot}%{_datadir}/applications
touch			%{buildroot}%{_datadir}/applications/mandriva-nvidia-settings.desktop

# icons
install -d -m755 %{buildroot}/%{_miconsdir} %{buildroot}/%{_iconsdir} %{buildroot}/%{_liconsdir}
convert share/pixmaps/nvidia-settings.png -resize 16x16 %{buildroot}/%{_miconsdir}/%{drivername}-settings.png
convert share/pixmaps/nvidia-settings.png -resize 32x32 %{buildroot}/%{_iconsdir}/%{drivername}-settings.png
convert share/pixmaps/nvidia-settings.png -resize 48x48 %{buildroot}/%{_liconsdir}/%{drivername}-settings.png

# install libraries
install -d -m755						%{buildroot}%{nvidia_libdir}/tls
install -m755 lib/tls/libnvidia-tls.so.%{version}		%{buildroot}%{nvidia_libdir}/tls
install -m755 lib/libnvidia-tls.so.%{version}			%{buildroot}%{nvidia_libdir}
install -m755 lib/libnvidia-cfg.so.%{version}			%{buildroot}%{nvidia_libdir}
install -m755 lib/libcuda.so.%{version}				%{buildroot}%{nvidia_libdir}
install -m755 lib/libGL.so.%{version}				%{buildroot}%{nvidia_libdir}
install -m755 lib/libGLcore.so.%{version}			%{buildroot}%{nvidia_libdir}
install -m755 X11R6/lib/libXvMCNVIDIA.so.%{version}		%{buildroot}%{nvidia_libdir}
install -m755 X11R6/lib/libXvMCNVIDIA.a				%{buildroot}%{nvidia_libdir}
/sbin/ldconfig -n						%{buildroot}%{nvidia_libdir}
ln -s libcuda.so.1						%{buildroot}%{nvidia_libdir}/libcuda.so
ln -s libGL.so.1						%{buildroot}%{nvidia_libdir}/libGL.so
ln -s libnvidia-cfg.so.1					%{buildroot}%{nvidia_libdir}/libnvidia-cfg.so
sed 's,__LIBGL_PATH__,%{nvidia_libdir},' lib/libGL.la >		%{buildroot}%{nvidia_libdir}/libGL.la
%ifarch %{biarches}
install -d -m755						%{buildroot}%{nvidia_libdir32}/tls
install -m755 lib32/tls/libnvidia-tls.so.%{version}		%{buildroot}%{nvidia_libdir32}/tls
install -m755 lib32/libnvidia-tls.so.%{version}			%{buildroot}%{nvidia_libdir32}
install -m755 lib32/libGL.so.%{version}				%{buildroot}%{nvidia_libdir32}
install -m755 lib32/libGLcore.so.%{version}			%{buildroot}%{nvidia_libdir32}
/sbin/ldconfig -n						%{buildroot}%{nvidia_libdir32}
ln -s libcuda.so.1						%{buildroot}%{nvidia_libdir32}/libcuda.so
ln -s libGL.so.1						%{buildroot}%{nvidia_libdir32}/libGL.so
ln -s libnvidia-cfg.so.1					%{buildroot}%{nvidia_libdir32}/libnvidia-cfg.so
sed 's,__LIBGL_PATH__,%{nvidia_libdir32},' lib32/libGL.la >	%{buildroot}%{nvidia_libdir32}/libGL.la
%endif

# install X.org files
install -d -m755						%{buildroot}%{xorg_libdir}/modules
install -m755 X11R6/lib/modules/libnvidia-wfb.so.%{version}	%{buildroot}%{xorg_libdir}/modules
/sbin/ldconfig -n						%{buildroot}%{xorg_libdir}/modules
%if %{mdkversion} <= 200800
# provided by xorg server 1.4
ln -s libnvidia-wfb.so.1					%{buildroot}%{xorg_libdir}/modules/libwfb.so
%endif
install -d -m755						%{buildroot}%{nvidia_extensionsdir}
install -m755 X11R6/lib/modules/extensions/libglx.so.%{version}	%{buildroot}%{nvidia_extensionsdir}
ln -s libglx.so.%{version}					%{buildroot}%{nvidia_extensionsdir}/libglx.so
mkdir -p							%{buildroot}%{nvidia_driversdir}
install -m755 X11R6/lib/modules/drivers/nvidia_drv.so		%{buildroot}%{nvidia_driversdir}
%if %{mdkversion} >= 200700
touch								%{buildroot}%{xorg_libdir}/modules/drivers/nvidia_drv.so
%endif
%if %{mdkversion} <= 200900
%if %{mdkversion} >= 200800
touch								%{buildroot}%{xorg_libdir}/modules/extensions/libglx.so
%endif
%endif

# ld.so.conf
install -d -m755		%{buildroot}%{ld_so_conf_dir}
echo "%{nvidia_libdir}" >	%{buildroot}%{ld_so_conf_dir}/%{ld_so_conf_file}
%ifarch %{biarches}
echo "%{nvidia_libdir32}" >>	%{buildroot}%{ld_so_conf_dir}/%{ld_so_conf_file}
%endif
%if %{mdkversion} >= 200700
install -d -m755		%{buildroot}%{_sysconfdir}/ld.so.conf.d
touch				%{buildroot}%{_sysconfdir}/ld.so.conf.d/GL.conf
%endif

# modprobe.conf
%if %{mdkversion} >= 200710
install -d -m755			%{buildroot}%{_sysconfdir}/modprobe.d
touch					%{buildroot}%{_sysconfdir}/modprobe.d/nvidia.conf
echo "alias nvidia %{modulename}" >	%{buildroot}%{_sysconfdir}/%{drivername}/modprobe.conf
%endif

# XvMCConfig
install -d -m755 %{buildroot}%{nvidia_xvmcconfdir}
echo "libXvMCNVIDIA_dynamic.so.1" > %{buildroot}%{nvidia_xvmcconfdir}/XvMCConfig

# don't strip files
export DONT_STRIP=1

%post -n %{driverpkgname}
%if %{mdkversion} >= 200710
# XFdrake used to generate an nvidia.conf file
[ -L %{_sysconfdir}/modprobe.d/nvidia.conf ] || rm -f %{_sysconfdir}/modprobe.d/nvidia.conf
%endif

%if %{mdkversion} >= 200700
current_glconf="$(readlink -e %{_sysconfdir}/ld.so.conf.d/GL.conf)"

%if %{mdkversion} < 200800
# Handle upgrading from setups where libwfb was not using alternatives.
# From 2008.0 onwards the calling of --set after --install on rename makes
# this unnecessary.
if [ "${current_glconf}" = "%{_sysconfdir}/nvidia97xx/ld.so.conf" ]; then
	wfblink="$(readlink %{_libdir}/xorg/modules/libnvidia-wfb.so.1)"
	if [ "${wfblink%.so.1*}" = "libnvidia-wfb" ]; then
		# The below update-alternatives will recreate this
		/bin/rm %{_libdir}/xorg/modules/libnvidia-wfb.so.1
	fi
fi
%endif

%define compat_ext %([ "%{_extension}" == ".bz2" ] || echo %{_extension})
%{_sbindir}/update-alternatives \
	--install %{_sysconfdir}/ld.so.conf.d/GL.conf gl_conf %{ld_so_conf_dir}/%{ld_so_conf_file} %{priority} \
	--slave %{_libdir}/xorg/modules/drivers/nvidia_drv.so nvidia_drv %{_libdir}/xorg/modules/drivers/%{drivername}/nvidia_drv.so \
	--slave %{_libdir}/xorg/modules/libnvidia-wfb.so.1 nvidia_wfb %{_libdir}/xorg/modules/libnvidia-wfb.so.%{version} \
	--slave %{_mandir}/man1/nvidia-settings.1%{_extension} man_nvidiasettings%{compat_ext} %{_mandir}/man1/.%{drivername}-settings.1%{_extension} \
	--slave %{_mandir}/man1/nvidia-xconfig.1%{_extension} man_nvidiaxconfig%{compat_ext} %{_mandir}/man1/.%{drivername}-xconfig.1%{_extension} \
	--slave %{_datadir}/applications/mandriva-nvidia-settings.desktop nvidia_desktop %{nvidia_deskdir}/mandriva-nvidia-settings.desktop \
	--slave %{_bindir}/nvidia-settings nvidia_settings %{nvidia_bindir}/nvidia-settings \
	--slave %{_bindir}/nvidia-smi nvidia_smi %{nvidia_bindir}/nvidia-smi \
	--slave %{_bindir}/nvidia-xconfig nvidia_xconfig %{nvidia_bindir}/nvidia-xconfig \
	--slave %{_bindir}/nvidia-bug-report.sh nvidia_bug_report %{nvidia_bindir}/nvidia-bug-report.sh \
	--slave %{_sysconfdir}/X11/XvMCConfig xvmcconfig %{nvidia_xvmcconfdir}/XvMCConfig \
%if %{mdkversion} <= 200800
	--slave %{_libdir}/xorg/modules/libwfb.so libwfb %{_libdir}/xorg/modules/libnvidia-wfb.so.%{version} \
%endif
%if %{mdkversion} >= 200710
	--slave %{_sysconfdir}/modprobe.d/nvidia.conf nvidia_modconf %{_sysconfdir}/%{drivername}/modprobe.conf \
%endif
%if %{mdkversion} >= 200910
	--slave %{xorg_extra_modules} xorg_extra_modules %{nvidia_extensionsdir} \
	--slave %{_bindir}/Xorg Xorg %{_bindir}/Xorg-1.6
%else
%if %{mdkversion} >= 200900
	--slave %{_libdir}/xorg/modules/extensions/libdri.so libdri.so %{_libdir}/xorg/modules/extensions/standard/libdri.so \
%endif
%if %{mdkversion} >= 200800
	--slave %{_libdir}/xorg/modules/extensions/libglx.so libglx %{nvidia_extensionsdir}/libglx.so
%endif
%endif

# ensure the links are created if its current state is manual
link_state=$(%{_sbindir}/update-alternatives --display gl_conf | head -1)
link_state=$(expr match "$link_state" 'gl_conf - status is \(.*\).')

if [ "$link_state" != "auto" ]; then
	current_link=$(readlink %{_sysconfdir}/alternatives/gl_conf)
	%{_sbindir}/update-alternatives --set gl_conf "$current_link"
fi

%if %{mdkversion} >= 200800
if [ "${current_glconf}" = "%{_sysconfdir}/nvidia97xx/ld.so.conf" ]; then
	# Adapt for the renaming of the driver. X.org config still has the old ModulePaths
	# but they do not matter as we are using alternatives for libglx.so now.
	%{_sbindir}/update-alternatives --set gl_conf %{ld_so_conf_dir}/%{ld_so_conf_file}
fi
%endif
# empty line so that /sbin/ldconfig is not passed to update-alternatives
%endif
# explicit /sbin/ldconfig due to alternatives
/sbin/ldconfig

%postun -n %{driverpkgname}
%if %{mdkversion} >= 200700
if [ ! -f %{ld_so_conf_dir}/%{ld_so_conf_file} ]; then
  %{_sbindir}/update-alternatives --remove gl_conf %{ld_so_conf_dir}/%{ld_so_conf_file}
fi
%endif
# explicit /sbin/ldconfig due to alternatives
/sbin/ldconfig

%post -n dkms-%{drivername}
/usr/sbin/dkms --rpm_safe_upgrade add -m %{drivername} -v %{version}-%{release} &&
/usr/sbin/dkms --rpm_safe_upgrade build -m %{drivername} -v %{version}-%{release} &&
/usr/sbin/dkms --rpm_safe_upgrade install -m %{drivername} -v %{version}-%{release} --force

# rmmod any old driver if present and not in use (e.g. by X)
rmmod nvidia > /dev/null 2>&1 || true

%preun -n dkms-%{drivername}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{drivername} -v %{version}-%{release} --all

# rmmod any old driver if present and not in use (e.g. by X)
rmmod nvidia > /dev/null 2>&1 || true

%clean
rm -rf %{buildroot}

%files -n %{driverpkgname}
%defattr(-,root,root)

%doc README.install.urpmi README.manual-setup
%doc %{pkgname}/usr/share/doc/*
%doc %{pkgname}/LICENSE

# ld.so.conf, modprobe.conf, xvmcconfig
%if %{mdkversion} >= 200710
# 2007.1
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%ghost %{_sysconfdir}/modprobe.d/nvidia.conf
%dir %{_sysconfdir}/%{drivername}
%{_sysconfdir}/%{drivername}/modprobe.conf
%{_sysconfdir}/%{drivername}/ld.so.conf
%{_sysconfdir}/%{drivername}/XvMCConfig
%else
%if %{mdkversion} >= 200700
# 2007.0
%ghost %{_sysconfdir}/ld.so.conf.d/GL.conf
%dir %{_sysconfdir}/ld.so.conf.d/GL
%dir %{_sysconfdir}/%{drivername}
%{_sysconfdir}/ld.so.conf.d/GL/%{drivername}.conf
%{_sysconfdir}/%{drivername}/XvMCConfig
%else
# 2006.0
%config(noreplace) %{_sysconfdir}/X11/XvMCConfig
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{drivername}.conf
%endif
%endif

%if %{mdkversion} >= 200700
%ghost %{_bindir}/nvidia-settings
%ghost %{_bindir}/nvidia-smi
%ghost %{_bindir}/nvidia-xconfig
%ghost %{_bindir}/nvidia-bug-report.sh
%dir %{nvidia_bindir}
%endif
%{nvidia_bindir}/nvidia-settings
%{nvidia_bindir}/nvidia-smi
%{nvidia_bindir}/nvidia-xconfig
%{nvidia_bindir}/nvidia-bug-report.sh

%if %{mdkversion} >= 200700
%ghost %{_mandir}/man1/nvidia-xconfig.1%{_extension}
%ghost %{_mandir}/man1/nvidia-settings.1%{_extension}
%{_mandir}/man1/.%{drivername}-xconfig.1*
%{_mandir}/man1/.%{drivername}-settings.1*
%else
%{_mandir}/man1/nvidia-xconfig.1*
%{_mandir}/man1/nvidia-settings.1*
%endif

%if %{mdkversion} >= 200700
%ghost %{_datadir}/applications/mandriva-nvidia-settings.desktop
%dir %{nvidia_deskdir}
%else
%{_menudir}/%{driverpkgname}
%endif
%{nvidia_deskdir}/mandriva-nvidia-settings.desktop

%{_miconsdir}/%{drivername}-settings.png
%{_iconsdir}/%{drivername}-settings.png
%{_liconsdir}/%{drivername}-settings.png

%dir %{nvidia_libdir}
%dir %{nvidia_libdir}/tls
%{nvidia_libdir}/*.so.%{version}
%{nvidia_libdir}/*.so.1
%{nvidia_libdir}/tls/*.so.%{version}
%{nvidia_libdir}/tls/*.so.1
%ifarch %{biarches}
%dir %{nvidia_libdir32}
%dir %{nvidia_libdir32}/tls
%{nvidia_libdir32}/*.so.%{version}
%{nvidia_libdir32}/*.so.1
%{nvidia_libdir32}/tls/*.so.%{version}
%{nvidia_libdir32}/tls/*.so.1
%endif

%if %{mdkversion} >= 200700
# 2007.0 -
%ghost %{xorg_libdir}/modules/libnvidia-wfb.so.1
%if %{mdkversion} <= 200800
# 2007.0 - 2008.0
%ghost %{xorg_libdir}/modules/libwfb.so
%endif
%else
# - 2006.0
%{xorg_libdir}/modules/libwfb.so
%{xorg_libdir}/modules/libnvidia-wfb.so.1
%endif
%{xorg_libdir}/modules/libnvidia-wfb.so.%{version}

%dir %{nvidia_extensionsdir}
%{nvidia_extensionsdir}/libglx.so.%{version}
%{nvidia_extensionsdir}/libglx.so
%if %{mdkversion} <= 200900
%if %{mdkversion} >= 200800
%ghost %{xorg_libdir}/modules/extensions/libglx.so
%endif
%endif

%if %{mdkversion} >= 200700
%ghost %{xorg_libdir}/modules/drivers/nvidia_drv.so
%dir %{nvidia_driversdir}
%endif
%{nvidia_driversdir}/nvidia_drv.so

%files -n %{drivername}-devel
%defattr(-,root,root)
%{_includedir}/%{drivername}
%{nvidia_libdir}/libXvMCNVIDIA.a
%{nvidia_libdir}/*.so
%{nvidia_libdir}/*.la
%ifarch %{biarches}
%{nvidia_libdir32}/*.so
%{nvidia_libdir32}/*.la
%endif

%files -n dkms-%{drivername}
%defattr(-,root,root)
%doc %{pkgname}/LICENSE
%{_usrsrc}/%{drivername}-%{version}-%{release}

%files -n %{drivername}-doc-html
%defattr(-,root,root)
%doc html-doc/*

