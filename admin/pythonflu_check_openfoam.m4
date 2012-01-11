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
AC_DEFUN([PYTHONFLU_CHECK_OPENFOAM],
[
AC_CHECKING(for OPENFOAM package)

AC_REQUIRE([CONFFLU_CHECK_OPENFOAM])

AC_SUBST(PYTHONFLU_CXXFLAGS)

PYTHONFLU_CXXFLAGS=[`echo ${OPENFOAM_CXXFLAGS} | sed -e"s%-Wold-style-cast %%g"`]
PYTHONFLU_CXXFLAGS=[`echo ${PYTHONFLU_CXXFLAGS} | sed -e"s%-Wall %%g"`]
PYTHONFLU_CXXFLAGS=[`echo ${PYTHONFLU_CXXFLAGS} | sed -e"s%-Wextra %%g"`]
dnl PYTHONFLU_CXXFLAGS=[`echo ${PYTHONFLU_CXXFLAGS} | sed -e"s%-O3 %-ggdb3 -DFULLDEBUG %g")`]

AC_MSG_NOTICE( @PYTHONFLU_CXXFLAGS@ == "${PYTHONFLU_CXXFLAGS}" )
AC_SUBST(PYTHONFLU_CXXFLAGS)



])


dnl --------------------------------------------------------------------------------
