SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $SCRIPT_DIR/env.sh

python $SCRIPT_DIR/../test/modelo_test.py $1 $2
python $SCRIPT_DIR/../test/exportar_modelo_test.py $1 $2