# [-h, --help]                              display this help text
# [-g, --model model_file]                  the model file (.smd)
# [-m, --mesh mesh_file]                    the mesh file (.smb)
# [-c, --case string]                       a string specifying the analysis case to run
# [-b, --traits]                         model traits filename
# [-a, --amsi]                           amsi options filename
#
#
#
AMSI_OPTIONS="./amsi_options_1_1.yaml"
MODEL_TRAITS="./pytorch_test.yaml"
CASE="pytorch"
MESH_FILE="../simple_model/coarse_box.smb"
MODEL_FILE="../simple_model/coarse_box.dmg"
 
mpirun -np 1 ./mumfim_singlescale -g $MODEL_FILE -m $MESH_FILE -c $CASE -b $MODEL_TRAITS -a $AMSI_OPTIONS
