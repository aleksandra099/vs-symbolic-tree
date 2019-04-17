# vs-symbolic-tree

- python version: 3.5.2
- install requirements with: pip install -r requirements.txt

- Procedure for running the program is as follows:
  - build llvm code with: myclang -I {path_to_klee_include} -emit-llvm -c -g {name_of_the_file}.c
  - when you execute the above line, you should get {name_of_the_file}.bc file
  - build with klee tool: myklee --write-sym-paths --write-pcs {name_of_the_file}.bc
  - once you run the command above, you should get folers klee-out-{nubmer} and klee-last which is a symlink to klee-out-{number}
  - run the python sym_tree.py


- Procedure for running the program is as follows (NEW):
  - make makeTree.sh and sym_tree.py executable by running "chmod +x && chmod +x makeTree.sh"
  - run makeTree.sh with "./makeTree.sh {absolute_path_to_c_file} {absolute_path_to_where_you_want_your_sym_tree_image}"
    e.g. "./makeTree.sh ~/Downloads/07_materijali/pointer_error_sym.c ~/Downloads/drvo" => this will make drvo.pdf and drvo.gv
    or simply run "./makeTree.sh -h" to see the usage
