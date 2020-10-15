#!/usr/bin/env python
# coding: utf-8

# In[48]:


import athena
import json
import glob
import jinja2 as jin

def save_config(config, number):
    with open("config/config_{0:03d}.json".format(number), "w") as outfile:
        outfile.write(json.dumps(config))
    return number+1
    
def create_obs_day_week(config, count):
    config['forecast'] = 1
    count = save_config(config, count)

    config['forecast'] = 48
    count = save_config(config, count)

    config['forecast'] = 7*48
    count = save_config(config, count)
    return count
    
config = json.loads(open("config/base.json").read())
config['epochs'] = 100

count = 1

db = athena.database.AthenaDatabase(cache=True, write=True)
df = db.summary_table() 
y_cols = athena.learning.add_features(df, forecast=1)
df.columns


# In[49]:


config['look_forward'] = 0
config['look_back'] = 60
config['num_cols'] =  ['vehicles', 'passengers']
config['cat_cols'] = ['time', 'day', 'month']
config['no_trans_cols'] = []
count = create_obs_day_week(config, count)


# In[50]:


config['look_forward'] = 0
config['look_back'] = 60
config['num_cols'] =  ['vehicles', 'passengers']
config['cat_cols'] = []
config['no_trans_cols'] = ['time_minutes_sin', 'time_minutes_cos', 'day_sin', 'day_cos', 'month_sin', 'month_cos']
count = create_obs_day_week(config, count)


# In[51]:


config['look_forward'] = 60
config['look_back'] = 10
config['num_cols'] =  ['passengers']
config['cat_cols'] = ['time', 'day', 'month']
config['no_trans_cols'] = []
count = create_obs_day_week(config, count)


# In[52]:


config['look_forward'] = 60
config['look_back'] = 10
config['num_cols'] =  ['passengers']
config['cat_cols'] = []
config['no_trans_cols'] = ['time_minutes_sin', 'time_minutes_cos', 'day_sin', 'day_cos', 'month_sin', 'month_cos']
count = create_obs_day_week(config, count)


# In[58]:


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
python lstm_single.py {{i}}
{% endfor %}
""")


filenames = glob.glob("config/config_0*")
with open("sbatch.sh", "w") as outfile:
    outfile.write(template.render({'work': filenames }))
    


# In[ ]:




