import config
import data_fetcher
import base64
import json
import pandas as pd
import datetime

global_logger = config.global_logger
config_object = config.config_object

data = []
data_processed = []

# Initialize dictionary for classification
ACTION_TYPE_DICT = data_fetcher.get_data_from_file(f"config/{config_object['CONFIGFILES']['classif_file']}")

# Create the dataframe with slots
def create_dataframe(data):
    global_logger.info('Creating dataframe')

    # Initialize Dataframe
    df = pd.DataFrame(columns=['Service', 'Start', 'Stop', 'Threat Type'])
    
    # Fill based on log data
    for log in data:
        # Decode base64 and parse
        log = parse_log(log) 
        
        service, start, stop, threat_type, resource, event_name = get_log_info(log)
        
        # Append row to DataFrame
        new_row = {'Service':service, 'Start':start, 'Stop':stop, 'Threat Type': threat_type}
        df.loc[len(df)] = new_row

    global_logger.info('Dataframe created')

    # Add action duration
    df['Duration'] = df['Stop'] - df['Start']

    # Reformat service
    df['Service_add'] = df['Service'].str.split('.').str[0]
    #df = df.assign(New_Service=df['Service'].str.split('.').str[0])
    
    df = df.sort_values("Start", axis = 0, ascending = True)
    return df


# Create a dictionary with the following structure for mindmap:
# dict(key=tuple(resource_name, service_name), value=dict(key=event_name, value=nb actions))
# example : {("MyS3bucket", "S3"): {GetObject: 42, PutObject: 55}, ("MyEC2VM", "EC2"): {StartInstance: 1, StopInstance: 2}}
def create_mindmap_dict(data):
    global_logger.info('Starting mindmap dict')
    mindmap_dict = {}
    for log in data:
        # Decode base64 and parse
        log = parse_log(log)

        # Fetch and parse logs
        service, start, stop, threat_type, resource_name, event_name = get_log_info(log)
        
        # Add a new key for resource
        if not ((resource_name, service) in mindmap_dict):
            mindmap_dict[(resource_name, service)] = {}
        
        # Add a new key for action
        if not (event_name in mindmap_dict[(resource_name, service)]):
            mindmap_dict[(resource_name, service)][event_name] = 0

        mindmap_dict[(resource_name, service)][event_name] += 1
    
    global_logger.info('Mindmap dict created')
    return mindmap_dict

# Decode base64 and parse
def parse_log(log):
    json_string = base64.b64decode(log['Payload']).decode('utf-8')
    return json.loads(json_string)

# Get the infos from the log
def get_log_info(log): 
    service = log['eventSource']
    start = parse_time(log['eventTime'])
    stop = start + datetime.timedelta(minutes=1)
    threat_type = classify_action(log['eventName'])
    
    if ('requestParameters' in log) and (log['requestParameters']):
        resource = get_resource(log['requestParameters'])
    else:
        resource = ''

    event_name = log['eventName']
    return service, start, stop, threat_type, resource, event_name


# Get the resource
# /!\ has not been tested for all services
def get_resource(request):
    tagstocheck = ['table', 'roleName', 'policyArn', 'functionName', 'bucketName', 'bucket', 'instanceId', 'tableName', 'roleArn', 'principalArn', \
        'trailName']
    for tag in tagstocheck:
        if tag in request:
            return request[tag]

    tagsinstancetocheck = ['snapshotSet', 'subnetSet', 'instanceSet', 'vpcSet', 'securityGroupIdSet']
    for tag in tagsinstancetocheck:
        if tag in request:
            if 'items' in request[tag]:
                return list(request[tag]['items'][0].values())[0]

    tagstoremove = ['maxRecords', 'maxResults', 'logGroupName', 'logGroupNamePrefix', 'nextToken', 'accountAttributeNameSet',\
             'limit', 'Host', 'keyId', 'dashboardName', 'InsightArn', 'checkIds', 'configurationARN', 'paginationToken', \
                'showSubscriptionDestinations', 'Type', 'Filter', 'filter', 'aggregateField', 'maxItems', \
                    'onlyAttached', 'language', 'map', 'endDate', 'FindingAggregatorArn', 'stackStatusFilter', 'stackName', \
                        'QueryString', 'scope', 'queryExecutionId', 'catalogId', 'crawlerNames', 'workGroup']
    for tag in tagstoremove:
        if tag in request:
            return ''

    data_fetcher.store_data_to_file("request_backup.json", str(request), True)
    
    return ''

# Time parsing
def parse_time(mytime):
    if type(mytime) == int:
        return datetime.datetime.fromtimestamp(mytime/1000)
    else:
        return datetime.datetime.strptime(mytime, '%Y-%m-%dT%H:%M:%SZ')

# Determine whether the action is a creation, modification of recon
def classify_action(action_type):
    for threat_type in ACTION_TYPE_DICT:
        for keyword in ACTION_TYPE_DICT[threat_type]:
            if keyword in action_type:
                return threat_type
    return 'Other'

 # Get user score based on actions made
def get_user_score():
    pass