from male_report.gene_report.page_0_g import cover_page
from male_report.gene_report.page_1_g import page_1_g
from male_report.gene_report.page_2_g import page_2_g
from male_report.gene_report.page_3_g import page_3_g
from male_report.gene_report.page_4_g import page_4_g
from male_report.gene_report.page_5_g import page_5_g
from male_report.gene_report.page_6_g import page_6_g
from male_report.gene_report.page_7_g import page_7_g
from male_report.gene_report.page_8_g import page_8_g
from male_report.gene_report.page_9_g import page_9_g
from male_report.gene_report.page_10_g import page_10_g
from male_report.gene_report.page_11_g import page_11_g
from male_report.gene_report.page_12_g import page_12_g


def generate_gene_report_pages(gene_report):
    return [
        cover_page(gene_report),
        page_1_g(gene_report),
        page_2_g(gene_report),
        page_3_g(gene_report),
        page_4_g(gene_report),
        page_5_g(gene_report),
        page_6_g(gene_report),
        page_7_g(gene_report),
        page_8_g(gene_report),
        page_9_g(gene_report),
        page_10_g(gene_report),
        page_11_g(gene_report),
        page_12_g(gene_report),
    ]
