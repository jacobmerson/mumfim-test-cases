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
#CASE="pytorch"
CASE="network"
#MESH_FILE="../simple_model/fine_box.smb"
#MODEL_FILE="../simple_model/fine_box.dmg"
MESH_FILE="./box.smb"
MODEL_FILE="./box.dmg"
 
mpirun -np 2 ./mumfim_multiscale -g $MODEL_FILE -m $MESH_FILE -c $CASE -b $MODEL_TRAITS -a $AMSI_OPTIONS
#mpirun -np 2 xterm -e lldb -- ./mumfim_multiscale -g $MODEL_FILE -m $MESH_FILE -c $CASE -b $MODEL_TRAITS -a $AMSI_OPTIONS
