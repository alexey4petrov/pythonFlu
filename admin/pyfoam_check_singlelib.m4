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
dnl See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
dnl
dnl Author : Alexey PETROV
dnl


dnl --------------------------------------------------------------------------------
AC_DEFUN([PYFOAM_CHECK_SINGLELIB],
[
AC_MSG_CHECKING(whether to use optimized pyFoam libraries structure)

AC_SUBST(USE_SINGLE_LIB)

AC_ARG_ENABLE( [singlelib],
               AC_HELP_STRING( [--disable-singlelib ],
		               [ enable singlelib to speedup compilation process ( disabled by default ) ]),
               [ USE_SINGLE_LIB=$enableval ],
	       [ USE_SINGLE_LIB="yes" ] )

singlelib=${USE_SINGLE_LIB}

AC_MSG_RESULT(${USE_SINGLE_LIB})
])


dnl --------------------------------------------------------------------------------
