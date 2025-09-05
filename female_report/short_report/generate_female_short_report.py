from typing import List

from female_report.short_report.generate_recommendation_page import (
    generate_recommendation_page,
    generate_supplements_page,  # Add this import
)
from female_report.short_report.page_0 import cover_page
from female_report.short_report.page_1 import page_1
from female_report.short_report.page_2 import page_2
from female_report.short_report.page_3 import page_3
from female_report.short_report.page_4 import page_4
from female_report.short_report.page_5 import page_5
from female_report.short_report.page_6 import page_6
from female_report.short_report.page_7 import page_7
from female_report.short_report.page_8 import page_8
from female_report.short_report.page_9 import page_9
from female_report.short_report.page_10 import page_10
from female_report.short_report.page_11 import page_11
from female_report.short_report.page_12 import page_12
from female_report.short_report.page_13 import page_13
from models.patient_models import BioMarkerGroup, BloodWorkBioMarkerGroup


def generate_female_short_report(
    report,
    blood_work_report: BloodWorkBioMarkerGroup,
    selectedBioMarkerGroups: List[BioMarkerGroup],
):
    # Helper function to check if recommendations exist
    def has_recommendations(panel_name=None):
        if not report.get("recommendations"):
            return False
        if panel_name:
            return any(
                rec.get("panel") == panel_name for rec in report["recommendations"]
            )
        return True

    # Helper function to check if supplement recommendations exist
    def has_supplement_recommendations(panel_name):
        if not report.get("recommendations"):
            return False
        return any(
            rec.get("panel") == panel_name and rec.get("category") == "supplements"
            for rec in report["recommendations"]
        )

    # Create the pages dynamically based on the data presence
    pages = [cover_page(report)]

    # Lipid-related pages
    if ("lipids" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.lipids and len(blood_work_report.lipids) > 0:
        pages.append(page_1(blood_work_report.lipids))
        if has_recommendations("lipids"):
            pages.append(generate_recommendation_page(report, "lipids"))

    if ("glucose" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.glucose and len(blood_work_report.glucose) > 0:
        pages.append(page_2(blood_work_report.glucose))
        if has_recommendations("glucose"):
            pages.append(generate_recommendation_page(report, "glucose"))

    if ("renal" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.renal and len(blood_work_report.renal) > 0:
        pages.append(page_3(blood_work_report.renal))
        if has_recommendations("renal"):
            pages.append(generate_recommendation_page(report, "renal"))

    if ("mineral" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.mineral and len(blood_work_report.mineral) > 0:
        pages.append(page_4(blood_work_report.mineral))
        if has_recommendations("mineral"):
            pages.append(generate_recommendation_page(report, "mineral"))

    if (
        ("inflammation_Markers" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups)
        and blood_work_report.inflammation_Markers and len(blood_work_report.inflammation_Markers) > 0
    ):
        pages.append(page_5(blood_work_report.inflammation_Markers))
        if has_recommendations("inflammation_Markers"):
            pages.append(generate_recommendation_page(report, "inflammation_Markers"))

    if ("vitamin" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.vitamin and len(blood_work_report.vitamin) > 0:
        pages.append(page_6(blood_work_report.vitamin))
        if has_recommendations("vitamin"):
            pages.append(generate_recommendation_page(report, "vitamin"))

    if ("electrolytes" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.electrolytes and len(blood_work_report.electrolytes) > 0:
        pages.append(page_7(blood_work_report.electrolytes))
        if has_recommendations("electrolytes"):
            pages.append(generate_recommendation_page(report, "electrolytes"))

    if ("liver_Enzymes" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.liver_Enzymes and len(blood_work_report.liver_Enzymes) > 0:
        pages.append(page_8(blood_work_report.liver_Enzymes))
        if has_recommendations("liver_Enzymes"):
            pages.append(generate_recommendation_page(report, "liver_Enzymes"))

    if (
        ("thyroid_Functions" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups)
        and blood_work_report.thyroid_Functions and len(blood_work_report.thyroid_Functions) > 0
    ):
        pages.append(page_9(blood_work_report.thyroid_Functions))

        # Check if regular recommendations exist (lifestyle/diet/activity)
        has_regular = any(
            rec.get("panel") == "thyroid_Functions"
            and rec.get("category") in ["lifestyle", "diet", "activity"]
            for rec in report.get("recommendations", [])
        )
        if has_regular:
            pages.append(generate_recommendation_page(report, "thyroid_Functions"))

    # Check supplements separately
    if has_supplement_recommendations("thyroid_Functions"):
        pages.append(generate_supplements_page(report, "thyroid_Functions"))

    if ("hormone" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.hormone and len(blood_work_report.hormone) > 0:
        pages.extend(
            [page_10(blood_work_report.hormone), page_11(blood_work_report.hormone)]
        )

        # Check if regular recommendations exist
        has_regular = any(
            rec.get("panel") == "hormone"
            and rec.get("category") in ["lifestyle", "diet", "activity"]
            for rec in report.get("recommendations", [])
        )
        if has_regular:
            pages.append(generate_recommendation_page(report, "hormone"))

        # Check supplements separately
        if has_supplement_recommendations("hormone"):
            pages.append(generate_supplements_page(report, "hormone"))

    if ("cbc" in selectedBioMarkerGroups or "full" in selectedBioMarkerGroups) and blood_work_report.cbc and len(blood_work_report.cbc) > 0:
        pages.extend([page_12(blood_work_report.cbc), page_13(blood_work_report.cbc)])
        if has_recommendations("cbc"):
            pages.append(generate_recommendation_page(report, "cbc"))

    return pages
