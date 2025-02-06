import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import io
import os

def create_unique_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    # Get the default style sheet
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1B4F72'),
        spaceAfter=25,
        alignment=1
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2E86C1'),
        spaceAfter=15
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=10
    )

    # Content elements
    elements = []
    
    # Title
    elements.append(Paragraph("SERVICE AGREEMENT", title_style))
    elements.append(Spacer(1, 20))
    
    # Reference and Date
    ref_date_data = [
        ['Reference Number:', data['ref_number']],
        ['Date:', data['date']]
    ]
    ref_date_table = Table(ref_date_data, colWidths=[2*inch, 4*inch])
    ref_date_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(ref_date_table)
    elements.append(Spacer(1, 20))
    
    # Client Information
    elements.append(Paragraph("CLIENT INFORMATION", header_style))
    client_data = [
        ['Client Name:', data['client_name']],
        ['Email:', data['client_email']],
        ['Registration Number:', data['registration_number']]
    ]
    client_table = Table(client_data, colWidths=[2*inch, 4*inch])
    client_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8F9FA')),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elements.append(client_table)
    elements.append(Spacer(1, 20))
    
    # Service Details
    elements.append(Paragraph("SERVICE DETAILS", header_style))
    service_data = [
        ['Service Type:', data['service_type']],
        ['Service Provider:', data['service_provider']],
        ['Service Fee:', f"{data['currency']} {data['fee_amount']}"]
    ]
    service_table = Table(service_data, colWidths=[2*inch, 4*inch])
    service_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8F9FA')),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    elements.append(service_table)
    elements.append(Spacer(1, 20))
    
    # Scope of Work
    elements.append(Paragraph("SCOPE OF WORK", header_style))
    elements.append(Paragraph(data['scope_of_work'], normal_style))
    
    # Build PDF with border
    def add_border(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#1B4F72'))
        canvas.setLineWidth(2)
        # Draw border
        canvas.rect(20, 20, doc.pagesize[0] - 40, doc.pagesize[1] - 40)
        canvas.restoreState()
    
    # Build the document
    doc.build(elements, onFirstPage=add_border, onLaterPages=add_border)
    buffer.seek(0)
    return buffer

def main():
    st.title("Professional Service Agreement Generator")
    st.markdown("---")

    with st.form("service_agreement_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Agreement Details")
            ref_number = st.text_input("Reference Number", placeholder="e.g., SA-2024-001")
            date = st.date_input("Agreement Date")
            client_name = st.text_input("Client Name")
            client_email = st.text_input("Client Email")

        with col2:
            st.subheader("Service Details")
            service_type = st.selectbox(
                "Service Type",
                ["VAT Services", "Business Support", "Consultancy", "Other"]
            )
            registration_number = st.text_input("Commercial Registration Number")
            service_provider = st.text_input("Service Provider Name")
            
        st.subheader("Additional Information")
        scope_of_work = st.text_area("Scope of Work", height=100)
        
        col3, col4 = st.columns(2)
        with col3:
            fee_amount = st.number_input("Service Fee", min_value=0.0, step=0.01)
        with col4:
            currency = st.selectbox("Currency", ["BHD", "USD", "EUR", "GBP"])

        submitted = st.form_submit_button("Generate Agreement")

    if submitted:
        if ref_number and client_name and service_provider:
            # Prepare data
            pdf_data = {
                'ref_number': ref_number,
                'date': date.strftime("%d-%m-%Y"),
                'client_name': client_name,
                'client_email': client_email,
                'service_type': service_type,
                'registration_number': registration_number,
                'service_provider': service_provider,
                'scope_of_work': scope_of_work,
                'fee_amount': fee_amount,
                'currency': currency
            }

            # Generate PDF
            pdf_buffer = create_unique_pdf(pdf_data)
            
            # Save PDF
            filename = f"service_agreement_{ref_number}_{date.strftime('%Y%m%d')}.pdf"
            
            # Provide download button
            st.success("✅ Service Agreement generated successfully!")
            st.download_button(
                label="📥 Download Service Agreement",
                data=pdf_buffer,
                file_name=filename,
                mime="application/pdf"
            )
        else:
            st.error("Please fill in all required fields")

if __name__ == "__main__":
    main()