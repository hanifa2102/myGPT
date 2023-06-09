import streamlit as st

def main():
    st.title("File Uploader and Input Text Field Example")

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file")

    # Input text field
    text_input = st.text_input("Enter some text")

    # Button to process uploaded file and entered text
    if st.button("Process"):
        if uploaded_file is not None:
            # Process the uploaded file
            st.write("Uploaded file:", uploaded_file.name)
            # Additional processing logic here...

        if text_input:
            # Process the entered text
            st.write("Entered text:", text_input)
            # Additional processing logic here...

if __name__ == "__main__":
    main()


# # Create the grid options
# grid_options_builder = GridOptionsBuilder.from_dataframe(df)
# grid_options_builder.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
# grid_options = grid_options_builder.build() 
#     # Render the AgGrid widget
# AgGrid(df, gridOptions=grid_options)