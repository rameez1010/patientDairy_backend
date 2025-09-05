import json
from pathlib import Path
from typing import Any, Dict, List

from models.patient_models import GeneResultsGrouped
from modules.patients.mappers.gene_results_mapper import GeneResultsMapper


def load_gene_panels_data() -> Dict[str, Any]:
    """Load gene panels configuration from genes-panels.json."""
    file_path = Path(__file__).parent.parent / "genes-panels.json"
    with open(file_path, "r") as f:
        return json.load(f)


def evaluate_and_group_gene_results(raw_response: Dict[str, Any]) -> GeneResultsGrouped:
    """
    Evaluate gene results from raw response and group them by panels.

    Args:
        raw_response (Dict[str, Any]): Raw response from Gemini AI containing gene results

    Returns:
        GeneResultsGrouped: Grouped gene results with risk assessments
    """
    # Initialize the gene results mapper
    mapper = GeneResultsMapper()

    # Map raw response to grouped gene results
    grouped_results = mapper.map_to_grouped_gene_results(raw_response)

    return grouped_results


def get_gene_info_by_name_and_rs(gene_name: str, rs_id: str = None) -> Dict[str, Any]:
    """
    Get gene information from the panels configuration.

    Args:
        gene_name (str): Name of the gene
        rs_id (str, optional): Reference SNP ID

    Returns:
        Dict containing gene information including possible genotypes and risk levels
    """
    panels_data = load_gene_panels_data()

    for panel in panels_data["panels"]:
        for gene in panel["genes"]:
            if gene["name"] == gene_name and (not rs_id or gene.get("rs_id") == rs_id):
                return {
                    "gene_name": gene["name"],
                    "rs_id": gene.get("rs_id"),
                    "panel": panel["panel"],
                    "genotypes": gene["genotypes"],
                }

    return None


def get_available_panels() -> List[str]:
    """
    Get list of available gene panels.

    Returns:
        List of panel names
    """
    panels_data = load_gene_panels_data()
    return [panel["panel"] for panel in panels_data["panels"]]


def get_genes_in_panel(panel_name: str) -> List[Dict[str, Any]]:
    """
    Get all genes in a specific panel.

    Args:
        panel_name (str): Name of the panel

    Returns:
        List of genes in the panel
    """
    panels_data = load_gene_panels_data()

    for panel in panels_data["panels"]:
        if panel["panel"] == panel_name:
            return panel["genes"]

    return []
