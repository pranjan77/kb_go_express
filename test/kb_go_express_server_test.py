# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_go_express.kb_go_expressImpl import kb_go_express
from kb_go_express.kb_go_expressServer import MethodContext
from kb_go_express.authclient import KBaseAuth as _KBaseAuth

from ExpressionUtils.ExpressionUtilsClient import ExpressionUtils
from KBaseFeatureValues.KBaseFeatureValuesClient import KBaseFeatureValues

from DataFileUtil.DataFileUtilClient import DataFileUtil


class kb_go_expressTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_go_express'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_go_express',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_go_express(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_go_express_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #exp_util=ExpressionUtils(os.environ['SDK_CALLBACK_URL'])
        #expressionparams = {
        #'expressionset_ref':'6878/391/8',
        #'workspace_name': 'pranjan77:narrative_1501696934297',
        #'output_obj_name': 'testout'
        #}

        #y = exp_util.get_expressionMatrix(expressionparams)
        #fpkm=y['exprMatrix_FPKM_ref']
        #print fpkm

        #DownloadExpressionParams = {
        #    'source_ref': '6878/391/8'
        #}

        #y = exp_util.download_expression(DownloadExpressionParams)
        #print y

        expression_object = '6878/413/15'

        df = DataFileUtil(os.environ['SDK_CALLBACK_URL'])

        expression_matrix_data = df.get_objects({'object_refs':
                                                  [expression_object]})['data'][0]['data']
        #print expression_matrix_data

        expression_matrix_TSV = []
        col_ids = expression_matrix_data['data']['col_ids']
        ids =  "\t". join ([str(x) for x in col_ids])
        print ids
        expression_matrix_TSV.append(" " + "\t" + ids + "\n")

        feature_list = expression_matrix_data['data']['row_ids']
        values = expression_matrix_data['data']['values']

        for feature, value in zip (feature_list, values):
            row_value =  "\t".join(map(str, value)) 
            expression_matrix_TSV.append (feature + "\t" + row_value + "\n")


        textstring_TSV = "".join (expression_matrix_TSV)
        file = open('/kb/module/work/testfile2.txt','w')  
        file.write(textstring_TSV)
        file.close()









        #exportmatrix_params ={
        #'ws_matrix_id' :fpkm
        #}



        #fv = KBaseFeatureValues (os.environ['SDK_CALLBACK_URL'])
        #exp_matrix = fv.export_matrix(exportmatrix_params)
        #print exp_matrix


        #tsv_params = {
        #'ws_matrix_id' : fpkm,
        #'to_shock': 1,
        #'file_path':'/kb/module/work/tmp/out.txt'
        #}

        #y = fv.matrix_to_tsv_file(tsv_params)
        #print y



        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass
