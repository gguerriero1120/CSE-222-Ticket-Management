"""Theater seating display (Milestone #2 - begins the seat-selection UI).

The seating chart is drawn on a Canvas so it works without any image file.
If a theater GIF named THEATER_GIF exists next to the program it is shown as
a background instead of the plain stage drawing.
"""
import os
import random
import tkinter as tk
from tkinter import messagebox

from ui_util import center_window

THEATER_GIF = "theater.gif"

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

SEAT, GAP = 22, 4
COLORS = {"open": "#7bc67b", "sold": "#9a9a9a", "chosen": "#f5c518"}


class TheaterGUI:
    def __init__(self, window, pricing, on_exit):
        """Builds the theater UI inside `window` (the main window)."""
        self.window = window
        self.pricing = pricing
        self.on_exit = on_exit
        self.seats = {}          # seat id -> dict(item, section, state)
        self.chosen = []         # seat ids in the order chosen
        self._build()

    # ------------------------------------------------------------ layout
    def _build(self):
        w = self.window
        w.title(f"Theater Ticket System - {self.pricing} Showing")
        w.resizable(False, False)
        center_window(w, 960, 640)

        tk.Label(w, text=f"{self.pricing} Showing", font=("Georgia", 16),
                 fg="purple").grid(row=0, column=0, columnspan=2, pady=(8, 2))

        self.canvas = tk.Canvas(w, width=640, height=540, bg="white",
                                highlightthickness=1,
                                highlightbackground="#999")
        self.canvas.grid(row=1, column=0, padx=10, pady=5)
        self._draw_theater()

        panel = tk.Frame(w, width=280)
        panel.grid(row=1, column=1, sticky="N", padx=10, pady=5)

        tk.Label(panel, text="Ticket Prices", font=("Georgia", 12, "bold")
                 ).pack(anchor="w")
        for sec, price in PRICES[self.pricing].items():
            tk.Label(panel, text=f"  {sec:<10} ${price:.2f}",
                     font=("Courier", 10)).pack(anchor="w")

        legend = tk.Frame(panel)
        legend.pack(anchor="w", pady=8)
        for text, key in (("Open", "open"), ("Sold", "sold"),
                          ("Selected", "chosen")):
            tk.Label(legend, bg=COLORS[key], width=2, relief="solid", bd=1
                     ).pack(side="left", padx=(0, 3))
            tk.Label(legend, text=text, font=("Helvetica", 9)
                     ).pack(side="left", padx=(0, 10))

        tk.Label(panel, text="Selected Seats", font=("Georgia", 12, "bold")
                 ).pack(anchor="w", pady=(6, 0))
        self.listbox = tk.Listbox(panel, width=34, height=11,
                                  font=("Courier", 10))
        self.listbox.pack(pady=3)

        self.total_label = tk.Label(panel, text="Total: $0.00",
                                    font=("Georgia", 13, "bold"))
        self.total_label.pack(anchor="e", pady=4)

        tk.Button(panel, text="Purchase Tickets", width=24,
                  command=self.purchase).pack(pady=3)
        tk.Button(panel, text="Clear Selection", width=24,
                  command=self.clear_selection).pack(pady=3)
        tk.Button(panel, text="Exit", width=24,
                  command=self.on_exit).pack(pady=3)

        self.status = tk.Label(w, text="Click a seat to select it. "
                               "Click again to deselect.",
                               font=("Helvetica", 9), anchor="w")
        self.status.grid(row=2, column=0, columnspan=2, sticky="W", padx=12)

    def _draw_theater(self):
        c = self.canvas
        if os.path.exists(THEATER_GIF):
            try:
                self.bg_image = tk.PhotoImage(file=THEATER_GIF)
                c.create_image(0, 0, image=self.bg_image, anchor="nw")
            except tk.TclError:
                self._draw_stage()
        else:
            self._draw_stage()

        rng = random.Random(42)              # same "sold" seats every run
        y = 70
        for section, (rows, count) in SECTIONS.items():
            c.create_text(320, y - 8, text=section.upper(),
                          font=("Helvetica", 8, "bold"), fill="#555")
            row_w = count * (SEAT + GAP) - GAP
            x0 = (640 - row_w) // 2
            for row in rows:
                c.create_text(x0 - 14, y + SEAT // 2, text=row,
                              font=("Helvetica", 9, "bold"))
                for n in range(1, count + 1):
                    x = x0 + (n - 1) * (SEAT + GAP)
                    sid = f"{row}{n}"
                    state = "sold" if rng.random() < 0.18 else "open"
                    item = c.create_rectangle(x, y, x + SEAT, y + SEAT,
                                              fill=COLORS[state],
                                              outline="#333")
                    self.seats[sid] = {"item": item, "section": section,
                                       "state": state}
                    c.tag_bind(item, "<Button-1>",
                               lambda e, s=sid: self.click_seat(s))
                y += SEAT + GAP
            y += 26                          # gap between sections

    def _draw_stage(self):
        self.canvas.create_rectangle(120, 10, 520, 45, fill="#6a3d9a",
                                     outline="#333")
        self.canvas.create_text(320, 28, text="S T A G E", fill="white",
                                font=("Georgia", 12, "bold"))

    # ---------------------------------------------------------- behavior
    def click_seat(self, sid):
        seat = self.seats[sid]
        if seat["state"] == "sold":
            self.status.config(text=f"Seat {sid} is already sold.")
            return
        if seat["state"] == "open":
            seat["state"] = "chosen"
            self.chosen.append(sid)
        else:
            seat["state"] = "open"
            self.chosen.remove(sid)
        self.canvas.itemconfig(seat["item"], fill=COLORS[seat["state"]])
        self._refresh()

    def _price(self, sid):
        return PRICES[self.pricing][self.seats[sid]["section"]]

    def _refresh(self):
        self.listbox.delete(0, tk.END)
        total = 0.0
        for sid in self.chosen:
            price = self._price(sid)
            total += price
            self.listbox.insert(
                tk.END, f"{sid:<4}{self.seats[sid]['section']:<11}${price:>6.2f}")
        self.total_label.config(text=f"Total: ${total:.2f}")
        self.status.config(text=f"{len(self.chosen)} seat(s) selected.")

    def clear_selection(self):
        for sid in self.chosen:
            self.seats[sid]["state"] = "open"
            self.canvas.itemconfig(self.seats[sid]["item"],
                                   fill=COLORS["open"])
        self.chosen = []
        self._refresh()

    def purchase(self):
        # Placeholder - full purchase logic comes in a later milestone.
        if not self.chosen:
            messagebox.showwarning("No Seats", "Please select at least one "
                                   "seat first.", parent=self.window)
            return
        messagebox.showinfo("Purchase", "Purchase processing will be "
                            "implemented in the next milestone.",
                            parent=self.window)
