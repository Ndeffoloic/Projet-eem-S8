        # Create left frame for parameters
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Create right frame for plots
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create parameter entries
        self.parameters = {
            "type_double_auction": tk.StringVar(),
            "type_price_determined": tk.StringVar(),
            "ZI_C": tk.StringVar(),
            "change_random": tk.StringVar()
        }
        for i, (name, var) in enumerate(self.parameters.items()):
            tk.Label(self.left_frame, text=name).grid(row=i, column=0)
            tk.Entry(self.left_frame, textvariable=var).grid(row=i, column=1)

        # Create run button
        self.run_button = tk.Button(self.left_frame, text="Simuler", command=self.run_simulation)
        self.run_button.grid(row=len(self.parameters)+4, column=0, columnspan=2)

        # Create next button
        self.next_button = tk.Button(self.left_frame, text="Next", command=self.next_plot)
        self.next_button.grid(row=len(self.parameters) + 5, column=0, columnspan=2)

        # Create prev button
        self.prev_button = tk.Button(self.left_frame, text="Prev", command=self.prev_plot)
        self.prev_button.grid(row=len(self.parameters) + 6, column=0, columnspan=2)

        # Create end button
        self.end_button = tk.Button(self.left_frame, text="End", command=self.close_window)
        self.end_button.grid(row=len(self.parameters) + 7, column=0, columnspan=2)
