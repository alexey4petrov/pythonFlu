#--------------------------------------------------------------------------------------
__CXX_INCLUDES__ := $(__CXX_INCLUDES__) \
	-I$(WM_PROJECT_DIR)/src/finiteVolume/lnInclude \
	-I$(VTKHOME)/include/vtk-5.0 \
	-I$(FOAM2VTK_ROOT_DIR)/lib/lnInclude


__LIB_FLAGS__ := $(__LIB_FLAGS__) \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lfiniteVolume \
	-L$(FOAM2VTK_ROOT_DIR)/lib -lfoam2vtk


#--------------------------------------------------------------------------------------
ifneq "$(FOAM2VTK_ROOT_DIR)xx" "xx"

pyfoam_root_dir:=../../../../..

include $(pyfoam_root_dir)/include.makefile

else

$(warning Define $$(FOAM2VTK_ROOT_DIR) to process this package)

all:
clean:

endif


#--------------------------------------------------------------------------------------
