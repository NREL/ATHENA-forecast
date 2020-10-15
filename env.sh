source activate athena-twin

export ATHENA_DATA_PATH=`pwd`/.data
mkdir -p $ATHENA_DATA_PATH
export ATHENA_CREDENTIALS_PATH=$HOME/.athena
mkdir -p $ATHENA_CREDENTIALS_PATH


