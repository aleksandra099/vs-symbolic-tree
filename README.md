# vs-symbolic-tree

- python version: 3.5.2
- install requirements with: pip install -r requirements.txt

- Procedure for running the program is as follows:
  - build llvm code with: myclang -I {path_to_klee_include} -emit-llvm -c -g {name_of_the_file}.c
  - when you execute the above line, you should get {name_of_the_file}.bc file
  - build with klee tool: myklee --write-sym-paths --write-pcs {name_of_the_file}.bc
  - once you run the command above, you should get folers klee-out-{nubmer} and klee-last which is a symlink to klee-out-{number}
  - run the python sym_tree.py
