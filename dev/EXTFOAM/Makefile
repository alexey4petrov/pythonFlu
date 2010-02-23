__CPPFLAGS__ := $(__CPPFLAGS__) \
	-I$(WM_PROJECT_DIR)/src/finiteVolume/lnInclude \
	-I$(EXTFOAM_ROOT_DIR)/src/OpenFOAM/lnInclude \
        -I$(PYFOAM_ROOT_DIR)/src
# -lextfoam

__LDFLAGS__ := $(__LDFLAGS__) \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lfiniteVolume \
	-L$(EXTFOAM_ROOT_DIR)/lib 


pyfoam_root_dir:=../..

include $(pyfoam_root_dir)/include.makefile
