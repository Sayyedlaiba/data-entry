import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Data Entry Dashboard")

# 2. Initialize Session State
# This holds our data in memory so it doesn't disappear when the app rerenders.
if "data_table" not in st.session_state:
    st.session_state.data_table = pd.DataFrame(
        columns=["Name", "Role", "Department", "Experience (Years)"]
    )

# 3. Reset Callback Function
def reset_table():
    st.session_state.data_table = pd.DataFrame(
        columns=["Name", "Role", "Department", "Experience (Years)"]
    )
    # Clear individual input widget states if needed
    st.session_state.input_name = ""
    st.session_state.input_role = ""
    st.session_state.input_exp = 0

# 4. Layout: Form on the Left (Sidebar), Table on the Right (Main Content)
st.title("📊 Team Roster Data Entry")
st.write("Enter details on the left to populate the master table on the right.")

---

# --- LEFT SIDEBAR: ENTRY FORM ---
with st.sidebar:
    st.header("Add New Entry")
    
    # We use a form component so the app only rerenders once the submit button is clicked
    with st.form(key="entry_form", clear_on_submit=True):
        name = st.text_input("Full Name", key="input_name")
        role = st.text_input("Job Role", key="input_role")
        dept = st.selectbox("Department", ["Engineering", "Design", "Product", "Marketing", "HR"])
        exp = st.number_input("Years of Experience", min_value=0, max_value=50, step=1, key="input_exp")
        
        submit_button = st.form_submit_button(label="Add to Table")
        
    # Actions taken upon form submission
    if submit_button:
        if name.strip() == "" or role.strip() == "":
            st.error("Please fill out both Name and Role fields.")
        else:
            # Create a new row dataframe
            new_row = pd.DataFrame([{
                "Name": name,
                "Role": role,
                "Department": dept,
                "Experience (Years)": exp
            }])
            
            # Concatenate the new row to our session state dataframe
            st.session_state.data_table = pd.concat(
                [st.session_state.data_table, new_row], 
                ignore_index=True
            )
            st.success(f"Added {name} successfully!")

    st.markdown("---")
    # Reset Button placed at the bottom of the sidebar
    st.button("Reset Entire Table", on_click=reset_table, type="primary")


# --- RIGHT MAIN PAGE: DATA TABLE ---
st.subheader("Current Database")

if st.session_state.data_table.empty:
    st.info("The table is currently empty. Use the sidebar form to add data.")
else:
    # st.dataframe makes the table interactive (sortable, searchable)
    st.dataframe(st.session_state.data_table, use_container_width=True)
    
    # Quick metric summary
    st.markdown("### Summary Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Total Entries", len(st.session_state.data_table))
    col2.metric("Avg. Experience", f"{st.session_state.data_table['Experience (Years)'].mean():.1f} years")
