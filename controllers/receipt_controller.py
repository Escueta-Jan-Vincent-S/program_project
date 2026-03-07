from datetime import datetime
import io
import os
import sys

STORE_NAME    = "Grocery Store Ngani"
STORE_ADDRESS = "San Pablo City, Laguna"
STORE_TEL     = "TEL. NO. : ____________"

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def generate_barcode_image(receipt_no):
    try:
        import barcode
        from barcode.writer import ImageWriter
        buf = io.BytesIO()
        code = barcode.get("code128", receipt_no, writer=ImageWriter())
        code.write(buf, options={
            "module_width": 0.8,
            "module_height": 8.0,
            "font_size": 6,
            "text_distance": 2,
            "quiet_zone": 2,
            "write_text": False
        })
        buf.seek(0)
        return buf
    except:
        return None

def print_pdf(cart, receipt_no):
    try:
        from reportlab.lib.pagesizes import A6
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        from PIL import Image

        filename = os.path.join(get_base_path(), f"receipt_{receipt_no}.pdf")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c = canvas.Canvas(filename, pagesize=A6)
        w, h = A6
        y = h - 15

        def center_text(text, size=10, bold=False):
            nonlocal y
            font = "Helvetica-Bold" if bold else "Helvetica"
            c.setFont(font, size)
            c.drawCentredString(w / 2, y, text)
            y -= size + 5

        def left_right(left, right, size=10, bold=False):
            nonlocal y
            font = "Helvetica-Bold" if bold else "Helvetica"
            c.setFont(font, size)
            c.drawString(15, y, left)
            c.drawRightString(w - 15, y, right)
            y -= size + 5

        def solid_line():
            nonlocal y
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.setDash()
            c.line(10, y, w - 10, y)
            y -= 8

        def dashed_line():
            nonlocal y
            c.setDash(3, 3)
            c.line(10, y, w - 10, y)
            c.setDash()
            y -= 8

        def four_col(desc, qty, unit, amount, size=9, bold=False):
            nonlocal y
            font = "Helvetica-Bold" if bold else "Helvetica"
            c.setFont(font, size)
            c.drawString(15, y, desc[:25])
            c.drawCentredString(w * 0.52, y, str(qty))
            c.drawCentredString(w * 0.68, y, unit)
            c.drawRightString(w - 15, y, amount)
            y -= size + 5

        # Store info
        center_text(f"* {STORE_NAME} *", size=11, bold=True)
        center_text(STORE_ADDRESS, size=9)
        center_text(STORE_TEL, size=9)
        center_text(f"DATE: {now}", size=8)
        center_text(f"RECEIPT NO: {receipt_no}", size=10, bold=True)
        solid_line()
        center_text("--- OFFICIAL RECEIPT ---", size=11, bold=True)
        solid_line()

        # Column headers
        four_col("DESCRIPTION", "QTY", "UNIT PRICE", "AMOUNT", bold=True)
        dashed_line()

        # Items
        total = 0
        for item in cart:
            amount = item["selling_price"] * item["quantity"]
            total += amount
            four_col(
                item["item_name"],
                str(item["quantity"]),
                f"P{item['selling_price']:.2f}",
                f"P{amount:.2f}"
            )

        dashed_line()

        # Total only
        left_right("TOTAL", f"P{total:.2f}", bold=True)
        solid_line()

        # Barcode image
        y -= 10
        barcode_buf = generate_barcode_image(receipt_no)
        if barcode_buf:
            img = Image.open(barcode_buf)
            barcode_path = os.path.join(get_base_path(), f"_temp_barcode.png")
            img.save(barcode_path)
            barcode_w = w - 30
            barcode_h = 40
            c.drawImage(barcode_path, 15, y - barcode_h,
                        width=barcode_w, height=barcode_h)
            y -= barcode_h + 10
            c.setFont("Helvetica", 8)
            c.drawCentredString(w / 2, y, receipt_no)
            y -= 12
            try:
                os.remove(barcode_path)
            except:
                pass
        else:
            center_text("| || ||| || | ||| || |", size=14)
            center_text(receipt_no, size=9)

        solid_line()
        center_text("* THANK YOU FOR SHOPPING! *", size=10, bold=True)
        center_text("Please come again!", size=9)

        c.save()
        os.startfile(filename)
        return f"PDF saved!\n{filename}"

    except ImportError:
        return "Please install:\npip install reportlab pillow python-barcode"
    except Exception as e:
        return f"PDF Error: {str(e)}"

def print_usb(cart, receipt_no):
    try:
        from escpos.printer import Usb
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        printer = Usb(0x04b8, 0x0202)

        printer.set(align="center", bold=True)
        printer.text(f"* {STORE_NAME} *\n")
        printer.set(align="center", bold=False)
        printer.text(f"{STORE_ADDRESS}\n{STORE_TEL}\n")
        printer.text(f"DATE: {now}\n")
        printer.set(bold=True)
        printer.text(f"RECEIPT NO: {receipt_no}\n")
        printer.text("=" * 32 + "\n")
        printer.set(align="center", bold=True)
        printer.text("OFFICIAL RECEIPT\n")
        printer.text("=" * 32 + "\n")

        printer.set(align="left", bold=True)
        printer.text(f"{'DESCRIPTION':<16}{'QTY':^5}{'UNIT':>6}{'AMT':>5}\n")
        printer.text("-" * 32 + "\n")

        total = 0
        printer.set(bold=False)
        for item in cart:
            amount = item["selling_price"] * item["quantity"]
            total += amount
            name = item["item_name"][:14]
            printer.text(
                f"{name:<16}{item['quantity']:^5}"
                f"P{item['selling_price']:>5.0f}P{amount:>4.0f}\n"
            )

        printer.text("-" * 32 + "\n")
        printer.set(bold=True)
        printer.text(f"{'TOTAL':<20}P{total:.2f}\n")
        printer.text("=" * 32 + "\n")

        # Barcode
        barcode_buf = generate_barcode_image(receipt_no)
        if barcode_buf:
            printer.image(barcode_buf)
        printer.set(align="center")
        printer.text(f"\n{receipt_no}\n")
        printer.set(align="center", bold=True)
        printer.text("\n* THANK YOU FOR SHOPPING! *\n")
        printer.text("Please come again!\n\n\n")
        printer.cut()

        return "Printed successfully!"

    except ImportError:
        return "Please install:\npip install python-escpos"
    except Exception:
        return "No printer detected!\nMake sure USB thermal\nprinter is connected."