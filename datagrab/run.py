from datagrab.datasources.ebay import ebay_pipeline as ebay_pipeline

if __name__ == '__main__':
    ebay_pipeline.start_pipeline(delete_temp_files=False, ebay_page_reach=35)
