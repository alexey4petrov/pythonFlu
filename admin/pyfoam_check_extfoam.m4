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


AC_DEFUN([PYFOAM_CHECK_EXTFOAM],dnl
[
AC_CHECKING(for extFoam package)

AC_LANG_SAVE
AC_LANG_CPLUSPLUS

EXTFOAM_CPPFLAGS=""
AC_SUBST(EXTFOAM_CPPFLAGS)

EXTFOAM_CXXFLAGS=""
AC_SUBST(EXTFOAM_CXXFLAGS)

EXTFOAM_LDFLAGS=""
AC_SUBST(EXTFOAM_LDFLAGS)

AC_SUBST(ENABLE_EXTFOAM)

extfoam_ok=no

AC_ARG_WITH( [extfoam],
             AC_HELP_STRING( [--with-extfoam=<path>],
		             [use <path> to look for extFoam installation] ),
             [extfoam_root_dir=${withval}],
	     [withval=yes])
   
if test ! "x${withval}" = "xno" ; then
   if test "x${withval}" = "xyes" ; then
      if test ! "x${DIFFUSION_ROOT_DIR}" = "x" && test -d ${DIFFUSION_ROOT_DIR} ; then
      	 extfoam_root_dir=${DIFFUSION_ROOT_DIR}
      fi
   fi

   AC_CHECK_FILE( [${extfoam_root_dir}/diffusionFoamLib/lnInclude], [ extfoam_ok=yes ], [ extfoam_ok=no ] )

   if test "x${extfoam_ok}" = "xyes" ; then
      EXTFOAM_CPPFLAGS="-I${extfoam_root_dir}/diffusionFoamLib/lnInclude"

      EXTFOAM_CXXFLAGS=""

      EXTFOAM_LDFLAGS="-L${extfoam_root_dir}/lib -lblockMatrix -ldiffusionFoam"
   fi
fi

if test "x${extfoam_ok}" = "xno" ; then
   AC_MSG_WARN([use either \${DIFFUSION_ROOT_DIR} or --with-extfoam=<path>])
fi

ENABLE_EXTFOAM=${extfoam_ok}
])

