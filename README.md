# iggyngs
# -------

# Load python module

source new-modules.sh
module load python

# Conda environment

# To install

conda create -n IGGYNGS --clone="$PYTHON_HOME"

# To activate

source activate IGGYNGS
prepending /n/home_rc/mclamp/envs/IGGYNGS/bin to PATH

# This is for illuminate

pip install xmltodict
pip install bitstring

conda remove dateutil
conda install dateutil
conda remove pytz
conda install docopt

pip install pandas --upgrade

# Path to source
export PYTHONPATH=`pwd`/src:`pwd`/src/external:$PYTHONPATH
