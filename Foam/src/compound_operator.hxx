//  pythonFlu - Python wrapping for OpenFOAM C++ API
//  Copyright (C) 2010- Alexey Petrov
//  Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
//  
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//  
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//  
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef compound_operator_hxx
#define compound_operator_hxx

//---------------------------------------------------------------------------
//In case of "<x>=" Python operations it is necessary to return "self" 
// (corresponding C++ OpenFOAM API returns void);
// otherwise object will be destroyed
%define PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Type, OperatorName )

%feature("pythonappend") Type::##OperatorName
%{
  return self
%}
%enddef


//-----------
// To prevent propagation of the previously defined "pythonappend" on the derived classes
// (if corresponding C++ OpenFOAM API returns non-void value, it is necessary to use the original SWIG implementation)
%define CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Type, OperatorName )
%feature("pythonappend") Type::##OperatorName##%{%};
%enddef


//--------------------------------------------------------------------------
%define PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Template, Type, OperatorName   )

%feature("pythonappend") Template< Type >::##OperatorName
%{
  return self
%}

%enddef


%define CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Template, Type, OperatorName )

%feature("pythonappend") Template< Type >::##OperatorName##%{%};

%enddef


//--------------------------------------------------------------------------
%define PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_2( Template, Type1, Type2, OperatorName   )

%feature("pythonappend") Template< Type1, Type2 >::##OperatorName
%{
  return self
%}

%enddef
//------------

%define CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_2( Template, Type1, Type2, OperatorName )

%feature("pythonappend") Template< Type1, Type2 >::##OperatorName##%{%};

%enddef


//--------------------------------------------------------------------------
%define PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Template, Type1, Type2, Type3, OperatorName   )

%feature("pythonappend") Template< Type1, Type2, Type3 >::##OperatorName
%{
  return self
%}

%enddef
//------------


%define CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Template, Type1, Type2, Type3, OperatorName )

%feature("pythonappend") Template< Type1, Type2, Type3 >::##OperatorName##%{%};

%enddef


//--------------------------------------------------------------------------
%define PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_4( Template1, Template2, Type1, Type2, Type3, OperatorName   )

%feature("pythonappend") Template1< Template2< Type1, Type2, Type3 > >::##OperatorName
%{
  return self
%}

%enddef
//------------


%define CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_4( Template1, Template2, Type1, Type2, Type3, OperatorName )

%feature("pythonappend") Template1< Template2< Type1, Type2, Type3 > >::##OperatorName##%{%};

%enddef


//--------------------------------------------------------------------------
#endif
