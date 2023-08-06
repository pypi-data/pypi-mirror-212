import json, requests

def getConfigPrabhu():
    ConfigData = {
        "configdata":
            {                    
                "app_url": {
                    "field_label": "Enter Application URL",
                    "datatype": "url",
                    "required": "yes",
                    "description": "app_url"
                },
                "user_type": {
                    "field_label": "Enter User Type",
                    "datatype": "text",
                    "required": "yes",
                    "description": "User Type"
                },
                "domain_name": {
                    "field_label": "Enter Domain name",
                    "datatype": "text",
                    "required": "yes",
                    "description": "Domain name"
                },                      
                "access_token": {
                    "field_label": "Enter Access Token",
                    "datatype": "text",
                    "required": "yes",
                    "description": "Access Token",                        
                },
                "get_unique_id":{
                    "field_label": "Enter Unique Identifier",
                    "datatype": "text",
                    "required": "yes",
                    "description": "To Perform Update and Delete record Operations",                        
                },
                "retry": {
                    "value": 3,
                    "field_label": "Enter Retry Connectivity",
                    "datatype": "int",
                    "required": "yes",
                    "description": "The number of retry connectivity"
                }
            }
        }
    
    return ConfigData