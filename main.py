import streamlit as st
import requests

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "instance_url" not in st.session_state:
    st.session_state.instance_url = ""

if "current_step" not in st.session_state:
    st.session_state.current_step = "login"  # Current step: 'login', 'scenarios', or 'api_process'


# Function to reset authentication state
def reset_authentication():
    st.session_state.authenticated = False
    st.session_state.session_id = None
    st.session_state.instance_url = ""
    st.session_state.current_step = "login"


# Logout function
def logout():
    try:
        # Call the logout endpoint
        logout_endpoint = f"{st.session_state.instance_url}entity/auth/logout"
        response = requests.post(logout_endpoint, cookies={".ASPXAUTH": st.session_state.session_id})
        if response.status_code == 204:
            st.success("Logged out successfully!")
        else:
            st.error(f"Failed to log out. Error: {response.text}")
    except Exception as e:
        st.error(f"Error during logout: {str(e)}")
    reset_authentication()


# Top-right Logout Button
def top_right_logout():
    top_bar = st.container()
    with top_bar:
        cols = st.columns([8, 1])  # Adjust proportions for layout
        with cols[1]:
            if st.session_state.authenticated:
                if st.button("Logout"):
                    logout()


# Page: Authentication Collapsible Section
def login_section():
    with st.expander("Login", expanded=(st.session_state.current_step == "login")):
        st.title("Acumatica API Automation - Login")

        # Input fields for user credentials and URLs
        base_url = st.text_input("Enter Base URL (e.g., http://localhost/)", value="http://localhost/")
        instance_name = st.text_input("Enter Instance Name (e.g., AcumaticaDBTest1)")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        tenant = st.text_input("Tenant")

        # Construct instance URL dynamically
        if base_url and instance_name:
            st.session_state.instance_url = f"{base_url}{instance_name}/"
            st.write(f"Instance URL: `{st.session_state.instance_url}`")
        else:
            st.write("Please enter both Base URL and Instance Name.")

        # Endpoint for authentication
        if st.session_state.instance_url:
            auth_endpoint = f"{st.session_state.instance_url}entity/auth/"

            if st.button("Authenticate"):
                # Payload for authentication
                auth_payload = {
                    "name": username,
                    "password": password,
                    "company": tenant,
                }

                try:
                    # API request for authentication
                    response = requests.post(f"{auth_endpoint}login", json=auth_payload)
                    if response.status_code == 204:
                        st.success("Authentication Successful!")
                        st.session_state.session_id = response.cookies.get('.ASPXAUTH', '')
                        st.session_state.authenticated = True

                        # Print the Session ID
                        st.write(f"Session ID: `{st.session_state.session_id}`")

                        # Move to the next step
                        st.session_state.current_step = "scenarios"
                    else:
                        st.error(f"Authentication failed. Error: {response.text}")
                except Exception as e:
                    st.error(f"Error during authentication: {str(e)}")
        else:
            st.write("Instance URL is not defined. Please provide a valid Base URL and Instance Name.")


# Page: Scenario Selection Collapsible Section
def scenario_section():
    with st.expander("Select Scenario", expanded=(st.session_state.current_step == "scenarios")):
        st.title("Select a Scenario to Automate")

        # Mock: Fetch available scenarios (replace this with actual API call if available)
        scenarios = ["Scenario 1", "Scenario 2", "Scenario 3"]
        selected_scenario = st.selectbox("Select a Scenario", scenarios)

        if st.button("Run Scenario"):
            st.session_state.selected_scenario = selected_scenario
            st.session_state.current_step = "api_process"


# Page: API Process Details Collapsible Section
def api_process_section():
    with st.expander("API Process Details", expanded=(st.session_state.current_step == "api_process")):
        st.title("Scenario Execution Details")

        # Display session ID
        st.write(f"Session ID: `{st.session_state.session_id}`")
        st.write(f"Selected Scenario: `{st.session_state.get('selected_scenario', 'None')}`")

        # Mock API process steps (replace with actual endpoint calls)
        steps = ["Step 1: Process GLIS", "Step 2: Post Transactions", "Step 3: Finalize"]
        for step in steps:
            st.write(f"Processing: {step}...")
            st.progress(steps.index(step) + 1)
        st.success("Scenario completed successfully!")


# Main App Logic
def main():
    top_right_logout()  # Show logout button on the top-right corner

    # Collapsible Sections for each step
    login_section()

    if st.session_state.authenticated:
        scenario_section()

    if st.session_state.current_step == "api_process":
        api_process_section()


if __name__ == "__main__":
    main()
