
from platinumtools.aws_classes.config_mapper_df import *
from platinumtools.aws_classes.class_helpers import *
from platinumtools.aws_classes.class_enhancement import *
from platinumtools.aws_classes.class_adapters import *
import json

sample_salesforce_raw_input = {
  "guid": "f27ecb0c-975d-dbac-82af-152b68e89902",
  "previous_guid": "91e52161-2a47-7ea4-8121-186f9b378e4a",
  "version": "1.0.0",
  "date": "2023-04-27 16:45:07",
  "connector_guid":"salesforce-testing-connector",
  "organization_guid": "123e4567-e89b-12d3-a456-client",
  "details": [
  {
    "Id": "a1k7c000001fqySAAQ",
    "Name": "0000043628",
    "OwnerId": "0055x00000C68rTAAR",
    "User__c": "0055x00000C68rTAAR",
    "sfid__c": "00Q7c00000Et2nGEAR",
    "Actor__c": "nwang@platinumfilings.com",
    "Object__c": "LEAD",
    "Activity__c": "UPDATE",
    "CreatedById": "0055x00000C68rTAAR",
    "Source_IP__c": "68.160.247.154",
    "ActionDate__c": "2023-04-27T20:11:10.000Z",
    "Description__c": "Peter Pan ()",
    "Record_Link__c": "<a href=\"/00Q7c00000Et2nGEAR\" target=\"_blank\">LEAD</a>",
    "SessionType__c": "Aura",
    "IsInteractive__c": True,
    "LastModifiedById": "0055x00000C68rTAAR"
  },
  {
    "Id": "a1k7c000001fqyTAAQ",
    "Name": "0000043632",
    "OwnerId": "0055x00000C68rTAAR",
    "User__c": "0055x00000C68rTAAR",
    "sfid__c": "00Q7c00000Et2nGEAR",
    "Actor__c": "nwang@platinumfilings.com",
    "Object__c": "LEAD",
    "Activity__c": "UPDATE",
    "CreatedById": "0055x00000C68rTAAR",
    "Source_IP__c": "68.160.247.154",
    "ActionDate__c": "2023-04-27T20:14:18.000Z",
    "Description__c": "Peter Pan ()",
    "Record_Link__c": "<a href=\"/00Q7c00000Et2nGEAR\" target=\"_blank\">LEAD</a>",
    "SessionType__c": "Aura",
    "IsInteractive__c": True,
    "LastModifiedById": "0055x00000C68rTAAR"
  },
  {
    "Id": "a1k7c000001fqyWAAQ",
    "Name": "0000043627",
    "OwnerId": "0055x00000C68rTAAR",
    "User__c": "0055x00000C68rTAAR",
    "sfid__c": "00Q7c00000Et2nGEAR",
    "Actor__c": "nwang@platinumfilings.com",
    "Object__c": "LEAD",
    "Activity__c": "UPDATE",
    "CreatedById": "0055x00000C68rTAAR",
    "Source_IP__c": "68.160.247.154",
    "ActionDate__c": "2023-04-27T20:09:28.000Z",
    "Description__c": "Peter Pan ()",
    "Record_Link__c": "<a href=\"/00Q7c00000Et2nGEAR\" target=\"_blank\">LEAD</a>",
    "SessionType__c": "Aura",
    "IsInteractive__c": True,
    "LastModifiedById": "0055x00000C68rTAAR"
  },
  {
    "Id": "a1k7c000001fqybAAA",
    "Name": "0000043629",
    "OwnerId": "0055x00000C68rTAAR",
    "User__c": "0055x00000C68rTAAR",
    "sfid__c": "00Q7c00000Et2nGEAR",
    "Actor__c": "nwang@platinumfilings.com",
    "Object__c": "LEAD",
    "Activity__c": "UPDATE",
    "CreatedById": "0055x00000C68rTAAR",
    "Source_IP__c": "68.160.247.154",
    "ActionDate__c": "2023-04-27T20:11:14.000Z",
    "Description__c": "Peter Pan ()",
    "Record_Link__c": "<a href=\"/00Q7c00000Et2nGEAR\" target=\"_blank\">LEAD</a>",
    "SessionType__c": "Aura",
    "IsInteractive__c": True,
    "LastModifiedById": "0055x00000C68rTAAR"
  },
  {
    "Id": "a1k7c000001fqycAAA",
    "Name": "0000043633",
    "OwnerId": "0055x00000C68rTAAR",
    "User__c": "0055x00000C68rTAAR",
    "sfid__c": "00Q7c00000Et2nGEAR",
    "Actor__c": "nwang@platinumfilings.com",
    "Object__c": "LEAD",
    "Activity__c": "UPDATE",
    "CreatedById": "0055x00000C68rTAAR",
    "Source_IP__c": "68.160.247.154",
    "ActionDate__c": "2023-04-27T20:14:21.000Z",
    "Description__c": "Peter Pan ()",
    "Record_Link__c": "<a href=\"/00Q7c00000Et2nGEAR\" target=\"_blank\">LEAD</a>",
    "SessionType__c": "Aura",
    "IsInteractive__c": True,
    "LastModifiedById": "0055x00000C68rTAAR"
  },
  {
    "Id": "a1k7c000001fqylAAA",
    "Name": "0000043631",
    "OwnerId": "0055x00000C68rTAAR",
    "User__c": "0055x00000C68rTAAR",
    "sfid__c": "00Q7c00000Et2nGEAR",
    "Actor__c": "nwang@platinumfilings.com",
    "Object__c": "LEAD",
    "Activity__c": "UPDATE",
    "CreatedById": "0055x00000C68rTAAR",
    "Source_IP__c": "68.160.247.154",
    "ActionDate__c": "2023-04-27T20:14:14.000Z",
    "Description__c": "Peter Pan ()",
    "Record_Link__c": "<a href=\"/00Q7c00000Et2nGEAR\" target=\"_blank\">LEAD</a>",
    "SessionType__c": "Aura",
    "IsInteractive__c": True,
    "LastModifiedById": "0055x00000C68rTAAR"
  },
  {
    "Id": "a1k7c000001fqyqAAA",
    "Name": "0000043634",
    "OwnerId": "0055x00000C68rTAAR",
    "User__c": "0055x00000C68rTAAR",
    "sfid__c": "00Q7c00000Et2nGEAR",
    "Actor__c": "nwang@platinumfilings.com",
    "Object__c": "LEAD",
    "Activity__c": "UPDATE",
    "CreatedById": "0055x00000C68rTAAR",
    "Source_IP__c": "68.160.247.154",
    "ActionDate__c": "2023-04-27T20:18:23.000Z",
    "Description__c": "Peter Pan ()",
    "Record_Link__c": "<a href=\"/00Q7c00000Et2nGEAR\" target=\"_blank\">LEAD</a>",
    "SessionType__c": "Aura",
    "IsInteractive__c": True,
    "LastModifiedById": "0055x00000C68rTAAR"
  }
],
  "hash_1": "d8298e88a929de23ab1bcb06f7a05d0e694f871fb15ef31800d8027d0f76a2ff",
  "hash_2": "3baea71e7edcb8b8aa4417fb640c0fa0d7f9791c8a2b17ca3f499d10f7a43dcd"
}

sample_chrome_raw_input = {
    'guid': '387a26ff-ceed-5015-a6c9-a2cad90329c0',
    'previous_guid': 'b5a496cb-8bfb-39fd-67f2-4d14feef1fa1',
    'version': "1.0.0",
    'date': "2023-05-12 17:50:00.026",
    'connector_guid': "chrome-extension-ddap-1",
    "organization_guid": "organization-1",
    "details":[
  {
    "url": "chrome://extensions/",
    "guid": "bcf17e37-a4b9-17b4-bed2-69aaf120f68c",
    "type": "tab-focus",
    "title": "Extensions",
    "domain": "extensions",
    "params": {},
    "duration": 2,
    "spanId": "3a2a3726-4985-7034-21de-175622df3ed7",
    "endTime": "2023-05-11T16:03:13.783Z",
    "incognito": False,
    "startTime": "2023-05-11T16:03:12.408Z",
    "timestamp": "2023-05-11T16:03:13.408Z"
  },
  {
    "url": "chrome://extensions/",
    "guid": "bcf17e37-a4b9-17b4-bed2-asd",
    "type": "tab-focus",
    "title": "Extensions",
    "domain": "extensions",
    "params": {},
    "duration": 1200,
    "spanId": "3a2a3726-4985-7034-21de-asd",
    "endTime": "2023-05-11T16:35:33.783Z",
    "incognito": False,
    "startTime": "2023-05-11T16:03:12.408Z",
    "timestamp": "2023-05-11T16:03:13.408Z"
  },
  {
    "id": 16,
    "url": "https://mazzzystar.github.io/images/2023-05-10/superCLUE.jpg",
    "guid": "0adeb6d2-c889-4592-0b46-e43e887e4d71",
    "mime": "image/jpeg",
    "type": "download",
    "state": "complete",
    "title": "The Leverage of LLMs for Individuals | TL;DR",
    "danger": "safe",
    "domain": "mazzzystar.github.io",
    "exists": True,
    "paused": False,
    "endTime": "2023-05-11T16:03:31.427Z",
    "fileSize": 72801,
    "filename": "C:\\Users\\NelsonWang\\Downloads\\guide\\superCLUE (2).jpg",
    "finalUrl": "https://mazzzystar.github.io/images/2023-05-10/superCLUE.jpg",
    "referrer": "https://mazzzystar.github.io/2023/05/10/LLM-for-individual/",
    "canResume": False,
    "incognito": False,
    "startTime": "2023-05-11T16:03:28.431Z",
    "timestamp": "2023-05-11T16:03:31.434Z",
    "totalBytes": 72801,
    "bytesReceived": 72801
  },
  {
    "url": "https://imgbb.com/",
    "guid": "cfe2aea7-dfdf-b8a7-1d55-c870e14fc203",
    "type": "upload",
    "files": [
      {
        "name": "iamge-.jpg",
        "size": 17292,
        "type": "image/jpeg",
        "lastModified": 1683577149679,
        "lastModifiedDate": "2023-05-08T20:19:09.679Z",
        "webkitRelativePath": ""
      }
    ],
    "title": "ImgBB — Upload Image — Free Image Hosting",
    "domain": "imgbb.com",
    "timestamp": "2023-05-11T16:01:02.290Z"
  }
],
    "hash_1": "d8298e88a929de23ab1bcb06f7a05d0e694f871fb15ef31800d8027d0f76a2ff",
    "hash_2": "3baea71e7edcb8b8aa4417fb640c0fa0d7f9791c8a2b17ca3f499d10f7a43dcd"
}

# Grab local json file named sample_windows
sample_widows_raw_input = {}



DEBUG = False


# def test_salesforce_enahncement_integration():
#     """Tests if things can be updated adapted then enhanced then published, no checks
#     """
#     organizationDBProvider = MockOrganizationQuerier
#     credentials = {}
#     settings = {}
#     publishingDBProvider = MockDatabaseProvider(credentials=credentials, settings=settings)

#     basic_enhancment = BasicEnhancement(
#         organizationDBProvider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider,
#         source_adapter=SalesforceAdapter(organizationQuerier=organizationDBProvider)
#     )

#     enhanced_events: dict["events": List[Event], "timeslots": List[Timeslot]] = basic_enhancment.transform(staging_events_events=sample_salesforce_raw_input)
#     # print(type(enhanced_events), enhanced_events)
#     # basic_enhancment.publish(enhanced_events=enhanced_events)
#     # basic_enhancment.publish(enhanced_events=enhanced_events["events"])
#     # basic_enhancment.publish(enhanced_events=enhanced_events["timeslots"])


def test_chrome_enhancment_integration():
  """Tests if the adapter can be used correctly
  """
  organizationDBProvider = MockOrganizationQuerier
  credentials = {}
  settings = {}
  publishingDBProvider = MockDatabaseProvider(credentials=credentials, settings=settings)

  basic_enhancment = BasicEnhancement(
      organizationDBProvider=organizationDBProvider,
      publishingDBProvider=publishingDBProvider,
      source_adapter=ChromeAdapter(organizationQuerier=organizationDBProvider)
  )

  enhanced_events: dict["events": List[Event], "timeslots": List[Timeslot]] = basic_enhancment.transform(staging_events_events=sample_chrome_raw_input)
  print(enhanced_events)
  # basic_enhancment.publish(enhanced_events=enhanced_events["events"])
  basic_enhancment.publish(enhanced_events=enhanced_events["timeslots"])

# def test_windows_enhancement_integration():
#   """Tests if Windows Adapter is used correctly
#   """
#   organizationDBProvider = MockOrganizationQuerier
#   credentials = {}
#   settings = {}
#   publishingDBProvider = MockDatabaseProvider(credentials=credentials, settings=settings)


#   # Open the JSON file
#   with open('sample_windows.json') as file:
#       # Load the JSON data into a variable
#       sample_windows_data = json.load(file)

#       basic_enhancment = BasicEnhancement(
#         organizationDBProvider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider,
#         source_adapter=WindowsAdapter(organizationQuerier=organizationDBProvider)
#       )
#       # Returns object of type: dict{event: List[Event], timeslot: List[Timeslot]}
#       enhanced_events: dict["events": List[Event], "timeslots": List[Timeslot]] = basic_enhancment.transform(staging_events_events=sample_windows_data)
#       # basic_enhancment.publish(enhanced_events=enhanced_events["events"])








