from Main import sqlConnector
from Main.Notification import show_notification


def generate_monthly_summary(store_id, month, year):
    if not store_id or not month or not year:
        show_notification("Store ID, month, and year are required.")
        return
    print(store_id, month, year)
    try:
        # Start transaction
        sqlConnector.connect("START TRANSACTION", ())

        # Query to calculate total withdrawals
        query_withdraw = """SELECT SUM(amount) AS total_withdraw
            FROM withdraw
            WHERE store_id = %s AND MONTH(withdraw_date) = %s AND YEAR(withdraw_date) = %s
        """
        result_withdraw = sqlConnector.connect(query_withdraw, (store_id, month, year))
        total_withdraw = result_withdraw[0][0] if result_withdraw and result_withdraw[0][0] is not None else 0
        print("total_withdraw", total_withdraw)

        # Query to calculate total expenses
        query_expenses = """SELECT SUM(amount) AS total_expenses
            FROM expense
            WHERE store_id = %s AND MONTH(expense_date) = %s AND YEAR(expense_date) = %s
        """
        result_expenses = sqlConnector.connect(query_expenses, (store_id, month, year))
        total_expenses = result_expenses[0][0] if result_expenses and result_expenses[0][0] is not None else 0
        print("total_expenses", total_expenses)

        # Query to calculate total merchandise
        query_merchandise = """SELECT SUM(Merch_Value) AS total_merchandise
            FROM merchandise
            WHERE StoreID = %s AND MONTH(Purchase_Date) = %s AND YEAR(Purchase_Date) = %s
        """
        result_merchandise = sqlConnector.connect(query_merchandise, (store_id, month, year))
        total_merchandise = result_merchandise[0][0] if result_merchandise and result_merchandise[0][0] is not None else 0
        print("total_merchandise", total_merchandise)

        # Query to calculate total cash_in_envelope
        query_cash = """SELECT SUM(cash_in_envelope) AS total_cash
            FROM employee_close
            WHERE store_id = %s AND MONTH(timestamp) = %s AND YEAR(timestamp) = %s
        """
        result_cash = sqlConnector.connect(query_cash, (store_id, month, year))
        total_cash = result_cash[0][0] if result_cash and result_cash[0][0] is not None else 0
        print("total_cash", total_cash)

        # Query to calculate total payroll
        query_payroll = """SELECT SUM(total_payment) AS total_payroll
            FROM Payroll
            WHERE store_id = %s AND MONTH(timeofDate) = %s AND YEAR(timeofDate) = %s
        """
        result_payroll = sqlConnector.connect(query_payroll, (store_id, month, year))
        total_payroll = result_payroll[0][0] if result_payroll and result_payroll[0][0] is not None else 0
        print("total_payroll", total_payroll)

        # Query to calculate total credit
        query_credit = """SELECT SUM(credit) AS total_credit
            FROM employee_close
            WHERE store_id = %s AND MONTH(timestamp) = %s AND YEAR(timestamp) = %s
        """
        result_credit = sqlConnector.connect(query_credit, (store_id, month, year))
        total_credit = result_credit[0][0] if result_credit and result_credit[0][0] is not None else 0
        print("total_credit", total_credit)

        # Calculate cash_and_credit
        cash_and_credit = total_cash + total_credit
        print("cash_and_credit", cash_and_credit)

        # Calculate actual_cash
        actual_cash = total_cash - total_payroll
        print("actual_cash", actual_cash)

        # Calculate actual_credit
        actual_credit = total_credit - (total_expenses + total_merchandise)
        print("actual_credit", actual_credit)

        # Check if a record exists in the summary table
        check_query = """SELECT COUNT(*) FROM summary
                              WHERE store_id = %s AND month = %s AND year = %s"""
        record_exists = sqlConnector.connect(check_query, (store_id, month, year))[0][0] > 0

        if record_exists:
            # Update the existing record
            print("record exists")
            update_query = """UPDATE summary
                              SET total_withdraw = %s, total_expenses = %s, total_merchandise = %s,
                                  cash_and_credit = %s, total_payroll = %s, actual_cash = %s, actual_credit = %s
                              WHERE store_id = %s AND month = %s AND year = %s"""
            sqlConnector.connect(update_query, (total_withdraw, total_expenses, total_merchandise,
                                                cash_and_credit, total_payroll, actual_cash, actual_credit, store_id, month, year))
        else:
            # Insert a new record
            insert_query = """INSERT INTO summary (store_id, month, year, total_withdraw, total_expenses,
                                                   total_merchandise, cash_and_credit, total_payroll, actual_cash, actual_credit)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            sqlConnector.connect(insert_query, (store_id, month, year, total_withdraw, total_expenses,
                                                total_merchandise, cash_and_credit, total_payroll, actual_cash, actual_credit))

        # Commit transaction
        sqlConnector.connect("COMMIT", ())
        show_notification("Monthly summary generated successfully.")

    except Exception as e:
        # Rollback transaction in case of an error
        sqlConnector.connect("ROLLBACK", ())
        show_notification(f"An error occurred while generating the summary: {str(e)}")