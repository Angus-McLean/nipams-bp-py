
#@title Fetch and Parse Data
from typing import OrderedDict
from utils.constants import *
import tempfile
from scipy.io import loadmat

FILE_PATTERN_MAT = r'.*\.mat$'
FILE_PATTERN_PICKLE = r'.*\.pickle$'

#### LOCAL DATA FILES #####
def fetch_data_from_local(folder='.',
      pattern='({FILE_PATTERN_MAT}|{FILE_PATTERN_PICKLE})',
      limit_files=10):
  # onlyfiles = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
  # matchedFiles = [file for file in onlyfiles if re.search(pattern, file)]
  
  dfFiles = pd.DataFrame(list(os.walk(folder)), columns=['path','folders','files'])
  dfFiles = dfFiles.set_index('path').files.explode().reset_index()
  dfFiles['filenames'] = dfFiles.reset_index()['path'] + '/' + dfFiles.files
  matchedFiles = dfFiles.filenames[dfFiles.filenames.str.contains(pattern)]
  
  return matchedFiles[:limit_files]


#### GOOGLE DRIVE ####
def connect_gdrive():
  from google.colab import drive
  drive.mount('/content/drive')

def fetch_data_from_gdrive(folder, pattern='*.mat$', limit_files=10):
  connect_gdrive()
  import glob

  if type(pattern)==str : pattern = [pattern]
  filenames = [glob.glob(folder+n) for n in pattern]
  filenames = [item for sublist in filenames for item in sublist]

  return filenames


#### GOOGLE CLOUD ####
def connect_gcs():
  global GLOBAL
  from google.cloud import storage

  client = storage.Client()
  bucket = client.get_bucket(os.environ['GCP_BUCKET'])

  return client, bucket

def fetch_data_from_gcs(folder='data_cleaned_LVET_m', pattern=FILE_PATTERN_MAT, dest_folder='data/raw_mat/', limit_files=10):
  client, bucket = connect_gcs()
  blobs = list(bucket.list_blobs(max_results=1000, prefix=folder))
  matchedBlobs = [blob for blob in blobs if re.search(pattern, blob.name)][:limit_files]
  
  filenames = []
  for blob in matchedBlobs:
    filename = dest_folder+blob.name.split('/')[-1]
    if not os.path.isfile(filename):
      # download file if doesn't exist
      blob.download_to_filename(filename)
    filenames.append(filename)
  
  return filenames


#### READ & PARSE .mat FILES ####
def read_mat_files(filenames, continuous=True):
  arrFilenameSubset = pd.Series(filenames).to_list()
  arrDfsImu, arrDfsBp = [], []
  for filename in arrFilenameSubset:
    # filename = 'data/raw_mat/'+blob.name.split('/')[-1]
    imuFile = loadmat(filename)

    if continuous:
      dfImu, dfBp = getContinuousDataFromMatlab(imuFile)
    else:
      dfBp = getBpDataFromMatlab(imuFile)
      dfImu = getImuDataFromMatlab(imuFile)
    
    dfBp['file'] = filename.split('/')[-1]
    dfImu['file'] = filename.split('/')[-1]
    arrDfsBp.append(dfBp)
    arrDfsImu.append(dfImu)

  dfBpAll = pd.concat(arrDfsBp).reset_index()
  dfImuAll = pd.concat(arrDfsImu).reset_index()
  return dfBpAll, dfImuAll

def getBpDataFromMatlab(dictImuData):
  bp_all = np.asarray(dictImuData['mlts_now'])
  dfBp = pd.DataFrame(bp_all, columns=BP_COLS)
  dfBp.index.name = 'heartbeat'
  return dfBp

def getImuDataFromMatlab(dictImuData):
  imu_all = np.asarray(dictImuData['mlfs_now'])
  imuShape = imu_all.shape
  imuInd = pd.MultiIndex.from_product([range(imuShape[2]), range(imuShape[0])], names=['heartbeat','step_index'])
  dfRaw = pd.concat([pd.DataFrame(imu_all[:,:,i]) for i in range(imuShape[2])]).reset_index(drop=True)
  dfRaw.columns = IMU_COLS
  dfRaw = dfRaw.set_index(imuInd).reset_index().drop('step_index', axis=1).set_index(['heartbeat','ts'])
  return dfRaw


def getContinuousDataFromMatlab(dictImuData):
  dfBpRaw = pd.concat([
    pd.DataFrame(dictImuData['bio_data'][:,[17,14,15]], columns=BP_COLS),
    pd.DataFrame(dictImuData['bio_ts']).T.rename(columns={0:'ts'}),
    pd.DataFrame(dictImuData['bio_data'][:,12], columns=['ecgTs'])
  ], axis=1)
  dfBpRaw.ts = pd.to_timedelta(dfBpRaw.ts, unit='s')

  dfImuRaw = pd.concat([
    pd.DataFrame(dictImuData['imu_data'], columns=IMU_DATA_COLS),
    pd.DataFrame(dictImuData['imu_ts']).rename(columns={0:'ts'})
  ], axis=1)
  dfImuRaw.ts = pd.to_timedelta(dfImuRaw.ts, unit='s')

  return dfImuRaw.set_index('ts'), dfBpRaw.set_index('ts')


def parseFileInfo(df, filenameCol='file'):
  ## TODO : Speed this up by taking only unique filenames, parse those, then do a join on original df
  a = df[filenameCol].str.extract(r'(sub\d+)_([A-z]+)(\d*)\.mat')
  a.columns = ['patient','test_type','test_num']
  return pd.concat([df, a], axis=1)


#### EXECUTION ####
def load_dataframe_from_mat(folder, pattern=FILE_PATTERN_MAT, limit_files=10):
  files = fetch_data_from_local(folder, pattern, limit_files=limit_files)
  dfBpAll, dfImuAll = read_mat_files(files)

  dfBpAll = parseFileInfo(dfBpAll)
  dfImuAll = parseFileInfo(dfImuAll)

  return dfBpAll, dfImuAll

def load_dataframe_from_pickle(folder, pattern=FILE_PATTERN_PICKLE):
  files = fetch_data_from_local(folder, pattern)
  arrDfs = [pd.read_pickle(f) for f in files]
  dfAll = pd.concat(arrDfs, axis=0)

  return dfAll


#### 
# def loadFiles(files):
#   arrDfsBp = []
#   arrDfsImu = []

#   for f in files:
#     imuFile = loadmat(f)
#     imuFile = loadmat(f);
#     if continuous:
#       dfImu, dfBp = getContinuousDataFromMatlab(imuFile)
#     else:
#       dfBp = getBpDataFromMatlab(imuFile)
#       dfImu = getImuDataFromMatlab(imuFile)
#     dfBp['file'] = f
#     dfImu['file'] = f
#     arrDfsBp.append(dfBp)
#     arrDfsImu.append(dfImu)

#   dfImuAll = pd.concat(arrDfsImu).reset_index().set_index(['file','heartbeat','ts'])
#   dfBpAll = pd.concat(arrDfsBp).reset_index().set_index(['file','heartbeat'])
#   return dfImuAll, dfBpAll

# def loadFilePath(filepath=None):
#   filenames = glob.glob(filepath)
#   # print('Found', len(filenames), 'Data Files')

#   arrFilenameSubset = pd.Series(filenames).to_list()
#   dfImuAll, dfBpAll = loadFiles(arrFilenameSubset)
  
#   return dfImuAll.astype('float16'), dfBpAll