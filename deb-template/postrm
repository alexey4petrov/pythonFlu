#!/bin/sh
# postrm script for #PACKAGE#
#
# see: dh_installdeb(1)

install_path=`python -c "import os; import Foam; print os.path.dirname( os.path.dirname( os.path.abspath( Foam.__file__ ) ) )"`
sudo rm -rf ${install_path}/Foam

exit 0
