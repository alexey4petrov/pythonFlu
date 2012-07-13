---------------------------------------------------------------------------
    pythonFlu r9.1-swig
---------------------------------------------------------------------------

  * Name this release after porting on the latest SWIG 2.X version - "swig" 

  * Porting on the new generation of SWIG wrapper - 2.X 
    (tested with 2.0.3 - 2.0.6)
  
  * Porting on the latest OpenCFD version of OpenFOAM - 2.1.1

  * The following new solvers were implemented in Python :
    
    compressible

	rhoPorousMRFLTSPimpleFoam

    	rhoPorousMRFSimpleFoam
    
	rhoSimplecFoam
    
    heatTransfer

	buoyantBoussinesqPimpleFoam
    
	chtMultiRegionSimpleFoam
    
    incompressible

	adjointShapeOptimizationFoam
    
	MRFSimpleFoam
    
	SRFPimpleFoam
    
	SRFSimpleFoam


---------------------------------------------------------------------------
    pythonFlu r9.0-porting
---------------------------------------------------------------------------

  * Name this release after the its main achivement - "porting on the latest 
    OpenFOAM versions and forks" 

  * Porting on the latest versions of OpenFOAM - 2.1.0 - 2.0.0
  
  * Porting on FreeFOAM up to the 0.1.0rc5
  
  * Porting on MacOS X
  
  * Support for multi-fork and multi-version OpenFOAM installations 
  
  * Moving installation procedure to "launchpad.net" (due to increased number of dependencies)
  
  * Full grown support for writing interactive applications (a special “managedFlu” intermediate 
    C++ layer was designed to provide precise memory management over OpenFOAM objects)
  
  * Advancement of the internal Python related module packaging
  
  * Support writing pure Python custom "functionObject"s


---------------------------------------------------------------------------
    pythonFlu r8.2-hybrid
---------------------------------------------------------------------------

  * Name this release after the reinvoked SALOME to OpenFOAM binding -
    "hybridFlu"

  * hybridFlu functionality comes in sources and was tested
    with SALOME r5.1.3 and OpenFOAM r1.7.1

  * Advancing pythonFlu make system in the way that any other third-party
    functionality can use and extend the referenced pythonFlu wrapping 
    defintion. 

  * As an example how to achive this look in the implementation 
    of hybridFlu related packages (foam2vtk and unv2foam)


---------------------------------------------------------------------------
    pythonFlu r8.1-Elvis
---------------------------------------------------------------------------

  * Name this release after the person who believed in this project 
    and inspired us continue its developement. Thank you "Elvis"!

  * Extracting Python solvers from the initial pythonFlu distribution.
    Since "Elvis" release pythonFlu kernel fucntionality and 
    corresponding Python solvers, that demonstrates this wrapping,
    will be advanced and ditributed separately. We encourage all
    pythonFlu users to follow this practise.
    
    Look at http://pythonflu.wikidot.com/solvers to see the avaialbe
    solvers

    Look at http://pythonflu.wikidot.com/install-solvers to learn
    how to install them

  * The following 7 new solvers were implemented in Python :

    - compressible / rhoPorousMRFPimpleFlux

    - incompressible / porousSimpleFlux
  
    - heatTransfer / buoyantPimpleFlux
  
    - multiPhase / compressibleInterFlux, interDyMFlux

    - multiPhase / twoLiquidMixingFlux (thanks to Dhasthagheer)

    - DNS / dnsFlux

  * The whole pythonFlu wrapping scheme were revised, as result size 
    of the corresponding binary packages were decresed in 3 - 5 times
    and amount of RAM needed to compile them decreased in about 2 times

  * pythonflu.wikidot.com web-site were updated to discuss in details 
    "installation from sources" procedure. Corresponding information
    can be found at http://pythonflu.wikidot.com/install-sources


---------------------------------------------------------------------------
    pythonFlu r8.0
---------------------------------------------------------------------------

  * Porting on the latest 1.7.1 and 1.6-ext OpenFOAM versions

  * "Maturity" of the wrapping increased in 2 times and reached 41% 
    (it is possible to reproduce 26 of 63 referenced OpenFOAM solvers)

  * Preparation of native Linux binary packages
    (available for Ubuntu and OpneSUSE, i386 and amd64 architectures)
  
  * Minor bug-fixing


---------------------------------------------------------------------------
