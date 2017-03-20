# HOW TO USE THIS
1. `git clone https://github.com/rmarren1/auto_bench`
2. Check if your machine has `boto` python library.
  * If not, `pip install boto`
  * OR if you are on machine without install ability (cortex, ugrad), do `git clone https://github.com/boto/boto` then copy the `boto/boto` directory into the `auto_bench` directory (you can delete the cloned `boto` if you want)
3. edit the `auto_bench/_set_keys.py` file. follow the instructions
4. now you can run `python auto_bench/get_fpci_data.py directory/ start end` to get files `start` through `end` and put them into the `directory` folder (or create one). note the slash is important in this command.
