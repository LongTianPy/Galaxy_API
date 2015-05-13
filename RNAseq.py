 #! /usr/bin/python
"""This script uses Galaxy API 'bioblend' to access galaxy instance with url and account info or API key. It aims to realize performing data analysis by visiting workflow stored in galaxy instance from command line."""
"""Despite of this, it still needs galaxy server running."""

###IMPORT###
from bioblend import galaxy
import optparse
import uuid




###FUNCTION###
def connect_to_galaxy():
	"""
		Connect to galaxy instance by options of url, email, password, API key.
		Note that if user has typed API key, email and password are not required.
		And if no API input, email and password should be indicated.
		"""

    GI = galaxy.GalaxyInstance(url="localhost:8080",key="2b55a6c05d88b92aff00b3a58c8cc409")

	try:
		GI.histories.get_histories()
		return GI
	except:
		print "Please make sure Galaxy is running."
def run_workflow(GI):
    history = GI.histories.create_history(str(uuid.uuid4()))
    workflow = GI.workflows.show_workflow('f2db41e1fa331b3e')
    library = GI.libraries.create_library(str(uuid.uuid4()))
    upload_lib = GI.libraries.upload_file_from_server(library['id'],server_dir='.') # No subfolders in library_import
    
    inputs={}
    for i in upload_lib:
        if i['name'][-2:] == 'fa':
            reference_genome_id = i['id']
        elif i['name'][-3:] == 'gtf':
            reference_annotation_id = i['id']
        else:
            inputs[i['name']]=i['id']
    inputnames = inputs.keys()
    inputnames = sorted(inputnames)
    datamap = {'127':{'src':'ld','id':inputs[inputnames[0]]},
              '128':{'src':'ld','id':inputs[inputnames[1]]},
              '129':{'src':'ld','id':inputs[inputnames[2]]},
              '130':{'src':'ld','id':inputs[inputnames[3]]},
              '132':{'src':'ld','id':reference_annotation_id},
              '131':{'src':'ld','id':reference_genome_id}
              }

    output = GI.workflows.run_workflow(workflow_id='f2db41e1fa331b3e',dataset_map=datamap,history_id=history['id'])
    for i in output['outputs']:
        GI.datasets.download_dataset(i,file_path='/home/outputs')


###MAIN###
if __name__ == '__main__':

    GI = connect_to_galaxy(url,email,password,API_key)
    run_workflow(GI)



