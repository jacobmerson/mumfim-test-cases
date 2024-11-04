MESH=meshes/thin_model/fine_anisotropic_refinement_AR2.smb
#MESH=meshes/thin_model/fine_anisotropic_refinement_AR2_8p.smb
MODEL=models/FCL_model_thin.dmg
CASE=bone_uniax_x 
ATTRIBUTES=models/test_ICNN.yaml
#mpirun -np 6 mumfim_multiscale -g $MODEL -m $MESH -c $CASE -b $ATTRIBUTES -a amsi_options_1_5.yaml
# single scale run
mpirun -np 1 mumfim_singlescale -g $MODEL -m $MESH -c $CASE -b $ATTRIBUTES -a amsi_options_1_5.yaml
