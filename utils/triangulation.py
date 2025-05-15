import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def process_ab_measurements(ab_pairs, ab_length_feet, job_name):
    coords = []
    A = (0, 0)
    B = (ab_length_feet * 12, 0)
    for a, b in ab_pairs:
        x = (a**2 - b**2 + (B[0])**2) / (2*B[0])
        y = (a**2 - x**2)**0.5 if a > x else 0
        coords.append((x, y))

    fig, ax = plt.subplots()
    xs, ys = zip(*coords)
    ax.plot(xs, ys, marker='o')
    ax.set_title("Triangulated Pool")
    plot_path = f"plots/{job_name}.png"
    fig.savefig(plot_path)
    plt.close()

    pdf_path = f"reports/{job_name}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Pool Plot Report", ln=True, align="C")
    pdf.image(plot_path, x=10, y=30, w=180)
    pdf.output(pdf_path)

    return coords, pdf_path