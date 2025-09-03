from setuptools import find_packages, setup
from typing import List



var = "-e ."

def get_requirements(file_path:str)->List[str]:              # return type hint - list where each element is a string
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        #requirements = [req.replace("\n", "") for req in requirements]
        requirements = [req.strip() for req in requirements]
        
        if var in requirements:
            requirements.remove(var)
            
    return requirements


setup( name = 'Data-Science-Salary-Project', 
       version = '0.0.1', 
       author = 'Dhanush Raj',
       author_email = 'dhanushlogan1004@gmail.com', 
       packages = find_packages(), 
       install_requires = get_requirements('requirements.txt')  )