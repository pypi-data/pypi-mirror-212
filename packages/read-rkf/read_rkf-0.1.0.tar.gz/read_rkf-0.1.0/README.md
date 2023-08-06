# A script to read the ams.rkf file which contains all the important data from an ams output file. This file generally contains 
# 1 Trajectories
# 2 Gradients 
# 3 Hessians 
# 4 Energies 
# 5 Band gaps and structures
# and so on 

# How to
# 1 Convert rkf file to a json object 
from read_rkf.creat_archive import rkf_to_json 
json_data = rkf_to_json(path_to_the_rkf_file)

# 2 Convert rkf file to a python dictionary 
from read_rkf.creat_archive import rkf_to_dict 
python_dict  = rkf_to_dict(path_to_the_rkf_file)

# 3 check the sections in the rkf file 
from read_rkf.parserkf import KFFile
data = KFFile(path_to_the_rkf_file)
all_sections = data.sections()
# e.g if you want a the first section?
section_content =  data.read_section(all_sections[0])
