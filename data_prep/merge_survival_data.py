import csv

# ---- 1. Read the nuclei CSV (has pct_malignant_epithelial_hard) ----
nuclei = {}
with open('/home/sbarua/per_slide_malignant_epithelial.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['patient_id']
        nuclei[pid] = {
            'pct_pos_nuclei': float(row['pct_malignant_epithelial_hard']),
            'total_nuclei': int(row['total_nuclei']),
            'n_malignant': int(row['n_malignant_epithelial']),
        }

print(f"Nuclei CSV: {len(nuclei)} patients loaded")

# ---- 2. Read the clinical TSV (has OS months, status, demographics) ----
clinical = {}
with open('/home/sbarua/gbm_tcga_clinical_data.tsv', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        pid = row['Patient ID']
        # Skip duplicates (some patients have multiple samples, take first)
        if pid in clinical:
            continue
        os_months = row['Overall Survival (Months)']
        os_status = row['Overall Survival Status']

        # Skip if missing survival data
        if os_months == 'NA' or os_months == '' or os_status == 'NA' or os_status == '':
            continue

        os_days = round(float(os_months) * 30.44, 2)
        os_event = 1 if '1:DECEASED' in os_status else 0

        clinical[pid] = {
            'age': row['Diagnosis Age'] if row['Diagnosis Age'] != 'NA' else '',
            'sex': row['Sex'] if row['Sex'] != 'NA' else '',
            'ethnicity': row['Ethnicity Category'] if row['Ethnicity Category'] != 'NA' else '',
            'race': row['Race Category'] if row['Race Category'] != 'NA' else '',
            'cancer_type_detailed': row['Cancer Type Detailed'],
            'histologic_type': row['Neoplasm Histologic Type Name'] if row['Neoplasm Histologic Type Name'] != 'NA' else '',
            'OS_time_days': os_days,
            'OS_event': os_event,
        }

print(f"Clinical TSV: {len(clinical)} patients with valid survival data")

# ---- 3. Merge: only patients in BOTH files ----
merged = []
for pid in nuclei:
    if pid in clinical:
        row = {
            'patient_id': pid,
            'age': clinical[pid]['age'],
            'sex': clinical[pid]['sex'],
            'ethnicity': clinical[pid]['ethnicity'],
            'race': clinical[pid]['race'],
            'cancer_type_detailed': clinical[pid]['cancer_type_detailed'],
            'histologic_type': clinical[pid]['histologic_type'],
            'OS_time_days': clinical[pid]['OS_time_days'],
            'OS_event': clinical[pid]['OS_event'],
            'pct_pos_nuclei': nuclei[pid]['pct_pos_nuclei'],
            'total_nuclei': nuclei[pid]['total_nuclei'],
            'n_malignant': nuclei[pid]['n_malignant'],
        }
        merged.append(row)

# Sort by patient_id
merged.sort(key=lambda x: x['patient_id'])

print(f"\nMatched patients: {len(merged)}")
print(f"Not found in clinical: {len(nuclei) - len(merged)}")

# Show unmatched
unmatched = [pid for pid in nuclei if pid not in clinical]
if unmatched:
    print(f"Unmatched patient IDs: {unmatched}")

# ---- 4. Write merged CSV ----
output_path = '/home/sbarua/merged_survival_data.csv'
fieldnames = ['patient_id', 'age', 'sex', 'ethnicity', 'race', 'cancer_type_detailed',
              'histologic_type', 'OS_time_days', 'OS_event', 'pct_pos_nuclei',
              'total_nuclei', 'n_malignant']

with open(output_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged)

print(f"\nSaved to: {output_path}")
print(f"\n--- Summary ---")
print(f"Total patients in merged file: {len(merged)}")
deceased = sum(1 for r in merged if r['OS_event'] == 1)
living = sum(1 for r in merged if r['OS_event'] == 0)
print(f"Deceased (OS_event=1): {deceased}")
print(f"Living (OS_event=0): {living}")

# Show first 5 rows
print(f"\nFirst 5 rows:")
for r in merged[:5]:
    print(f"  {r['patient_id']} | age={r['age']} | OS_days={r['OS_time_days']} | event={r['OS_event']} | pct={r['pct_pos_nuclei']:.4f}")
