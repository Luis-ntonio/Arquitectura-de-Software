import asyncio

from fastapi import HTTPException
from functions import cases
from database import init_sample_data
from models import Cases

async def demonstrate_case_flow():
    print("--- Demonstrating Case Management Flow (Simulating API Calls) ---")

    # Initialize with some sample data
    sample_data = init_sample_data()
    print("\nInitial Cases:")
    await list_cases_simulation()

    # Simulate creating a new case by calling the router function
    print("\n--- Creating a New Case (Simulating API POST) ---")
    new_case_data = Cases(
        id="simulated_new_case",  # Ensure you are setting the 'id' here
        name="Simulated New Case",
        status="Draft",
        description="This case was created through a simulated API call.",
        client_id=list(sample_data['client_db'].keys())[0] if sample_data['client_db'] else None,
        attorney_id=list(sample_data['attorney_db'].keys())[0] if sample_data['attorney_db'] else None,
        attachment_id=None
    )
    try:
        created_case = await cases.create_new_case(new_case_data)
        print(f"Simulated Case Created with ID: {created_case.id}, Name: {created_case.name}")
        print("\nCases After Creation:")
        await list_cases_simulation()

        # Simulate deleting the newly created case by calling the router function
        if created_case and created_case.id:
            case_id_to_delete = created_case.id
            print(f"\n--- Deleting Case with ID: {case_id_to_delete} (Simulating API DELETE) ---")
            try:
                await cases.delete_existing_case(case_id_to_delete)
                print(f"Simulated deletion of case with ID: {case_id_to_delete} successful.")
                print("\nCases After Deletion:")
                await list_cases_simulation()
            except HTTPException as e:
                print(f"Error during simulated deletion: {e.detail}")
        else:
            print("\nCould not delete the newly created case (ID not found).")

    except HTTPException as e:
        print(f"Error during simulated case creation: {e.detail}")

async def list_cases_simulation():
    all_cases = await cases.read_cases()
    if all_cases:
        for case in all_cases:
            print(f"ID: {case.id}, Name: {case.name}, Status: {case.status}")
    else:
        print("No cases found.")

if __name__ == "__main__":
    asyncio.run(demonstrate_case_flow())