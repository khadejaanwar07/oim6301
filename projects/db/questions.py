import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _():
    from datetime import date

    as_of = date(2026, 11, 1)
    return (as_of,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B: Babson Bean Café

    ## 1. Business Questions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 1: What were the three best-selling products last month?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            p.name AS product,
            SUM(ol.quantity) AS units_sold
        FROM order_lines ol
        JOIN products p
            ON ol.product_id = p.product_id
        JOIN orders o
            ON ol.order_id = o.order_id
        WHERE o.ordered_at >= DATE_TRUNC('month', DATE '{as_of}') - INTERVAL '1 month'
          AND o.ordered_at < DATE_TRUNC('month', DATE '{as_of}')
        GROUP BY p.name
        ORDER BY units_sold DESC
        LIMIT 3
    """)# Question 1: What were the three best-selling products last month?
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In October 2026, Flat White and Croissant were the best-selling products with 27 units each, followed by Cappuccino with 25 units sold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 2: What are the revenue, cost and margin for each menu category?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH product_totals AS (
            SELECT
                p.category,
                SUM(ol.quantity * ol.unit_price) AS revenue,
                SUM(ol.quantity * p.cost) AS cost
            FROM order_lines ol
            JOIN products p ON ol.product_id = p.product_id
            GROUP BY p.category
        ),
        option_totals AS (
            SELECT
                p.category,
                SUM(ol.quantity * lo.price_charged) AS revenue,
                SUM(ol.quantity * opt.cost) AS cost
            FROM line_options lo
            JOIN order_lines ol ON lo.line_id = ol.line_id
            JOIN products p ON ol.product_id = p.product_id
            JOIN options opt ON lo.option_id = opt.option_id
            GROUP BY p.category
        )
        SELECT
            pt.category,
            pt.revenue + COALESCE(ot.revenue, 0) AS total_revenue,
            pt.cost + COALESCE(ot.cost, 0) AS total_cost,
            pt.revenue + COALESCE(ot.revenue, 0)
                - pt.cost - COALESCE(ot.cost, 0) AS margin
        FROM product_totals pt
        LEFT JOIN option_totals ot ON pt.category = ot.category
        ORDER BY margin DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Coffee generated the highest revenue at $10,914.26 and the highest margin at $7,164.45, followed by food with a margin of $4,058.21, tea at $2,840.01 and other products at $885.87. These figures include add-on revenue and costs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 3: Which loyalty members spend more than the average member?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH line_totals AS (
            SELECT
                ol.order_id,
                ol.line_id,
                ol.quantity * ol.unit_price
                    + ol.quantity * COALESCE(
                        SUM(lo.price_charged), 0
                    ) AS line_total
            FROM order_lines ol
            LEFT JOIN line_options lo
                ON ol.line_id = lo.line_id
            GROUP BY
                ol.order_id,
                ol.line_id,
                ol.quantity,
                ol.unit_price
        ),
        order_totals AS (
            SELECT
                order_id,
                SUM(line_total) AS order_total
            FROM line_totals
            GROUP BY order_id
        ),
        member_totals AS (
            SELECT
                m.member_id,
                m.first_name,
                COUNT(o.order_id) AS number_of_orders,
                COALESCE(SUM(ot.order_total), 0) AS total_spent
            FROM members m
            LEFT JOIN orders o
                ON m.member_id = o.member_id
            LEFT JOIN order_totals ot
                ON o.order_id = ot.order_id
            GROUP BY m.member_id, m.first_name
        )
        SELECT
            member_id,
            first_name,
            number_of_orders,
            ROUND(total_spent, 2) AS total_spent,
            ROUND(
                total_spent / NULLIF(number_of_orders, 0), 2
            ) AS average_order
        FROM member_totals
        WHERE total_spent > (
            SELECT AVG(total_spent)
            FROM member_totals
        )
        ORDER BY total_spent DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Out of 50 loyalty members, 30 spent more than the average member. Member19 spent the most at $621.54 across 27 orders, followed by Member6 at $578.48 and Member40 at $556.35
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 4: Do all orders have payments that match their total?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH product_totals AS (
            SELECT
                order_id,
                SUM(quantity * unit_price) AS product_total
            FROM order_lines
            GROUP BY order_id
        ),
        option_totals AS (
            SELECT
                ol.order_id,
                SUM(ol.quantity * lo.price_charged) AS option_total
            FROM order_lines ol
            JOIN line_options lo ON ol.line_id = lo.line_id
            GROUP BY ol.order_id
        ),
        payment_totals AS (
            SELECT
                order_id,
                SUM(amount) AS payment_total
            FROM payments
            GROUP BY order_id
        )
        SELECT
            o.order_id,
            pt.product_total + COALESCE(ot.option_total, 0)
                AS order_total,
            pay.payment_total,
            pay.payment_total -
                (pt.product_total + COALESCE(ot.option_total, 0))
                AS difference
        FROM orders o
        JOIN product_totals pt ON o.order_id = pt.order_id
        LEFT JOIN option_totals ot ON o.order_id = ot.order_id
        LEFT JOIN payment_totals pay ON o.order_id = pay.order_id
        WHERE pay.payment_total IS NULL
           OR ABS(pay.payment_total -
               (pt.product_total + COALESCE(ot.option_total, 0))) > 0.001
        ORDER BY o.order_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Out of 1,200 orders, two had payment totals that did not match their purchase amounts. Order 1 had a total of $6.33 but payments of $7.33, while Order 2 had a total of $29.98 but payments of $30.98. Both were overpaid by $1.00, matching the errors I intentionally added in make_data.py.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 5: Which loyalty members have never placed an order?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            m.member_id,
            m.first_name,
            m.join_date
        FROM members m
        LEFT JOIN orders o
            ON m.member_id = o.member_id
        WHERE o.order_id IS NULL
        ORDER BY m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Five loyalty members have never placed an order: Member46, Member47, Member48, Member49 and Member50. All five joined the loyalty program in 2025 but have not made a purchase.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 6: What percentage of orders were paid at least partly with loyalty points each month?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            STRFTIME(o.ordered_at, '%Y-%m') AS month,
            COUNT(*) AS total_orders,
            COUNT(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM payments p
                    WHERE p.order_id = o.order_id
                      AND p.method = 'points'
                )
            ) AS orders_using_points,
            ROUND(
                100.0 * COUNT(*) FILTER (
                    WHERE EXISTS (
                        SELECT 1
                        FROM payments p
                        WHERE p.order_id = o.order_id
                          AND p.method = 'points'
                    )
                ) / COUNT(*),
                2
            ) AS points_percentage
        FROM orders o
        WHERE o.ordered_at <= DATE '{as_of}'
        GROUP BY STRFTIME(o.ordered_at, '%Y-%m')
        ORDER BY month
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The share of orders paid at least partly with loyalty points varied by month. July 2026 had the highest share at 50.52%, with 49 out of 97 orders using points. In comparison, May 2026 had a lower share of 36.46%. This shows that loyalty point usage fluctuated throughout the year.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 7: Which products have not sold in the last 60 days?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            p.product_id,
            p.name,
            p.category,
            p.available_today
        FROM products p
        WHERE NOT EXISTS (
            SELECT 1
            FROM order_lines ol
            JOIN orders o
                ON ol.order_id = o.order_id
            WHERE ol.product_id = p.product_id
              AND o.ordered_at >= DATE '{as_of}' - INTERVAL '60 days'
              AND o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        )
        ORDER BY p.name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. How I Know These Numbers Are Right
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Working With the Agent
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Reading It Back

    Prediction: Question 2

    I chose Question 2, which calculates revenue, cost and margin by product category using the PRODUCTS, ORDER_LINES and LINE_OPTIONS tables.

    I have 2,405 order lines and 2,122 line options. I predict the joins will produce around 3,500 rows before grouping. I'm using a LEFT JOIN because some order lines have multiple add-ons while others have none. This means every order line will appear at least once, and lines with multiple add-ons will appear more than once.

    I'll compare my prediction with the actual number of rows and explain any difference.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Going Further
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Time Spent
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
