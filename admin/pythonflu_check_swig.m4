dnl pythonFlu - Python wrapping for OpenFOAM C++ API
dnl Copyright (C) 2010- Alexey Petrov
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
dnl See http://sourceforge.net/projects/pythonflu
dnl
dnl Author : Alexey PETROV
dnl


dnl --------------------------------------------------------------------------------
AC_DEFUN([PYTHONFLU_CHECK_SWIG],
[
AC_CHECKING(pythonFlu check SWIG package)

AC_REQUIRE([CONFFLU_CHECK_SWIG])

if test "x${swig_ok}" = "xyes"; then
  supported_version="The supported versions of the SWIG are 1.3.38-1.3.40, 2.0.3-2.0.6. To use pythonFlu, please install one of them."
  workable_swig="no"
  message="Your SWIG version is not supported"

  if test ${SWIG_NUMERIC_VERSION} -ge "010338" -a ${SWIG_NUMERIC_VERSION} -le "010340"; then
    workable_swig="yes"
  elif test ${SWIG_NUMERIC_VERSION} -ge "020000" -a ${SWIG_NUMERIC_VERSION} -le "020002"; then
    workable_swig="no"
    message="${message}, because there is bug in the SWIG. For more detail see http://sourceforge.net/tracker/index.php?func=detail&aid=3191275&group_id=1645&atid=101645. "
  elif test ${SWIG_NUMERIC_VERSION} -ge "020003" -a ${SWIG_NUMERIC_VERSION} -le "020006"; then
    workable_swig="yes"
  elif test ${SWIG_NUMERIC_VERSION} -eq "020007"; then
    workable_swig="no"
    message="${message}, because there is bug in the SWIG. For more details see http://sourceforge.net/tracker/index.php?func=detail&aid=3530118&group_id=1645&atid=101645"
  fi

  if test "x${workable_swig}" = "xno"; then
    echo ${message}
    echo ${supported_version}
    swig_ok="no"
  fi
    
fi

])


dnl --------------------------------------------------------------------------------
