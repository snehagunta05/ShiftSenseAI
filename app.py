import streamlit as st

from hindsight_service import (
    initialize_bank,
    save_shift,
    recall_previous_incidents,
    analyze_incident,
    generate_handover,
    response_to_text
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ShiftSense AI",
    page_icon="🏭",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🏭 ShiftSense AI")

st.caption(
    "Industrial Shift Handover & Operational Memory"
)


# ============================================================
# INITIALIZE
# ============================================================

if "initialized" not in st.session_state:

    st.session_state.initialized = False


if not st.session_state.initialized:

    with st.spinner(
        "Connecting to Hindsight..."
    ):

        try:

            initialize_bank()

            st.session_state.initialized = True

        except Exception as e:

            st.error(
                "Hindsight connection failed."
            )

            st.code(
                str(e)
            )

            st.stop()


# ============================================================
# SIDEBAR
# ============================================================

page = st.sidebar.radio(

    "Select Module",

    [
        "Dashboard",
        "Record Shift",
        "Analyze Incident",
        "Search Memory",
        "Generate Handover",
        "Demo"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Memory System",
            "ONLINE"
        )

    with col2:

        st.metric(
            "Hindsight Bank",
            "ACTIVE"
        )

    with col3:

        st.metric(
            "Incident Analysis",
            "READY"
        )

    st.divider()

    st.subheader(
        "How ShiftSense AI works"
    )

    st.write(
        """
        ShiftSense AI stores industrial shift information
        in Hindsight's long-term memory.

        When a new incident occurs, the system can search
        previous shift reports and identify relevant
        historical information.
        """
    )

    st.info(
        """
        Example workflow:

        Shift 1 → Incident recorded

        Shift 2 → Corrective action recorded

        Shift 3 → Similar incident occurs

        ShiftSense AI → Retrieves previous knowledge
        """
    )


# ============================================================
# RECORD SHIFT
# ============================================================

elif page == "Record Shift":

    st.header("📝 Record Shift")

    with st.form(
        "shift_form"
    ):

        shift_id = st.text_input(
            "Shift ID",
            "SHIFT-001"
        )

        machine = st.text_input(
            "Machine",
            "M04"
        )

        operator = st.text_input(
            "Operator",
            "Operator 01"
        )

        shift = st.selectbox(
            "Shift",
            [
                "Morning",
                "Afternoon",
                "Night"
            ]
        )

        status = st.selectbox(
            "Machine Status",
            [
                "Normal",
                "Warning",
                "Critical"
            ]
        )

        temperature = st.text_input(
            "Temperature",
            "82°C"
        )

        vibration = st.text_input(
            "Vibration",
            "4.2 mm/s"
        )

        pressure = st.text_input(
            "Pressure",
            "5.1 bar"
        )

        incident = st.text_area(
            "Incident",
            "Machine temperature increased above normal range."
        )

        actions = st.text_area(
            "Corrective Actions",
            "Cooling fan inspected and cleaned."
        )

        notes = st.text_area(
            "Operator Notes",
            "Temperature returned closer to normal."
        )

        submit = st.form_submit_button(
            "💾 Save Shift",
            use_container_width=True
        )

    if submit:

        shift_data = {

            "shift_id": shift_id,

            "machine": machine,

            "operator": operator,

            "date": str(
                st.session_state.get(
                    "date",
                    "2026-09-29"
                )
            ),

            "shift": shift,

            "status": status,

            "temperature": temperature,

            "vibration": vibration,

            "pressure": pressure,

            "incident": incident,

            "actions": actions,

            "notes": notes
        }

        try:

            with st.spinner(
                "Saving shift to Hindsight..."
            ):

                result = save_shift(
                    shift_data
                )

            st.success(
                "✅ Shift successfully stored!"
            )

            st.write(
                response_to_text(result)
            )

        except Exception as e:

            st.error(
                "Failed to save shift."
            )

            st.code(
                str(e)
            )


# ============================================================
# ANALYZE INCIDENT
# ============================================================

elif page == "Analyze Incident":

    st.header(
        "🚨 Analyze Current Incident"
    )

    machine = st.text_input(
        "Machine",
        "M04"
    )

    incident = st.text_area(
        "Current Incident",

        "Machine M04 temperature increased again "
        "and vibration is higher than normal."
    )

    temperature = st.text_input(
        "Current Temperature",
        "86°C"
    )

    vibration = st.text_input(
        "Current Vibration",
        "5.0 mm/s"
    )

    pressure = st.text_input(
        "Current Pressure",
        "5.2 bar"
    )

    if st.button(
        "🔍 Analyze Historical Incidents",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Analyzing historical memory..."
            ):

                result = analyze_incident(

                    machine=machine,

                    incident=incident,

                    temperature=temperature,

                    vibration=vibration,

                    pressure=pressure
                )

            st.success(
                "Analysis completed."
            )

            st.subheader(
                "🧠 ShiftSense AI Result"
            )

            st.markdown(
                response_to_text(result)
            )

        except Exception as e:

            st.error(
                "Incident analysis failed."
            )

            st.code(
                str(e)
            )


# ============================================================
# SEARCH MEMORY
# ============================================================

elif page == "Search Memory":

    st.header(
        "🔎 Search Historical Memory"
    )

    query = st.text_area(

        "What do you want to know?",

        "What happened previously when machine M04 overheated?"
    )

    if st.button(
        "Search Hindsight Memory",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Searching historical memory..."
            ):

                result = recall_previous_incidents(
                    query
                )

            st.subheader(
                "Historical Results"
            )

            st.markdown(
                response_to_text(result)
            )

        except Exception as e:

            st.error(
                "Memory search failed."
            )

            st.code(
                str(e)
            )


# ============================================================
# GENERATE HANDOVER
# ============================================================

elif page == "Generate Handover":

    st.header(
        "📋 Generate Shift Handover"
    )

    machine = st.text_input(
        "Machine",
        "M04"
    )

    if st.button(
        "Generate Handover",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Generating handover from historical memory..."
            ):

                result = generate_handover(
                    machine
                )

            st.subheader(
                "📋 Handover"
            )

            st.markdown(
                response_to_text(result)
            )

        except Exception as e:

            st.error(
                "Handover generation failed."
            )

            st.code(
                str(e)
            )


# ============================================================
# DEMO
# ============================================================

elif page == "Demo":

    st.header(
        "🎯 Hackathon Demo"
    )

    st.write(
        """
        This creates three historical shift reports
        involving the same machine.
        """
    )

    if st.button(
        "🚀 Load Demo Data",
        use_container_width=True
    ):

        demo_data = [

            {
                "shift_id": "DEMO-001",
                "machine": "M04",
                "operator": "Ravi",
                "date": "2026-09-20",
                "shift": "Morning",
                "status": "Warning",
                "temperature": "82°C",
                "vibration": "4.2 mm/s",
                "pressure": "5.1 bar",
                "incident": (
                    "M04 temperature increased "
                    "above normal range."
                ),
                "actions": (
                    "Cooling fan inspected and cleaned."
                ),
                "notes": (
                    "Temperature decreased after maintenance."
                )
            },

            {
                "shift_id": "DEMO-002",
                "machine": "M04",
                "operator": "Anil",
                "date": "2026-09-21",
                "shift": "Afternoon",
                "status": "Normal",
                "temperature": "76°C",
                "vibration": "3.6 mm/s",
                "pressure": "5.0 bar",
                "incident": (
                    "No major incident."
                ),
                "actions": (
                    "Cooling system monitored."
                ),
                "notes": (
                    "Machine remained stable."
                )
            },

            {
                "shift_id": "DEMO-003",
                "machine": "M04",
                "operator": "Suresh",
                "date": "2026-09-22",
                "shift": "Night",
                "status": "Warning",
                "temperature": "84°C",
                "vibration": "4.7 mm/s",
                "pressure": "5.2 bar",
                "incident": (
                    "M04 temperature increased again "
                    "and vibration became elevated."
                ),
                "actions": (
                    "Cooling fan and ventilation "
                    "path inspected."
                ),
                "notes": (
                    "Possible recurring cooling issue."
                )
            }
        ]

        successful = 0

        for data in demo_data:

            try:

                save_shift(data)

                successful += 1

            except Exception as e:

                st.error(
                    f"Error storing {data['shift_id']}: {e}"
                )

        if successful == 3:

            st.success(
                "✅ All demo shift records stored!"
            )

            st.info(
                """
                Now go to **Analyze Incident**.

                Machine:
                M04

                Incident:
                Machine M04 temperature increased again
                and vibration is higher than normal.

                Click **Analyze Historical Incidents**.
                """
            )

        else:

            st.warning(
                f"{successful}/3 records stored."
            )