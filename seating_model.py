"""Seat selection algorithm and per-section sales tracking (no GUI code).

The theater display (theater_display.py) calls this module, so the rules can
be tested without opening a window.
"""

# Section name -> (rows, seats per row)
SECTIONS = {
    "Orchestra": ("ABCDEFGH", 14),
    "Mezzanine": ("IJKL", 16),
    "Balcony": ("MNO", 18),
}
PRICES = {
    "Matinee": {"Orchestra": 15.00, "Mezzanine": 12.00, "Balcony": 9.00},
    "Evening": {"Orchestra": 25.00, "Mezzanine": 20.00, "Balcony": 14.00},
}
MAX_PER_ORDER = 8


class SeatingModel:
    def __init__(self, pricing, pre_sold=()):
        self.pricing = pricing
        self.section_of = {}        # seat id -> section name
        self.rows = {}              # section -> list of rows, each a list of seat ids
        for section, (row_letters, count) in SECTIONS.items():
            self.rows[section] = []
            for letter in row_letters:
                row = [f"{letter}{n}" for n in range(1, count + 1)]
                self.rows[section].append(row)
                for sid in row:
                    self.section_of[sid] = section
        self.sold = set()           # seats already purchased
        self.chosen = []            # seats selected, not yet purchased
        self.sold_count = {s: 0 for s in SECTIONS}      # seats sold per section
        self.receipts = {s: 0.0 for s in SECTIONS}      # dollars per section
        for sid in pre_sold:
            self._mark_sold(sid)

    # ------------------------------------------------------------ queries
    def capacity(self, section):
        return sum(len(r) for r in self.rows[section])

    def sold_in(self, section):
        return self.sold_count[section]

    def chosen_in(self, section):
        return sum(1 for s in self.chosen if self.section_of[s] == section)

    def remaining(self, section):
        """Seats in the section that are neither sold nor currently selected."""
        return self.capacity(section) - self.sold_count[section] \
            - self.chosen_in(section)

    def section_sold_out(self, section):
        return self.sold_count[section] >= self.capacity(section)

    def theater_sold_out(self):
        return all(self.section_sold_out(s) for s in SECTIONS)

    def price(self, seat_id):
        return PRICES[self.pricing][self.section_of[seat_id]]

    def total(self):
        return sum(self.price(s) for s in self.chosen)

    def total_receipts(self):
        return sum(self.receipts.values())

    def total_sold(self):
        return sum(self.sold_count.values())

    def open_sections(self):
        """Sections that still have seats that can be sold."""
        return [s for s in SECTIONS if not self.section_sold_out(s)]

    # --------------------------------------------------------- selection
    def toggle(self, seat_id):
        """Click on a seat. Returns (changed, message)."""
        if seat_id not in self.section_of:
            return False, "That seat does not exist."
        if seat_id in self.sold:
            return False, f"Seat {seat_id} is already sold."
        if seat_id in self.chosen:
            self.chosen.remove(seat_id)
            return True, f"Seat {seat_id} unselected."
        if len(self.chosen) >= MAX_PER_ORDER:
            return False, f"You can buy at most {MAX_PER_ORDER} seats at a time."
        self.chosen.append(seat_id)
        return True, f"Seat {seat_id} selected."

    def auto_select(self, section, quantity):
        """Select `quantity` seats in `section` from the option lists.

        Looks for the first row (front to back) with enough open seats side by
        side. If no row has them together, takes the first open seats in
        order. Returns (list of seats selected, message).
        """
        if section not in SECTIONS:
            return [], "Please choose a section."
        if self.section_sold_out(section):
            return [], f"{section} is sold out."
        if not 1 <= quantity <= MAX_PER_ORDER:
            return [], f"Choose between 1 and {MAX_PER_ORDER} seats."
        if len(self.chosen) + quantity > MAX_PER_ORDER:
            return [], (f"You can buy at most {MAX_PER_ORDER} seats at a time "
                        f"({len(self.chosen)} already selected).")
        if quantity > self.remaining(section):
            return [], (f"Only {self.remaining(section)} seat(s) left in "
                        f"{section}.")

        def free(sid):
            return sid not in self.sold and sid not in self.chosen

        picked = None
        for row in self.rows[section]:              # 1. together in one row
            run = []
            for sid in row:
                run = run + [sid] if free(sid) else []
                if len(run) == quantity:
                    picked = run
                    break
            if picked:
                break
        together = picked is not None
        if not picked:                              # 2. any open seats
            picked = [sid for row in self.rows[section]
                      for sid in row if free(sid)][:quantity]
        self.chosen.extend(picked)
        where = "together" if together else "(not all together)"
        return picked, f"Selected {', '.join(picked)} {where}."

    def clear_selection(self):
        released = list(self.chosen)
        self.chosen = []
        return released

    # ---------------------------------------------------------- purchase
    def _mark_sold(self, seat_id):
        section = self.section_of[seat_id]
        self.sold.add(seat_id)
        self.sold_count[section] += 1

    def purchase(self):
        """Buy the selected seats. Returns the list of (seat, section, price)."""
        bought = []
        for sid in self.chosen:
            if sid in self.sold:                    # defensive: never sell twice
                continue
            section = self.section_of[sid]
            price = self.price(sid)
            self._mark_sold(sid)
            self.receipts[section] += price
            bought.append((sid, section, price))
        self.chosen = []
        return bought
