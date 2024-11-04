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
MESH_FILE="../real-fcl/meshes/thin_model/fine_anisotropic_refinement_AR2.smb"
MODEL_FILE="../real-fcl/models/FCL_model_thin.dmg"
MODEL_TRAITS="./pytorch_convergence.yaml"
CASE=pytorch_H2_delaunay_bone_uniax_x_one_realization_density_180
 
mpirun -np 2 ./mumfim_multiscale -g $MODEL_FILE -m $MESH_FILE -c $CASE -b $MODEL_TRAITS -a $AMSI_OPTIONS
#mpirun -np 2 xterm -e lldb -- ./mumfim_multiscale -g $MODEL_FILE -m $MESH_FILE -c $CASE -b $MODEL_TRAITS -a $AMSI_OPTIONS
