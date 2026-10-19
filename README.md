# ASCEND EchoLV

### Gradio-Based Left Ventricular Segmentation, Quantitative Analysis, and EF Classification from A4C Echocardiography

**ASCEND TOWER | IT And Software Development Lab, Pakistan**

*Research Supervisor: Dr. M. Raza Ali*

> [!IMPORTANT]
> **Research and educational use only.** ASCEND EchoLV is a non-diagnostic research prototype. It has not undergone clinical validation and must not be used for medical diagnosis, treatment, or patient-care decisions.

---

## Overview

**ASCEND EchoLV** is the interactive application built on top of the research pipeline documented in **[CAMUS-LV-Research](https://github.com/ayeshaacheema/CAMUS-LV-Research)**. It takes a paired end-diastolic (ED) and end-systolic (ES) apical four-chamber (A4C) echocardiography frame and runs the frozen research models to produce:

- Left ventricle (LV) cavity segmentation
- LV geometry: area and long-axis length
- Single-plane volume estimates: EDV, ESV, stroke volume (SV)
- Ejection fraction (EF) estimate
- EF-band classification (Lower / Intermediate / Higher)

This repository contains the **application code and frozen inference pipeline**. The full experimental record (segmentation experiments, quantitative analysis, classification, robustness study) is in the research repository linked above.

## Inference Pipeline

**ED/ES image input → preprocessing → Large U-Net segmentation → LV geometry → EDV/ESV → SV/EF → EF-band classification → visualization and reporting**

The models are frozen: no retraining occurs during case analysis.

## Application Features

| Module                  | Functionality                                                                 |
| ----------------------- | ----------------------------------------------------------------------------- |
| New Analysis            | Upload ED/ES NIfTI images, optional expert masks, and case details            |
| Clinical View           | Visualize LV contours and quantitative cardiac measurements                   |
| Segmentation Explorer   | Inspect original frames, binary masks, probability maps, and contours         |
| Quantitative Analysis   | Examine LV areas, lengths, volumes, SV, and EF                                |
| EF Classification       | View geometry-derived and learned EF-band outputs                             |
| Ground Truth Comparison | Compare predicted and expert LV masks using Dice and IoU                      |
| Model Information       | Inspect segmentation architecture, classifier details, and evaluation results |
| Case Management         | Save, reopen, review, and compare analysis cases                              |
| Reporting               | Export research reports as PDF and case data as CSV                           |

Screenshots of each module are available in the [research repository README](https://github.com/ayeshaacheema/CAMUS-LV-Research#application-screenshots).

## Frozen Models

| Component          | Configuration                                                    |
| ------------------ | ---------------------------------------------------------------- |
| Segmentation model | Large U-Net, 7,759,521 parameters                                |
| Input              | Grayscale A4C ED/ES frames, resized to 256×256                   |
| Output             | Sigmoid probability map, thresholded at 0.50                     |
| Classifier         | StandardScaler + Logistic Regression on 8 LV-derived features    |
| EF bands           | Lower ≤ 40%, Intermediate 40–50%, Higher ≥ 50%                   |

Reported evaluation (50 CAMUS patients, 100 frames): overall Dice **0.9292**, IoU **0.8700**; learned classifier accuracy **70.0%** (35/50), macro-F1 **0.663**. See the research repository for the full methodology and limitations.

## Repository Structure

```
ASCEND-EchoLV/
├── app.py                  # Application entry point
├── echolv_app.py           # Gradio interface
├── frozen_inference.py     # Frozen segmentation + measurement + classification pipeline
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container build
├── phase1_segmentation/
│   └── phase1F_final_model/models/          # Frozen U-Net
└── phase3_classification/
    └── phase3C_classifier_development/models/   # Frozen EF-band classifier
```

## Installation

**Requirements:** Python 3.10+ (TensorFlow/Keras and Gradio are installed via `requirements.txt`).

```bash
git clone https://github.com/ayeshaacheema/ASCEND-EchoLV.git
cd ASCEND-EchoLV

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

Gradio prints a local URL in the terminal (by default `http://127.0.0.1:7860`). Open it in your browser.

### Run with Docker

```bash
docker build -t ascend-echolv .
docker run -p 7860:7860 ascend-echolv
```

Then open `http://localhost:7860`.

## Using the App

1. Open **New Analysis**.
2. Upload the **ED** and **ES** A4C frames as NIfTI files (`.nii` / `.nii.gz`) from the same patient.
3. *(Optional)* Upload the expert LV masks for ED and ES to enable Dice/IoU comparison.
4. Enter the case details and run the analysis.
5. Review results in **Clinical View**, **Segmentation Explorer**, **Quantitative Analysis**, and **EF Classification**.
6. Save the case, then export a **PDF report** or **CSV** from the Reporting module.

## Input Format

- Paired ED and ES frames from the **apical four-chamber (A4C / 4CH)** view.
- NIfTI format, as used by the CAMUS dataset.
- The pipeline expects image spacing metadata to be present in the NIfTI header, since it is used for area and volume calculation.

## Dataset

The models were developed on the [CAMUS dataset](https://www.creatis.insa-lyon.fr/Challenge/camus/) (Leclerc et al., *IEEE Transactions on Medical Imaging*, 2019). The dataset is **not** redistributed here. Please obtain it from an authorized source and respect its terms of use.

## Limitations

- Volumes are **single-plane A4C geometric estimates**, not biplane Simpson measurements or independently validated clinical volumes.
- Classifier scores are **uncalibrated** and do not indicate the probability that a prediction is correct.
- Evaluation used 50 patients from one dataset (CAMUS); external generalization has not been established.
- Performance is lower on end-systolic frames and on Medium/Poor image-quality cases.
- The "Clinical View" label refers to the interface only and does not imply clinical validation.

## Related Repository

- **[CAMUS-LV-Research](https://github.com/ayeshaacheema/CAMUS-LV-Research)**: full experimental workflow, results, and analysis behind this application.

## Acknowledgments

Developed during a computer vision research internship at **ASCEND TOWER, IT AND Software Development Lab**, under the supervision of **Dr. M. Raza Ali**. The CAMUS dataset authors are acknowledged for making their data publicly accessible.

## License

No open-source license has been added. Project materials are not licensed for reuse unless permission is granted. Third-party datasets and software remain subject to their respective terms.
