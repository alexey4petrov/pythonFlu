#!/usr/bin/env python

import ext_icoFoam

class py_get_time( ext_icoFoam.t_get_time_base ):
	def __init__( self ):
	    ext_icoFoam.t_get_time_base.__init__( self )
	    
            from Foam.OpenFOAM import Time, fileName
            a_runTime = Time( Time.controlDictName.fget(), fileName( "." ), fileName( "cavity" ) )
        
            from ext_icoFoam import shared_ptr_Time
            self.m_runTime_ptr = shared_ptr_Time(a_runTime)
        
        def call ( self ): 
            return self.m_runTime_ptr
        
class get_mesh( ext_icoFoam.t_get_mesh_base ):
    def __init__(self):
        ext_icoFoam.t_get_mesh_base.__init__(self)                
    def call( self,the_runTime):
        
        from Foam.OpenFOAM.include import createMesh
        a_mesh = createMesh( the_runTime )
        
        from ext_icoFoam import shared_ptr_fvMesh
        self.m_mesh_ptr = shared_ptr_fvMesh(a_mesh) 
        
        return self.m_mesh_ptr
        
class get_fields( ext_icoFoam.t_get_fields_base ):
    def __init__(self):
        ext_icoFoam.t_get_fields_base .__init__(self)
    def call( self, the_runTime, the_mesh  ):
        
        import createFields
        transportProperties, nu, p, U, phi, pRefCell, pRefValue = createFields.createFields( the_runTime, the_mesh )

        self.m_fields = ext_icoFoam.t_fields()
        
        from ext_icoFoam import shared_ptr_IOdictionary
        self.m_fields.transportProperties_ptr = shared_ptr_IOdictionary( transportProperties )
        
        from ext_icoFoam import shared_ptr_volScalarField
        self.m_fields.p_ptr = shared_ptr_volScalarField( p )
        
        from ext_icoFoam import shared_ptr_volVectorField
        self.m_fields.U_ptr = shared_ptr_volVectorField( U )
        
        from ext_icoFoam import shared_ptr_surfaceScalarField
        self.m_fields.phi_ptr = shared_ptr_surfaceScalarField( phi )
        
        from ext_icoFoam import shared_ptr_dimensionedScalar
        self.m_fields.nu_ptr = shared_ptr_dimensionedScalar( nu )

        self.m_fields.pRefCell = pRefCell
        self.m_fields.pRefValue = pRefValue
        
        return self.m_fields
        
class get_piso_ctrls( ext_icoFoam.t_piso_controls_base ):
    def __init__(self):
        ext_icoFoam.t_piso_controls_base.__init__( self )
    def call(self,the_mesh):
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr, ddtPhiCorr = readPISOControls( the_mesh )

        a_piso_ctrls = ext_icoFoam.t_piso_controls()
        a_piso_ctrls.piso = piso
        a_piso_ctrls.nCorr = nCorr
        a_piso_ctrls.nNonOrthCorr = nNonOrthCorr
        a_piso_ctrls.momentumPredictor = momentumPredictor
        a_piso_ctrls.fluxGradp =False 
        # no ddtPhiCorr in icoFoam.c, no fluxGradp in icoFoam.py
        a_piso_ctrls.transSonic = transonic
        a_piso_ctrls.nOuterCorr = nOuterCorr
        return a_piso_ctrls
        
#---------main-------------

a_getTime=py_get_time()
a_getmesh=get_mesh()
a_getfields=get_fields()
a_piso_controls=get_piso_ctrls()
 

my_solver=ext_icoFoam.solver(a_getTime,a_getmesh,a_getfields)
my_solver.run(a_piso_controls)


