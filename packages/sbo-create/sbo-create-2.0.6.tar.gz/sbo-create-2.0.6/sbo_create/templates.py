#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Templates date updated: 2023-05-13


def doinst_script():
    bg = "\x1b[48;5;4m"
    fg = "\x1b[38;5;7m"
    cl = f"{bg}{fg}"

    template: str = """
%s################################################################################
%s#                     COPY WHAT YOU WANT EXIT AND PASTE                        #
%s#                          PRESS \"q or Q\" TO EXIT                              #
%s################################################################################

# $RCSfile: doinst.sh,v $
# $Revision: 1.9 $
# $Date: 2023-05-11 07:58:15+01 $
# DW

# NOTE DO:
# PLEASE only keep the functions/sections/commands that you need.
# PLEASE delete EVERYTHING else (including these comments).
# PLEASE let us know in the comment section of the upload form if including
#        custom functions or commands.

# NOTE PLEASE DO NOT:
# Add or change user or group accounts.
# Change any of the default system settings files.
# Add commands that take forever to complete.
# Use applications like checkinstall or installwatch, that 'touch' every file
# on the system.


# NOTE on paths
# Most commands do not have an initial '/' in directory path arguments so that
# they work correctly when using pkgtools --root <path> or $ROOT options.
# Installpkg and friends chdir to $ROOT or --root <path> before installing packages.
# The exceptions are the 'chroot' commands which do use an initial '/'.
# The chroot command is used to avoid files on the host being changed when
# using --root or $ROOT.
#
# Example: /usr/bin/update-desktop-database -q usr/share/applications
#          ^Full path for command^             ^No initial slash^

# NOTE on tests
# [ -e <path> ]    => Tests if a directory or file exists.
# [ -x <command> ] => Tests if command is executable.
#                     Will also fail silently if not -e too.

# NOTE on redirections
# Most commands redirect stdout and stderr to /dev/null to keep down the noise.
# If you need to see error messages while testing, the easiest way is to
# temporarily comment out 2>&1.

# FUNCTION:    config()
# DESCRIPTION: Discards identical copies of config and rc.INIT files.
# ARGUMENTS:   A single filename.
# NOTE
# Files should be installed with a .new extension.
# Example: etc/rc.d/rc.myshinynewdaemon.new
# We don't clobber if it's avoidable.
# "slackpkg new-config" is one way that users can list+process .new files.

config() {
  NEW="$1"
  OLD="$(dirname $NEW)/$(basename $NEW .new)"
  # If there's no config file by that name, mv it over:
  if [ ! -r $OLD ]; then
    mv $NEW $OLD
  elif [ "$(cat $OLD | md5sum)" = "$(cat $NEW | md5sum)" ]; then
    # toss the redundant copy
    rm $NEW
  fi
  # Otherwise, we leave the .new copy for the admin to consider...
}

# FUNCTION:    preserve_perms()
# DESCRIPTION: Keeps the executable bit that a user may have set (or unset) on
#              an rc.INIT or config file since she first installed a package.
# ARGUMENTS:   A single filename.
# NOTE
# This calls the above config() function to discard identical copies.
# Files should be installed with a .new extension.
# Use for files in etc/rc.d/ and etc/profile.d/
# Other config files may also need this.

preserve_perms() {
  NEW="$1"
  OLD="$(dirname $NEW)/$(basename $NEW .new)"
  if [ -e $OLD ]; then
    cp -a $OLD ${NEW}.incoming
    cat $NEW > ${NEW}.incoming
    mv ${NEW}.incoming $NEW
  fi
  config $NEW
}

# FUNCTION:    schema_install()
# DESCRIPTION: Installs options (schemas) to the gnome config database.
# ARGUMENTS:    A single filename.
# NOTE Not to be confused with glib schemas

schema_install() {
  SCHEMA="$1"
  GCONF_CONFIG_SOURCE="xml::etc/gconf/gconf.xml.defaults" \\
  chroot . gconftool-2 --makefile-install-rule \\
    /etc/gconf/schemas/$SCHEMA \\
    1>/dev/null
}

# Examples (NOTE must be *after* their respective function definitions!)

# Does the finished package have files in etc/gconf/schemas/?
schema_install blah.schemas

# Does the finished package have init files in etc/rc.d/?
preserve_perms etc/rc.d/rc.INIT.new

# Does the finished package have config files in etc/?
config etc/configfile.new

# DESCRIPTION: Updates the system desktop database.
# Does the finished package have a .desktop file in usr/share/applications/?
if [ -x /usr/bin/update-desktop-database ]; then
  /usr/bin/update-desktop-database -q usr/share/applications >/dev/null 2>&1
fi

# DESCRIPTION: Updates the system mime database.
# Does the finished package have files in usr/share/mime/?
if [ -x /usr/bin/update-mime-database ]; then
  /usr/bin/update-mime-database usr/share/mime >/dev/null 2>&1
fi

# DESCRIPTION: Updates the GTK icon cache.
# Does the finished package have files in usr/share/icons/hicolor/?
# If other icon themes are installed, then add to/modify this as needed
if [ -e usr/share/icons/hicolor/icon-theme.cache ]; then
  if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -f usr/share/icons/hicolor >/dev/null 2>&1
  fi
fi

# DESCRIPTION: GSettings (glib2) schema compiler.
# Does the finished package have files in usr/share/glib-2.0/schemas/?
# NOTE Not to be confused with gnome setting schemas
if [ -e usr/share/glib-2.0/schemas ]; then
  if [ -x /usr/bin/glib-compile-schemas ]; then
    /usr/bin/glib-compile-schemas usr/share/glib-2.0/schemas >/dev/null 2>&1
  fi
fi

# DESCRIPTION: Updates the GIO cache.
# Does the finished package have files in /usr/lib(64)/gio/modules/?
# If needed -- be sure to sed @LIBDIR@ inside the build script
# Example: sed -i "s|@LIBDIR@|/usr/lib$LIBDIRSUFFIX|g" doinst.sh
# NOTE An initial '/' in the lib dir here because of 'chroot'.
# NOTE Be sure to use double-quotes ""
chroot . /usr/bin/gio-querymodules @LIBDIR@/gio/modules/ 1> /dev/null >/dev/null 2>&1

%s################################################################################
""" % (cl, cl, cl, cl, cl)
    return template


def douninst_script():
    bg = "\x1b[48;5;4m"
    fg = "\x1b[38;5;7m"
    cl = f"{bg}{fg}"
    template: str = """
%s################################################################################
%s#                          PRESS \"q or Q\" TO EXIT                              #
%s################################################################################
#
# douninst.sh
#
# uninstall script for Slackware >= 15.0
#
# NOTE: This script is run AFTER package removal, so be careful!
#       Consider it optional, use if it is really needed.""" % (cl, cl, cl)
    return template


def slack_desc_template(name: str) -> str:
    if not name:
        name: str = 'None'
    template: str = f"""# HOW TO EDIT THIS FILE:
# The "handy ruler" below makes it easier to edit a package description.
# Line up the first '|' above the ':' following the base package name, and
# the '|' on the right side marks the last column you can put a character in.
# You must make exactly 11 lines for the formatting to be correct.  It's also
# customary to leave one space after the ':' except on otherwise blank lines.

{' ':{len(name)}}|-----handy-ruler------------------------------------------------------|
{name}: {name} (short description of app)
{name}:
{name}:
{name}:
{name}:
{name}:
{name}:
{name}:
{name}:
{name}:
{name}:"""
    return template


def info_template(name: str, version: str, maintainer: str, email: str) -> str:
    template: str = f'''PRGNAM="{name}"
VERSION="{version}"
HOMEPAGE=""
DOWNLOAD=""
MD5SUM=""
DOWNLOAD_x86_64=""
MD5SUM_x86_64=""
REQUIRES=""
MAINTAINER="{maintainer}"
EMAIL="{email}"'''
    return template


class SlackBuilds(object):

    def __init__(self, app_name, version, year, maintainer, live):
        self.app_name = app_name
        self.version = version
        self.year = year
        self.maintainer = maintainer
        self.live = live

    def autotools(self):

        autotools_template = """#!/bin/bash

# Slackware build script for %s

# Copyright %s %s %s
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cd $(dirname $0) ; CWD=$(pwd)

PRGNAM=%s
VERSION=${VERSION:-%s}
BUILD=${BUILD:-1}
TAG=${TAG:-_SBo}
PKGTYPE=${PKGTYPE:-tgz}

if [ -z "$ARCH" ]; then
  case "$( uname -m )" in
    i?86) ARCH=i586 ;;
    arm*) ARCH=arm ;;
       *) ARCH=$( uname -m ) ;;
  esac
fi

# If the variable PRINT_PACKAGE_NAME is set, then this script will report what
# the name of the created package would be, and then exit. This information
# could be useful to other scripts.
if [ ! -z "${PRINT_PACKAGE_NAME}" ]; then
  echo "$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE"
  exit 0
fi

TMP=${TMP:-/tmp/SBo}
PKG=$TMP/package-$PRGNAM
OUTPUT=${OUTPUT:-/tmp}

if [ "$ARCH" = "i586" ]; then
  SLKCFLAGS="-O2 -march=i586 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "i686" ]; then
  SLKCFLAGS="-O2 -march=i686 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "x86_64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
elif [ "$ARCH" = "aarch64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
else
  SLKCFLAGS="-O2"
  LIBDIRSUFFIX=""
fi

set -e

rm -rf $PKG
mkdir -p $TMP $PKG $OUTPUT
cd $TMP
rm -rf $PRGNAM-$VERSION
tar xvf $CWD/$PRGNAM-$VERSION.tar.gz
cd $PRGNAM-$VERSION
chown -R root:root .
find -L . \\
 \( -perm 777 -o -perm 775 -o -perm 750 -o -perm 711 -o -perm 555 \\
  -o -perm 511 \) -exec chmod 755 {} \; -o \\
 \( -perm 666 -o -perm 664 -o -perm 640 -o -perm 600 -o -perm 444 \\
  -o -perm 440 -o -perm 400 \) -exec chmod 644 {} \;

CFLAGS="$SLKCFLAGS" \\
CXXFLAGS="$SLKCFLAGS" \\
./configure \\
  --prefix=/usr \\
  --libdir=/usr/lib${LIBDIRSUFFIX} \\
  --sysconfdir=/etc \\
  --localstatedir=/var \\
  --mandir=/usr/man \\
  --docdir=/usr/doc/$PRGNAM-$VERSION \\
  --disable-static \\
  --build=$ARCH-slackware-linux

make
make install DESTDIR=$PKG

# Don't ship .la files:
rm -f $PKG/{,usr/}lib${LIBDIRSUFFIX}/*.la

find $PKG -print0 | xargs -0 file | grep -e "executable" -e "shared object" | grep ELF \\
  | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null || true

find $PKG/usr/man -type f -exec gzip -9 {} \\;
for i in $( find $PKG/usr/man -type l ) ; do ln -s $( readlink $i ).gz $i.gz ; rm $i ; done

# Compress info pages and remove the package's dir file
# If no info pages are installed by the software, don't leave this in the script
rm -f $PKG/usr/info/dir
gzip -9 $PKG/usr/info/*.info*

# Remove perllocal.pod and other special files that don't need to be installed,
# as they will overwrite what's already on the system.  If this is not needed,
# remove it from the script.
# Remove 'special' files
find $PKG -name perllocal.pod \\
  -o -name ".packlist" \\
  -o -name "*.bs" \\
  | xargs rm -f

mkdir -p $PKG/usr/doc/$PRGNAM-$VERSION
cp -a <documentation> $PKG/usr/doc/$PRGNAM-$VERSION
cat $CWD/$PRGNAM.SlackBuild > $PKG/usr/doc/$PRGNAM-$VERSION/$PRGNAM.SlackBuild

mkdir -p $PKG/install
cat $CWD/slack-desc > $PKG/install/slack-desc
cat $CWD/doinst.sh > $PKG/install/doinst.sh

cd $PKG
/sbin/makepkg -l y -c n $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
""" % (self.app_name, self.year, self.maintainer, self.live, self.app_name, self.version)
        return autotools_template

    def cmake(self):

        cmake_template = """#!/bin/bash

# Slackware build script for %s

# Copyright %s %s %s
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cd $(dirname $0) ; CWD=$(pwd)

PRGNAM=%s
VERSION=${VERSION:-%s}
BUILD=${BUILD:-1}
TAG=${TAG:-_SBo}
PKGTYPE=${PKGTYPE:-tgz}

if [ -z "$ARCH" ]; then
  case "$( uname -m )" in
    i?86) ARCH=i586 ;;
    arm*) ARCH=arm ;;
       *) ARCH=$( uname -m ) ;;
  esac
fi

# If the variable PRINT_PACKAGE_NAME is set, then this script will report what
# the name of the created package would be, and then exit. This information
# could be useful to other scripts.
if [ ! -z "${PRINT_PACKAGE_NAME}" ]; then
  echo "$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE"
  exit 0
fi

TMP=${TMP:-/tmp/SBo}
PKG=$TMP/package-$PRGNAM
OUTPUT=${OUTPUT:-/tmp}

if [ "$ARCH" = "i586" ]; then
  SLKCFLAGS="-O2 -march=i586 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "i686" ]; then
  SLKCFLAGS="-O2 -march=i686 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "x86_64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
elif [ "$ARCH" = "aarch64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
else
  SLKCFLAGS="-O2"
  LIBDIRSUFFIX=""
fi

set -e # Exit on most errors

rm -rf $PKG
mkdir -p $TMP $PKG $OUTPUT
cd $TMP
rm -rf $PRGNAM-$VERSION
tar xvf $CWD/$PRGNAM-$VERSION.tar.gz
cd $PRGNAM-$VERSION
chown -R root:root .
find -L . \\
 \\( -perm 777 -o -perm 775 -o -perm 750 -o -perm 711 -o -perm 555 \\
  -o -perm 511 \) -exec chmod 755 {} \\; -o \\
 \\( -perm 666 -o -perm 664 -o -perm 640 -o -perm 600 -o -perm 444 \\
  -o -perm 440 -o -perm 400 \\) -exec chmod 644 {} \\;

mkdir -p build
cd build
  cmake \\
    -DCMAKE_C_FLAGS:STRING="$SLKCFLAGS" \\
    -DCMAKE_CXX_FLAGS:STRING="$SLKCFLAGS" \\
    -DCMAKE_INSTALL_PREFIX=/usr \\
    -DLIB_SUFFIX=${LIBDIRSUFFIX} \\
    -DMAN_INSTALL_DIR=/usr/man \\
    -DCMAKE_BUILD_TYPE=Release ..
  make
  make install/strip DESTDIR=$PKG
cd ..

# Don't ship .la files:
rm -f $PKG/{,usr/}lib${LIBDIRSUFFIX}/*.la

find $PKG -print0 | xargs -0 file | grep -e "executable" -e "shared object" | grep ELF \\
  | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null || true

find $PKG/usr/man -type f -exec gzip -9 {} \\;
for i in $( find $PKG/usr/man -type l ) ; do ln -s $( readlink $i ).gz $i.gz ; rm $i ; done

# Compress info pages and remove the package's dir file
# If no info pages are installed by the software, don't leave this in the script
rm -f $PKG/usr/info/dir
gzip -9 $PKG/usr/info/*.info*

# Remove perllocal.pod and other special files that don't need to be installed,
# as they will overwrite what's already on the system.  If this is not needed,
# remove it from the script.
find $PKG -name perllocal.pod -o -name ".packlist" -o -name "*.bs" | xargs rm -f || true

mkdir -p $PKG/usr/doc/$PRGNAM-$VERSION
cp -a <documentation> $PKG/usr/doc/$PRGNAM-$VERSION
cat $CWD/$PRGNAM.SlackBuild > $PKG/usr/doc/$PRGNAM-$VERSION/$PRGNAM.SlackBuild

mkdir -p $PKG/install
cat $CWD/slack-desc > $PKG/install/slack-desc
cat $CWD/doinst.sh > $PKG/install/doinst.sh

cd $PKG
/sbin/makepkg -l y -c n $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
""" % (self.app_name, self.year, self.maintainer, self.live, self.app_name, self.version)
        return cmake_template

    def perl(self):

        perl_template = """#!/bin/bash

# Slackware build script for %s

# Copyright %s %s %s
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cd $(dirname $0) ; CWD=$(pwd)

PRGNAM=%s
VERSION=${VERSION:-%s}
BUILD=${BUILD:-1}
TAG=${TAG:-_SBo}
PKGTYPE=${PKGTYPE:-tgz}

SRCNAM="$(printf $PRGNAM | cut -d- -f2-)"

if [ -z "$ARCH" ]; then
  case "$( uname -m )" in
    i?86) ARCH=i586 ;;
    arm*) ARCH=arm ;;
       *) ARCH=$( uname -m ) ;;
  esac
fi

# If the variable PRINT_PACKAGE_NAME is set, then this script will report what
# the name of the created package would be, and then exit. This information
# could be useful to other scripts.
if [ ! -z "${PRINT_PACKAGE_NAME}" ]; then
  echo "$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE"
  exit 0
fi

TMP=${TMP:-/tmp/SBo}
PKG=$TMP/package-$PRGNAM
OUTPUT=${OUTPUT:-/tmp}

if [ "$ARCH" = "i586" ]; then
  SLKCFLAGS="-O2 -march=i586 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "i686" ]; then
  SLKCFLAGS="-O2 -march=i686 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "x86_64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
elif [ "$ARCH" = "aarch64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
else
  SLKCFLAGS="-O2"
  LIBDIRSUFFIX=""
fi

set -e

rm -rf $PKG
mkdir -p $TMP $PKG $OUTPUT
cd $TMP
rm -rf $SRCNAM-$VERSION
tar xvf $CWD/$SRCNAM-$VERSION.tar.gz
cd $SRCNAM-$VERSION
chown -R root:root .
find -L . \\
 \\( -perm 777 -o -perm 775 -o -perm 750 -o -perm 711 -o -perm 555 \\
  -o -perm 511 \) -exec chmod 755 {} \\; -o \\
 \\( -perm 666 -o -perm 664 -o -perm 640 -o -perm 600 -o -perm 444 \\
  -o -perm 440 -o -perm 400 \\) -exec chmod 644 {} \\;

# Build method #1 (preferred)
perl Makefile.PL \\
  PREFIX=/usr \\
  INSTALLDIRS=vendor \\
  INSTALLVENDORMAN1DIR=/usr/man/man1 \\
  INSTALLVENDORMAN3DIR=/usr/man/man3
make
make test
make install DESTDIR=$PKG

# Build method #2
# requires perl-Module-Build or perl-Module-Build-Tiny
perl Build.PL \\
  --installdirs vendor \\
  --config installvendorman1dir=/usr/man/man1 \\
  --config installvendorman3dir=/usr/man/man3
./Build
./Build test
./Build install \\
  --destdir $PKG

find $PKG -print0 | xargs -0 file | grep -e "executable" -e "shared object" | grep ELF \\
  | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null || true

find $PKG/usr/man -type f -exec gzip -9 {} \\;
for i in $( find $PKG/usr/man -type l ) ; do ln -s $( readlink $i ).gz $i.gz ; rm $i ; done

# Remove perllocal.pod and other special files that don't need to be installed,
# as they will overwrite what's already on the system.
find $PKG -name perllocal.pod -o -name ".packlist" -o -name "*.bs" | xargs rm -f || true

# Remove empty directories
find $PKG -depth -type d -empty -delete || true

mkdir -p $PKG/usr/doc/$PRGNAM-$VERSION
cp -a <documentation> $PKG/usr/doc/$PRGNAM-$VERSION
cat $CWD/$PRGNAM.SlackBuild > $PKG/usr/doc/$PRGNAM-$VERSION/$PRGNAM.SlackBuild

mkdir -p $PKG/install
cat $CWD/slack-desc > $PKG/install/slack-desc

cd $PKG
/sbin/makepkg -l y -c n $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
""" % (self.app_name, self.year, self.maintainer, self.live, self.app_name, self.version)
        return perl_template

    def python(self):

        python_template = """#!/bin/bash

# Slackware build script for %s

# Copyright %s %s %s
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cd $(dirname $0) ; CWD=$(pwd)

PRGNAM=%s
VERSION=${VERSION:-%s}
BUILD=${BUILD:-1}
TAG=${TAG:-_SBo}
PKGTYPE=${PKGTYPE:-tgz}

if [ -z "$ARCH" ]; then
  case "$( uname -m )" in
    i?86) ARCH=i586 ;;
    arm*) ARCH=arm ;;
       *) ARCH=$( uname -m ) ;;
  esac
fi

# If the variable PRINT_PACKAGE_NAME is set, then this script will report what
# the name of the created package would be, and then exit. This information
# could be useful to other scripts.
if [ ! -z "${PRINT_PACKAGE_NAME}" ]; then
  echo "$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE"
  exit 0
fi

TMP=${TMP:-/tmp/SBo}
PKG=$TMP/package-$PRGNAM
OUTPUT=${OUTPUT:-/tmp}

if [ "$ARCH" = "i586" ]; then
  SLKCFLAGS="-O2 -march=i586 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "i686" ]; then
  SLKCFLAGS="-O2 -march=i686 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "x86_64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
elif [ "$ARCH" = "aarch64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
else
  SLKCFLAGS="-O2"
  LIBDIRSUFFIX=""
fi

set -e

rm -rf $PKG
mkdir -p $TMP $PKG $OUTPUT
cd $TMP
rm -rf $PRGNAM-$VERSION
tar xvf $CWD/$PRGNAM-$VERSION.tar.gz
cd $PRGNAM-$VERSION
chown -R root:root .
find -L . \\
 \\( -perm 777 -o -perm 775 -o -perm 750 -o -perm 711 -o -perm 555 \\
  -o -perm 511 \\) -exec chmod 755 {} \\; -o \\
 \\( -perm 666 -o -perm 664 -o -perm 640 -o -perm 600 -o -perm 444 \\
  -o -perm 440 -o -perm 400 \\) -exec chmod 644 {} \\;

### For python2
python2 setup.py install --root=$PKG

### For python3
python3 setup.py install --root=$PKG

## If your application only has a pyproject.toml:
python3 -m build --wheel --no-isolation
python3 -m installer --destdir "$PKG" dist/*.whl

find $PKG -print0 | xargs -0 file | grep -e "executable" -e "shared object" | grep ELF \\
  | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null || true

find $PKG/usr/man -type f -exec gzip -9 {} \\;
for i in $( find $PKG/usr/man -type l ) ; do ln -s $( readlink $i ).gz $i.gz ; rm $i ; done

mkdir -p $PKG/usr/doc/$PRGNAM-$VERSION
cp -a <documentation> $PKG/usr/doc/$PRGNAM-$VERSION
cat $CWD/$PRGNAM.SlackBuild > $PKG/usr/doc/$PRGNAM-$VERSION/$PRGNAM.SlackBuild

mkdir -p $PKG/install
cat $CWD/slack-desc > $PKG/install/slack-desc
cat $CWD/doinst.sh > $PKG/install/doinst.sh

cd $PKG
/sbin/makepkg -l y -c n $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
""" % (self.app_name, self.year, self.maintainer, self.live, self.app_name, self.version)
        return python_template

    def rubygem(self):

        rubygem_template = """#!/bin/bash

# Slackware build script for %s

# Copyright %s %s %s
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cd $(dirname $0) ; CWD=$(pwd)

PRGNAM=rubygem-%s
VERSION=${VERSION:-%s}
BUILD=${BUILD:-1}
TAG=${TAG:-_SBo}
PKGTYPE=${PKGTYPE:-tgz}

SRCNAM=%s

if [ -z "$ARCH" ]; then
  case "$( uname -m )" in
    i?86) ARCH=i586 ;;
    arm*) ARCH=arm ;;
       *) ARCH=$( uname -m ) ;;
  esac
fi

# If the variable PRINT_PACKAGE_NAME is set, then this script will report what
# the name of the created package would be, and then exit. This information
# could be useful to other scripts.
if [ ! -z "${PRINT_PACKAGE_NAME}" ]; then
  echo "$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE"
  exit 0
fi

TMP=${TMP:-/tmp/SBo}
PKG=$TMP/package-$PRGNAM
OUTPUT=${OUTPUT:-/tmp}

if [ "$ARCH" = "i586" ]; then
  SLKCFLAGS="-O2 -march=i586 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "i686" ]; then
  SLKCFLAGS="-O2 -march=i686 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "x86_64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
elif [ "$ARCH" = "aarch64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
else
  SLKCFLAGS="-O2"
  LIBDIRSUFFIX=""
fi

set -e

rm -rf $PKG
mkdir -p $TMP $PKG $OUTPUT
cd $TMP

# Get the full path of the ruby installation, for gems
DESTDIR=$( ruby -r rbconfig -e '
include RbConfig
printf("%s/%s/gems/%s\\n",
    CONFIG["libdir"],
    CONFIG["RUBY_INSTALL_NAME"],
    CONFIG["ruby_version"]
      )
')

# print a friendly warning of unsatisfied ":runtime" dependencies
# good to leave in place, even if the gem doesn't have any dependencies. 
# things could always change
gem specification $CWD/$SRCNAM-$VERSION.gem | \\
    ruby -r yaml -r rbconfig -e '
c = RbConfig::CONFIG
path = sprintf("%s/%s/gems/%s",
        c["libdir"],
        c["RUBY_INSTALL_NAME"],
        c["ruby_version"])
sys_gemspecs = Dir.glob(path + "/specifications/**/*.gemspec").map {|g| gs = Gem::Specification.load(g); gs.name }
obj = Gem::Specification.from_yaml($stdin)
obj.dependencies.each {|dep|
        if not(dep.type == :runtime)
                next
        end
        if not(sys_gemspecs.include?(dep.name))
                $stderr.write("WARNING: #{dep.name} gem not found\\n")
                sleep 0.5
        end

}'

gem install \\
    --local \\
    --no-update-sources\ \\
    --ignore-dependencies \\
    --backtrace \\
    --install-dir $PKG/$DESTDIR \\
    --bindir $PKG/usr/bin \\
    $CWD/$SRCNAM-$VERSION.gem

find $PKG -print0 | xargs -0 file | grep -e "executable" -e "shared object" | grep ELF \\
  | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null || true

# Remove cached gem from install, if you are so inspired ..
#rm -rf $PKG/$DESTDIR/cache

mkdir -p $PKG/usr/doc/$PRGNAM-$VERSION
tar -x -O --file=$CWD/$SRCNAM-$VERSION.gem data.tar.gz \\
  | tar -xz -C $PKG/usr/doc/$PRGNAM-$VERSION --file=- \\
  <documentation>
cat $CWD/$PRGNAM.SlackBuild > $PKG/usr/doc/$PRGNAM-$VERSION/$PRGNAM.SlackBuild

mkdir -p $PKG/install
cat $CWD/slack-desc > $PKG/install/slack-desc
cat $CWD/doinst.sh > $PKG/install/doinst.sh

cd $PKG
/sbin/makepkg -l y -c n $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
""" % (self.app_name, self.year, self.maintainer, self.live, self.app_name, self.version, self.app_name,
       "%s", "%s", "%s", "%s", "%s", "%s")
        return rubygem_template

    def haskell(self):

        haskell_template = """#!/bin/bash

# Slackware build script for %s

# Copyright %s %s %s
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cd $(dirname $0) ; CWD=$(pwd)

PRGNAM=haskell-%s
VERSION=${VERSION:-%s}
BUILD=${BUILD:-1}
TAG=${TAG:-_SBo}
PKGTYPE=${PKGTYPE:-tgz}

SRCNAM="$( echo $PRGNAM | cut -d- -f2- )"

GHC_VERSION=$(ghc --numeric-version)

if [ -z "$ARCH" ]; then
  case "$( uname -m )" in
    i?86) ARCH=i586 ;;
    arm*) ARCH=arm ;;
       *) ARCH=$( uname -m ) ;;
  esac
fi

# If the variable PRINT_PACKAGE_NAME is set, then this script will report what
# the name of the created package would be, and then exit. This information
# could be useful to other scripts.
if [ ! -z "${PRINT_PACKAGE_NAME}" ]; then
  echo "$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE"
  exit 0
fi

TMP=${TMP:-/tmp/SBo}
PKG=$TMP/package-$PRGNAM
OUTPUT=${OUTPUT:-/tmp}

if [ "$ARCH" = "i586" ]; then
  SLKCFLAGS="-O2 -march=i586 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "i686" ]; then
  SLKCFLAGS="-O2 -march=i686 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "x86_64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
elif [ "$ARCH" = "aarch64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
else
  SLKCFLAGS="-O2"
  LIBDIRSUFFIX=""
fi

set -e

rm -rf $PKG
mkdir -p $TMP $PKG $OUTPUT
cd $TMP
rm -rf $SRCNAM-$VERSION
tar xvf $CWD/$SRCNAM-$VERSION.tar.gz
cd $SRCNAM-$VERSION
chown -R root:root .
find -L . \\
 \( -perm 777 -o -perm 775 -o -perm 750 -o -perm 711 -o -perm 555 \\
  -o -perm 511 \) -exec chmod 755 {} \\; -o \\
 \\( -perm 666 -o -perm 664 -o -perm 640 -o -perm 600 -o -perm 444 \\
  -o -perm 440 -o -perm 400 \\) -exec chmod 644 {} \\;

# Your application will probably need different configure flags;
# these are provided as an example only.
# Be sure to build only shared libraries unless there's some need for
# static.
CFLAGS="$SLKCFLAGS" \\
CXXFLAGS="$SLKCFLAGS" \\
runghc Setup configure \\
  --prefix=/usr \\
  --libdir=/usr/lib${LIBDIRSUFFIX} \\
  --libsubdir=ghc-${GHC_VERSION}/$SRCNAM-$VERSION \\
  --enable-shared \\
  --enable-library-profiling \\
  --docdir=/usr/doc/$PRGNAM-$VERSION

runghc Setup build
runghc Setup haddock
runghc Setup copy --destdir=$PKG
runghc Setup register --gen-pkg-config

PKGCONFD=/usr/lib${LIBDIRSUFFIX}/ghc-${GHC_VERSION}/package.conf.d
PKGID=$( grep -E "^id: " $SRCNAM-$VERSION.conf | cut -d" " -f2 )
mkdir -p $PKG/$PKGCONFD
mv $SRCNAM-$VERSION.conf $PKG/$PKGCONFD/$PKGID.conf

find $PKG -print0 | xargs -0 file | grep -e "executable" -e "shared object" | grep ELF \\
  | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null || true

mkdir -p $PKG/usr/doc/$PRGNAM-$VERSION
cp -a <documentation> $PKG/usr/doc/$PRGNAM-$VERSION
cat $CWD/$PRGNAM.SlackBuild > $PKG/usr/doc/$PRGNAM-$VERSION/$PRGNAM.SlackBuild

mkdir -p $PKG/install
cat $CWD/slack-desc > $PKG/install/slack-desc
cat $CWD/doinst.sh > $PKG/install/doinst.sh

cd $PKG
/sbin/makepkg -l y -c n $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
""" % (self.app_name, self.year, self.maintainer, self.live, self.app_name, self.version)
        return haskell_template

    def meson(self):

        autotools_template = """#!/bin/bash

# Slackware build script for %s

# Copyright %s %s %s
# All rights reserved.
#
# Redistribution and use of this script, with or without modification, is
# permitted provided that the following conditions are met:
#
# 1. Redistributions of this script must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
#  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO
#  EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

cd $(dirname $0) ; CWD=$(pwd)

PRGNAM=%s
VERSION=${VERSION:-%s}
BUILD=${BUILD:-1}
TAG=${TAG:-_SBo}
PKGTYPE=${PKGTYPE:-tgz}

if [ -z "$ARCH" ]; then
  case "$( uname -m )" in
    i?86) ARCH=i586 ;;
    arm*) ARCH=arm ;;
       *) ARCH=$( uname -m ) ;;
  esac
fi

# If the variable PRINT_PACKAGE_NAME is set, then this script will report what
# the name of the created package would be, and then exit. This information
# could be useful to other scripts.
if [ ! -z "${PRINT_PACKAGE_NAME}" ]; then
  echo "$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE"
  exit 0
fi

TMP=${TMP:-/tmp/SBo}
PKG=$TMP/package-$PRGNAM
OUTPUT=${OUTPUT:-/tmp}

if [ "$ARCH" = "i586" ]; then
  SLKCFLAGS="-O2 -march=i586 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "i686" ]; then
  SLKCFLAGS="-O2 -march=i686 -mtune=i686"
  LIBDIRSUFFIX=""
elif [ "$ARCH" = "x86_64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
elif [ "$ARCH" = "aarch64" ]; then
  SLKCFLAGS="-O2 -fPIC"
  LIBDIRSUFFIX="64"
else
  SLKCFLAGS="-O2"
  LIBDIRSUFFIX=""
fi

set -e
# If you prefer to do selective error checking with
#   command || exit 1
# then that's also acceptable.

rm -rf $PKG
mkdir -p $TMP $PKG $OUTPUT
cd $TMP
rm -rf $PRGNAM-$VERSION
tar xvf $CWD/$PRGNAM-$VERSION.tar.gz
cd $PRGNAM-$VERSION
chown -R root:root .
find -L . \\
 \\( -perm 777 -o -perm 775 -o -perm 750 -o -perm 711 -o -perm 555 \\
  -o -perm 511 \) -exec chmod 755 {} \\; -o \\
 \\( -perm 666 -o -perm 664 -o -perm 640 -o -perm 600 -o -perm 444 \\
  -o -perm 440 -o -perm 400 \\) -exec chmod 644 {} \\;

mkdir build
cd build
  CFLAGS="$SLKCFLAGS" \\
  CXXFLAGS="$SLKCFLAGS" \\
  meson .. \\
    --buildtype=release \\
    --infodir=/usr/info \\
    --libdir=/usr/lib${LIBDIRSUFFIX} \\
    --localstatedir=/var \\
    --mandir=/usr/man \\
    --prefix=/usr \\
    --sysconfdir=/etc \\
    -Dstrip=true
  "${NINJA:=ninja}"
  DESTDIR=$PKG $NINJA install
cd ..

rm -f $PKG/{,usr/}lib${LIBDIRSUFFIX}/*.la

find $PKG -print0 | xargs -0 file | grep -e "executable" -e "shared object" | grep ELF \\
  | cut -f 1 -d : | xargs strip --strip-unneeded 2> /dev/null || true

find $PKG/usr/man -type f -exec gzip -9 {} \\;
for i in $( find $PKG/usr/man -type l ) ; do ln -s $( readlink $i ).gz $i.gz ; rm $i ; done

# Compress info pages and remove the package's dir file
# If no info pages are installed by the software, don't leave this in the script
rm -f $PKG/usr/info/dir
gzip -9 $PKG/usr/info/*.info*

find $PKG -name perllocal.pod \\
  -o -name ".packlist" \\
  -o -name "*.bs" \\
  | xargs rm -f

mkdir -p $PKG/usr/doc/$PRGNAM-$VERSION
cp -a <documentation> $PKG/usr/doc/$PRGNAM-$VERSION
cat $CWD/$PRGNAM.SlackBuild > $PKG/usr/doc/$PRGNAM-$VERSION/$PRGNAM.SlackBuild

mkdir -p $PKG/install
cat $CWD/slack-desc > $PKG/install/slack-desc
cat $CWD/doinst.sh > $PKG/install/doinst.sh

cd $PKG
/sbin/makepkg -l y -c n $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
""" % (self.app_name, self.year, self.maintainer, self.live, self.app_name, self.version)
        return autotools_template
