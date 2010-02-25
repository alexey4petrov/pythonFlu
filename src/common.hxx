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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef common_hxx
#define common_hxx


//---------------------------------------------------------------------------
%module( directors="1", allprotected="1" ) pyfoam;


//---------------------------------------------------------------------------
%{
  namespace Foam
  {}
  
  using namespace Foam;
  
  int main() 
  {
    return 0;
  }  
  
  // To process error within "director" classes
  #include "error.H"
  
  // To simulate Info functionality with Python "__str__" method
  #include "OStringStream.H"
  #include <stdio.h>
%}


//---------------------------------------------------------------------------
%feature( "director:except" ) 
{
  if ( $error != NULL ) {
    //PyErr_Print();
    Foam::error::printStack( Foam::Info );
    Swig::DirectorMethodException::raise("Error detected when calling director's method");
  }
}


//---------------------------------------------------------------------------
%define DIRECTOR_EXTENDS( Typename )
  static const Foam::Typename&
  ext_lookupObject( const Foam::objectRegistry& theRegistry, const Foam::word& theName )
  {
    const Foam::Typename& res = theRegistry.lookupObject< Foam::Typename >( theName );
    
    if ( const SwigDirector_##Typename* director = dynamic_cast< const SwigDirector_##Typename* >( &res ) )
      return *director;

    return res;
  }
%enddef


//--------------------------------------------------------------------------
%define DIRECTOR_PRE_EXTENDS( Typename )

%{
   #include "Time.H"
   #include "regIOobject.H"
   #include "IOdictionary.H"

   #include "fvPatchField.H"
   #include "src/finiteVolume/fields/fvPatchFields/fvPatchField_ConstructorToTable.hxx"
   #include "mixedFvPatchField.H"
   #include "fixedGradientFvPatchField.H"   

   #include DIRECTOR_INCLUDE
%}

%typemap( out ) Foam::Typename&
{
  Swig::Director *director = SWIG_DIRECTOR_CAST( $1 );
  if ( Swig::Director *director = SWIG_DIRECTOR_CAST( $1 ) ) {
    $result = director->swig_get_self();
    Py_INCREF( $result );
  } else {
    $result = SWIG_NewPointerObj( SWIG_as_voidptr( $1 ), $1_descriptor, 0 |  0 );
  }
}

%enddef


//---------------------------------------------------------------------------
%define BAREPTR_TYPEMAP( Type )

%typemap( in ) Type* ( void  *argp = 0, int check = 0, Type* result ) 
{
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Type * ), SWIG_POINTER_DISOWN | %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = %reinterpret_cast( argp, Type * );
    // "Director" derived classes need special care
    if ( Swig::Director *director = SWIG_DIRECTOR_CAST( result ) ) {
      PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
    }
  }
  $1 = result;
}

%enddef


//---------------------------------------------------------------------------
%define COMMON_EXTENDS
{
  char* __str__()
  {
    Foam::OStringStream aStream;
    aStream << "\n" << *self;
    return strdup( aStream.str().c_str() );
  }
}
%enddef


//---------------------------------------------------------------------------
// To support native Python of iteration over containers
%inline
%{
  namespace Foam
  {
    struct TStopIterationException
    {};

    template< class TContainer >
    struct TContainer_iterator
    {
      typedef typename TContainer::reference TReturnType;

      TContainer_iterator( TContainer& the_Container )
        : m_container( the_Container )
        , m_iter( the_Container.begin() )
      {}

      TReturnType __iter__()
      {
        return *(this->m_iter++);
      }

      TReturnType next() throw( const TStopIterationException& )
      {
        if ( this->m_iter != m_container.end() )
          return this->__iter__();
        
        throw TStopIterationException();
      }

    private :
      TContainer& m_container;
      typename TContainer::iterator m_iter;
    };


    template< class TPtrContainer >
    struct TPtrContainer_iterator
    {
      typedef typename TPtrContainer::value_type TReturnType;

      TPtrContainer_iterator( TPtrContainer& the_Container )
        : m_container( the_Container )
        , m_iter( the_Container.begin() )
      {}

      TReturnType __iter__()
      {
        return *(this->m_iter++);
      }

      TReturnType next() throw( const TStopIterationException& )
      {
        if ( this->m_iter != m_container.end() )
          return this->__iter__();
        
        throw TStopIterationException();
      }

    private :
      TPtrContainer& m_container;
      typename TPtrContainer::iterator m_iter;
    };
  }
%}

%typemap(throws) const Foam::TStopIterationException& %{
  PyErr_SetString( PyExc_StopIteration, "out of range" );
  SWIG_fail;
%}


//---------------------------------------------------------------------------
//For using tmp<T> & autoPtr<T> as T
%define TMP_PYTHONAPPEND_ATTR( Type ) __getattr__
%{
    name = args[ 0 ]
    try:
        return _swig_getattr( self, Type, name )
    except AttributeError:
        if self.valid() :
            attr = None
            exec "attr = self.__call__().%s" % name
            return attr
        pass
    raise AttributeError()
%}
%enddef


//---------------------------------------------------------------------------
%define TMP_EXTEND_ATTR( Type )
    void __getattr__( const char* name ){} // dummy function
%enddef


//---------------------------------------------------------------------------
%ignore operator <<;
%ignore operator >>;

%ignore operator ==;
%ignore operator !=;

%ignore operator -;
%ignore operator +;
%ignore operator *;
%ignore operator /;

%ignore operator &;
%ignore operator ^;

%ignore operator &&;

%ignore *::operator =;
%ignore *::operator [];

%ignore *::operator ++;
%ignore *::operator --;

%ignore *::operator !;


//---------------------------------------------------------------------------
#endif

