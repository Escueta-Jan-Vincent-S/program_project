from datetime import datetime

STORE_NAME    = "LANZ & LINDLY MINIMART"
STORE_ADDRESS = "****ADDRESS****"
STORE_TEL     = "TEL. NO."

def print_pdf(cart, receipt_no):
    try:
        from reportlab.lib.pagesizes import A6
        from reportlab.pdfgen import canvas
        import os, sys

        # Output path
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))

        filename = os.path.join(base, f"receipt_{receipt_no}.pdf")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c = canvas.Canvas(filename, pagesize=A6)
        w, h = A6
        y = h - 20

        def line(text, font="Helvetica", size=10, bold=False):
            nonlocal y
            if bold:
                font = "Helvetica-Bold"
            c.setFont(font, size)
            c.drawCentredString(w / 2, y, text)
            y -= size + 4

        def divider():
            nonlocal y
            c.line(10, y, w - 10, y)
            y -= 8

        line(STORE_NAME, size=12, bold=True)
        line(STORE_ADDRESS)
        line(STORE_TEL)
        line(f"RECEIPT NO. {receipt_no}")
        line(now, size=9)
        divider()
        line("RECEIPT", size=12, bold=True)
        divider()

        # Items
        total = 0
        for item in cart:
            amount = item["selling_price"] * item["quantity"]
            total += amount
            c.setFont("Helvetica", 9)
            c.drawString(10, y, f"{item['item_name']} x{item['quantity']}")
            c.drawRightString(w - 10, y, f"P{amount:.2f}")
            y -= 14

        divider()

        for label, value in [("TOTAL", f"P{total:.2f}"), ("CASH", "P0.00"), ("CHANGE", "P0.00")]:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(10, y, label)
            c.drawRightString(w - 10, y, value)
            y -= 14

        divider()
        line("THANK YOU", bold=True)

        c.save()

        # Open PDF automatically
        os.startfile(filename)
        return f"PDF saved!\n{filename}"

    except ImportError:
        return "Please install reportlab:\npip install reportlab"
    except Exception as e:
        return f"PDF Error: {str(e)}"

def print_usb(cart, receipt_no):
    try:
        from escpos.printer import Usb
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Common thermal printer USB vendor/product IDs
        # Adjust these to match your printer
        printer = Usb(0x04b8, 0x0202)

        printer.set(align="center", bold=True)
        printer.text(f"{STORE_NAME}\n")
        printer.set(align="center", bold=False)
        printer.text(f"{STORE_ADDRESS}\n{STORE_TEL}\n")
        printer.text(f"RECEIPT NO. {receipt_no}\n{now}\n")
        printer.text("-" * 32 + "\n")
        printer.set(align="center", bold=True)
        printer.text("RECEIPT\n")
        printer.text("-" * 32 + "\n")

        total = 0
        printer.set(align="left", bold=False)
        for item in cart:
            amount = item["selling_price"] * item["quantity"]
            total += amount
            printer.text(f"{item['item_name']} x{item['quantity']}\n")
            printer.text(f"  P{amount:.2f}\n")

        printer.text("-" * 32 + "\n")
        printer.set(bold=True)
        printer.text(f"TOTAL   P{total:.2f}\n")
        printer.text(f"CASH    P0.00\n")
        printer.text(f"CHANGE  P0.00\n")
        printer.text("-" * 32 + "\n")
        printer.set(align="center", bold=True)
        printer.text("THANK YOU\n\n\n")
        printer.cut()

        return "Printed successfully!"

    except ImportError:
        return "Please install escpos:\npip install python-escpos"
    except Exception:
        return "No printer detected!\nMake sure USB thermal\nprinter is connected."