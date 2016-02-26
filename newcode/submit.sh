#!/bin/bash
#$ -cwd
#$ -l h_vmem=8G
#$ -q medium
#$ -o /home/usuaris/pranava/acl2016/shorts/ppattach/newcode/qsublogs
#$ -e /home/usuaris/pranava/acl2016/shorts/ppattach/newcode/qsublogs 
#$ -V 

maxiter=${1}
tau=${2}
eta=${3}
prep=${4}

python -u /home/usuaris/pranava/acl2016/shorts/ppattach/newcode/logisticReg.py ${maxiter} ${cfile} ${tau} ${eta} ${prep} 

