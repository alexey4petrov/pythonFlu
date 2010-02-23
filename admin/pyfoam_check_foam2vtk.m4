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


dnl --------------------------------------------------------------------------------
AC_DEFUN([PYFOAM_CHECK_FOAM2VTK],dnl
[
AC_CHECKING(for foam2vtk package)

AC_REQUIRE([PYFOAM_CHECK_VTK])

AC_LANG_SAVE
AC_LANG_CPLUSPLUS

FOAM2VTK_CPPFLAGS=""
AC_SUBST(FOAM2VTK_CPPFLAGS)

FOAM2VTK_CXXFLAGS=""
AC_SUBST(FOAM2VTK_CXXFLAGS)

FOAM2VTK_LDFLAGS=""
AC_SUBST(FOAM2VTK_LDFLAGS)

AC_SUBST(ENABLE_FOAM2VTK)

foam2vtk_ok=no

dnl --------------------------------------------------------------------------------
AC_ARG_WITH( [foam2vtk],
             AC_HELP_STRING( [--with-foam2vtk=<path>],
		             [use <path> to look for foam2vtk installation] ),
             [foam2vtk_root_dir=${withval}],
	     [withval=yes])
   
dnl --------------------------------------------------------------------------------
if test "x${withval}" = "xyes" ; then
   if test ! "x${FOAM2VTK_ROOT_DIR}" = "x" && test -d ${FOAM2VTK_ROOT_DIR} ; then
      foam2vtk_root_dir=${FOAM2VTK_ROOT_DIR}
   fi
fi

dnl --------------------------------------------------------------------------------
AC_CHECK_FILE( [${foam2vtk_root_dir}/lib/vtkFoamInterfaces.H], [ foam2vtk_ok=yes ], [ foam2vtk_ok=no ] )

if test "x${foam2vtk_ok}" = "xyes" ; then
   FOAM2VTK_CPPFLAGS="-I${foam2vtk_root_dir}/lib/lnInclude"
   CPPFLAGS="${FOAM2VTK_CPPFLAGS}"

   dnl AC_CHECK_HEADERS( [vtkFoamInterfaces.H], [ foam2vtk_ok=yes ], [ foam2vtk_ok=no ] )
fi

dnl --------------------------------------------------------------------------------
AC_CHECK_FILE( [${foam2vtk_root_dir}/lib/libfoam2vtk.so], [ foam2vtk_ok=yes ], [ foam2vtk_ok=no ] )

if test "x${foam2vtk_ok}" = "xyes" ; then
   FOAM2VTK_CXXFLAGS=""

   FOAM2VTK_LDFLAGS="-L${foam2vtk_root_dir}/lib -lfoam2vtk"

   dnl AC_MSG_CHECKING( for linking to foam2vtk library )
   dnl AC_LINK_IFELSE( [ AC_LANG_PROGRAM( [ [ #include <vtkFoamInterfaces.H> ] ],
   dnl    			                [ new Foam::vtkFoamInterface< Foam::scalar >() ] ) ],
   dnl 					[ foam2vtk_ok=yes ],
   dnl 					[ foam2vtk_ok=no ] )
   dnl AC_MSG_RESULT( ${foam2vtk_ok} )
fi

if test "x${foam2vtk_ok}" = "xno" ; then
   AC_MSG_WARN([use either \${FOAM2VTK_ROOT_DIR} or --with-foam2vtk=<path>])
fi

dnl --------------------------------------------------------------------------------
ENABLE_FOAM2VTK=${foam2vtk_ok}
])

