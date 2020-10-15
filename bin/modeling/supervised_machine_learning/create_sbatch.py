""" Author: Monte Lunacek
    Purpose: Create several *.sbatch files for running parameter searches on Eagle.
"""
import jinja2 as jin
import shutil
import os
import glob

# This is the main sbatch template
template = jin.Template("""#!/bin/bash
#SBATCH --ntasks=36           # CPU cores requested for job
#SBATCH --nodes=1             # Keeep all cores on the same node
#SBATCH --time=4:00:00        # Job should run for up to 2 hours (for example)
#SBATCH --account=athena

cd $HOME/athena/ATHENA-twin/
source eagle.sh
cd bin/modeling/supervised_machine_learning

# create the base scenario
{% for i in work %}
{{i}}
{% endfor %}
""")

workload = {
    "C": ["python supervised_machine_learning.py --split group --group obs --nsplits 5 --features C",
          "python supervised_machine_learning.py --split group --group day --nsplits 5 --features C",
          "python supervised_machine_learning.py --split group --group week --nsplits 5 --features C"],

    "CP": ["python supervised_machine_learning.py --split group --group obs --nsplits 5 --features CP",
          "python supervised_machine_learning.py --split group --group day --nsplits 5 --features CP",
          "python supervised_machine_learning.py --split group --group week --nsplits 5 --features CP"],

    "CPW": ["python supervised_machine_learning.py --split group --group obs --nsplits 5 --features CPW",
            "python supervised_machine_learning.py --split group --group day --nsplits 5 --features CPW",
            "python supervised_machine_learning.py --split group --group week --nsplits 5 --features CPW"],

    "CPWF_obs": ["python supervised_machine_learning.py --split group --group obs --nsplits 5 --features CPWF"],
    "CPWF_day": ["python supervised_machine_learning.py --split group --group day --nsplits 5 --features CPWF"],
    "CPWF_week": ["python supervised_machine_learning.py --split group --group week --nsplits 5 --features CPWF"],

    "CPWFT_obs": ["python supervised_machine_learning.py --split group --group obs --nsplits 5 --features CPWFT"],
    "CPWFT_day": ["python supervised_machine_learning.py --split group --group day --nsplits 5 --features CPWFT"],
    "CPWFT_week": ["python supervised_machine_learning.py --split group --group week --nsplits 5 --features CPWFT"],
}

if __name__ == "__main__":

    # remove old sbatch files
    for x in glob.glob("*_sbatch.sh"):
        os.remove(x)

    # remove old slurm files
    for x in glob.glob("slurm-*.out"):
        os.remove(x)

    # create new jobs
    filenames = []
    for k,v in workload.items():
        filename = "{}_sbatch.sh".format(k)
        with open(filename, "w") as outfile:
            outfile.write(template.render(work=v))
        filenames.append(filename)

    # create submit script
    with open("submit.sh", 'w') as outfile:
        for filename in filenames:
            outfile.write("sbatch {}\n".format(filename))

