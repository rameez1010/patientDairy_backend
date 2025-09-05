from datetime import datetime

from models.doctor_models import FullscriptData
from queries.doctor_queries import select_doctor_by_id, update_doctor_fullscript_data
from queries.patient_queries import get_patient_by_id, update_patient_fullscript_id

from .fullscript_sdk import FullscriptSDK


class FullscriptService:
    def __init__(self):
        self.fullscript_sdk = FullscriptSDK()

    async def _get_doctor_or_raise(self, doctor_id: str):
        """
        Helper method to get a doctor by ID and raise an exception if not found
        """
        doctor = await select_doctor_by_id(doctor_id)
        if not doctor:
            raise Exception("Doctor not found")
        return doctor

    def _create_fullscript_data_from_oauth(self, oauth_data: dict) -> FullscriptData:
        """
        Helper method to create a FullscriptData object from OAuth response data
        """
        return FullscriptData(
            access_token=oauth_data.get("access_token"),
            refresh_token=oauth_data.get("refresh_token"),
            token_type=oauth_data.get("token_type"),
            expires_in=oauth_data.get("expires_in"),
            scope=oauth_data.get("scope"),
            created_at=datetime.fromisoformat(oauth_data.get("created_at").replace("Z", "+00:00")),
            resource_owner_id=oauth_data.get("resource_owner", {}).get("id"),
            resource_owner_type=oauth_data.get("resource_owner", {}).get("type"),
        )

    async def get_access_token(self, code: str, doctor_id: str):
        try:
            doctor = await self._get_doctor_or_raise(doctor_id)

            oauth_response = await self.fullscript_sdk.get_access_token(code)

            oauth_data = oauth_response.get("oauth", {})
            fullscript_data = self._create_fullscript_data_from_oauth(oauth_data)

            await update_doctor_fullscript_data(doctor_id, fullscript_data)

            return oauth_response
        except Exception as e:
            print(f"Failed to get access token: {str(e)}")
            raise Exception(f"Failed to get access token: {str(e)}")

    async def refresh_token(self, doctor_id: str):
        try:
            doctor = await self._get_doctor_or_raise(doctor_id)

            refresh_response = await self.fullscript_sdk.refresh_access_token(doctor.fullscript_data.refresh_token)

            oauth_data = refresh_response.get("oauth", {})
            updated_fullscript_data = self._create_fullscript_data_from_oauth(oauth_data)

            await update_doctor_fullscript_data(doctor_id, updated_fullscript_data)

            return refresh_response
        except Exception as e:
            raise Exception(f"Failed to refresh token: {str(e)}")

    async def get_session_grant_token(self, doctor_id: str):
        """
        Get session grant for Fullscript Embed
        """
        try:
            doctor = await self._get_doctor_or_raise(doctor_id)

            if not doctor.fullscript_data:
                raise Exception("Doctor has no Fullscript data. Please authenticate with Fullscript first.")

            refresh_token = doctor.fullscript_data.refresh_token

            refreshed_oauth_response = await self.fullscript_sdk.refresh_access_token(refresh_token)
            oauth_data = refreshed_oauth_response.get("oauth", {})
            refreshed_access_token = oauth_data.get("access_token")

            updated_fullscript_data = self._create_fullscript_data_from_oauth(oauth_data)

            await update_doctor_fullscript_data(doctor_id, updated_fullscript_data)

            session_grant_response = await self.fullscript_sdk.get_session_grant(refreshed_access_token)

            return session_grant_response
        except Exception as e:
            print(f"Failed to get session grant: {str(e)}")
            raise Exception(f"Failed to get session grant: {str(e)}")

    async def create_fullscript_patient(self, patient_id: str, doctor_id: str):
        """
        Creates a patient in Fullscript and stores the Fullscript patient ID in our system

        """
        try:
            # Get the doctor and ensure they have Fullscript access
            doctor = await self._get_doctor_or_raise(doctor_id)

            if not doctor.fullscript_data:
                raise Exception("Doctor has no Fullscript data. Please authenticate with Fullscript first.")

            # Get the patient data from our system
            patient = await get_patient_by_id(patient_id)
            if not patient:
                raise Exception("Patient not found")

            # Refresh the token to ensure we have a valid access token
            refreshed_oauth_response = await self.fullscript_sdk.refresh_access_token(
                doctor.fullscript_data.refresh_token
            )
            oauth_data = refreshed_oauth_response.get("oauth", {})
            refreshed_access_token = oauth_data.get("access_token")

            # Update doctor's Fullscript data with refreshed tokens
            updated_fullscript_data = self._create_fullscript_data_from_oauth(oauth_data)
            await update_doctor_fullscript_data(doctor_id, updated_fullscript_data)

            # Format the patient data for Fullscript
            fullscript_patient_data = {
                "email": patient.email,
                "first_name": patient.firstName,
                "last_name": patient.lastName,
                "metadata": {"id": patient_id},
            }

            # Create the patient in Fullscript
            response = await self.fullscript_sdk.create_patient(refreshed_access_token, fullscript_patient_data)

            # Extract the Fullscript patient ID from the response
            fullscript_patient_id = response.get("patient", {}).get("id")

            if not fullscript_patient_id:
                raise Exception("Failed to get Fullscript patient ID from response")

            # Update our patient record with the Fullscript patient ID
            await update_patient_fullscript_id(patient_id, fullscript_patient_id)

            return response
        except Exception as e:
            print(f"Failed to create Fullscript patient: {str(e)}")
            raise Exception(f"Failed to create Fullscript patient: {str(e)}")

    async def get_patient_treatment_plans(self, patient_id: str, doctor_id: str):
        """
        Get all treatment plans for a patient in Fullscript
        """
        try:
            # Get the doctor and ensure they have Fullscript access
            doctor = await self._get_doctor_or_raise(doctor_id)

            if not doctor.fullscript_data:
                raise Exception("Doctor has no Fullscript data. Please authenticate with Fullscript first.")

            # Get the patient data from our system
            patient = await get_patient_by_id(patient_id)
            if not patient:
                raise Exception("Patient not found")

            # Check if the patient has a Fullscript patient ID
            if not hasattr(patient, "fullscriptPatientId") or not patient.fullscriptPatientId:
                raise Exception("Patient has no Fullscript ID. Please create the patient in Fullscript first.")

            # Refresh the token to ensure we have a valid access token
            refreshed_oauth_response = await self.fullscript_sdk.refresh_access_token(
                doctor.fullscript_data.refresh_token
            )
            oauth_data = refreshed_oauth_response.get("oauth", {})
            refreshed_access_token = oauth_data.get("access_token")

            # Update doctor's Fullscript data with refreshed tokens
            updated_fullscript_data = self._create_fullscript_data_from_oauth(oauth_data)
            await update_doctor_fullscript_data(doctor_id, updated_fullscript_data)

            # Get treatment plans from Fullscript
            treatment_plans_response = await self.fullscript_sdk.get_patient_treatment_plans(
                refreshed_access_token, patient.fullscriptPatientId
            )

            return treatment_plans_response
        except Exception as e:
            print(f"Failed to get patient treatment plans: {str(e)}")
            raise Exception(f"Failed to get patient treatment plans: {str(e)}")

    async def get_treatment_plan(self, treatment_plan_id: str, doctor_id: str):
        """
        Get a single treatment plan by ID

        """
        try:
            # Get the doctor and ensure they have Fullscript access
            doctor = await self._get_doctor_or_raise(doctor_id)

            if not doctor.fullscript_data:
                raise Exception("Doctor has no Fullscript data. Please authenticate with Fullscript first.")

            # Refresh the token to ensure we have a valid access token
            refreshed_oauth_response = await self.fullscript_sdk.refresh_access_token(
                doctor.fullscript_data.refresh_token
            )
            oauth_data = refreshed_oauth_response.get("oauth", {})
            refreshed_access_token = oauth_data.get("access_token")

            # Update doctor's Fullscript data with refreshed tokens
            updated_fullscript_data = self._create_fullscript_data_from_oauth(oauth_data)
            await update_doctor_fullscript_data(doctor_id, updated_fullscript_data)

            # Get the treatment plan from Fullscript
            treatment_plan_response = await self.fullscript_sdk.get_treatment_plan(
                refreshed_access_token, treatment_plan_id
            )

            return treatment_plan_response
        except Exception as e:
            print(f"Failed to get treatment plan: {str(e)}")
            raise Exception(f"Failed to get treatment plan: {str(e)}")

    async def cancel_treatment_plan(self, treatment_plan_id: str, doctor_id: str):
        """
        Cancel a treatment plan

        """
        try:
            # Get the doctor and ensure they have Fullscript access
            doctor = await self._get_doctor_or_raise(doctor_id)

            if not doctor.fullscript_data:
                raise Exception("Doctor has no Fullscript data. Please authenticate with Fullscript first.")

            # Refresh the token to ensure we have a valid access token
            refreshed_oauth_response = await self.fullscript_sdk.refresh_access_token(
                doctor.fullscript_data.refresh_token
            )
            oauth_data = refreshed_oauth_response.get("oauth", {})
            refreshed_access_token = oauth_data.get("access_token")

            # Update doctor's Fullscript data with refreshed tokens
            updated_fullscript_data = self._create_fullscript_data_from_oauth(oauth_data)
            await update_doctor_fullscript_data(doctor_id, updated_fullscript_data)

            # Cancel the treatment plan in Fullscript
            cancel_response = await self.fullscript_sdk.cancel_treatment_plan(refreshed_access_token, treatment_plan_id)

            return cancel_response
        except Exception as e:
            print(f"Failed to cancel treatment plan: {str(e)}")
            raise Exception(f"Failed to cancel treatment plan: {str(e)}")
