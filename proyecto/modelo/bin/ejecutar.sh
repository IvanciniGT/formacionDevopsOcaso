SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $SCRIPT_DIR/env.sh

python $SCRIPT_DIR/../src/generar_modelo.py $1 $2