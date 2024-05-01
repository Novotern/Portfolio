import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.markdown("<h1 style='text-align:center;'>LOAN METRICS</h1>", unsafe_allow_html=True)

st.markdown("""<center>

# Interest Rate Spread

Interest Rate Spread is a fundamental measure used in the finance and banking industry to evaluate the profitability of lending activities. It represents the difference between the interest rate earned on loans extended by a financial institution and the interest rate paid on the deposits it holds or other funding sources.

Interest Rate Spread = Loan Interest Rate - Deposit Interest Rate

The interest rate spread is a crucial metric for assessing the profitability and efficiency of lending operations. A positive spread indicates that the institution is earning more from its loans than it is paying on its funding sources, resulting in net interest income. Conversely, a negative spread suggests that the institution may be paying out more in interest than it is earning from its loans, potentially leading to reduced profitability or losses.

Financial institutions carefully manage their interest rate spread to ensure that it is sufficient to cover operating expenses, credit risk, loan loss provisions, and provide an adequate return to shareholders. Changes in market interest rates, economic conditions, and regulatory policies can impact the interest rate spread, making it essential for institutions to monitor and adjust their lending practices accordingly.

</center>""", unsafe_allow_html=True)



data = pd.read_csv("data/loan_data.csv")

data['date']=pd.to_datetime(data['date'])
data['year']=data['date'].dt.year

# Initialize the figure
fig1 = go.Figure()

# Colors for differentiating each year's trend
colors = ['blue', 'red', 'green', 'purple']  # Add more colors if you have more than 4 years

# Adding a trace for each year
for i, (year, group) in enumerate(data.groupby('year')):
    fig1.add_trace(go.Scatter(
        x=group['month'], 
        y=group['interest_rate_spread'],
        mode='lines+markers',
        name=f'Interest Rate Spread {year}',
        line=dict(color=colors[i % len(colors)], width=2),
        marker=dict(size=7, color=colors[i % len(colors)], opacity=0.5)
    ))

# Update the layout
fig1.update_layout(
    title='<b>Interest Rate Spread Over Time</b>',
    xaxis_title='<b>Month</b>',
    yaxis_title='<b>Interest Rate Spread (%)</b>',
    template='seaborn'
)

with st.expander('Interest Rate Spread Over Time', True):
    st.plotly_chart(fig1, use_container_width=True)
    if st.checkbox('Show raw data', key=1):
        st.write(group[['month', 'interest_rate_spread']])
        
        

# Function to plot interest rate spread for a specific year or all years
def plot_interest_rate_spread(data, year='all'):
    # Ensure column names are lowercase
    data.columns = data.columns.str.lower()
    
    # Extract year from date if not already done
    if 'year' not in data.columns:
        data['year'] = data['date'].dt.year

    # Initialize the figure
    fig2 = go.Figure()

    # Define colors for differentiation
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'pink']  # Extend as needed

    if year == 'all':
        # Plot data for all years
        for i, (year, group) in enumerate(data.groupby('year')):
            fig2.add_trace(go.Scatter(
                x=group['month'], 
                y=group['interest_rate_spread'],
                text=group['interest_rate_spread'].round(2),
                mode='lines+markers+text',
                name=f'{year}',
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=7, color=colors[i % len(colors)], opacity=0.5),
                textposition="top center"
            ))
    else:
        # Plot data for the specified year
        group = data[data['year'] == year]
        fig2.add_trace(go.Scatter(
            x=group['month'], 
            y=group['interest_rate_spread'],
            text=group['interest_rate_spread'].round(2),
            mode='lines+markers+text',
            name=f'{year}',
            line=dict(color='blue', width=2),
            marker=dict(size=7, color='blue', opacity=0.5),
            textposition="top center"
        ))

    # Update the layout
    fig2.update_layout(
        title=f'Interest Rate Spread Over Time{" for Year " + str(year) if year != "all" else ""}',
        xaxis_title='Month',
        yaxis_title='Interest Rate Spread (%)',
        template='plotly_white'
    )

    # Show the figure
    # fig2.show()
    return fig2

# Example usage:
# plot_interest_rate_spread(data, year='all')  # To plot all years
# plot_interest_rate_spread(data, year=2023)    # To plot data for the year 2023

with st.expander('Distribution of Interest', True):
    year = st.selectbox('Year', [2020, 2021, 2022, 2023, 2024])
    if year:
        st.plotly_chart(plot_interest_rate_spread(data, year=year), use_container_width=True)
        
        
# Summary statistics
mean_spread = np.mean(data.interest_rate_spread)
median_spread = np.median(data.interest_rate_spread)
std_dev_spread = np.std(data.interest_rate_spread)

# Plotting histogram of interest rate spread
fig3 = px.histogram(x=data.interest_rate_spread, nbins=10, histnorm='probability density')
fig3.update_layout(title='Distribution of Interest Rate Spread',
                  xaxis_title='Interest Rate Spread (%)',
                  yaxis_title='Probability Density',
                  template='plotly_white')

# Add summary statistics annotations
fig3.add_annotation(x=mean_spread, y=0.1, text=f'Mean: {mean_spread:.2f}', showarrow=True, arrowhead=1, ax=-50, ay=-40)
fig3.add_annotation(x=median_spread, y=0.1, text=f'Median: {median_spread:.2f}', showarrow=True, arrowhead=1, ax=-50, ay=-60)
fig3.add_annotation(x=mean_spread+std_dev_spread, y=0.08, text=f'+1 Std Dev: {mean_spread+std_dev_spread:.2f}', showarrow=True, arrowhead=1, ax=-50, ay=-80)
fig3.add_annotation(x=mean_spread-std_dev_spread, y=0.08, text=f'-1 Std Dev: {mean_spread-std_dev_spread:.2f}', showarrow=True, arrowhead=1, ax=-50, ay=-80)

with st.expander('Distibution of Interest Rate Spread', True):
    st.plotly_chart(fig3, use_container_width=True)
    
fig4 = px.scatter(data, x='loan_volume', y='interest_rate_spread', color='year', trendline="ols", labels={'loan_volume':'Loan Volume', 'interest_rate_spread':'Interest Rate Spread', 'year': 'Year'})
fig4.update_traces(marker=dict(size=10, opacity=0.5))
fig4.update_layout(title='Relationship Between Loan Volume and Interest Rate Spread', template='plotly_white')

with st.expander('Relationship', True):
    st.plotly_chart(fig4, use_container_width=True)
    
    
# Calculate correlation between interest rate spread and unemployment rate
correlation_coefficient = np.corrcoef(data.interest_rate_spread, data.unemployment_rate)[0, 1]

# Plotting the relationship between interest rate spread and unemployment rate
num_months = 60
months = np.arange(1, num_months + 1)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=months, y=data.interest_rate_spread,
                         mode='lines+markers',
                         name='Interest Rate Spread',
                         line=dict(color='blue', width=2),
                         marker=dict(size=7, color='blue', opacity=0.5)))

fig5.add_trace(go.Scatter(x=months, y=data.unemployment_rate,
                         mode='lines',
                         name='Unemployment Rate',
                         line=dict(color='red', width=2, dash='dash')))

fig5.update_layout(title='Relationship Between Interest Rate Spread and Unemployment Rate',
                  xaxis_title='Months',
                  yaxis_title='Value',
                  template='plotly_white')

# Add correlation coefficient as annotation
fig5.add_annotation(x=0.9, y=0.9,
                   text=f'Correlation Coefficient: {correlation_coefficient:.2f}',
                   showarrow=False,
                   xref='paper', yref='paper',
                   font=dict(size=12, color='black'),
                   bgcolor='lightgrey',
                   opacity=0.8)

with st.expander('Interest Rate vs Umemployment', True):
    st.plotly_chart(fig5, use_container_width=True)