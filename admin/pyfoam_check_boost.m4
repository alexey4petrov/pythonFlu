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


AC_DEFUN([PYFOAM_CHECK_BOOST],dnl
[
AC_CHECKING(for Boost Library)

AC_LANG_SAVE
AC_LANG_CPLUSPLUS

BOOST_CPPFLAGS=""
AC_SUBST(BOOST_CPPFLAGS)

BOOST_CXXFLAGS=""
AC_SUBST(BOOST_CXXFLAGS)

ENABLE_BOOST="no"
AC_SUBST(ENABLE_BOOST)

boost_ok=no
AC_SUBST(boost_ok)

AC_ARG_WITH( [boost],
             AC_HELP_STRING([--with-boost=<path>],
		            [use <path> to look for Boost installation]),
             [],
	     [withval=yes])
   
if test ! "x${withval}" = "xno" ; then
   if test "x${withval}" = "xyes" ; then
      if test ! "x${BOOSTDIR}" = "x" && test -d ${BOOSTDIR} ; then
      	 boost_dir=${BOOSTDIR}
      else
	 boost_dir="/usr"
      fi
   else
      boost_dir=${withval}
   fi

   AC_CHECK_FILE( [${boost_dir}/include/boost/shared_ptr.hpp], [ boost_ok=yes ], [ boost_ok=no ] )

   if test "x${boost_ok}" = "xyes" ; then
      test ! "x${boost_dir}" = "x/usr" && BOOST_CPPFLAGS="-I${boost_dir}/include"
      CPPFLAGS="${BOOST_CPPFLAGS}"

      BOOST_CXXFLAGS="-ftemplate-depth-40"
      CXXFLAGS="${BOOST_CXXFLAGS}"

      AC_CHECK_HEADERS( [boost/shared_ptr.hpp], [ boost_ok=yes ], [ boost_ok=no ] )

      if test "x${boost_ok}" = "xyes" ; then
         AC_MSG_CHECKING( Boost shared_ptr functionality )
      	 AC_LINK_IFELSE( [ AC_LANG_PROGRAM( [ [ #include <boost/shared_ptr.hpp> ] ],
      			                    [ [ boost::shared_ptr< int >( new int ) ] ] ) ],
					    [ boost_ok=yes ],
					    [ boost_ok=no ] )
         AC_MSG_RESULT( ${boost_ok} )
      fi
   fi
fi

if test "x${boost_ok}" = "xno" ; then
   AC_MSG_WARN([use either ${BOOSTDIR} or --with-boost=<path>])
fi

ENABLE_BOOST=${boost_ok}

AC_LANG_RESTORE
])
