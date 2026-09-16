import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
    freight_charges[[
      16.75,
      22.25,
      25.0,
      20.25,
      36.25]
    """,
    name="_"
)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
