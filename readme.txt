#--------------------------------------------------------------------------------------
pythonFlu r8.1-Elvis
#--------------------------------------------------------------------------------------

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


#--------------------------------------------------------------------------------------
pythonFlu r8.0
#--------------------------------------------------------------------------------------

  * Porting on the latest 1.7.1 and 1.6-ext OpenFOAM versions

  * "Maturity" of the wrapping increased in 2 times and reached 41% 
    (it is possible to reproduce 26 of 63 referenced OpenFOAM solvers)

  * Preparation of native Linux binary packages
    (available for Ubuntu and OpneSUSE, i386 and amd64 architectures)
  
  * Minor bug-fixing


#--------------------------------------------------------------------------------------
