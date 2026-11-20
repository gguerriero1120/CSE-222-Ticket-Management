"""Theater seating display (Milestone #3).

Customers can pick seats two ways:
  1. click seats directly on the seating chart, or
  2. choose a section from an option list and a number of seats, then press
     "Select Seats" (the program finds the best open seats in that section).

The rules and the per-section counts live in seating_model.py.
If a theater GIF named THEATER_GIF exists next to the program it is shown as
the canvas background instead of the plain stage drawing.
"""
import os
import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

from seating_model import SECTIONS, PRICES, MAX_PER_ORDER, SeatingModel
from ui_util import center_window

THEATER_GIF = "theater.gif"
SHOW_TIMES = [(14, 0), (20, 0)]          # 2:00 PM and 8:00 PM shows

SEAT, GAP = 22, 4
COLORS = {"open": "#7bc67b", "sold": "#9a9a9a", "chosen": "#f5c518"}
CANVAS_W, CANVAS_H = 640, 540


def next_show_text(now=None):
    """Return the next show time after `now`, e.g. '8:00 PM'."""
    now = now or time.localtime()
    minutes = now.tm_hour * 60 + now.tm_min
    for hour, minute in SHOW_TIMES:
        if hour * 60 + minute > minutes:
            break
    else:
        hour, minute = SHOW_TIMES[0]     # none left today: first show tomorrow
    suffix = "AM" if hour < 12 else "PM"
    return f"{(hour - 1) % 12 + 1}:{minute:02d} {suffix}"


class TheaterGUI:
    def __init__(self, window, pricing, on_exit):
        """Builds the theater UI inside `window` (the main window)."""
        self.window = window
        self.pricing = pricing
        self.on_exit = on_exit
        rng = random.Random(42)           # same "sold" seats every run
        every_seat = SeatingModel(pricing).section_of
        pre_sold = [s for s in every_seat if rng.random() < 0.18]
        self.model = SeatingModel(pricing, pre_sold)
        self.items = {}                   # seat id -> canvas item
        self.order_no = 1000              # last ticket order number
        self._build()
        self._tick()
        self._refresh()

    # ------------------------------------------------------------ layout
    def _build(self):
        w = self.window
        w.title(f"Theater Ticket System - {self.pricing} Showing")
        w.resizable(False, False)
        center_window(w, 1010, 680)

        tk.Label(w, text=f"{self.pricing} Showing", font=("Georgia", 16),
                 fg="purple").grid(row=0, column=0, pady=(8, 2))
        self.banner = tk.Label(w, text="", font=("Georgia", 12, "bold"),
                               fg="white", bg=w.cget("bg"))
        self.banner.grid(row=0, column=1, sticky="EW", padx=10, pady=(8, 2))

        self.canvas = tk.Canvas(w, width=CANVAS_W, height=CANVAS_H,
                                bg="white", highlightthickness=1,
                                highlightbackground="#999")
        self.canvas.grid(row=1, column=0, padx=10, pady=5, sticky="N")
        self._draw_theater()

        panel = tk.Frame(w)
        panel.grid(row=1, column=1, sticky="N", padx=10, pady=5)

        # current time / next show time
        clock = tk.Frame(panel)
        clock.pack(fill="x")
        self.time_label = tk.Label(clock, font=("Helvetica", 10, "bold"),
                                   anchor="w")
        self.time_label.pack(side="left")
        self.show_label = tk.Label(clock, font=("Helvetica", 10, "bold"),
                                   anchor="e")
        self.show_label.pack(side="right")

        # option lists: section + number of seats
        pick = tk.LabelFrame(panel, text=" Select seating ",
                             font=("Georgia", 10, "bold"), padx=8, pady=4)
        pick.pack(fill="x", pady=6)
        tk.Label(pick, text="Section:", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky="E", pady=3)
        self.section_var = tk.StringVar()
        self.section_box = ttk.Combobox(pick, textvariable=self.section_var,
                                        state="readonly", width=26)
        self.section_box.grid(row=0, column=1, padx=6)
        self.section_box.bind("<<ComboboxSelected>>", self._section_changed)
        tk.Label(pick, text="Seats:", font=("Helvetica", 10)).grid(
            row=1, column=0, sticky="E", pady=3)
        self.qty_var = tk.StringVar(value="1")
        self.qty_box = tk.Spinbox(pick, from_=1, to=MAX_PER_ORDER, width=5,
                                  textvariable=self.qty_var, justify="right",
                                  state="readonly")
        self.qty_box.grid(row=1, column=1, sticky="W", padx=6)
        self.select_btn = tk.Button(pick, text="Select Seats", width=14,
                                    command=self.select_from_lists)
        self.select_btn.grid(row=2, column=0, columnspan=2, pady=4)
        self.price_label = tk.Label(pick, text="", font=("Helvetica", 9),
                                    fg="#333")
        self.price_label.grid(row=3, column=0, columnspan=2)

        # per-section sales table
        tk.Label(panel, text="Seats by Section", font=("Georgia", 11, "bold")
                 ).pack(anchor="w")
        table = tk.Frame(panel)
        table.pack(fill="x")
        for col, head in enumerate(("Section", "Price", "Sold", "Left")):
            tk.Label(table, text=head, font=("Helvetica", 9, "bold"),
                     width=10 if col == 0 else 7,
                     anchor="w" if col == 0 else "e").grid(row=0, column=col)
        self.section_rows = {}
        for r, sec in enumerate(SECTIONS, start=1):
            labels = []
            for col in range(4):
                lab = tk.Label(table, font=("Courier", 10),
                               width=10 if col == 0 else 7,
                               anchor="w" if col == 0 else "e")
                lab.grid(row=r, column=col)
                labels.append(lab)
            self.section_rows[sec] = labels

        legend = tk.Frame(panel)
        legend.pack(anchor="w", pady=6)
        for text, key in (("Open", "open"), ("Sold", "sold"),
                          ("Selected", "chosen")):
            tk.Label(legend, bg=COLORS[key], width=2, relief="solid", bd=1
                     ).pack(side="left", padx=(0, 3))
            tk.Label(legend, text=text, font=("Helvetica", 9)
                     ).pack(side="left", padx=(0, 10))

        tk.Label(panel, text="Selected Seats", font=("Georgia", 11, "bold")
                 ).pack(anchor="w")
        self.listbox = tk.Listbox(panel, width=38, height=6,
                                  font=("Courier", 10))
        self.listbox.pack(pady=3)
        self.total_label = tk.Label(panel, text="Total: $0.00",
                                    font=("Georgia", 13, "bold"))
        self.total_label.pack(anchor="e", pady=2)

        self.buy_btn = tk.Button(panel, text="Purchase Tickets", width=24,
                                 command=self.purchase)
        self.buy_btn.pack(pady=2)
        self.clear_btn = tk.Button(panel, text="Clear Selection", width=24,
                                   command=self.clear_selection)
        self.clear_btn.pack(pady=2)
        tk.Button(panel, text="Exit", width=24, command=self.on_exit
                  ).pack(pady=2)

        self.status = tk.Label(w, text="Click a seat, or choose a section and "
                               "number of seats.", font=("Helvetica", 9),
                               anchor="w")
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

        y = 70
        self.section_label_items = {}
        for section, (rows, count) in SECTIONS.items():
            self.section_label_items[section] = c.create_text(
                320, y - 8, text=section.upper(),
                font=("Helvetica", 8, "bold"), fill="#555")
            row_w = count * (SEAT + GAP) - GAP
            x0 = (CANVAS_W - row_w) // 2
            for row in rows:
                c.create_text(x0 - 14, y + SEAT // 2, text=row,
                              font=("Helvetica", 9, "bold"))
                for n in range(1, count + 1):
                    x = x0 + (n - 1) * (SEAT + GAP)
                    sid = f"{row}{n}"
                    item = c.create_rectangle(x, y, x + SEAT, y + SEAT,
                                              outline="#333")
                    self.items[sid] = item
                    c.tag_bind(item, "<Button-1>",
                               lambda e, s=sid: self.click_seat(s))
                y += SEAT + GAP
            y += 26

    def _draw_stage(self):
        self.canvas.create_rectangle(120, 10, 520, 45, fill="#6a3d9a",
                                     outline="#333")
        self.canvas.create_text(320, 28, text="S T A G E", fill="white",
                                font=("Georgia", 12, "bold"))

    # ------------------------------------------------------------- clock
    def _tick(self):
        try:
            self.time_label.config(
                text="Current Time: " + time.strftime("%I:%M %p").lstrip("0"))
            self.show_label.config(text="Next Show Time: " + next_show_text())
            self.window.after(1000, self._tick)
        except tk.TclError:
            pass                      # window was closed or rebuilt

    # ---------------------------------------------------------- behavior
    def click_seat(self, sid):
        if self.model.theater_sold_out():
            return
        changed, msg = self.model.toggle(sid)
        self.status.config(text=msg)
        if changed:
            self._refresh()

    def _section_changed(self, event=None):
        sec = self._selected_section()
        if sec:
            self.price_label.config(
                text=f"The price of a {sec} seat is "
                     f"${PRICES[self.pricing][sec]:.2f}")

    def _selected_section(self):
        return self.section_var.get().split(" - ")[0] \
            if self.section_var.get() else ""

    def select_from_lists(self):
        section = self._selected_section()
        if not section:
            messagebox.showwarning("Section", "Please choose a section first.",
                                   parent=self.window)
            return
        try:
            qty = int(self.qty_var.get())
        except ValueError:
            qty = 0
        picked, msg = self.model.auto_select(section, qty)
        self.status.config(text=msg)
        if not picked:
            messagebox.showwarning("Cannot Select Seats", msg,
                                   parent=self.window)
        self._refresh()

    def clear_selection(self):
        self.model.clear_selection()
        self.status.config(text="Selection cleared.")
        self._refresh()

    def purchase(self):
        m = self.model
        if not m.chosen:
            messagebox.showwarning("No Seats", "Please select at least one "
                                   "seat first.", parent=self.window)
            return
        lines = "\n".join(f"{s}  {m.section_of[s]}  ${m.price(s):.2f}"
                          for s in m.chosen)
        if not messagebox.askyesno(
                "Confirm Purchase",
                f"Buy these seats?\n\n{lines}\n\nTotal: ${m.total():.2f}",
                parent=self.window):
            return
        bought = m.purchase()
        total = sum(p for _, _, p in bought)
        self.status.config(text=f"Purchased {len(bought)} seat(s) for "
                                f"${total:.2f}. Thank you!")
        self.order_no += 1
        self._refresh()
        self.show_ticket(self.order_no, bought, total)

    def show_ticket(self, order_no, bought, total):
        """Display the ticket(s) for a completed purchase in its own window."""
        win = tk.Toplevel(self.window)
        win.title(f"Ticket - Order {order_no}")
        win.resizable(False, False)
        win.transient(self.window)
        height = 250 + 22 * len(bought)
        center_window(win, 380, height)

        tk.Label(win, text="UPTOWN THEATER", font=("Georgia", 16, "bold"),
                 fg="purple").pack(pady=(12, 0))
        tk.Label(win, text=f"{self.pricing} Showing", font=("Georgia", 11)
                 ).pack()
        tk.Label(win, text=time.strftime("Purchased %m/%d/%Y  %I:%M %p"),
                 font=("Helvetica", 9)).pack()
        tk.Label(win, text=f"Order #{order_no}   Next show: "
                           f"{next_show_text()}",
                 font=("Helvetica", 9)).pack(pady=(0, 6))

        tk.Label(win, text="-" * 44, font=("Courier", 9)).pack()
        tk.Label(win, text=f"{'Seat':<6}{'Section':<12}{'Price':>8}",
                 font=("Courier", 10, "bold")).pack()
        for sid, section, price in bought:
            tk.Label(win, text=f"{sid:<6}{section:<12}${price:>7.2f}",
                     font=("Courier", 10)).pack()
        tk.Label(win, text="-" * 44, font=("Courier", 9)).pack()
        tk.Label(win, text=f"Total: ${total:.2f}",
                 font=("Georgia", 12, "bold")).pack(anchor="e", padx=30)
        tk.Label(win, text="Please keep this ticket. Enjoy the show!",
                 font=("Helvetica", 9)).pack(pady=4)
        tk.Button(win, text="Close", width=14, command=win.destroy
                  ).pack(pady=6)
        win.focus_set()

    # ---------------------------------------------------------- redrawing
    def _refresh(self):
        m = self.model
        # seat colors
        for sid, item in self.items.items():
            state = ("sold" if sid in m.sold else
                     "chosen" if sid in m.chosen else "open")
            self.canvas.itemconfig(item, fill=COLORS[state])

        # selected list and total
        self.listbox.delete(0, tk.END)
        for sid in m.chosen:
            self.listbox.insert(
                tk.END, f"{sid:<4}{m.section_of[sid]:<11}${m.price(sid):>6.2f}")
        self.total_label.config(text=f"Total: ${m.total():.2f}")

        # per-section table
        for sec, labels in self.section_rows.items():
            out = m.section_sold_out(sec)
            labels[0].config(text=sec, fg="#b00020" if out else "black")
            labels[1].config(text=f"${PRICES[self.pricing][sec]:.2f}")
            labels[2].config(text=str(m.sold_in(sec)))
            labels[3].config(text="SOLD OUT" if out else str(m.remaining(sec)),
                             fg="#b00020" if out else "black")
            self.canvas.itemconfig(self.section_label_items[sec],
                                   text=sec.upper() + ("  -  SOLD OUT" if out
                                                       else ""),
                                   fill="#b00020" if out else "#555")

        # option list holds only sections that can still be sold
        values = [f"{s} - ${PRICES[self.pricing][s]:.2f} ({m.remaining(s)} left)"
                  for s in m.open_sections() if m.remaining(s) > 0]
        self.section_box.config(values=values)
        current = self._selected_section()
        match = [v for v in values if v.startswith(current + " - ")]
        self.section_var.set(match[0] if match else "")
        if not match:
            self.price_label.config(text="")
        else:
            self._section_changed()

        # sold-out theater: banner and disabled interface
        if m.theater_sold_out():
            self.banner.config(text="This showing has been sold out.",
                               bg="#b00020")
            state = "disabled"
        else:
            self.banner.config(text="", bg=self.window.cget("bg"))
            state = "normal"
        self.select_btn.config(state=state)
        self.buy_btn.config(state=state)
        self.clear_btn.config(state=state)
        self.section_box.config(state="disabled" if state == "disabled"
                                else "readonly")
        self.qty_box.config(state="disabled" if state == "disabled"
                            else "readonly")
