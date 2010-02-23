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


AC_DEFUN([PYFOAM_CHECK_PYTHON],dnl
[
AC_CHECKING(for Python environemnt)

AC_LANG_SAVE
AC_LANG_CPLUSPLUS

PYTHON_CPPFLAGS=""
AC_SUBST(PYTHON_CPPFLAGS)

PYTHON_CXXFLAGS=""
AC_SUBST(PYTHON_CXXFLAGS)

dnl --------------------------------------------------------------------------------
python_ok=yes
AC_SUBST(python_ok)

AC_CHECK_PROG( [python_ok], [python], [yes], [no] )

if test "x${python_ok}" = "xno" ; then
   AC_MSG_ERROR( [Python need to be installed to continue] )
fi

dnl --------------------------------------------------------------------------------
AC_LANG_RESTORE
])
