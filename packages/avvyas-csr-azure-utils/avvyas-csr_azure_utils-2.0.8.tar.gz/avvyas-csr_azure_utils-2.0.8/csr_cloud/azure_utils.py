from __future__ import absolute_import

from csr_cloud.file_utils import StorageFileUtils
from csr_cloud.meta_utils import MetaDataUtils

# For future use if we enable TVNET/Autoscaler
# from csr_cloud.general_utils import GeneralUtils
# class AzureUtils(StorageFileUtils, MetaDataUtils, GeneralUtils):

class AzureUtils(StorageFileUtils, MetaDataUtils):
    def __init__(self, account_name, account_key, cloudname, feature):
        StorageFileUtils.__init__(self, account_name, account_key, cloudname, feature)
        MetaDataUtils.__init__(self, feature)
        
        # For future use if we enable TVNET/Autoscaler
        # GeneralUtils.__init__(self)

