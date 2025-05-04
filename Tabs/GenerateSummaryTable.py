from Main import sqlConnector
from Main.Notification import show_notification


def generate_monthly_summary(store_id, month, year):
    if not store_id or not month or not year:
        show_notification("Store ID, month, and year are required.")
        return
    print(store_id, month, year)
    try:
        # Query to calculate total withdrawals
        query = """SELECT SUM(amount) AS total_withdraw
            FROM withdraw
            WHERE store_id = %s AND MONTH(withdraw_date) = %s AND YEAR(withdraw_date) = %s
        """
        result = sqlConnector.connect(query, (store_id, month, year))
        total_withdraw = result[0][0] if result and result[0][0] is not None else 0
        print("total_withdraw",total_withdraw)

        # Check if a record exists in the summary table
        check_query = """SELECT COUNT(*) FROM summary
                              WHERE store_id = %s AND month = %s AND year = %s"""
        record_exists = sqlConnector.connect(check_query, (store_id, month, year))[0][0] > 0

        if record_exists:
            # Update the existing record
            print("record exists")
            update_query = """UPDATE summary
                              SET total_withdraw = %s
                              WHERE store_id = %s AND month = %s AND year = %s"""
            sqlConnector.connect(update_query, (total_withdraw, store_id, month, year))
        else:
            # Insert a new record
            insert_query = """INSERT INTO summary (store_id, month, year, total_withdraw)
                              VALUES (%s, %s, %s, %s)"""
            sqlConnector.connect(insert_query, (store_id, month, year, total_withdraw))

        show_notification("Monthly summary generated successfully.")

    except Exception as e:
        show_notification(f"An error occurred while generating the summary: {str(e)}")