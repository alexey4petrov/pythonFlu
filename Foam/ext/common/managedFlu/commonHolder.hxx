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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
#ifndef commonHolder_hxx
#define commonHolder_hxx


//---------------------------------------------------------------------------
%define HOLDERS_CALL_SHARED_PTR_EXTENSION( Type )
Foam::Type& __call__()
{
  return self->operator*();
}
%enddef

%define HOLDERS_CALL_SMART_TMP_EXTENSION( Type )
Foam::Type& __call__()
{
  return self->operator()();
}
%enddef

%define HOLDERS_CALL_SMART_TMP_EXTENSION_TEMPLATE1( Template, Type )
Template< Type >& __call__()
{
  return self->operator()();
}
%enddef

%define HOLDERS_CALL_SMART_TMP_EXTENSION_TEMPLATE2( Template, Type1, Type2 )
Template< Type1, Type2 >& __call__()
{
  return self->operator()();
}
%enddef

%define HOLDERS_CALL_SMART_TMP_EXTENSION_TEMPLATE3( Template, Type1, Type2, Type3 )
Template< Type1, Type2, Type3 >& __call__()
{
  return self->operator()();
}
%enddef


//--------------------------------------------------------------------------------------
%define FUNCTION_HOLDER_EXTEND( Type )
{
Type##Holder holder( const Foam::Deps& the_deps )
{
  return Type##Holder( boost::shared_ptr< Type >( self ), the_deps );
}
}
%enddef


//--------------------------------------------------------------------------------------
%define FUNCTION_HOLDER_EXTEND_SMART_PTR_TEMPLATE1( Template, Type1 )
{
Template##Holder< Type1 > holder( const Foam::Deps& the_deps )
{
  return Template##Holder< Type1 >(  get_smart_tmp( self ), the_deps );
}
}
%enddef

%define FUNCTION_HOLDER_EXTEND_SMART_PTR_TEMPLATE3( Template, Type1, Type2, Type3 )
{
Template##Holder< Type1, Type2, Type3 > holder( const Foam::Deps& the_deps )
{
  return Template##Holder< Type1, Type2, Type3 >( get_smart_tmp( self ), the_deps );
}
}
%enddef


//--------------------------------------------------------------------------------------
#endif
