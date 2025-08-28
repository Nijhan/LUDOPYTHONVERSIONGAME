import sys,os
#from rich.console import Console

#console=Console()

#pwd file
print(__file__)
current_path=os.path.dirname(__file__)

print(current_path)

newPath=os.path.join(current_path,"../..")

print(newPath)

calculated_abs_path=os.path.abspath(newPath)

print(calculated_abs_path)