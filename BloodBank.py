import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------- Blood Bank Data Initialization -------------------
blood_data = {
    'A+': 10, 'A-': 5, 'B+': 8, 'B-': 3,
    'O+': 15, 'O-': 2, 'AB+': 6, 'AB-': 1
}

donors = []  # List to store donor dictionaries

# ------------------- Function to Add Donor -------------------
def add_donor():
    name = name_entry.get()
    blood_group = blood_group_combobox.get()
    age = age_entry.get()
    contact = contact_entry.get()

    if not (name and blood_group and age and contact):
        messagebox.showerror("Input Error", "Please fill all fields!")
        return

    donor = {
        'Name': name,
        'Blood Group': blood_group,
        'Age': age,
        'Contact': contact
    }
    donors.append(donor)

    # Insert into live donor table
    donor_tree.insert('', tk.END, values=(donor['Name'], donor['Age'], donor['Blood Group'], donor['Contact']))

    # Update blood stock
    blood_data[blood_group] += 1
    update_chart()
    messagebox.showinfo("Success", "Donor added successfully!")
    clear_fields()

# ------------------- Function to Clear Input Fields -------------------
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    blood_group_combobox.set('')

# ------------------- Function to View All Donors in New Window -------------------
def view_donors():
    donor_window = tk.Toplevel(root)
    donor_window.title("Donor Details")
    donor_window.geometry("550x400")

    tree = ttk.Treeview(donor_window, columns=("Name", "Age", "Blood Group", "Contact"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Blood Group", text="Blood Group")
    tree.heading("Contact", text="Contact")

    tree.column("Name", width=150)
    tree.column("Age", width=80)
    tree.column("Blood Group", width=100)
    tree.column("Contact", width=150)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for donor in donors:
        tree.insert("", tk.END, values=(donor['Name'], donor['Age'], donor['Blood Group'], donor['Contact']))

# ------------------- Function to Update Blood Stock Chart -------------------
def update_chart():
    blood_groups = list(blood_data.keys())
    quantities = list(blood_data.values())

    ax.clear()
    bars = ax.bar(
        blood_groups, quantities,
        color=['#FF9999', '#FFCC99', '#99CCFF', '#CCFF99', '#FF6666', '#6666FF', '#66FF66', '#FFFF66']
    )

    ax.set_title("Blood Group Availability", fontsize=14, fontweight='bold')
    ax.set_xlabel("Blood Groups", fontsize=12, fontweight='bold')
    ax.set_ylabel("Units Available", fontsize=12, fontweight='bold')
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

    for bar, qty in zip(bars, quantities):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 1, str(qty),
                ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

    canvas.draw()

# ------------------- Main Application Window -------------------
root = tk.Tk()
root.title("🩸 Blood Bank Management System")
root.geometry("1000x750")
root.configure(bg='#F4F6F7')

# Title
tk.Label(root, text="Blood Bank Management System", font=("Arial", 22, "bold"), bg='#F4F6F7', fg="#2C3E50").pack(pady=20)

# ------------------- Donor Input Form -------------------
form_frame = tk.LabelFrame(root, text="Donor Information", font=("Arial", 14, "bold"), padx=20, pady=20, bg='#F4F6F7')
form_frame.pack(pady=10)

# Name
tk.Label(form_frame, text="Name:", font=("Arial", 12, "bold"), bg='#F4F6F7').grid(row=0, column=0, padx=10, pady=10, sticky='e')
name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
name_entry.grid(row=0, column=1, padx=10, pady=10)

# Blood Group
tk.Label(form_frame, text="Blood Group:", font=("Arial", 12, "bold"), bg='#F4F6F7').grid(row=1, column=0, padx=10, pady=10, sticky='e')
blood_group_combobox = ttk.Combobox(form_frame, values=list(blood_data.keys()), font=("Arial", 12), width=28)
blood_group_combobox.grid(row=1, column=1, padx=10, pady=10)

# Age
tk.Label(form_frame, text="Age:", font=("Arial", 12, "bold"), bg='#F4F6F7').grid(row=2, column=0, padx=10, pady=10, sticky='e')
age_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
age_entry.grid(row=2, column=1, padx=10, pady=10)

# Contact
tk.Label(form_frame, text="Contact:", font=("Arial", 12, "bold"), bg='#F4F6F7').grid(row=3, column=0, padx=10, pady=10, sticky='e')
contact_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
contact_entry.grid(row=3, column=1, padx=10, pady=10)

# Buttons
tk.Button(form_frame, text="➕ Add Donor", command=add_donor,
          font=("Arial", 12, "bold"), bg='#27AE60', fg='white', width=15).grid(row=4, column=0, padx=10, pady=20)

tk.Button(form_frame, text="👁 View Donors", command=view_donors,
          font=("Arial", 12, "bold"), bg='#2980B9', fg='white', width=15).grid(row=4, column=1, padx=10, pady=20)

# ------------------- Blood Stock Chart -------------------
chart_frame = tk.LabelFrame(root, text="Blood Stock Status", font=("Arial", 14, "bold"), padx=10, pady=10, bg='#F4F6F7')
chart_frame.pack(pady=20)

fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, chart_frame)
canvas.get_tk_widget().pack()
update_chart()

# ------------------- Live Donor Table -------------------
donor_table_frame = tk.LabelFrame(root, text="All Donor Details", font=("Arial", 14, "bold"), bg="#F4F6F7", padx=10, pady=10)
donor_table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

donor_tree = ttk.Treeview(donor_table_frame, columns=("Name", "Age", "Blood Group", "Contact"), show="headings")
donor_tree.heading("Name", text="Name")
donor_tree.heading("Age", text="Age")
donor_tree.heading("Blood Group", text="Blood Group")
donor_tree.heading("Contact", text="Contact")

donor_tree.column("Name", width=150)
donor_tree.column("Age", width=80)
donor_tree.column("Blood Group", width=100)
donor_tree.column("Contact", width=150)

donor_tree.pack(fill=tk.BOTH, expand=True)

# Add Scrollbar (optional)
scrollbar = ttk.Scrollbar(donor_tree, orient="vertical", command=donor_tree.yview)
donor_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# ------------------- Mainloop -------------------
root.mainloop()
