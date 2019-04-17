#/!bin/bash

function usage {
	echo -e "\nUsage: $0 [absoulte_path_to_c_file] [absoulte_path_to_save_image]"
}


if [ $# -le 1 ]
then
	usage
	exit 1
fi

if [[ ($# == "--help") || $# == "-h" ]]
then
	usage
	exit 0
fi

myclang="~/build/llvm/Release/bin/clang"
myklee="~/build/klee/Release+Asserts/bin/klee"
picture_path="$2"
sym_tree_path="$(pwd)/sym_tree.py"
tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
cd $tmp_dir

full_filename=$(basename -- "$1")
filename="${full_filename%.*}"

myclang_command="$myclang -I ~/build/klee/include/ -emit-llvm -c -g $1"
myklee_command="$myklee --write-sym-paths --write-pcs $tmp_dir/$filename.bc"

eval "$myclang_command" && eval "$myklee_command" && eval "python3 $sym_tree_path -d 10 -o $picture_path"

rm -rf $tmp_dir
