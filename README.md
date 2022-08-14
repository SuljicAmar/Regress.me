# Regress.me

[Regress.me](https://regress.me) is an easy to use data/model visualization tool powered by Python (Dash/Plotly). Simply upload a .csv file to get started. 

If you want to run the app locally run 

```python
  python client_app.py
```

## Visualizations 

There are 15 graphs available inlcuding
- Correlation matrix
- Scatter chart
- Bar chart
- Distribution chart
- Line chart
- Pie chart
- Scatter matrix
- Box plot
- Histogram
- 2D Contour
- 2D Histogram
- 3D Scatter chart
- 3D Line chart
- Surface plot
- Mesh grid

## OLS

To run an OLS model, just select a non binary quanitative variable as the dependent variable.

## Logistic Regression

To run a logistic model, select a binary quanitative variable as the dependent variable. 

## Errors

Common Errors:
- Not uploading a dataset than can be read into a Pandas dataframe
  - if your data is not uploading then please try with a simple dataset like Iris to make sure the site works. If the problem still persists then make a post on discussions
- Selecting dependent variable as independent variable
- perfect collinearity for OLS
- perfect seperation for logit
