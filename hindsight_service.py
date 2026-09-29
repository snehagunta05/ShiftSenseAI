import os
import asyncio
import threading

from dotenv import load_dotenv
from hindsight_client import Hindsight


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(override=True)

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "shiftsense-production"
)


# ============================================================
# CLIENT
# ============================================================

_client = None


def get_client():
    global _client

    if _client is None:

        if not HINDSIGHT_API_KEY:
            raise RuntimeError(
                "HINDSIGHT_API_KEY is missing from .env"
            )

        _client = Hindsight(
            base_url=HINDSIGHT_BASE_URL,
            api_key=HINDSIGHT_API_KEY,
            timeout=60.0
        )

    return _client


# ============================================================
# ASYNC RUNNER
# ============================================================

def run_async(coroutine):

    result = {
        "value": None,
        "error": None
    }

    def worker():

        try:

            result["value"] = asyncio.run(coroutine)

        except Exception as e:

            result["error"] = e

    thread = threading.Thread(
        target=worker
    )

    thread.start()
    thread.join()

    if result["error"]:

        raise result["error"]

    return result["value"]


# ============================================================
# INITIALIZE BANK
# ============================================================

async def _initialize_bank():

    client = get_client()

    return await client.acreate_bank(

        bank_id=BANK_ID,

        name="ShiftSense AI",

        background=(
            "ShiftSense AI is an industrial shift handover "
            "and operational memory system. It stores shift "
            "reports, equipment conditions, incidents, "
            "operator observations, corrective actions, "
            "and lessons learned."
        ),

        retain_mission=(
            "Extract useful industrial operational knowledge "
            "including machines, symptoms, incidents, "
            "measurements, corrective actions, causes, "
            "and lessons learned."
        ),

        reflect_mission=(
            "Analyze historical industrial shift information "
            "and provide evidence-based operational insights. "
            "Do not invent facts."
        ),

        enable_observations=True,

        enable_text_search=True,

        enable_temporal_retrieval=True,

        enable_graph_retrieval=True,

        enable_reranking=True
    )


def initialize_bank():

    return run_async(
        _initialize_bank()
    )


# ============================================================
# SAVE SHIFT
# ============================================================

async def _save_shift(shift_data):

    client = get_client()

    shift_id = str(
        shift_data.get(
            "shift_id",
            "UNKNOWN"
        )
    )

    machine = str(
        shift_data.get(
            "machine",
            "UNKNOWN"
        )
    )

    operator = str(
        shift_data.get(
            "operator",
            "UNKNOWN"
        )
    )

    date = str(
        shift_data.get(
            "date",
            "UNKNOWN"
        )
    )

    shift = str(
        shift_data.get(
            "shift",
            "UNKNOWN"
        )
    )

    status = str(
        shift_data.get(
            "status",
            "UNKNOWN"
        )
    )

    temperature = str(
        shift_data.get(
            "temperature",
            "Not recorded"
        )
    )

    vibration = str(
        shift_data.get(
            "vibration",
            "Not recorded"
        )
    )

    pressure = str(
        shift_data.get(
            "pressure",
            "Not recorded"
        )
    )

    incident = str(
        shift_data.get(
            "incident",
            "None"
        )
    )

    actions = str(
        shift_data.get(
            "actions",
            "None"
        )
    )

    notes = str(
        shift_data.get(
            "notes",
            "None"
        )
    )

    content = f"""
INDUSTRIAL SHIFT REPORT

Shift ID:
{shift_id}

Date:
{date}

Shift:
{shift}

Machine:
{machine}

Operator:
{operator}

Machine Status:
{status}

Temperature:
{temperature}

Vibration:
{vibration}

Pressure:
{pressure}

Incident:
{incident}

Corrective / Preventive Actions:
{actions}

Operator Notes:
{notes}
"""

    metadata = {

        "shift_id": shift_id,

        "machine": machine,

        "operator": operator,

        "date": date,

        "shift": shift,

        "status": status
    }

    return await client.aretain(

        bank_id=BANK_ID,

        content=content,

        context=(
            "Industrial shift handover report "
            "stored by ShiftSense AI."
        ),

        metadata=metadata,

        tags=[
            "shift-report",
            "industrial",
            machine
        ]
    )


def save_shift(shift_data):

    return run_async(
        _save_shift(shift_data)
    )


# ============================================================
# RECALL HISTORICAL INCIDENTS
# ============================================================

async def _recall_previous_incidents(query):

    client = get_client()

    return await client.arecall(

        bank_id=BANK_ID,

        query=query,

        max_tokens=2000,

        budget="mid",

        include_chunks=True
    )


def recall_previous_incidents(query):

    return run_async(
        _recall_previous_incidents(query)
    )


# ============================================================
# GENERAL RECALL
# ============================================================

def recall(query):

    return recall_previous_incidents(
        query
    )


# ============================================================
# INCIDENT ANALYSIS
# ============================================================

async def _analyze_incident(

    machine,
    incident,
    temperature="",
    vibration="",
    pressure=""
):

    client = get_client()

    query = f"""
Current industrial incident:

Machine:
{machine}

Incident:
{incident}

Current Temperature:
{temperature}

Current Vibration:
{vibration}

Current Pressure:
{pressure}

Analyze the historical ShiftSense AI memory.

Answer these questions:

1. Have similar incidents happened before?

2. Which machine was involved?

3. What symptoms were observed?

4. What corrective actions were previously taken?

5. Are there recurring patterns?

6. What lessons were learned?

7. What should the current operator check?

Use only information supported by stored memories.

Clearly distinguish historical information from
recommendations or observations.
"""

    return await client.areflect(

        bank_id=BANK_ID,

        query=query,

        budget="low"
    )


def analyze_incident(

    machine,

    incident,

    temperature="",

    vibration="",

    pressure=""
):

    return run_async(

        _analyze_incident(

            machine=machine,

            incident=incident,

            temperature=temperature,

            vibration=vibration,

            pressure=pressure
        )
    )


# ============================================================
# HANDOVER GENERATION
# ============================================================

async def _generate_handover(machine):

    client = get_client()

    query = f"""
Generate a concise industrial shift handover for:

Machine:
{machine}

Use historical ShiftSense AI memories.

Include:

- Recent incidents
- Previous symptoms
- Previous corrective actions
- Current risks or warnings
- Important observations
- What the next shift should monitor

Use only stored historical information.
Do not invent facts.
"""

    return await client.areflect(

        bank_id=BANK_ID,

        query=query,

        budget="low"
    )


def generate_handover(machine):

    return run_async(
        _generate_handover(machine)
    )


# ============================================================
# RESPONSE FORMATTER
# ============================================================

def response_to_text(response):

    if response is None:

        return "No response received."

    # Reflect response
    if hasattr(response, "text"):

        text = response.text

        if text:

            return str(text)

    # Recall response
    if hasattr(response, "results"):

        results = response.results

        if not results:

            return "No matching historical memories found."

        output = []

        for result in results:

            if hasattr(result, "text"):

                output.append(
                    str(result.text)
                )

            else:

                output.append(
                    str(result)
                )

        return "\n\n".join(output)

    return str(response)