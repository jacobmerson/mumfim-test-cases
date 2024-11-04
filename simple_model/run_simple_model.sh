#!/bin/bash
#SBATCH -t 02:00:00
#SBATCH -N 6
#SBATCH -n 37
#SBATCH --gres=gpu:6 -C cuda-mode-exclusive
#SBATCH --cpus-per-gpu=24
#SBATCH -J uniform_networks
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mersoj2@rpi.edu

module load spectrum-mpi
EXE=/gpfs/u/scratch/PASC/shared/spack/spack/var/spack/environments/mumfim/.spack-env/view/bin/mumfim_multiscale
BASE_DIR=/gpfs/u/scratch/PASC/PASCmrsn/simple_model/
MESH=${BASE_DIR}/fine_box.smb
MODEL=${BASE_DIR}/fine_box.dmg
#MESH=${BASE_DIR}/fine_box2_4parts.smb
#MODEL=${BASE_DIR}/fine_box2.dmg
#ATTRIBUTES=${BASE_DIR}/simple_model_delaunay_nets.yaml
ATTRIBUTES=${BASE_DIR}/simple_model.yaml
AMSI_OPTIONS=${BASE_DIR}/amsi_options_${SLURM_JOB_ID}.yaml
## Couse Mesh Cases:
#CASE="bone_uniax_x_decrease_steps_and_damping"
#CASE=increase_step_size
#CASE=high_modulus2
#CASE=high_modulus_increase_damping
CASE=small_steps_E1000x

NUM_GPU_PER_NODE=6
NUM_MACRO_RANKS=1
NUM_MICRO_RANKS=36
#NUM_MICRO_RANKS=`expr ${NUM_MACRO_RANKS} \* ${NUM_GPU_PER_NODE}`

cat >> ${AMSI_OPTIONS} << EOF
amsi: 
  multiscale: 
    scales:
      macro: ${NUM_MACRO_RANKS}
      micro_fo: ${NUM_MICRO_RANKS}
    relations:
      macro: [micro_fo]
      micro_fo: [macro]
  analysis:
    petsc:
      enabled: true
      options file: ${BASE_DIR}/petsc_options_pilut
    results directory: ${BASE_DIR}/uniform_results/${CASE}_${SLURM_JOB_ID}
EOF


export KOKKOS_NUM_DEVICES=${NUM_GPU_PER_NODE}

echo "Starting Job at `date` on $HOSTNAME"
echo "JOB_ID: $SLURM_JOB_ID"
echo "JOB_NAME: $SLURM_JOB_NAME"
echo "JOB_NPROCS: $SLURM_NPROCS"
echo "EXE: $EXE"
echo "AMSI Options: $AMSI_OPTIONS"
echo "Mesh: $MESH"
echo "Model: $MODEL"
echo "Case: $CASE"
echo "MACRO RANKS: ${NUM_MACRO_RANKS}"
echo "MICRO RANKS: ${NUM_MICRO_RANKS}"
echo "Attributes: $ATTRIBUTES"
echo "KOKKOS_DEVICES: " ${KOKKOS_NUM_DEVICES}


REMAINDER=0
if [ "x$SLURM_NPROCS" = "x" ]
then
  if [ "x$SLURM_NTASKS_PER_NODE" = "x" ]
  then
    SLURM_NTASKS_PER_NODE=1
  fi
  SLURM_NPROCS=`expr $SLURM_JOB_NUM_NODES \* $SLURM_NTASKS_PER_NODE`
else
  if [ "x$SLURM_NTASKS_PER_NODE" = "x" ]
  then
    SLURM_NTASKS_PER_NODE=`expr $SLURM_NPROCS / $SLURM_JOB_NUM_NODES`
    REMAINDER=`expr $SLURM_NPROCS % $SLURM_JOB_NUM_NODES`
  fi
fi

srun hostname -s | sort -u > /tmp/hosts.$SLURM_JOB_ID
grep -q 'release 7\.' /etc/redhat-release
if [ $? -eq 0 ]; then
    net_suffix=-ib
fi
awk "{ print \$0\"$net_suffix slots=\" $SLURM_NTASKS_PER_NODE+(NR<=$REMAINDER); }" /tmp/hosts.$SLURM_JOB_ID >/tmp/tmp.$SLURM_JOB_ID
mv /tmp/tmp.$SLURM_JOB_ID /tmp/hosts.$SLURM_JOB_ID

mpirun -x KOKKOS_NUM_DEVICES --map-by node --bind-to core -hostfile /tmp/hosts.$SLURM_JOB_ID -np $SLURM_NPROCS $EXE -b -2 -g $MODEL -c $CASE -m $MESH -b $ATTRIBUTES -a $AMSI_OPTIONS
#mpirun -x KOKKOS_NUM_DEVICES --map-by node --bind-to core --report-bindings -hostfile /tmp/hosts.$SLURM_JOB_ID -np $SLURM_NPROCS $EXE -b -2 -g $MODEL -c $CASE -m $MESH -b $ATTRIBUTES -a $AMSI_OPTIONS

echo "Ending Job at `date`"
rm /tmp/hosts.$SLURM_JOB_ID

