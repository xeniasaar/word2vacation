import streamlit as st

# Add this line to prevent unnecessary re-execution on every reload
st.set_page_config(layout="wide")

# Define a function that takes input from sliders and performs some computation
def process_data(input1, input2):
    # Perform computation based on the slider inputs
    result = input1 * input2  # Replace this with your own computation logic

    # Return the result
    return result

# Create sliders for input parameters
input1 = st.slider('Input 1', min_value=0, max_value=10, value=5)
input2 = st.slider('Input 2', min_value=0, max_value=10, value=5)

# Run the function with the slider inputs
output = process_data(input1, input2)

# Display the output
st.write('Output:', output)

if __name__ == "__main__":
    # Add the `--server.port $PORT` argument to run on the correct port for GitHub Pages
    st.server.run(port=$PORT)