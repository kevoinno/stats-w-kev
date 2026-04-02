import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import statsmodels.formula.api as smf
    import matplotlib.pyplot as plt

    return mo, np, pd, plt, smf


@app.cell
def _(np):
    np.random.seed(67) # setting seed for reproducibility
    return


@app.cell
def _(np, pd, plt):
    def simulate_data(n = 50000, # number of customers in the A/A test
                      avg_spend = 20, # average spend for a normal customer
                      big_back_spend = 10, # average additional spend for a big back customer
                      broken = False): # whether the A/A test should show a "broken results"
        # simulate customer type
        is_big_back = np.random.choice(a = [0, 1], size = n, p = [0.7, 0.3]) # 30% of customers are big backs
        # simulate spend for each customer
        spend = avg_spend + (big_back_spend * is_big_back) + np.random.normal(loc = 0, scale = 2)
        # assign probabilities to being in class 1
        base_probs = np.repeat(a = 0.5, repeats = n)
        if broken:
            probs = np.where(is_big_back, 0.7, 0.5) # big backs are more likely to be in button 1
        else:
            probs = base_probs
        # assign to 1st red button or 2nd red button
        has_button_1 = np.random.binomial(np.repeat(1, n), p = probs)

        df = pd.DataFrame(
            {
                'is_big_back' : is_big_back,
                'spend' : spend,
                'has_button_1' : has_button_1 # button 1 = 1, button 2 = 0
            }
        )

        df['customer_id'] = df.index
        df_reordered = df[['customer_id', 'is_big_back', 'spend', 'has_button_1']]

        return df_reordered

    def balance_chart(df):
        counts = df.groupby(['has_button_1', 'is_big_back']).size().unstack(fill_value=0)
        proportions = counts.div(counts.sum(axis=1), axis=0).loc[[1, 0]]

        fig, ax = plt.subplots()
        x = np.arange(len(proportions))
        width = 0.35

        ax.bar(x - width/2, proportions[0], width, label='Normal Customer')
        ax.bar(x + width/2, proportions[1], width, label='Big Back Customer')

        ax.set_xticks(x)
        ax.set_xticklabels(['Button 1', 'Button 2'])
        ax.set_xlabel('Group')
        ax.set_ylabel('Proportion of Customers')
        ax.set_title('Balance Check: Customer Type by Button Group')
        ax.legend()

        return fig

    def plot_ci(results):
        ci = results.conf_int().drop('Intercept')
        estimates = results.params.drop('Intercept')

        fig, ax = plt.subplots()
        y = np.arange(len(estimates))

        ax.errorbar(estimates, y,
                    xerr=[estimates - ci[0], ci[1] - estimates],
                    fmt='o', capsize=5)
        ax.axvline(x=0, linestyle='--', color='red', linewidth=1)
        ax.set_yticks(y)
        ax.set_yticklabels(estimates.index)
        ax.set_xlabel('Coefficient Estimate')
        ax.set_title('95% Confidence Intervals')

        return fig

    return balance_chart, plot_ci, simulate_data


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Data

    We are simulating the results of an A/A test.

    Imagine we are testing whether changing "Order Online" button from red to yellow will increase average monthly customer spend. Before we run an A/B test, we want to check whether our results will be trustworthy using an A/A test.

    Our simulated dataset will have the following columns:

    |Column|Definition|
    |------|----------|
    |customer_id| id for the customer that is spending|
    |is_big_back| 0 = normal customer, 1 = big back customer (spends more on average)|
    |spend| monthly spend of the given customer|
    |has_button_1| group that the customer is assigned to. 0 = red button #2, 1 = red button #1|

    Think of `has_button_1` as a variable that specifies whether the user is in the treated or control group. In an A/A test, these groups are shown the same button.
    """)
    return


@app.cell
def _(simulate_data):
    broken_data = simulate_data(broken = True) # broken A/A test
    normal_data = simulate_data(broken = False) # A/A test
    print(f"Preview of the data:")
    print(broken_data.head())
    return broken_data, normal_data


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Simulation of a broken A/A test

    Below, we simulate what our results might be if something in our A/B testing is breaking the random assignment of customers to each button group.

    In this case, the pipeline is broken because it is assigning "big back" customers to the button 1 more often than button 2.
    """)
    return


@app.cell
def _(balance_chart, broken_data):
    balance_chart(broken_data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As a result, we notice that the average monthly customer spend for button 1 is significantly higher than button 2. This doesn't make sense though, because button 1 and 2 are both the same red button!
    """)
    return


@app.cell
def _(broken_data, smf):
    # run broken a/a test
    model = smf.ols('spend~has_button_1', data = broken_data).fit()
    res = model.summary()
    print(res)
    return (model,)


@app.cell
def _(model, plot_ci):
    plot_ci(model)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Simulation of an expected A/A test result

    If the customers were truly randomly assigned to button 1 or 2, we would have a correct A/B testing pipeline.

    The button 1 group is now comparable to the button 2 group, containing the same proportion of big backs.
    """)
    return


@app.cell
def _(balance_chart, normal_data):
    balance_chart(normal_data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since the the button 1 and button 2 groups are comparable and they are shown the same red button, we expect do not expect a significant effect when we do a t-test.

    This is evidence that our A/B testing system is working properly and we are ready to run an actual A/B test now!
    """)
    return


@app.cell
def _(normal_data, smf):
    # run a/a test with correct results
    normal_model = smf.ols('spend~has_button_1', data = normal_data).fit()
    normal_res = normal_model.summary()
    print(normal_res)
    return (normal_model,)


@app.cell
def _(normal_model, plot_ci):
    plot_ci(normal_model)
    return


if __name__ == "__main__":
    app.run()
