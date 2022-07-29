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

A preview of the charts available:

https://user-images.githubusercontent.com/70349769/172089621-34f74cc0-edf6-49c3-b347-79b1cd0f133c.mov



## OLS

To run an OLS model, just select a non binary quanitative variable as the dependent variable.



https://user-images.githubusercontent.com/70349769/172089834-1cc61fa5-ad5f-4df8-a069-32175ea27d3b.mov



## Logistic Regression

To run a logistic model, select a binary quanitative variable as the dependent variable. 



https://user-images.githubusercontent.com/70349769/172089981-56229e03-cd67-4551-950a-503b47f9ec24.mov



## Errors

Currently, there is no means of displaying errors to the user. This means that if you tried performing an action and nothing occurred then there was an error. 

Over time I am hoping to fix this. 

Common Errors:
- Not uploading a dataset than can be read into a Pandas dataframe
  - if your data is not uploading then please try with a simple dataset like Iris to make sure the site works. If the problem still persists then make a post on discussions
- Selecting dependent variable as independent variable
- perfect collinearity for OLS
- perfect seperation for logit
