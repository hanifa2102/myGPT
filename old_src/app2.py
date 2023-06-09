import streamlit as st
import pandas as pd
from sqlalchemy import create_engine,text

# Create a SQLAlchemy engine
engine = create_engine("sqlite:///mydatabase.db")

def main():
    st.title("Streamlit App with SQLAlchemy and SQLite")

    # Get user input for DataFrame
    st.header("Enter DataFrame")
    csv_file = st.file_uploader("Upload CSV file", type="csv")
    if csv_file is not None:
        df = pd.read_csv(csv_file)

        # Display the DataFrame
        st.header("DataFrame")
        st.dataframe(df)

        # Save DataFrame to database
        if st.button("Save to Database"):
            try:
                df.to_sql("mytable", engine, if_exists="replace", index=False)
                st.success("DataFrame saved to database successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        if st.button('display db'):
            st.write(read_data_from_database())

def read_data_from_database():
    # Establish a connection
    with engine.connect() as connection:
        # Execute a SQL query and retrieve data
        query = text("SELECT * FROM mytable")
        result = connection.execute(query)

        # Convert the result to a Pandas DataFrame
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df

if __name__ == "__main__":
    main()

