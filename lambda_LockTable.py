# this little bit of python will connect to the dynamodb locktable table and spit out the 
# cluster, owner and lock time in a format that prometheus can read.
# we fake zip it in terraform so we don't have binary files sitting in github.
import boto3, json, time, datetime, re

def lambda_handler(event, content):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("LockTable")
    items = table.scan()['Items']
    result = []
    for item in items:
        result.append("LockTable"+json.dumps(item).replace(" ","") +" "+str(right_now)+'\n')
    http_result = ''.join(filter(str.isascii, result))
    string_cleanup = http_result.replace('"cluster"','cluster').replace('"owner"','owner').replace('"time"','time').replace(':','=')

    return {
        'statusCode': 200,
        'body': string_cleanup
    }
