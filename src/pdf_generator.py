import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_compliance_pdf(output_path: str, case_data: dict):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#0D1117'),
        spaceAfter=12
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#FF6B00'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#24292E'),
        leading=13
    )

    # Document Header
    story.append(Paragraph("FRAUDGUARD AI — COMPLIANCE AUDIT REPORT", title_style))
    story.append(Paragraph("CONFIDENTIAL // REGULATORY & LEGAL CASE FILE", ParagraphStyle('Sub', parent=body_style, textColor=colors.HexColor('#57606A'))))
    story.append(Spacer(1, 15))

    # Case Metadata Table
    meta_data = [
        ["Transaction Hash", case_data.get("transaction_hash", "N/A")],
        ["Origin Account", case_data.get("account_id", "N/A")],
        ["Destination Account", case_data.get("dest_account_id", "N/A")],
        ["Amount (INR)", f"INR {case_data.get('transaction_amount', 0.0):,.2f}"],
        ["Risk Score / Band", f"{case_data.get('assessment', {}).get('final_risk_score', 0.0):.1f}/100 ({case_data.get('assessment', {}).get('risk_band', 'N/A')})"],
        ["Recommended Action", case_data.get("investigation_report", {}).get("action", "AUTO_APPROVE")]
    ]
    
    t_meta = Table(meta_data, colWidths=[150, 390])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F6F8FA')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#24292E')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # AI Audit Summary
    story.append(Paragraph("AI INVESTIGATOR SUMMARY", section_heading))
    summary_text = case_data.get("investigation_report", {}).get("investigation_summary", "No summary available.").replace("$", "INR ")
    story.append(Paragraph(summary_text.replace('\n', '<br/>'), body_style))
    story.append(Spacer(1, 15))

    # SHAP Attribution Table
    story.append(Paragraph("TOP RISK DRIVERS (SHAP EXPLAINABILITY)", section_heading))
    drivers = case_data.get("explainability", {}).get("top_risk_drivers", [])
    
    driver_rows = [["Feature Name", "SHAP Impact Score"]]
    for d in drivers:
        driver_rows.append([d.get("feature", "N/A"), f"{d.get('shap_value', 0.0):.4f}"])
        
    t_drivers = Table(driver_rows, colWidths=[300, 240])
    t_drivers.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#161B22')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FFFFFF')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
    ]))
    story.append(t_drivers)

    doc.build(story)