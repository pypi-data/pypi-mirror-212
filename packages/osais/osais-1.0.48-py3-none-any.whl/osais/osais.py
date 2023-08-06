
__version__="1.0.48"

## ========================================================================
## 
##                      Utilities starts here 
## 
## ========================================================================

## ------------------------------------------------------------------------
#       OSAIS python Tools (used by libOSAISVirtualAI.py)
## ------------------------------------------------------------------------

import uuid 
import subprocess as sp
import pkg_resources
import os
import platform
import ctypes
import threading
import boto3
import asyncio

cuda=0                          ## from cuda import cuda, nvrtc
gObserver=None

## ------------------------------------------------------------------------
#       Observer (check updates in directory)
## ------------------------------------------------------------------------

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, fnOnFileCreated, _args):
        self.fnOnFileCreated = fnOnFileCreated
        self._args = _args

    def on_created(self, event):

        if event.is_directory:
            return
        if event.event_type == 'created':
            ## only notify if uid in the filename (otherwise we are getting notified of another AI's job !)
            if self._args["-uid"] in event.src_path:
                self.fnOnFileCreated(os.path.dirname(event.src_path)+"/", os.path.basename(event.src_path), self._args)

def start_observer_thread(path, fnOnFileCreated, _args):

    ## watch directory and call back if file was created
    def watch_directory(path, fnOnFileCreated, _args):    

        print ("=> starting a watch on path: "+path+"\r\n")
        global gObserver
        if gObserver!=None:
            gObserver.stop()
        event_handler = NewFileHandler(fnOnFileCreated, _args)
        gObserver = Observer()
        gObserver.schedule(event_handler, path, recursive=False)
        gObserver.start()
        gObserver.join(1)

    thread = threading.Thread(target=watch_directory, args=(path, fnOnFileCreated, _args))
    thread.start()
    return watch_directory

def start_notification_thread(fnOnNotify):
    def _run(_fn):
        _fn()
    thread = threading.Thread(target=_run, args=(fnOnNotify))
    thread.start()
    return _run

async def wait_250ms():
  await asyncio.sleep(0.250)

## ------------------------------------------------------------------------
#       Directory utils
## ------------------------------------------------------------------------

## list content of a directory
def listDirContent(_dir):
    from os.path import isfile, join
    onlyfiles = [f for f in os.listdir(_dir)]
    ret="Found "+str (len(onlyfiles)) + " files in path "+_dir+"<br><br>";
    for x in onlyfiles:
        if isfile(join(_dir, x)):
            ret = ret+x+"<br>"
        else:
            ret = ret+"./"+x+"<br>"

    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string+"<br>"+ret

def clearOldFiles(_dir):  
    from datetime import timedelta
    from datetime import datetime
    _now=datetime.now()
    cutoff_time = _now - timedelta(minutes=10)
    for filename in os.listdir(_dir):
        file_path = os.path.join(_dir, filename)
        modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        if modification_time < cutoff_time:
            os.remove(file_path)
            
## ------------------------------------------------------------------------
#       System utils
## ------------------------------------------------------------------------

def consoleLog(err): 
    msg=""
    try: 
        if err["msg"]:
            msg=err["msg"]
    except: 
        try: 
            if err.msg:
                msg=err.msg
        except: 
            try:
                if err.args and err.args[0]:
                    msg=err.args[0]         
            except: 
                msg="???"
    print("CRITICAL: "+msg)

## get a meaningful name for our machine
def get_machine_name() :
    _machine=str (hex(uuid.getnode()))
    _isDocker=is_running_in_docker()
    if _isDocker:
        _machine = os.environ.get('HOSTNAME') or os.popen('hostname').read().strip()
    return _machine

## which OS are we running on?
def get_os_name():
    os_name = platform.system()
    return os_name

## Are we running inside a docker session?
def is_running_in_docker():
    if os.path.exists('/proc/self/cgroup'):
        with open('/proc/self/cgroup', 'rt') as f:
            return 'docker' in f.read()
    return False

## get ip address of the host
def get_container_ip():
    import socket

    # Get the hostname of the machine running the script
    hostname = socket.gethostname()

    # Get the IP address of the container by resolving the hostname
    ip_address = socket.gethostbyname(hostname)
    return ip_address

## get our external ip address
def get_external_ip():
    import requests
    url = "https://api.ipify.org"
    try: 
        ## do not fail whole lib for this
        response = requests.get(url)
        return response.text.strip()
    except: 
        return "0.0.0.0"

## get our external port
def get_port(): 
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    return port

## just to get the list of all installed Python modules in the running session
def get_list_of_modules():
    installed_packages = pkg_resources.working_set
    installed_packages_list=[]
    for i in installed_packages:
        installed_packages_list.append({i.key: i.version})
    return installed_packages_list

## create a tunnel via cloudflare
def create_tunnel(port):
    import subprocess
    import re
    try:
        command = ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in process.stderr:
            data = line.decode('utf-8')
            output = re.search(r'https:\/\/.*\.trycloudflare\.com', data)
            if output and output.group(0):
                return f'{output.group(0)}/'

        print('Could not create a Tunnel')
        return None
    
    except Exception as err:
        print('Could not create a Tunnel')
        return None
    
## ------------------------------------------------------------------------
#       GPU utils
## ------------------------------------------------------------------------

## which GPU is this? (will require access to nvidia-smi)
def get_gpu_attr(_attr):
   output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
   COMMAND = "nvidia-smi --query-gpu="+_attr+" --format=csv"
   try:
        memory_use_info = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
   except sp.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
   memory_use_values = [x.replace('\r', '') for i, x in enumerate(memory_use_info)]
   return memory_use_values


## get GPU Cuda info
# see here: https://gist.github.com/tispratik/42a71cae34389fd7c8e89496ae8813ae
def getCudaInfo():
    
    display_name = "no GPU"
    display_cores = "0"
    display_major = "0"
    display_minor = "0"

    if cuda:
        CUDA_SUCCESS = 0
        CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT = 16
        CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR = 39
        CU_DEVICE_ATTRIBUTE_CLOCK_RATE = 13
        CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE = 36

        nGpus = ctypes.c_int()
        name = b' ' * 100
        cc_major = ctypes.c_int()
        cc_minor = ctypes.c_int()
        cores = ctypes.c_int()
        threads_per_core = ctypes.c_int()
        clockrate = ctypes.c_int()
        freeMem = ctypes.c_size_t()
        totalMem = ctypes.c_size_t()

        result = ctypes.c_int()
        device = ctypes.c_int()
        context = ctypes.c_void_p()
        error_str = ctypes.c_char_p()

        result=cuda.cuInit(0)
        if(result != CUDA_SUCCESS):
            print("error %d " % (result))
            return 0
        
        if(cuda.cuDeviceGetCount(ctypes.byref(nGpus)) != CUDA_SUCCESS):
            return 0

        for i in range(nGpus.value):

            # get device
            if(cuda.cuDeviceGet(ctypes.byref(device), i) != CUDA_SUCCESS):
                return 0
            if (cuda.cuDeviceComputeCapability(ctypes.byref(cc_major), ctypes.byref(cc_minor), device) != CUDA_SUCCESS):  
                return 0
            if (cuda.cuDeviceGetName(ctypes.c_char_p(name), len(name), device) != CUDA_SUCCESS): 
                return 0
            if(cuda.cuDeviceGetAttribute(ctypes.byref(cores), CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, device) != CUDA_SUCCESS):
                return 0

        display_name=name.split(b'\0', 1)[0].decode()
        display_major=cc_major.value
        display_minor=cc_minor.value
        display_cores=cores.value * _ConvertSMVer2Cores(cc_major.value, cc_minor.value)

    return {
        "name": display_name,
        "compute_major": display_major,
        "compute_minor": display_minor,
        "cuda cores": display_cores 
    }

def _ConvertSMVer2Cores(major, minor):
    # Returns the number of CUDA cores per multiprocessor for a given
    # Compute Capability version. There is no way to retrieve that via
    # the API, so it needs to be hard-coded.
    return {
    # Tesla
      (1, 0):   8,      # SM 1.0
      (1, 1):   8,      # SM 1.1
      (1, 2):   8,      # SM 1.2
      (1, 3):   8,      # SM 1.3
    # Fermi
      (2, 0):  32,      # SM 2.0: GF100 class
      (2, 1):  48,      # SM 2.1: GF10x class
    # Kepler
      (3, 0): 192,      # SM 3.0: GK10x class
      (3, 2): 192,      # SM 3.2: GK10x class
      (3, 5): 192,      # SM 3.5: GK11x class
      (3, 7): 192,      # SM 3.7: GK21x class
    # Maxwell
      (5, 0): 128,      # SM 5.0: GM10x class
      (5, 2): 128,      # SM 5.2: GM20x class
      (5, 3): 128,      # SM 5.3: GM20x class
    # Pascal
      (6, 0):  64,      # SM 6.0: GP100 class
      (6, 1): 128,      # SM 6.1: GP10x class
      (6, 2): 128,      # SM 6.2: GP10x class
    # Volta
      (7, 0):  64,      # SM 7.0: GV100 class
      (7, 2):  64,      # SM 7.2: GV11b class
    # Turing
      (7, 5):  64,      # SM 7.5: TU10x class
    }.get((major, minor), 64)   # unknown architecture, return a default value

## ------------------------------------------------------------------------
#       getInfo endoint
## ------------------------------------------------------------------------

## get various info about this host
def getHostInfo(_engine):
    from datetime import datetime
    now = datetime.now()
    objGPU={}
    objGPU["memory_free"]=get_gpu_attr("memory.free")[0]
    objGPU["memory_used"]=get_gpu_attr("memory.used")[0]
    objGPU["name"]=get_gpu_attr("gpu_name")[0]
    objGPU["driver_version"]=get_gpu_attr("driver_version")[0]
    objGPU["temperature"]=get_gpu_attr("temperature.gpu")[0]
    objGPU["utilization"]=get_gpu_attr("utilization.gpu")[0]

    objCuda=getCudaInfo()        
    return {
        "datetime": now.strftime("%d/%m/%Y %H:%M:%S"), 
        "isDocker": is_running_in_docker(),
        "internal IP": get_container_ip(),
        "port": get_port(),
        "engine": _engine,
        "machine": get_machine_name(),
        "GPU": objGPU,
        "Cuda": objCuda,
        "modules": get_list_of_modules()
    }

## ------------------------------------------------------------------------
#       File / Image utils
## ------------------------------------------------------------------------

def getS3BucketRoot () :
    return "s3://osais/"

def getS3BucketInputDir () :
    return "input/"

def getS3BucketOutputDir () :
    return "output/"

## downloads an image as file from external URL
def osais_downloadImage(url) :
    root=getS3BucketRoot()
    if root in url:
        return osais_downloadFileFromS3(url, gInputDir)

    import urllib.request

    # Determine the file name and extension of the image based on the URL.
    file_name, file_extension = os.path.splitext(url)
    print ("will download image from "+url)
    
    # Define the local file path where the image will be saved.
    spliter='/'
    local_filename=file_name.split(spliter)[-1]
    local_file_path = f"./_input/{local_filename}{file_extension}"

    # Download the image from the URL and save it locally.
    response = urllib.request.urlopen(url)
    image_data = response.read()
    with open(local_file_path, 'wb') as f:
        f.write(image_data)

    return f"{local_filename}{file_extension}"

## upload image to S3 and tag it
def osais_uploadFileToS3(_filename, _dirS3, objTag): 
    global gS3
    global gS3Bucket
    root=getS3BucketRoot()
    if gS3!=None:
        try:
            from urllib import parse    
            # Filename - File to upload
            # Bucket - Bucket to upload to (the top level directory under AWS S3)
            # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
            _baseName=os.path.basename(_filename)
            gS3.meta.client.upload_file(Filename=_filename, Bucket=gS3Bucket, Key=_dirS3+_baseName, ExtraArgs={
                'ACL':'public-read', 
                "Tagging": parse.urlencode(objTag)
            })
            print("=> Uploaded "+_filename+" to S3")
            return root+_dirS3+_baseName
            
        except Exception as err:
            consoleLog({"msg":"Could not upload file to S3"})
            raise err
        
    return False

def osais_downloadFileFromS3(_filePath, _dir): 
    global gS3
    global gS3Bucket

    if gS3!=None:
        try:
            # Filename - File to upload
            # Bucket - Bucket to upload to (the top level directory under AWS S3)
            # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
            _baseName=os.path.basename(_filePath)
            local_file_path = _dir+_baseName

            gS3.Bucket(gS3Bucket).download_file(_filePath, local_file_path)
            print("=> Downloaded "+_filePath+" from S3")
            return local_file_path
        except Exception as err:
            consoleLog({"msg":"Could not download file "+_filePath+" from S3"})
            raise err
        
    return False


## ========================================================================
## 
##                      OSAIS starts here 
## 
## ========================================================================

## ------------------------------------------------------------------------
#       OSAIS python Lib (interface between AIs and OSAIS)
## ------------------------------------------------------------------------

import requests
import schedule
import json
import sys
import base64
from datetime import datetime
import argparse

##from osais import osais_initializeAI, osais_getInfo, osais_getHarwareInfo, osais_isDocker, osais_getClientID, osais_getDirectoryListing, osais_runAI, osais_authenticateAI, osais_isDebug, osais_authenticateClient, osais_postRequest, osais_downloadImage, osais_uploadFileToS3

## ------------------------------------------------------------------------
#       all global vars
## ------------------------------------------------------------------------

gVersionLibOSAIS=__version__    ## version of this library (to keep it latest everywhere)
gUsername=None                  ## user owning this AI (necessary to claim VirtAI regs)

gName=None                      ## name of this AI (name of engine)
gVersion="0.0.0"                ## name of this AI's version (version of engine)
gDescription=None               ## AI's quick description
gGithub=None                    ## where this AI came from (on internet)
gMachineName=get_machine_name() ## the name of the machine (will change all the time if inside docker, ot keep same if running on local server)
gLastChecked_at=datetime.utcnow()  ## when was this AI last used for processing anything
gLastProcessStart_at=None       ## when was this AI last start event for processing anything

## virtual AI / local /docker ? note: AI can act BOTH at the same time as VirtualAI and a LocalAI for a gateway
gIsDocker=is_running_in_docker()   ## are we running in a Docker?
gIsVirtualAI=False              ## are we working as a Virtual AI config?
gIsLocal=False                  ## are we working locally (with a gateway)?
gIsDebug=False                  ## are we working in debug (localhost server)? note: we cannot be PROD and DEBUG at the same time
gAITunel=None                   ## tunnel for where to call this AI (caller in a docker cannot call localhost:port)

## OSAIS location
gOriginOSAIS=None               ## location of OSAIS (Prod or debug)

## authenticate into OSAIS as a VAI
gVAIToken=None                  ## VAI token used for authentication into OSAIS
gVAISecret=None                 ## VAI secret used for authentication into OSAIS
gVAIAuthToken=None              ## authToken into OSAIS for when working as virtual AI

## authenticate into OSAIS as a CLIENT (most likely DEMO CLIENT)
gClientID=None                  ## ID of authenticated client into OSAIS 
gClientAuthToken=None           ## the resulting Auth token as Client, after login

## Gateway
gOriginGateway=None             ## location of the local gateway for this (local) AI, as http://{ip}:{port} or preferrably <tunnel>

## AWS related
gS3=None
gS3Bucket=None
gAWSID=None
gAWSSecret=None
gAWSSession=None

## IP and Ports
gExtIP=get_external_ip()        ## where this AI can be accessed from outside (IP)
gIPLocal=get_container_ip()     ## where this AI can be accessed locally
gPortAI=None                    ## port where this AI is accessed (will be set by AI config)
gPortGateway=3023               ## port where the gateway can be accessed
gPortLocalOSAIS=3022            ## port where a local OSAIS can be accessed

## temp cache
gAProcessed=[]                  ## all token being sent to processing (never call twice for same)
gIsScheduled=False              ## do we have a scheduled event running?

## run times
gIsBusy=False                   ## True if AI busy processing
gDefaultCost=1000               ## default cost value in ms (will get overriden fast, this value is no big deal)
gaProcessTime=[]                ## Array of last x (10/20?) time spent for processed requests 
gAverageCostInUSD=0             ## average cost value in USD

## processing specifics
gArgsOSAIS=None                 ## the args passed to the AI which are specific to OSAIS for sending notifications

## when running as vAI
gInputDir="./_input/"
gOutputDir="./_output/"

AI_PROGRESS_ERROR=-1
AI_PROGRESS_REQSENT=0                  # unused (that s for OSAIS to know it sent the req)
AI_PROGRESS_REQRECEIVED=1
AI_PROGRESS_AI_STARTED=2
AI_PROGRESS_INIT_IMAGE=3
AI_PROGRESS_DONE_IMAGE=4
AI_PROGRESS_AI_STOPPED=5

## ------------------------------------------------------------------------
#       Load config
## ------------------------------------------------------------------------

# load the config file into a JSON
def _loadConfig(_name): 
    global gVersion
    global gDescription
    global gGithub
    global gDefaultCost

    _json = None
    _dirFile=None
    try:
        from pathlib import Path
        current_working_directory = Path.cwd()
        _dirFile=f'{current_working_directory}/{_name}.json'
        fJSON = open(_dirFile)
        _json = json.load(fJSON)
    except Exception as err:
        print(f'CRITICAL: No config file {_dirFile}')
        sys.exit()

    # do not set global vars for osais config
    if _name!= "osais":
        gVersion=_json["version"]
        gDescription=_json["description"]
        gGithub=_json["github"]
        _cost=_json["default_cost"]
        if _cost!=None:
            gDefaultCost=_cost

    return _json

# get the full AI config, including JSON params and hardware info
def _getFullConfig(_name) :
    global gUsername
    global gPortAI
    global gName
    global gVAIToken
    global gVAISecret
    global gOriginOSAIS
    global gIsVirtualAI
    global gIPLocal
    global gExtIP
    global gIsLocal
    global gAITunel

    _ip=gExtIP
    if gIsDebug:
        _ip=gIPLocal                ## we register with local ip if we are in local gateway mode

    _location=gAITunel
    if _location==None:
        _location=f'http://{_ip}:{gPortAI}/'

    _jsonBase=_loadConfig("osais")
    _jsonAI=_loadConfig(_name)

    objCudaInfo=getCudaInfo()
    gpuName="no GPU"
    if objCudaInfo != 0 and "name" in objCudaInfo and objCudaInfo["name"]:
        gpuName=objCudaInfo["name"]

    _jsonAI["ip"]=_ip
    _jsonAI["port"]=gPortAI
    _jsonAI["location"]=_location
    return {
        "username": gUsername,
        "os": get_os_name(),
        "gpu": gpuName,
        "machine": get_machine_name(),
        "location": _location,
        "ip": _ip,
        "port": gPortAI,
        "osais": gOriginOSAIS,
        "gateway": "http://"+_ip+":3023/",
        "config_ai": _jsonAI,
        "config_base": _jsonBase
    }

## PUBLIC - are we running in DEBUG mode?
def osais_isDebug():
    global gIsDebug
    return gIsDebug

## PUBLIC - are we running in local mode?
def osais_isLocal():
    global gIsLocal
    return gIsLocal

## PUBLIC - are we running in VAI mode?
def osais_isVirtualAI():
    global gIsVirtualAI
    return gIsVirtualAI

## PUBLIC - load the config of this AI
def osais_loadConfig(_name): 
    return _loadConfig(_name)

def _setPropVal(key, val):
    global gUsername
    global gIsVirtualAI
    global gIsDebug
    global gIsLocal
    global gName
    global gVAIToken
    global gVAISecret
    global gAWSSession
    global gS3
    global gS3Bucket
    global gOriginOSAIS

    global gAWSID
    global gAWSSecret

    if key=='TUNNEL_OSAIS' and val!=None and gOriginOSAIS==None:
        if gOriginOSAIS==None:
            if gIsDebug: 
                if val:
                    gOriginOSAIS=val     # we prefer to get the tunnel location of osais
                else:
                    gOriginOSAIS="http://"+gIPLocal+":3022/"
            else:
                gOriginOSAIS="https://opensourceais.com/"

    if key == "USERNAME" and val!=None and gUsername==None:
        gUsername = val

    if key == "IS_DEBUG" and val!=None:
        _isDebug= (val=="True")
        if _isDebug!=gIsDebug:
            print(f'=> is DEBUG updated to {_isDebug}')
            gIsDebug=_isDebug

    if key == "IS_LOCAL" and val!=None:
        _isLocal = (val=="True")
        if _isLocal!=gIsLocal:
            print(f'=> is Local updated to {_isLocal}')
            gIsLocal=_isLocal
                
    if key == "IS_VIRTUALAI" and val!=None:
        _isVirtualAI = (val=="True")
        if _isVirtualAI!=gIsVirtualAI:
            print(f'=> is Virtual updated to {_isVirtualAI}')
            gIsVirtualAI=_isVirtualAI

    if key == "ENGINE" and val!=None:
        _name = val
        if _name!=gName:
            print(f"=> Engine name updated to '{_name}'")
            gName=_name
    
    if key == "S3_BUCKET" and val!=None:
        _s3 = val
        if _s3!=gS3Bucket:
            print(f"=> Set S3 bucket to '{_s3}'")
            gS3Bucket=_s3
                
    if key == "VAI_ID" and val!=None and gVAIToken==None:
        gVAIToken = val
    
    if key == "VAI_SECRET" and val!=None and gVAISecret==None:
        gVAISecret = val
    
    if key == "AWS_ACCESS_KEY_ID" and val!=None and gAWSID==None:
        gAWSID = val
    
    if key=='AWS_ACCESS_KEY_SECRET' and val!=None and gAWSSecret==None:
        gAWSSecret=val

## PUBLIC - Get env from file (local or docker)
def osais_getEnv(_filename):
    global gUsername
    global gIsVirtualAI
    global gIsDebug
    global gIsLocal
    global gName
    global gVAIToken
    global gVAISecret
    global gAWSSession
    global gS3
    global gS3Bucket
    global gOriginOSAIS
    global gAWSID
    global gAWSSecret

    ## read env from config file
    if _filename!=None:
        try:
            with open(_filename, "r") as f:
                content = f.read()
            print(f'=> Reading env vars from {_filename}')
            variables = content.split("\n")
            for var in variables:
                if var!="":
                    key, value = var.split("=")
                    _setPropVal(key, value)

        except Exception as err: 
            consoleLog({"msg": f'No env file {_filename}'})

    # overload with env settings if any
    print(f'=> Setting env vars from ENV...')    
    _setPropVal("USERNAME", os.environ.get('USERNAME'))
    _setPropVal("ENGINE", os.environ.get('ENGINE'))
    _setPropVal("IS_VIRTUALAI", os.environ.get('IS_VIRTUALAI'))
    _setPropVal("IS_LOCAL", os.environ.get('IS_LOCAL'))
    _setPropVal("IS_DEBUG", os.environ.get('IS_DEBUG'))
    _setPropVal("S3_BUCKET", os.environ.get('S3_BUCKET'))
    _setPropVal("VAI_ID", os.environ.get('VAI_ID'))
    _setPropVal("VAI_SECRET", os.environ.get('VAI_SECRET'))
    _setPropVal("AWS_ACCESS_KEY_ID", os.environ.get('AWS_ACCESS_KEY_ID'))
    _setPropVal("AWS_ACCESS_KEY_SECRET", os.environ.get('AWS_ACCESS_KEY_SECRET'))    
    _setPropVal("TUNNEL_OSAIS", os.environ.get('TUNNEL_OSAIS'))

    ## log into S3
    if gAWSID!=None and gAWSSecret!=None:
        gAWSSession = boto3.Session(
            region_name="eu-west-2",            ## todo : externalise this
            aws_access_key_id=gAWSID,
            aws_secret_access_key=gAWSSecret
        )
        gS3 = gAWSSession.resource('s3')
        print(f'=> Logged into AWS S3')
        
    return {
        "name": gName,
        "osais": gOriginOSAIS,
        "username": gUsername,
        "isLocal": gIsLocal,
        "isVirtualAI": gIsVirtualAI,
        "isDebug": gIsDebug
    }

## ------------------------------------------------------------------------
#       cost calculation
## ------------------------------------------------------------------------

# init the dafault cost array
def _initializeCost() :
    global gDefaultCost
    global gaProcessTime
    from array import array
    gaProcessTime=array('f', [gDefaultCost,gDefaultCost,gDefaultCost,gDefaultCost,gDefaultCost,gDefaultCost,gDefaultCost,gDefaultCost,gDefaultCost,gDefaultCost])

# init the dafault cost array
def _addCost(_cost) :
    global gaProcessTime
    gaProcessTime.insert(0, _cost)
    gaProcessTime.pop()

# init the dafault cost array
def _getAverageCostInMs() :
    global gaProcessTime
    average = sum(gaProcessTime) / len(gaProcessTime)
    return average

## ------------------------------------------------------------------------
#       args processing
## ------------------------------------------------------------------------

# where is the output dir?
def _getOutputDir():
    global gArgsOSAIS
    global gOutputDir

    if gArgsOSAIS!=None and  gArgsOSAIS.outdir!=None:
        return gArgsOSAIS.outdir
    return gOutputDir

# receives args from request and put them in a array for processing
def _getArgs(_args):
    aResult = []
    for key, value in _args.items():
        if key.startswith("-"):
            aResult.append(key)
            aResult.append(value)
    return aResult

# give new args 
def _argsFromFilter(_originalArgs, _aFilter, _bKeep):
    from werkzeug.datastructures import MultiDict
    _dict = MultiDict([])
    for i, arg in enumerate(_originalArgs):
        if _bKeep:
            if arg in _aFilter and i < len(_originalArgs) - 1:
                _dict.add(arg, _originalArgs[i+1])
        else:
            if arg not in _aFilter and i < len(_originalArgs) - 1:
                _dict.add(arg, _originalArgs[i+1])
    
    _args=_getArgs(_dict)
    return _args

## ------------------------------------------------------------------------
#       System info
## ------------------------------------------------------------------------

def _clearDir():
    clearOldFiles(gInputDir)
    clearOldFiles(gOutputDir)

## PUBLIC - running in docker?
def osais_isDocker() :
    global gIsDocker
    return gIsDocker

## PUBLIC - info about harware this AI is running on
def osais_getHarwareInfo() :
    global gName
    return getHostInfo(gName)

## PUBLIC - get list of files in a dir (check what was generated)
def osais_getDirectoryListing(_dir) :
    return listDirContent(_dir)

## PUBLIC - info about this AI
def osais_getInfo() :
    global gExtIP
    global gPortAI
    global gName
    global gVersion
    global gIsDocker
    global gMachineName
    global gUsername
    global gIsBusy
    global gLastProcessStart_at
    global gLastChecked_at
    global gAverageCostInUSD
    global gAITunel

    objConf=_getFullConfig(gName)
    return {
        "name": gName,
        "version": gVersion,
        "location": objConf["location"],
        "osais": objConf["osais"],
        "gateway": objConf["gateway"],
        "isRunning": True,    
        "isDocker": gIsDocker,    
        "lastActive_at": gLastChecked_at,
        "lastProcessStart_at": gLastProcessStart_at,
        "machine": gMachineName,
        "owner": gUsername, 
        "isAvailable": (gIsBusy==False),
        "averageResponseTime": _getAverageCostInMs(), 
        "averageCost": gAverageCostInUSD,           ## todo
        "config_ai": objConf["config_ai"],
        "config_base": objConf["config_base"]
    }

## ------------------------------------------------------------------------
#       connect to Gateway
## ------------------------------------------------------------------------

# notify the gateway of our AI config file
def _connectWithGateway() : 
    global gName
    global gOriginGateway

    headers = {
        "Content-Type": 'application/json', 
        'Accept': 'text/plain',
    }
    objParam=_getFullConfig(gName)

    ## notify gateway
    try:
        response = requests.post(f"{gOriginGateway}api/v1/public/ai/config", headers=headers, data=json.dumps(objParam))
        objRes=response.json()["data"]
        if objRes is None:
            raise ValueError("CRITICAL: could not notify Gateway on "+gOriginGateway)

    except Exception as err:
        consoleLog({"msg":"could not notify Gateway on "+gOriginGateway})
        raise err
    return True

## PUBLIC - Reset connection to local gateway
def osais_resetGateway():
    global gOriginGateway
    global gOriginOSAIS
    global gUsername

    ## note: if in Docker, we can only call the gateway on its tunnel
    ## ask OSAIS the gateways (and tunnel location) for the same owner of this AI
    try:
        headers = {
            "Content-Type": 'application/json', 
            'Accept': 'text/plain',
        }
        response = requests.get(f"{gOriginOSAIS}api/v1/public/user/{gUsername}/gateways", headers=headers)
        objRes=response.json()["data"]
        if objRes is None:
            raise ValueError("could not access OSAIS on "+gOriginOSAIS)

        ## take the first gateway and notify
        ## todo later ... maybe we update ALL gateways with this AI? (the AI is a slave of all this user's gatyeways?)
        gOriginGateway=objRes[0]["domain"]

    except Exception as err:
        consoleLog({"msg":"could not notify OSAIS on "+gOriginOSAIS})
        raise err

    try:
        _connectWithGateway()
    except Exception as err:
        consoleLog({"msg":"Could not reset connection to Gateway"})
        raise err
    
    return True

## ------------------------------------------------------------------------
#       authenticate into OSAIS as virtual AI
## ------------------------------------------------------------------------

# Authenticate into OSAIS as a VAI
def _loginVAI(_originOSAIS, _token, _secret):
    global gName

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{_originOSAIS}api/v1/public/virtualai/login", headers=headers, data=json.dumps({
            "token": _token,
            "secret": _secret
        }))

        objRes=response.json()["data"]
        if objRes is None:
            consoleLog({"msg": "COULD NOT LOGIN into "+_originOSAIS+", stopping it here"})
            sys.exit()
        return objRes["authToken"]    
    except Exception as err:
        consoleLog({"msg":"Exception raised while trying to login as VAI into "+_originOSAIS})
        raise err

## call OSAIS to update Virt AI config
def _updateVAIConfig(): 
    global gName
    global gOriginOSAIS
    global gVAIAuthToken

    objParam=_getFullConfig(gName)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gVAIAuthToken}"
    }

    try:
        response = requests.patch(f"{gOriginOSAIS}api/v1/private/virtualai/config", headers=headers, data=json.dumps({
            "jsonEngine": objParam["config_ai"],
        }))

        objRes=response.json()["data"]
        if objRes is None:
            consoleLog({"msg": "COULD NOT UPDATE CONFIG"})
            return False
        else:
            print("=> We patched VAI config of OSAIS at "+gOriginOSAIS)
        return True
    except Exception as err:
        consoleLog({"msg":"Exception raised while trying to update VAI config into "+gOriginOSAIS})
        return False

## PUBLIC - Authenticate the Virtual AI into OSAIS
def osais_authenticateAI():
    global gIsVirtualAI
    global gOriginOSAIS
    global gIsScheduled
    global gVAIToken
    global gVAISecret
    global gVAIAuthToken

    resp={"data": None}
    if gIsVirtualAI:
        try:
            ## login as VAI 
            gVAIAuthToken=_loginVAI(gOriginOSAIS, gVAIToken, gVAISecret)
            _updateVAIConfig()

        except Exception as err:
            consoleLog({"msg":"Exception raised while trying to authenticate to OSAIS"})
            raise err
        
        # Run the scheduler
        if gIsScheduled==False:
            gIsScheduled=True
            schedule.every().day.at("10:30").do(_loginVAI)

    return resp

## ------------------------------------------------------------------------
#       authenticate into OSAIS as Client (user)
## ------------------------------------------------------------------------

## get info about this authenticated CLIENT
def getClientInfo():
    global gOriginOSAIS

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gClientAuthToken}"
    }

    objRes=None
    try:
        response = requests.get(f"{gOriginOSAIS}api/v1/private/client", headers=headers)
        objRes=response.json()["data"]            
    except Exception as err:
        return {"data": objRes}

    return {"data": objRes}

## token of the authenticated CLIENT
def osais_getClientID(): 
    return gClientID

## authenticate as a CLIENT
def _authenticateClient(_route, _id, _secret):
    headers = {
        "Content-Type": "application/json"
    }
    try:
        url=f"{_route}api/v1/public/client/demo"      ## get a demo auth token
        if _id!= None:
            url=f"{_route}api/v1/public/client/login"
        response = requests.post(url, headers=headers, data=json.dumps({
            "token": _id,
            "secret": _secret
        }))

        objRes=response.json()["data"]
        if objRes is None:
            consoleLog({"msg": "COULD NOT LOGIN AS CLIENT into "+_route})
        resp={"data": {
            "token": objRes["token"],
            "authToken": objRes["authToken"],
        }}
        return resp

    except Exception as err:
        consoleLog({"msg":"Exception raised while trying to login as CLIENT into "+_route})
        resp={"data": {
            "token": None,
            "authToken": None
        }}

# Authenticate into OSAIS (as client)
def osais_authenticateClient(_id, _secret):
    global gOriginOSAIS
    global gClientAuthToken
    global gClientID
    global gIsLocal

    resp={"data": None}
    
    ## log as client into osais
    resp=_authenticateClient(gOriginOSAIS, _id, _secret)
    gClientAuthToken=resp["data"]["authToken"]
    gClientID=resp["data"]["token"]
        
    dataClient=getClientInfo()
    resp["data"]["user"]=dataClient["data"]["user"]
    return resp 

def authenticateClientAsDemo():
    return osais_authenticateClient(None, None)

## ------------------------------------------------------------------------
#       ask OSAIS to process a request
## ------------------------------------------------------------------------

def osais_postRequest(objReq):
    global gClientAuthToken
    global gName

    resp={"data": None}
    _url=None
    _authToken=gClientAuthToken
    _url=f"{gOriginOSAIS}api/v1/private/client/ai/"+objReq.gName

    try:
        response = requests.post(_url, headers={
            "Content-Type": "application/json",
            'Accept': 'text/plain',
            "Authorization": f"Bearer {_authToken}"
        }, data=json.dumps(objReq))
        objRes=response.json()["data"]
        if objRes is None:
            consoleLog({"msg": "COULD NOT post request"})
        resp={"data": objRes}

    except Exception as err:
        raise err

    return resp 

## ------------------------------------------------------------------------
#       Run the AI
## ------------------------------------------------------------------------

## PUBLIC - parse args for OSAIS (not those for AI)
def osais_initParser(aArg):
    global gArgsOSAIS
    global gInputDir
    global gOutputDir

    # Create the parser
    vq_parser = argparse.ArgumentParser(description='Arg parser init by OSAIS')

    # Add the AI Gateway / OpenSourceAIs arguments
    vq_parser.add_argument("-orig",  "--origin", type=str, help="Caller's origin", default=None , dest='OSAIS_origin')      ##  this is for comms with AI Gateway
    vq_parser.add_argument("-t",  "--token", type=str, help="OpenSourceAIs token", default="0", dest='tokenAI')             ##  this is for comms with OpenSourceAIs
    vq_parser.add_argument("-u",  "--username", type=str, help="OpenSourceAIs username", default="", dest='username')       ##  this is for comms with OpenSourceAIs
    vq_parser.add_argument("-uid",  "--unique_id", type=int, help="Unique ID of this AI session", default=0, dest='uid')    ##  this is for comms with OpenSourceAIs
    vq_parser.add_argument("-odir", "--outdir", type=str, help="Output directory", default=gOutputDir, dest='outdir')
    vq_parser.add_argument("-idir", "--indir", type=str, help="input directory", default=gInputDir, dest='indir')
    vq_parser.add_argument("-cycle", "--cycle", type=int, help="cycle", default=0, dest='cycle')
    vq_parser.add_argument("-filename", "--filename", type=str, help="filename", default="default", dest='filename')

    gArgsOSAIS = vq_parser.parse_args(aArg)
    if gArgsOSAIS.OSAIS_origin!=None:
        print("=> origin set to "+gArgsOSAIS.OSAIS_origin)
    else:
        print("=> origin set to None")
    return True
    
## run the AI (at least try)
def _runAI(isWarmup, *args, ):
    global gIsBusy
    global gAProcessed
    global gName 
    global gLastProcessStart_at
    global gOriginOSAIS
    global gIsLocal

    ## get args
    fn_run=args[0]
    _args=args[1]

    ## do not process twice same uid
    _uid=_args.get('-uid')
    if _uid in gAProcessed:
        consoleLog({"msg": "Not processing "+str(_uid)+", already tried!"})
        return  None    
    print ("\r\n=> Processing request with UID "+str(_uid))

    ## process the filename and download it locally
    try:
        ## the filename of the locally downloaded "url_upload" url (or the S3 url)
        _filename=_args.get('-filename')

        # if file was in S3, download it
        _isFileInS3= getS3BucketRoot() in _filename
        if _isFileInS3:
            try:
                # download the file locally, reset dir to ours
                _basename=_filename[11:]
                _filename=osais_downloadFileFromS3(_basename, gInputDir)
                _args["-filename"]=os.path.basename(_filename)
                _args["-idir"]=gInputDir
                _args["-odir"]=gOutputDir

            except Exception as err:
                raise err
        else:
            if not _args["-warmup"]:
                raise ValueError("CRITICAL: require a upload url in S3 ")
                
    except Exception as err:
        print("=> did not get a -filename, we continue")
        _args["-idir"]=gInputDir
        _args["-odir"]=gOutputDir

    if isWarmup:
        _args["-idir"]="./static/"
        print("=> Warming up...")

    ## start time
    gIsBusy=True
    beg_date = datetime.utcnow()
    
    ## reprocess AI args
    aArgForparserAI=_getArgs(_args)
    args_ExclusiveOSAIS=['-orig', '-t', '-u', '-uid', '-cycle', '-warmup']
    aArgForparserAI=_argsFromFilter(aArgForparserAI, args_ExclusiveOSAIS, False)

    ## Init OSAIS Params (from all args, keep only those for OSAIS)
    aArgForParserOSAIS=_getArgs(_args)
    args_ExclusiveOSAIS.append('-odir')
    args_ExclusiveOSAIS.append('-idir')
    aArgForParserOSAIS=_argsFromFilter(aArgForParserOSAIS, args_ExclusiveOSAIS, True)
    osais_initParser(aArgForParserOSAIS)

    ## now that we have processed args, we keep them locally (avoid globals messup)
    _localOrig=gArgsOSAIS.OSAIS_origin
    _localT=gArgsOSAIS.tokenAI
    _localU=gArgsOSAIS.username
    _localUID=gArgsOSAIS.uid
    _localODir=gArgsOSAIS.outdir
    _localIDir=gArgsOSAIS.indir
    _localCycle=gArgsOSAIS.cycle
    _localFilename=gArgsOSAIS.filename
    _isGateway=None

    if isWarmup:
        _localOrig=None
    else :
        ## req received from a gateway ot OSAIS?
        _isGateway = not (_localOrig == "https://opensourceais.com/" or _localOrig == "https://opensourceais.com" or _localOrig[:5]== "http:")
        print("=> before run: processed args from url: "+str(aArgForparserAI)+"\r\n")

    ## notify OSAIS (Req received)
    CredsParam=getCredsParams(_localT, _localU, _isGateway)
    MorphingParam=getMorphingParams(_localUID, _localCycle, _localFilename)
    StageParam=getStageParams(AI_PROGRESS_REQRECEIVED, 0)
    osais_notify(_localOrig, CredsParam, MorphingParam , StageParam)

    ## processing accepted
    gLastProcessStart_at=datetime.utcnow()
    gAProcessed.append(_uid)

    ## notify OSAIS (start)
    StageParam=getStageParams(AI_PROGRESS_AI_STARTED, 0)
    osais_notify(_localOrig, CredsParam, MorphingParam , StageParam)

    ## start watch file creation
    _output=_getOutputDir()
    watch_directory(_output, osais_onNotifyFileCreated, _args)
    
    ## Notif OSAIS
    StageParam=getStageParams(AI_PROGRESS_INIT_IMAGE, 0)
    osais_notify(_localOrig, CredsParam, MorphingParam , StageParam)

    ## run AI
    response=None
    try:
        if len(args)==2:
            response=fn_run(aArgForparserAI)
        else:
            if len(args)==3:
                response=fn_run(aArgForparserAI, args[2])
            else:
                response=fn_run(aArgForparserAI, args[2], args[3])
    except Exception as err:
        gIsBusy=False
        consoleLog({"msg": "Error processing args in RUN command"})
        raise err

    ## calculate cost
    gIsBusy=False
    end_date = datetime.utcnow()
    delta=end_date - beg_date
    cost = int(delta.total_seconds()* 1000 + delta.microseconds / 1000)

    if isWarmup:
        _strDelta=str(delta)
        print("\r\n=> AI ready!")
        print("=> Able to process requests in "+_strDelta+" secs\r\n")
    else:
        _addCost(cost)

    ## notify end
    StageParam=getStageParams(AI_PROGRESS_AI_STOPPED, cost)
    osais_notify(_localOrig, CredsParam, MorphingParam , StageParam)

    ## default OK response if the AI does not send any
    if response==None:
        response=True
    return response

### PUBLIC - warmup the AI (at least try)
def osais_warmupAI(*args):
    return _runAI(True, *args)

## PUBLIC - run the AI (at least try)
def osais_runAI(*args):
    return _runAI(False, *args)

## ------------------------------------------------------------------------
#       get formatted params from AI current state
## ------------------------------------------------------------------------

def getCredsParams(_token, _username, _isGateway) :
    global gName
    global gArgsOSAIS
    return {
        "engine": gName, 
        "version": gVersion, 
        "tokenAI": _token,
        "username": _username,
        "isGateway": _isGateway
    } 

def getMorphingParams(_localUID, _localCycle, _localFilename) :
    global gArgsOSAIS
    return {
        "uid": _localUID,
        "cycle": _localCycle,
        "filename": _localFilename
    }

def getStageParams(_stage, _cost) :
    global gArgsOSAIS
    if _stage==AI_PROGRESS_REQRECEIVED:
        return {"stage": AI_PROGRESS_REQRECEIVED, "descr":"Acknowledged request"}
    if _stage==AI_PROGRESS_ERROR:
        return {"stage": AI_PROGRESS_AI_STOPPED, "descr":"AI stopped with error"}
    if _stage==AI_PROGRESS_AI_STARTED:
        return {"stage": AI_PROGRESS_AI_STARTED, "descr":"AI started"}
    if _stage==AI_PROGRESS_AI_STOPPED:
        return {"stage": AI_PROGRESS_AI_STOPPED, "descr":"AI stopped", "cost": _cost}
    if _stage==AI_PROGRESS_INIT_IMAGE:
        return {"stage": AI_PROGRESS_INIT_IMAGE, "descr":"destination image = "+gArgsOSAIS.filename}
    if _stage==AI_PROGRESS_DONE_IMAGE:
        return {"stage": AI_PROGRESS_DONE_IMAGE, "descr":"copied input image to destination image"}
    return {"stage": AI_PROGRESS_ERROR, "descr":"error"}

## ------------------------------------------------------------------------
#       Notifications to Gateway / OSAIS
## ------------------------------------------------------------------------

# Upload image to OSAIS 
def _uploadImageToOSAIS(_origin, objParam):
    if gIsVirtualAI==False:
        return None
    
    global gVAIAuthToken
    
    # lets go call OSAIS AI Gateway / or OSAIS itself
    headers = {
        "Content-Type": 'application/json', 
        'Accept': 'text/plain',
        "Authorization": f"Bearer {gVAIAuthToken}"
    }

    api_url=f"{_origin}api/v1/private/virtualai/upload"        
    payload = json.dumps(objParam)
    response = requests.post(api_url, headers=headers, data=payload )
    objRes=response.json()
    return objRes    

# Upload image to a local gateway
def _uploadImageToGateway(_origin, objParam):
    if gIsVirtualAI==False:
        return None
    
    global gVAIAuthToken
    
    # lets go call OSAIS AI Gateway / or OSAIS itself
    headers = {
        "Content-Type": 'application/json', 
        'Accept': 'text/plain',
    }

    api_url=f"{_origin}api/v1/public/upload"        
    payload = json.dumps(objParam)
    response = requests.post(api_url, headers=headers, data=payload )
    objRes=response.json()
    return objRes    

async def _delayed_onNotifyFileCreated(_dir, _filename, _args):
    ## a small wait
    await wait_250ms()

    _isGateway=None
    _origin=_args.get('-orig')
    if _origin!=None:
        _isGateway = not (_origin == "https://opensourceais.com/" or _origin == "https://opensourceais.com" or _origin[:5]== "http:")

    ## upload image to S3
    objTag={
        "uid": _args["-uid"],
        "username": _args["-u"]
    }
    _fileS3=osais_uploadFileToS3(_dir+_filename, getS3BucketOutputDir(), objTag)

    # notify
    _cycle=0
    try: 
        if _args["-cycle"]:
            _cycle=_args["-cycle"]
    except:
        _cycle=0

    _stageParam=getStageParams(AI_PROGRESS_DONE_IMAGE, 0)
    _morphingParam=getMorphingParams(_args["-uid"], _cycle, _fileS3)
    _credsParam=getCredsParams(_args["-t"], _args["-u"], _isGateway)
    osais_notify(_origin, _credsParam, _morphingParam, _stageParam)            # OSAIS Notification
    return True

## got notified of file creation (by watch)
def osais_onNotifyFileCreated(_dir, _filename, _args):
    asyncio.run(_delayed_onNotifyFileCreated(_dir, _filename, _args))

def _notifyGateway(_origin, objParam):
    headers = {
        "Content-Type": "application/json"
    }
    api_url=f"{_origin}api/v1/public/notify"
    try: 
        response = requests.post(api_url, headers=headers, data=json.dumps(objParam))
        objRes=response.json()
        return objRes
    except Exception as err:
            raise err

def _notifyOSAIS(objParam):
    global gOriginOSAIS
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gVAIAuthToken}"
    }
    api_url=f"{gOriginOSAIS}api/v1/private/virtualai/notify"
    try: 
        response = requests.post(api_url, headers=headers, data=json.dumps(objParam))
        objRes=response.json()
        return objRes
    except Exception as err:
            raise err

# Direct Notify OSAIS 
def osais_notify(_origin, CredParam, MorphingParam, StageParam):
    global gIPLocal
    global gPortGateway
    global gIsVirtualAI
    global gIsLocal
    global gVAIAuthToken
    global gLastChecked_at

    ## no notification of warmup or unknown caller
    if _origin==None:
        return None
    
    gLastChecked_at = datetime.utcnow()

    # notification console log
    merged = dict()
    merged.update(CredParam)
    merged.update(MorphingParam)

    _filename=""
    if MorphingParam["filename"]!="":
        _filename=MorphingParam["filename"]

    objParam={
        "response": {
            "token": CredParam["tokenAI"],
            "uid": str(MorphingParam["uid"]),
            "stage": str(StageParam["stage"]),
            "cycle": str(MorphingParam["cycle"]),
            "engine": CredParam["engine"],
            "username": CredParam["username"],
            "descr": StageParam["descr"],
            "filename": _filename
        }
    }

    if "cost" in StageParam:
        objParam["response"]["cost"]= str(StageParam["cost"])

    ## Notify OSAIS (as Virtual AI)
    if gIsVirtualAI and CredParam["isGateway"]==False:
        try: 
            objRes=_notifyOSAIS(objParam)
            _at=objRes["data"]["notified_at"]
            print("\r\n ["+_at+"] => Notified OSAIS ("+str(StageParam["stage"])+"/ "+StageParam["descr"]+"): "+str(merged))
        except:
            consoleLog({"msg": "VAI Failed to notify stage ("+str(StageParam["stage"])+ ") to OSAIS"})

    ## Notify Gateway (as Local AI)
    if gIsLocal and CredParam["isGateway"]==True :
        try: 
            objRes=_notifyGateway(_origin, objParam)
            _at=objRes["data"]["notified_at"]
            print("\r\n ["+_at+"] => Notified Gateway ("+str(StageParam["stage"])+"/ "+StageParam["descr"]+"): "+str(merged)+ " on: "+_origin+"\r\n")
        except:
            consoleLog({"msg": "Local AI Failed to notify stage ("+str(StageParam["stage"])+ ") to local Gateway "+_origin})

    if StageParam["stage"]==AI_PROGRESS_DONE_IMAGE:
        # we do not need to upload if already in s3
        if not getS3BucketRoot() in _filename:
            if gIsVirtualAI==True:
                _dir=MorphingParam["odir"]
                if _dir==None:
                    _dir=gOutputDir
                _dirImage=_dir+_filename

                with open(_dirImage, "rb") as image_file:
                    image_data = image_file.read()

                im_b64 = base64.b64encode(image_data).decode("utf8")
                param={
                    "image": im_b64,
                    "uid": str(MorphingParam["uid"]),
                    "cycle": str(MorphingParam["cycle"]),
                    "engine": CredParam["engine"],
                }   

    #            if CredParam["isGateway"]==True:
    #                _uploadImageToGateway(_origin, param)

                if CredParam["isGateway"]==False:
                    _uploadImageToOSAIS(_origin, param)
    return objRes

## ------------------------------------------------------------------------
#       Init processing
## ------------------------------------------------------------------------

## PUBLIC - resetting who this AI is talking to (OSAIS prod and dbg)
def osais_resetOSAIS(_location):
    global gOriginOSAIS
    gOriginOSAIS=_location
    return True

## PUBLIC - Init the Virtual AI
def osais_initializeAI(_envFile, _envSecret):
    global gIsDocker
    global gIsDebug
    global gIsLocal
    global gIsVirtualAI
    global gUsername
    global gName
    global gPortAI
    global gVersion
    global gPortGateway
    global gPortLocalOSAIS
    global gIPLocal
    global gExtIP
    global gOriginGateway
    global gVAIAuthToken
    global gOriginOSAIS
    global gClientAuthToken
    global gAITunel

    ## load env 
    obj=osais_getEnv(_envFile)
    obj2=osais_getEnv(_envSecret)
    gIsLocal=obj["isLocal"]
    gIsVirtualAI=obj["isVirtualAI"]
    gUsername=obj["username"]
    gName=obj["name"]

    ## from env, load AI config
    gConfig=osais_loadConfig(gName)
    gPortAI = gConfig["port"]
    gVersion = gConfig["version"]

    ## try to create a tunnel
    gAITunel=create_tunnel(gPortAI)

    ## make sure we have a config file
    _loadConfig(gName)

    ## where is OSAIS for us?
    ## we set OSAIS location in all cases (even if in gateway) because this AI can generate it s own page for sending reqs (needs a client logged into OSAIS)
    if gIsDebug==False:
        osais_resetOSAIS("https://opensourceais.com/")
    
    if gIsVirtualAI:
        try:
            osais_authenticateAI()
        except Exception as err:
            print("=> CRITICAL: Could not connect virtual AI "+gName+ " to OSAIS")
            return None
    
    if gIsLocal:
        try:
            ## where is the Gateway for us? 
            osais_resetGateway()
        except Exception as err:
            print("CRITICAL: could not notify Gateway at "+gOriginGateway)
            return None

    dataClient=authenticateClientAsDemo()

    ## init default cost
    _initializeCost()

    ## output the config we are runing on
    print("\r\n<===== Config =====>\r\n")
    print("=> engine:                  "+str(gName) + " v"+str(gVersion))
    if gIsDocker:
        print("=> in Docker:               True")
    else:
        print("=> in Docker:               False")
    print("=> is Debug:                "+str(gIsDebug))
    print("=> OSAIS:                   "+str(gOriginOSAIS))
    print("\r\n=> is Local:                "+str(gIsLocal))
    if gIsLocal:
        print(" > gateway:                 "+gOriginGateway)
        print(" > AI location:             "+str(gIPLocal)+":"+str(gPortAI))
        if gAITunel!=None:
            print(" > AI tunnel :              "+gAITunel)
    print("\r\n=> is Virtual:              "+str(gIsVirtualAI))
    if gIsVirtualAI:
        print(" > virtAI location (ext.):  "+str(gExtIP)+":"+str(gPortAI))
        print(" > OSAIS location:          "+gOriginOSAIS)
        if gVAIAuthToken!=None:
            print(" > is connected to OSAIS:   True")
        else:
            print(" > is connected to OSAIS:   False")
    if gClientAuthToken!=None:
        print("\r\n=> is connected as Client:  True")
        print(" > client ID:               "+dataClient["data"]["token"])
    else:
        print("\r\n=> is connected as Client:  False")
    print("\r\n=> Pay to owner:            "+str(gUsername))
    print("\r\n<===== /Config =====>\r\n")

    return {
        "engine":gName,
        "client": dataClient["data"]
    }

## ------------------------------------------------------------------------
#       Starting point of Lib
## ------------------------------------------------------------------------

# Multithreading for observers
watch_directory=start_observer_thread(_getOutputDir(), osais_onNotifyFileCreated, None)     

#cleaning dir every 10min
schedule.every(10).minutes.do(_clearDir)

#login into OSAIS as client every 24h
schedule.every(3600).minutes.do(authenticateClientAsDemo)

#login as VAI every 24h +1min
schedule.every(3601).minutes.do(osais_authenticateAI)

print("\r\n=> Python OSAIS Lib is loaded...")