def format_rupiah(value):
            """Format angka menjadi mata uang Rupiah."""
            try:
                return f"Rp {value:,.0f}".replace(",", ".")
            except (ValueError, TypeError):
                return "Rp 0"
