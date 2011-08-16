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
#ifndef functionObject_ConstructorToTable_hh
#define functionObject_ConstructorToTable_hh


//---------------------------------------------------------------------------
#include <Foam/src/OpenFOAM/db/runTimeSelection/runTimeSelectionTables.hh>

#include <functionObject.H>


//---------------------------------------------------------------------------
namespace Foam
{
  // The idea is to redirect static calls to corresponding virtual functions
  // To use this class it will be necessary first too derive from it and provide 
  // some implementation for the pure virtual methods
  template< int counter >        
  struct functionObjectConstructorToTableBase : TConstructorToTableCounter< functionObject >
  {
    //----------------------------------------------------------------------------------------
    static autoPtr< functionObject > 
    New( const word& name, const Time& t, const dictionary& dict )
    { 
      std::cout << "New\n";
      return engine->_new_( name, t, dict ); 
    }
    
    virtual autoPtr< functionObject > 
    _new_( const word& name, const Time& t, const dictionary& dict ) = 0;
    
        
    //----------------------------------------------------------------------------------------
    virtual ~functionObjectConstructorToTableBase()
    {}
    
    void init( functionObjectConstructorToTableBase* derived, const word& lookup )
    {
      engine = derived;
      
      functionObject::constructdictionaryConstructorTables();
      functionObject::dictionaryConstructorTablePtr_->insert( lookup, New );
    }
  private:
    static functionObjectConstructorToTableBase* engine;
  };
    
  template< int counter > functionObjectConstructorToTableBase< counter >* 
  functionObjectConstructorToTableBase< counter >::engine = NULL;
}


//---------------------------------------------------------------------------
#endif
