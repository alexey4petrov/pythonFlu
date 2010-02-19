dnl Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
dnl 
dnl This program is free software: you can redistribute it and/or modify
dnl it under the terms of the GNU General Public License as published by
dnl the Free Software Foundation, either version 3 of the License, or
dnl (at your option) any later version.
dnl
dnl This program is distributed in the hope that it will be useful,
dnl but WITHOUT ANY WARRANTY; without even the implied warranty of
dnl MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
dnl GNU General Public License for more details.
dnl 
dnl You should have received a copy of the GNU General Public License
dnl along with this program.  If not, see <http://www.gnu.org/licenses/>.
dnl 
dnl See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
dnl
dnl Author : Alexey PETROV
dnl


AC_DEFUN([PYFOAM_CHECK_OPENFOAM],dnl
[
AC_CHECKING(for OpenFOAM library)

openfoam_ok=no

if test ! "x${withval}" = "xno" ; then
   AC_MSG_CHECKING(location of the OpenFOAM installation)
   if test -d "${WM_PROJECT_DIR}" ; then
      openfoam_ok=yes
   fi
   AC_MSG_RESULT($openfoam_ok)
fi

if test "x${openfoam_ok}" = "xno" ; then
   AC_MSG_ERROR([it is neceesary to source OpenFOAM environment first])
fi

])

