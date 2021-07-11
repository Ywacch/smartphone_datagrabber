from datagrab.datasources.ebay import pipeline as ebay_pipeline

if __name__ == '__main__':
    ebay_pipeline.start_pipeline(delete_temp_files=False, send_mail=True, send_to_mongo=False)
