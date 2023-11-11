# Shorter version of python readme

## requirements
- cmake >= 3.16 (`python -m pip install cmake`)
- libboost >= 1.49.0 (`sudo apt install libboost-all-dev` or `brew install boost`)
- python3 and pybind11 (`conda create -n <env name> python=3.10` and `python -m pip install "pybind11[global]"`)

Ubuntu:
```bash
sudo apt-get update
sudo apt-get install build-essential libboost-all-dev python3-dev python3-pybind11 
./compile.sh
python -m pip install -e .
```

## build / compile
to compile the cpp code, stay in the **root directory** of the folder and run the following commands:
```bash
mkdir build
cmake -B build ./ -DCMAKE_BUILD_TYPE=Release -DPYTHON=true
make -C build -j
./build/lifelong --inputFile <the_input_file_name> -o <output_file_location>
```
_Note:_
1. remember to set `-DPYTHON=true` to use the python code for real
2. the input file name is the relative path to the json file that contains the problem description
3. remember to recompile the code after changing the python file
4. remember to run `python -m pip install -e .` after the first time you compile the code
5. for making the breakpoints in the python files, use `pdb.set_trace()`, don't use `breakpoint()`, remember to recompile 

people sometimes prefer oneliner during debugging and testing:
```bash
rm -r build; mkdir build; cmake -B build ./ -DCMAKE_BUILD_TYPE=Release -DPYTHON=true; make -C build -j; ./build/lifelong --inputFile ./example_problems/random.domain/random_20.json -o test.json     
```
