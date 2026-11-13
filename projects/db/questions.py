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

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B: Babson Bean Café

    ## 1. Business Questions

    ## 2. How I Know These Numbers Are Right

    ## 3. Working With the Agent

    ## 4. Reading It Back

    ## 5. Going Further

    ## 6. Time Spent
    """)
    return


if __name__ == "__main__":
    app.run()
