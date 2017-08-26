import time
import json
import glob
import os
import uuid
import errno
import subprocess
import zipfile
import shutil
import csv
import numpy
import fileinput
import re

from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport
from GenomeSearchUtil.GenomeSearchUtilClient import GenomeSearchUtil
#from biokbase.workspace.client import Workspace as Workspace
from Workspace.WorkspaceClient import Workspace as Workspace


#from biokbase.workspace.client import Workspace


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))



class GOExpressUtil:

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _parse_csv_to_json (self, csv_path, outjson):

        df = dict()
        df['data'] = list()
        df['categories'] = list()
        df['conditions'] = list()

        with open(csv_path, 'rb') as resultfile:
            next (resultfile)
            result = csv.reader(resultfile, delimiter=',')
            for row in result:
             image_path = os.path.basename(row[11].rstrip())

             row_details = {'go_id':row[1],
                'ave_rank': row[2],
                'ave_score': row[3],
                'total_count':row[4],
                'data_count': row[5],
                'p_val': row[6],
                'name_1006': row[7],
                'namespace_1003': row[8],
                'condition1': row[9],
                'condition2': row[10],
                'pathTOHMAP': "images" + "/" + image_path
            }

             df['data'].append(row_details)

             df['categories'].append(row[8])
             df['conditions'].append(row[9])
             df['conditions'].append(row[10])

        unique_categories = list(set(df['categories']))
        unique_conditions = list(set(df['conditions']))

        df['categories'] = unique_categories
        df['conditions'] = unique_conditions


        outfile = open (outjson, "w")

        outfile.write(json.dumps(df))
        outfile.close()

        return outjson




    def _expression_object_to_tsv(self, expression_object, expression_matrix_TSV_path):
    

                log ('Starting get_expression_matrix')
       
                expression_matrix_data = self.dfu.get_objects({'object_refs':
                                                  [expression_object]})['data'][0]['data']
                #print expression_matrix_data

                expression_matrix_TSV = []
                col_ids = expression_matrix_data['data']['col_ids']
                ids =  "\t". join ([str(x) for x in col_ids])
                
                expression_matrix_TSV.append(" " + "\t" + ids + "\n")

                feature_list = expression_matrix_data['data']['row_ids']
                values = expression_matrix_data['data']['values']

                for feature, value in zip (feature_list, values):
                    row_value =  "\t".join(map(str, value)) 
                    expression_matrix_TSV.append (feature + "\t" + row_value + "\n")


                textstring_TSV = "".join (expression_matrix_TSV)
                #TODO put some try and catch here
                file = open(expression_matrix_TSV_path,'w')  
                file.write(textstring_TSV)
                file.close()

                return expression_matrix_TSV_path



    def _get_go_maps_from_genome(self, genome_ref):
        
        log('start parsing GO terms from genome')

        feature_num = self.gsu.search({'ref': genome_ref})['num_found']

        genome_features = self.gsu.search({'ref': genome_ref,
                                               'limit': feature_num,
                                               'sort_by': [['feature_id', True]]})['features']



        feature_id_go_id_list_map = {}
        go_id_feature_id_list_map = {}
        go_id_go_term_map = {}
        feature_id_feature_info_map = {}

        for genome_feature in genome_features:
                feature_id = genome_feature.get('feature_id')
                feature_func = genome_feature.get('function')
                feature_type = genome_feature.get('feature_type')
                ontology_terms = genome_feature.get('ontology_terms')
                #print "ontology"
                #print ontology_terms

                #print ('{}\t{}\t{}'.format(feature_id, feature_func , feature_type))



                #feature_id_feature_info_map.update({feature_id: {'function': feature_func,
                 #                                                'feature_type': feature_type}})

                go_id_list = []
                if ontology_terms:
                    for ontology_id, ontology_term in ontology_terms.iteritems():
                        if re.match('[gG][oO]\:.*', ontology_id):
                            go_id_go_term_map.update({ontology_id: ontology_term})
                            go_id_list.append(ontology_id)

                if go_id_list:
                    feature_id_go_id_list_map.update({feature_id: go_id_list})

                    for go_id in go_id_list:
                        if go_id in go_id_feature_id_list_map:
                            feature_ids = go_id_feature_id_list_map.get(go_id)
                            feature_ids.append(feature_id)
                            go_id_feature_id_list_map.update({go_id: feature_ids})
                        else:
                            go_id_feature_id_list_map.update({go_id: [feature_id]})
                else:
                    if not re.match('.*\.\d*', feature_id):
                        feature_id_go_id_list_map.update({feature_id: 'Unlabeled'})
        return (feature_id_go_id_list_map, go_id_feature_id_list_map,
                go_id_go_term_map, genome_features)




    def _get_ontology_hash(self):
        ontology_hash = dict()
        ontologies = self.ws.get_objects([{'workspace': 'KBaseOntology',
                                           'name': 'gene_ontology'},
                                          {'workspace': 'KBaseOntology',
                                           'name': 'plant_ontology'}])
        ontology_hash.update(ontologies[0]['data']['term_hash'])
        ontology_hash.update(ontologies[1]['data']['term_hash'])

        return ontology_hash

    def _generate_supporting_files(self, result_directory,  
                                   feature_id_go_id_list_map, genome_ref,
                                    genome_features, ontology_hash, params):
                 
        supporting_files = list()

        feature_id_go_ids_map_file = os.path.join(result_directory, 'feature_id_go_ids_map.txt')
        go_id_description_file = os.path.join(result_directory, 'go_id_description.txt')
        feature_ids_file = os.path.join(result_directory, 'feature_ids_description.txt')
        genome_info_file = os.path.join(result_directory, 'genome_info.txt')
        expression_matrix_file = os.path.join(result_directory, 'expression_matrix.txt')
        condition_sample_relationship_file = os.path.join(result_directory, 'condition_sample_relationship.txt')


        file_list = {
            "feature_id_go_ids_map_file": feature_id_go_ids_map_file,
            "go_id_description_file" :go_id_description_file,
            "feature_ids_file": feature_ids_file,
            "genome_info_file": genome_info_file,
            "expression_matrix_file" : expression_matrix_file,
            "condition_sample_relationship_file" : condition_sample_relationship_file
        }
       

        supporting_files.append(feature_id_go_ids_map_file)
        supporting_files.append(go_id_description_file)
        supporting_files.append(feature_ids_file)
        supporting_files.append(genome_info_file)
        supporting_files.append(expression_matrix_file)
        supporting_files.append(condition_sample_relationship_file)

       
        total_feature_ids = feature_id_go_id_list_map.keys()
        feature_ids_with_feature = []
        for feature_id, go_ids in feature_id_go_id_list_map.iteritems():
            if isinstance(go_ids, list):
                    feature_ids_with_feature.append(feature_id)
        genome_name = self.ws.get_object_info3({'objects': 
                                                    [{'ref': genome_ref}]})['infos'][0][1]

        #print genome_info_file
        with open(genome_info_file, 'wb') as genome_info_file:
                genome_info_file.write('genome_name: {}\n'.format(genome_name))
                genome_info_file.write('features: {}\n'.format(len(total_feature_ids)))
                genome_info_file.write('features with term: {}'.format(len(feature_ids_with_feature)))

        seen_go_id = dict()
       
        with open(feature_id_go_ids_map_file, 'wb') as feature_id_go_ids_map_file:
            with open(go_id_description_file, 'wb') as go_id_description_file:

                feature_id_go_ids_map_file.write('{}\t{}\n'.format("gene_id", "go_id"))
                go_id_description_file.write('{}\t{}\t{}\n'.format("go_id","name_1006", "namespace_1003")) 
                                                                        
                for feature_id, go_ids in feature_id_go_id_list_map.iteritems():
                    if isinstance(go_ids, str):
                        feature_id_go_ids_map_file.write('{}\t{}\n'.format(feature_id, 
                                                                            go_ids))
                        ontology_name = ontology_hash.get(go_ids).get('name')
                        ontology_namespace = ontology_hash.get(go_ids).get('namespace')
                        if not go_ids in seen_go_id:
                            seen_go_id[go_ids] = 1
                            
                            go_id_description_file.write('{}\t{}\t{}\n'.format(go_ids, 
                                                                        ontology_name, 
                                                                        ontology_namespace))
                    else:
                        for go_id in go_ids: 
                            feature_id_go_ids_map_file.write('{}\t{}\n'.format(feature_id, 
                                                                                go_id))
                            ontology_name = ontology_hash.get(go_id).get('name')
                            ontology_namespace = ontology_hash.get(go_id).get('namespace')
                            if not go_id in seen_go_id:
                                seen_go_id[go_id] = 1
                                go_id_description_file.write('{}\t{}\t{}\n'.format(go_id, 
                                                                        ontology_name, 
                                                                        ontology_namespace))

                        

        with open(feature_ids_file, 'wb') as feature_ids_file:
            feature_ids_file.write('{}\t{}\t{}\n'.format("gene_id", "external_gene_name" , "description"))

            for genome_feature in genome_features:
                feature_id = genome_feature.get('feature_id')
                feature_func = genome_feature.get('function')
                feature_type = genome_feature.get('feature_type')
                ontology_terms = genome_feature.get('ontology_terms')

                if ontology_terms:
                    #feature_func1 = feature_func.decode('string_escape')
                    #feature_func1.replace("'", r".")
                    external_gene_name = feature_id + ":" + feature_func
                    external_gene_name = external_gene_name[:50]

                    external_gene_name = '"' + external_gene_name + '"'


                    feature_func1 = '"' + feature_func + '"'
                    feature_ids_file.write('{}\t{}\t{}\n'.format(feature_id, external_gene_name, feature_func1))

        expression_matrix_file = self._expression_object_to_tsv(params['expression_ref'],
                                                                expression_matrix_file)  
                                                                
        #condition_sample_relationship_file = self._write_condition_sample_relationship(params['sample_n_conditions'])          

        sample_n_conditions = params['sample_n_conditions']

        with open(condition_sample_relationship_file, 'wb') as condition_sample_relationship_file:
          for conditions in sample_n_conditions:
             condition_sample_relationship_file.write ('{}:{}\n'.format(conditions['condition'],
                                                                ",".join(conditions['sample_id'])))

        result_file = os.path.join(result_directory, 'supporting_files.zip')
        with zipfile.ZipFile(result_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
            for supporting_file in supporting_files:
                 zip_file.write(supporting_file, 
                               os.path.basename(supporting_file))

        return [{'path': result_file,
                'name': os.path.basename(result_file),
                'label': os.path.basename(result_file),
                'description': 'GOexpress supporting files',
                'file_list': file_list
                }]



    def _run_command(self, command):
        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed commend:\n{}\n'.format(command) +
            'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
            return exitCode
        else:
            error_msg = 'Error running commend:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)
            return 'error'

    def _run_goexpress_command(self, result_directory, 
                                        supporting_files, params):
        params['num_permutations'] = 1000
        r = supporting_files[0]['file_list']
        result_files = os.listdir(result_directory)
        rcmd_list = ['Rscript', os.path.join(os.path.dirname(__file__), 'GOExpress.R')]
        rcmd_list.extend(['--outDir', result_directory])
        rcmd_list.extend(['--expMatrix', r['expression_matrix_file'] ])
        rcmd_list.extend(['--gi2go', r['feature_id_go_ids_map_file'] ])
        rcmd_list.extend(['--geneDes', r['feature_ids_file'] ])
        rcmd_list.extend(['--goDes', r['go_id_description_file'] ])
        rcmd_list.extend(['--cond', r['condition_sample_relationship_file'] ])
        rcmd_list.extend(['--Nper', params['num_permutations'] ])

        rcmd_str = " ".join(str(x) for x in rcmd_list)

        print rcmd_str

#        print rcmd_str
        self._run_command(rcmd_str)


    def _generate_report_from_dir(self, output_html_files, supporting_files, params):
        
        objects_created = []

        report_params = {'message': '',
                         'workspace_name': params.get('workspace_name'),
                         'objects_created': objects_created,
                         'file_links': supporting_files,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                        'report_object_name': 'kb_goexpress_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)
        report_output = {'report_name': output['name'], 'report_ref': output['ref']}
        return report_output




    def _generate_goexpress_report (self, result_directory, params):

         #create report directory and image sub directory
        report_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(report_directory)
        report_image_directory = os.path.join(report_directory, "images")
        self._mkdir_p(report_image_directory)
        #copy all images to report directory
        for pngfile in glob.iglob(os.path.join(result_directory, "*.png")):
            shutil.copy(pngfile, report_image_directory)

        html_template = os.path.join(os.path.dirname(__file__), "report.html")
        shutil.copy(html_template, report_directory)

        script_file = os.path.join(os.path.dirname(__file__), "script.js")
        shutil.copy(script_file, report_directory)

        csv_path =  os.path.join(result_directory, "AllCombined.csv")
        json_path = os.path.join(result_directory, "out.json")
        
        json_path = self._parse_csv_to_json (csv_path, json_path)
        shutil.copy(json_path, report_directory)
        shutil.copy(csv_path, report_directory)

        report_shock_id = self.dfu.file_to_shock({'file_path': report_directory,
                                                'pack': 'zip'})['shock_id']

        html_report = list()

        report_file_path = os.path.join(report_directory, 'report.html')

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(report_file_path),
                            'label': os.path.basename(report_file_path),
                            'description': 'HTML summary report for GOExpress App'})
        return html_report
        




    def __init__(self, config):
            self.ws_url = config["workspace-url"]
            self.callback_url = config['SDK_CALLBACK_URL']
            self.token = config['KB_AUTH_TOKEN']
            self.shock_url = config['shock-url']
            self.dfu = DataFileUtil(self.callback_url)
            self.gsu = GenomeSearchUtil(self.callback_url)
            self.ws = Workspace(self.ws_url, token=self.token)
            self.scratch = config['scratch']


    def run_goexpress_app(self, params):

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)


        (feature_id_go_id_list_map, 
             go_id_feature_id_list_map,
             go_id_go_term_map, 
             genome_features) = self._get_go_maps_from_genome(params['genome_ref'])

        
        ontology_hash = self._get_ontology_hash()

        
        supporting_files = self._generate_supporting_files(result_directory, 
                                                feature_id_go_id_list_map, 
                                                params['genome_ref'],
                                                genome_features, ontology_hash, params)

        exitcode = self._run_goexpress_command(result_directory, 
                                        supporting_files, params)

        print exitcode

        
        output_html_files = self._generate_goexpress_report (result_directory, params)
        print output_html_files

        outx =  self._generate_report_from_dir(output_html_files, supporting_files, params)
        print outx
        


