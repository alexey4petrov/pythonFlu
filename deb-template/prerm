#!/bin/sh
# prerm script for #PACKAGE#
#
# see: dh_installdeb(1)

set -e

install_path=`python -c "import os; import Foam; print os.path.dirname( os.path.dirname( os.path.abspath( Foam.__file__ ) ) )"`
sudo easy_install -m Foam
sudo rm -rf ${install_path}/Foam-*.egg*

exit 0
