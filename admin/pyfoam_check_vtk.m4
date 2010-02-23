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
AC_DEFUN([PYFOAM_CHECK_VTK],dnl
[
AC_CHECKING(for VTK Library)

AC_LANG_SAVE
AC_LANG_CPLUSPLUS

VTK_CPPFLAGS=""
AC_SUBST(VTK_CPPFLAGS)

VTK_CXXFLAGS=""
AC_SUBST(VTK_CXXFLAGS)

VTK_LDFLAGS=""
AC_SUBST(VTK_LDFLAGS)

vtk_ok=yes

dnl --------------------------------------------------------------------------------
vtk_includes_ok=no
AC_ARG_WITH( [vtk_includes],
             AC_HELP_STRING( [--with-vtk-includes=<path>],
		             [use <path> to look for VTK includes] ),
             [],
	     [ with_vtk_includes=no ] )
   
dnl AC_MSG_NOTICE( \${with_vtk_includes} ${with_vtk_includes})

if test "x${with_vtk_includes}" = "xno" ; then
   with_vtk_includes=/usr/include/`ls /usr/include | grep vtk`
fi

AC_CHECK_FILE( [${with_vtk_includes}/vtkPlane.h], [ vtk_includes_ok=yes ], [ vtk_includes_ok=no ] )

if test "x${vtk_includes_ok}" = "xyes" ; then
   VTK_CPPFLAGS="-I${with_vtk_includes}"
   CPPFLAGS="${VTK_CPPFLAGS}"

   AC_CHECK_HEADERS( [vtkPlane.h], [ vtk_includes_ok=yes ], [ vtk_includes_ok=no ] )
fi

if test "x${vtk_includes_ok}" = "xno" ; then
   AC_MSG_ERROR( [use --with-vtk-includes=<path> to define VTK header files location] )
fi

dnl --------------------------------------------------------------------------------
vtk_libraries_ok=no
AC_ARG_WITH( [vtk_libraries],
             AC_HELP_STRING( [--with-vtk-libraries=<path>],
		             [use <path> to look for VTK libraries] ),
             [],
	     [ with_vtk_libraries=no ]  )
   
if test "x${with_vtk_libraries}" = "xno" ; then
   with_vtk_libraries=/usr/lib
fi

AC_CHECK_FILE( [${with_vtk_libraries}/libvtkCommon.so], [ vtk_libraries_ok=yes ], [ vtk_libraries_ok=no ] )

if test "x${vtk_libraries_ok}" = "xyes" ; then
   VTK_CXXFLAGS="-Wno-deprecated"
   CXXFLAGS="${VTK_CXXFLAGS}"

   test ! "x${with_vtk_libraries}" = "x/usr/lib" && VTK_LDFLAGS="-L${with_vtk_libraries}"
   LDFLAGS="${VTK_LDFLAGS} -lvtkCommon -lvtkFiltering"

   AC_MSG_CHECKING( for linking to VTK libraries )
   AC_LINK_IFELSE( [ AC_LANG_PROGRAM( [ [ #include <vtkPlane.h> ] ],
      			                [ [ vtkPlane::New() ] ] ) ],
					[ vtk_libraries_ok=yes ],
					[ vtk_libraries_ok=no ] )
   AC_MSG_RESULT( ${vtk_libraries_ok} )
fi

if test "x${vtk_libraries_ok}" = "xno" ; then
   AC_MSG_ERROR( [use --with-vtk-libraries=<path> to define VTK libraries location] )
fi

dnl --------------------------------------------------------------------------------
AC_LANG_RESTORE
])
