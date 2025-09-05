def get_gene_data(results, gene_name, rs_id=None, field="genotype"):
    """
    Get gene data by name and optionally by rs_id.
    - If rs_id is provided, matches both name and rs_id
    - If rs_id is None, matches by name only (includes genes with and without rs_id)
    - Returns single value if one match, list if multiple matches
    """
    matches = []
    for panel_genes in results["geneResultsGrouped"].values():
        for gene in panel_genes:
            if rs_id is not None:
                # Match both name and rs_id
                if gene["name"] == gene_name and gene["rs_id"] == rs_id:
                    matches.append(gene[field] if field else gene)
            else:
                # Match by name only (includes both rs_id and non-rs_id genes)
                if gene["name"] == gene_name:
                    matches.append(gene[field] if field else gene)

    return matches[0] if len(matches) == 1 else matches
