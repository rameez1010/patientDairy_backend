from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore


def process_document_sample(
    project_id: str = "333120675205",
    location: str = "us",
    processor_id: str = "538f3a86b7ddab95",
    # file_path: str = "",
    file_content: bytes = "",
    mime_type: str = "application/pdf",
    field_mask: Optional[str] = None,
    processor_version_id: Optional[str] = None,
) -> None:
    # You must set the `api_endpoint` if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
        name = client.processor_version_path(project_id, location, processor_id, processor_version_id)
    else:
        # The full resource name of the processor, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}`
        name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    # with open(file_path, "rb") as image:
    #     image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    process_options = documentai.ProcessOptions(
        # Process only specific pages
        # individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
        #     pages=[1]
        # )
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    result = client.process_document(request=request)

    types = []
    mention_text = []

    # Each Document.entity is a classification
    for entity in result.document.entities:
        classification = entity.type_
        types.append(classification)
        mention_text.append(entity.mention_text)
        final_result = dict(zip(types, mention_text))
    return final_result
