"""
FIGYELEM! A program futtatásához szükséges külső modulok telepítése:
---------------------------------------------------------------
A következő csomagokat telepítsed a parancssorból a következő paranccsal:
pip install pillow==10.1.0 qrcode==7.4.2 reportlab==4.0.4 pandas==2.1.1
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os
import subprocess
import sys
import webbrowser
import pandas as pd
import csv
from datetime import datetime
import qrcode
from PIL import Image, ImageTk, ImageDraw
import base64
from io import BytesIO
import uuid

# Színek és konstansok
LIGHT_BG_COLOR = '#f0f8ff'
LIGHT_TEXT_COLOR = '#333333'
LIGHT_BUTTON_COLOR = '#d3d3d3'
LIGHT_ENTRY_COLOR = '#ffffff'
DARK_BG_COLOR = '#2d2d2d'
DARK_TEXT_COLOR = '#ffffff'
DARK_BUTTON_COLOR = '#555555'
DARK_ENTRY_COLOR = '#444444'
DARK_SCROLLBAR_COLOR = '#666666'
PDF_BG_COLOR = HexColor(LIGHT_BG_COLOR)
PDF_TEXT_COLOR = HexColor(LIGHT_TEXT_COLOR)
ENTRY_WIDTH = 30
MENU_BG_COLOR = '#e0e0e0'
MENU_TEXT_COLOR = '#333333'
DARK_MENU_BG_COLOR = '#444444'
DARK_MENU_TEXT_COLOR = '#ffffff'
PAPER_SAVING_FACTOR = 0.95
PHOTO_SIZE = (150, 150)
DEFAULT_PHOTO_FORMAT = "PNG"
VERSION = "5.2"

def load_language(lang):
    default_texts = {
        "app_title": "Címnyilvántartó Program",
        "label_id": "ID:",
        "label_name": "Név:",
        "label_nickname": "Becenév:",
        "label_phone": "Telefonszám:",
        "label_email": "E-mail:",
        "label_address": "Cím:",
        "label_workplace": "Munkahely:",
        "label_work_email": "Munkahelyi E-mail:",
        "label_work_phone": "Munkahelyi Telefon:",
        "label_note": "Megjegyzés:",
        "button_new_contact": "Új felvétel",
        "button_search": "Keresés",
        "button_modify": "Módosítás",
        "button_abc_sort": "ABC Listázás",
        "button_delete": "Kontakt törlése",
        "button_save": "Mentés",
        "button_load": "Betöltés",
        "button_clear": "Üres rekord",
        "menu_file": "Fájl",
        "menu_new_contact": "Új felvétel",
        "menu_search": "Keresés",
        "menu_modify": "Módosítás",
        "menu_delete": "Kontakt törlése",
        "menu_save": "Mentés",
        "menu_load": "Betöltés",
        "menu_clear": "Üres rekord",
        "menu_switch_database": "Adatbázis váltás",
        "menu_new_database": "Új adatbázis",
        "menu_exit": "Kilépés",
        "toggle_language": "Nyelv váltás",
        "menu_check_duplicates": "Duplikált ID-k keresése",
        "menu_rebuild_ids": "Újra indexelés",
        "menu_print": "Nyomtatás",
        "menu_print_selected": "Kiválasztott kontakt PDF-be",
        "menu_print_all": "Teljes lista PDF-be",
        "menu_export_csv": "Teljes lista CSV-be",
        "menu_help": "Súgó",
        "menu_user_guide": "Felhasználói dokumentáció",
        "menu_description": "Program leírása",
        "menu_dark_mode": "Sötét mód váltása",
        "menu_print_user_guide": "Felhasználói kézikönyv nyomtatása PDF-be",
        "menu_print_description": "Program leírás nyomtatása PDF-be",
        "confirm_title": "Megerősítés",
        "confirm_delete": "Valóban törölni akarod?",
        "confirm_switch_database": "Vannak nem mentett változtatások. Biztosan váltani akar adatbázist?",
        "confirm_new_database": "Vannak nem mentett változtatások. Biztosan új adatbázist akar létrehozni?",
        "confirm_unsaved": "Vannak nem mentett változtatások. Szeretnéd menteni?",
        "error_title": "Hiba",
        "error_duplicate_ids": "Duplikált ID-k találhatók: {duplicate_ids}",
        "error_csv_open_failed": "Hiba történt a CSV fájl létrehozása során",
        "info_title": "Info",
        "info_csv_created": "A CSV fájl elkészült: {filename}",
        "program_title": "Címnyilvántartó Program",
        "footer_version": "Verzió: {version} | Nyomtatás dátuma: {current_time}",
        "eco_message": "Ön eddig {saved_pages} oldal papírt takarított meg!",
        "csv_headers": ["ID", "Név", "Becenév", "Telefonszám", "E-mail", "Cím", "Munkahely", "Munkahelyi E-mail", "Munkahelyi Telefon", "Megjegyzés", "Fénykép"],
        "current_database": "Aktuális adatbázis: {0}",
        "loaded_data": "Feltöltött adatok: {0} | Keresés eredménye: {1}",
        "user_guide": {
            "title": "Felhasználói kézikönyv",
            "sections": {
                "intro": {
                    "title": "Bevezetés",
                    "content": "Ez a program egy címnyilvántartó alkalmazás, amellyel könnyedén kezelheted kapcsolataidat."
                },
                "basic_operations": {
                    "title": "Alapvető műveletek",
                    "items": [
                        "Új kapcsolat hozzáadása: Ctrl+N vagy 'Új felvétel' gomb",
                        "Kapcsolat módosítása: Ctrl+M vagy 'Módosítás' gomb",
                        "Kapcsolat törlése: Ctrl+T vagy 'Törlés' gomb",
                        "Keresés: Ctrl+K vagy 'Keresés' gomb",
                        "ABC sorrend: Ctrl+A vagy 'ABC Listázás' gomb"
                    ]
                },
                "data_management": {
                    "title": "Adatkezelés",
                    "items": [
                        "Adatok mentése: Ctrl+S vagy 'Mentés' gomb",
                        "Adatok betöltése: Ctrl+L vagy 'Betöltés' gomb",
                        "Adatbázis váltás: Ctrl+D vagy 'Fájl' > 'Adatbázis váltás'",
                        "Új adatbázis: Ctrl+Shift+N vagy 'Fájl' > 'Új adatbázis'"
                    ]
                },
                "export_features": {
                    "title": "Exportálási lehetőségek",
                    "items": [
                        "Egyedi kapcsolat PDF-be: Ctrl+P",
                        "Teljes lista PDF-be: Ctrl+Shift+P",
                        "Teljes lista CSV-be: Ctrl+E",
                        "QR kód generálás: Automatikus a kiválasztott kapcsolathoz"
                    ]
                },
                "special_features": {
                    "title": "Speciális funkciók",
                    "items": [
                        "Fénykép kezelés: Kattintson a fénykép mezőre",
                        "Téma váltás: F3 billentyű",
                        "Nyelv váltás: Ctrl+Shift+L",
                        "Duplikált ID-k keresése: Ctrl+Shift+D",
                        "Újraindexelés: Ctrl+Shift+R"
                    ]
                },
                "troubleshooting": {
                    "title": "Hibaelhárítás",
                    "items": [
                        "Fájl nem található: Ellenőrizze az elérési utat és jogosultságokat",
                        "PDF generálási hiba: Ellenőrizze a ReportLab telepítését",
                        "Lassú működés: Csökkentse az adatbázis méretét",
                        "QR kód nem olvasható: Ellenőrizze a kötelező mezőket"
                    ]
                }
            }
        },
        "description": {
            "title": "Program leírás",
            "sections": {
                "about": {
                    "title": "A programról",
                    "content": "Ez a program egy teljes értékű címnyilvántartó alkalmazás, amelyet Pythonban fejlesztettek. Fő célja a kapcsolatok hatékony kezelése és szervezése."
                },
                "features": {
                    "title": "Főbb jellemzők",
                    "items": [
                        "Intuitív felhasználói felület Tkinter alapokon",
                        "Többnyelvű támogatás (magyar/angol)",
                        "Adatok tárolása JSON formátumban",
                        "PDF és CSV exportálási lehetőség",
                        "QR kód generálás vCard formátumban",
                        "Fényképkezelés integrálva",
                        "Sötét/világos téma választása"
                    ]
                },
                "technical": {
                    "title": "Technikai részletek",
                    "items": [
                        "Python 3.x alapú megoldás",
                        "Tkinter GUI keretrendszer",
                        "ReportLab PDF generáláshoz",
                        "Pillow képmegjelenítéshez",
                        "qrcode QR kód generáláshoz",
                        "pandas CSV exportáláshoz"
                    ]
                },
                "requirements": {
                    "title": "Követelmények",
                    "content": "A program futtatásához szükséges Python 3.x és a következő külső modulok: pillow, qrcode, reportlab, pandas."
                },
                "contact": {
                        "title": "Kapcsolat",
                        "content": "Fejlesztő: Varga László (DeepSeek AI segítségével. Köszi Szebi!)\nE-mail: laszlo.varga4@proton.me\nTelefon: +36 70 296 8840\nVerzió:    5.2\nDátum: 2025.03.20."                   
                }
            }
        }
    }
    
    if lang == "en":
        en_texts = {
            "app_title": "Contact Manager Program",
            "label_id": "ID:",
            "label_name": "Name:",
            "label_nickname": "Nickname:",
            "label_phone": "Phone:",
            "label_email": "Email:",
            "label_address": "Address:",
            "label_workplace": "Workplace:",
            "label_work_email": "Work Email:",
            "label_work_phone": "Work Phone:",
            "label_note": "Note:",
            "button_new_contact": "New contact",
            "button_search": "Search",
            "button_modify": "Modify",
            "button_abc_sort": "ABC Listing",
            "button_delete": "Delete contact",
            "button_save": "Save",
            "button_load": "Load",
            "button_clear": "Clear record",
            "menu_file": "File",
            "menu_new_contact": "New contact",
            "menu_search": "Search",
            "menu_modify": "Modify",
            "menu_delete": "Delete contact",
            "menu_save": "Save",
            "menu_load": "Load",
            "menu_clear": "Clear record",
            "menu_switch_database": "Switch database",
            "menu_new_database": "New database",
            "menu_exit": "Exit",
            "toggle_language": "Switch language",
            "menu_check_duplicates": "Check duplicate IDs",
            "menu_rebuild_ids": "Rebuild indexes",
            "menu_print": "Print",
            "menu_print_selected": "Selected contact to PDF",
            "menu_print_all": "Full list to PDF",
            "menu_export_csv": "Export full list to CSV",
            "menu_help": "Help",
            "menu_user_guide": "User documentation",
            "menu_description": "Program description",
            "menu_dark_mode": "Toggle dark mode",
            "menu_print_user_guide": "Print user guide to PDF",
            "menu_print_description": "Print program description to PDF",
            "confirm_title": "Confirmation",
            "confirm_delete": "Are you sure you want to delete?",
            "confirm_switch_database": "There are unsaved changes. Are you sure you want to switch database?",
            "confirm_new_database": "There are unsaved changes. Are you sure you want to create new database?",
            "confirm_unsaved": "There are unsaved changes. Do you want to save?",
            "error_title": "Error",
            "error_duplicate_ids": "Duplicate IDs found: {duplicate_ids}",
            "error_csv_open_failed": "Error occurred while creating CSV file",
            "info_title": "Info",
            "info_csv_created": "CSV file created: {filename}",
            "program_title": "Contact Manager Program",
            "footer_version": "Version: {version} | Print date: {current_time}",
            "eco_message": "You saved {saved_pages} pages of paper so far!",
            "csv_headers": ["ID", "Name", "Nickname", "Phone", "Email", "Address", "Workplace", "Work Email", "Work Phone", "Note", "Photo"],
            "current_database": "Current database: {0}",
            "loaded_data": "Loaded data: {0} | Search results: {1}",
            "user_guide": {
                "title": "User Guide",
                "sections": {
                    "intro": {
                        "title": "Introduction",
                        "content": "This is a contact manager application that helps you manage your contacts easily."
                    },
                    "basic_operations": {
                        "title": "Basic Operations",
                        "items": [
                            "Add new contact: Ctrl+N or 'New contact' button",
                            "Modify contact: Ctrl+M or 'Modify' button",
                            "Delete contact: Ctrl+T or 'Delete' button",
                            "Search: Ctrl+K or 'Search' button",
                            "ABC sorting: Ctrl+A or 'ABC Listing' button"
                        ]
                    },
                    "data_management": {
                        "title": "Data Management",
                        "items": [
                            "Save data: Ctrl+S or 'Save' button",
                            "Load data: Ctrl+L or 'Load' button",
                            "Switch database: Ctrl+D or 'File' > 'Switch database'",
                            "New database: Ctrl+Shift+N or 'File' > 'New database'"
                        ]
                    },
                    "export_features": {
                        "title": "Export Features",
                        "items": [
                            "Single contact to PDF: Ctrl+P",
                            "Full list to PDF: Ctrl+Shift+P",
                            "Full list to CSV: Ctrl+E",
                            "QR code generation: Automatic for selected contact"
                        ]
                    },
                    "special_features": {
                        "title": "Special Features",
                        "items": [
                            "Photo management: Click on photo field",
                            "Theme toggle: F3 key",
                            "Language switch: Ctrl+Shift+L",
                            "Check duplicate IDs: Ctrl+Shift+D",
                            "Rebuild indexes: Ctrl+Shift+R"
                        ]
                    },
                    "troubleshooting": {
                        "title": "Troubleshooting",
                        "items": [
                            "File not found: Check path and permissions",
                            "PDF generation error: Verify ReportLab installation",
                            "Slow performance: Reduce database size",
                            "QR code not readable: Check required fields"
                        ]
                    }
                }
            },
            "description": {
                "title": "Program Description",
                "sections": {
                    "about": {
                        "title": "About",
                        "content": "This is a full-featured contact manager application developed in Python. Its main purpose is efficient contact management and organization."
                    },
                    "features": {
                        "title": "Main Features",
                        "items": [
                            "Intuitive Tkinter-based user interface",
                            "Multi-language support (Hungarian/English)",
                            "Data storage in JSON format",
                            "PDF and CSV export options",
                            "QR code generation in vCard format",
                            "Integrated photo management",
                            "Dark/light theme selection"
                        ]
                    },
                    "technical": {
                        "title": "Technical Details",
                        "items": [
                            "Python 3.x based solution",
                            "Tkinter GUI framework",
                            "ReportLab for PDF generation",
                            "Pillow for image display",
                            "qrcode for QR code generation",
                            "pandas for CSV export"
                        ]
                    },
                    "requirements": {
                        "title": "Requirements",
                        "content": "To run this program you need Python 3.x and the following external modules: pillow, qrcode, reportlab, pandas."
                    },
                    "contact": {
                        "title": "Contact",
                        "content": "Developer: Varga László\nVersion: 5.2\nDate: 2025.03.20."
                    }
                }
            }
        }
        return {**default_texts, **en_texts}
    return default_texts

class CustomMessageBox:
    def __init__(self, master, title, message, dark_mode=False):
        self.master = master
        self.dark_mode = dark_mode
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.geometry(f"{max(300, min(500, len(message)*8))}x100")
        self.top.configure(bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        
        self.label = tk.Label(self.top, text=message, 
                            bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR, 
                            fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR)
        self.label.pack(pady=10, padx=10)
        
        self.button = tk.Button(self.top, text="OK", command=self.top.destroy,
                              bg=DARK_BUTTON_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR,
                              fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR)
        self.button.pack(pady=10)

class CustomYesNoMessageBox:
    def __init__(self, master, title, message, dark_mode=False):
        self.master = master
        self.dark_mode = dark_mode
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.geometry(f"{max(300, min(500, len(message)*8))}x100")
        self.top.configure(bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        
        self.label = tk.Label(self.top, text=message,
                            bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR,
                            fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR)
        self.label.pack(pady=10, padx=10)
        
        button_frame = tk.Frame(self.top, bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        button_frame.pack(pady=10)
        
        self.yes_button = tk.Button(button_frame, text="Igen", command=self.yes,
                                  bg=DARK_BUTTON_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR,
                                  fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR)
        self.yes_button.pack(side=tk.LEFT, padx=10)
        
        self.no_button = tk.Button(button_frame, text="Nem", command=self.no,
                                 bg=DARK_BUTTON_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR,
                                 fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR)
        self.no_button.pack(side=tk.RIGHT, padx=10)
        
        self.response = None

    def yes(self):
        self.response = True
        self.top.destroy()

    def no(self):
        self.response = False
        self.top.destroy()

    def show(self):
        self.master.wait_window(self.top)
        return self.response

class PhotoWidgets:
    def __init__(self, master, dark_mode=False):
        self.master = master
        self.dark_mode = dark_mode
        self.current_photo = None
        self.current_photo_tk = None
        self.current_photo_path = None
        self.current_database = None
        
        self.main_frame = tk.Frame(master, bg=DARK_BG_COLOR if dark_mode else LIGHT_BG_COLOR)
        self.main_frame.grid(row=1, column=5, rowspan=10, padx=10, pady=5, sticky="ns")
        
        self.photo_frame = tk.Frame(self.main_frame, 
                                  bg=DARK_BG_COLOR if dark_mode else LIGHT_BG_COLOR,
                                  bd=2, relief=tk.GROOVE)
        self.photo_frame.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)
        
        self.photo_label = tk.Label(self.photo_frame, 
                                  text="Fénykép",
                                  bg=DARK_BG_COLOR if dark_mode else LIGHT_BG_COLOR,
                                  fg=DARK_TEXT_COLOR if dark_mode else LIGHT_TEXT_COLOR,
                                  font=('Arial', 10, 'bold'))
        self.photo_label.pack(pady=(5, 0))
        
        self.photo_widget = tk.Label(self.photo_frame, 
                                   bg=DARK_BG_COLOR if dark_mode else LIGHT_BG_COLOR,
                                   cursor="hand2")
        self.photo_widget.pack(pady=5)
        self.photo_widget.bind("<Button-1>", self.upload_photo)
        
        self.remove_photo_button = tk.Button(
            self.photo_frame,
            text="Fénykép eltávolítása",
            command=self.remove_photo,
            bg=DARK_BUTTON_COLOR if dark_mode else LIGHT_BUTTON_COLOR,
            fg=DARK_TEXT_COLOR if dark_mode else LIGHT_TEXT_COLOR,
            font=('Arial', 8)
        )
        self.remove_photo_button.pack(pady=5)
        
        self.default_avatar = self.create_default_avatar()
        self.set_photo(self.default_avatar)
        
        self.qr_frame = tk.Frame(self.main_frame, 
                               bg=DARK_BG_COLOR if dark_mode else LIGHT_BG_COLOR,
                               bd=2, relief=tk.GROOVE)
        self.qr_frame.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)
        
        self.qr_label = tk.Label(self.qr_frame, 
                               text="vCard QR kód",
                               bg=DARK_BG_COLOR if dark_mode else LIGHT_BG_COLOR,
                               fg=DARK_TEXT_COLOR if dark_mode else LIGHT_TEXT_COLOR,
                               font=('Arial', 10, 'bold'))
        self.qr_label.pack(pady=(5, 0))
        
        self.qr_widget = tk.Label(self.qr_frame, 
                                bg=DARK_BG_COLOR if dark_mode else LIGHT_BG_COLOR)
        self.qr_widget.pack(pady=5)
        
        self.current_qr = None
    
    def set_database(self, db_name):
        self.current_database = db_name
        db_base = os.path.splitext(db_name)[0]
        self.photo_dir = f"contact_photos_{db_base}"
        if not os.path.exists(self.photo_dir):
            os.makedirs(self.photo_dir)
    
    def create_default_avatar(self):
        img = Image.new('RGB', PHOTO_SIZE, color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        draw.ellipse((30, 30, 120, 120), fill=(255, 255, 255))
        draw.ellipse((50, 60, 70, 80), fill=(0, 0, 0))
        draw.ellipse((80, 60, 100, 80), fill=(0, 0, 0))
        draw.arc((50, 70, 100, 110), start=0, end=180, fill=(0, 0, 0), width=2)
        return img
    
    def set_photo(self, photo, photo_path=None):
        photo = photo.resize(PHOTO_SIZE, Image.LANCZOS)
        self.current_photo = photo
        self.current_photo_tk = ImageTk.PhotoImage(photo)
        self.photo_widget.config(image=self.current_photo_tk)
        self.current_photo_path = photo_path
    
    def upload_photo(self, event=None):
        if not self.current_database:
            return None
            
        file_path = filedialog.askopenfilename(
            title="Fénykép feltöltése",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                if not os.path.exists(self.photo_dir):
                    os.makedirs(self.photo_dir)
                
                photo = Image.open(file_path)
                unique_filename = f"{uuid.uuid4()}.{DEFAULT_PHOTO_FORMAT.lower()}"
                save_path = os.path.join(self.photo_dir, unique_filename)
                photo.save(save_path, format=DEFAULT_PHOTO_FORMAT)
                self.set_photo(photo, save_path)
                return save_path
            except Exception as e:
                print(f"Hiba a fénykép feltöltésekor: {e}")
                return None
        return None
    
    def remove_photo(self):
        if self.current_photo_path and os.path.exists(self.current_photo_path):
            try:
                os.remove(self.current_photo_path)
            except Exception as e:
                print(f"Hiba a fénykép törlésekor: {e}")
        self.set_photo(self.create_default_avatar())
        self.current_photo_path = None
    
    def generate_vcard_qr(self, contact_data):
        try:
            name = contact_data.get('name', '')
            phone = contact_data.get('phone', '')
            email = contact_data.get('email', '')
            address = contact_data.get('address', '')
            workplace = contact_data.get('workplace', '')
            work_email = contact_data.get('work_email', '')
            work_phone = contact_data.get('work_phone', '')
            note = contact_data.get('note', '')
            
            vcard_data = [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"FN:{name}",
                f"TEL;TYPE=CELL:{phone}",
                f"EMAIL:{email}",
                f"ADR:{address}",
                f"ORG:{workplace}",
                f"EMAIL;TYPE=WORK:{work_email}",
                f"TEL;TYPE=WORK:{work_phone}",
                f"NOTE:{note}",
                "END:VCARD"
            ]
            vcard_str = "\n".join(vcard_data).encode('utf-8')
            
            qr = qrcode.QRCode(version=1, box_size=4, border=2)
            qr.add_data(vcard_str)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            return img
        except Exception as e:
            print(f"Hiba a QR kód generálásakor: {e}")
            return None
    
    def update_qr_code(self, contact_data):
        qr_img = self.generate_vcard_qr(contact_data)
        if qr_img:
            qr_img = qr_img.resize((150, 150), Image.LANCZOS)
            self.current_qr = ImageTk.PhotoImage(qr_img)
            self.qr_widget.config(image=self.current_qr)
        else:
            self.clear_qr_code()
    
    def clear_qr_code(self):
        self.qr_widget.config(image='')
    
    def get_photo_path(self):
        return self.current_photo_path

class Cimnyilvantarto:
    def __init__(self, master):
        self.master = master
        self.settings = self.load_settings()
        self.dark_mode = self.settings.get("dark_mode", False)
        self.pages_saved = self.settings.get("pages_saved", 0)
        self.current_database = self.settings.get("current_database", "contacts.json")
        window_geometry = self.settings.get("window", "1000x700")
        
        self.icon_size = self.settings.get("icon_size", 14)
        self.menu_text_size = self.settings.get("menu_text_size", 9)
        self.button_text_size = self.settings.get("button_text_size", 9)
        
        global LANGUAGE, TEXTS
        LANGUAGE = self.settings.get("lang", "hu")
        TEXTS = load_language(LANGUAGE)
        
        self.icon_font = ("Arial", self.icon_size)
        self.button_font = ("Arial", self.button_text_size)
        self.menu_font = ("Arial", self.menu_text_size)
        
        master.title(TEXTS.get("app_title", "Címnyilvántartó Program"))
        master.geometry(window_geometry)
        
        self.contacts = []
        self.current_search_indices = []
        self.data_changed = False
        self.free_ids = set()
        
        self.load_icons()
        self.configure_grid()
        self.create_menu()
        self.create_entries()
        self.create_buttons()
        self.create_listbox()
        self.create_info_footer()
        self.set_shortcuts()
        
        self.photo_widgets = PhotoWidgets(self.master, self.dark_mode)
        self.photo_widgets.set_database(self.current_database)
        
        if self.dark_mode:
            self.apply_dark_mode()
        
        master.protocol("WM_DELETE_WINDOW", self.auto_mentes)
        self.betolt(silent=True)

    def configure_grid(self):
        for i in range(6):
            self.master.grid_columnconfigure(i, weight=1 if i < 5 else 0)
        
        for i in range(16):
            self.master.grid_rowconfigure(i, weight=0)
        self.master.grid_rowconfigure(14, weight=1)

    def load_icons(self):
        self.new_icon = "📄"
        self.search_icon = "🔍"
        self.modify_icon = "✏️"
        self.delete_icon = "🗑️"
        self.save_icon = "💾"
        self.load_icon = "📂"
        self.clear_icon = "🧹"
        self.exit_icon = "🚪"
        self.language_icon = "🌐"
        self.duplicate_icon = "🔄"
        self.rebuild_icon = "🔧"
        self.print_icon = "🖨️"
        self.print_all_icon = "📋"
        self.export_icon = "📊"
        self.help_icon = "❓"
        self.description_icon = "📝"
        self.dark_mode_icon = "🌙"
        self.print_help_icon = "📘"
        self.print_desc_icon = "📋"
        self.button_new_icon = "➕"
        self.button_search_icon = "🔎"
        self.button_modify_icon = "✏️"
        self.button_sort_icon = "🔠"
        self.button_delete_icon = "🗑️"
        self.button_save_icon = "💾"
        self.button_load_icon = "📂"
        self.button_clear_icon = "🧹"
        self.database_icon = "🗄️"
        self.new_db_icon = "🆕"
        self.photo_icon = "📷"

    def load_settings(self):
        try:
            if os.path.exists('set.json'):
                with open('set.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    settings.setdefault("icon_size", 14)
                    settings.setdefault("menu_text_size", 9)
                    settings.setdefault("button_text_size", 9)
                    settings.setdefault("pages_saved", 0)
                    settings.setdefault("current_database", "contacts.json")
                    return settings
            return {
                "dark_mode": False,
                "window": "1000x700",
                "lang": "hu",
                "icon_size": 14,
                "menu_text_size": 9,
                "button_text_size": 9,
                "pages_saved": 0,
                "current_database": "contacts.json"
            }
        except Exception as e:
            print(f"Hiba a beállítások betöltésekor: {e}")
            return {
                "dark_mode": False,
                "window": "1000x700",
                "lang": "hu",
                "icon_size": 14,
                "menu_text_size": 9,
                "button_text_size": 9,
                "pages_saved": 0,
                "current_database": "contacts.json"
            }

    def save_settings(self):
        try:
            settings = {
                "dark_mode": self.dark_mode,
                "window": self.master.geometry(),
                "lang": LANGUAGE,
                "icon_size": self.icon_size,
                "menu_text_size": self.menu_text_size,
                "button_text_size": self.button_text_size,
                "pages_saved": self.pages_saved,
                "current_database": self.current_database
            }
            with open('set.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Hiba a beállítások mentésekor: {e}")

    def apply_dark_mode(self):
        bg_color = DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR
        text_color = DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR
        entry_color = DARK_ENTRY_COLOR if self.dark_mode else LIGHT_ENTRY_COLOR
        button_color = DARK_BUTTON_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR
        menu_bg = DARK_MENU_BG_COLOR if self.dark_mode else MENU_BG_COLOR
        menu_text = DARK_MENU_TEXT_COLOR if self.dark_mode else MENU_TEXT_COLOR
        
        self.master.configure(bg=bg_color)
        
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=bg_color, fg=text_color)
            elif isinstance(widget, (tk.Entry, tk.Text)):
                widget.configure(bg=entry_color, fg=text_color)
            elif isinstance(widget, tk.Button):
                widget.configure(bg=button_color, fg=text_color)
            elif isinstance(widget, tk.Listbox):
                widget.configure(bg=menu_bg, fg=text_color)
            elif isinstance(widget, tk.Scrollbar):
                widget.configure(bg=DARK_SCROLLBAR_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR,
                               troughcolor=bg_color)
        
        self.menubar.configure(bg=menu_bg, fg=menu_text)
        self.file_menu.configure(bg=menu_bg, fg=menu_text)
        self.print_menu.configure(bg=menu_bg, fg=menu_text)
        self.help_menu.configure(bg=menu_bg, fg=menu_text)
        
        self.footer_label.configure(bg=menu_bg, fg=menu_text)
        self.eco_label.configure(bg=bg_color)
        
        self.photo_widgets.main_frame.configure(bg=bg_color)
        self.photo_widgets.photo_frame.configure(bg=bg_color)
        self.photo_widgets.qr_frame.configure(bg=bg_color)
        self.photo_widgets.photo_widget.configure(bg=bg_color)
        self.photo_widgets.qr_widget.configure(bg=bg_color)
        self.photo_widgets.photo_label.configure(bg=bg_color, fg=text_color)
        self.photo_widgets.qr_label.configure(bg=bg_color, fg=text_color)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_dark_mode()

    def create_menu(self):
        self.menubar = tk.Menu(self.master, bg=MENU_BG_COLOR, fg=MENU_TEXT_COLOR, font=self.menu_font)
        self.master.config(menu=self.menubar)
        
        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg=MENU_BG_COLOR, fg=MENU_TEXT_COLOR, font=self.menu_font)
        self.menubar.add_cascade(label=TEXTS.get("menu_file", "Fájl"), menu=self.file_menu)
        self.file_menu.add_command(
            label=f"{self.new_icon} {TEXTS.get('menu_new_contact', 'Új felvétel')}", 
            command=self.uj_contact,
            font=self.menu_font,
            accelerator="Ctrl+N"
        )
        self.file_menu.add_command(
            label=f"{self.search_icon} {TEXTS.get('menu_search', 'Keresés')}", 
            command=self.kereses,
            font=self.menu_font,
            accelerator="Ctrl+K"
        )
        self.file_menu.add_command(
            label=f"{self.modify_icon} {TEXTS.get('menu_modify', 'Módosítás')}", 
            command=self.modosit,
            font=self.menu_font,
            accelerator="Ctrl+M"
        )
        self.file_menu.add_command(
            label=f"{self.delete_icon} {TEXTS.get('menu_delete', 'Kontakt törlése')}", 
            command=self.torles,
            font=self.menu_font,
            accelerator="Ctrl+T"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=f"{self.save_icon} {TEXTS.get('menu_save', 'Mentés')}", 
            command=self.mentes,
            font=self.menu_font,
            accelerator="Ctrl+S"
        )
        self.file_menu.add_command(
            label=f"{self.load_icon} {TEXTS.get('menu_load', 'Betöltés')}", 
            command=self.betolt,
            font=self.menu_font,
            accelerator="Ctrl+L"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=f"{self.clear_icon} {TEXTS.get('menu_clear', 'Üres rekord')}", 
            command=self.clear_entries,
            font=self.menu_font,
            accelerator="Ctrl+R"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=f"{self.database_icon} {TEXTS.get('menu_switch_database', 'Adatbázis váltás')}", 
            command=self.switch_database,
            font=self.menu_font,
            accelerator="Ctrl+D"
        )
        self.file_menu.add_command(
            label=f"{self.new_db_icon} {TEXTS.get('menu_new_database', 'Új adatbázis')}", 
            command=self.create_new_database,
            font=self.menu_font,
            accelerator="Ctrl+Shift+N"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=f"{self.exit_icon} {TEXTS.get('menu_exit', 'Kilépés')}", 
            command=self.auto_mentes,
            font=self.menu_font,
            accelerator="Ctrl+Q"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=f"{self.language_icon} {TEXTS.get('toggle_language', 'Nyelv váltás')}", 
            command=self.toggle_language,
            font=self.menu_font,
            accelerator="Ctrl+Shift+L"
        )
        self.file_menu.add_command(
            label=f"{self.duplicate_icon} {TEXTS.get('menu_check_duplicates', 'Duplikált ID-k keresése')}", 
            command=self.check_duplicate_ids,
            font=self.menu_font,
            accelerator="Ctrl+Shift+D"
        )
        self.file_menu.add_command(
            label=f"{self.rebuild_icon} {TEXTS.get('menu_rebuild_ids', 'Újra indexelés')}", 
            command=self.rebuild_ids,
            font=self.menu_font,
            accelerator="Ctrl+Shift+R"
        )

        self.print_menu = tk.Menu(self.menubar, tearoff=0, bg=MENU_BG_COLOR, fg=MENU_TEXT_COLOR, font=self.menu_font)
        self.menubar.add_cascade(label=TEXTS.get("menu_print", "Nyomtatás"), menu=self.print_menu)
        self.print_menu.add_command(
            label=f"{self.print_icon} {TEXTS.get('menu_print_selected', 'Kiválasztott kontakt PDF-be')}", 
            command=self.nyomtatas_pdf,
            font=self.menu_font,
            accelerator="Ctrl+P"
        )
        self.print_menu.add_command(
            label=f"{self.print_all_icon} {TEXTS.get('menu_print_all', 'Teljes lista PDF-be')}", 
            command=self.teljes_lista_pdf,
            font=self.menu_font,
            accelerator="Ctrl+Shift+P"
        )
        self.print_menu.add_command(
            label=f"{self.export_icon} {TEXTS.get('menu_export_csv', 'Teljes lista CSV-be')}", 
            command=self.export_to_csv,
            font=self.menu_font,
            accelerator="Ctrl+E"
        )

        self.help_menu = tk.Menu(self.menubar, tearoff=0, bg=MENU_BG_COLOR, fg=MENU_TEXT_COLOR, font=self.menu_font)
        self.menubar.add_cascade(label=TEXTS.get("menu_help", "Súgó"), menu=self.help_menu)
        self.help_menu.add_command(
            label=f"{self.help_icon} {TEXTS.get('menu_user_guide', 'Felhasználói dokumentáció')}", 
            command=self.show_help,
            font=self.menu_font,
            accelerator="F1"
        )
        self.help_menu.add_command(
            label=f"{self.description_icon} {TEXTS.get('menu_description', 'Program leírása')}", 
            command=self.show_description,
            font=self.menu_font,
            accelerator="F2"
        )
        self.help_menu.add_command(
            label=f"{self.dark_mode_icon} {TEXTS.get('menu_dark_mode', 'Sötét mód váltása')}", 
            command=self.toggle_dark_mode,
            font=self.menu_font,
            accelerator="F3"
        )
        self.help_menu.add_command(
            label=f"{self.print_help_icon} {TEXTS.get('menu_print_user_guide', 'Felhasználói kézikönyv nyomtatása PDF-be')}", 
            command=self.print_user_guide,
            font=self.menu_font,
            accelerator="F4"
        )
        self.help_menu.add_command(
            label=f"{self.print_desc_icon} {TEXTS.get('menu_print_description', 'Program leírás nyomtatása PDF-be')}", 
            command=self.print_description_pdf,
            font=self.menu_font,
            accelerator="F5"
        )

    def find_available_databases(self):
        databases = []
        i = 1
        while True:
            db_name = f"contacts{i}.json" if i > 1 else "contacts.json"
            if os.path.exists(db_name):
                databases.append(db_name)
                i += 1
            else:
                break
        return databases if databases else ["contacts.json"]

    def switch_database(self):
        if self.data_changed:
            response = CustomYesNoMessageBox(
                self.master, 
                TEXTS.get("confirm_title", "Megerősítés"), 
                TEXTS.get("confirm_switch_database", "Vannak nem mentett változtatások. Biztosan váltani akar adatbázist?"), 
                self.dark_mode
            ).show()
            
            if not response:
                return
        
        databases = self.find_available_databases()
        
        if not databases:
            return
        
        selection_window = tk.Toplevel(self.master)
        selection_window.title(TEXTS.get("select_database_title", "Adatbázis kiválasztása"))
        selection_window.geometry("400x300")
        selection_window.configure(bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        
        label = tk.Label(
            selection_window,
            text=TEXTS.get("select_database_prompt", "Válassza ki a használni kívánt adatbázist:"),
            bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR,
            fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR
        )
        label.pack(pady=10)
        
        listbox = tk.Listbox(
            selection_window,
            bg=DARK_ENTRY_COLOR if self.dark_mode else LIGHT_ENTRY_COLOR,
            fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for db in databases:
            listbox.insert(tk.END, db)
        
        def select_db():
            selection = listbox.curselection()
            if selection:
                new_database = databases[selection[0]]
                
                if self.data_changed:
                    self.mentes()
                
                self.current_database = new_database
                self.photo_widgets.set_database(new_database)
                self.save_settings()
                self.betolt(silent=True)
                selection_window.destroy()
        
        button_frame = tk.Frame(selection_window, bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        button_frame.pack(pady=10)
        
        select_button = tk.Button(
            button_frame,
            text="Kiválaszt",
            command=select_db,
            bg=DARK_BUTTON_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR,
            fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR
        )
        select_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Mégse",
            command=selection_window.destroy,
            bg=DARK_BUTTON_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR,
            fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR
        )
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def create_new_database(self):
        if self.data_changed:
            response = CustomYesNoMessageBox(
                self.master, 
                TEXTS.get("confirm_title", "Megerősítés"), 
                TEXTS.get("confirm_new_database", "Vannak nem mentett változtatások. Biztosan új adatbázist akar létrehozni?"), 
                self.dark_mode
            ).show()
            
            if not response:
                return
        
        i = 1
        while True:
            new_db_name = f"contacts{i}.json" if i > 1 else "contacts.json"
            if not os.path.exists(new_db_name):
                break
            i += 1
        
        with open(new_db_name, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        
        if self.data_changed:
            self.mentes()
        
        self.current_database = new_db_name
        self.photo_widgets.set_database(new_db_name)
        self.save_settings()
        self.betolt(silent=True)

    def toggle_language(self):
        global LANGUAGE, TEXTS
        LANGUAGE = "en" if LANGUAGE == "hu" else "hu"
        TEXTS = load_language(LANGUAGE)
        
        self.master.title(TEXTS.get("app_title", "Címnyilvántartó Program"))
        
        for widget in self.master.winfo_children():
            widget.destroy()
        
        self.load_icons()
        self.create_menu()
        self.create_entries()
        self.create_buttons()
        self.create_listbox()
        self.create_info_footer()
        
        self.photo_widgets = PhotoWidgets(self.master, self.dark_mode)
        self.photo_widgets.set_database(self.current_database)
        
        if self.dark_mode:
            self.apply_dark_mode()
        
        self.abc_listazas()

    def rebuild_ids(self):
        for index, contact in enumerate(self.contacts, start=1):
            contact['id'] = index
        self.free_ids = set()
        self.data_changed = True
        self.abc_listazas()

    def show_text_window(self, title, text, width=700, height=450):
        window = tk.Toplevel(self.master)
        window.title(title)
        window.geometry(f"{width}x{height}")
        window.configure(bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        
        text_frame = tk.Frame(window, bg=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_box = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg=DARK_ENTRY_COLOR if self.dark_mode else LIGHT_ENTRY_COLOR,
            fg=DARK_TEXT_COLOR if self.dark_mode else LIGHT_TEXT_COLOR,
            padx=10,
            pady=10
        )
        text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_box.yview)
        
        text_box.insert(tk.END, text)
        text_box.config(state=tk.DISABLED)
        
        def copy_text(event):
            self.master.clipboard_clear()
            self.master.clipboard_append(text_box.selection_get())
        
        text_box.bind("<Control-c>", copy_text)
        text_box.bind("<Control-C>", copy_text)

    def show_help(self):
        """Display comprehensive help information in a new window"""
        try:
            help_text = []
            if "user_guide" in TEXTS:
                for section_name, section in TEXTS["user_guide"].get("sections", {}).items():
                    help_text.append(f"\n{section.get('title', '')}\n{'=' * len(section.get('title', ''))}")
                    if 'content' in section:
                        help_text.append(f"\n{section['content']}\n")
                    if 'items' in section:
                        help_text.extend([f"• {item}" for item in section['items']])
                    help_text.append("\n")
            
            # Add keyboard shortcuts section
            help_text.append("\nGyorsbillentyűk\n==============")
            help_text.extend([
                "\n• Ctrl+N - Új kapcsolat",
                "• Ctrl+M - Módosítás",
                "• Ctrl+T - Törlés",
                "• Ctrl+K - Keresés",
                "• Ctrl+S - Mentés",
                "• Ctrl+L - Betöltés",
                "• Ctrl+P - PDF export (kiválasztott)",
                "• Ctrl+Shift+P - PDF export (összes)",
                "• Ctrl+E - CSV export",
                "• Ctrl+D - Adatbázis váltás",
                "• Ctrl+A - ABC sorrend",
                "• Ctrl+R - Mezők törlése",
                "• F1 - Súgó",
                "• F2 - Program leírás",
                "• F3 - Sötét mód váltás",
                "• F4 - Felhasználói kézikönyv nyomtatása",
                "• F5 - Program leírás nyomtatása",
                "• Ctrl+Shift+L - Nyelv váltás",
                "• Ctrl+Shift+D - Duplikált ID-k keresése",
                "• Ctrl+Shift+R - Újraindexelés"
            ])
            
            if "requirements" in TEXTS:
                help_text.append(f"\n\n{TEXTS['requirements']['title']}\n{'=' * len(TEXTS['requirements']['title'])}")
                help_text.append(f"\n{TEXTS['requirements']['content']}")
            
            help_text.append(f"\n\n{TEXTS.get('eco_message', 'Ön eddig {saved_pages} oldal papírt takarított meg!').format(saved_pages=self.pages_saved)}")
            help_text.append("\n\nVerzió: 5.2 | Fejlesztő: Varga László | 2025.03.20.")
            
            self.show_text_window(
                TEXTS.get("user_guide", {}).get("title", "Felhasználói kézikönyv"),
                "\n".join(help_text),
                width=800,
                height=600
            )
        except Exception as e:
            messagebox.showerror(
                TEXTS.get("error_title", "Error"),
                f"{TEXTS.get('error_loading_guide', 'Failed to load guide')}: {str(e)}"
            )

    def show_description(self):
        """Display detailed program description in a new window"""
        try:
            desc_text = []
            if "description" in TEXTS:
                for section_name, section in TEXTS["description"].get("sections", {}).items():
                    desc_text.append(f"\n{section.get('title', '')}\n{'=' * len(section.get('title', ''))}")
                    if 'content' in section:
                        desc_text.append(f"\n{section['content']}\n")
                    if 'items' in section:
                        desc_text.extend([f"• {item}" for item in section['items']])
                    desc_text.append("\n")
            
            # Add technical details
            desc_text.append("\nTechnikai információk\n====================")
            desc_text.extend([
                "\n• Python verzió: 3.x",
                "• Használt könyvtárak:",
                "  - Tkinter (GUI)",
                "  - ReportLab (PDF generálás)",
                "  - Pillow (képkezelés)",
                "  - qrcode (QR kód generálás)",
                "  - pandas (CSV export)"
            ])
            
            desc_text.append("\n\nLicenc: MIT")
            desc_text.append("\nFejlesztő: Varga László")
            desc_text.append(f"\nVerzió: {VERSION} | Utolsó frissítés: 2025.03.20.")
            
            self.show_text_window(
                TEXTS.get("description", {}).get("title", "Program leírás"),
                "\n".join(desc_text),
                width=800,
                height=600
            )
        except Exception as e:
            messagebox.showerror(
                TEXTS.get("error_title", "Error"),
                f"{TEXTS.get('error_loading_description', 'Failed to load description')}: {str(e)}"
            )

    def print_user_guide(self):
        try:
            help_text = []
            if "user_guide" in TEXTS:
                for section_name, section in TEXTS["user_guide"].get("sections", {}).items():
                    help_text.append(f"\n{section.get('title', '')}\n{'=' * len(section.get('title', ''))}")
                    if 'content' in section:
                        help_text.append(f"\n{section['content']}\n")
                    if 'items' in section:
                        help_text.extend([f"• {item}" for item in section['items']])
                    help_text.append("\n")
            
            if "requirements" in TEXTS:
                help_text.append(f"\n\n{TEXTS['requirements']['title']}\n{'=' * len(TEXTS['requirements']['title'])}")
                help_text.append(f"\n{TEXTS['requirements']['content']}")
            
            filename = "felhasznaloi_kezikonyv.pdf"
            self.generate_pdf_from_text("\n".join(help_text), filename)
            self.show_pdf(filename)
            self.calculate_paper_saving(len(help_text) // 60)
        except Exception as e:
            pass

    def print_description_pdf(self):
        try:
            desc_text = []
            if "description" in TEXTS:
                for section_name, section in TEXTS["description"].get("sections", {}).items():
                    desc_text.append(f"\n{section.get('title', '')}\n{'=' * len(section.get('title', ''))}")
                    if 'content' in section:
                        desc_text.append(f"\n{section['content']}\n")
                    if 'items' in section:
                        desc_text.extend([f"• {item}" for item in section['items']])
                    desc_text.append("\n")
            
            filename = "program_leiras.pdf"
            self.generate_pdf_from_text("\n".join(desc_text), filename)
            self.show_pdf(filename)
            self.calculate_paper_saving(len(desc_text) // 60)
        except Exception as e:
            pass

    def generate_pdf_from_text(self, text, filename):
        c = canvas.Canvas(filename, pagesize=A4)
        
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
            c.setFont("DejaVuSans", 8)
        except:
            c.setFont("Helvetica", 8)
        
        c.setFillColor(PDF_TEXT_COLOR)
        c.setStrokeColor(PDF_TEXT_COLOR)

        def add_header_footer(canvas, page_number):
            try:
                canvas.setFont("DejaVuSans-Bold", 12)
            except:
                canvas.setFont("Helvetica-Bold", 12)
            canvas.drawCentredString(A4[0]/2, A4[1]-30, TEXTS.get("program_title", "Címnyilvántartó Program"))
            
            try:
                canvas.setFont("DejaVuSans", 6)
            except:
                canvas.setFont("Helvetica", 6)
            canvas.drawCentredString(A4[0]/2, A4[1]-40, f"({os.path.abspath(filename)})")
            
            try:
                canvas.setFont("DejaVuSans", 10)
            except:
                canvas.setFont("Helvetica", 10)
            canvas.drawCentredString(A4[0]/2, A4[1]-50, f"{TEXTS.get('footer_version', 'Verzió: {version} | Nyomtatás dátuma: {current_time}').format(version=VERSION, current_time=datetime.now().strftime('%Y-%m-%d. %H:%M'))}")
            try:
                canvas.setFont("DejaVuSans", 8)
            except:
                canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(A4[0]/2, 10, f"Oldal: {page_number}")
            canvas.drawString(A4[0]-150, A4[1]-70, f"Megtakarított papír: {self.pages_saved} oldal")

        page_number = 1
        add_header_footer(c, page_number)

        lines = text.splitlines()
        y = 750
        for line in lines:
            if y < 40:
                c.showPage()
                page_number += 1
                add_header_footer(c, page_number)
                y = 750
            c.drawString(50, y, line)
            y -= 12

        c.save()

    def create_entries(self):
        tk.Label(self.master, text=TEXTS.get("label_id", "ID:"), 
               bg=LIGHT_BG_COLOR if not self.dark_mode else DARK_BG_COLOR,
               fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR).grid(row=2, column=0, sticky="e", padx=2, pady=1)
        self.id_entry = tk.Entry(self.master, width=ENTRY_WIDTH,
                               bg=LIGHT_ENTRY_COLOR if not self.dark_mode else DARK_ENTRY_COLOR,
                               fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR)
        self.id_entry.grid(row=2, column=1, columnspan=3, sticky="we", padx=2, pady=1)

        labels = [
            (TEXTS.get("label_name", "Név:"), 3),
            (TEXTS.get("label_nickname", "Becenév:"), 4),
            (TEXTS.get("label_phone", "Telefonszám:"), 5),
            (TEXTS.get("label_email", "E-mail:"), 6),
            (TEXTS.get("label_address", "Cím:"), 7),
            (TEXTS.get("label_workplace", "Munkahely:"), 8),
            (TEXTS.get("label_work_email", "Munkahelyi E-mail:"), 9),
            (TEXTS.get("label_work_phone", "Munkahelyi Telefon:"), 10),
            (TEXTS.get("label_note", "Megjegyzés:"), 11)
        ]
        
        self.entries = []
        for text, row in labels:
            tk.Label(self.master, text=text,
                   bg=LIGHT_BG_COLOR if not self.dark_mode else DARK_BG_COLOR,
                   fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR).grid(row=row, column=0, sticky="e", padx=2, pady=1)
            
            if text == TEXTS.get("label_note", "Megjegyzés:"):
                entry = tk.Text(self.master, width=ENTRY_WIDTH, height=3,
                              bg=LIGHT_ENTRY_COLOR if not self.dark_mode else DARK_ENTRY_COLOR,
                              fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR)
                entry.grid(row=row, column=1, columnspan=3, sticky="we", padx=2, pady=1)
            else:
                entry = tk.Entry(self.master, width=ENTRY_WIDTH,
                               bg=LIGHT_ENTRY_COLOR if not self.dark_mode else DARK_ENTRY_COLOR,
                               fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR)
                entry.grid(row=row, column=1, columnspan=3, sticky="we", padx=2, pady=1)
            
            if text in [TEXTS.get("label_email", "E-mail:"), TEXTS.get("label_work_email", "Munkahelyi E-mail:")]:
                email_icon = tk.Label(self.master, text="✉", fg="blue", cursor="hand2",
                                    bg=LIGHT_BG_COLOR if not self.dark_mode else DARK_BG_COLOR,
                                    font=self.icon_font)
                email_icon.grid(row=row, column=4, sticky="w", padx=2)
                email_icon.bind("<Button-1>", lambda e, entry=entry: self.send_email(entry))
            
            self.entries.append(entry)

    def create_buttons(self):
        buttons = [
            (f"{self.button_new_icon} {TEXTS.get('button_new_contact', 'Új felvétel')}", self.uj_contact, 12, 0),
            (f"{self.button_search_icon} {TEXTS.get('button_search', 'Keresés')}", self.kereses, 12, 1),
            (f"{self.button_modify_icon} {TEXTS.get('button_modify', 'Módosítás')}", self.modosit, 12, 2),
            (f"{self.button_sort_icon} {TEXTS.get('button_abc_sort', 'ABC Listázás')}", self.abc_listazas, 12, 3),
            (f"{self.button_delete_icon} {TEXTS.get('button_delete', 'Kontakt törlése')}", self.torles, 13, 0),
            (f"{self.button_save_icon} {TEXTS.get('button_save', 'Mentés')}", self.mentes, 13, 1),
            (f"{self.button_load_icon} {TEXTS.get('button_load', 'Betöltés')}", self.betolt, 13, 2),
            (f"{self.button_clear_icon} {TEXTS.get('button_clear', 'Üres rekord')}", self.clear_entries, 13, 3)
        ]
        
        for text, command, row, col in buttons:
            button = tk.Button(self.master, text=text, command=command,
                             bg=LIGHT_BUTTON_COLOR if not self.dark_mode else DARK_BUTTON_COLOR,
                             fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR,
                             font=self.button_font,
                             compound=tk.LEFT)
            button.grid(row=row, column=col, sticky="we", padx=5, pady=5)

    def create_listbox(self):
        self.listbox = tk.Listbox(self.master, width=50, height=10,
                                bg=MENU_BG_COLOR if not self.dark_mode else DARK_MENU_BG_COLOR,
                                fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR)
        self.listbox.grid(row=14, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.select_contact)
        
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical",
                                    bg=DARK_SCROLLBAR_COLOR if self.dark_mode else LIGHT_BUTTON_COLOR,
                                    troughcolor=DARK_BG_COLOR if self.dark_mode else LIGHT_BG_COLOR)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.grid(row=14, column=4, sticky="ns")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

    def create_info_footer(self):
        current_time = datetime.now().strftime("%Y-%m-%d. %H:%M")
        
        self.db_label = tk.Label(self.master,
                              text=TEXTS.get("current_database", "Aktuális adatbázis: {0}").format(self.current_database),
                              bg=LIGHT_BG_COLOR if not self.dark_mode else DARK_BG_COLOR,
                              fg="blue" if not self.dark_mode else "#4CAF50",
                              font=("Arial", 10, "bold"))
        self.db_label.grid(row=0, column=0, columnspan=6, sticky="we", padx=5, pady=2)
        
        self.info_label = tk.Label(self.master,
                                text=TEXTS.get("loaded_data", "Feltöltött adatok: {0} | Keresés eredménye: {1}").format(len(self.contacts), len(self.current_search_indices) if hasattr(self, 'current_search_indices') else 0),
                                bg=LIGHT_BG_COLOR if not self.dark_mode else DARK_BG_COLOR,
                                fg=LIGHT_TEXT_COLOR if not self.dark_mode else DARK_TEXT_COLOR)
        self.info_label.grid(row=1, column=0, columnspan=6, sticky="we", padx=5, pady=2)
        
        self.eco_label = tk.Label(self.master,
                               text=TEXTS.get("eco_message", "Ön eddig {saved_pages} oldal papírt takarított meg!").format(saved_pages=self.pages_saved),
                               bg=LIGHT_BG_COLOR if not self.dark_mode else DARK_BG_COLOR,
                               fg="green" if not self.dark_mode else "#4CAF50",
                               font=("Arial", 8, "italic"))
        self.eco_label.grid(row=15, column=0, columnspan=6, sticky="we", padx=5, pady=2)
        
        self.footer_label = tk.Label(self.master,
                                  text=f"DeepSeek-R1 ver.:9.11 | By: VargaL. | {TEXTS.get('footer_version', 'Verzió: {version} | Nyomtatás dátuma: {current_time}').format(version=VERSION, current_time=current_time)}",
                                  fg=MENU_TEXT_COLOR if not self.dark_mode else DARK_MENU_TEXT_COLOR,
                                  bg=MENU_BG_COLOR if not self.dark_mode else DARK_MENU_BG_COLOR)
        self.footer_label.grid(row=16, column=0, columnspan=6, sticky="we", padx=5, pady=5)

    def set_shortcuts(self):
        shortcuts = {
            '<Control-n>': lambda e: self.uj_contact(),
            '<Control-k>': lambda e: self.kereses(),
            '<Control-m>': lambda e: self.modosit(),
            '<Control-t>': lambda e: self.torles(),
            '<Control-s>': lambda e: self.mentes(),
            '<Control-l>': lambda e: self.betolt(),
            '<Control-p>': lambda e: self.nyomtatas_pdf(),
            '<Control-Shift-P>': lambda e: self.teljes_lista_pdf(),
            '<Control-e>': lambda e: self.export_to_csv(),
            '<Control-q>': lambda e: self.auto_mentes(),
            '<Control-r>': lambda e: self.clear_entries(),
            '<Control-a>': lambda e: self.abc_listazas(),
            '<F1>': lambda e: self.show_help(),
            '<F2>': lambda e: self.show_description(),
            '<F3>': lambda e: self.toggle_dark_mode(),
            '<F4>': lambda e: self.print_user_guide(),
            '<F5>': lambda e: self.print_description_pdf(),
            '<Control-Shift-D>': lambda e: self.check_duplicate_ids(),
            '<Control-Shift-R>': lambda e: self.rebuild_ids(),
            '<Control-Shift-L>': lambda e: self.toggle_language(),
            '<Control-d>': lambda e: self.switch_database(),
            '<Control-Shift-N>': lambda e: self.create_new_database()
        }
        
        for key, command in shortcuts.items():
            self.master.bind(key, command)

    def calculate_paper_saving(self, pages):
        self.pages_saved += int(pages * PAPER_SAVING_FACTOR)
        self.settings["pages_saved"] = self.pages_saved
        self.save_settings()
        self.eco_label.config(text=TEXTS.get("eco_message", "Ön eddig {saved_pages} oldal papírt takarított meg!").format(saved_pages=self.pages_saved))
        return self.pages_saved

    def uj_contact(self):
        contact_data = self.get_contact_data()
        if not self.validate_contact_data(contact_data):
            return
        
        if self.free_ids:
            contact_data['id'] = min(self.free_ids)
            self.free_ids.remove(contact_data['id'])
        else:
            contact_data['id'] = len(self.contacts) + 1
        
        photo_path = self.photo_widgets.upload_photo()
        if photo_path:
            contact_data['photo'] = photo_path
        
        self.contacts.append(contact_data)
        self.data_changed = True
        self.clear_entries()
        self.update_info()
        self.abc_listazas()

    def get_contact_data(self):
        return {
            'name': self.entries[0].get().strip(),
            'nickname': self.entries[1].get().strip(),
            'phone': self.entries[2].get().strip(),
            'email': self.entries[3].get().strip(),
            'address': self.entries[4].get().strip(),
            'workplace': self.entries[5].get().strip(),
            'work_email': self.entries[6].get().strip(),
            'work_phone': self.entries[7].get().strip(),
            'note': self.entries[8].get("1.0", tk.END).strip()
        }

    def validate_contact_data(self, contact_data):
        if not contact_data['name'] or not contact_data['phone']:
            return False
        return True

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        for entry in self.entries:
            if isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
            else:
                entry.delete(0, tk.END)
        
        self.photo_widgets.set_photo(self.photo_widgets.create_default_avatar())
        self.photo_widgets.clear_qr_code()

    def update_info(self):
        total = len(self.contacts)
        search_count = len(self.current_search_indices) if hasattr(self, 'current_search_indices') else 0
        self.info_label.config(text=TEXTS.get("loaded_data", "Feltöltött adatok: {0} | Keresés eredménye: {1}").format(total, search_count))
        self.db_label.config(text=TEXTS.get("current_database", "Aktuális adatbázis: {0}").format(self.current_database))

    def kereses(self):
        criteria = {}
        id_value = self.id_entry.get().strip().lower()
        if id_value:
            criteria['id'] = id_value

        for field, entry in zip(
            ['name', 'nickname', 'phone', 'email', 'address', 'workplace', 'work_email', 'work_phone', 'note'],
            self.entries
        ):
            value = entry.get().strip().lower() if isinstance(entry, tk.Entry) else entry.get("1.0", tk.END).strip().lower()
            if value:
                criteria[field] = value

        if not criteria:
            self.current_search_indices = list(range(len(self.contacts)))
        else:
            self.current_search_indices = [
                idx for idx, contact in enumerate(self.contacts)
                if all(
                    (field == 'id' and str(contact.get('id', '')).lower() == value) or
                    (field != 'id' and value in str(contact.get(field, '')).lower())
                    for field, value in criteria.items()
                )
            ]

        self.listbox.delete(0, tk.END)
        for idx in self.current_search_indices:
            contact = self.contacts[idx]
            self.listbox.insert(tk.END, f"{contact['id']}. {contact['name']} - {contact['phone']}")
        self.update_info()

    def select_contact(self, event):
        if not self.listbox.curselection() or not hasattr(self, 'current_search_indices'):
            return
        
        selected_index = self.listbox.curselection()[0]
        if selected_index >= len(self.current_search_indices):
            return
        
        index = self.current_search_indices[selected_index]
        contact = self.contacts[index]
        self.clear_entries()
        self.id_entry.insert(0, contact['id'])
        
        for entry, value in zip(self.entries, [
            contact['name'], contact['nickname'], contact['phone'],
            contact['email'], contact['address'], contact['workplace'],
            contact['work_email'], contact['work_phone'], contact['note']
        ]):
            if isinstance(entry, tk.Text):
                entry.insert("1.0", value)
            else:
                entry.insert(0, value)
        
        if 'photo' in contact and contact['photo']:
            try:
                photo = Image.open(contact['photo'])
                self.photo_widgets.set_photo(photo, contact['photo'])
            except Exception as e:
                print(f"Hiba a fénykép betöltésekor: {e}")
                self.photo_widgets.set_photo(self.photo_widgets.create_default_avatar())
        else:
            self.photo_widgets.set_photo(self.photo_widgets.create_default_avatar())
        
        self.photo_widgets.update_qr_code(contact)

    def modosit(self):
        if not self.listbox.curselection() or not hasattr(self, 'current_search_indices'):
            return
        
        selected_index = self.listbox.curselection()[0]
        if selected_index >= len(self.current_search_indices):
            return
        
        index = self.current_search_indices[selected_index]
        contact_data = self.get_contact_data()
        
        if not self.validate_contact_data(contact_data):
            return
        
        photo_path = self.photo_widgets.get_photo_path()
        if photo_path:
            contact_data['photo'] = photo_path
        elif 'photo' in self.contacts[index]:
            contact_data['photo'] = self.contacts[index]['photo']
        
        self.contacts[index] = contact_data
        self.data_changed = True
        self.clear_entries()
        self.update_info()
        self.abc_listazas()

    def torles(self):
        if not self.listbox.curselection() or not hasattr(self, 'current_search_indices'):
            return
        
        selected_index = self.listbox.curselection()[0]
        if selected_index >= len(self.current_search_indices):
            return
        
        confirm = CustomYesNoMessageBox(
            self.master, 
            TEXTS.get("confirm_title", "Megerősítés"), 
            TEXTS.get("confirm_delete", "Valóban törölni akarod?"), 
            self.dark_mode
        ).show()
        
        if not confirm:
            return
        
        index = self.current_search_indices[selected_index]
        contact = self.contacts.pop(index)
        
        if 'photo' in contact and contact['photo'] and os.path.exists(contact['photo']):
            try:
                os.remove(contact['photo'])
            except Exception as e:
                print(f"Hiba a fénykép törlésekor: {e}")
        
        self.free_ids.add(contact['id'])
        self.data_changed = True
        self.clear_entries()
        self.update_info()
        self.abc_listazas()

    def abc_listazas(self):
        magyar_abc = "aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz"
        
        def magyar_sorrend(szo):
            return [magyar_abc.index(karakter) if karakter in magyar_abc else len(magyar_abc) for karakter in szo.lower()]

        self.contacts.sort(key=lambda x: magyar_sorrend(x['name']))
        self.listbox.delete(0, tk.END)
        
        for contact in self.contacts:
            self.listbox.insert(tk.END, f"{contact['id']}. {contact['name']} - {contact['phone']}")
        
        self.current_search_indices = list(range(len(self.contacts)))
        self.update_info()

    def mentes(self):
        try:
            with open(self.current_database, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, ensure_ascii=False, indent=4)
            self.data_changed = False
        except Exception as e:
            pass

    def betolt(self, silent=False):
        if not os.path.exists(self.current_database):
            self.contacts = []
            return
        
        try:
            with open(self.current_database, 'r', encoding='utf-8') as f:
                self.contacts = json.load(f)
            
            used_ids = set()
            for contact in self.contacts:
                if 'id' not in contact:
                    contact['id'] = len(self.contacts) + 1
                used_ids.add(contact['id'])
            
            all_ids = set(range(1, len(self.contacts) + 1))
            self.free_ids = all_ids - used_ids
        
            self.abc_listazas()
            self.update_info()
        except Exception as e:
            print(f"Hiba az adatok betöltésekor: {e}")
            self.contacts = []

    def auto_mentes(self):
        if hasattr(self, 'data_changed') and self.data_changed:
            response = CustomYesNoMessageBox(
                self.master, 
                TEXTS.get("confirm_title", "Megerősítés"), 
                TEXTS.get("confirm_unsaved", "Vannak nem mentett változtatások. Szeretnéd menteni?"), 
                self.dark_mode
            ).show()
            if response:
                self.mentes()
        
        self.save_settings()
        self.master.destroy()

    def nyomtatas_pdf(self):
        if not hasattr(self, 'listbox') or not self.listbox.curselection() or not hasattr(self, 'current_search_indices'):
            return
        
        selected_index = self.listbox.curselection()[0]
        if selected_index >= len(self.current_search_indices):
            return
        
        index = self.current_search_indices[selected_index]
        contact = self.contacts[index]
        
        db_base = os.path.splitext(self.current_database)[0]
        filename = f"{db_base}_{contact['name']}_contact.pdf"
        
        try:
            self.generate_pdf([contact], filename)
            self.show_pdf(filename)
            self.calculate_paper_saving(1)
        except Exception as e:
            print(f"Hiba a PDF generálásakor: {e}")

    def teljes_lista_pdf(self):
        if not self.contacts:
            return
        
        db_base = os.path.splitext(self.current_database)[0]
        filename = f"{db_base}_teljes_lista.pdf"
        excel_filename = f"{db_base}_teljes_lista.xlsx"
        
        try:
            estimated_pages = max(1, len(self.contacts) // 10)
            self.generate_pdf(self.contacts, filename)
            self.generate_excel(self.contacts, excel_filename)
            self.show_pdf(filename)
            self.calculate_paper_saving(estimated_pages)
        except Exception as e:
            print(f"Hiba a PDF generálásakor: {e}")

    def _draw_contact(self, c, contact, x, y):
        try:
            c.setFont("DejaVuSans", 10)
        except:
            c.setFont("Helvetica", 10)
        c.drawString(x, y, f"{TEXTS.get('label_id', 'ID:')}: {contact['id']}")
        y -= 12

        try:
            c.setFont("DejaVuSans-Bold", 10)
        except:
            c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, f"{TEXTS.get('label_name', 'Név:')}: {contact['name']}")
        y -= 12

        photo_width, photo_height = 80, 80
        qr_width, qr_height = 80, 80
        
        if 'photo' in contact and contact['photo'] and os.path.exists(contact['photo']):
            try:
                c.drawImage(contact['photo'], x, y - photo_height - 5, width=photo_width, height=photo_height)
            except Exception as e:
                print(f"Hiba a fénykép betöltésekor PDF-hez: {e}")
        
        qr_img = self.photo_widgets.generate_vcard_qr(contact)
        if qr_img:
            temp_qr_path = f"temp_qr_{contact['id']}.png"
            qr_img.save(temp_qr_path)
            c.drawImage(temp_qr_path, x + photo_width + 10, y - qr_height - 5, width=qr_width, height=qr_height)
            os.remove(temp_qr_path)
        
        try:
            c.setFont("DejaVuSans", 8)
        except:
            c.setFont("Helvetica", 8)
        fields = [
            ('label_nickname', 'nickname'),
            ('label_phone', 'phone'),
            ('label_email', 'email'),
            ('label_address', 'address'),
            ('label_workplace', 'workplace'),
            ('label_work_email', 'work_email'),
            ('label_work_phone', 'work_phone'),
            ('label_note', 'note')
        ]
        
        for label, field in fields:
            value = str(contact[field])
            if value:
                c.drawString(x, y - photo_height - 15, f"{TEXTS.get(label, label.capitalize())}: {value}")
                y -= 10
        
        return y - photo_height - 20

    def generate_pdf(self, data, filename):
        c = canvas.Canvas(filename, pagesize=A4)
        
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
            c.setFont("DejaVuSans", 8)
        except:
            c.setFont("Helvetica", 8)
        
        c.setFillColor(PDF_TEXT_COLOR)
        c.setStrokeColor(PDF_TEXT_COLOR)

        def add_header_footer(canvas, page_number):
            try:
                canvas.setFont("DejaVuSans-Bold", 12)
            except:
                canvas.setFont("Helvetica-Bold", 12)
            canvas.drawCentredString(A4[0]/2, A4[1]-30, TEXTS.get("program_title", "Címnyilvántartó Program"))
            
            try:
                canvas.setFont("DejaVuSans", 6)
            except:
                canvas.setFont("Helvetica", 6)
            canvas.drawCentredString(A4[0]/2, A4[1]-40, f"({os.path.abspath(filename)})")
            
            try:
                canvas.setFont("DejaVuSans", 10)
            except:
                canvas.setFont("Helvetica", 10)
            canvas.drawCentredString(A4[0]/2, A4[1]-50, f"{TEXTS.get('footer_version', 'Verzió: {version} | Nyomtatás dátuma: {current_time}').format(version=VERSION, current_time=datetime.now().strftime('%Y-%m-%d. %H:%M'))}")
            try:
                canvas.setFont("DejaVuSans", 8)
            except:
                canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(A4[0]/2, 10, f"Oldal: {page_number}")
            canvas.drawString(A4[0]-150, A4[1]-70, f"Megtakarított papír: {self.pages_saved} oldal")

        page_number = 1
        add_header_footer(c, page_number)

        x_left = 20
        x_right = A4[0]/2 + 5
        y_start = A4[1] - 70
        
        min_space_needed = 150
        contact_spacing = 20

        for i in range(0, len(data), 2):
            if y_start < min_space_needed:
                c.showPage()
                page_number += 1
                add_header_footer(c, page_number)
                y_start = A4[1] - 70

            if i < len(data):
                contact = data[i]
                y = y_start
                y = self._draw_contact(c, contact, x_left, y)
                
            if i + 1 < len(data):
                contact = data[i+1]
                y = y_start
                y = self._draw_contact(c, contact, x_right, y)

            y_start = y

        c.save()

    def show_pdf(self, filename):
        try:
            if os.name == 'nt':
                os.startfile(filename)
            elif os.name == 'posix':
                if sys.platform == 'darwin':
                    subprocess.run(['open', filename])
                else:
                    subprocess.run(['xdg-open', filename])
        except Exception as e:
            print(f"Hiba a PDF megnyitásakor: {e}")

    def send_email(self, entry):
        email = entry.get().strip()
        if email:
            webbrowser.open(f"mailto:{email}")
        else:
            pass

    def check_duplicate_ids(self):
        id_counts = {}
        for contact in self.contacts:
            contact_id = contact.get('id')
            if contact_id in id_counts:
                id_counts[contact_id] += 1
            else:
                id_counts[contact_id] = 1

        duplicates = {id: count for id, count in id_counts.items() if count > 1}
        
        if duplicates:
            duplicate_ids = ", ".join(map(str, duplicates.keys()))
            CustomMessageBox(self.master, TEXTS.get("error_title", "Hiba"), TEXTS.get("error_duplicate_ids", "Duplikált ID-k találhatók: {duplicate_ids}").format(duplicate_ids=duplicate_ids), self.dark_mode)
        else:
            pass

    def generate_excel(self, data, filename):
        try:
            df_data = []
            for contact in data:
                contact_data = contact.copy()
                if 'photo' in contact_data:
                    contact_data['photo'] = "Fénykép elérhető" if contact_data['photo'] else "Nincs fénykép"
                df_data.append(contact_data)
            
            df = pd.DataFrame(df_data)
            df.to_excel(filename, index=False)
        except Exception as e:
            raise Exception(f"Excel fájl generálása sikertelen: {e}")

    def export_to_csv(self):
        db_base = os.path.splitext(self.current_database)[0]
        filename = f"{db_base}_teljes_lista.csv"
        try:
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(TEXTS.get("csv_headers", ["ID", "Név", "Becenév", "Telefonszám", "E-mail", "Cím", "Munkahely", "Munkahelyi E-mail", "Munkahelyi Telefon", "Megjegyzés", "Fénykép"]))
                
                for contact in self.contacts:
                    writer.writerow([
                        contact.get('id', ''),
                        contact.get('name', ''),
                        contact.get('nickname', ''),
                        contact.get('phone', ''),
                        contact.get('email', ''),
                        contact.get('address', ''),
                        contact.get('workplace', ''),
                        contact.get('work_email', ''),
                        contact.get('work_phone', ''),
                        contact.get('note', ''),
                        "Van" if 'photo' in contact and contact['photo'] else "Nincs"
                    ])
            
            CustomMessageBox(
                self.master, 
                TEXTS.get("info_title", "Info"), 
                TEXTS.get("info_csv_created", "A CSV fájl elkészült: {filename}").format(filename=filename), 
                self.dark_mode
            )
        except Exception as e:
            CustomMessageBox(
                self.master, 
                TEXTS.get("error_title", "Hiba"), 
                TEXTS.get("error_csv_open_failed", "Hiba történt a CSV fájl létrehozása során"), 
                self.dark_mode
            )

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=LIGHT_BG_COLOR)
    app = Cimnyilvantarto(root)
    root.mainloop()
