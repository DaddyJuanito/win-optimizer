import tkinter
import tkinter.messagebox
import customtkinter
from uninstaller import call_uninstall_programs
from code.tweaks import MouseTweaks

# Set appearance mode and color theme
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Windows Optimizer.py")
        self.geometry("1100x580")

        # Configure grid layout (4x4)
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Create topbar frame with widgets
        self.topbar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.topbar_frame.grid(row=0, column=0, columnspan=4, sticky="new")
        self.topbar_frame.grid_columnconfigure(0, weight=0)
        self.logo_label = customtkinter.CTkLabel(
            self.topbar_frame,
            text="Windows Optimizer",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=10, pady=(5, 5))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=0, column=3, padx=10, pady=(5, 0), sticky="e")

        # Create tabview
        self.tabview = customtkinter.CTkTabview(self, width=950, height=550)
        self.tabview.grid(row=1, column=0, columnspan=4, padx=(10, 10), pady=(5, 10))
        self.tabview.add("Basic Tweaks")
        self.tabview.add("Uninstaller")
        self.tabview.add("Hardware")
        self.tabview.add("About")

        # Set tab columns
        self.tabview.tab("Basic Tweaks").grid_columnconfigure(3, weight=1)
        self.tabview.tab("Uninstaller").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Hardware").grid_columnconfigure(0, weight=1)
        self.tabview.tab("About").grid_columnconfigure(0, weight=1)

        # Basic Tweaks Tab
        self.system_tweaks = customtkinter.CTkScrollableFrame(
            self.tabview.tab("Basic Tweaks"),
            label_text="System Tweaks",
            width=300,
            height=400,
        )
        self.system_tweaks.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        self.system_tweaks.grid_columnconfigure(0, weight=1)
        self.system_tweaks.grid_rowconfigure(0, weight=0)

        # Create system_tweaks_switches list
        self.system_tweaks_switches = []
        for i in range(20):
            switch = customtkinter.CTkSwitch(
                master=self.system_tweaks, text=f"Custom Tweak {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.system_tweaks_switches.append(switch)


        # ...
        # Create mouse_tweaks
        self.mouse_tweaks = MouseTweaks(
            self.tabview.tab("Basic Tweaks"),
            label_text="Mouse Tweaks")

        # Basic Tweaks: Create textbox
        self.textbox = customtkinter.CTkTextbox(
            self.tabview.tab("Basic Tweaks"), state="disabled")
        self.textbox.grid(row=0, column=3, padx=(0, 0),
                          pady=(10, 10), sticky="e")
        self.textbox.grid_columnconfigure((0), weight=1)

        def tweak_hover(e, arg):
            self.textbox.configure(state="normal")
            self.textbox.insert(0.0, f"More info about button {str(arg)}")

        def tweak_hover_leave(e, arg):
            self.textbox.delete(0.0, "end")
            self.textbox.configure(state="disabled")

        # Basic Tweaks: Create hover event description for system tweaks
        for i in range(20):
            self.system_tweaks_switches[i].bind(
                '<Enter>', lambda e, arg=i: tweak_hover(e, arg))
            self.system_tweaks_switches[i].bind(
                '<Leave>', lambda e, arg=i: tweak_hover_leave(e, arg))

        # Basic Tweaks: Create hover event description for mouse tweaks
        for i in range(20):
            self.mouse_tweaks_switches[i].bind(
                '<Enter>', lambda e, arg=i: tweak_hover(e, arg))
            self.mouse_tweaks_switches[i].bind(
                '<Leave>', lambda e, arg=i: tweak_hover_leave(e, arg))

        # Basic Tweaks: Apply Button
        self.string_input_button = customtkinter.CTkButton(
            self.tabview.tab("Basic Tweaks"),
            text="Apply",
            command=self.open_input_dialog_event,
        )
        self.string_input_button.grid(row=0, column=2, padx=(10, 10), pady=(0, 0))

        # Uninstaller Tab
        self.refresh_programs_event()

        # Uninstaller: Uninstall Button
        self.uninstall_button = customtkinter.CTkButton(
            self.tabview.tab("Uninstaller"),
            text="Uninstall",
            command=self.open_input_dialog_event,
        )
        self.uninstall_button.grid(row=0, column=1, padx=(10, 10), pady=(0, 0), sticky="e")

        # Uninstaller: Refresh Button
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Uninstaller"), text="Refresh",
                                                        command=self.refresh_programs_event)
        self.string_input_button.grid(row=0, column=2, padx=(10, 10), pady=(0, 0))  

        # Hardware Tab
        # ...

        self.label_hardware = customtkinter.CTkLabel(
            self.tabview.tab("Hardware"), text="GUI COMING SOON")
        self.label_hardware.grid(row=0, column=0, padx=20, pady=20)
            
        # About Tab
        # ...
        self.label_about = customtkinter.CTkLabel(
            self.tabview.tab("About"), text="GUI COMING SOON")
        self.label_about.grid(row=0, column=0, padx=20, pady=20)

        # set default values
        self.system_tweaks_switches[0].select()
        self.system_tweaks_switches[4].select() 
        self.appearance_mode_optionemenu.set("Dark")

    # Event handlers
    #def open_input_dialog_event(self):
        #dialog = customtkinter.CTkInputDialog(
            #text="Type 'YES' if you want to apply the Tweaks", title="apply_tweak")
        #print("User Response:", dialog.get_input())
    def open_input_dialog_event(self):
        selected_items_array = self.get_selected_items()
        results = call_uninstall_programs(selected_items_array)
        #self.refresh_programs_event()
        print (results)

    def get_selected_items(self):
        return [
            switch._text for switch in self.uninstall_list_switches if switch.get()
        ]
    
    def refresh_programs_event(self):
        list_of_programs = get_installed_programs()

        self.uninstall_list = customtkinter.CTkScrollableFrame(self.tabview.tab(
            "Uninstaller"), label_text="Installed Programs", width=400, height=400)
        self.uninstall_list.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        self.uninstall_list.grid_columnconfigure((0), weight=1)
        self.uninstall_list.grid_rowconfigure((0), weight=0)
        self.uninstall_list_switches = []

        for i, item in enumerate(list_of_programs):
            switch = customtkinter.CTkSwitch(
                master=self.uninstall_list, text=f"{item}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="w")
            self.uninstall_list_switches.append(switch)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def topbar_button_event(self):
        print("topbar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
