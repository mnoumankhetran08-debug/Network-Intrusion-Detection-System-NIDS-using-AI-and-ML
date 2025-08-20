import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import pickle

# Function to load the pre-trained Random Forest Classifier
def load_model():
    with open('random_forest_classifier0032.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Function to handle file upload
def upload_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        df = pd.read_csv(filename)
        return df
    else:
        return None

# Function to detect network intrusions
def detect_intrusions():
    global df
    if df is None:
        messagebox.showerror("Error", "Please upload a CSV file first!")
        return
    
    model = load_model()
    X = df.drop(columns=['Label', 'Attack'])
    y_pred = model.predict(X)
    
    # Get the indices of rows where attacks are detected
    attack_indices = df.index[y_pred == 1].tolist()
    
    # Get the attack names
    attack_names = df.loc[attack_indices, 'Attack'].tolist()
    
    # Display detection results
    if len(attack_indices) > 0:
        detection_results = f"Detected attacks: {len(attack_indices)}\nRow numbers: {attack_indices}\nAttack names: {attack_names}"
    else:
        detection_results = "No attacks detected!"
    
    # Display detection results with scrolling
    root = tk.Tk()
    root.title("Detection Results")
    root.configure(bg="sky blue")  # Change background color
    root.geometry("800x400")  # Set window size
    
    text = scrolledtext.ScrolledText(root, wrap="word", height=20, width=80, bg="White")  # Change text background color
    text.insert("1.0", detection_results)
    text.pack(expand=True, fill="both")
    
    root.mainloop()

# Main GUI function
def main():
    global df
    
    # Create the main window
    root = tk.Tk()
    root.title("Network Intrusion Detection System")
    root.configure(bg="sky blue")  # Change background color
    root.geometry("800x400")  # Set window size
    
    # Function to handle file upload
    def upload():
        global df
        df = upload_file()
        if df is not None:
            upload_label.config(text="File Uploaded Successfully!")
        else:
            upload_label.config(text="Upload Failed!")
    
    # Function to detect intrusions
    def detect():
        detect_intrusions()
    
    # Create widgets
    upload_button = tk.Button(root, text="Upload CSV File", command=upload, bg="Yellow")  # Change button background color
    detect_button = tk.Button(root, text="Detect", command=detect, bg="Salmon")  # Change button background color
    upload_label = tk.Label(root, text="", bg="lightblue", fg="Red")  # Change label background and text color
    
    # Pack the widgets
    upload_button.pack(expand=True)
    detect_button.pack(expand=True)
    upload_label.pack(expand=True)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    df = None
    main()
