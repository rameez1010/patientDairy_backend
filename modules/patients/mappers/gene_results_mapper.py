from datetime import datetime
import json
from typing import Any, Dict, Optional

from models.patient_models import Gene, GeneResultReport, GeneResultsGrouped


class GeneResultsMapper:
    def __init__(self):
        # Load the genes-panels.json configuration
        with open("genes-panels.json", "r") as file:
            self.panels_config = json.load(file)

        # Create panel name mappings for easier access
        self.panel_mappings = {
            "Vitamin D": "vitamin_d",
            "Serum Glucose": "serum_glucose",
            "Sex Hormones": "sex_hormones",
            "Thyroid Function": "thyroid_function",
            "Lipids": "lipids",
            "CBC": "cbc",
            "Vitamins B": "vitamins_b",
            "Minerals - Detox": "minerals_detox",
            "Hormones": "hormones",
        }

    @staticmethod
    def parse_gene_result(response: Dict[str, Any], gene_name: str) -> Optional[str]:
        """Helper function to parse gene result from the response."""
        return response.get(gene_name, None)

    def get_risk_level_for_genotype(self, gene_name: str, genotype: str, rs_id: str = None) -> str:
        """
        Determine risk level based on genotype and genes-panels.json configuration
        """
        for panel in self.panels_config["panels"]:
            for gene in panel["genes"]:
                # Match by gene name and optionally rs_id
                if gene["name"] == gene_name and (not rs_id or gene.get("rs_id") == rs_id):
                    for genotype_info in gene["genotypes"]:
                        if genotype_info["genotype"] == genotype:
                            return genotype_info["risk_level"]

        # Default to normal if no match found
        return "normal"

    def get_panel_for_gene(self, gene_name: str, rs_id: str = None) -> str:
        """
        Find which panel a gene belongs to based on genes-panels.json
        """
        for panel in self.panels_config["panels"]:
            for gene in panel["genes"]:
                if gene["name"] == gene_name and (not rs_id or gene.get("rs_id") == rs_id):
                    return panel["panel"]

        # Default panel if not found
        return "Unknown"

    def map_raw_gene_to_gene_model(self, gene_name: str, genotype: str, rs_id: str = None) -> Gene:
        """
        Map a single gene result to Gene model
        """
        panel = self.get_panel_for_gene(gene_name, rs_id)
        risk_level = self.get_risk_level_for_genotype(gene_name, genotype, rs_id)

        return Gene(name=gene_name, genotype=genotype, risk_level=risk_level, rs_id=rs_id, panel=panel)

    def map_to_grouped_gene_results(self, response: Dict[str, Any]) -> GeneResultsGrouped:
        """
        Maps Gemini AI response to grouped gene results based on panels
        """
        # Initialize all panel groups
        grouped_results = {
            "vitamin_d": [],
            "serum_glucose": [],
            "sex_hormones": [],
            "thyroid_function": [],
            "lipids": [],
            "cbc": [],
            "vitamins_b": [],
            "minerals_detox": [],
            "hormones": [],
        }

        # Gene mapping with their respective rs_ids
        gene_mappings = [
            ("CYP2R1", "rs10741657"),
            ("VDR", "rs2228570"),
            ("TCF7L2", "rs7903146"),
            ("TCF7L2", "rs12255372"),
            ("MTNR1B", "rs10830963"),
            ("DIO2", "rs225014"),
            ("CYP17A1", "rs743572"),
            ("SRD5A2", "rs523349"),
            ("UGT2B15", "rs1902023"),
            ("CYP19A1", None),
            ("COMT", "rs4680"),
            ("CYP1A1", "rs1048943"),
            ("CYP1B1", "rs1056836"),
            ("GSTT1", None),
            ("GSTP1", "rs1695"),
            ("GSTM1", None),
            ("PSRC1", "rs599839"),
            ("SLCO1B1", "rs4149056"),
            ("APOE", "rs7412"),
            ("APOE", "rs429358"),
            ("MLXIPL", "rs3812316"),
            ("9P21", "rs10757278"),
            ("9P21", "rs10757274"),
            ("9P21", "rs4977574"),
            ("PCSK9", "rs11591147"),
            ("TMPRSS2", "rs2070788"),
            ("CDKN2A", "rs10757278"),
            ("PPARG", None),
            ("MTHFR", "rs1801133"),
            ("MTHFR", "rs1801131"),
            ("SOD2", "rs4880"),
            ("GPx", "rs1050450"),
            ("FOXO3", "rs2802292"),
            ("SIRT1", "rs3758391"),
            ("CYP1A2", None),
            ("HTR2A", "rs6311"),
            ("UGT2B17", None),
            ("CYP3A4", "rs2740574"),
            ("MAOA", "rs6323"),
            ("DRD2", None),
            ("ADRA2B", None),
            ("SLC6A4", None),
            ("TPH2", None),
            ("OPRM1", None),
            ("BDNF", None),
            ("CLOCK", None),
        ]

        # Process each gene from the response
        for gene_name, rs_id in gene_mappings:
            # Handle special cases for gene names in response
            response_key = gene_name
            if gene_name == "TCF7L2" and rs_id == "rs7903146":
                response_key = "TCF7L2_rs7903146"
            elif gene_name == "TCF7L2" and rs_id == "rs12255372":
                response_key = "TCF7L2_rs12255372"
            elif gene_name == "APOE" and rs_id == "rs7412":
                response_key = "APOE_rs7412"
            elif gene_name == "APOE" and rs_id == "rs429358":
                response_key = "APOE_rs429358"
            elif gene_name == "9P21" and rs_id == "rs10757278":
                response_key = "NineP21_rs10757278"
            elif gene_name == "9P21" and rs_id == "rs10757274":
                response_key = "NineP21_rs10757274"
            elif gene_name == "9P21" and rs_id == "rs4977574":
                response_key = "NineP21_rs4977574"
            elif gene_name == "MTHFR" and rs_id == "rs1801133":
                response_key = "MTHFR_rs1801133"
            elif gene_name == "MTHFR" and rs_id == "rs1801131":
                response_key = "MTHFR_rs1801131"

            genotype = self.parse_gene_result(response, response_key)

            if genotype:
                gene_model = self.map_raw_gene_to_gene_model(gene_name, genotype, rs_id)
                panel_name = self.panel_mappings.get(gene_model.panel)

                if panel_name and panel_name in grouped_results:
                    grouped_results[panel_name].append(gene_model)

        # Convert to GeneResultsGrouped model, only including non-empty lists
        return GeneResultsGrouped(
            vitamin_d=grouped_results["vitamin_d"] if grouped_results["vitamin_d"] else None,
            serum_glucose=grouped_results["serum_glucose"] if grouped_results["serum_glucose"] else None,
            sex_hormones=grouped_results["sex_hormones"] if grouped_results["sex_hormones"] else None,
            thyroid_function=grouped_results["thyroid_function"] if grouped_results["thyroid_function"] else None,
            lipids=grouped_results["lipids"] if grouped_results["lipids"] else None,
            cbc=grouped_results["cbc"] if grouped_results["cbc"] else None,
            vitamins_b=grouped_results["vitamins_b"] if grouped_results["vitamins_b"] else None,
            minerals_detox=grouped_results["minerals_detox"] if grouped_results["minerals_detox"] else None,
            hormones=grouped_results["hormones"] if grouped_results["hormones"] else None,
        )

    def map_to_gene_result_report(self, response: Dict[str, Any], collection_date: str = None) -> GeneResultReport:
        """
        Maps Gemini AI response to a complete gene result report
        """
        grouped_results = self.map_to_grouped_gene_results(response)

        return GeneResultReport(
            createdAt=datetime.now(),
            reportDate=collection_date or datetime.now().strftime("%Y-%m-%d"),
            geneResultsGrouped=grouped_results,
        )
