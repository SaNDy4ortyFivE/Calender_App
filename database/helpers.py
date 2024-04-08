from database import db_instance
from services.helpers import custom_logger

def fetch_from_db(sql_query: str, values: tuple):
    '''Fetches records from Database'''
    results = []
    try:
        custom_logger.logger.debug("[Helper]Fetching for query:" + sql_query)
        custom_logger.logger.debug("[Helper]Values for query:" + str(values))
        cur = db_instance.conn.cursor()
        if len(values) == 0:
            cur.execute(sql_query)
        else:
            cur.execute(sql_query, values)
        results = cur.fetchall()
    except Exception as e:
        custom_logger.logger.error("[Helper]Error occured when fetching records from Database:" + repr(e), exc_info=True)

    return results



def insert_new_record(sql_query: str, values: tuple):
    '''Inserts a new record into database'''
    record_inserted = False
    try:
        custom_logger.logger.debug("[Helper]Fetching for query:" + sql_query)
        cur = db_instance.conn.cursor()
        if len(values) == 0:
            cur.execute(sql_query)
        else:
            custom_logger.logger.debug("[Helper]Values for query:" + str(values))
            cur.execute(sql_query, values)
        custom_logger.logger.debug("[Helper]Record inserted into Database")
        record_inserted=True
    except Exception as e:
        custom_logger.logger.error("[Helper]Error occured when inserting new record into Database:" + repr(e), exc_info=True)
    return record_inserted



def insert_bulk_records(prepared_sql_query: str, values: list):
    '''Inserts records in bulk into database'''
    records_inserted = False
    try:
        custom_logger.logger.debug("[Helper]Fetching for query:" + prepared_sql_query)
        cur = db_instance.conn.cursor()
        for v in values:
            custom_logger.logger.debug("[Helper]Values for query:" + str(v))
            cur.execute(prepared_sql_query, v)
        custom_logger.logger.debug("[Helper]Records inserted into Database")
        records_inserted = True
    except Exception as e:
        custom_logger.logger.error("[Helper]Error occured when inserting multiple records into Database:" + repr(e), exc_info=True)
    return records_inserted



def commit_transactions():
    done = False
    try:
        custom_logger.logger.debug("Committing...")
        db_instance.conn.commit()
        custom_logger.logger.debug("Commit done...")
        done = True
    except Exception as e:
        custom_logger.logger.error("[Helper]Error occured during commit:" + repr(e), exc_info=True)
    return done