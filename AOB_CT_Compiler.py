import tkinter as tk
from tkinter import scrolledtext, messagebox

cheat_table_texts = []

def compile_cheat_tables():
    enable_code = ""
    disable_code = ""
    compiled_script = ""

    # Retrieve the cheat table inputs
    cheat_tables = []
    for text_widget in cheat_table_texts:
        cheat_table = text_widget.get("1.0", "end-1c")
        cheat_tables.append(cheat_table)

    for i, cheat_table in enumerate(cheat_tables):
        # Remove code above [ENABLE] section
        enable_start_index = cheat_table.find("[ENABLE]")
        enable_section = cheat_table[enable_start_index:].strip()

        # Find the enable section of the cheat table
        enable_start_index = enable_section.find("aobscanmodule")
        enable_end_index = enable_section.find("[DISABLE]")
        enable_section = enable_section[enable_start_index:enable_end_index].strip()

        # Modify the identifiers in the enable section
        modified_enable_section = enable_section.replace("INJECT", f"INJECT{i+1}")
        modified_enable_section = modified_enable_section.replace("return", f"return{i+1}")
        modified_enable_section = modified_enable_section.replace("newmem", f"newmem{i+1}")
        modified_enable_section = modified_enable_section.replace("code", f"code{i+1}")

        # Append the compiled code for this cheat table
        compiled_script += f"\n//ASSEMBLY SCRIPT #{i + 1} ENABLED:\n"
        compiled_script += modified_enable_section
        compiled_script += "\n\n"

        # Append the enable code for this cheat table to the enable section
        enable_code += f"\n//ASSEMBLY SCRIPT #{i + 1} ENABLED:\n"
        enable_code += modified_enable_section
        enable_code += "\n"

        # Find the disable section of the cheat table
        disable_start_index = cheat_table.find("db")
        disable_end_index = cheat_table.find("\n", disable_start_index)
        disable_section = cheat_table[disable_start_index:disable_end_index].strip()

        # Insert the INJECT number above the first db line in the disable section
        modified_disable_section = f"INJECT{i+1}:\n" + disable_section + "\n"

        # Append the disable code for this cheat table to the disable section
        disable_code += f"\n//ASSEMBLY SCRIPT #{i + 1} DISABLED:\n"
        disable_code += modified_disable_section

        # Retrieve and modify the injection point section
        address_injection_point_start_index = cheat_table.find("// ORIGINAL CODE - INJECTION POINT:")
        address_injection_point_section = cheat_table[address_injection_point_start_index:].strip()

        address_injection_point_start_index = address_injection_point_section.find("// ORIGINAL CODE - INJECTION POINT:")
        address_injection_point_end_index =  address_injection_point_section.find("\n")
        address_injection_point_section = address_injection_point_section[address_injection_point_start_index:address_injection_point_end_index].strip()

        modified_address_injection_point = address_injection_point_section.replace("ORIGINAL CODE - INJECTION POINT:", f"INJECTION POINT ASSEMBLY SCRIPT #{i+1}:")
        
        # Append the modified injection point to the compiled script
        compiled_script += modified_address_injection_point

        # Retrieve and modify the Author section
        author_start_index = cheat_table.find("{ Game")
        author_section = cheat_table[author_start_index:].strip()

        author_start_index = author_section.find("{ Game")
        author_end_index =  author_section.find("[ENABLE]")
        author_section = author_section[author_start_index:author_end_index].strip()
        
        modified_author_section = author_section.replace("{ Game", "{\nGame")

        # Append the modified injection point to the compiled script
        compiled_script += modified_author_section
    
    # Construct the final compiled script
    compiled_script = f"{modified_author_section}\n\n[ENABLE]{enable_code}\n[DISABLE]{disable_code}\nunregistersymbol(*)\ndealloc(*)\n{modified_address_injection_point}"


    # Display the compiled script in the GUI
    compiled_text.config(state=tk.NORMAL)
    compiled_text.delete("1.0", "end")
    compiled_text.insert("1.0", compiled_script)
    compiled_text.config(state=tk.DISABLED)


def add_cheat_table():
    # Create a new text widget for the cheat table
    cheat_table_text = scrolledtext.ScrolledText(cheat_tables_inner_frame, width=60, height=8)
    cheat_table_text.pack(side=tk.TOP, padx=10, pady=5)
    cheat_table_texts.append(cheat_table_text)
    delete_button.config(state=tk.NORMAL)


def delete_cheat_table():
    if cheat_table_texts:
        cheat_table_text = cheat_table_texts.pop()
        cheat_table_text.pack_forget()
        cheat_table_text.destroy()
    if not cheat_table_texts:
        delete_button.config(state=tk.DISABLED)


def copy_compiled_cheat_tables():
    compiled_script = compiled_text.get("1.0", "end-1c")
    window.clipboard_clear()
    window.clipboard_append(compiled_script)
    messagebox.showinfo("Copy Success", "Compiled Cheat Table has been copied to clipboard!")


# Create the main window
window = tk.Tk()
window.title("Cheat Table Script Compiler - Solocase#9274")

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate window size based on screen width and height
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
window.geometry(f"{window_width}x{window_height}")

# Create a frame for the cheat tables
cheat_tables_frame = tk.Frame(window)
cheat_tables_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a frame to hold the cheat tables and the add/delete buttons
cheat_tables_inner_frame = tk.Frame(cheat_tables_frame)
cheat_tables_inner_frame.pack(side=tk.TOP)

# Create a button to add cheat tables
add_button = tk.Button(cheat_tables_inner_frame, text="Add Assembly Script", command=add_cheat_table)
add_button.pack(side=tk.LEFT, padx=10, pady=5, anchor="nw")

# Create a button to delete cheat tables
delete_button = tk.Button(cheat_tables_inner_frame, text="Delete Assembly Script", command=delete_cheat_table, state=tk.DISABLED)
delete_button.pack(side=tk.LEFT, padx=10, pady=5, anchor="nw")

# Create a frame for the compiled script
compiled_frame = tk.Frame(window)
compiled_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a text widget to display the compiled script
compiled_text = scrolledtext.ScrolledText(compiled_frame, width=80, height=20)
compiled_text.pack(fill=tk.BOTH, expand=True)
compiled_text.config(state=tk.DISABLED)

# Create a frame for the buttons
button_frame = tk.Frame(compiled_frame)
button_frame.pack(side=tk.TOP, pady=5)

# Create a button to compile the cheat tables
compile_button = tk.Button(button_frame, text="Compile Scripts", command=compile_cheat_tables)
compile_button.pack(side=tk.LEFT, padx=5)

# Create a button to copy the compiled cheat tables
copy_button = tk.Button(button_frame, text="Copy Compiled Scripts", command=copy_compiled_cheat_tables)
copy_button.pack(side=tk.LEFT, padx=5)

# Start the GUI event loop
window.mainloop()