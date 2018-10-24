#!/bin/bash

if [[ "$VIRTUAL_ENV" != "" ]]
then
  invenv=1
else
  invenv=0
fi

if [[ $invenv == 0 ]]; then
    if [ ! -d '.venv' ]; then
        echo "Initializing virtualenv..."
        virtualenv .venv --python=python3
        source .venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        echo "Activating virtualenv..."
        source .venv/bin/activate
    fi
fi

version=`cat version`

echo "Removing old build and dist..."
rm -rf build
rm -rf dist

echo "Pyinstaller packing..."
pyinstaller pybackup2.spec --log-level WARN

echo "Compressing into .tar.gz format..."
tar -czvf dist/pybackup2-ubuntu64-$version.tar.gz -C dist pybackup2

echo "Creating .deb package..."
deb_pkg_dir=dist/pybackup2-ubuntu64-$version

mkdir -p $deb_pkg_dir/DEBIAN
mkdir -p $deb_pkg_dir/usr/bin
mkdir -p $deb_pkg_dir/usr/share/applications
mkdir -p $deb_pkg_dir/usr/share/pixmaps
mkdir -p $deb_pkg_dir/etc/systemd/system

cp dist/pybackup2 $deb_pkg_dir/usr/bin/
cp linux/control $deb_pkg_dir/DEBIAN/
# cp linux/postinst $deb_pkg_dir/DEBIAN/
cp linux/pybackup2.desktop $deb_pkg_dir/usr/share/applications/
cp pybackup2.ico $deb_pkg_dir/usr/share/pixmaps/
# cp pybackup2.service $deb_pkg_dir/etc/systemd/system/

sed -i "s/Version:.*/Version: $version/" $deb_pkg_dir/DEBIAN/control
dpkg-deb --build $deb_pkg_dir
rm -r $deb_pkg_dir

if [[ $invenv == 0 ]]
then
    deactivate
fi

echo "Completed."
