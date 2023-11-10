import tkinter
import tkinter.messagebox
import customtkinter


def tweak_hover(e, arg):
    self.textbox.configure(state="normal")
    self.textbox.insert(0.0, f"More info about button {str(arg)}")

def tweak_hover_leave(e, arg):
    self.textbox.delete(0.0, "end")
    self.textbox.configure(state="disabled")

class MouseTweaks(customtkinter.CTkScrollableFrame):
    def __init__(self, tabview, label_text="Mouse Tweaks"):
        super().__init__(tabview, label_text=label_text, width=300, height=400)
        self.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        self.grid_columnconfigure(1, weight=1)

        self.mouse_tweaks_switches = []

        self.label_markC = customtkinter.CTkLabel(
            master=self, text="MarkC Fix: ")
        self.label_markC.grid(row=0, column=0, padx=(
            15, 0), pady=(0, 0), sticky="w")
        markC_fix = customtkinter.CTkOptionMenu(master=self, dynamic_resizing=True,
                                                values=["100%", "200%", "300%"])
        markC_fix.grid(row=0, column=1, padx=0, pady=(0, 10))
        self.mouse_tweaks_switches.append(markC_fix)
        for i in range(19):
            switch = customtkinter.CTkSwitch(
                master=self, text=f"Mouse Tweak {i}")
            switch.grid(row=i + 1, column=0, padx=10, pady=(0, 20))
            self.mouse_tweaks_switches.append(switch)

                    # Basic Tweaks: Create hover event description for mouse tweaks
        for i in range(20):
            self.mouse_tweaks_switches[i].bind(
                '<Enter>', lambda e, arg=i: tweak_hover(e, arg))
            self.mouse_tweaks_switches[i].bind(
                '<Leave>', lambda e, arg=i: tweak_hover_leave(e, arg))