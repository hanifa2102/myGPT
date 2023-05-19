import streamlit as st

def main():
    st.title("Button and Input Text Field Example")

    # Input text field
    text_input = st.text_input("Enter text")

    # Button to display entered text
    if st.button("Display Text"):
        if text_input:
            st.write("Entered text:", text_input)
        else:
            st.write("No text entered.")

if __name__ == "__main__":
    main()