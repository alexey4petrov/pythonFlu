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
AC_DEFUN([PYTHONFLU_CHECK_CREATING_PACKAGE],
[
  AC_CHECKING(packages which will be included to deb(rpm) package)

  AC_SUBST(WITH_CONFFLU)
 
  AC_SUBST(WITH_SOLVERS)

  AC_ARG_WITH( [confflu],
             AC_HELP_STRING( [--with-confflu],
                             [include confflu to deb(rpm) package] ),
             [WITH_CONFFLU=yes],
             [WITH_CONFFLU=no] )


  AC_ARG_WITH( [solvers],
             AC_HELP_STRING( [--with-solvers],
                             [include solvers & models to deb(rpm) package] ),
             [WITH_SOLVERS=yes],
             [WITH_SOLVERS=no] )

  AC_MSG_NOTICE( @WITH_CONFFLU@ == "${WITH_CONFFLU}" )
  AC_MSG_NOTICE( @WITH_SOLVERS@ == "${WITH_SOLVERS}" )
])


dnl --------------------------------------------------------------------------------
