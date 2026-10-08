import random
import sys
import tkinter as tk
from tkinter import ttk, messagebox


class HandCricketGUI:

    def __init__(self, root):
        self.root = root
        self.root.title(" Hand Cricket - Odd or Even")

        # Set default window size
        self.root.geometry("700x800")
        self.root.minsize(550, 650)
        self.root.resizable(True, True)

        # Full-Screen & Fit Screen State
        self.is_fullscreen = False

        # Fit to Screen (Maximize window on startup)
        try:
            if sys.platform.startswith("win"):
                self.root.state("zoomed")
            else:
                self.root.attributes("-zoomed", True)
        except Exception:
            pass

        # Keyboard Bindings for Full Screen & Fit Screen
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # ==================================================
        # COLOR PALETTE & STYLES
        # ==================================================
        self.BG_DARK = "#0f172a"  # Slate 900
        self.BG_CARD = "#1e293b"  # Slate 800
        self.BG_ACCENT = "#334155"  # Slate 700
        self.COLOR_PRIMARY = "#6366f1"  # Indigo
        self.COLOR_SUCCESS = "#10b981"  # Emerald
        self.COLOR_DANGER = "#ef4444"  # Red
        self.COLOR_GOLD = "#f59e0b"  # Amber / Gold
        self.COLOR_TEXT = "#f8fafc"  # Slate 50
        self.COLOR_MUTED = "#94a3b8"  # Slate 400

        self.root.configure(bg=self.BG_DARK)

        # Game State Data
        self.reset_game_data()

        # Build UI Structure Header
        self.create_header()

        # Build Scrollable Container for Fit-Screen Responsiveness
        self.setup_scrollable_container()

        # Start at Toss Screen
        self.show_toss_screen()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)

    def setup_scrollable_container(self):
        # Outer main container canvas for smooth responsiveness
        self.canvas = tk.Canvas(
            self.root, bg=self.BG_DARK, highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.root, orient="vertical", command=self.canvas.yview
        )
        self.container = tk.Frame(self.canvas, bg=self.BG_DARK)

        self.container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.container, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.canvas_window, width=e.width
            ),
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def reset_game_data(self):
        self.player_score = 0
        self.npc_score = 0
        self.current_innings = 1
        self.player_bats_first = True
        self.is_player_batting = True
        self.target = None
        self.toss_choice = "even"
        self.toss_player_num = 1
        self.ball_count = 0

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ==================================================
    # UI HEADER & CONTROLS
    # ==================================================
    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.BG_CARD, pady=12, padx=15)
        header_frame.pack(fill="x", side="top")

        title = tk.Label(
            header_frame,
            text=" ODD OR EVEN - HAND CRICKET",
            font=("Segoe UI", 16, "bold"),
            fg=self.COLOR_GOLD,
            bg=self.BG_CARD,
        )
        title.pack(side="left")

        # Controls Hint / Fullscreen Button
        controls_btn = tk.Button(
            header_frame,
            text=" ⛶ Fullscreen (F11)",
            font=("Segoe UI", 9, "bold"),
            bg=self.BG_ACCENT,
            fg=self.COLOR_TEXT,
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.toggle_fullscreen,
        )
        controls_btn.pack(side="right")

    # ==================================================
    # SCREEN 1: TOSS SELECTION
    # ==================================================
    def show_toss_screen(self):
        self.clear_container()

        title_lbl = tk.Label(
            self.container,
            text=" THE TOSS",
            font=("Segoe UI", 16, "bold"),
            fg=self.COLOR_TEXT,
            bg=self.BG_DARK,
        )
        title_lbl.pack(pady=(15, 15))

        # Card Box
        card = tk.Frame(self.container, bg=self.BG_CARD, padx=20, pady=20)
        card.pack(fill="x", padx=20)

        # Odd or Even Choice
        tk.Label(
            card,
            text="Step 1: Choose Odd or Even",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_MUTED,
            bg=self.BG_CARD,
        ).pack(anchor="w", pady=(0, 8))

        toss_opt_frame = tk.Frame(card, bg=self.BG_CARD)
        toss_opt_frame.pack(pady=(0, 20))

        self.toss_var = tk.StringVar(value="even")

        def select_toss_call(val):
            self.toss_var.set(val)
            btn_even.config(
                bg=self.COLOR_PRIMARY if val == "even" else self.BG_ACCENT
            )
            btn_odd.config(
                bg=self.COLOR_PRIMARY if val == "odd" else self.BG_ACCENT
            )

        btn_even = tk.Button(
            toss_opt_frame,
            text="EVEN",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_PRIMARY,
            fg=self.COLOR_TEXT,
            width=12,
            height=2,
            relief="flat",
            cursor="hand2",
            command=lambda: select_toss_call("even"),
        )
        btn_even.pack(side="left", padx=10)

        btn_odd = tk.Button(
            toss_opt_frame,
            text="ODD",
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_ACCENT,
            fg=self.COLOR_TEXT,
            width=12,
            height=2,
            relief="flat",
            cursor="hand2",
            command=lambda: select_toss_call("odd"),
        )
        btn_odd.pack(side="left", padx=10)

        # Toss Number Choice (1-10)
        tk.Label(
            card,
            text="Step 2: Choose your Toss Number (1 - 10)",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_MUTED,
            bg=self.BG_CARD,
        ).pack(anchor="w", pady=(0, 10))

        num_frame = tk.Frame(card, bg=self.BG_CARD)
        num_frame.pack(pady=(0, 20))

        self.selected_toss_btn = None
        self.toss_num_var = tk.IntVar(value=1)

        for i in range(1, 11):
            btn = tk.Button(
                num_frame,
                text=str(i),
                font=("Segoe UI", 11, "bold"),
                width=4,
                height=1,
                bg=self.BG_ACCENT,
                fg=self.COLOR_TEXT,
                relief="flat",
                cursor="hand2",
            )
            btn.config(
                command=lambda n=i, b=btn: self.set_toss_num(n, b, num_frame)
            )
            row = 0 if i <= 5 else 1
            col = (i - 1) % 5
            btn.grid(row=row, column=col, padx=5, pady=5)
            if i == 1:
                self.set_toss_num(1, btn, num_frame)

        # Toss Action Button
        toss_btn = tk.Button(
            self.container,
            text=" FLIP COIN & TOSS",
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_GOLD,
            fg="#000000",
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.process_toss,
        )
        toss_btn.pack(fill="x", padx=20, pady=20)

    def set_toss_num(self, num, btn, parent):
        self.toss_num_var.set(num)
        for child in parent.winfo_children():
            child.config(bg=self.BG_ACCENT)
        btn.config(bg=self.COLOR_SUCCESS)

    # ==================================================
    # SCREEN 2: TOSS RESULT & DECISION
    # ==================================================
    def process_toss(self):
        player_num = self.toss_num_var.get()
        npc_num = random.randint(1, 10)
        toss_sum = player_num + npc_num
        is_even = toss_sum % 2 == 0
        actual_result = "even" if is_even else "odd"
        player_call = self.toss_var.get()

        player_won_toss = player_call == actual_result

        self.clear_container()

        title_lbl = tk.Label(
            self.container,
            text=" TOSS RESULT",
            font=("Segoe UI", 16, "bold"),
            fg=self.COLOR_TEXT,
            bg=self.BG_DARK,
        )
        title_lbl.pack(pady=(15, 15))

        card = tk.Frame(self.container, bg=self.BG_CARD, padx=20, pady=20)
        card.pack(fill="x", padx=20)

        res_info = (
            f"You chose: {player_num}  |  NPC chose: {npc_num}\n"
            f"Total = {toss_sum} ({actual_result.upper()})\n\n"
            f"You called {player_call.upper()}!"
        )
        tk.Label(
            card,
            text=res_info,
            font=("Segoe UI", 12),
            fg=self.COLOR_TEXT,
            bg=self.BG_CARD,
            justify="center",
        ).pack(pady=10)

        if player_won_toss:
            win_lbl = tk.Label(
                card,
                text=" YOU WON THE TOSS!",
                font=("Segoe UI", 14, "bold"),
                fg=self.COLOR_SUCCESS,
                bg=self.BG_CARD,
            )
            win_lbl.pack(pady=10)

            tk.Label(
                card,
                text="Choose your role:",
                font=("Segoe UI", 11),
                fg=self.COLOR_MUTED,
                bg=self.BG_CARD,
            ).pack(pady=(10, 5))

            dec_frame = tk.Frame(card, bg=self.BG_CARD)
            dec_frame.pack(pady=10)

            btn_bat = tk.Button(
                dec_frame,
                text=" BAT FIRST",
                font=("Segoe UI", 12, "bold"),
                bg=self.COLOR_PRIMARY,
                fg=self.COLOR_TEXT,
                width=12,
                height=2,
                relief="flat",
                cursor="hand2",
                command=lambda: self.start_match(player_bats_first=True),
            )
            btn_bat.pack(side="left", padx=10)

            btn_bowl = tk.Button(
                dec_frame,
                text=" BOWL FIRST",
                font=("Segoe UI", 12, "bold"),
                bg=self.COLOR_PRIMARY,
                fg=self.COLOR_TEXT,
                width=12,
                height=2,
                relief="flat",
                cursor="hand2",
                command=lambda: self.start_match(player_bats_first=False),
            )
            btn_bowl.pack(side="left", padx=10)

        else:
            win_lbl = tk.Label(
                card,
                text=" NPC WON THE TOSS!",
                font=("Segoe UI", 14, "bold"),
                fg=self.COLOR_DANGER,
                bg=self.BG_CARD,
            )
            win_lbl.pack(pady=10)

            npc_dec = random.choice(["bat", "bowl"])
            player_bats = npc_dec == "bowl"

            dec_text = f"NPC elected to {npc_dec.upper()} first!"
            tk.Label(
                card,
                text=dec_text,
                font=("Segoe UI", 12, "bold"),
                fg=self.COLOR_GOLD,
                bg=self.BG_CARD,
            ).pack(pady=10)

            start_btn = tk.Button(
                self.container,
                text="START MATCH ",
                font=("Segoe UI", 13, "bold"),
                bg=self.COLOR_SUCCESS,
                fg=self.COLOR_TEXT,
                height=2,
                relief="flat",
                cursor="hand2",
                command=lambda: self.start_match(
                    player_bats_first=player_bats
                ),
            )
            start_btn.pack(fill="x", padx=20, pady=20)

    # ==================================================
    # SCREEN 3: MATCH ENGINE & PLAYING FIELD
    # ==================================================
    def start_match(self, player_bats_first):
        self.player_bats_first = player_bats_first
        self.is_player_batting = player_bats_first
        self.current_innings = 1
        self.player_score = 0
        self.npc_score = 0
        self.target = None
        self.ball_count = 0

        self.setup_match_screen()

    def setup_match_screen(self):
        self.clear_container()

        # Banner Header
        self.banner_lbl = tk.Label(
            self.container,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg=self.COLOR_GOLD,
            bg=self.BG_DARK,
        )
        self.banner_lbl.pack(pady=(10, 10))

        # Scorecard Panel
        score_frame = tk.Frame(self.container, bg=self.BG_DARK)
        score_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Player Score Card
        self.p_card = tk.Frame(
            score_frame,
            bg=self.BG_CARD,
            padx=15,
            pady=10,
            bd=1,
            relief="solid",
        )
        self.p_card.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(
            self.p_card,
            text="YOU",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLOR_MUTED,
            bg=self.BG_CARD,
        ).pack()
        self.p_role_lbl = tk.Label(
            self.p_card,
            text="",
            font=("Segoe UI", 10),
            fg=self.COLOR_SUCCESS,
            bg=self.BG_CARD,
        )
        self.p_role_lbl.pack()
        self.p_score_lbl = tk.Label(
            self.p_card,
            text="0",
            font=("Segoe UI", 24, "bold"),
            fg=self.COLOR_TEXT,
            bg=self.BG_CARD,
        )
        self.p_score_lbl.pack()

        # NPC Score Card
        self.npc_card = tk.Frame(
            score_frame,
            bg=self.BG_CARD,
            padx=15,
            pady=10,
            bd=1,
            relief="solid",
        )
        self.npc_card.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tk.Label(
            self.npc_card,
            text="NPC",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLOR_MUTED,
            bg=self.BG_CARD,
        ).pack()
        self.npc_role_lbl = tk.Label(
            self.npc_card,
            text="",
            font=("Segoe UI", 10),
            fg=self.COLOR_DANGER,
            bg=self.BG_CARD,
        )
        self.npc_role_lbl.pack()
        self.npc_score_lbl = tk.Label(
            self.npc_card,
            text="0",
            font=("Segoe UI", 24, "bold"),
            fg=self.COLOR_TEXT,
            bg=self.BG_CARD,
        )
        self.npc_score_lbl.pack()

        # Event Commentary Log
        tk.Label(
            self.container,
            text="MATCH COMMENTARY",
            font=("Segoe UI", 9, "bold"),
            fg=self.COLOR_MUTED,
            bg=self.BG_DARK,
        ).pack(anchor="w", padx=20, pady=(5, 2))

        log_frame = tk.Frame(self.container, bg=self.BG_CARD)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.log_text = tk.Text(
            log_frame,
            height=8,
            bg=self.BG_CARD,
            fg=self.COLOR_TEXT,
            font=("Consolas", 10),
            wrap="word",
            relief="flat",
            state="disabled",
        )
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(
            side="left", fill="both", expand=True, padx=5, pady=5
        )

        # Action Keypad
        self.action_lbl = tk.Label(
            self.container,
            text="Select your number (1 - 10):",
            font=("Segoe UI", 11, "bold"),
            fg=self.COLOR_TEXT,
            bg=self.BG_DARK,
        )
        self.action_lbl.pack(pady=(0, 5))

        keypad_frame = tk.Frame(self.container, bg=self.BG_DARK)
        keypad_frame.pack(pady=(0, 15))

        for i in range(1, 11):
            btn = tk.Button(
                keypad_frame,
                text=str(i),
                font=("Segoe UI", 12, "bold"),
                width=5,
                height=2,
                bg=self.COLOR_PRIMARY,
                fg=self.COLOR_TEXT,
                relief="flat",
                cursor="hand2",
                command=lambda n=i: self.play_turn(n),
            )
            row = 0 if i <= 5 else 1
            col = (i - 1) % 5
            btn.grid(row=row, column=col, padx=4, pady=4)

        self.update_scorecard_ui()

    def add_commentary(self, text, tag_color=None):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_scorecard_ui(self):
        # Header banner
        if self.current_innings == 1:
            batting_team = (
                "YOU ARE BATTING "
                if self.is_player_batting
                else "NPC IS BATTING "
            )
            self.banner_lbl.config(text=f"1st INNINGS: {batting_team}")
        else:
            req_runs = (self.target + 1) - (
                self.player_score if self.is_player_batting else self.npc_score
            )
            req_runs = max(req_runs, 0)
            self.banner_lbl.config(
                text=f"2nd INNINGS: Target = {self.target + 1} | Need {req_runs} runs"
            )

        # Roles & Scores
        self.p_role_lbl.config(
            text="BATTING " if self.is_player_batting else "BOWLING "
        )
        self.npc_role_lbl.config(
            text="BOWLING " if self.is_player_batting else "BATTING "
        )

        self.p_score_lbl.config(text=str(self.player_score))
        self.npc_score_lbl.config(text=str(self.npc_score))

        if self.is_player_batting:
            self.action_lbl.config(text="Choose runs to hit (1 - 10):")
        else:
            self.action_lbl.config(text="Choose a number to bowl (1 - 10):")

    def play_turn(self, player_val):
        self.ball_count += 1
        npc_val = random.randint(1, 10)

        if self.is_player_batting:
            if player_val == npc_val:
                self.add_commentary(
                    f" [Ball {self.ball_count}] You played {player_val} | NPC bowled {npc_val} ➔ OUT!"
                )
                self.handle_wicket()
            else:
                self.player_score += player_val
                self.add_commentary(
                    f" [Ball {self.ball_count}] You: {player_val} | NPC: {npc_val} ➔ +{player_val} Runs (Score: {self.player_score})"
                )
                if (
                    self.current_innings == 2
                    and self.player_score > self.target
                ):
                    self.add_commentary(" TARGET PASSED!")
                    self.show_game_over_screen()
        else:
            if player_val == npc_val:
                self.add_commentary(
                    f" [Ball {self.ball_count}] You bowled {player_val} | NPC played {npc_val} ➔ OUT!"
                )
                self.handle_wicket()
            else:
                self.npc_score += npc_val
                self.add_commentary(
                    f" [Ball {self.ball_count}] You: {player_val} | NPC: {npc_val} ➔ NPC +{npc_val} Runs (Score: {self.npc_score})"
                )
                if self.current_innings == 2 and self.npc_score > self.target:
                    self.add_commentary(" NPC PASSED TARGET!")
                    self.show_game_over_screen()

        self.update_scorecard_ui()

    def handle_wicket(self):
        if self.current_innings == 1:
            self.target = (
                self.player_score if self.player_bats_first else self.npc_score
            )
            self.current_innings = 2
            self.is_player_batting = not self.player_bats_first
            self.ball_count = 0
            self.add_commentary(
                f"\n 1st Innings Ended! Target set to {self.target + 1} runs.\n--- 2nd INNINGS BEGINS ---\n"
            )
        else:
            self.show_game_over_screen()

    # ==================================================
    # SCREEN 4: FINAL RESULTS
    # ==================================================
    def show_game_over_screen(self):
        self.clear_container()

        title_lbl = tk.Label(
            self.container,
            text=" MATCH FINISHED ",
            font=("Segoe UI", 16, "bold"),
            fg=self.COLOR_GOLD,
            bg=self.BG_DARK,
        )
        title_lbl.pack(pady=(15, 15))

        card = tk.Frame(self.container, bg=self.BG_CARD, padx=20, pady=25)
        card.pack(fill="x", padx=20)

        # Winner Logic
        if self.player_score > self.npc_score:
            res_title = " CONGRATULATIONS! YOU WON!"
            res_color = self.COLOR_SUCCESS
            diff = self.player_score - self.npc_score
            sub_text = f"You defeated the NPC by {diff} runs!"
        elif self.npc_score > self.player_score:
            res_title = " GAME OVER! NPC WON!"
            res_color = self.COLOR_DANGER
            diff = self.npc_score - self.player_score
            sub_text = f"NPC defeated you by {diff} runs!"
        else:
            res_title = " IT'S A TIE!"
            res_color = self.COLOR_GOLD
            sub_text = "Both teams scored the exact same runs!"

        tk.Label(
            card,
            text=res_title,
            font=("Segoe UI", 14, "bold"),
            fg=res_color,
            bg=self.BG_CARD,
        ).pack(pady=(0, 5))
        tk.Label(
            card,
            text=sub_text,
            font=("Segoe UI", 11),
            fg=self.COLOR_TEXT,
            bg=self.BG_CARD,
        ).pack(pady=(0, 15))

        # Final Score Summary Box
        score_box = tk.Frame(card, bg=self.BG_ACCENT, padx=15, pady=15)
        score_box.pack(fill="x", pady=10)

        tk.Label(
            score_box,
            text=f"Your Final Score: {self.player_score}",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_TEXT,
            bg=self.BG_ACCENT,
        ).pack(anchor="w", pady=2)
        tk.Label(
            score_box,
            text=f"NPC Final Score:  {self.npc_score}",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLOR_TEXT,
            bg=self.BG_ACCENT,
        ).pack(anchor="w", pady=2)

        # Play Again Button
        restart_btn = tk.Button(
            self.container,
            text=" PLAY AGAIN",
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_PRIMARY,
            fg=self.COLOR_TEXT,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.restart_game,
        )
        restart_btn.pack(fill="x", padx=20, pady=20)

    def restart_game(self):
        self.reset_game_data()
        self.show_toss_screen()


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = HandCricketGUI(root)
    root.mainloop()