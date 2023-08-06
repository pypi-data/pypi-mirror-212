import pytest
from platinumtools.aws_classes.class_enhancement import *
from platinumtools.dda_constants import *




# def common_processor_using_mock():

#     publisher_credentials = {}
#     publisher_settings = {}

#     organizationDBProvider = MockOrganizationQuerier
#     publishingDBProvider = MockStagingDatabaseProviderWithChrome(credentials=publisher_credentials, settings=publisher_settings)
#     processor = BetterCommonProcessor(
#         job_parameters={"guid": "387a26ff-ceed-5015-a6c9-a2cad90329c0" },
#         organization_provider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider
#     ) # Should expect for transformation Strategies to be automatically updated

#     return processor

# # def test_picks_chrome_enhancement_instantiation(common_processor_using_mock):
# #     processor = common_processor_using_mock
# #     processor.runJobs() # Should also post at the Mock Database


# def test_picks_salesforce_enhancement():
    
#     organizationDBProvider = MockOrganizationQuerier
#     publishingDBProvider = MockStagingDatabaseProviderWithChrome(credentials={}, settings={})
#     processor = BetterCommonProcessor(
#         job_parameters={"guid": "f27ecb0c-975d-dbac-82af-152b68e89902" },
#         organization_provider=organizationDBProvider,
#         publishingDBProvider=publishingDBProvider
#     ) # Should expect for transformation Strategies to be automatically updated
    
#     processor.runJobs() # Should also post at the Mock Database


def test_picks_real_job():
    
    organizationDBProvider = MockOrganizationQuerier
    
    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "TABLENAME": "event",
        "GET_TABLENAME": "staging_events",
         "COLUMN_NAMES": [
                        "user_guid",
                        "timestamp_utc",
                        "application",
                        "operation",
                        "event_guid",
                        "organization_guid",
                        "staging_guid",
                        "source_type",
                        "connector_guid",
                        "version",
                        "organization_id",
                        "user_id",
                        "user_team_id",
                        "profile_id",
                        "user_timezone",
                        "timestamp_client_local",
                        "month_number",
                        "month_name",
                        "weekday_number",
                        "weekday_name",
                        "day",
                        "hour",
                        "minute",
                        "time_slot",
                        "week_number",
                        "date",
                        "operation_type",
                        "application_type",
                        "interface_type",
                        "work_hour_type",
                        "raw_details",
                        "start_time",
                        "end_time",
                        "duration",
                        "description",
                        "title",
                        "url",
                        "attachments",
                        "action_origin",
                        "span_guid",
                        "root_reference",
                        "root_start",
                        "root_end",
                        "root_duration"
                        ]

    }
    publishingDBProvider = PostgreSQLProvider(credentials=credentials, settings=settings)

    processor = BetterCommonProcessor(
        job_parameters={"guid": "55c38902-37ed-9207-be6f-443ab4e68172",
                       },
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    
    processor.runJobs() # Should also post at the Mock Database