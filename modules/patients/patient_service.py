import io
from typing import Any, Dict

from PyPDF2 import PdfMerger

from config.cloud_storage import upload_blob
from engines.biomarker_engine import evaluate_biomarkers_and_group
from female_report.short_report.generate_female_short_report import (
    generate_female_short_report,
)
from male_report.short_report.generate_male_short_report import (
    generate_male_short_report,
)
from models.patient_models import Patient
from modules.patients.helpers.date_helpers import parse_collection_date
from modules.patients.mappers import bloodwork_results_mapper
from modules.patients.mappers.bloodwork_results_mapper import BloodworkResultsMapper
from modules.patients.mappers.gene_results_mapper import GeneResultsMapper
from modules.patients.utils.file_utils import calculate_file_hash
from utils.helpers import is_name_match
from queries.patient_queries import (
    add_blood_work_reports_to_patient,
    add_gene_result_reports_to_patient,
    check_duplicate_blood_work_file_hash,
    check_duplicate_gene_result_file_hash,
    get_patient_latest_blood_work_report,
)


class PatientService:
    def __init__(self):
        self.bloodwork_mapper = BloodworkResultsMapper()
        self.gene_mapper = GeneResultsMapper()

    async def add_patient_blood_work_report(
        self, patient_id: str, doctor_id: str, raw_response: Dict[str, Any], file_content: bytes, file_name: str, patient_full_name: str, force_upload: bool = False
    ) -> Any:
        # Calculate file hash for duplicate detection
        file_hash = calculate_file_hash(file_content)

        # Check for duplicate file

        is_duplicate = await check_duplicate_blood_work_file_hash(patient_id, doctor_id, file_hash)
        if is_duplicate:
            raise ValueError("This file has already been uploaded for this patient.")
    
        # Map raw response to blood work report model
        blood_work = self.bloodwork_mapper.map_to_bloodwork_results(raw_response)

        # Validate patient name using helpers
        extracted_name = blood_work.patient or blood_work.name
        if extracted_name and not is_name_match(extracted_name, patient_full_name):
            if not force_upload:
                return {
                    "error": True,
                    "error_type": "name_mismatch",
                    "message": f"Uploaded report name '{extracted_name}' does not match patient name '{patient_full_name}'. Proceed only if you are sure.",
                    "extracted_name": extracted_name,
                    "patient_full_name": patient_full_name
                }
            # else: allow upload to proceed

        # Determine gender for biomarker evaluation
        sex = "male" if str(blood_work.sex).strip().upper().startswith(("M", "MALE")) else "female"

        age = blood_work.age
        dateOfBirth = blood_work.dateOfBirth
        # Evaluate and group biomarkers
        grouped_results = evaluate_biomarkers_and_group(blood_work, sex)

        parsed_collection_date = parse_collection_date(blood_work.collectionDate) if blood_work.collectionDate else None
        parsed_dateOfBirth = parse_collection_date(dateOfBirth) if dateOfBirth else None

        # Store blood work report with file hash and name
        updated_patient = await add_blood_work_reports_to_patient(
            patient_id,
            doctor_id,
            sex,
            age,
            parsed_dateOfBirth,
            parsed_collection_date,
            grouped_results,
            file_hash,
            file_name,
        )

        return updated_patient

    async def add_patient_gene_results_report(
        self,
        patient_id: str,
        doctor_id: str,
        raw_response: Dict[str, Any],
        collection_date: str = None,
        file_content: bytes = None,
        file_name: str = None,
    ) -> Patient:
        # Calculate file hash for duplicate detection
        file_hash = calculate_file_hash(file_content)

        # Check for duplicate file
        is_duplicate = await check_duplicate_gene_result_file_hash(patient_id, doctor_id, file_hash)
        if is_duplicate:
            raise ValueError("This file has already been uploaded for this patient.")

        gene_result_report = self.gene_mapper.map_to_gene_result_report(raw_response, collection_date)

        updated_patient = await add_gene_result_reports_to_patient(
            patient_id, doctor_id, gene_result_report, file_hash, file_name
        )

        return updated_patient

    async def generate_report(self, request_data: Dict[str, Any]) -> str:
        patient_id = request_data["id"]
        latest_blood_work_report = await get_patient_latest_blood_work_report(patient_id)
        request_data["age"] = latest_blood_work_report.age
        request_data["sex"] = latest_blood_work_report.sex
        request_data["dateOfBirth"] = latest_blood_work_report.dateOfBirth
        request_data["collectionDate"] = latest_blood_work_report.reportDate
        request_data["practitioner"] = latest_blood_work_report.practitioner

        sex_value = latest_blood_work_report.sex

        selectedBioMarkerGroups = request_data["selectedBioMarkerGroups"]
        # Generate report buffers based on patient sex
        if sex_value in ["f", "female"]:
            buffers = generate_female_short_report(
                request_data,
                latest_blood_work_report.bloodWorkBioMarkerGroup,
                selectedBioMarkerGroups,
            )
        elif sex_value in ["m", "male"]:
            buffers = generate_male_short_report(
                request_data,
                latest_blood_work_report.bloodWorkBioMarkerGroup,
                selectedBioMarkerGroups,
            )
        else:
            raise ValueError(f"Unsupported sex value: {sex_value}")

        # Merge all page buffers
        merger = PdfMerger()
        for buffer in buffers:
            merger.append(buffer)

        final_buffer = io.BytesIO()
        merger.write(final_buffer)
        merger.close()

        # Upload the merged PDF
        final_buffer.seek(0)
        report_date = getattr(latest_blood_work_report, 'reportDate', '')
        bio_marker_str = '_'.join(request_data.get('selectedBioMarkerGroups', []))
        filename = f"{request_data.get('firstName', '')}_{request_data.get('lastName', '')}_{request_data.get('id', '')}_{report_date}_{bio_marker_str}_report_.pdf"
        
        upload_blob(final_buffer, filename)

        return filename
