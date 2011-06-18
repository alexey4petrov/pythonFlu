dnl confFlu - pythonFlu configuration package
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
AC_DEFUN([CONFFLU_CHECK_PYTHONFLU],
[
AC_CHECKING(for pyFoam package)

AC_REQUIRE([CONFFOAM_CHECK_OPENFOAM])
AC_REQUIRE([CONFFOAM_CHECK_SWIG])
AC_REQUIRE([CONFFOAM_CHECK_PYTHON])

AC_SUBST(ENABLE_PYTHONFLU)
AC_SUBST(PYTHONFLU_ROOT_DIR)

pythonflu_ok=no
PYTHONFLU_ROOT_DIR=""

dnl --------------------------------------------------------------------------------
check_pythonflu=[`python -c "import Foam.finiteVolume; print \"ok\"" 2>/dev/null`]

if test "${check_pythonflu}" == "ok"; then
    pythonflu_ok=yes
    PYTHONFLU_ROOT_DIR=[`python -c "import os; import Foam; print os.path.dirname( os.path.dirname( os.path.abspath( Foam.__file__ ) ) )"`]
fi


dnl --------------------------------------------------------------------------------
ENABLE_PYTHONFLU=${pythonflu_ok}
])


dnl --------------------------------------------------------------------------------
