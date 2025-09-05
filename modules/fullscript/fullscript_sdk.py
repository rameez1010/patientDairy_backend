import json
from typing import Dict

import httpx
from config.env_config import settings

class FullscriptSDK:
    def __init__(self):
        self.client_id = settings.FULLSCRIPT_CLIENT_ID
        self.client_secret = settings.FULLSCRIPT_CLIENT_SECRET
        self.redirect_uri = settings.FULLSCRIPT_REDIRECT_URI
        self.base_url = settings.FULLSCRIPT_API_URL

    async def get_access_token(self, code: str) -> Dict:
        token_url = f"{self.base_url}/oauth/token"

        request_data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, json=request_data)
            response.raise_for_status()
            return response.json()

    async def refresh_access_token(self, refresh_token: str) -> Dict:
        token_url = f"{self.base_url}/oauth/token"

        request_data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, json=request_data)
            response.raise_for_status()
            return response.json()

    async def get_session_grant(self, access_token: str) -> Dict:
        session_grant_url = f"{self.base_url}/clinic/embeddable/session_grants"

        auth_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(session_grant_url, headers=auth_headers)
            response.raise_for_status()

            return response.json()

    async def create_patient(self, access_token: str, patient_data: Dict) -> Dict:
        patient_data = json.dumps(patient_data)
        patient_url = f"{self.base_url}/clinic/patients"
        auth_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(patient_url, data=patient_data, headers=auth_headers)
            print("============> Patient response: ", response.json())

            response.raise_for_status()
            return response.json()

    async def get_patient_treatment_plans(self, access_token: str, fullscript_patient_id: str) -> Dict:
        treatment_plans_url = f"{self.base_url}/clinic/patients/{fullscript_patient_id}/treatment_plans"
        auth_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.get(treatment_plans_url, headers=auth_headers)
            response.raise_for_status()
            return response.json()

    async def get_treatment_plan(self, access_token: str, treatment_plan_id: str) -> Dict:
        treatment_plan_url = f"{self.base_url}/clinic/treatment_plans/{treatment_plan_id}"
        auth_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.get(treatment_plan_url, headers=auth_headers)
            response.raise_for_status()
            return response.json()

    async def cancel_treatment_plan(self, access_token: str, treatment_plan_id: str) -> Dict:
        cancel_url = f"{self.base_url}/clinic/treatment_plans/{treatment_plan_id}/cancel"
        auth_headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(cancel_url, headers=auth_headers)
            print("============> Cancel response: ", response.json())
            response.raise_for_status()
            return response.json()
