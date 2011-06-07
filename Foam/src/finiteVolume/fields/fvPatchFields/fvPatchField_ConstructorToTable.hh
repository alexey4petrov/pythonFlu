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
#ifndef fvPatchField_ConstructorToTable_hh
#define fvPatchField_ConstructorToTable_hh


#include <fvPatchField.H>
#include <volMesh.H>


//---------------------------------------------------------------------------
namespace Foam
{
  // A helper class which provides run-time support for the instationation 
  // of the classes derived from this one
  template< class TRegisteredToTable >        
  struct TConstructorToTableCounter
  {
    static int counter()
    {
      return m_Counter;
    }
  protected:
    TConstructorToTableCounter()
    {
      m_Counter += 1;
    }
  private:
    static int m_Counter;
  };
    
  template< class TRegisteredToTable > int TConstructorToTableCounter< TRegisteredToTable >::m_Counter = 0;
}


//---------------------------------------------------------------------------
namespace Foam
{
  // The idea is to redirect static calls to corresponding virtual functions
  // To use this class it will be necessary first too derive from it and provide 
  // some implementation for the pure virtual methods
  template< class Type, int counter >        
  struct fvPatchFieldConstructorToTableBase : TConstructorToTableCounter< fvPatchField< Type > >
  {
    //----------------------------------------------------------------------------------------
    static tmp< fvPatchField< Type > > New_patch( const fvPatch& p, 
                                                  const DimensionedField< Type, volMesh >& iF ) 
    { 
      return engine->new_patch( p, iF ); 
    }
    
    virtual tmp< fvPatchField< Type > > new_patch( const fvPatch& p, 
                                                   const DimensionedField< Type, volMesh >& iF ) = 0;
    
    
    //----------------------------------------------------------------------------------------
    static tmp< fvPatchField< Type > > New_patchMapper( const fvPatchField< Type >& ptf,
                                                        const fvPatch& p, 
                                                        const DimensionedField< Type, volMesh >& iF,
                                                        const fvPatchFieldMapper& m ) 
    { 
      return engine->new_patchMapper( ptf, p, iF, m ); 
    }
    
    
    virtual tmp< fvPatchField< Type > > new_patchMapper( const fvPatchField< Type >& ptf,
                                                         const fvPatch& p, 
                                                         const DimensionedField< Type, volMesh >& iF,
                                                         const fvPatchFieldMapper& m ) = 0;
    
    
    //----------------------------------------------------------------------------------------
    static tmp< fvPatchField< Type > > New_dictionary( const fvPatch& p, 
                                                       const DimensionedField< Type, volMesh >& iF, 
                                                       const dictionary& dict ) 
    { 
      return engine->new_dictionary( p, iF, dict ); 
    }
    
    virtual tmp< fvPatchField< Type > > new_dictionary( const fvPatch& p, 
                                                        const DimensionedField< Type, volMesh >& iF, 
                                                        const dictionary& dict ) = 0;
    
    
    //----------------------------------------------------------------------------------------
    virtual ~fvPatchFieldConstructorToTableBase()
    {}
    
    void init( fvPatchFieldConstructorToTableBase* derived, const word& lookup )
    {
      engine = derived;
      
      fvPatchField< Type >::constructpatchConstructorTables(); 
      fvPatchField< Type >::patchConstructorTablePtr_->insert( lookup, New_patch );
      
      fvPatchField< Type >::constructpatchMapperConstructorTables(); 
      fvPatchField< Type >::patchMapperConstructorTablePtr_->insert( lookup, New_patchMapper ); 
      
      fvPatchField< Type >::constructdictionaryConstructorTables(); 
      fvPatchField< Type >::dictionaryConstructorTablePtr_->insert( lookup, New_dictionary ); 
    }
  private:
    static fvPatchFieldConstructorToTableBase* engine;
    
  };
    
  template< class T, int counter > fvPatchFieldConstructorToTableBase< T, counter >* fvPatchFieldConstructorToTableBase< T, counter >::engine = NULL;
}


//---------------------------------------------------------------------------
#endif
