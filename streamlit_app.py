## sample 

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from datetime import datetime



st.title('Anna\'s first streamlit app')

st.header('Typical Python App')

DATE_COLUMN = 'order_date'
DATA_URL = ('https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv')

def load_data(nrows, DATA_URL):
    try: 
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        if DATE_COLUMN: 
                data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], format='%Y-%m-%d')
        return data
    except:
        raise ValueError('Failed to load URL')

## Load 10,000 rows of data into the dataframe.
data = load_data(100, DATA_URL)
## Notify the reader that the data was successfully loaded.
st.write('Data updated', datetime.now())

orders_by_latest_status = data.iloc[data.groupby(['id','user_id'])['order_date'].idxmax()]
     
b = (
   alt.Chart(orders_by_latest_status)
   .mark_bar()
   .encode(
            alt.Y('order_date', type='temporal', timeUnit='yearmonth', title='Order Month'),
            alt.X('user_id', type='quantitative', aggregate='distinct', title='Customers'),
            alt.Color('status', type='nominal', title='Latest Order Status')
        )
)

st.altair_chart(b)

python_version = '''
           
                DATE_COLUMN = 'order_date'
                DATA_URL = ('https://raw.githubusercontent.com/dbt-labs/jaffle_shop/main/seeds/raw_orders.csv')

                def load_data(nrows, DATA_URL):
                    try: 
                        data = pd.read_csv(DATA_URL, nrows=nrows)
                        lowercase = lambda x: str(x).lower()
                        data.rename(lowercase, axis='columns', inplace=True)
                        if DATE_COLUMN: 
                                data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], format='%Y-%m-%d')
                        return data
                    except:
                        raise ValueError('Failed to load URL')

                ## Load 10,000 rows of data into the dataframe.
                data = load_data(100, DATA_URL)
                ## Notify the reader that the data was successfully loaded.
                st.write('Data updated', datetime.now())

                orders_by_latest_status = data.iloc[data.groupby(['id','user_id'])['order_date'].idxmax()]
                    
                b = (
                alt.Chart(orders_by_latest_status)
                .mark_bar()
                .encode(
                            alt.Y('order_date', type='temporal', timeUnit='yearmonth', title='Order Month'),
                            alt.X('user_id', type='quantitative', aggregate='distinct', title='Customers'),
                            alt.Color('status', type='nominal', title='Latest Order Status')
                        )
                )

                st.altair_chart(b)

                '''

with st.expander("See Python code"):
    st.code(python_version, language='python')

st.header('A more flexible SQL deployment')

## OR do this with a database directly 

# Initialize connection.
conn = st.experimental_connection('snowflake', type='sql')

# Perform query.
df = conn.query('''

                WITH orders AS(

                    SELECT 
                        id as order_id,
                        user_id as customer_id,
                        MAX_BY(status, order_date) as latest_order_status, 
                        MAX(order_date) as latest_order_date
                    FROM RAW_ORDERS
                    GROUP BY ALL

                )

                SELECT
                    DATE_TRUNC('month', LATEST_ORDER_DATE)::date as month, 
                    latest_order_status, 
                    count(distinct order_id) as orders,
                    count(distinct customer_id) as customers
                FROM orders
                GROUP BY ALL
                ORDER BY 1

                ''', ttl=600)

# Print results.
c = (
   alt.Chart(df)
   .mark_bar()
   .encode(
            alt.Y('month', type='temporal', timeUnit='yearmonth', title='Order Month'),
            alt.X('customers', type='quantitative', title='Customers'),
            alt.Color('latest_order_status', type='nominal', title='Latest Order Status')
        )
)

st.altair_chart(c)

sql_version = '''

            ## OR do this with a database directly 

            # Initialize connection.
            conn = st.experimental_connection('snowflake', type='sql')

            # Perform query.
            df = conn.query(\'\'\'

                            WITH orders AS(

                                SELECT 
                                    id as order_id,
                                    user_id as customer_id,
                                    MAX_BY(status, order_date) as latest_order_status, 
                                    MAX(order_date) as latest_order_date
                                FROM RAW_ORDERS
                                GROUP BY ALL

                            )

                            SELECT
                                DATE_TRUNC('month', LATEST_ORDER_DATE)::date as month, 
                                latest_order_status, 
                                count(distinct order_id) as orders,
                                count(distinct customer_id) as customers
                            FROM orders
                            GROUP BY ALL
                            ORDER BY 1

                            \'\'\', ttl=600)

            # Print results.
            c = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                        alt.Y('month', type='temporal', timeUnit='yearmonth', title='Order Month'),
                        alt.X('customers', type='quantitative', title='Customers'),
                        alt.Color('latest_order_status', type='nominal', title='Latest Order Status')
                    )
            )

            st.altair_chart(c)
        '''

with st.expander("See Python + SQL code"):
    st.code(sql_version, language='python')