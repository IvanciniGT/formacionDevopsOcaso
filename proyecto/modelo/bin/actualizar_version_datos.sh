SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# TODOS: 
## Validar que me estén pasando una versión... y que sea válida
## Validar que se esté ubicado en la rama develop para poder hacer este trabajo
[[ $(git branch | grep -c "* develop") == 1 ]] && echo "Procediendo a actualizar los datos" || echo "Los datos solo pueden actualizarse desde la rama develop" && exit 1

git -C $SCRIPT_DIR/../datos fetch
git -C $SCRIPT_DIR/../datos checkout $1
git -C $SCRIPT_DIR/.. add datos

