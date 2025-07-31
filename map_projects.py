# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import re 

# Comprehensive Greek Regions and Prefectures with coordinates
GREEK_PREFECTURES_COORDS = {
    # Ανατολική Μακεδονία - Θράκη
    'Έβρος': {'lat': 40.8477, 'lon': 25.8738, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Ξάνθη': {'lat': 41.1355, 'lon': 24.8882, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Ροδόπη': {'lat': 41.1179, 'lon': 25.4064, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Καβάλα': {'lat': 40.9396, 'lon': 24.4019, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    'Δράμα': {'lat': 41.1533, 'lon': 24.1428, 'region': 'Ανατολ. Μακεδονία - Θράκη', 'color': '#FF6B6B'},
    
    # Κεντρική Μακεδονία
    'Θεσσαλονίκη': {'lat': 40.6401, 'lon': 22.9444, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Ημαθία': {'lat': 40.5167, 'lon': 22.2, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Πέλλα': {'lat': 40.8, 'lon': 22.5, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Πιερία': {'lat': 40.3, 'lon': 22.6, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Σέρρες': {'lat': 41.0856, 'lon': 23.5469, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Κιλκίς': {'lat': 40.9939, 'lon': 22.8750, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Χαλκιδική': {'lat': 40.2, 'lon': 23.3, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},
    'Άγιον Όρος': {'lat': 40.16, 'lon': 24.28, 'region': 'Κεντρική Μακεδονία', 'color': '#4ECDC4'},

    # Δυτική Μακεδονία
    'Κοζάνη': {'lat': 40.30, 'lon': 21.78, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},
    'Γρεβενά': {'lat': 40.0833, 'lon': 21.4167, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},
    'Καστοριά': {'lat': 40.5167, 'lon': 21.2667, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},
    'Φλώρινα': {'lat': 40.7833, 'lon': 21.4167, 'region': 'Δυτική Μακεδονία', 'color': '#A569BD'},

    # Ήπειρος
    'Άρτα': {'lat': 39.1667, 'lon': 20.9833, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    'Θεσπρωτία': {'lat': 39.5, 'lon': 20.25, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    'Ιωάννινα': {'lat': 39.6667, 'lon': 20.85, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    'Πρέβεζα': {'lat': 39.0833, 'lon': 20.75, 'region': 'Ήπειρος', 'color': '#5DADE2'},
    
    # Αττική
    'Αττική': {'lat': 37.9838, 'lon': 23.7275, 'region': 'Αττική', 'color': '#45B7D1'},
    'Άγιο Όρος': {'lat': 40.2575, 'lon': 24.3258, 'region': 'Άγιο Όρος', 'color': '#D2B4DE'},
    'Νήσων (Αττική)': {'lat': 37.4, 'lon': 23.5, 'region': 'Αττική', 'color': '#45B7D1'},
    
    # Θεσσαλία
    'Θεσσαλία': {'lat': 39.6339, 'lon': 22.4194, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Λάρισα': {'lat': 39.6339, 'lon': 22.4194, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Μαγνησία': {'lat': 39.3681, 'lon': 22.9426, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Τρίκαλα': {'lat': 39.555, 'lon': 21.768, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    'Καρδίτσα': {'lat': 39.364, 'lon': 21.921, 'region': 'Θεσσαλία', 'color': '#96CEB4'},
    
    # Στερεά Ελλάδα
    'Στερεά Ελλάδα': {'lat': 38.5, 'lon': 22.5, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Εύβοια': {'lat': 38.5, 'lon': 24.0, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Βοιωτία': {'lat': 38.367, 'lon': 23.1, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Φθιώτιδα': {'lat': 38.9, 'lon': 22.4, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Φωκίδα': {'lat': 38.5, 'lon': 22.5, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    'Ευρυτανία': {'lat': 38.9, 'lon': 21.6, 'region': 'Στερεά Ελλάδα', 'color': '#FFEAA7'},
    
    # Δυτική Ελλάδα
    'Αχαΐα': {'lat': 38.2466, 'lon': 21.7346, 'region': 'Δυτική Ελλάδα', 'color': '#DDA0DD'},
    'Αιτωλοακαρνανία': {'lat': 38.6, 'lon': 21.4, 'region': 'Δυτική Ελλάδα', 'color': '#DDA0DD'},
    'Ηλεία': {'lat': 37.8, 'lon': 21.3, 'region': 'Δυτική Ελλάδα', 'color': '#DDA0DD'},
    
    # Πελοπόννησος
    'Πελοπόννησος': {'lat': 37.5, 'lon': 22.3, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Αργολίδα': {'lat': 37.5, 'lon': 22.8, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Αρκαδία': {'lat': 37.4, 'lon': 22.3, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Κορινθία': {'lat': 37.9, 'lon': 22.9, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Λακωνία': {'lat': 37.0, 'lon': 22.4, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    'Μεσσηνία': {'lat': 37.0, 'lon': 21.9, 'region': 'Πελοπόννησος', 'color': '#98D8C8'},
    
    # Ιόνια νησιά
    'Κέρκυρα': {'lat': 39.6243, 'lon': 19.9217, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Κεφαλληνία': {'lat': 38.1742, 'lon': 20.5275, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Ιθάκη': {'lat': 38.364, 'lon': 20.722, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Λευκάδα': {'lat': 38.8267, 'lon': 20.7033, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    'Ζάκυνθος': {'lat': 37.7833, 'lon': 20.9000, 'region': 'Ιόνια νησιά', 'color': '#F7DC6F'},
    
    # Νότιο Αιγαίο
    'Νότιο Αιγαίο': {'lat': 36.4, 'lon': 25.4, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κυκλάδες': {'lat': 37.0, 'lon': 25.0, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Δωδεκάνησα': {'lat': 36.4, 'lon': 27.2, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Νάξος': {'lat': 37.1036, 'lon': 25.3779, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Πάρος': {'lat': 37.084, 'lon': 25.148, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Θήρα': {'lat': 36.3932, 'lon': 25.4615, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Τήνος': {'lat': 37.5375, 'lon': 25.1618, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Ρόδος': {'lat': 36.434, 'lon': 28.217, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Άνδρος': {'lat': 37.8333, 'lon': 24.9333, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κάλυμνος': {'lat': 36.95, 'lon': 26.9833, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Μήλος': {'lat': 36.7467, 'lon': 24.4444, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κως': {'lat': 36.894, 'lon': 27.288, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κέα - Κύθνος': {'lat': 37.65, 'lon': 24.3333, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    'Κάρπαθος': {'lat': 35.507, 'lon': 27.213, 'region': 'Νότιο Αιγαίο', 'color': '#BB8FCE'},
    
    # Βόρειο Αιγαίο
    'Βόρειο Αιγαίο': {'lat': 39.1, 'lon': 26.0, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Λέσβος': {'lat': 39.1, 'lon': 26.5, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Κρήτη': {'lat': 35.2401, 'lon': 24.8093, 'region': 'Κρήτη', 'color': '#FAD7A0'},
    'Χίος': {'lat': 38.4, 'lon': 26.1, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Σάμος': {'lat': 37.7, 'lon': 26.8, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Λήμνος': {'lat': 39.9167, 'lon': 25.2500, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    'Ικαρία': {'lat': 37.6167, 'lon': 26.1500, 'region': 'Βόρειο Αιγαίο', 'color': '#85C1E9'},
    
    # Κρήτη
    'Κρήτη': {'lat': 35.3, 'lon': 24.8, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Ηράκλειο': {'lat': 35.3387, 'lon': 25.1442, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Χανιά': {'lat': 35.5, 'lon': 23.8, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Ρέθυμνο': {'lat': 35.4, 'lon': 24.5, 'region': 'Κρήτη', 'color': '#F8C471'},
    'Λασίθι': {'lat': 35.2, 'lon': 25.7, 'region': 'Κρήτη', 'color': '#F8C471'},
    
    # Ήπειρος
    'Ήπειρος': {'lat': 39.5, 'lon': 20.5, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Ιωάννινα': {'lat': 39.6650, 'lon': 20.8537, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Άρτα': {'lat': 39.16, 'lon': 20.98, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Πρέβεζα': {'lat': 38.96, 'lon': 20.75, 'region': 'Ήπειρος', 'color': '#82E0AA'},
    'Θεσπρωτία': {'lat': 39.5, 'lon': 20.2, 'region': 'Ήπειρος', 'color': '#82E0AA'},
}

# Comprehensive DEYA to Prefecture mapping - ΠΟΛΥ ΕΚΤΕΤΑΜΕΝΟ
DEYA_TO_PREFECTURE = {
    # Existing Entries...
    'ΔΕΥΑ ΑΒΔΗΡΩΝ': 'Ξάνθη', 'ΔΕΥΑ ΑΒΔΗΡΩΝ ': 'Ξάνθη',
    'ΔΕΥΑ ΑΛΕΞΑΝΔΡΟΥΠΟΛΗΣ': 'Έβρος', 'ΔΕΥΑ ΑΛΕΞΑΝΔΡΟΎΠΟΛΗΣ': 'Έβρος',
    'ΔΕΥΑ ΔΙΔΥΜΟΤΕΙΧΟΥ': 'Έβρος', 'ΔΕΥΑ ΟΡΕΣΤΙΑΔΑΣ': 'Έβρος',
    'ΔΕΥΑ ΞΑΝΘΗΣ': 'Ξάνθη', 'ΔΕΥΑ ΞΆΝΘΗΣ': 'Ξάνθη',
    'ΔΕΥΑ ΚΟΜΟΤΗΝΗΣ': 'Ροδόπη', 'ΔΕΥΑ ΚΟΜΟΤΉΝΗΣ': 'Ροδόπη',
    'ΔΕΥΑ ΚΑΒΑΛΑΣ': 'Καβάλα', 'ΔΕΥΑ ΚΑΒΆΛΑΣ': 'Καβάλα',
    'ΔΕΥΑ ΘΑΣΟΥ': 'Καβάλα', 'ΔΕΥΑ ΘΆΣΟΥ': 'Καβάλα',
    'ΔΕΥΑ ΠΑΓΓΑΙΟΥ': 'Καβάλα', 'ΔΕΥΑ ΠΑΓΓΑΊΟΥ': 'Καβάλα',
    'ΔΕΥΑ ΝΕΣΤΟΥ': 'Καβάλα', 'ΔΕΥΑ ΝΈΣΤΟΥ': 'Καβάλα', 'ΔΕΥΑ ΝΕΣΤΟΥ ': 'Καβάλα',
    'ΔΕΥΑ ΔΡΑΜΑΣ': 'Δράμα', 'ΔΕΥΑ ΔΡΆΜΑΣ': 'Δράμα',
    'Δήμος ΔΟΞΑΤΟΥ': 'Δράμα', 'Δήμος ΠΡΟΣΟΤΣΑΝΗΣ': 'Δράμα',
    'ΔΉΜΟΣ ΠΡΟΣΟΤΣΆΝΗΣ': 'Δράμα', 'Δήμος ΣΟΥΦΛΙΟΥ': 'Έβρος',
    'Δήμος ΙΑΣΜΟΥ': 'Ροδόπη', 'Δήμος ΜΑΡΩΝΕΙΑΣ - ΣΑΠΩΝ': 'Ροδόπη',
    'Δήμος ΚΑΤΩ ΝΕΥΡΟΚΟΠΙΟΥ': 'Δράμα', 'Δήμος ΠΑΡΑΝΕΣΤΙΟΥ': 'Δράμα',
    'Δήμος ΣΑΜΟΘΡΑΚΗΣ': 'Έβρος', 'Δήμος ΤΟΠΕΙΡΟΥ': 'Ξάνθη',
    'Δήμος ΜΥΚΗΣ': 'Ξάνθη', 'ΔΉΜΟΣ ΜΥΚΉΣ': 'Ξάνθη',
    'ΔΕΥΑ ΘΕΡΜΑΪΚΟΥ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΘΕΡΜΑΪΚΟΎ ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΒΕΡΟΙΑΣ': 'Ημαθία', 'ΔΕΥΑ ΒΈΡΟΙΑΣ': 'Ημαθία',
    'ΔΕΥΑ ΑΛΕΞΑΝΔΡΕΙΑΣ': 'Ημαθία', 'ΔΕΥΑ ΑΛΕΞΆΝΔΡΕΙΑΣ': 'Ημαθία',
    'ΔΕΥΑ Έδεσσας': 'Πέλλα', 'ΔΕΥΑ ΕΔΕΣΣΑΣ': 'Πέλλα',
    'ΔΕΥΑ ΑΛΜΩΠΙΑΣ': 'Πέλλα', 'ΔΕΥΑ ΑΛΜΩΠΊΑΣ': 'Πέλλα', 'ΔΕΥΑ ΑΛΜΩΠΙΑΣ ': 'Πέλλα',
    'ΔΕΥΑ ΔΙΟΥ-ΟΛΥΜΠΟΥ': 'Πιερία', 'ΔΕΥΑ ΔΊΟΥ-ΟΛΎΜΠΟΥ': 'Πιερία',
    'ΔΕΥΑ ΒΙΣΑΛΤΙΑΣ': 'Σέρρες', 'ΔΕΥΑ ΒΙΣΑΛΤΊΑΣ': 'Σέρρες',
    'ΔΕΥΑ ΗΡΑΚΛΕΙΑΣ': 'Σέρρες', 'ΔΕΥΑ ΗΡΑΚΛΕΊΑΣ': 'Σέρρες',
    'ΔΕΥΑ ΒΟΛΒΗΣ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΒΟΛΒΉΣ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΒΟΛΒΗΣ ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΔΗΜΟΥ ΔΕΛΤΑ': 'Θεσσαλονίκη', 'ΔΕΥΑ ΔΉΜΟΥ ΔΈΛΤΑ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΚΙΛΚΙΣ': 'Κιλκίς', 'ΔΕΥΑ ΚΙΛΚΊΣ': 'Κιλκίς',
    'ΕΥΔΑΠ': 'Αττική', 'Ε.Υ.Δ.Α.Π.': 'Αττική',
    'ΔΕΥΑ ΒΟΛΟΥ': 'Μαγνησία', 'ΔΕΥΑ ΒΌΛΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΛΑΡΙΣΑΣ': 'Λάρισα', 'ΔΕΥΑ ΛΆΡΙΣΑΣ': 'Λάρισα',
    'ΔΕΥΑ ΤΡΙΚΑΛΩΝ': 'Τρίκαλα', 'ΔΕΥΑ ΤΡΙΚΆΛΩΝ': 'Τρίκαλα',
    'ΔΕΥΑ ΚΑΡΔΙΤΣΑΣ': 'Καρδίτσα', 'ΔΕΥΑ ΚΑΡΔΊΤΣΑΣ': 'Καρδίτσα',
    'ΔΕΥΑ ΚΕΡΚΥΡΑΣ': 'Κέρκυρα', 'ΔΕΥΑ ΚΈΡΚΥΡΑΣ': 'Κέρκυρα',
    'ΔΕΥΑ ΚΕΦΑΛΛΗΝΙΑΣ': 'Κεφαλληνία', 'ΔΕΥΑ ΚΕΦΑΛΛΗΝΊΑΣ': 'Κεφαλληνία',
    'ΔΕΥΑ ΖΑΚΥΝΘΟΥ': 'Ζάκυνθος', 'ΔΕΥΑ ΖΑΚΎΝΘΟΥ': 'Ζάκυνθος',
    'ΔΕΥΑ ΛΕΥΚΑΔΟΣ': 'Λευκάδα', 'ΔΕΥΑ ΛΕΥΚΆΔΟΣ': 'Λευκάδα',
    'ΔΕΥΑ ΑΙΓΙΑΛΕΙΑΣ': 'Αχαΐα', 'ΔΕΥΑ ΑΙΓΙΑΛΕΊΑΣ': 'Αχαΐα',
    'ΔΕΥΑ ΠΑΤΡΑΣ': 'Αχαΐα', 'ΔΕΥΑ ΠΆΤΡΑΣ': 'Αχαΐα',
    'ΔΕΥΑ ΜΕΣΟΛΟΓΓΙΟΥ': 'Αιτωλοακαρνανία', 'ΔΕΥΑ ΜΕΣΟΛΟΓΓΊΟΥ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΠΥΡΓΟΥ': 'Ηλεία', 'ΔΕΥΑ ΠΎΡΓΟΥ': 'Ηλεία',
    'ΔΕΥΑ ΧΑΛΚΙΔΑΣ': 'Εύβοια', 'ΔΕΥΑ ΧΑΛΚΊΔΑΣ': 'Εύβοια',
    'ΔΕΥΑ ΛΙΒΑΔΕΙΑΣ': 'Βοιωτία', 'ΔΕΥΑ ΛΙΒΑΔΕΊΑΣ': 'Βοιωτία',
    'ΔΕΥΑ ΛΑΜΙΑΣ': 'Φθιώτιδα', 'ΔΕΥΑ ΛΑΜΊΑΣ': 'Φθιώτιδα',
    'ΔΕΥΑ ΗΡΑΚΛΕΙΟΥ': 'Ηράκλειο', 'ΔΕΥΑ ΗΡΑΚΛΕΊΟΥ': 'Ηράκλειο',
    'ΔΕΥΑ ΧΑΝΙΩΝ': 'Χανιά', 'ΔΕΥΑ ΧΑΝΊΩΝ': 'Χανιά',
    'ΔΕΥΑ ΡΕΘΥΜΝΟΥ': 'Ρέθυμνο', 'ΔΕΥΑ ΡΕΘΎΜΝΟΥ': 'Ρέθυμνο',
    'ΔΕΥΑ ΛΑΣΙΘΙΟΥ': 'Λασίθι', 'ΔΕΥΑ ΛΑΣΙΘΊΟΥ': 'Λασίθι',
    'ΔΕΥΑ ΙΩΑΝΝΙΝΩΝ': 'Ιωάννινα', 'ΔΕΥΑ ΙΩΑΝΝΊΝΩΝ': 'Ιωάννινα',
    'ΔΕΥΑ ΑΡΤΑΣ': 'Άρτα', 'ΔΕΥΑ ΆΡΤΑΣ': 'Άρτα',
    'ΔΕΥΑ ΠΡΕΒΕΖΑΣ': 'Πρέβεζα', 'ΔΕΥΑ ΠΡΈΒΕΖΑΣ': 'Πρέβεζα',
    'ΔΕΥΑ ΚΟΡΙΝΘΟΥ': 'Κορινθία', 'ΔΕΥΑ ΚΟΡΊΝΘΟΥ': 'Κορινθία',
    'ΔΕΥΑ ΑΡΓΟΛΙΔΑΣ': 'Αργολίδα', 'ΔΕΥΑ ΑΡΓΟΛΊΔΑΣ': 'Αργολίδα',
    'ΔΕΥΑ ΣΠΑΡΤΗΣ': 'Λακωνία', 'ΔΕΥΑ ΣΠΆΡΤΗΣ': 'Λακωνία',
    'ΔΕΥΑ ΚΑΛΑΜΑΤΑΣ': 'Μεσσηνία', 'ΔΕΥΑ ΚΑΛΑΜΆΤΑΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΤΡΙΠΟΛΗΣ': 'Αρκαδία', 'ΔΕΥΑ ΤΡΊΠΟΛΗΣ': 'Αρκαδία',
    'ΔΕΥΑ ΣΥΡΟΥ': 'Κυκλάδες', 'ΔΕΥΑ ΣΎΡΟΥ': 'Κυκλάδες',
    'ΔΕΥΑ ΜΥΚΟΝΟΥ': 'Κυκλάδες', 'ΔΕΥΑ ΜΥΚΌΝΟΥ': 'Κυκλάδες',
    'ΔΕΥΑ ΣΑΝΤΟΡΙΝΗΣ': 'Κυκλάδες', 'ΔΕΥΑ ΣΑΝΤΟΡΊΝΗΣ': 'Κυκλάδες',
    'ΔΕΥΑ ΡΟΔΟΥ': 'Δωδεκάνησα', 'ΔΕΥΑ ΡΌΔΟΥ': 'Δωδεκάνησα',
    'ΔΕΥΑ ΚΩ': 'Δωδεκάνησα', 'ΔΕΥΑ ΚΩΣ': 'Δωδεκάνησα',
    'ΔΕΥΑ ΜΥΤΙΛΗΝΗΣ': 'Λέσβος', 'ΔΕΥΑ ΜΥΤΙΛΉΝΗΣ': 'Λέσβος',
    'ΔΕΥΑ ΧΙΟΥ': 'Χίος', 'ΔΕΥΑ ΧΊΟΥ': 'Χίος',
    'ΔΕΥΑ ΣΑΜΟΥ': 'Σάμος', 'ΔΕΥΑ ΣΆΜΟΥ': 'Σάμος',
    'ΔΕΥΑ ΛΗΜΝΟΥ': 'Λήμνος', 'ΔΕΥΑ ΛΉΜΝΟΥ': 'Λήμνος',
    
    # --- ΝΕΕΣ ΠΡΟΣΘΗΚΕΣ ---
    'ΔΕΥΑ ΒΟΡΕΙΟΥ ΑΞΟΝΑ ΧΑΝΙΩΝ': 'Χανιά',
    'ΔΕΥΑ ΘΗΒΑΙΩΝ': 'Βοιωτία',
    'ΔΗΜΟΣ ΑΝΩΓΕΙΩΝ': 'Ρέθυμνο',
    'ΔΕΥΑ ΠΑΙΟΝΙΑΣ': 'Κιλκίς',
    'ΔΕΥΑ ΧΑΛΚΗΔΟΝΟΣ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΚΥΜΗΣ - ΑΛΙΒΕΡΙΟΥ': 'Εύβοια',
    'ΔΕΥΑ. ΔΙΟΥ ΟΛΥΜΠΟΥ': 'Πιερία',
    'ΔΗΜΟΣ ΛΗΜΝΟΥ': 'Λήμνος',
    'ΔΕΥΑ ΛΕΣΒΟΥ': 'Λέσβος',
    'ΔΕΥΑ ΣΕΡΡΩΝ': 'Σέρρες',
    'ΔΕΥΑ ΑΓΡΙΝΙΟΥ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΠΥΛΟΥ-ΝΕΣΤΟΡΟΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΔΕΛΦΩΝ': 'Φωκίδα',
    'ΔΗΜΟΣ ΑΜΟΡΓΟΥ': 'Νάξος',
    'ΔΕΥΑ ΜΑΛΕΒΙΖΙΟΥ': 'Ηράκλειο',
    'ΔΕΥΑ ΠΑΡΟΥ': 'Πάρος',
    'ΔΗΜΟΣ ΦΥΛΗΣ': 'Αττική',
    'ΔΕΥΑ ΜΕΤΕΩΡΩΝ': 'Τρίκαλα',
    'ΔΕΥΑ ΘΗΡΑΣ': 'Θήρα',
    'ΔΗΜΟΣ ΤΗΝΟΥ': 'Τήνος',
    'ΔΕΥΑ ΣΚΟΠΕΛΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΕΡΜΙΟΝΙΔΑΣ (ΚΡΑΝΙΔΙΟΥ)': 'Αργολίδα',
    'ΔΗΜΟΣ ΜΑΚΡΑΚΩΜΗΣ': 'Φθιώτιδα',
    'ΔΕΥΑ ΤΥΡΝΑΒΟΥ': 'Λάρισα',
    'ΔΕΥΑ ΚΕΦΑΛΟΝΙΑΣ': 'Κεφαλληνία',
    'ΔΗΜΟΣ ΝΑΞΟΥ ΚΑΙ ΜΙΚΡΩΝ ΚΥΚΛΑΔΩΝ': 'Νάξος',
    'ΔΗΜΟΣ ΜΟΝΕΜΒΑΣΙΑΣ': 'Λακωνία',
    'ΔΕΥΑ ΜΙΝΩΑ ΠΕΔΙΑΔΑΣ': 'Ηράκλειο',
    'ΔΕΥΑ ΠΑΤΡΕΩΝ': 'Αχαΐα',
    'ΔΗΜΟΣ ΑΡΙΣΤΟΤΕΛΗ': 'Χαλκιδική',
    'ΔΕΥΑ ΧΕΡΣΟΝΗΣΟΥ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΑΡΧΑΝΩΝ ΑΣΤΕΡΟΥΣΙΩΝ': 'Ηράκλειο',
    'ΔΕΥΑ ΑΡΓΟΥΣ - ΜΥΚΗΝΩΝ': 'Αργολίδα',
    'ΟΡΓΑΝΙΣΜΟΣ ΑΝΑΠΤΥΞΗΣ ΚΡΗΤΗΣ Α.Ε. (ΟΑΚ ΑΕ)': 'Κρήτη',
    'ΔΕΥΑ ΕΛΑΣΣΟΝΑΣ': 'Λάρισα',
    'ΔΗΜΟΣ ΑΜΥΝΤΑΙΟΥ': 'Φλώρινα',
    'ΔΕΥΑ ΠΑΛΑΜΑ': 'Καρδίτσα',
    'ΔΗΜΟΣ ΑΜΦΙΚΛΕΙΑΣ -ΕΛΑΤΕΙΑΣ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΑΜΦΙΛΟΧΙΑΣ': 'Αιτωλοακαρνανία',
    'ΔΗΜΟΣ ΑΡΓΟΥΣ ΟΡΕΣΤΙΚΟΥ': 'Καστοριά',
    'ΙΜ ΜΕΓΙΣΤΗΣ ΛΑΥΡΑΣ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΓΑΥΔΟΥ': 'Χανιά',
    'ΔΕΥΑ ΞΥΛΟΚΑΣΤΡΟΥ - ΕΥΡΩΣΤΙΝΗΣ': 'Κορινθία',
    'ΔΗΜΟΣ ΟΙΧΑΛΙΑΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΚΑΣΤΟΡΙΑΣ': 'Καστοριά',
    'ΔΕΥΑ ΒΟΪΟΥ': 'Κοζάνη',
    'ΔΗΜΟΣ ΣΕΡΒΙΩΝ': 'Κοζάνη',
    'ΔΗΜΟΣ ΛΙΜΝΗΣ ΠΛΑΣΤΗΡΑ': 'Καρδίτσα',
    'ΔΕΥΑ ΕΡΕΤΡΙΑΣ': 'Εύβοια',
    'ΔΕΥΑ ΝΑΥΠΛΙΕΩΝ': 'Αργολίδα',
    'ΔΗΜΟΣ ΔΥΤΙΚΗΣ ΜΑΝΗΣ': 'Μεσσηνία',
    'ΔΕΥΑ ΒΟΡΕΙΑΣ ΚΥΝΟΥΡΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΕΜΜΑΝΟΥΗΛ ΠΑΠΠΑ': 'Σέρρες',
    'ΔΗΜΟΣ ΔΩΔΩΝΗΣ': 'Ιωάννινα',
    'ΙΜ ΣΙΜΩΝΟΣ ΠΕΤΡΑΣ': 'Άγιον Όρος',
    'ΙΜ ΞΕΝΟΦΩΝΤΟΣ': 'Άγιον Όρος',
    'ΔΕΥΑ. ΠΕΛΛΑΣ': 'Πέλλα',
    'ΔΗΜΟΣ ΛΕΥΚΑΔΑΣ': 'Λευκάδα',
    'ΔΗΜΟΣ ΠΡΕΒΕΖΗΣ': 'Πρέβεζα',
    'ΔΗΜΟΣ ΠΑΡΓΑΣ': 'Πρέβεζα',
    'ΔΗΜΟΣ ΜΕΤΣΟΒΟΥ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΞΗΡΟΜΕΡΟΥ': 'Αιτωλοακαρνανία',
    'ΔΗΜΟΣ ΔΩΡΙΔΟΣ': 'Φωκίδα',
    'ΔΗΜΟΣ ΓΟΡΤΥΝΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΙΕΡΑΠΕΤΡΑΣ': 'Λασίθι',
    'ΔΗΜΟΣ ΛΟΚΡΩΝ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΔΙΣΤΟΜΟΥ - ΑΡΑΧΟΒΑΣ - ΑΝΤΙΚΥΡΑΣ': 'Βοιωτία',
    'ΔΗΜΟΣ ΚΑΡΥΣΤΟΥ': 'Εύβοια',
    'ΔΗΜΟΣ ΤΡΟΙΖΗΝΙΑΣ ΜΕΘΑΝΩΝ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΦΙΛΙΑΤΩΝ': 'Θεσπρωτία',
    'ΔΕΥΑ ΦΑΡΣΑΛΩΝ': 'Λάρισα',
    'ΔΕΥΑ ΑΡΧΑΙΑΣ ΟΛΥΜΠΙΑΣ': 'Ηλεία',
    'ΔΗΜΟΣ ΖΙΤΣΑΣ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΣΕΡΙΦΟΥ': 'Μήλος',
    'ΔΗΜΟΣ ΑΓΙΟΥ ΕΥΣΤΡΑΤΙΟΥ': 'Λήμνος',
    'ΔΗΜΟΣ ΜΕΓΑΛΟΠΟΛΗΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΤΗΛΟΥ': 'Ρόδος',
    'ΔΗΜΟΣ ΠΡΕΣΠΩΝ': 'Φλώρινα',
    'ΔΗΜΟΣ ΑΚΤΙΟΥ - ΒΟΝΙΤΣΑΣ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΝΑΥΠΑΚΤΙΑΣ': 'Αιτωλοακαρνανία',
    'ΔΕΥΑ ΧΑΛΚΙΔΕΩΝ': 'Εύβοια',
    'ΔΕΥΑ ΛΟΥΤΡΑΚΙΟΥ - ΠΕΡΑΧΩΡΑΣ': 'Κορινθία',
    'ΔΕΥΑ ΣΙΚΥΩΝΙΩΝ': 'Κορινθία',
    'ΔΗΜΟΣ ΑΓΡΑΦΩΝ': 'Ευρυτανία',
    'ΔΗΜΟΣ ΣΤΥΛΙΔΑΣ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΑΝΔΡΟΥ': 'Άνδρος',
    'ΔΗΜΟΣ ΕΥΡΩΤΑ': 'Λακωνία',
    'ΔΗΜΟΣ ΑΣΤΥΠΑΛΑΙΑΣ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΑΛΙΑΡΤΟΥ ΘΕΣΠΕΩΝ': 'Βοιωτία',
    'ΔΕΥΑ ΣΚΥΔΡΑΣ': 'Πέλλα',
    'ΔΕΥΑ ΘΕΡΜΗΣ': 'Θεσσαλονίκη',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΛΕΚΑΝΟΠΕΔΙΟΥ ΙΩΑΝΝΙΝΩΝ': 'Ιωάννινα',
    'ΔΕΥΑ ΡΗΓΑ ΦΕΡΑΙΟΥ': 'Μαγνησία',
    'ΔΗΜΟΣ ΣΟΥΛΙΟΥ': 'Θεσπρωτία',
    'ΔΗΜΟΣ ΑΛΟΝΝΗΣΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΠΥΛΗΣ ΤΡΙΚΑΛΩΝ': 'Τρίκαλα',
    'ΔΕΥΑ ΣΚΙΑΘΟΥ': 'Μαγνησία',
    'ΔΗΜΟΣ ΒΟΡΕΙΩΝ ΤΖΟΥΜΕΡΚΩΝ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΚΟΝΙΤΣΑΣ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΠΩΓΩΝΙΟΥ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΑΜΑΡΙΟΥ': 'Ρέθυμνο',
    'ΔΗΜΟΣ ΒΕΛΟΥ ΒΟΧΑΣ': 'Κορινθία',
    'ΔΕΥΑ ΗΓΟΥΜΕΝΙΤΣΑΣ': 'Θεσπρωτία',
    'ΔΗΜΟΣ ΚΕΝΤΡΙΚΩΝ ΤΖΟΥΜΕΡΚΩΝ': 'Άρτα',
    'ΔΗΜΟΣ ΠΑΞΩΝ': 'Κέρκυρα',
    'ΔΕΥΑ ΜΥΛΟΠΟΤΑΜΟΥ': 'Ρέθυμνο',
    'ΔΕΥΑ ΣΕΛΙΝΟΥ': 'Χανιά',
    'ΔΗΜΟΣ ΓΟΡΤΥΝΑΣ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΜΕΓΑΡΕΩΝ': 'Αττική',
    'ΔΕΥΑ ΣΥΜΗΣ': 'Ρόδος',
    'ΔΗΜΟΣ ΟΡΧΟΜΕΝΟΥ': 'Βοιωτία',
    'ΔΗΜΟΣ ΚΑΛΑΒΡΥΤΩΝ': 'Αχαΐα',
    'ΙΜ ΔΟΧΕΙΑΡΙΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΠΥΛΑΙΑΣ - ΧΟΡΤΙΑΤΗ': 'Θεσσαλονίκη',
    'ΙΜ ΓΡΗΓΟΡΙΟΥ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΝΕΑΣ ΠΡΟΠΟΝΤΙΔΑΣ': 'Χαλκιδική',
    'ΔΕΥΑ ΑΡΤΑΙΩΝ': 'Άρτα',
    'ΔΗΜΟΣ ΖΗΡΟΥ': 'Πρέβεζα',
    'ΔΗΜΟΣ ΚΑΜΕΝΩΝ ΒΟΥΡΛΩΝ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΔΟΜΟΚΟΥ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΠΗΝΕΙΟΥ': 'Ηλεία',
    'ΔΗΜΟΣ ΚΥΘΗΡΩΝ': 'Νήσων (Αττική)',
    'ΔΕΥΑ ΣΗΤΕΙΑΣ ΛΑΣΙΘΙΟΥ': 'Λασίθι',
    'ΔΗΜΟΣ ΧΑΛΚΗΣ': 'Ρόδος',
    'ΔΕΥΑ ΛΑΥΡΕΩΤΙΚΗΣ': 'Αττική',
    'ΔΗΜΟΣ ΡΑΦΗΝΑΣ - ΠΙΚΕΡΜΙΟΥ': 'Αττική',
    'ΔΕΥΑ ΜΕΣΣΗΝΗΣ': 'Μεσσηνία',
    'ΔΗΜΟΣ ΠΟΡΟΥ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΗΡΩΙΚΗΣ Ν. ΨΑΡΩΝ': 'Χίος',
    'ΔΗΜΟΣ ΔΥΤΙΚΗΣ ΣΑΜΟΥ': 'Σάμος',
    'ΔΕΥΑ ΤΡΙΦΥΛΙΑΣ': 'Μεσσηνία',
    'ΔΗΜΟΣ ΝΟΤΙΑΣ ΚΥΝΟΥΡΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΠΟΛΥΓΥΡΟΥ': 'Χαλκιδική',
    'ΔΗΜΟΣ ΖΑΓΟΡΙΟΥ': 'Ιωάννινα',
    'ΔΗΜΟΣ ΖΑΓΟΡΑΣ - ΜΟΥΡΕΣΙΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΖΑΧΑΡΩΣ': 'Ηλεία',
    'ΔΕΥΑ ΦΛΩΡΙΝΑΣ': 'Φλώρινα',
    'ΔΗΜΟΣ ΝΕΣΤΟΡΙΟΥ': 'Καστοριά',
    'ΔΕΥΑ ΓΡΕΒΕΝΩΝ': 'Γρεβενά',
    'ΙΜ ΙΒΗΡΩΝ': 'Άγιον Όρος',
    'ΙΜ ΞΗΡΟΠΟΤΑΜΟΥ': 'Άγιον Όρος',
    'ΙΜ ΠΑΝΤΟΚΡΑΤΟΡΟΣ': 'Άγιον Όρος',
    'ΙΜ ΖΩΓΡΑΦΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΛΑΓΚΑΔΑ': 'Θεσσαλονίκη',
    'ΔΗΜΟΣ ΤΑΝΑΓΡΑΣ': 'Βοιωτία',
    'ΔΗΜΟΣ ΝΙΚΟΛΑΟΥ ΣΚΟΥΦΑ': 'Άρτα',
    'ΔΕΥΑ ΦΑΡΚΑΔΟΝΑΣ': 'Τρίκαλα',
    'ΔΕΥΑ ΑΛΜΥΡΟΥ': 'Μαγνησία',
    'ΔΗΜΟΣ ΔΙΟΝΥΣΟΥ': 'Αττική',
    'ΔΕΥΑ.ΝΑΟΥΣΑΣ': 'Ημαθία',
    'ΔΗΜΟΣ ΓΕΩΡΓΙΟΥ ΚΑΡΑΪΣΚΑΚΗ': 'Άρτα',
    'ΙΜ ΚΟΥΤΛΟΥΜΟΥΣΙΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΩΡΑΙΟΚΑΣΤΡΟΥ': 'Θεσσαλονίκη',
    'ΙΜ ΕΣΦΙΓΜΕΝΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΔΥΜΑΙΩΝ': 'Αχαΐα',
    'ΔΕΥΑ ΑΓΙΑΣ': 'Λάρισα',
    'ΔΗΜΟΣ ΙΘΑΚΗΣ': 'Ιθάκη',
    'ΙΜ ΣΤΑΥΡΟΝΙΚΗΤΑ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΒΕΛΒΕΝΤΟΥ': 'Κοζάνη',
    'ΔΕΥΑ ΣΟΦΑΔΩΝ': 'Καρδίτσα',
    'ΔΗΜΟΣ ΚΕΑΣ': 'Κέα - Κύθνος',
    'ΔΗΜΟΣ ΚΙΣΣΑΜΟΥ': 'Χανιά',
    'ΔΗΜΟΣ ΑΠΟΚΟΡΩΝΟΥ': 'Χανιά',
    'ΔΗΜΟΣ ΣΠΑΤΩΝ ΑΡΤΕΜΙΔΟΣ': 'Αττική',
    'ΔΗΜΟΣ ΝΙΣΥΡΟΥ': 'Κως',
    'ΔΕΥΑ ΚΑΛΥΜΝΟΥ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΙΣΤΙΑΙΑΣ - ΑΙΔΗΨΟΥ': 'Εύβοια',
    'ΔΗΜΟΣ ΜΑΝΔΡΑΣ-ΕΙΔΥΛΛΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΑΙΓΙΝΑΣ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΛΕΡΟΥ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΣΠΕΤΣΩΝ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΑΓΚΙΣΤΡΙΟΥ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΣΚΥΡΟΥ': 'Εύβοια',
    'ΔΗΜΟΣ ΕΡΥΜΑΝΘΟΥ': 'Αχαΐα',
    'ΔΗΜΟΣ ΚΥΘΝΟΥ': 'Κέα - Κύθνος',
    'ΔΗΜΟΣ ΗΡΩΪΚΗΣ ΝΗΣΟΥ ΚΑΣΟΥ': 'Κάρπαθος',
    'ΔΕΥΑ ΔΕΣΚΑΤΗΣ': 'Γρεβενά',
    'ΙΜ ΦΙΛΟΘΕΟΥ': 'Άγιον Όρος',
    'ΙΜ ΧΙΛΑΝΔΑΡΙΟΥ': 'Άγιον Όρος',
    'ΔΗΜΟΣ ΠΥΔΝΑΣ-ΚΟΛΙΝΔΡΟΥ': 'Πιερία',
    'ΔΕΥΑ ΦΑΙΣΤΟΥ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΦΟΛΕΓΑΝΔΡΟΥ': 'Θήρα',
    'ΔΗΜΟΣ ΜΗΛΟΥ': 'Μήλος',
    'ΔΗΜΟΣ ΣΙΚΙΝΟΥ': 'Θήρα',
    'ΔΗΜΟΣ ΟΙΝΟΥΣΣΩΝ': 'Χίος',
    'ΔΕΥΑ ΑΝΑΤΟΛΙΚΗΣ ΜΑΝΗΣ': 'Λακωνία',
    'ΔΗΜΟΣ ΚΡΩΠΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΣΑΡΩΝΙΚΟΥ': 'Αττική',
    'ΔΕΥΑ ΠΕΛΛΑΣ': 'Πέλλα',
    'ΔΗΜΟΣ ΑΜΦΙΠΟΛΗΣ': 'Σέρρες',
    'ΔΗΜΟΣ ΣΙΘΩΝΙΑΣ': 'Χαλκιδική',
    'ΔΗΜΟΣ ΚΑΣΣΑΝΔΡΑΣ': 'Χαλκιδική',
    'ΙΜ ΒΑΤΟΠΑΙΔΙΟΥ': 'Άγιον Όρος',
    'ΔΕΥΑ ΝΑΟΥΣΑΣ': 'Ημαθία',
    'ΔΗΜΟΣ ΘΕΡΜΟΥ': 'Αιτωλοακαρνανία',
    'ΔΗΜΟΣ ΗΛΙΔΑΣ': 'Ηλεία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΚΑΡΔΙΤΣΑΣ ΚΑΙ ΛΟΙΠΩΝ ΔΗΜΩΝ': 'Καρδίτσα',
    'ΔΗΜΟΣ ΑΡΓΙΘΕΑΣ': 'Καρδίτσα',
    'ΔΕΥΑ ΣΙΝΤΙΚΗΣ': 'Σέρρες',
    'ΔΗΜΟΣ ΔΙΟΥ-ΟΛΥΜΠΟΥ': 'Πιερία',
    'ΔΗΜΟΣ ΜΑΡΚΟΠΟΥΛΟΥ ΜΕΣΟΓΑΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΚΗΦΙΣΙΑΣ': 'Αττική',
    'ΔΕΥΑ ΜΑΝΤΟΥΔΙΟΥ-ΛΙΜΝΗΣ-ΑΓΙΑΣ ΑΝΝΑΣ': 'Εύβοια',
    'ΔΙΑΒΑΘΜΙΔΙΚΟΣ ΣΥΝΔΕΣΜΟΣ ΗΛΕΙΑΣ ΤΗΣ ΠΕΡΙΦΕΡΕΙΑΣ ΔΥΤΙΚΗΣ ΕΛΛΑΔΑΣ': 'Ηλεία',
    'ΔΗΜΟΣ ΚΑΡΠΕΝΗΣΙΟΥ': 'Ευρυτανία',
    'ΔΗΜΟΣ ΑΝΔΡΑΒΙΔΑΣ - ΚΥΛΛΗΝΗΣ': 'Ηλεία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ Ο.Τ.Α. Ν. ΦΘΙΩΤΙΔΑΣ': 'Φθιώτιδα',
    'ΔΗΜΟΣ ΠΑΙΑΝΙΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΣΑΛΑΜΙΝΑΣ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΥΔΡΑΣ': 'Νήσων (Αττική)',
    'ΔΗΜΟΣ ΩΡΩΠΙΩΝ': 'Αττική',
    'ΔΗΜΟΣ ΒΡΙΛΗΣΣΙΩΝ': 'Αττική',
    'ΔΗΜΟΣ ΚΑΡΠΑΘΟΥ': 'Κάρπαθος',
    'ΔΗΜΟΣ ΑΓΑΘΟΝΗΣΙΟΥ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΑΝΑΦΗΣ': 'Θήρα',
    'ΔΗΜΟΣ ΕΛΑΦΟΝΗΣΟΥ': 'Λακωνία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΔΗΜΩΝ ΚΑΛΑΜΑΤΑΣ - ΜΕΣΣΗΝΗΣ': 'Μεσσηνία',
    'ΔΗΜΟΣ ΛΕΙΨΩΝ': 'Κάλυμνος',
    'ΔΗΜΟΣ ΚΙΜΩΛΟΥ': 'Μήλος',
    'ΔΗΜΟΣ ΑΝΤΙΠΑΡΟΥ': 'Πάρος',
    'ΔΗΜΟΣ ΣΙΦΝΟΥ': 'Μήλος',
    'ΠΕΡΙΦΕΡΕΙΑ ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ': 'Νότιο Αιγαίο',
    'ΔΗΜΟΣΙΗΤΩΝ': 'Θήρα', 
    'ΔΗΜΟΣ ΟΡΟΠΕΔΙΟΥ ΛΑΣΙΘΙΟΥ': 'Λασίθι',
    'ΔΗΜΟΣ ΣΦΑΚΙΩΝ': 'Χανιά',

    # Corrections for unmapped items
    'ΔΕΥΑ ΚΙΛΕΛΕΡ': 'Λάρισα',
    'ΔΗΜΟΣ ΝΟΤΙΟΥ ΠΗΛΙΟΥ': 'Μαγνησία',
    'ΔΕΥΑ ΒΟΡΕΙΟΥ ΑΞΟΝΑ ΧΑΝΙΩΝ': 'Χανιά',

    # New batch of unmapped items from user
    'ΙΜ ΑΓΙΟΥ ΠΑΥΛΟΥ': 'Άγιο Όρος',
    'ΔΕΥΑ ΚΟΖΑΝΗΣ': 'Κοζάνη',
    'ΕΥΑΘ': 'Θεσσαλονίκη',
    'ΔΕΥΑ ΜΟΥΖΑΚΙΟΥ': 'Καρδίτσα',
    'ΔΕΥΑ ΑΓΙΟΥ ΝΙΚΟΛΑΟΥ': 'Λασίθι',
    'ΔΗΜΟΣ ΙΚΑΡΙΑΣ': 'Σάμος',
    'ΔΗΜΟΣ ΑΓΙΟΥ ΒΑΣΙΛΕΙΟΥ': 'Ρέθυμνο',
    'ΔΗΜΟΣ ΒΙΑΝΝΟΥ': 'Ηράκλειο',
    'ΔΗΜΟΣ ΝΕΑΣ ΖΙΧΝΗΣ': 'Σέρρες',
    'ΔΕΥΑ ΚΑΤΕΡΙΝΗΣ': 'Πιερία',
    'ΔΕΥΑ ΖΑΚΥΝΘΙΩΝ': 'Ζάκυνθος',
    'ΔΕΥΑ ΤΕΜΠΩΝ': 'Λάρισα',
    'ΔΕΥΑ ΕΟΡΔΑΙΑΣ': 'Κοζάνη',
    'ΔΗΜΟΣ ΑΝΑΤΟΛΙΚΗΣ ΣΑΜΟΥ': 'Σάμος',
    'ΔΗΜΟΣ ΜΑΡΑΘΩΝΟΣ': 'Αττική',
    'ΔΕΥΑ ΕΠΙΔΑΥΡΟΥ': 'Αργολίδα',
    'ΔΗΜΟΣ ΦΟΥΡΝΩΝ ΚΟΡΣΕΩΝ': 'Σάμος',
    'ΔΗΜΟΣ ΑΜΥΝΤΑΙΟΥ': 'Φλώρινα',
    'ΔΕΥΑ ΒΟΡΕΙΑΣ ΚΥΝΟΥΡΙΑΣ': 'Αρκαδία',
    'ΔΗΜΟΣ ΗΛΙΔΑΣ': 'Ηλεία',
    'ΔΗΜΟΣ ΣΑΛΑΜΙΝΑΣ': 'Αττική',
    'ΔΗΜΟΣ ΘΕΡΜΟΥ': 'Αιτωλοακαρνανία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ ΔΗΜΩΝ ΚΑΛΑΜΑΤΑΣ - ΜΕΣΣΗΝΗΣ & ΚΟΙΝΟΤΗΤΩΝ ΠΕΡΙΟΧΗΣ ΚΑΛΑΜΑΤΑΣ': 'Μεσσηνία',
    'ΣΥΝΔΕΣΜΟΣ ΥΔΡΕΥΣΗΣ Ο.Τ.Α. Ν. ΦΘΙΩΤΙΔΑΣ ΑΠΟ ΠΗΓΕΣ "ΚΑΝΑΛΙΑ" ΠΥΡΓΟΥ ΥΠΑΤΗΣ': 'Φθιώτιδα',
    'ΟΤΑ Β\' ΒΑΘΜΟΥ ΠΕΡΙΦΕΡΕΙΑ ΝΟΤΙΟΥ ΑΙΓΑΙΟΥ': 'Νότιο Αιγαίο'
}

def normalize_greek(text):
    """
    Normalizes a Greek string by converting to uppercase, removing accents,
    and stripping extra whitespace and punctuation.
    """
    if not isinstance(text, str):
        return ''
        
    text = text.upper().strip()
    
    # Define accent mappings
    replacements = {
        'Ά': 'Α', 'Έ': 'Ε', 'Ή': 'Η', 'Ί': 'Ι', 'Ό': 'Ο', 'Ύ': 'Υ', 'Ώ': 'Ω',
        'Ϊ': 'Ι', 'Ϋ': 'Υ'
    }
    
    for accented, unaccented in replacements.items():
        text = text.replace(accented, unaccented)
        
    # Remove common punctuation and collapse whitespace
    text = re.sub(r'[\.\(\)-]', ' ', text) # Replace punctuation with a space
    text = re.sub(r'\s+', ' ', text).strip() # Collapse multiple spaces to one and strip again
    
    return text

@st.cache_data(ttl=3600, show_spinner="Analyzing Excel file...")
def load_and_analyze_excel_enhanced(excel_file):
    """Enhanced loading with comprehensive data analysis."""
    try:
        df = pd.read_excel(excel_file, sheet_name=0)
        


        st.write(f"📊 Φορτώθηκαν **{len(df):,}** γραμμές με **{len(df.columns)}** στήλες")
        
        # Find project number column
        project_number_col = None
        for col_name in ['Α/Α', 'ΑΑ', 'A/A', 'AA', 'Project_ID', 'ID', 'Αρ.']:
            if col_name in df.columns:
                project_number_col = col_name
                break
        
        if project_number_col is None:
            df.insert(0, 'Α/Α', range(1, len(df) + 1))
            project_number_col = 'Α/Α'
        
        # Clean data
        df = df.dropna(how='all')
        if project_number_col in df.columns:
            df = df.dropna(subset=[project_number_col])
        
        # Clean string columns
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(['nan', 'None', '', 'NaN'], pd.NA)
        
        # Find water utility column
        water_utility_col = None
        for col_name in ['Φορέας Ύδρευσης', 'ΔΕΥΑ', 'Φορέας', 'Water_Utility']:
            if col_name in df.columns:
                water_utility_col = col_name
                break
        
        if water_utility_col is None:
            df['Φορέας Ύδρευσης'] = 'Άγνωστος'
            water_utility_col = 'Φορέας Ύδρευσης'
        
        # Add prefecture mapping with debugging
        # Add prefecture mapping using the normalization function for robust matching
    
        # 1. Create a new column in your DataFrame with the normalized utility names
        df['normalized_utility'] = df[water_utility_col].apply(normalize_greek)
        
        # 2. Create a new, normalized dictionary for mapping
        normalized_map = {normalize_greek(k): v for k, v in DEYA_TO_PREFECTURE.items()}
        
        # 3. Perform the mapping using the normalized values
        df['Νομός'] = df['normalized_utility'].map(normalized_map)
        
        # Debug: Show unmapped DEYAs
        unmapped_deyas = df[df['Νομός'].isna()][water_utility_col].value_counts()
        if not unmapped_deyas.empty:
            st.warning("⚠️ ΔΕΥΑ/Δήμοι που δεν αντιστοιχίστηκαν σε νομούς:")
            for deya, count in unmapped_deyas.items():
                st.write(f"• **{deya}**: {count} έργα")
            
            # Try fuzzy matching for unmapped DEYAs
            st.info("💡 Προσπαθώ αυτόματη αντιστοίχιση...")
            
            additional_mappings = {}
            for unmapped_deya in unmapped_deyas.index:
                # Simple fuzzy matching logic
                deya_clean = unmapped_deya.upper().strip()
                
                # Check if it contains known city names
                city_mappings = {
                    'ΘΕΣΣΑΛΟΝΙΚ': 'Θεσσαλονίκη', 'ΑΘΗΝ': 'Αττική', 'ΠΑΤΡ': 'Αχαΐα',
                    'ΒΟΛΟΣ': 'Μαγνησία', 'ΛΑΡΙΣ': 'Λάρισα', 'ΙΩΑΝΝΙΝ': 'Ιωάννινα',
                    'ΗΡΑΚΛΕΙ': 'Ηράκλειο', 'ΧΑΝΙ': 'Χανιά', 'ΚΑΒΑΛ': 'Καβάλα',
                    'ΔΡΑΜ': 'Δράμα', 'ΚΟΜΟΤΙΝ': 'Ροδόπη', 'ΞΑΝΘ': 'Ξάνθη',
                    'ΑΛΕΞΑΝΔΡΟΥΠΟΛ': 'Έβρος', 'ΣΕΡΡ': 'Σέρρες', 'ΚΕΡΚΥΡ': 'Κέρκυρα'
                }
                
                for city_part, prefecture in city_mappings.items():
                    if city_part in deya_clean:
                        additional_mappings[unmapped_deya] = prefecture
                        break
            
            # Apply additional mappings
            if additional_mappings:
                st.success(f"✅ Αυτόματη αντιστοίχιση {len(additional_mappings)} ΔΕΥΑ:")
                for deya, prefecture in additional_mappings.items():
                    st.write(f"• **{deya}** → {prefecture}")
                
                # Update the dataframe
                for deya, prefecture in additional_mappings.items():
                    df.loc[df[water_utility_col] == deya, 'Νομός'] = prefecture
        
        # Fill remaining unmapped as 'Άλλος'
        df['Νομός'] = df['Νομός'].fillna('Άλλος')
        
        # Find or create region column
        region_col = None
        for col_name in ['Περιφέρεια', 'Region', 'Περιοχή']:
            if col_name in df.columns:
                region_col = col_name
                break
        
        if region_col is None:
            # Create region mapping from prefectures
            df['Περιφέρεια'] = df['Νομός'].map(
                lambda x: GREEK_PREFECTURES_COORDS.get(x, {}).get('region', 'Άλλη')
            )
            region_col = 'Περιφέρεια'
        
        # Convert numeric columns
        potential_numeric_cols = []
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in 
                  ['προϋπολογισμός', 'budget', 'κόστος', 'cost', 'πληθυσμός', 'population', 'χρόνος', 'time', 'μήνες', 'months']):
                potential_numeric_cols.append(col)

        # Force convert budget column specifically
        budget_column_I = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
        if budget_column_I in df.columns:
            # Clean the budget column - remove any non-numeric characters except decimal points
            df[budget_column_I] = df[budget_column_I].astype(str).str.replace(',', '').str.replace('€', '').str.replace(' ', '')
            df[budget_column_I] = pd.to_numeric(df[budget_column_I], errors='coerce')


        for col in potential_numeric_cols:
            if col in df.columns and col != budget_column_I:  # Don't double-convert
                df[col] = pd.to_numeric(df[col], errors='coerce')


        
        # Add project type column
        project_type_cols = ['Είδος Έργου', 'Project_Type', 'Type', 'Τύπος']
        for col_name in project_type_cols:
            if col_name in df.columns:
                df['Κατηγορία Έργου'] = df[col_name].fillna('Άλλο')
                break
        else:
            df['Κατηγορία Έργου'] = 'Άλλο'
        
        st.success(f"✅ Επεξεργασία ολοκληρώθηκε! Έργα: **{len(df):,}**")
        
        return df
        
    except Exception as e:
        st.error(f"❌ Σφάλμα φόρτωσης: {e}")
        return None

def create_interactive_map_by_prefecture(df):
    """Create interactive map showing projects by prefecture (νομός)."""
    center_lat, center_lon = 39.0, 22.0
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=6, 
        tiles='OpenStreetMap'
    )
    
    # Group by prefecture
    if 'Νομός' in df.columns:
        # Ensure required columns exist for aggregation
        agg_dict = {'Α/Α': 'count', 'Φορέας Ύδρευσης': 'nunique'}
        
        # Add column I budget specifically - CHECK IF IT EXISTS FIRST
        budget_column_I = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
        budget_cols = [col for col in df.columns if 'προϋπολογισμός' in str(col).lower()]
        if budget_column_I in df.columns:
            # Check if the column has numeric data
            numeric_budget_data = df[budget_column_I].dropna()
            if len(numeric_budget_data) > 0:
                agg_dict[budget_column_I] = ['sum', 'mean', 'count']
                st.write(f"✅ Adding {budget_column_I} to aggregation. Sample values: {numeric_budget_data.head().tolist()}")
            else:
                st.warning(f"⚠️ {budget_column_I} has no numeric data!")
        else:
            st.error(f"❌ {budget_column_I} not found in DataFrame!")
            # Try to find similar columns
            budget_cols = [col for col in df.columns if 'προϋπολογισμός' in str(col).lower()]
            st.write(f"Available budget columns: {budget_cols}")
            if budget_cols:
                budget_column_I = budget_cols[0]  # Use the first available budget column
                agg_dict[budget_column_I] = ['sum', 'mean', 'count']
                st.info(f"Using alternative budget column: {budget_column_I}")

        prefecture_data = df.groupby('Νομός').agg(agg_dict).round(0)
        
        # Flatten column names
        new_cols = {}
        new_cols['Α/Α_count'] = 'Έργα'
        new_cols['Φορέας Ύδρευσης_nunique'] = 'ΔΕΥΑ_Count'
        
        # Add column I budget columns
        if budget_column_I in df.columns:
            new_cols[f'{budget_column_I}_sum'] = 'Συνολικός_Προϋπ_Ι'
            new_cols[f'{budget_column_I}_mean'] = 'Μέσος_Προϋπ_Ι'
            new_cols[f'{budget_column_I}_count'] = 'Έργα_με_Προϋπ_Ι'
        
        for col in budget_cols:
            if col != budget_column_I:
                new_cols[f'{col}_sum'] = f'{col}_sum'
                new_cols[f'{col}_mean'] = f'{col}_mean'
                
        prefecture_data.columns = ['_'.join(col).strip() for col in prefecture_data.columns.values]
        prefecture_data = prefecture_data.rename(columns=new_cols)

        for prefecture, data in prefecture_data.iterrows():
            if prefecture in GREEK_PREFECTURES_COORDS and data['Έργα'] > 0:
                coords = GREEK_PREFECTURES_COORDS[prefecture]
                
                # --- Pre-calculate financial data for use in multiple sections ---
                # Correctly reference the renamed budget column
                budget_sum_col_name = 'Συνολικός_Προϋπ_Ι'
                if budget_sum_col_name in data.index:
                    total_budget = data[budget_sum_col_name]
                else:
                    total_budget = 0

                # 1. Header Section
                popup_parts = [
                    f'<div style="font-family: Arial; min-width: 400px; max-width: 500px; padding: 20px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">',
                    f'<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">',
                    f'<h3 style="margin: 0; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 8px; display: flex; align-items: center;">',
                    f'<span style="font-size: 24px; margin-right: 10px;">🏛️</span>',
                    f'{prefecture}',
                    f'<span style="background: #3498db; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; margin-left: auto;">{coords["region"]}</span>',
                    f'</h3>',
                    f'<div style="display: flex; justify-content: space-around; margin: 15px 0; padding: 10px; background: #ecf0f1; border-radius: 8px;">',
                    f'<div style="text-align: center;">',
                    f'<span style="font-size: 28px; font-weight: bold; color: #e74c3c;">{int(data["Έργα"])}</span>',
                    f'<div style="color: #7f8c8d; font-size: 12px;">Συνολικά Έργα</div>',
                    f'</div>',
                    f'<div style="text-align: center;">',
                    f'<span style="font-size: 28px; font-weight: bold; color: #27ae60;">€{total_budget:,.0f}</span>',
                    f'<div style="color: #7f8c8d; font-size: 12px;">Συνολικός Προϋπ.</div>',
                    f'</div>',
                    f'<div style="text-align: center;">',
                    f'<span style="font-size: 28px; font-weight: bold; color: #f39c12;">{int(data["ΔΕΥΑ_Count"])}</span>',
                    f'<div style="color: #7f8c8d; font-size: 12px;">ΔΕΥΑ/Δήμοι</div>',
                    f'</div>',
                    f'</div>',
                    f'</div>'
                ]

                # --- Add example projects section ---
                projects_in_prefecture = df[df['Νομός'] == prefecture]
                if not projects_in_prefecture.empty:
                    # Find title and budget columns
                    title_col = next((col for col in projects_in_prefecture.columns if 'τίτλος' in col.lower()), 'Τίτλος Έργου')
                    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
                    
                    # Sort by budget if column exists, otherwise take first projects
                    if budget_col in projects_in_prefecture.columns:
                        top_projects = projects_in_prefecture.nlargest(3, budget_col)
                    else:
                        top_projects = projects_in_prefecture.head(3)
                    
                    project_list_html = []
                    for _, project in top_projects.iterrows():
                        title = project.get(title_col, 'N/A')
                        budget_val = f"€{project.get(budget_col, 0):,.0f}" if budget_col in project else "N/A"
                        project_list_html.append(f'<li style="margin-bottom: 5px;"><strong>{title[:60]}...</strong><br><small style="color: #27ae60;">{budget_val}</small></li>')

                    if project_list_html:
                        popup_parts.extend([
                            f'<div style="background: #f9f9f9; padding: 12px; border-radius: 8px; margin-top: 15px;">',
                            f'<h4 style="margin: 0 0 10px 0; color: #34495e; border-bottom: 2px solid #e0e0e0; padding-bottom: 5px;">🏗️ Παραδείγματα Έργων</h4>',
                            f'<ul style="list-style-type: none; padding-left: 0; margin: 0;">',
                            ''.join(project_list_html),
                            f'</ul>',
                            f'</div>'
                        ])

                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #27ae60; display: flex; align-items: center;"><span style="margin-right: 8px;">💰</span>Οικονομικά Στοιχεία</h4>')

                budget_col_sum = 'Συνολικός_Προϋπ_Ι'  # This refers to column I budget
                budget_col_mean = 'Μέσος_Προϋπ_Ι'

                if budget_col_sum in data and data[budget_col_sum] > 0:
                    total_budget = data[budget_col_sum]
                    avg_budget = data[budget_col_mean] if budget_col_mean in data and pd.notna(data[budget_col_mean]) else 0
                    
                    popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                    popup_parts.append(f'<span><strong>Συνολικός Π/Υ:</strong></span>')
                    popup_parts.append(f'<span style="color: #27ae60; font-weight: bold;">€{total_budget:,.0f}</span>')
                    popup_parts.append(f'</div>')
                    
                    if avg_budget > 0:
                        popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                        popup_parts.append(f'<span><strong>Μέσος Π/Υ:</strong></span>')
                        popup_parts.append(f'<span style="color: #f39c12; font-weight: bold;">€{avg_budget:,.0f}</span>')
                        popup_parts.append(f'</div>')
                    
                    # NEW CODE: Budget per Municipality/Region calculation
                    prefecture_df = df[df['Νομός'] == prefecture]
                    
                    # Find budget column (column I)
                    budget_column_I = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
                    
                    # Check if we have municipality/region data and budget data
                    if budget_column_I in prefecture_df.columns:
                        # Group by municipality (ΔΕΥΑ/Δήμος) to calculate budget per region
                        municipality_budget = prefecture_df.groupby('Φορέας Ύδρευσης')[budget_column_I].agg(['sum', 'count', 'mean']).reset_index()
                        municipality_budget = municipality_budget[municipality_budget['sum'] > 0]  # Only municipalities with budget data
                        
                        if not municipality_budget.empty:
                            # Calculate total municipalities with budget data
                            municipalities_with_budget = len(municipality_budget)
                            avg_budget_per_municipality = municipality_budget['sum'].mean()
                            
                            popup_parts.append(f'<div style="margin-top: 10px; border-top: 1px solid #ecf0f1; padding-top: 8px;">')
                            popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                            popup_parts.append(f'<span><strong>Δήμοι με Π/Υ:</strong></span>')
                            popup_parts.append(f'<span style="color: #9b59b6; font-weight: bold;">{municipalities_with_budget}</span>')
                            popup_parts.append(f'</div>')
                            
                            popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                            popup_parts.append(f'<span><strong>Μέσος Π/Υ/Δήμο:</strong></span>')
                            popup_parts.append(f'<span style="color: #8e44ad; font-weight: bold;">€{avg_budget_per_municipality:,.0f}</span>')
                            popup_parts.append(f'</div>')
                            
                            # Show top 3 municipalities by budget
                            top_municipalities = municipality_budget.nlargest(3, 'sum')
                            popup_parts.append(f'<div style="margin-top: 8px;">')
                            popup_parts.append(f'<div style="font-size: 12px; color: #7f8c8d; margin-bottom: 5px;">Top 3 Δήμοι (Π/Υ):</div>')
                            
                            for idx, row in top_municipalities.iterrows():
                                municipality_name = row['Φορέας Ύδρευσης']
                                municipality_budget_amount = row['sum']
                                municipality_projects = row['count']
                                
                                # Truncate long municipality names
                                display_name = municipality_name[:25] + "..." if len(municipality_name) > 25 else municipality_name
                                
                                popup_parts.append(f'<div style="font-size: 10px; margin: 2px 0; padding: 3px; background: #f8f9fa; border-radius: 3px;">')
                                popup_parts.append(f'<strong>{display_name}</strong><br>')
                                popup_parts.append(f'€{municipality_budget_amount:,.0f} ({municipality_projects} έργα)')
                                popup_parts.append(f'</div>')
                            
                            popup_parts.append(f'</div>')
                            popup_parts.append(f'</div>')
                else:
                    popup_parts.append('<div style="text-align: center; color: #7f8c8d; font-size: 12px; padding: 10px 0;">Δεν υπάρχουν διαθέσιμα οικονομικά στοιχεία.</div>')

                popup_parts.append('</div>')

                # 3. Project Progress Analytics
                prefecture_df = df[df['Νομός'] == prefecture]
                progress_col = next((col for col in ['Ποσοστό Ολοκλήρωσης', 'Progress', 'Completion'] if col in prefecture_df.columns), None)
                status_col = next((col for col in ['Στάδιο', 'Status', 'Phase', 'Τρέχουσα Κατάσταση'] if col in prefecture_df.columns), None)

                popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #8e44ad; display: flex; align-items: center;"><span style="margin-right: 8px;">📈</span>Πρόοδος Έργων</h4>')

                if progress_col:
                    # Extract completion percentages
                    completion_data = prefecture_df[progress_col].dropna()
                    completion_values = []
                    for comp in completion_data:
                        if isinstance(comp, str):
                            percentages = re.findall(r'(\d+)%', comp)
                            if percentages:
                                completion_values.extend([int(p) for p in percentages])
                    
                    if completion_values:
                        avg_completion = np.mean(completion_values)
                        completed = sum(1 for v in completion_values if v >= 100)
                        in_progress = sum(1 for v in completion_values if 50 <= v < 100)
                        early_stage = sum(1 for v in completion_values if v < 50)
                        
                        popup_parts.append(f'<div style="margin-bottom: 10px; text-align: center;">')
                        popup_parts.append(f'<div style="font-size: 24px; color: #8e44ad; font-weight: bold;">{avg_completion:.1f}%</div>')
                        popup_parts.append(f'<div style="color: #7f8c8d; font-size: 12px;">Μέση Ολοκλήρωση</div>')
                        popup_parts.append(f'</div>')
                        
                        # Progress bar
                        popup_parts.append(f'<div style="background: #ecf0f1; border-radius: 10px; height: 8px; margin: 10px 0;">')
                        popup_parts.append(f'<div style="background: linear-gradient(90deg, #e74c3c, #f39c12, #27ae60); width: {avg_completion}%; height: 100%; border-radius: 10px;"></div>')
                        popup_parts.append(f'</div>')
                        
                        popup_parts.append('<div style="display: flex; justify-content: space-between; font-size: 11px; margin-top: 8px;">')
                        popup_parts.append(f'<span>✅ Ολοκλήρωση: {completed}</span>')
                        popup_parts.append(f'<span>🔄 Σε εξέλιξη: {in_progress}</span>')
                        popup_parts.append(f'<span>🔨 Έναρξη: {early_stage}</span>')
                        popup_parts.append('</div>')

                if status_col:
                    status_counts = prefecture_df[status_col].value_counts().head(3)
                    if not status_counts.empty:
                        popup_parts.append('<div style="margin-top: 10px; border-top: 1px solid #ecf0f1; padding-top: 8px;">')
                        popup_parts.append('<div style="font-size: 12px; color: #7f8c8d;">Κύρια Στάδια:</div>')
                        for status, count in status_counts.items():
                            popup_parts.append(f'<div style="font-size: 11px;">• {status}: {count}</div>')
                        popup_parts.append('</div>')

                popup_parts.append('</div>')

                popup_parts.append('</div>')

                # 4. Project Categories
                popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #e67e22; display: flex; align-items: center;"><span style="margin-right: 8px;">🏗️</span>Κατηγορίες Έργων</h4>')

                if 'Κατηγορία Έργου' in prefecture_df.columns:
                    budget_col_name = next((col for col in prefecture_df.columns if 'προϋπολογισμός' in col), None)
                    category_counts = prefecture_df['Κατηγορία Έργου'].value_counts().head(4)

                    if not category_counts.empty:
                        popup_parts.append('<ul style="list-style: none; padding: 0; margin: 0; font-size: 12px;">')
                        for category, count in category_counts.items():
                            category_budget = 0
                            if budget_col_name:
                                category_budget = prefecture_df[prefecture_df['Κατηγορία Έργου'] == category][budget_col_name].sum()
                            
                            popup_parts.append(f'<li style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #ecf0f1;">')
                            popup_parts.append(f'<span>{str(category)} ({count})</span>')
                            popup_parts.append(f'<strong style="color: #27ae60;">€{category_budget:,.0f}</strong>')
                            popup_parts.append(f'</li>')
                        popup_parts.append('</ul>')

                # Priority distribution if available
                priority_col = next((col for col in prefecture_df.columns if 'προτεραιότητα' in str(col).lower()), None)
                if priority_col:
                    priority_counts = prefecture_df[priority_col].value_counts().head(3)
                    if not priority_counts.empty:
                        popup_parts.append('<div style="margin-top: 10px; border-top: 1px solid #ecf0f1; padding-top: 8px;">')
                        popup_parts.append('<div style="font-size: 12px; color: #7f8c8d; margin-bottom: 5px;">Προτεραιότητες:</div>')
                        popup_parts.append('<div style="display: flex; gap: 8px; font-size: 10px;">')
                        
                        priority_colors = {'1η': '#e74c3c', '2η': '#f39c12', '3η': '#27ae60'}
                        for priority, count in priority_counts.items():
                            color = priority_colors.get(str(priority)[:2], '#95a5a6')
                            popup_parts.append(f'<span style="background: {color}; color: white; padding: 2px 6px; border-radius: 12px;">{priority}: {count}</span>')
                        
                        popup_parts.append('</div>')
                        popup_parts.append('</div>')

                popup_parts.append('</div>')

                # Demographics & Impact Section
                popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #16a085; display: flex; align-items: center;"><span style="margin-right: 8px;">👥</span>Δημογραφικά & Επίδραση</h4>')

                # NEW CODE: Budget efficiency per region
                budget_column_I = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
                if budget_column_I in prefecture_df.columns:
                    budget_data = prefecture_df[budget_column_I].dropna()
                    if not budget_data.empty:
                        total_prefecture_budget = budget_data.sum()
                        num_municipalities = len(prefecture_df['Φορέας Ύδρευσης'].unique())
                        budget_per_municipality_avg = total_prefecture_budget / num_municipalities if num_municipalities > 0 else 0
                        
                        popup_parts.append(f'<div style="margin-top: 10px; padding: 8px; background: #e8f5e8; border-radius: 6px;">')
                        popup_parts.append(f'<div style="font-size: 11px; color: #16a085; text-align: center;">')
                        popup_parts.append(f'💰 <strong>Οικονομική Αποδοτικότητα</strong><br>')
                        popup_parts.append(f'€{budget_per_municipality_avg:,.0f} μέσος Π/Υ ανά δήμο<br>')
                        popup_parts.append(f'{num_municipalities} συνολικοί δήμοι/φορείς')
                        popup_parts.append(f'</div>')
                        popup_parts.append(f'</div>')

                popup_parts.append('</div>')

                # 5. Timeline Information
                popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #3498db; display: flex; align-items: center;"><span style="margin-right: 8px;">📅</span>Χρονοδιάγραμμα</h4>')

                # Timeline analysis
                time_cols = [col for col in prefecture_df.columns if any(word in str(col).lower() for word in ['χρόνος', 'μήνες', 'time', 'months'])]
                date_cols = [col for col in prefecture_df.columns if 'ημερομηνί' in str(col).lower()]

                if time_cols:
                    time_data = prefecture_df[time_cols[0]].dropna()
                    if len(time_data) > 0:
                        avg_duration = time_data.mean() if pd.api.types.is_numeric_dtype(time_data) else 0
                        
                        if avg_duration > 0:
                            popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                            popup_parts.append(f'<span><strong>Μέση Διάρκεια:</strong></span>')
                            popup_parts.append(f'<span style="color: #3498db; font-weight: bold;">{avg_duration:.1f} μήνες</span>')
                            popup_parts.append(f'</div>')
                        
                        # Duration categories
                        if pd.api.types.is_numeric_dtype(time_data):
                            short_term = len(time_data[time_data <= 12])
                            medium_term = len(time_data[(time_data > 12) & (time_data <= 36)])
                            long_term = len(time_data[time_data > 36])
                            
                            popup_parts.append('<div style="display: flex; justify-content: space-between; font-size: 11px; margin-top: 8px;">')
                            popup_parts.append(f'<span>⚡ Βραχυπρόθεσμα: {short_term}</span>')
                            popup_parts.append(f'<span>🔄 Μεσοπρόθεσμα: {medium_term}</span>')
                            popup_parts.append(f'<span>⏳ Μακροπρόθεσμα: {long_term}</span>')
                            popup_parts.append('</div>')

                # Current year projects
                from datetime import datetime
                current_year = datetime.now().year

                if date_cols:
                    dates_data = prefecture_df[date_cols[0]].dropna()
                    current_year_projects = 0
                    
                    for date_str in dates_data:
                        if isinstance(date_str, str) and str(current_year) in date_str:
                            current_year_projects += 1
                    
                    if current_year_projects > 0:
                        popup_parts.append(f'<div style="margin-top: 10px; padding: 8px; background: #e8f6ff; border-radius: 6px; text-align: center;">')
                        popup_parts.append(f'<span style="color: #3498db; font-weight: bold;">🚀 Έργα {current_year}: {current_year_projects}</span>')
                        popup_parts.append(f'</div>')

                popup_parts.append('</div>')

                # 6. Demographics & Impact Section
                popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #16a085; display: flex; align-items: center;"><span style="margin-right: 8px;">👥</span>Δημογραφικά & Επίδραση</h4>')

                # Population served
                pop_cols = [col for col in prefecture_df.columns if 'πληθυσμός' in str(col).lower() and prefecture_df[col].dtype in ['int64', 'float64']]
                if pop_cols:
                    pop_data = prefecture_df[pop_cols[0]].dropna()
                    if len(pop_data) > 0:
                        total_population = pop_data.sum()
                        avg_population = pop_data.mean()
                        
                        popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                        popup_parts.append(f'<span><strong>Συν. Πληθυσμός:</strong></span>')
                        popup_parts.append(f'<span style="color: #16a085; font-weight: bold;">{total_population:,.0f}</span>')
                        popup_parts.append(f'</div>')
                        
                        popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                        popup_parts.append(f'<span><strong>Μέσος/Έργο:</strong></span>')
                        popup_parts.append(f'<span style="color: #f39c12; font-weight: bold;">{avg_population:,.0f}</span>')
                        popup_parts.append(f'</div>')

                # DEYA count
                deya_count = len(prefecture_df['Φορέας Ύδρευσης'].unique())
                popup_parts.append(f'<div style="display: flex; justify-content: space-between; margin: 8px 0;">')
                popup_parts.append(f'<span><strong>ΔΕΥΑ/Δήμοι:</strong></span>')
                popup_parts.append(f'<span style="color: #9b59b6; font-weight: bold;">{deya_count}</span>')
                popup_parts.append(f'</div>')

                # Environmental impact indicators
                popup_parts.append('<div style="margin-top: 10px; padding: 8px; background: #e8f8f5; border-radius: 6px;">')
                popup_parts.append('<div style="font-size: 11px; color: #16a085; text-align: center;">')
                popup_parts.append(f'🌍 Περιβαλλοντική Επίδραση: {len(prefecture_df)} έργα')
                popup_parts.append('<br>💧 Βελτίωση ποιότητας νερού & υγείας')
                popup_parts.append('</div>')
                popup_parts.append('</div>')

                popup_parts.append('</div>')

                # Enhanced Information Section (instead of interactive buttons)
                popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #c0392b; display: flex; align-items: center;"><span style="margin-right: 8px;">📋</span>Πρόσθετες Πληροφορίες</h4>')

                # Quick stats grid
                popup_parts.append('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11px;">')

                # Total projects in region
                region_projects = len(df[df['Περιφέρεια'] == coords['region']])
                popup_parts.append(f'<div style="background: #ecf0f1; padding: 8px; border-radius: 6px; text-align: center;">')
                popup_parts.append(f'<strong>📍 Περιφέρεια</strong><br>{coords["region"]}<br>Έργα: {region_projects}')
                popup_parts.append(f'</div>')

                # Prefecture rank
                prefecture_counts = df['Νομός'].value_counts()
                prefecture_rank = list(prefecture_counts.index).index(prefecture) + 1 if prefecture in prefecture_counts.index else 0
                popup_parts.append(f'<div style="background: #ecf0f1; padding: 8px; border-radius: 6px; text-align: center;">')
                popup_parts.append(f'<strong>🏆 Κατάταξη</strong><br>#{prefecture_rank}<br>από {len(prefecture_counts)} νομούς')
                popup_parts.append(f'</div>')

                # Budget per capita if available
                if 'total_population' in locals() and total_population > 0 and budget_col_sum and data[budget_col_sum] > 0:
                    budget_per_capita = data[budget_col_sum] / total_population
                    popup_parts.append(f'<div style="background: #ecf0f1; padding: 8px; border-radius: 6px; text-align: center;">')
                    popup_parts.append(f'<strong>💰 Π/Υ ανά κάτοικο</strong><br>€{budget_per_capita:.0f}')
                    popup_parts.append(f'</div>')

                # Project density
                popup_parts.append(f'<div style="background: #ecf0f1; padding: 8px; border-radius: 6px; text-align: center;">')
                popup_parts.append(f'<strong>🎯 Πυκνότητα</strong><br>{int(data["Έργα"])}/{deya_count} ΔΕΥΑ')
                popup_parts.append(f'</div>')

                popup_parts.append('</div>')

                # Note about clicking
                popup_parts.append('<div style="margin-top: 10px; padding: 8px; background: #fff3cd; border-radius: 6px; border-left: 4px solid #ffc107;">')
                popup_parts.append('<div style="font-size: 10px; color: #856404;">')
                popup_parts.append('<strong>💡 Συμβουλή:</strong> Κάντε κλικ στον χάρτη για να επιλέξετε άλλο νομό και να δείτε τα στοιχεία του.')
                popup_parts.append('</div>')
                popup_parts.append('</div>')

                popup_parts.append('</div>')

                # 8. Visual Performance Indicators
                popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #2c3e50; display: flex; align-items: center;"><span style="margin-right: 8px;">📊</span>Δείκτες Απόδοσης</h4>')

                # Heuristic performance score calculation
                score = 50  # Base score
                factors = []

                avg_completion = np.mean([int(p) for p in re.findall(r'(\d+)%', ' '.join(prefecture_df[progress_col].dropna().astype(str)))]) if progress_col and re.findall(r'(\d+)%', ' '.join(prefecture_df[progress_col].dropna().astype(str))) else 0
                if avg_completion > 75: score += 20; factors.append('✅ Υψηλή πρόοδος')
                elif avg_completion > 40: score += 10; factors.append('👍 Καλή πρόοδος')
                else: score -= 5; factors.append('⏳ Χαμηλή πρόοδος')

                if budget_col_sum and data[budget_col_sum] > 10000000: score += 10; factors.append('💰 Μεγάλος Π/Υ')
                if len(prefecture_df) > 15: score += 10; factors.append('📈 Πολλά έργα')
                else: score -= 5

                score = max(0, min(100, score)) # Clamp score between 0 and 100
                
                score_color = '#27ae60' if score > 70 else ('#f39c12' if score > 40 else '#e74c3c')

                # Gauge meter
                popup_parts.append(f'<div style="text-align: center; margin-bottom: 10px;">')
                popup_parts.append(f'<div style="font-size: 28px; font-weight: bold; color: {score_color};">{score}/100</div>')
                popup_parts.append(f'<div style="background: #ecf0f1; border-radius: 10px; height: 10px; margin: 5px 0;">')
                popup_parts.append(f'<div style="background: {score_color}; width: {score}%; height: 100%; border-radius: 10px;"></div>')
                popup_parts.append(f'</div>')
                popup_parts.append(f'</div>')

                # Score factors
                if factors:
                    popup_parts.append('<div style="font-size: 11px; text-align: center; color: #7f8c8d;">')
                    popup_parts.append(' &bull; '.join(factors))
                    popup_parts.append('</div>')

                popup_parts.append('</div>')

                # Regional Budget Breakdown
                budget_column_I = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
                if budget_column_I in prefecture_df.columns:
                    popup_parts.append('<div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 15px;">')
                    popup_parts.append('<h4 style="margin: 0 0 10px 0; color: #2c3e50; display: flex; align-items: center;"><span style="margin-right: 8px;">🏛️</span>Κατανομή Προϋπολογισμού ανά Δήμο</h4>')
                    
                    # Calculate budget distribution by municipality
                    municipality_stats = prefecture_df.groupby('Φορέας Ύδρευσης')[budget_column_I].agg(['sum', 'count']).reset_index()
                    municipality_stats = municipality_stats[municipality_stats['sum'] > 0]
                    municipality_stats = municipality_stats.sort_values('sum', ascending=False)
                    
                    if not municipality_stats.empty:
                        total_budget_in_prefecture = municipality_stats['sum'].sum()
                        
                        popup_parts.append('<div style="max-height: 120px; overflow-y: auto; font-size: 11px;">')
                        for idx, row in municipality_stats.head(5).iterrows():  # Show top 5
                            municipality = row['Φορέας Ύδρευσης']
                            budget = row['sum']
                            projects = row['count']
                            percentage = (budget / total_budget_in_prefecture) * 100
                            
                            # Truncate name for display
                            display_name = municipality[:30] + "..." if len(municipality) > 30 else municipality
                            
                            popup_parts.append(f'<div style="margin: 5px 0; padding: 5px; background: #f8f9fa; border-left: 4px solid #3498db; border-radius: 3px;">')
                            popup_parts.append(f'<strong>{display_name}</strong><br>')
                            popup_parts.append(f'€{budget:,.0f} ({percentage:.1f}%) - {projects} έργα')
                            popup_parts.append(f'</div>')
                        
                        popup_parts.append('</div>')
                        
                        if len(municipality_stats) > 5:
                            popup_parts.append(f'<div style="text-align: center; font-size: 10px; color: #7f8c8d; margin-top: 5px;">...και {len(municipality_stats) - 5} ακόμη δήμοι</div>')
                    
                    popup_parts.append('</div>')

                popup_parts.append('</div>')
                popup_text = ''.join(popup_parts)
                
                # Circle size based on projects (square root scale for better visibility)
                radius = max(8, min(int(np.sqrt(data['Έργα']) * 4), 40))
                
                folium.CircleMarker(
                    location=[coords['lat'], coords['lon']],
                    radius=radius,
                    popup=folium.Popup(popup_text, max_width=520, max_height=600),
                    color=coords['color'],
                    fillColor=coords['color'],
                    fillOpacity=0.7,
                    weight=3,
                    tooltip=f'{prefecture}: {int(data["Έργα"])} έργα'
                ).add_to(m)
                
                # Add project count label inside the circle
                folium.Marker(
                    location=[coords['lat'], coords['lon']],
                    icon=folium.DivIcon(
                        html=f'<div style="color: white; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); font-size: 12px;">{int(data["Έργα"])}</div>',
                        icon_size=(25, 25),
                        icon_anchor=(12, 12)
                    )
                ).add_to(m)
    
    # Enhanced legend with more regions
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 320px; height: 240px; 
                background-color: white; border:3px solid grey; z-index:9999; 
                font-size:11px; padding: 12px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
    <h4 style="margin-top: 0; color: #333; text-align: center;">🗺️ Χάρτης Έργων ανά Νομό</h4>
    <hr style="margin: 8px 0;">
    <div style="columns: 2; column-gap: 15px;">
    <p><i class="fa fa-circle" style="color:#FF6B6B"></i> Ανατ. Μακεδονία - Θράκη</p>
    <p><i class="fa fa-circle" style="color:#4ECDC4"></i> Κεντρική Μακεδονία</p>
    <p><i class="fa fa-circle" style="color:#45B7D1"></i> Αττική</p>
    <p><i class="fa fa-circle" style="color:#96CEB4"></i> Θεσσαλία</p>
    <p><i class="fa fa-circle" style="color:#FFEAA7"></i> Στερεά Ελλάδα</p>
    <p><i class="fa fa-circle" style="color:#DDA0DD"></i> Δυτική Ελλάδα</p>
    <p><i class="fa fa-circle" style="color:#98D8C8"></i> Πελοπόννησος</p>
    <p><i class="fa fa-circle" style="color:#F7DC6F"></i> Ιόνια νησιά</p>
    <p><i class="fa fa-circle" style="color:#BB8FCE"></i> Νότιο Αιγαίο</p>
    <p><i class="fa fa-circle" style="color:#85C1E9"></i> Βόρειο Αιγαίο</p>
    <p><i class="fa fa-circle" style="color:#F8C471"></i> Κρήτη</p>
    <p><i class="fa fa-circle" style="color:#82E0AA"></i> Ήπειρος</p>
    </div>
    <hr style="margin: 8px 0;">
    <p style="text-align: center; font-size: 10px; color: #666;">
    <strong>Μέγεθος κύκλου</strong> = Αριθμός έργων ανά νομό<br>
    <strong>Αριθμός</strong> = Συνολικά έργα νομού
    </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

def create_interactive_charts(df, selected_region=None, selected_prefecture=None):
    """Create interactive Plotly charts."""
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_region and selected_region != 'Όλες':
        filtered_df = filtered_df[filtered_df['Περιφέρεια'] == selected_region]
    
    if selected_prefecture and selected_prefecture != 'Όλοι':
        filtered_df = filtered_df[filtered_df['Νομός'] == selected_prefecture]
    
    if len(filtered_df) == 0:
        st.warning("❌ Δεν βρέθηκαν έργα για τα επιλεγμένα κριτήρια.")
        return
    
    # --- Main Content Area ---
    st.header("🗺️ Γενικός Χάρτης Έργων")
    
    # Create and display the map
    interactive_map = create_interactive_map_by_prefecture(df)
    map_data = st_folium(interactive_map, width=1200, height=600, key="charts_map")

    # Store the clicked prefecture
    if map_data and map_data['last_object_clicked_popup']:
        popup_html = map_data['last_object_clicked_popup']
        # Extract prefecture name from the popup's HTML content
        match = re.search(r'📍 (.*?)</h4', popup_html)
        if match:
            st.session_state['selected_prefecture_on_map'] = match.group(1).strip()
    
    # Enhanced metrics row
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("🏗️ Έργα", f"{len(filtered_df):,}")
    
    with col2:
        regions_count = len(filtered_df['Περιφέρεια'].unique())
        st.metric("🗺️ Περιφέρειες", regions_count)
    
    with col3:
        prefectures_count = len(filtered_df['Νομός'].unique())
        st.metric("🏛️ Νομοί", prefectures_count)
    
    with col4:
        deya_count = len(filtered_df['Φορέας Ύδρευσης'].unique())
        st.metric("🏢 ΔΕΥΑ/Δήμοι", deya_count)
    
    with col5:
        # Use the specific budget column
        budget_column_I = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
        if budget_column_I in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[budget_column_I]):
            total_budget = filtered_df[budget_column_I].sum() / 1_000_000_000
            st.metric("💰 Συν. Προϋπ.", f"{total_budget:.2f}B €")
        else:
            st.metric("💰 Συν. Προϋπ.", "N/A")
    
    with col6:
        # Use a specific population column
        population_col = 'Πληθυσμός'
        if population_col in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[population_col]):
            total_population = filtered_df[population_col].sum() / 1_000_000
            st.metric("👥 Πληθυσμός", f"{total_population:.1f}M")
        else:
            st.metric("👥 Πληθυσμός", "N/A")
    
    # Interactive charts in multiple rows
    st.subheader("📊 Διαδραστικά Γραφήματα")
    
    # First row - Regional and Prefecture distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive regional pie chart
        if len(filtered_df['Περιφέρεια'].unique()) > 1:
            region_counts = filtered_df['Περιφέρεια'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=region_counts.index,
                values=region_counts.values,
                hole=0.3,
                textinfo='label+percent+value',
                textposition='auto',
                marker=dict(
                    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                           '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8C471', '#82E0AA']
                )
            )])
            
            fig.update_layout(
                title={
                    'text': "📍 Κατανομή έργων ανά Περιφέρεια",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📍 Μία περιφέρεια επιλεγμένη")
    
    with col2:
        # Interactive prefecture bar chart
        prefecture_counts = filtered_df['Νομός'].value_counts().head(10)
        if not prefecture_counts.empty:
            
            fig = go.Figure(data=[go.Bar(
                y=prefecture_counts.index,
                x=prefecture_counts.values,
                orientation='h',
                marker=dict(
                    color=prefecture_counts.values,
                    colorscale='viridis',
                    showscale=True
                ),
                text=prefecture_counts.values,
                textposition='auto'
            )])
            
            fig.update_layout(
                title={
                    'text': "🏛️ Top 10 Νομοί (Αριθμός έργων)",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Αριθμός Έργων",
                yaxis_title="Νομός",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Second row - Project types and DEYA distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive project types
        if 'Κατηγορία Έργου' in filtered_df.columns:
            project_types = filtered_df['Κατηγορία Έργου'].value_counts().head(8)
            if not project_types.empty:
                
                fig = go.Figure(data=[go.Bar(
                    x=project_types.index,
                    y=project_types.values,
                    marker=dict(
                        color=project_types.values,
                        colorscale='blues',
                        showscale=True
                    ),
                    text=project_types.values,
                    textposition='auto'
                )])
                
                fig.update_layout(
                    title={
                        'text': "🏗️ Κατανομή ανά Είδος Έργου",
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    xaxis_title="Είδος Έργου",
                    yaxis_title="Αριθμός Έργων",
                    xaxis={'tickangle': 45},
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("🏗️ Δεν υπάρχουν δεδομένα ειδών έργων")
    
    with col2:
        # Interactive DEYA distribution
        deya_counts = filtered_df['Φορέας Ύδρευσης'].value_counts().head(10)
        if not deya_counts.empty:
            
            fig = go.Figure(data=[go.Pie(
                labels=deya_counts.index,
                values=deya_counts.values,
                textinfo='label+percent',
                textposition='auto',
                marker=dict(
                    colors=px.colors.qualitative.Set3
                )
            )])
            
            fig.update_layout(
                title={
                    'text': "🏢 Top 10 ΔΕΥΑ/Δήμοι",
                    'x': 0.5,
                    'xanchor': 'center'
                },
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Third row - Budget and Population analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive budget distribution
        budget_cols = [col for col in filtered_df.columns if 'προϋπολογισμός' in str(col).lower() and filtered_df[col].dtype in ['int64', 'float64']]
        if budget_cols:
            budget_data = filtered_df[budget_cols[0]].dropna()
            if len(budget_data) > 0:
                # Create budget ranges
                budget_ranges = pd.cut(
                    budget_data,
                    bins=[0, 100000, 500000, 1000000, 5000000, float('inf')],
                    labels=['<100K', '100K-500K', '500K-1M', '1M-5M', '>5M'],
                    include_lowest=True
                ).value_counts()
                
                fig = go.Figure(data=[go.Pie(
                    labels=budget_ranges.index,
                    values=budget_ranges.values,
                    hole=0.4,
                    textinfo='label+percent+value',
                    marker=dict(
                        colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                    )
                )])
                
                fig.update_layout(
                    title={
                        'text': "💰 Κατανομή Προϋπολογισμών",
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💰 Δεν υπάρχουν δεδομένα προϋπολογισμών")
        else:
            st.info("💰 Δεν βρέθηκε στήλη προϋπολογισμού")
    
    with col2:
        # Interactive priority distribution
        priority_cols = [col for col in filtered_df.columns if 'προτεραιότητα' in str(col).lower()]
        if priority_cols:
            priority_data = filtered_df[priority_cols[0]].value_counts()
            if not priority_data.empty:
                
                # Color mapping for priorities
                priority_colors = []
                for priority in priority_data.index:
                    if '1η' in str(priority):
                        priority_colors.append('#ff4444')  # Red for high priority
                    elif '2η' in str(priority):
                        priority_colors.append('#ffaa44')  # Orange for medium priority
                    else:
                        priority_colors.append('#44ff44')  # Green for low priority
                
                fig = go.Figure(data=[go.Bar(
                    x=priority_data.index,
                    y=priority_data.values,
                    marker=dict(
                        color=priority_colors
                    ),
                    text=priority_data.values,
                    textposition='auto'
                )])
                
                fig.update_layout(
                    title={
                        'text': "⭐ Κατανομή Προτεραιοτήτων",
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    xaxis_title="Προτεραιότητα",
                    yaxis_title="Αριθμός Έργων",
                    xaxis={'tickangle': 45},
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("⭐ Δεν υπάρχουν δεδομένα προτεραιοτήτων")
        else:
            st.info("⭐ Δεν βρέθηκε στήλη προτεραιότητας")
    
    # Fourth row - Timeline and Population analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive timeline analysis
        time_cols = [col for col in filtered_df.columns if any(word in str(col).lower() for word in ['χρόνος', 'μήνες', 'time', 'months'])]
        if time_cols:
            time_data = filtered_df[time_cols[0]].dropna()
            if len(time_data) > 0:
                
                fig = go.Figure(data=[go.Histogram(
                    x=time_data,
                    nbinsx=15,
                    marker=dict(
                        color='lightblue',
                        line=dict(color='darkblue', width=1)
                    )
                )])
                
                fig.update_layout(
                    title={
                        'text': "⏱️ Κατανομή Χρόνου Ολοκλήρωσης",
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    xaxis_title="Μήνες",
                    yaxis_title="Αριθμός Έργων",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("⏱️ Δεν υπάρχουν δεδομένα χρόνου")
        else:
            st.info("⏱️ Δεν βρέθηκε στήλη χρόνου")
    
    with col2:
        # Interactive population analysis
        pop_cols = [col for col in filtered_df.columns if 'πληθυσμός' in str(col).lower() and filtered_df[col].dtype in ['int64', 'float64']]
        if pop_cols:
            pop_data = filtered_df[pop_cols[0]].dropna()
            if len(pop_data) > 0:
                # Create population ranges
                pop_ranges = pd.cut(
                    pop_data,
                    bins=[0, 1000, 5000, 10000, 50000, float('inf')],
                    labels=['<1K', '1K-5K', '5K-10K', '10K-50K', '>50K'],
                    include_lowest=True
                ).value_counts()
                
                fig = go.Figure(data=[go.Bar(
                    x=pop_ranges.index,
                    y=pop_ranges.values,
                    marker=dict(
                        color=pop_ranges.values,
                        colorscale='blues',
                        showscale=True
                    ),
                    text=pop_ranges.values,
                    textposition='auto'
                )])
                
                fig.update_layout(
                    title={
                        'text': "👥 Κατανομή Εξυπηρετούμενου Πληθυσμού",
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    xaxis_title="Εύρος Πληθυσμού",
                    yaxis_title="Αριθμός Έργων",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👥 Δεν υπάρχουν δεδομένα πληθυσμού")
        else:
            st.info("👥 Δεν βρέθηκε στήλη πληθυσμού")

    # Πέμπτη σειρά - Ανάλυση ανά Δήμο/ΔΕΥΑ
    st.subheader("🏢 Ανάλυση ΔΕΥΑ/Δήμων")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top ΔΕΥΑ με περισσότερα έργα
        deya_projects = filtered_df.groupby('Φορέας Ύδρευσης').agg({
            'Α/Α': 'count',
            'Νομός': 'first'
        }).sort_values('Α/Α', ascending=False).head(15)
        
        # Δημιουργία labels με νομό
        labels_with_prefecture = [
            f"{deya} ({prefecture})" 
            for deya, prefecture in zip(deya_projects.index, deya_projects['Νομός'])
        ]
        
        fig = go.Figure(data=[go.Bar(
            y=[label[:40] + "..." if len(label) > 40 else label for label in labels_with_prefecture],
            x=deya_projects['Α/Α'],
            orientation='h',
            marker=dict(
                color=deya_projects['Α/Α'],
                colorscale='plasma',
                showscale=True
            ),
            text=deya_projects['Α/Α'],
            textposition='auto'
        )])
        
        fig.update_layout(
            title="🏆 Top 15 ΔΕΥΑ/Δήμοι (Αριθμός Έργων)",
            xaxis_title="Αριθμός Έργων",
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Κατανομή έργων ανά μέγεθος ΔΕΥΑ
        deya_counts = filtered_df['Φορέας Ύδρευσης'].value_counts()
        
        # Κατηγοριοποίηση ΔΕΥΑ
        size_categories = []
        for count in deya_counts.values:
            if count >= 10:
                size_categories.append('Μεγάλα ΔΕΥΑ (10+ έργα)')
            elif count >= 5:
                size_categories.append('Μεσαία ΔΕΥΑ (5-9 έργα)')
            elif count >= 2:
                size_categories.append('Μικρά ΔΕΥΑ (2-4 έργα)')
            else:
                size_categories.append('Πολύ Μικρά ΔΕΥΑ (1 έργο)')
        
        size_distribution = pd.Series(size_categories).value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=size_distribution.index,
            values=size_distribution.values,
            hole=0.4,
            textinfo='label+percent+value',
            marker=dict(
                colors=['#e74c3c', '#f39c12', '#f1c40f', '#95a5a6']
            )
        )])
        
        fig.update_layout(
            title="📊 Κατανομή ΔΕΥΑ ανά Μέγεθος",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

def create_project_progress_analysis(df, selected_region, selected_prefecture):
    """Create comprehensive project progress analysis tab."""
    
    st.subheader("📊 Ανάλυση Προόδου Έργων")
    st.markdown("Εις βάθος ανάλυση της προόδου έργων με βάση τα δεδομένα από το Word document")
    
    # Word-derived columns for analysis
    word_columns = {
        'Τίτλος Έργου (Word)': 'project_title_word',
        'Τρέχουσα Κατάσταση': 'current_status',
        'Φάση Έργου': 'project_phase', 
        'Τεχνικά Στοιχεία': 'technical_specs',
        'Ημερομηνίες': 'dates',
        'Ποσοστό Ολοκλήρωσης': 'completion_percentage',
        'Χρηματοδότηση': 'funding',
        'Κατάσταση Έγκρισης': 'approval_status',
        'Πηγές από Word': 'sources'
    }
    
    # Check which columns exist
    available_word_columns = {k: v for k, v in word_columns.items() if k in df.columns}
    
    if not available_word_columns:
        st.error("❌ Δεν βρέθηκαν στήλες Word. Βεβαιωθείτε ότι το αρχείο περιέχει τις στήλες από X έως AF.")
        return
    
    st.success(f"✅ Βρέθηκαν {len(available_word_columns)} στήλες Word για ανάλυση")
    
    # Progress Overview Metrics
    st.subheader("🎯 Συνολική Επισκόπηση Προόδου")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        # Projects with status info
        if 'Τρέχουσα Κατάσταση' in df.columns:
            status_count = len(df[df['Τρέχουσα Κατάσταση'].notna() & (df['Τρέχουσα Κατάσταση'] != '')])
            st.metric("📋 Έργα με Κατάσταση", f"{status_count:,}")
        
    with col2:
        # Projects with phase info
        if 'Φάση Έργου' in df.columns:
            phase_count = len(df[df['Φάση Έργου'].notna() & (df['Φάση Έργου'] != '')])
            st.metric("⚙️ Έργα με Φάση", f"{phase_count:,}")
    
    with col3:
        # Projects with completion percentage
        if 'Ποσοστό Ολοκλήρωσης' in df.columns:
            completion_count = len(df[df['Ποσοστό Ολοκλήρωσης'].notna() & (df['Ποσοστό Ολοκλήρωσης'] != '')])
            st.metric("📈 Έργα με % Ολοκλήρωσης", f"{completion_count:,}")
    
    with col4:
        # Projects with dates
        if 'Ημερομηνίες' in df.columns:
            dates_count = len(df[df['Ημερομηνίες'].notna() & (df['Ημερομηνίες'] != '')])
            st.metric("📅 Έργα με Ημερομηνίες", f"{dates_count:,}")
    
    with col5:
        # Projects with approval status
        if 'Κατάσταση Έγκρισης' in df.columns:
            approval_count = len(df[df['Κατάσταση Έγκρισης'].notna() & (df['Κατάσταση Έγκρισης'] != '')])
            st.metric("✅ Έργα με Έγκριση", f"{approval_count:,}")
    
    # Detailed Progress Analysis
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Ανάλυση Φάσεων", 
        "📈 Ανάλυση Ολοκλήρωσης", 
        "📅 Χρονική Ανάλυση", 
        "💰 Ανάλυση Χρηματοδότησης"
    ])
    
    with tab1:
        create_phase_analysis(df)
    
    with tab2:
        create_completion_analysis(df)
    
    with tab3:
        create_timeline_analysis(df)
    
    with tab4:
        create_funding_analysis(df, selected_region, selected_prefecture)

def create_phase_analysis(df):
    """Detailed project phase analysis."""
    st.subheader("⚙️ Αναλυτική Ανάλυση Φάσεων Έργων")
    
    if 'Φάση Έργου' not in df.columns:
        st.warning("⚠️ Δεν βρέθηκε στήλη 'Φάση Έργου'")
        return
    
    # Extract and analyze phases
    phase_data = df['Φάση Έργου'].dropna()
    all_phases = []
    
    for phases in phase_data:
        if isinstance(phases, str) and phases.strip():
            phase_list = [p.strip() for p in phases.split(';') if p.strip()]
            all_phases.extend(phase_list)
    
    if not all_phases:
        st.warning("⚠️ Δεν βρέθηκαν δεδομένα φάσεων")
        return
    
    # Phase distribution
    phase_counts = pd.Series(all_phases).value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive phase distribution chart
        fig = go.Figure(data=[go.Bar(
            x=phase_counts.values,
            y=phase_counts.index,
            orientation='h',
            marker=dict(
                color=phase_counts.values,
                colorscale='viridis',
                showscale=True
            ),
            text=phase_counts.values,
            textposition='auto'
        )])
        
        fig.update_layout(
            title="📊 Κατανομή Φάσεων Έργων",
            xaxis_title="Αριθμός Έργων",
            yaxis_title="Φάση",
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Phase progression pie chart
        fig = go.Figure(data=[go.Pie(
            labels=phase_counts.index[:8],  # Top 8 phases
            values=phase_counts.values[:8],
            hole=0.3,
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title="🔄 Κυκλική Κατανομή Φάσεων",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Phase progression mapping
    st.subheader("📋 Κατηγοριοποίηση Φάσεων")
    
    # Define phase categories
    phase_categories = {
        'Προκαταρκτικές Φάσεις': ['Μελέτη', 'Σχεδιασμός', 'Έγκριση', 'Προκήρυξη'],
        'Διαδικασίες Ανάθεσης': ['Διακήρυξη', 'Δημοπράτηση', 'Διαγωνισμός', 'Ανάθεση'],
        'Υλοποίηση': ['Κατασκευή', 'Εγκατάσταση', 'Εργασίες', 'Υλοποίηση'],
        'Ολοκλήρωση': ['Ολοκλήρωση', 'Παραλαβή', 'Λειτουργία']
    }
    
    # Categorize phases
    categorized_phases = {category: 0 for category in phase_categories.keys()}
    uncategorized_phases = []
    
    for phase in all_phases:
        categorized = False
        for category, keywords in phase_categories.items():
            if any(keyword.lower() in phase.lower() for keyword in keywords):
                categorized_phases[category] += 1
                categorized = True
                break
        if not categorized:
            uncategorized_phases.append(phase)
    
    # Display categorized results
    col1, col2 = st.columns(2)
    
    with col1:
        # Category breakdown
        fig = go.Figure(data=[go.Bar(
            x=list(categorized_phases.keys()),
            y=list(categorized_phases.values()),
            marker=dict(
                color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
            ),
            text=list(categorized_phases.values()),
            textposition='auto'
        )])
        
        fig.update_layout(
            title="📊 Κατηγοριοποίηση Φάσεων",
            xaxis_title="Κατηγορία Φάσης",
            yaxis_title="Αριθμός Έργων",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Progress funnel
        total_projects = sum(categorized_phases.values())
        if total_projects > 0:
            percentages = [v/total_projects*100 for v in categorized_phases.values()]
            
            fig = go.Figure(go.Funnel(
                y=list(categorized_phases.keys()),
                x=list(categorized_phases.values()),
                textinfo="value+percent initial"
            ))
            
            fig.update_layout(
                title="🔽 Διαδικασία Εξέλιξης Έργων",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed phase table
    st.subheader("📋 Λεπτομερής Πίνακας Φάσεων")
    
    phase_df = pd.DataFrame({
        'Φάση': phase_counts.index,
        'Αριθμός Έργων': phase_counts.values,
        'Ποσοστό': (phase_counts.values / len(df) * 100).round(1)
    })
    
    st.dataframe(phase_df, use_container_width=True)

def create_completion_analysis(df):
    """Analyze project completion percentages."""
    st.subheader("📈 Ανάλυση Ποσοστού Ολοκλήρωσης")
    
    if 'Ποσοστό Ολοκλήρωσης' not in df.columns:
        st.warning("⚠️ Δεν βρέθηκε στήλη 'Ποσοστό Ολοκλήρωσης'")
        return
    
    # Extract completion percentages
    completion_data = df['Ποσοστό Ολοκλήρωσης'].dropna()
    
    # Parse percentages from text
    completion_values = []
    for comp in completion_data:
        if isinstance(comp, str):
            # Extract numbers followed by %
            percentages = re.findall(r'(\d+)%', comp)
            if percentages:
                completion_values.extend([int(p) for p in percentages])
    
    if not completion_values:
        st.warning("⚠️ Δεν βρέθηκαν έγκυρα ποσοστά ολοκλήρωσης")
        return
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_completion = np.mean(completion_values)
        st.metric("📊 Μέσο Ποσοστό", f"{avg_completion:.1f}%")
    
    with col2:
        median_completion = np.median(completion_values)
        st.metric("📊 Διάμεσο Ποσοστό", f"{median_completion:.1f}%")
    
    with col3:
        max_completion = np.max(completion_values)
        st.metric("📊 Μέγιστο Ποσοστό", f"{max_completion}%")
    
    with col4:
        completed_projects = sum(1 for v in completion_values if v >= 100)
        st.metric("✅ Ολοκληρωμένα", f"{completed_projects}")
    
    # Completion distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram of completion percentages
        fig = go.Figure(data=[go.Histogram(
            x=completion_values,
            nbinsx=20,
            marker=dict(
                color='lightblue',
                line=dict(color='darkblue', width=1)
            )
        )])
        
        fig.update_layout(
            title="📊 Κατανομή Ποσοστών Ολοκλήρωσης",
            xaxis_title="Ποσοστό Ολοκλήρωσης (%)",
            yaxis_title="Αριθμός Έργων",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Completion ranges
        ranges = ['0-25%', '26-50%', '51-75%', '76-99%', '100%']
        range_counts = [
            sum(1 for v in completion_values if 0 <= v <= 25),
            sum(1 for v in completion_values if 26 <= v <= 50),
            sum(1 for v in completion_values if 51 <= v <= 75),
            sum(1 for v in completion_values if 76 <= v <= 99),
            sum(1 for v in completion_values if v >= 100)
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=ranges,
            values=range_counts,
            hole=0.4,
            marker=dict(
                colors=['#ff6b6b', '#ffa726', '#ffee58', '#66bb6a', '#4caf50']
            )
        )])
        
        fig.update_layout(
            title="🎯 Κατηγορίες Προόδου",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def create_timeline_analysis(df):
    """Analyze project timelines and dates."""
    st.subheader("📅 Χρονική Ανάλυση Έργων")
    
    if 'Ημερομηνίες' not in df.columns:
        st.warning("⚠️ Δεν βρέθηκε στήλη 'Ημερομηνίες'")
        return
    
    # Extract dates
    date_data = df['Ημερομηνίες'].dropna()
    all_dates = []
    
    for dates in date_data:
        if isinstance(dates, str) and dates.strip():
            # Extract dates in various formats
            date_patterns = [
                r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4})\b',
                r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2})\b'
            ]
            
            for pattern in date_patterns:
                found_dates = re.findall(pattern, dates)
                all_dates.extend(found_dates)
    
    if not all_dates:
        st.warning("⚠️ Δεν βρέθηκαν έγκυρες ημερομηνίες")
        return
    
    # Parse dates
    parsed_dates = []
    for date_str in all_dates:
        try:
            # Try different date formats
            for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d/%m/%y']:
                try:
                    parsed_date = pd.to_datetime(date_str, format=fmt)
                    parsed_dates.append(parsed_date)
                    break
                except:
                    continue
        except:
            continue
    
    if not parsed_dates:
        st.warning("⚠️ Δεν ήταν δυνατή η ανάλυση των ημερομηνιών")
        return
    
    # Timeline statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        min_date = min(parsed_dates)
        st.metric("📅 Παλαιότερη Ημ/νία", min_date.strftime('%d/%m/%Y'))
    
    with col2:
        max_date = max(parsed_dates)
        st.metric("📅 Νεότερη Ημ/νία", max_date.strftime('%d/%m/%Y'))
    
    with col3:
        date_span = (max_date - min_date).days
        st.metric("📊 Χρονικό Εύρος", f"{date_span} ημέρες")
    
    with col4:
        total_dates = len(parsed_dates)
        st.metric("📊 Συνολικές Ημ/νίες", f"{total_dates}")
    
    # Timeline visualization
    # Group dates by year and month
    date_df = pd.DataFrame({'Date': parsed_dates})
    date_df['Year'] = date_df['Date'].dt.year
    date_df['Month'] = date_df['Date'].dt.month
    date_df['YearMonth'] = date_df['Date'].dt.to_period('M')
    
    monthly_counts = date_df.groupby('YearMonth').size().reset_index(name='Count')
    monthly_counts['YearMonth_str'] = monthly_counts['YearMonth'].astype(str)
    
    fig = go.Figure(data=[go.Scatter(
        x=monthly_counts['YearMonth_str'],
        y=monthly_counts['Count'],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    )])
    
    fig.update_layout(
        title="📈 Χρονολογική Κατανομή Έργων",
        xaxis_title="Χρονική Περίοδος",
        yaxis_title="Αριθμός Ημερομηνιών",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def create_funding_analysis(df, selected_region, selected_prefecture):
    """Analyze project funding sources."""
    st.subheader("💰 Ανάλυση Πηγών Χρηματοδότησης")
    
    if 'Χρηματοδότηση' not in df.columns:
        st.warning("⚠️ Δεν βρέθηκε στήλη 'Χρηματοδότηση'")
        return
    
    # Extract funding sources
    funding_data = df['Χρηματοδότηση'].dropna()
    all_funding = []
    
    for funding in funding_data:
        if isinstance(funding, str) and funding.strip():
            funding_list = [f.strip() for f in funding.split(';') if f.strip()]
            all_funding.extend(funding_list)
    
    if not all_funding:
        st.warning("⚠️ Δεν βρέθηκαν δεδομένα χρηματοδότησης")
        return
    
    # Funding distribution
    funding_counts = pd.Series(all_funding).value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Funding sources bar chart
        fig = go.Figure(data=[go.Bar(
            x=funding_counts.values,
            y=funding_counts.index,
            orientation='h',
            marker=dict(
                color=funding_counts.values,
                colorscale='blues',
                showscale=True
            ),
            text=funding_counts.values,
            textposition='auto'
        )])
        
        fig.update_layout(
            title="💰 Κατανομή Πηγών Χρηματοδότησης",
            xaxis_title="Αριθμός Έργων",
            yaxis_title="Πηγή Χρηματοδότησης",
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Funding pie chart
        fig = go.Figure(data=[go.Pie(
            labels=funding_counts.index,
            values=funding_counts.values,
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title="🔄 Ποσοστιαία Κατανομή Χρηματοδότησης",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed funding table
    st.subheader("📋 Λεπτομερής Πίνακας Χρηματοδότησης")
    
    funding_df = pd.DataFrame({
        'Πηγή Χρηματοδότησης': funding_counts.index,
        'Αριθμός Έργων': funding_counts.values,
        'Ποσοστό': (funding_counts.values / len(df) * 100).round(1)
    })
    
    st.dataframe(funding_df, use_container_width=True)

def create_summary_tables(df, selected_region=None, selected_prefecture=None):
    """Create interactive summary tables."""
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_region and selected_region != 'Όλες':
        filtered_df = filtered_df[filtered_df['Περιφέρεια'] == selected_region]
    
    if selected_prefecture and selected_prefecture != 'Όλοι':
        filtered_df = filtered_df[filtered_df['Νομός'] == selected_prefecture]
    
    st.subheader("📊 Συγκεντρωτικοί Πίνακες")
    
    # Prefecture summary
    if 'Νομός' in filtered_df.columns:
        st.write("**🏛️ Συγκεντρωτικός Πίνακας ανά Νομό**")
        
        # Dynamic aggregation
        agg_dict = {'Α/Α': 'count', 'Φορέας Ύδρευσης': 'nunique'}
        
        # Dynamically find columns for budget, population, and time
        budget_cols = [col for col in filtered_df.columns if 'προϋπολογισμός' in str(col).lower() and pd.api.types.is_numeric_dtype(filtered_df[col])]
        pop_cols = [col for col in filtered_df.columns if 'πληθυσμός' in str(col).lower() and pd.api.types.is_numeric_dtype(filtered_df[col])]
        time_cols = [col for col in filtered_df.columns if any(word in str(col).lower() for word in ['χρόνος', 'μήνες', 'time', 'months']) and pd.api.types.is_numeric_dtype(filtered_df[col])]

        # Add first found column of each type to aggregation
        if budget_cols:
            agg_dict[budget_cols[0]] = ['sum', 'mean']
        if pop_cols:
            agg_dict[pop_cols[0]] = 'sum'
        if time_cols:
            agg_dict[time_cols[0]] = 'mean'

        summary_data = filtered_df.groupby('Νομός').agg(agg_dict).round(0)
        
        # Flatten column names dynamically
        new_columns = ['Αριθμός Έργων', 'Αριθμός ΔΕΥΑ']
        if budget_cols:
            new_columns.extend([f'Συνολικός Προϋπ. (€)', f'Μέσος Προϋπ. (€)'])
        if pop_cols:
            new_columns.append(f'Συνολικός Πληθυσμός')
        if time_cols:
            new_columns.append(f'Μέσος Χρόνος (Μήνες)')

        summary_data.columns = new_columns
        
        # Sort by number of projects
        summary_data = summary_data.sort_values('Αριθμός Έργων', ascending=False)
        
        # Format large numbers
        if budget_cols:
            for col in ['Συνολικός Προϋπ. (€)', 'Μέσος Προϋπ. (€)']:
                if col in summary_data.columns:
                    summary_data[col] = summary_data[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        
        if pop_cols and 'Συνολικός Πληθυσμός' in summary_data.columns:
            summary_data['Συνολικός Πληθυσμός'] = summary_data['Συνολικός Πληθυσμός'].apply(
                lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"
            )
        if time_cols and 'Μέσος Χρόνος (Μήνες)' in summary_data.columns:
            summary_data['Μέσος Χρόνος (Μήνες)'] = summary_data['Μέσος Χρόνος (Μήνες)'].apply(
                lambda x: f"{x:,.1f}" if pd.notna(x) else "N/A"
            )
        
        st.dataframe(summary_data, use_container_width=True)
    
    # DEYA summary
    st.write("**🏢 Συγκεντρωτικός Πίνακας ανά ΔΕΥΑ/Δήμο**")
    
    deya_summary = filtered_df.groupby('Φορέας Ύδρευσης').agg({
        'Α/Α': 'count',
        'Νομός': 'first',
        'Περιφέρεια': 'first'
    }).rename(columns={
        'Α/Α': 'Αριθμός Έργων',
        'Νομός': 'Νομός',
        'Περιφέρεια': 'Περιφέρεια'
    }).sort_values('Αριθμός Έργων', ascending=False)
    
    st.dataframe(deya_summary.head(20), use_container_width=True)

def main():
    """Main function to run the Streamlit app."""
    # Set page config at the top level
    st.set_page_config(
        page_title="Διαδραστικός Χάρτης Έργων Ύδρευσης",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for better performance
    st.markdown("""
    <style>
        /* Hide Streamlit default elements */
        .main > div:first-child { padding-top: 0; }
        /* Optimize rendering */
        .stDataFrame { width: 100% !important; }
        /* Improve sidebar performance */
        .sidebar .sidebar-content { will-change: auto; }
    </style>
    """, unsafe_allow_html=True)
    
    # --- Sidebar --- #
    with st.sidebar:
        # Clear cache button
        if st.button('🔄 Επαναφόρτωση & Καθαρισμός Cache'):
            st.cache_data.clear()
            st.rerun()
            
        # Logo handling with multiple fallback paths
        logo_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo.png"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "loho.png"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "loho.png")
        ]
        
        logo_found = False
        for path in logo_paths:
            if os.path.exists(path):
                st.image(path, use_container_width=True)
                logo_found = True
                break
                
        if not logo_found:
            st.markdown("### 🗺️ Έργα Ύδρευσης")
            
        st.title("🗺️ Διαδραστικός Χάρτης Έργων Ύδρευσης")
        st.markdown("---")
    
    # Main content
    st.title("🗺️ Διαδραστικός Χάρτης Έργων Ύδρευσης Ελλάδας")
    st.markdown("**🚀 Διαδραστική ανάλυση έργων ύδρευσης ανά νομό και περιφέρεια**")
    
    # Enhanced sidebar
    with st.sidebar:
        st.header("📂 Φόρτωση Δεδομένων")
        
        # Check for corrected_teset_.xlsx in the current directory
        excel_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corrected_teset_.xlsx")
        
        if os.path.exists(excel_file_path):
            # If the file exists, use it automatically
            try:
                uploaded_file = open(excel_file_path, 'rb')
                st.success("✅ Βρέθηκε και φορτώθηκε το αρχείο: corrected_teset_.xlsx")
            except Exception as e:
                st.error(f"Σφάλμα κατά τη φόρτωση του αρχείου: {e}")
                uploaded_file = None
        else:
            # If the file doesn't exist, show file uploader
            st.warning("Δεν βρέθηκε το αρχείο corrected_teset_.xlsx. Παρακαλώ ανεβάστε το αρχείο σας.")
            uploaded_file = st.file_uploader(
                "📊 Ανεβάστε το Excel αρχείο:", 
                type=['xlsx', 'xls'],
                help="Επιλέξτε αρχείο Excel με έργα ύδρευσης"
            )
        
        if uploaded_file:
            with st.spinner("⏳ Φόρτωση και ανάλυση δεδομένων..."):
                df = load_and_analyze_excel_enhanced(uploaded_file)
                
                if df is not None:
                    # Cache the loaded dataframe
                    st.session_state['df'] = df
                    
                    # Show success message with data stats
                    st.success(f"✅ Φορτώθηκαν {len(df):,} εγγραφές με {len(df.columns)} πεδία")
                    
                    # Enhanced statistics in expander for better organization
                    with st.expander("📊 Συνοπτικά Στατιστικά", expanded=True):
                        # Regional breakdown with progress bars
                        if 'Περιφέρεια' in df.columns:
                            st.subheader("🗺️ Έργα ανά Περιφέρεια")
                            region_counts = df['Περιφέρεια'].value_counts()
                            total = len(df)
                            
                            # Show top 5 regions with progress bars
                            for region, count in region_counts.head(5).items():
                                percentage = (count / total) * 100
                                st.write(f"**{region}**")
                                st.progress(percentage / 100, f"{count:,} έργα ({percentage:.1f}%)")
                            
                            # Show "other" if there are more regions
                            if len(region_counts) > 5:
                                other_count = total - sum(region_counts.head(5))
                                other_percentage = (other_count / total) * 100
                                st.write(f"**Άλλες Περιφέρειες**")
                                st.progress(other_percentage / 100, f"{other_count:,} έργα ({other_percentage:.1f}%)")
                        
                        # Top prefectures with metrics
                        prefecture_counts = df['Νομός'].value_counts()
                        st.write("**🏛️ Top 5 Νομοί:**")
                        for prefecture, count in prefecture_counts.head(5).items():
                            st.write(f"• {prefecture}: {count}")
                else:
                    st.error("❌ Αποτυχία φόρτωσης αρχείου")
                    return
        else:
            st.info("👆 Ανεβάστε το Excel αρχείο για να ξεκινήσετε")
            return
    
    # Check if data exists
    if 'df' not in st.session_state:
        st.info("📁 Παρακαλώ φορτώστε το Excel αρχείο από την πλαϊνή μπάρα")
        return
    
    df = st.session_state['df']
    
    # Enhanced filter section
    st.subheader("🎯 Φίλτρα Επιλογής")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        regions = ['Όλες'] + sorted(df['Περιφέρεια'].unique().tolist())
        selected_region = st.selectbox(
            "🗺️ Περιφέρεια:",
            regions,
            key="region_selector"
        )
    
    with col2:
        # Dynamic prefecture selection
        if selected_region and selected_region != 'Όλες':
            available_prefectures = sorted(df[df['Περιφέρεια'] == selected_region]['Νομός'].unique())
        else:
            available_prefectures = sorted(df['Νομός'].unique())
        
        prefectures = ['Όλοι'] + available_prefectures
        selected_prefecture = st.selectbox(
            "🏛️ Νομός:",
            prefectures,
            key="prefecture_selector"
        )
    
    with col3:
        # Quick project type filter
        project_types = ['Όλα'] + sorted(df['Κατηγορία Έργου'].dropna().unique())
        selected_type = st.selectbox(
            "🏗️ Είδος Έργου:",
            project_types,
            key="quick_type_filter"
        )
    
    # Apply quick filter
    display_df = df.copy()
    if selected_type != 'Όλα':
        display_df = display_df[display_df['Κατηγορία Έργου'] == selected_type]
    
    # Διαδραστική αναζήτηση
    with st.expander("🔍 Αναζήτηση Έργων", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_title = st.text_input(
                "🔍 Αναζήτηση στον τίτλο:",
                key="search_title"
            )
        
        with col2:
            search_deya = st.selectbox(
                "🏢 ΔΕΥΑ/Δήμος:",
                ['Όλα'] + sorted(df['Φορέας Ύδρευσης'].unique()),
                key="search_deya"
            )
        
        with col3:
            # Φίλτρο προϋπολογισμού
            budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
            if budget_col in df.columns:
                budget_values = df[budget_col].dropna()
                if len(budget_values) > 0:
                    min_budget, max_budget = st.slider(
                        "💰 Εύρος Προϋπολογισμού (€):",
                        min_value=int(budget_values.min()),
                        max_value=int(budget_values.max()),
                        value=(int(budget_values.min()), int(budget_values.max())),
                        step=10000,
                        key="budget_slider"
                    )
        
        # Εφαρμογή φίλτρων αναζήτησης
        search_df = df.copy()
        
        if search_title:
            title_col = next((col for col in df.columns if 'τίτλος' in col.lower()), None)
            if title_col:
                search_df = search_df[search_df[title_col].str.contains(search_title, case=False, na=False)]
        
        if search_deya != 'Όλα':
            search_df = search_df[search_df['Φορέας Ύδρευσης'] == search_deya]
        
        if budget_col in df.columns and 'min_budget' in locals():
            search_df = search_df[
                (search_df[budget_col] >= min_budget) & 
                (search_df[budget_col] <= max_budget)
            ]
        
        if len(search_df) != len(df):
            st.success(f"🎯 Βρέθηκαν {len(search_df):,} έργα που ταιριάζουν στα κριτήρια")
            
            # Εμφάνιση αποτελεσμάτων
            display_columns = [
                col for col in ['Τίτλος Έργου', 'Φορέας Ύδρευσης', 'Νομός', budget_col, 'Κατηγορία Έργου']
                if col in search_df.columns
            ]
            
            st.dataframe(search_df[display_columns].head(10), use_container_width=True)
            
            if len(search_df) > 10:
                st.info(f"📋 Εμφανίζονται τα πρώτα 10 από {len(search_df)} αποτελέσματα")
            
            # Ενημέρωση των display_df για τις καρτέλες
            display_df = search_df.copy()

    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Διαδραστικός Χάρτης ανά Νομό", 
        "📊 Διαδραστικά Γραφήματα", 
        "📋 Συγκεντρωτικοί Πίνακες",
        "🔍 Ανάλυση Προόδου Έργων",
        "📍 Λεπτομερής Ανάλυση ανά Νομό/Δήμο"
    ])

    with tab1:
        st.subheader("🗺️ Διαδραστικός Χάρτης ανά Νομό")
        m = create_interactive_map_by_prefecture(display_df)
        map_data = st_folium(m, width=725, height=500)  # Render map and capture interaction
        if map_data and 'last_clicked_popup' in map_data and map_data['last_clicked_popup']:
            popup_html = map_data['last_clicked_popup']['html']
            prefecture_name_match = re.search(r'<h3>(.*?)</h3>', popup_html)
            if prefecture_name_match:
                prefecture_name = prefecture_name_match.group(1).strip()
                st.session_state['selected_prefecture_from_map'] = prefecture_name
        
        if 'selected_prefecture_from_map' in st.session_state and st.session_state['selected_prefecture_from_map']:
            st.subheader(f"Έργα για το Νομό: {st.session_state['selected_prefecture_from_map']}")
            prefecture_projects = display_df[display_df['Νομός'] == st.session_state['selected_prefecture_from_map']]
            st.dataframe(prefecture_projects, use_container_width=True)
    
    with tab2:
        create_interactive_charts(display_df, selected_region, selected_prefecture)
    
    with tab3:
        create_summary_tables(display_df, selected_region, selected_prefecture)
    
    with tab4:
        create_project_progress_analysis(display_df, selected_region, selected_prefecture)

    with tab5:
        create_detailed_regional_analysis(display_df, selected_region, selected_prefecture)

    # Data export functionality
    with st.expander("📁 Εξαγωγή Δεδομένων"):
        export_format = st.selectbox("Επιλέξτε μορφή εξαγωγής:", ["CSV", "Excel"])
        if export_format == "CSV":
            @st.cache
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')
            csv = convert_df(display_df)
            st.download_button("Εξαγωγή CSV", csv, "data.csv", "text/csv")
        elif export_format == "Excel":
            @st.cache
            def convert_df(df):
                return df.to_excel(index=False).encode('utf-8')
            excel = convert_df(display_df)
            st.download_button("Εξαγωγή Excel", excel, "data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def create_detailed_regional_analysis(df, selected_region=None, selected_prefecture=None):
    """Λεπτομερής ανάλυση έργων ανά νομό και δήμο με προϋπολογισμούς."""
    
    st.subheader("📍 Λεπτομερής Ανάλυση ανά Νομό/Δήμο")
    st.markdown("Εξερευνήστε αναλυτικά τα έργα, προϋπολογισμούς και στατιστικά για κάθε νομό και δήμο")
    
    # Φίλτρα επιλογής
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analysis_level = st.radio(
            "🎯 Επίπεδο Ανάλυσης:",
            ["Ανά Νομό", "Ανά Δήμο/ΔΕΥΑ", "Σύγκριση Νομών"],
            key="analysis_level"
        )
    
    with col2:
        # Επιλογή συγκεκριμένου νομού για βαθύτερη ανάλυση
        prefectures_list = ['Όλοι'] + sorted(df['Νομός'].unique().tolist())
        focus_prefecture = st.selectbox(
            "🏛️ Επιλογή Νομού για Ανάλυση:",
            prefectures_list,
            key="focus_prefecture"
        )
    
    with col3:
        # Επιλογή παραμέτρου ανάλυσης
        analysis_param = st.selectbox(
            "📊 Παράμετρος Ανάλυσης:",
            ["Προϋπολογισμός", "Αριθμός Έργων", "Πληθυσμός", "Χρόνος Ολοκλήρωσης"],
            key="analysis_param"
        )
    
    # Ανάλυση ανά επίπεδο
    if analysis_level == "Ανά Νομό":
        create_prefecture_analysis(df, analysis_param, focus_prefecture)
    elif analysis_level == "Ανά Δήμο/ΔΕΥΑ":
        create_municipality_analysis(df, analysis_param, focus_prefecture)
    else:
        create_prefecture_comparison(df, analysis_param)

def create_prefecture_analysis(df, analysis_param, focus_prefecture):
    """Ανάλυση ανά νομό."""
    st.subheader("🏛️ Ανάλυση ανά Νομό")
    
    # Προετοιμασία δεδομένων
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    pop_col = next((col for col in df.columns if 'πληθυσμός' in col.lower()), None)
    time_col = next((col for col in df.columns if any(word in col.lower() for word in ['χρόνος', 'μήνες'])), None)
    
    # Ομαδοποίηση ανά νομό
    prefecture_stats = df.groupby('Νομός').agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        budget_col: ['sum', 'mean', 'count'] if budget_col in df.columns and df[budget_col].notna().sum() > 0 else 'count',
        pop_col: 'sum' if pop_col else 'count',
        time_col: 'mean' if time_col else 'count'
    }).round(2)
    
    # Flatten columns
    prefecture_stats.columns = [
        'Αριθμός Έργων', 'Αριθμός ΔΕΥΑ/Δήμων', 
        'Συνολικός Προϋπολογισμός', 'Μέσος Προϋπολογισμός', 'Έργα με Προϋπολογισμό',
        'Συνολικός Πληθυσμός', 'Μέση Διάρκεια (μήνες)'
    ]
    
    # Top 10 νομοί
    if analysis_param == "Προϋπολογισμός" and 'Συνολικός Προϋπολογισμός' in prefecture_stats.columns:
        sorted_stats = prefecture_stats.nlargest(10, 'Συνολικός Προϋπολογισμός')
        metric_col = 'Συνολικός Προϋπολογισμός'
    else:
        sorted_stats = prefecture_stats.nlargest(10, 'Αριθμός Έργων')
        metric_col = 'Αριθμός Έργων'
    
    # Δημιουργία γραφημάτων
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart για top νομούς
        fig = go.Figure(data=[go.Bar(
            y=sorted_stats.index,
            x=sorted_stats[metric_col],
            orientation='h',
            marker=dict(
                color=sorted_stats[metric_col],
                colorscale='viridis',
                showscale=True
            ),
            text=[f"{x:,.0f}" for x in sorted_stats[metric_col]],
            textposition='auto'
        )])
        
        fig.update_layout(
            title=f"🏆 Top 10 Νομοί - {analysis_param}",
            xaxis_title=analysis_param,
            yaxis_title="Νομός",
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart για περιφερειακή κατανομή
        region_stats = df.groupby('Περιφέρεια')['Α/Α'].count().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=region_stats['Περιφέρεια'],
            values=region_stats['Α/Α'],
            hole=0.3,
            textinfo='label+percent',
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        
        fig.update_layout(
            title="🗺️ Κατανομή Έργων ανά Περιφέρεια",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Λεπτομερής πίνακας
    st.subheader("📋 Λεπτομερής Πίνακας Νομών")
    
    # Μορφοποίηση αριθμών
    display_stats = prefecture_stats.copy()
    if 'Συνολικός Προϋπολογισμός' in display_stats.columns:
        display_stats['Συνολικός Προϋπολογισμός'] = display_stats['Συνολικός Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
        display_stats['Μέσος Προϋπολογισμός'] = display_stats['Μέσος Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
    
    st.dataframe(display_stats.sort_values('Αριθμός Έργων', ascending=False), use_container_width=True)
    
    # Εάν επιλέχθηκε συγκεκριμένος νομός
    if focus_prefecture != 'Όλοι':
        st.subheader(f"🔍 Εις Βάθος Ανάλυση: {focus_prefecture}")
        create_single_prefecture_deep_dive(df, focus_prefecture)

def create_municipality_analysis(df, analysis_param, focus_prefecture):
    """Ανάλυση ανά δήμο/ΔΕΥΑ."""
    st.subheader("🏢 Ανάλυση ανά Δήμο/ΔΕΥΑ")
    
    # Φιλτράρισμα δεδομένων
    if focus_prefecture != 'Όλοι':
        filtered_df = df[df['Νομός'] == focus_prefecture]
        st.info(f"📍 Εμφάνιση δεδομένων για το Νομό: **{focus_prefecture}**")
    else:
        filtered_df = df.copy()
    
    # Προετοιμασία δεδομένων
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    
    municipality_stats = filtered_df.groupby(['Φορέας Ύδρευσης', 'Νομός']).agg({
        'Α/Α': 'count',
        budget_col: ['sum', 'mean'] if budget_col in filtered_df.columns else 'count',
        'Κατηγορία Έργου': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'N/A'
    }).round(2)
    
    # Flatten columns
    municipality_stats.columns = ['Αριθμός Έργων', 'Συνολικός Προϋπολογισμός', 'Μέσος Προϋπολογισμός', 'Κύρια Κατηγορία']
    municipality_stats = municipality_stats.reset_index()
    
    # Sorting
    if analysis_param == "Προϋπολογισμός":
        municipality_stats = municipality_stats.sort_values('Συνολικός Προϋπολογισμός', ascending=False)
    else:
        municipality_stats = municipality_stats.sort_values('Αριθμός Έργων', ascending=False)
    
    # Top 15 δήμοι
    top_municipalities = municipality_stats.head(15)
    
    # Γραφήματα
    col1, col2 = st.columns(2)
    
    with col1:
        # Horizontal bar chart
        fig = go.Figure(data=[go.Bar(
            y=[f"{row['Φορέας Ύδρευσης'][:25]}..." if len(row['Φορέας Ύδρευσης']) > 25 else row['Φορέας Ύδρευσης'] 
               for _, row in top_municipalities.iterrows()],
            x=top_municipalities['Αριθμός Έργων'],
            orientation='h',
            marker=dict(
                color=top_municipalities['Αριθμός Έργων'],
                colorscale='blues',
                showscale=True
            ),
            text=top_municipalities['Αριθμός Έργων'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Έργα: %{x}<br><extra></extra>'
        )])
        
        fig.update_layout(
            title="🏆 Top 15 Δήμοι/ΔΕΥΑ (Αριθμός Έργων)",
            xaxis_title="Αριθμός Έργων",
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Συνολικός Προϋπολογισμός' in top_municipalities.columns:
            # Scatter plot: Έργα vs Προϋπολογισμός
            fig = go.Figure(data=[go.Scatter(
                x=top_municipalities['Αριθμός Έργων'],
                y=top_municipalities['Συνολικός Προϋπολογισμός'],
                mode='markers+text',
                text=[name[:10] + "..." if len(name) > 10 else name 
                      for name in top_municipalities['Φορέας Ύδρευσης']],
                textposition='top center',
                marker=dict(
                    size=top_municipalities['Αριθμός Έργων'] * 2,
                    color=top_municipalities['Συνολικός Προϋπολογισμός'],
                    colorscale='viridis',
                    showscale=True,
                    colorbar=dict(title="Προϋπολογισμός")
                ),
                hovertemplate='<b>%{text}</b><br>Έργα: %{x}<br>Προϋπολογισμός: €%{y:,.0f}<br><extra></extra>'
            )])
            
            fig.update_layout(
                title="💰 Σχέση Έργων - Προϋπολογισμού",
                xaxis_title="Αριθμός Έργων",
                yaxis_title="Συνολικός Προϋπολογισμός (€)",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Λεπτομερής πίνακας
    st.subheader("📊 Πλήρης Πίνακας Δήμων/ΔΕΥΑ")
    
    # Μορφοποίηση
    display_municipalities = municipality_stats.copy()
    if 'Συνολικός Προϋπολογισμός' in display_municipalities.columns:
        display_municipalities['Συνολικός Προϋπολογισμός'] = display_municipalities['Συνολικός Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
        display_municipalities['Μέσος Προϋπολογισμός'] = display_municipalities['Μέσος Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
    
    # Pagination
    page_size = 20
    total_pages = len(display_municipalities) // page_size + (1 if len(display_municipalities) % page_size > 0 else 0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page_number = st.selectbox(
            f"📄 Επιλέξτε σελίδα (1-{total_pages}):",
            range(1, total_pages + 1),
            key="municipality_page"
        )
    
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    
    st.dataframe(
        display_municipalities.iloc[start_idx:end_idx],
        use_container_width=True
    )
    
    # Στατιστικά
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏢 Συνολικοί Δήμοι/ΔΕΥΑ", len(municipality_stats))
    with col2:
        total_projects = municipality_stats['Αριθμός Έργων'].sum()
        st.metric("🏗️ Συνολικά Έργα", f"{total_projects:,}")
    with col3:
        if 'Συνολικός Προϋπολογισμός' in municipality_stats.columns:
            total_budget = municipality_stats['Συνολικός Προϋπολογισμός'].sum()
            st.metric("💰 Συνολικός Προϋπολογισμός", f"€{total_budget:,.0f}")
    with col4:
        avg_projects = municipality_stats['Αριθμός Έργων'].mean()
        st.metric("📊 Μέσος Αριθμός Έργων/Δήμο", f"{avg_projects:.1f}")

def create_prefecture_comparison(df, analysis_param):
    """Σύγκριση νομών."""
    st.subheader("⚖️ Σύγκριση Νομών")
    
    # Επιλογή νομών για σύγκριση
    col1, col2 = st.columns(2)
    
    with col1:
        available_prefectures = sorted(df['Νομός'].unique().tolist())
        selected_prefectures = st.multiselect(
            "📍 Επιλέξτε Νομούς για Σύγκριση (max 6):",
            available_prefectures,
            default=available_prefectures[:6],
            max_selections=6,
            key="comparison_prefectures"
        )
    
    with col2:
        comparison_metrics = st.multiselect(
            "📊 Επιλέξτε Μετρικές:",
            ["Αριθμός Έργων", "Προϋπολογισμός", "Αριθμός ΔΕΥΑ", "Μέση Διάρκεια"],
            default=["Αριθμός Έργων", "Προϋπολογισμός"],
            key="comparison_metrics"
        )
    
    if not selected_prefectures:
        st.warning("⚠️ Επιλέξτε τουλάχιστον έναν νομό για σύγκριση")
        return
    
    # Φιλτράρισμα και προετοιμασία δεδομένων
    comparison_df = df[df['Νομός'].isin(selected_prefectures)]
    
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    time_col = next((col for col in df.columns if any(word in col.lower() for word in ['χρόνος', 'μήνες'])), None)
    
    comparison_stats = comparison_df.groupby('Νομός').agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        budget_col: 'sum' if budget_col in comparison_df.columns else 'count',
        time_col: 'mean' if time_col else 'count'
    }).round(2)
    
    comparison_stats.columns = ['Αριθμός Έργων', 'Αριθμός ΔΕΥΑ', 'Προϋπολογισμός', 'Μέση Διάρκεια']
    
    # Radar chart για σύγκριση
    if len(selected_prefectures) <= 3:
        fig = go.Figure()
        
        for prefecture in selected_prefectures:
            if prefecture in comparison_stats.index:
                values = []
                for metric in comparison_metrics:
                    if metric in comparison_stats.columns:
                        # Normalize values (0-100 scale)
                        max_val = comparison_stats[metric].max()
                        normalized_val = (comparison_stats.loc[prefecture, metric] / max_val) * 100
                        values.append(normalized_val)
                
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],  # Close the polygon
                    theta=comparison_metrics + [comparison_metrics[0]],
                    fill='toself',
                    name=prefecture
                ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title="📊 Σύγκριση Νομών (Normalized σε κλίμακα 0-100)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Bar charts για κάθε μετρική
    for i, metric in enumerate(comparison_metrics):
        if metric in comparison_stats.columns:
            col1, col2 = st.columns(2) if i % 2 == 0 else (col2, col1)
            
            with col1 if i % 2 == 0 else col2:
                fig = go.Figure(data=[go.Bar(
                    x=comparison_stats.index,
                    y=comparison_stats[metric],
                    marker=dict(
                        color=comparison_stats[metric],
                        colorscale='viridis'
                    ),
                    text=[f"{x:,.0f}" for x in comparison_stats[metric]],
                    textposition='auto'
                )])
                
                fig.update_layout(
                    title=f"📊 {metric}",
                    xaxis_title="Νομός",
                    yaxis_title=metric,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Σύγκριση σε πίνακα
    st.subheader("📋 Συγκριτικός Πίνακας")
    
    display_comparison = comparison_stats.copy()
    if 'Προϋπολογισμός' in display_comparison.columns:
        display_comparison['Προϋπολογισμός'] = display_comparison['Προϋπολογισμός'].apply(
            lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
        )
    
    st.dataframe(display_comparison.sort_values('Αριθμός Έργων', ascending=False), use_container_width=True)

def create_single_prefecture_deep_dive(df, prefecture_name):
    """Εις βάθος ανάλυση συγκεκριμένου νομού."""
    prefecture_df = df[df['Νομός'] == prefecture_name].copy()
    
    if len(prefecture_df) == 0:
        st.warning(f"⚠️ Δεν βρέθηκαν έργα για το νομό {prefecture_name}")
        return
    
    # Βασικά στατιστικά
    col1, col2, col3, col4 = st.columns(4)
    
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    
    with col1:
        total_projects = len(prefecture_df)
        st.metric("🏗️ Συνολικά Έργα", f"{total_projects:,}")
    
    with col2:
        unique_deya = len(prefecture_df['Φορέας Ύδρευσης'].unique())
        st.metric("🏢 ΔΕΥΑ/Δήμοι", unique_deya)
    
    with col3:
        if budget_col in prefecture_df.columns:
            total_budget = prefecture_df[budget_col].sum()
            st.metric("💰 Συνολικός Προϋπολογισμός", f"€{total_budget:,.0f}")
    
    with col4:
        if budget_col in prefecture_df.columns:
            avg_budget = prefecture_df[budget_col].mean()
            st.metric("📊 Μέσος Προϋπολογισμός", f"€{avg_budget:,.0f}")
    
    # Κατανομή ανά ΔΕΥΑ
    col1, col2 = st.columns(2)
    
    with col1:
        deya_counts = prefecture_df['Φορέας Ύδρευσης'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=deya_counts.index,
            values=deya_counts.values,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Έργα: %{value}<br>Ποσοστό: %{percent}<br><extra></extra>'
        )])
        
        fig.update_layout(
            title=f"🏢 Κατανομή Έργων ανά ΔΕΥΑ/Δήμο - {prefecture_name}",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Κατηγορία Έργου' in prefecture_df.columns:
            category_counts = prefecture_df['Κατηγορία Έργου'].value_counts()
            
            fig = go.Figure(data=[go.Bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                marker=dict(
                    color=category_counts.values,
                    colorscale='blues'
                ),
                text=category_counts.values,
                textposition='auto'
            )])
            
            fig.update_layout(
                title=f"🏗️ Κατηγορίες Έργων - {prefecture_name}",
                xaxis_title="Αριθμός Έργων",
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Λίστα όλων των έργων
    st.subheader(f"📋 Πλήρης Λίστα Έργων - {prefecture_name}")
    
    # Επιλογή στηλών για εμφάνιση
    available_columns = [col for col in prefecture_df.columns if col not in ['normalized_utility']]
    default_columns = [
        'Τίτλος Έργου', 'Φορέας Ύδρευσης', 
        budget_col if budget_col in prefecture_df.columns else 'Κατηγορία Έργου',
        'Κατηγορία Έργου'
    ]
    
    selected_columns = st.multiselect(
        "📊 Επιλέξτε στήλες για εμφάνιση:",
        available_columns,
        default=[col for col in default_columns if col in available_columns],
        key=f"columns_{prefecture_name}"
    )
    
    if selected_columns:
        # Φίλτρο για ΔΕΥΑ
        selected_deya = st.multiselect(
            "🏢 Φιλτράρισμα ανά ΔΕΥΑ (προαιρετικό):",
            sorted(prefecture_df['Φορέας Ύδρευσης'].unique()),
            key=f"deya_filter_{prefecture_name}"
        )
        
        display_df = prefecture_df.copy()
        if selected_deya:
            display_df = display_df[display_df['Φορέας Ύδρευσης'].isin(selected_deya)]
        
        # Μορφοποίηση προϋπολογισμού αν υπάρχει
        if budget_col in selected_columns and budget_col in display_df.columns:
            display_df[budget_col] = display_df[budget_col].apply(
                lambda x: f"€{x:,.0f}" if pd.notna(x) and x != 0 else "N/A"
            )
        
        st.dataframe(
            display_df[selected_columns].reset_index(drop=True),
            use_container_width=True
        )
        
        # Κουμπί εξαγωγής
        csv = display_df[selected_columns].to_csv(index=False)
        st.download_button(
            label=f"📥 Εξαγωγή σε CSV - {prefecture_name}",
            data=csv,
            file_name=f"projects_{prefecture_name}.csv",
            mime="text/csv"
        )

def create_export_summary(df):
    """Δημιουργία συγκεντρωτικών δεδομένων για εξαγωγή."""
    budget_col = 'Προϋπολογισμός (συνολική ΔΔ προ ΦΠΑ)'
    
    summary = df.groupby(['Περιφέρεια', 'Νομός']).agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        budget_col: ['sum', 'mean', 'count'] if budget_col in df.columns else 'count'
    })
    
    return summary

def create_prefecture_export(df):
    """Εξαγωγή δεδομένων ανά νομό."""
    return df.groupby('Νομός').agg({
        'Α/Α': 'count',
        'Φορέας Ύδρευσης': 'nunique',
        'Περιφέρεια': 'first'
    }).reset_index()

def create_municipality_export(df):
    """Εξαγωγή δεδομένων ανά δήμο."""
    return df.groupby(['Φορέας Ύδρευσης', 'Νομός']).agg({
        'Α/Α': 'count',
        'Περιφέρεια': 'first'
    }).reset_index()

    # Export δεδομένων
    st.subheader("📥 Εξαγωγή Δεδομένων")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Εξαγωγή Συγκεντρωτικών", key="export_summary"):
            summary_data = create_export_summary(display_df)
            csv = summary_data.to_csv(index=True)
            st.download_button(
                label="⬇️ Κατέβασμα CSV",
                data=csv,
                file_name="water_projects_summary.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🏛️ Εξαγωγή ανά Νομό", key="export_prefectures"):
            prefecture_data = create_prefecture_export(display_df)
            csv = prefecture_data.to_csv(index=False)
            st.download_button(
                label="⬇️ Κατέβασμα CSV",
                data=csv,
                file_name="projects_by_prefecture.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🏢 Εξαγωγή ανά ΔΕΥΑ", key="export_municipalities"):
            municipality_data = create_municipality_export(display_df)
            csv = municipality_data.to_csv(index=False)
            st.download_button(
                label="⬇️ Κατέβασμα CSV",
                data=csv,
                file_name="projects_by_municipality.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()