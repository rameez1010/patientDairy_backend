import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Font registration (should be done only once)
pdfmetrics.registerFont(TTFont("Roboto-Thin", "male_report/fonts/Roboto-Thin.ttf"))
pdfmetrics.registerFont(
    TTFont("Roboto-Regular", "male_report/fonts/Roboto-Regular.ttf")
)
pdfmetrics.registerFont(TTFont("Roboto-Bold", "male_report/fonts/Roboto-Bold.ttf"))


def format_panel_name(panel_name):
    """Format panel names for display (e.g., 'thyroid_Functions' -> 'Thyroid')"""
    # Remove underscores and split into words
    words = panel_name.replace("_", " ").split()
    # Capitalize first letter of each word and take only the first word
    formatted = " ".join(word.capitalize() for word in words)
    # Split again and take first part (e.g., "Thyroid Functions" -> "Thyroid")
    return formatted.split()[0]


def generate_supplements_page(data, panel_name):
    """Generate a PDF page with supplement recommendations for a specific panel"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Background setup
    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    # White rectangle for content area
    c.setFillColor("white")
    c.rect(0, 20, 612, 300, stroke=0, fill=1)

    # Get only supplement recommendations for the specified panel
    panel_recommendations = [
        rec
        for rec in data.get("recommendations", [])
        if rec.get("panel") == panel_name and rec.get("category") == "supplements"
    ]

    if not panel_recommendations:
        c.showPage()
        c.save()
        return buffer

    # Title
    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, f"{format_panel_name(panel_name)} Supplement Recommendations")

    # Subtitle
    c.setFillColor("gray")
    c.setFont("Roboto-Regular", 11)
    c.drawString(70, 583, "Please follow these supplement recommendations:")

    # Divider line
    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 575, 550, 575)

    # Initialize text position
    y_position = 550
    line_height = 16
    category_spacing = 17

    # Draw each supplement recommendation
    for rec in panel_recommendations:
        # Action (main recommendation)
        c.setFillColor("#333333")
        c.setFont("Roboto-Regular", 11)
        c.drawString(70, y_position, f"• {rec.get('action', '')}")
        y_position -= line_height

        # Details (bullet points)
        c.setFillColor("gray")
        c.setFont("Roboto-Regular", 10)
        for detail in rec.get("details", []):
            text_object = c.beginText(90, y_position)
            text_object.textLine(f"- {detail}")
            c.drawText(text_object)
            y_position -= 12

            # Page break check
            if y_position < 50:
                c.showPage()
                y_position = 750
                c.drawImage(
                    bg_image_path,
                    0,
                    0,
                    width=612,
                    height=800,
                    preserveAspectRatio=False,
                )
                # Redraw header if we broke page
                c.setFillColor("#333333")
                c.setFont("Roboto-Regular", 11)
                c.drawString(70, y_position, f"• {rec.get('action', '')} (cont'd):")
                y_position -= line_height

        y_position -= category_spacing  # Extra space after each recommendation

    c.showPage()
    c.save()
    return buffer


def generate_recommendation_page(data, panel_name):
    "Generate a PDF page with recommendations for a specific panel"
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Background setup
    bg_image_path = "male_report/short_report/bg_new.jpg"
    c.drawImage(bg_image_path, 0, 0, width=612, height=800, preserveAspectRatio=False)

    # White rectangle for content area
    c.setFillColor("white")
    c.rect(0, 20, 612, 300, stroke=0, fill=1)

    # Get recommendations excluding supplements for the specified panel
    panel_recommendations = [
        rec
        for rec in data.get("recommendations", [])
        if rec.get("panel") == panel_name and rec.get("category") != "supplements"
    ]

    if not panel_recommendations:
        c.showPage()
        c.save()
        return buffer

    # Title
    c.setFillColor("#BF7BD3")
    c.setFont("Roboto-Bold", 25)
    c.drawString(70, 610, f"{format_panel_name(panel_name)} Recommendations")

    # Subtitle
    c.setFillColor("gray")
    c.setFont("Roboto-Regular", 11)
    c.drawString(
        70,
        583,
        f"Please follow the recommendations below to optimize your {panel_name} levels:",
    )

    # Divider line
    c.setStrokeColor("#adb5bd")
    c.setLineWidth(0.2)
    c.line(70, 575, 550, 575)

    # Initialize text position
    y_position = 550
    line_height = 16
    category_spacing = 17

    # Group recommendations by category
    categories = {}
    for rec in panel_recommendations:
        category = rec.get("category", "general")
        if category not in categories:
            categories[category] = []
        categories[category].append(rec)

    # Draw each category
    for category, recs in categories.items():
        # Category header
        c.setFillColor("#BF7BD3")
        c.setFont("Roboto-Bold", 12)
        c.drawString(70, y_position, f"{category.capitalize()}:")
        y_position -= line_height

        # Recommendations
        for rec in recs:
            # Action (main recommendation)
            c.setFillColor("#333333")
            c.setFont("Roboto-Regular", 11)
            c.drawString(70, y_position, f"• {rec.get('action', '')}")
            y_position -= line_height

            # Details (bullet points)
            c.setFillColor("gray")
            c.setFont("Roboto-Regular", 10)
            # Handle gender-specific details
            details = rec.get("details", [])
            if rec["action"] == "Limit alcohol" and len(details) >= 2:
                # Use the appropriate detail based on sex
                sex = data.get("sex", "M")  # Default to Male if not specified
                if sex == "M":
                    detail = details[0]  # Male recommendation (2 drinks/day)
                else:
                    detail = details[1]  # Female recommendation (1 drink/day)

                # Draw the selected detail
                text_object = c.beginText(90, y_position)
                text_object.textLine(f"- {detail}")
                c.drawText(text_object)
                y_position -= 12

            else:
                for detail in details:
                    text_object = c.beginText(90, y_position)
                    text_object.textLine(f"- {detail}")
                    c.drawText(text_object)
                    y_position -= 12

                    # Page break check
                    if y_position < 50:
                        c.showPage()
                        y_position = 750
                        c.drawImage(
                            bg_image_path,
                            0,
                            0,
                            width=612,
                            height=800,
                            preserveAspectRatio=False,
                        )
                        # Redraw category header if we broke page
                        c.setFillColor("#BF7BD3")
                        c.setFont("Roboto-Bold", 12)
                        c.drawString(
                            70, y_position, f"{category.capitalize()} (cont'd):"
                        )
                        y_position -= line_height

            y_position -= category_spacing  # Extra space after each recommendation

    c.showPage()
    c.save()
    return buffer
