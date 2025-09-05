from typing import Any, Dict, Optional

from models.patient_models import FunctionalMedicineIntakeForm, FunctionalMedicineIntakeFormUpdate
from queries.patient_queries import check_medical_form_completion, get_patient_by_id, update_patient_medical_form


class MedicalFormService:
    async def check_form_completion(self, patient_id: str) -> Dict[str, Any]:
        """
        Check if the patient's Functional Medicine Intake Form is complete
        """
        try:
            # Get patient data
            patient = await get_patient_by_id(patient_id)
            if not patient:
                return {"is_complete": False, "message": "Patient not found"}

            # Check form completion
            is_complete = await check_medical_form_completion(patient_id)

            return {"is_complete": is_complete, "message": "Form completion status checked successfully"}
        except Exception as e:
            raise Exception(f"Failed to check form completion: {str(e)}")

    async def update_medical_form(
        self, patient_id: str, form_data: FunctionalMedicineIntakeFormUpdate
    ) -> Dict[str, Any]:
        """
        Update the patient's Functional Medicine Intake Form
        """
        try:
            # Get current patient data
            patient = await get_patient_by_id(patient_id)
            if not patient:
                raise Exception("Patient not found")

            # Update the medical form
            await update_patient_medical_form(patient_id, form_data)

            return {
                "patient_id": patient_id,
                "message": "Medical form updated successfully",
            }
        except Exception as e:
            raise Exception(f"MedicalFormService: Failed to update medical form: {str(e)}")

    async def get_medical_form(self, patient_id: str) -> Optional[FunctionalMedicineIntakeForm]:
        """
        Get the patient's current Functional Medicine Intake Form
        """
        try:
            patient = await get_patient_by_id(patient_id)
            if not patient:
                return None

            return patient.functionalMedicineIntakeForm
        except Exception as e:
            raise Exception(f"Failed to get medical form: {str(e)}")
