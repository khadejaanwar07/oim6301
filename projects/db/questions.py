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

    ##  Business Questions
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
    In October 2026, Mocha was the best-selling product with 35 units sold, followed by Drip Coffee with 33 units and Blueberry Muffin with 30 units.
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
                SUM(ps.revenue) AS revenue,
                SUM(ps.units_sold * p.cost) AS cost
            FROM product_sales ps
            JOIN products p
                ON ps.product_id = p.product_id
            GROUP BY p.category
        ),
        option_totals AS (
            SELECT
                p.category,
                SUM(ol.quantity * lo.price_charged) AS revenue,
                SUM(ol.quantity * opt.cost) AS cost
            FROM line_options lo
            JOIN order_lines ol
                ON lo.line_id = ol.line_id
            JOIN products p
                ON ol.product_id = p.product_id
            JOIN options opt
                ON lo.option_id = opt.option_id
            GROUP BY p.category
        )
        SELECT
            p.category,
            ROUND(COALESCE(pt.revenue, 0)
                + COALESCE(ot.revenue, 0), 2) AS total_revenue,
            ROUND(COALESCE(pt.cost, 0)
                + COALESCE(ot.cost, 0), 2) AS total_cost,
            ROUND(
                COALESCE(pt.revenue, 0)
                + COALESCE(ot.revenue, 0)
                - COALESCE(pt.cost, 0)
                - COALESCE(ot.cost, 0),
                2
            ) AS margin
        FROM (
            SELECT DISTINCT category
            FROM products
        ) p
        LEFT JOIN product_totals pt
            ON p.category = pt.category
        LEFT JOIN option_totals ot
            ON p.category = ot.category
        ORDER BY margin DESC
    """)

  
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Coffee generated the highest revenue at $11,495.74 and the highest margin at $7,568.84, followed by food with a margin of $4,459.65 and tea at $2,937.79. The other category had no sales. I used the product_sales view from Part A to calculate product revenue and added the revenue and costs from options separately.
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
    Out of 50 loyalty members, 32 spent more than the average member. Member40 spent the most at $685.34 across 30 orders, followed by Member41 at $612.99 and Member29 at $601.24.
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
    Out of 1,200 orders, two had payment totals that did not match their purchase amounts. Order 1 had a total of $5.24 but payments of $6.24, while Order 2 had a total of $38.50 but payments of $39.50. Both were overpaid by $1.00, matching the errors I intentionally added in `make_data.py`.
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
        WHERE o.ordered_at < DATE '{as_of}' + INTERVAL '1 day'
        GROUP BY STRFTIME(o.ordered_at, '%Y-%m')
        ORDER BY month
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The share of orders paid at least partly with loyalty points varied by month. In May 2026, 54.17% of orders (52 out of 96) used loyalty points, compared with 36.47% in February 2026. This shows that loyalty point usage changed throughout the year.
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
    Bottled Water and Orange Juice had no sales in the 60-day period ending November 1, 2026. Both products are currently unavailable and had no recorded sales during that period.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 8: What is the average number of add-ons per order line for each coffee and tea product?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH options_per_line AS (
            SELECT
                ol.line_id,
                ol.product_id,
                COUNT(lo.option_id) AS number_of_options
            FROM order_lines ol
            LEFT JOIN line_options lo
                ON ol.line_id = lo.line_id
            GROUP BY ol.line_id, ol.product_id
        )
        SELECT
            p.name AS product,
            p.category,
            COUNT(opl.line_id) AS number_of_lines,
            ROUND(AVG(opl.number_of_options), 2) AS average_options
        FROM products p
        JOIN options_per_line opl
            ON p.product_id = opl.product_id
        WHERE p.category IN ('coffee', 'tea')
        GROUP BY p.product_id, p.name, p.category
        ORDER BY average_options DESC, p.name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Cold Brew had the highest average number of add-ons at 1.63 per order line, followed by Espresso at 1.61. Black Tea and Mocha both averaged 1.54 add-ons per line. These averages include orders where customers selected no add-ons.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Question 9: Which ordering channel generates more sales revenue?
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH line_totals AS (
            SELECT
                ol.order_id,
                ol.quantity * ol.unit_price
                    + ol.quantity * COALESCE(SUM(lo.price_charged), 0)
                    AS line_revenue
            FROM order_lines ol
            LEFT JOIN line_options lo
                ON ol.line_id = lo.line_id
            GROUP BY ol.order_id, ol.line_id,
                     ol.quantity, ol.unit_price
        ),
        order_revenue AS (
            SELECT
                order_id,
                SUM(line_revenue) AS revenue
            FROM line_totals
            GROUP BY order_id
        )
        SELECT
            o.channel,
            COUNT(*) AS total_orders,
            ROUND(SUM(r.revenue), 2) AS total_revenue,
            ROUND(AVG(r.revenue), 2) AS average_order_value
        FROM orders o
        JOIN order_revenue r ON o.order_id = r.order_id
        GROUP BY o.channel
        ORDER BY total_revenue DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counter orders generated more revenue at $12,522.14 compared with $12,252.95 from app orders, despite the app receiving more orders (609 versus 591). Counter orders also had a higher average value of $21.19 compared with $20.12 for app orders.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 10: Which day of the week has the highest average number of orders on days with sales?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        WITH daily_orders AS (
            SELECT
                CAST(ordered_at AS DATE) AS order_date,
                DAYNAME(ordered_at) AS day_of_week,
                COUNT(*) AS orders
            FROM orders
            WHERE ordered_at < DATE '{as_of}' + INTERVAL '1 day'
            GROUP BY order_date, day_of_week
        )
        SELECT
            day_of_week,
            COUNT(*) AS days_with_orders,
            SUM(orders) AS total_orders,
            ROUND(AVG(orders), 2) AS average_daily_orders
        FROM daily_orders
        GROUP BY day_of_week
        ORDER BY average_daily_orders DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tuesday had the highest average number of orders at 3.59 per day, followed by Wednesday at 3.58 and Monday at 3.55. Friday had the lowest average at 2.84 orders per day. These averages are based only on days when at least one order was recorded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH channel_revenue AS (
            SELECT SUM(amount) AS total
            FROM (
                SELECT
                    o.channel,
                    SUM(ol.quantity * ol.unit_price) AS amount
                FROM orders o
                JOIN order_lines ol ON o.order_id = ol.order_id
                GROUP BY o.channel

                UNION ALL

                SELECT
                    o.channel,
                    SUM(ol.quantity * lo.price_charged) AS amount
                FROM orders o
                JOIN order_lines ol ON o.order_id = ol.order_id
                JOIN line_options lo ON ol.line_id = lo.line_id
                GROUP BY o.channel
            )
        ),
        independent_total AS (
            SELECT
                (SELECT SUM(quantity * unit_price)
                 FROM order_lines)
                +
                (SELECT SUM(ol.quantity * lo.price_charged)
                 FROM order_lines ol
                 JOIN line_options lo ON ol.line_id = lo.line_id)
                AS total
        )
        SELECT
            ROUND(c.total, 2) AS channel_revenue,
            ROUND(i.total, 2) AS independent_revenue,
            ROUND(c.total - i.total, 2) AS difference,
            ABS(c.total - i.total) < 0.01 AS numbers_match
        FROM channel_revenue c
        CROSS JOIN independent_total i
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked Question 9 by calculating total revenue in two different ways. First, I added revenue from counter and app orders. Then I calculated revenue directly from the order lines and their add-ons. Both methods gave $24,775.09, with a difference of $0.00, which confirms that the revenue totals match.
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH order_amounts AS (
            SELECT
                o.order_id,
                COALESCE((
                    SELECT SUM(ol.quantity * ol.unit_price)
                    FROM order_lines ol
                    WHERE ol.order_id = o.order_id
                ), 0)
                +
                COALESCE((
                    SELECT SUM(ol.quantity * lo.price_charged)
                    FROM order_lines ol
                    JOIN line_options lo
                        ON ol.line_id = lo.line_id
                    WHERE ol.order_id = o.order_id
                ), 0) AS order_total,

                COALESCE((
                    SELECT SUM(p.amount)
                    FROM payments p
                    WHERE p.order_id = o.order_id
                ), 0) AS payment_total
            FROM orders o
        ),
        mismatches AS (
            SELECT order_id
            FROM order_amounts
            WHERE ABS(payment_total - order_total) > 0.001
        )
        SELECT
            COUNT(*) AS mismatches_found,
            2 AS expected_mismatches,
            STRING_AGG(CAST(order_id AS VARCHAR), ', '
                       ORDER BY order_id) AS order_ids,
            COUNT(*) = 2
            AND COUNT(*) FILTER (WHERE order_id IN (1, 2)) = 2
                AS check_passed
        FROM mismatches
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I also checked the payment mismatches from Question 4 using a separate calculation of each order's purchase total and payments. The query identified exactly two mismatches, Orders 1 and 2, which matches the errors I intentionally created in `make_data.py`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##  Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Initially, the agent generated order times randomly between 7 AM and 6 PM, which meant orders were almost evenly distributed throughout the day.

    When I plotted the orders by hour, I noticed that the pattern didn't seem realistic for a campus café. I would expect more customers in the morning and around lunchtime.

    I changed the code in make_data.py from random.randint() to random.choices() and assigned higher weights to the morning and lunch hours. I then regenerated the data and checked the chart again.

    The updated chart showed a clear morning peak around 9 AM and another busy period around 12 PM to 1 PM, which made more sense for the café.

    This change is visible in the ORDERS section of make_data.py, where the order hours are generated
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading It Back

     Prediction: Question 2

    This three-table join also helped me understand why calculating product revenue directly after joining LINE_OPTIONS could lead to double-counting. Therefore, in Question 2, I calculated product revenue and option revenue separately before combining them by category.
    """)
    return


@app.cell
def _(ask):
    ask("""
           SELECT COUNT(*) AS actual_joined_rows
    FROM products p
    JOIN order_lines ol
        ON p.product_id = ol.product_id
    LEFT JOIN line_options lo
        ON ol.line_id = lo.line_id
        """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I predicted that joining the PRODUCTS, ORDER_LINES and LINE_OPTIONS tables would produce around 3,500 rows. The actual result was 3,490 rows, which was only 10 fewer than my prediction.

    The number of rows increases because some order lines have multiple add-ons, so they appear more than once after the join. I used a LEFT JOIN to include order lines without add-ons.

    For Question 2, the final result has one row per menu category, showing total revenue, cost and margin. The query uses the `product_sales` view for product revenue and calculates add-ons separately to avoid counting product revenue more than once.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I wanted to see how loyalty point usage changed over time, so I created a chart showing the percentage of orders paid at least partly with points each month.
    """)
    return


@app.cell
def _(as_of, ask, mo):

    import altair as alt

    # Get monthly loyalty point usage
    points_data = ask(f"""
        SELECT
            STRFTIME(o.ordered_at, '%Y-%m') AS month,
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
       WHERE o.ordered_at < DATE '{as_of}'
        GROUP BY STRFTIME(o.ordered_at, '%Y-%m')
        ORDER BY month
    """)

    # Create a horizontal bar chart
    base = alt.Chart(points_data).encode(
        y=alt.Y(
            "month:O",
            title="Month",
            sort="ascending",
            axis=alt.Axis(
                labelFontSize=14,
                titleFontSize=16
            )
        ),
        x=alt.X(
            "points_percentage:Q",
            title="Orders Using Loyalty Points (%)",
            scale=alt.Scale(domain=[0, 60]),
            axis=alt.Axis(
                labelFontSize=14,
                titleFontSize=16
            )
        )
    )

    # Draw the bars
    bars = base.mark_bar(
        color="steelblue",
        size=20
    )

    # Display the percentage beside each bar
    labels = base.mark_text(
        align="left",
        baseline="middle",
        dx=5,
        fontSize=13
    ).encode(
        text=alt.Text(
            "points_percentage:Q",
            format=".2f"
        )
    )

    # Combine bars and labels
    points_chart = (
        (bars + labels)
        .properties(
            title=alt.TitleParams(
                text="Monthly Loyalty Point Usage",
                fontSize=18,
                anchor="middle"
            ),
            width=420,
            height=400
        )
    )

    # Display the chart in Marimo
    mo.ui.altair_chart(points_chart)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I created a chart to see how often customers used loyalty points throughout the year. Usage varied by month, with May 2026 reaching 54.17% compared with 36.47% in February. This made it easier to see how customer use of loyalty points changed over time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    14 hours
    """)
    return


if __name__ == "__main__":
    app.run()
