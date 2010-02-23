#--------------------------------------------------------------------------------------
__CPPFLAGS__ := $(__CPPFLAGS__) \
	-I$(WM_PROJECT_DIR)/src/finiteVolume/lnInclude \
	-I$(UNV2FOAM_ROOT_DIR)/lib/lnInclude


__LIB_FLAGS__ := $(__LIB_FLAGS__) \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lfiniteVolume \
	-L$(UNV2FOAM_ROOT_DIR)/lib -lunv2foam


#--------------------------------------------------------------------------------------
ifneq "$(UNV2FOAM_ROOT_DIR)xx" "xx"

pyfoam_root_dir:=../../../../..

include $(pyfoam_root_dir)/include.makefile

else

$(warning Define $$(UNV2FOAM_ROOT_DIR) to process this package)

all:
clean:

endif


#--------------------------------------------------------------------------------------
