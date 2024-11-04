EXE=/lore/mersoj/biotissue/biotissue/spack-build/macro/test/multiscale/bio_multiscale
#EXE=bio_multiscale
PROBLEM_DIR=`pwd`/${PROBLEM}
MESH_PREFIX=FCL_model
#ELEMS="course"
#ELEMS="fine"
ELEMS="course"
MODEL=FCL_model.smd
#CASES="traction_load_x_newfn"
CASES="uniax_x_cpu"
VALGRIND=false
TOTALVIEW=false
PERF=false
HPCTOOLKIT=false
TTY=`tty`
ETTY=`tty`
HOST=`hostname`
# singlescale
NPS=2
# multiscale
MACROS=1
MICROS=1
LB=-2
#bgq
AMSI_FILE="${PROBLEM_DIR}/amsi_test_options"
