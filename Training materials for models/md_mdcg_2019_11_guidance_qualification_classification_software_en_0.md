# Medical Device Coordination Group Document

# MDCG 2019-11

# Guidance on Qualification and Classification of Software in Regulation (EU) 2017/745 – MDR and Regulation (EU) 2017/746 – IVDR

October 2019

This document has been endorsed by the Medical Device Coordination Group (MDCG) established by Article 103 of Regulation (EU) 2017/745. The MDCG is composed of representatives of all Member States and it is chaired by a representative of the European Commission.

The document is not a European Commission document and it cannot be regarded as reflecting the official position of the European Commission. Any views expressed in this document are not legally binding and only the Court of Justice of the European Union can give binding interpretations of Union law.
# Guidance on Qualification and Classification of Software

# October 2019

# Guidance on Qualification and Classification of Software in Regulation (EU) 2017/745 – MDR and Regulation (EU) 2017/746 – IVDR

Page 1 of 28
# Table of Contents

1. Scope and purpose of this document 3
2. Definitions and abbreviations 3
3. Qualification 6
1. Introduction to qualification criteria 6
2. Medical Device Software (MDSW) 7
3. ‘Software driving or influencing the use of a medical device’ 8
4. Qualification criteria of MDSW as an in vitro diagnostic medical device 10
4. Classification of MDSW per MDR 2017/745 12
1. Implementing Rules 12
2. Classification Rules 12
5. Classification and implementing rules per IVDR 2017/746 15
1. Implementing Rules: 15
2. Classification Rules: 15
6. Considerations on placing on the market and conformity assessment of MDSW 16
1. Option 1: as a medical device in its own right 16
2. Option 2: as an integral component/part of a device 17
7. Modules 17
8. Consideration of changes to an MDSW 18
9. Annex I: Illustrative examples of qualification of software used in the healthcare environment 18
10. Annex II - Qualification examples of Medical Device Software (MDSW) according to Figures 1 and 2 24
11. Annex III - Usability of the IMDRF risk classification framework in the context of the MDR 26
12. Annex IV – Classification examples 27

Page 2 of 28
# 1. Scope and purpose of this document

This document, which primarily targets medical software manufacturers, defines the criteria for the qualification of software falling within the scope of the new medical devices regulations1 and provides guidance on the application of classification criteria for software under Regulation (EU) 2017/745 – MDR and Regulation (EU) 2017/746 – IVDR.2 The guidance also provides information related to placing on the market. The classification criteria (classification rules) are set out in Annex VIII of the Medical Devices Regulation (EU) 2017/745 (MDR) and Annex VIII of the In vitro Diagnostic Medical Devices Regulation (EU) 2017/746 (IVDR).

The criteria specified in this document shall also apply to applications (commonly referred to as apps), may they be operating on a mobile phone, in the cloud or on other platforms.

# 2. Definitions and abbreviations

# Intended purpose:

According to Regulation (EU) 2017/745 – MDR, “Intended purpose” means the use for which a device is intended according to the data supplied by the manufacturer on the label, in the instructions for use or in promotional or sales materials or statements and as specified by the manufacturer in the clinical evaluation;3

According to Regulation (EU) 2017/746 – IVDR, “Intended purpose” means the use for which a device is intended according to the data supplied by the manufacturer on the label, in the instructions for use or in promotional or sales materials or statements or as specified by the manufacturer in the performance evaluation;4

# Accessory:

According to Regulation (EU) 2017/745 – MDR, “Accessory for a medical device” means an article which, whilst not being itself a medical device, is intended by its manufacturer to be used together with one or several particular medical device(s) to specifically enable the medical device(s) to be used in accordance with its/their intended purpose(s) or to specifically and directly assist the medical functionality of the medical device(s) in terms of its/their intended purpose(s);5

According to Regulation (EU) 2017/746 – IVDR, “Accessory for an in vitro diagnostic medical device” means an article which, whilst not being itself an in vitro diagnostic medical device, is intended by its manufacturer to be used together with one or several particular in vitro diagnostic medical device(s) to specifically enable the in vitro diagnostic medical device(s) to be used in accordance with its/their intended purpose(s) or to specifically and directly assist the medical functionality of the in vitro diagnostic medical device(s) in terms of its/their intended purpose(s);6

Note: Software accessory may be driving or influencing the use of a medical device.

Note: Manufacturers must describe in the technical documentation accessories of a medical device or an in vitro diagnostic medical device which are intended to be used in combination with it; and in case

1 The use of “The Medical Devices Regulations” from here on out refers to both Regulation (EU) 2017/745 – MDR and 2 Regulation (EU) 2017/746 – IVDR.

It shall be noted that the term “standalone software” which was used in the text of the medical device directives, is no longer used in the context of the Medical Device Regulation. The rationale of the change is that software should be qualified and classified depending on its intended purpose uniquely, regardless of its location.

4 Article 2(12) of Regulation (EU) 2017/745 – MDR

5 Article 2(12) of Regulation (EU) 2017/746 – IVDR

6 Article 2(2) of Regulation (EU) 2017/745 – MDR

Article 2(4) of Regulation (EU) 2017/746 – IVDR
# Placing on the market:

According to Regulation (EU) 2017/745 – MDR, “Placing on the market” means the first making available of a device, other than an investigational device, on the Union market; 8

According to Regulation (EU) 2017/746 – IVDR, “Placing on the market” means the first making available of a device, other than a device for performance study, on the Union market; 9

# Putting into service:

According to Regulation (EU) 2017/745 – MDR, “Putting into service” means the stage at which a device, other than an investigational device, has been made available to the final user as being ready for use on the Union market for the first time for its intended purpose; 10

According to Regulation (EU) 2017/746 – IVDR, “Putting into service” means the stage at which a device, other than a device for performance study, has been made available to the final user as being ready for use on the Union market for the first time for its intended purpose; 11

# Medical device:

“medical device” means any instrument, apparatus, appliance, software, implant, reagent, material or other article intended by the manufacturer to be used, alone or in combination, for human beings for one or more of the following specific medical purposes:

- diagnosis, prevention, monitoring, prediction, prognosis, treatment or alleviation of disease,
- diagnosis, monitoring, treatment, alleviation of, or compensation for, an injury or disability,
- investigation, replacement or modification of the anatomy or of a physiological or pathological process or state,
- providing information by means of in vitro examination of specimens derived from the human body, including organ, blood and tissue donations,

and which does not achieve its principal intended action by pharmacological, immunological or metabolic means, in or on the human body, but which may be assisted in its function by such means.

The following products shall also be deemed to be medical devices:

- devices for the control or support of conception;
- products specifically intended for the cleaning, disinfection or sterilisation of devices as referred to in Article 1(4) and of those referred to in the first paragraph of this point. 12

# Active medical device:

“active device” means any device, the operation of which depends on a source of energy other than that generated by the human body for that purpose, or by gravity, and which acts by changing the density of or converting that energy. Devices intended to transmit energy, substances or other elements between an active device and the patient, without any significant change, shall not be deemed to be active devices. Software shall also be deemed to be an active device; 13

7 Article 32.2(c), Annex I, Chapter III Section 23.4(f), Annex II Section 1.1(h) of Regulation (EU) 2017/745 – MDR Article 829.2(c) and Annex II Section 1.1(m) of Regulation (EU) 2017/746 – IVDR

9 Article 2(28) of Regulation (EU) 2017/745 – MDR

10 Article 2(21) of Regulation (EU) 2017/746 – IVDR

11 Article 2(29) of Regulation (EU) 2017/745 – MDR

12 Article 2(22) of Regulation (EU) 2017/746 – IVDR

13 Article 2(1) of Regulation (EU) 2017/745 – MDR Article 2(4) of Regulation (EU) 2017/745 – MDR
# In vitro diagnostic medical device:

“In vitro diagnostic medical device” means any medical device which is a reagent, reagent product, calibrator, control material, kit, instrument, apparatus, piece of equipment, software or system, whether used alone or in combination, intended by the manufacturer to be used in vitro for the examination of specimens, including blood and tissue donations, derived from the human body, solely or principally for the purpose of providing information on one or more of the following:

- concerning a physiological or pathological process or state;
- concerning congenital physical or mental impairments;
- concerning the predisposition to a medical condition or a disease;
- to determine the safety and compatibility with potential recipients;
- to predict treatment response or reactions;
- to define or monitor therapeutic measures.

Specimen receptacles shall also be deemed to be in vitro diagnostic medical devices;14

# Software:

For the purpose of this guidance, “software” is defined as a set of instructions that processes input data and creates output data.

# Input data:

Any data provided to software in order to obtain output data after computation of this data can be considered as input data. Input data examples (non-exhaustive):

- Data given through the use of a human data-input device such as a keyboard, mouse, stylus, or touch screen;
- Data given through speech recognition;
- Digital document: formatted for general purpose such as Word file or pdf file or jpeg image, formatted for medical purpose such as DICOM file or ECG records or Electronic Health Record, unformatted document. Note that digital documents have to be differentiated from software able to read such documents;
- Data received from/transmitted by devices.

# Output data:

Any data produced by a software can be considered as an output data. Output data examples (non-exhaustive):

- Screen display data (such as layout with number, characters, picture, graphics, etc.);
- Print data (such as layout with number, characters, picture, graphics, etc.);
- Audio data;
- Digital document (formatted for a general purpose such as Word file or pdf file or jpeg image, or formatted for medical purpose such as DICOM file or ECG records or Electronic Health Record, unformatted document).
- Haptic buzzing as an alternative to audio sound.

# Software driving or influencing the use of a device

Software which is intended to drive or influence the use of a (hardware) medical device and does not have or perform a medical purpose on its own, nor does it create information on its own for one or more of the medical purposes described in the definition of a medical device or an in vitro diagnostic medical device. This software can, but is not limited to:

- (a) operate, modify the state of, or control the device either through an interface (e.g., software, hardware) or via the operator of this device;
- (b) or supply output related to the (hardware) functioning of that device.

Note: Software driving or influencing the use of a (hardware) medical device may be qualified as an accessory for a (hardware) medical device.

14 Article 2(2) of Regulation (EU) 2017/746 – IVDR
# Medical Device Software (MDSW)

Medical device software is software that is intended to be used, alone or in combination, for a purpose as specified in the definition of a “medical device” in the medical devices regulation15 or in vitro diagnostic medical devices regulation16.

# 3. Qualification

# 3.1. Introduction to qualification criteria

The purpose of this section is to clarify what software is in itself subject to the medical devices regulations.

Software must have a medical purpose on its own to be qualified as a medical device software (MDSW). It should be noted that the intended purpose as described by the manufacturer of the software is relevant for the qualification and classification of any device.

In order to be qualified as medical device software, the product must first fulfil the definition of software according to this guidance and the definition of a medical device according to Article 2(1) of Regulation (EU) 2017/745 – MDR. To be qualified as an in vitro diagnostic medical device software, the product must additionally fulfil the definition of an in vitro diagnostic medical device according to Article 2(2) of Regulation (EU) 2017/746 – IVDR.

Where a given product does not fall under the definition of a medical device, or is excluded by the scope of the Medical Devices Regulations, other Community and/or national legislation may be applicable. Software that does not meet the definition of a medical device or an in vitro diagnostic medical device (i.e. software that is not MDSW) but is intended by the manufacturer to be an accessory for a medical device, or an in vitro diagnostic medical device, falls respectively under the scope of the Regulation (EU) 2017/745 – MDR or Regulation (EU) 2017/746 – IVDR.

Software can directly control a (hardware) medical device (e.g. radiotherapy treatment software), can provide immediate decision-triggering information (e.g. blood glucose meter software), or can provide support for healthcare professionals (e.g. ECG interpretation software).

It is important to clarify that not all software used within healthcare is qualified as a medical device. For example, “Simple search”, which refers to the retrieval of records by matching record metadata against record search criteria or to the retrieval of information does not qualify as medical device software (e.g. library functions).

However, software which is intended to process, analyse, create or modify medical information may be qualified as a medical device software if the creation or modification of that information is governed by a medical intended purpose. For example, the software which alters the representation of data for a medical purpose would qualify as a medical device software. (e.g. “searching image for findings that support a clinical hypothesis as to the diagnosis or evolution of therapy” or “software which locally amplifies the contrast of the finding on an image display so that it serves as a decision support or suggests an action to be taken by the user”). However, altering the representation of data for embellishment/cosmetic or compatibility purposes does not readily qualify the software as medical device software.

Software intended for non-medical purposes (excluding MDR Annex XVI devices), such as invoicing or staff planning, does not qualify as a medical device software. These software do not fall under the Medical Devices Regulations.

15 Article 2(1) of Regulation (EU) 2017/745 – MDR

16 Article 2(2) of Regulation (EU) 2017/746 – IVDR
A task such as e-mailing, web or voice messaging, data parsing, word processing, and back-up is by itself not considered as having a medical purpose.

Additionally, software may run on different operating systems or in virtual environments. These operating systems or virtual environments do not impact the qualification criteria.

It must be highlighted that the risk of harm to patients, users of the software, or any other person, related to the use of the software within healthcare, including a possible malfunction is not a criterion on whether the software qualifies as a medical device.

# 3.2. Medical Device Software (MDSW)

Medical device software is software that is intended to be used, alone or in combination, for a purpose as specified in the definition of a “medical device” in the MDR or IVDR, regardless of whether the software is independent or driving or influencing the use of a device.

Note 1: MDSW may be independent, by having its own intended medical purpose and thus meeting the definition of a medical device or in vitro diagnostic medical device on its own (i.e. alone).

MDSW that uses maternal parameters such as age, concentration of serum markers and information obtained through foetal ultrasound examination for evaluating the risk of trisomy 21.

MDSW that receives measurements from transrectal ultrasound findings, age, and in vitro diagnostic instruments and calculates a patient’s risk of developing prostate cancer.

Mass Spectrometry MDSW intended to analyse LC-MS/MS data to be used for microorganism identification and detection of antibiotic resistance.

MDSW smartwatch app, which is intended to send alarm notifications to the user and/or health practitioner when it recognises irregular heartbeats for the purpose of detecting cardiac arrhythmia.

Note 2: If the software drives or influences a (hardware) medical device and also has a medical purpose, then it is qualified as a MDSW.

Melanoma image analysis software intended to drive a near-infrared laser light scanner.

MDSW intended to measure and transmit blood glucose levels, calculate insulin dose required and drive the insulin pump to administer the calculated dosage (closed loop insulin delivery system).

Note 3: Software may be qualified as MDSW regardless of its location (e.g. operating in the cloud, on a computer, on a mobile phone, or as an additional functionality on a hardware medical device).

MDSW that is intended to operate a point of care test from a remote location.

Note 4: MDSW may be intended to be used by healthcare professionals or laypersons (e.g. patients or other users).

MDSW that provides insulin dose recommendations to a patient regardless of the method of delivery of the prescribed dose, whether via an insulin pump, insulin pen or insulin syringe.

17 Where MDSW is intended to be used by a lay person, the manufacturer shall apply safety and performance requirements outlined in MDR Annex I. 22 and 23.4 (w); or IVDR Annex I. 9.4 and 20.4.2.

18 MDSW which can be considered as an IVD for self-testing shall be considered as a device intended to be used by laypersons.

Page 7 of 28
Manufacturers must ensure that all regulatory requirements for placing on the market and conformity assessment have been fulfilled. As set out in Article 7 of MDR and IVDR, this also entails that any claims, relating to the intended medical purpose of their MDSW are supported by clinical evidence. If this is not the case, the software would not meet the requirements of the regulations and therefore may not be CE marked as a medical device, nor present said claims.

# 3.3. ‘Software driving or influencing the use of a medical device’

Is software intended to drive or influence the use of a (hardware) medical device and does not have or perform a medical purpose on its own, nor does it create information on its own for one or more of the medical purposes described in the definition of a medical device or an in vitro diagnostic medical device. This software can, but is not limited to:

- a) operate, modify the state of, or control the device either through an interface (e.g., software, hardware) or via the operator of this device
- b) or supply output related to the (hardware) functioning of that device

Note: Software that is driving or influencing the use of a medical device is covered by the medical devices regulations either as a part/component of a device or as an accessory for a medical device. (refer to Figure 2, box 2).

Software that is intended to be used to operate a clinical chemistry analyser. Software with built-in electronic controls for IVD quality control procedures. These quality control procedures are intended to provide users with assurance that the device is performing within specifications.

# Decision steps for qualification of software as MDSW (Figure 1)

Decision step 1: if the product is software according to Section 2 (Definitions and Abbreviations) of this guidance, then it may be a medical device software, proceed to decision step 2; if the product is not software according to the definition of this guidance, then it is not covered by this guidance but may still be covered by the Medical Devices Regulations.

Decision step 2: if the product is an MDR Annex XVI device, or is an accessory for a medical device19, or is software driving or influencing the use of a medical device, then it must be considered as part of that device in its regulatory process or independently if it is an accessory. If it is not, proceed to decision step 3.

Decision step 3: if the software does perform an action on data, or performs an action beyond storage, archival, communication20, simple search, lossless compression (i.e. using a compression procedure that allows the exact reconstruction of the original data) then it may be a medical device software (Refer to section 3.1 for more guidance on these software functions) proceed to step 4.

Decision step 4: is the action for the benefit of individual patients? Examples of software which are not considered as being for the benefit of individual patients are those which are intended only to aggregate population data, provide generic diagnostic or treatment pathways (not directed to individual patients), scientific literature, medical atlases, models and templates as well as software intended only for epidemiological studies or registers.

Decision step 5: Is the software medical device software (MDSW) according to the definition of this guidance?

19 According to Article 2(2) of the Medical Devices Regulation or In Vitro Diagnostic Medical Devices Regulation.

20 Communication: The flow of information from one point, known as the source, to another, the receiver; Source: IEEE 610.10-1994.

Page 8 of 28
# Decision Steps to Assist Qualification of MDSW

Is the product 'Software' according to the definition of this guidance?

Not covered by this guidance

Is the software an 'MDR Annex XVI device' 'Accessory' for medical device according to Art. 2/2) of the MDR or IDR or 'software driving or influencing the use of (hardware) medical device'?

Is the software performing an action on data different from storage, archiving, communication or simple search?

Yes

Is the action for the benefit of individual patients?

Yes

The software is Medical Device Software (MDSW) according to the definition of this guidance.

Covered by the Medical Devices Regulations

Not covered by the Medical Devices Regulations*

Medical Devices Regulations* refers to the two Regulations (EU) 2017/746 on applicable regulations Regulation (EU) 2017/745 on Medical Devices (MDR) and IVDR

Page 9 of 28
# 3.4. Qualification criteria of MDSW as an in vitro diagnostic medical device

Medical Device Software (MDSW) fulfilling the definition of an in vitro diagnostic medical device falls under the in vitro diagnostic medical devices Regulation (EU) 2017/746. Provided that MDSW is intended specifically by its manufacturer to be used together with an in vitro diagnostic medical device to enable it to be used in accordance with its intended purpose, this MDSW falls under the scope of the in vitro diagnostic medical devices regulation and shall be treated as an In Vitro Diagnostic MDSW (IVD MDSW) in its own right.

In cases when software is driving or influencing the use of a (hardware) device, the software should be considered as falling under the respective regulation of the driven or influenced (hardware) device. Software that analyses and interprets the optical density delivered by an ELISA reader, line or spot pattern of a blot. Such software takes raw data outputs and use clinical algorithms for diagnostic and/or prognostic purposes, in which case it qualifies as IVD MDSW.

# Decision steps for qualification of MDSW as either a medical device or an in vitro diagnostic medical device (Figure 2)

# Decision Step 1:

Does the Medical Device Software (MDSW) provide information within the scope of the in vitro diagnostic medical device definition?

MDSW which provides information according to Regulation (EU) 2017/746 – IVDR Article 2(2) (a) to (f) should qualify as In Vitro Diagnostic Medical Device Software (IVD MDSW)

- (a) concerning a physiological or pathological process or state (by investigation of this process or state); or
- (b) concerning congenital physical or mental impairments
- (c) concerning the predisposition to a medical condition or a disease;
- (d) to determine the safety and compatibility with potential recipients;
- (e) to predict treatment response or reactions;
- (f) to define or monitoring therapeutic measures.

A MDSW which falls under the definition set out in EU Article 2 (1) of Regulation (EU) 2017/745 – MDR should qualify as Medical Device Software (MD MDSW). In specific, the following considerations should apply on the provision of information by software on:

- (g) diagnosis, prevention, monitoring, prediction, prognosis, treatment or alleviation of disease
- (h) diagnosis, monitoring, treatment, alleviation of, or compensation for, an injury or disability,
- (i) investigation, replacement or modification of the anatomy or of a physiological or pathological process or state,
- (j) control or support of conception;
- (k) products specifically intended for the cleaning, disinfection or sterilization of devices as referred to in Article 1(4) and Annex XVI products.

# Decision Step 2:

Does the MDSW create information based on data obtained by in vitro diagnostic medical devices only?

If the information provided is based on data obtained solely from in vitro diagnostic medical devices, then the software is an in vitro diagnostic medical device and is therefore an IVD MDSW. If the data analysed is obtained from a combination of both in vitro diagnostic medical devices and medical devices, proceed to step 3.

Page 10 of 28
# Decision Step 3

Is the intended purpose substantially driven by data sources coming from in vitro diagnostic medical devices? If yes, then the applicable legislation is Regulation (EU) 2017/746. If the intended purpose is substantially driven by data sources coming from medical devices, then the applicable legislation is Regulation (EU) 2017/745.

In the condition where the intended purpose of the MDSW output data fulfills both the medical device and in vitro diagnostic medical device definitions set out in the MDR and IVDR (refer to Decision Step 2), a weighting of the data sources based on the significance of the information 21 in relation to fulfilling the intended purpose should be conducted to aid the manufacturer in determining which regulation to apply.

Annex II of this guidance offers some prescriptive examples of how such a weighting may be performed.

# Medical Device Software (MDSW) according to the definition of this guidance

Does the MDSW provide information within the MD definition?

Does the MDSW provide information based on data obtained by a medical device?

Is the intended purpose substantially driven by data sources coming from:

Covered by Regulation (EU) 2017/746 (IVDR)
Covered by Regulation (EU) 2017/745 (MDR)

Figure: Decision steps to assist qualification of MDSW as either an In Vitro Diagnostic Medical Device Software (IVD MDSW) or a Medical Device Software (MD MDSW)

21 A qualitative approach is intended to drive the weighting of data. The weighing aims to assess the contribution of each data towards achieving the result.

Page 11 of 28
# 4. Classification of MDSW per MDR 2017/745

# 4.1. Implementing Rules

All implementing rules in Annex VIII of Regulation (EU) 2017/745 shall be considered. Special considerations on Implementing Rule 3.3 and 3.5:

The first sentence of implementing rule 3.3 of Annex VIII clarifies the regime applicable to software driving or influencing the use of a device:

‘Software, which drives or influences the use of a device, shall fall within the same class as the device’

The second sentence of implementing rule 3.3 of Annex VIII clarifies that the regime applicable to Independent MDSW:

‘If software is independent of any other device, it shall be classified in its own right’

This rule should also be considered at least as an orientation for finding the correct (minimum) classification of software which is placed on the market in combination with a (hardware) medical device. Therefore, Medical Device Software that both achieves its own intended purpose and also drives or influences the use of a (hardware) device for a medical purpose is classified on its own, based on the intended purpose achieved. In such a case, however, the risk class shall not be lower than the risk class of the hardware medical device.

Implementing rule 3.5 of Annex VIII is relevant for all devices and states that:

‘If several rules, or if, within the same rule, several sub-rules, apply to the same device based on the device’s intended purpose, the strictest rule and sub-rule resulting in higher classification will apply’

Melanoma image analysis software intended to be used with a near-infrared laser light scanner, which is considered class IIa per Rule 10. The software “drives or influences the use of” the near-infrared laser light scanner as it is intended to take control of the scanner by letting it execute proprietary multi-exposure programs for the detection of melanoma. As such, implementing rule 3.3 applies. However, Rule 11 would also apply based on the intended medical purpose of the software e.g. cancer diagnosis. The MDSW would be classified as class III based on Rule 11 (see section Classification Rules) and per implementing rule 3.5 of Annex VIII.

# 4.2. Classification Rules

Rules 9, 10 and 12 mainly categorise the risks related to the exchange of energy/substances between the body and diagnostic or therapeutic active devices, taking into account the different healthcare situations (condition of patients). MDSW, in the majority of cases, does not (directly) relate to such risks. It relates to the consequences of indirect harm from failure to provide correct information.

Therefore, in line with Recital 5 of the Medical Device Regulation and international guidance from the IMDRF (International Medical Device Regulators Forum) 22, Rule 11 was introduced into the MDR and is intended to address the risks related to the information provided by an active device, such as MDSW. Rule 11, in particular, describes and categorises the significance of the information provided by the active device to the healthcare decision (patient management) in combination with the healthcare situation (patient condition).

As software is defined as an active device, for the classification of active (hardware) devices, which also includes MDSW providing information for patient management, Rules 9, 10, 11, 12, 13, 15 and

22 IMDRF is a voluntary group of medical device regulators from around the world who have come together to build on the strong foundational work of the Global Harmonization Task Force on Medical Devices (GHTF) and aims to accelerate international medical device regulatory harmonization and convergence.

Page 12 of 28
# 4.2.1. Rule 11 – Software for decisions with diagnosis or therapeutic purposes or software intended to monitor physiological processes

Rule 11 states:

Software intended to provide information which is used to take decisions with diagnosis or therapeutic purposes is classified as class IIa, except if such decisions have an impact that may cause:

- death or an irreversible deterioration of a person's state of health, in which case it is in class III; or
- a serious deterioration of a person's state of health or a surgical intervention, in which case it is classified as class IIb.

Software intended to monitor physiological processes is classified as class IIa, except if it is intended for monitoring of vital physiological parameters, where the nature of variations of those parameters is such that it could result in immediate danger to the patient, in which case it is classified as class IIb.

All other software is classified as class I.

The text of Rule 11 can be divided into what are essentially three sub-rules that are applied depending on the intended use/purpose of the MDSW:

- 11a: (3 first paragraphs of Rule 11) intended to provide information which is used to take decisions with diagnostic or therapeutic purposes;
- 11b: (Paragraph 4 of Rule 11) intended to monitor physiological processes or parameters;
- 11c: (Paragraph 5 of Rule 11) all other uses.

# Sub-rule 11a)

The wording “intended to provide information which is used to take decisions with diagnosis or therapeutic purposes” describes, in very general terms, the “mode of action” which is characteristic of all MDSW. Therefore, this sub-rule is generally applicable to all MDSW (excluding those MDSW that have no medical purpose).

Sub-rule 11a), states that MDSW (which is intended to provide information which is used to take decisions with diagnosis or therapeutic purposes) is classified as class IIa.

There are two exceptions from sub-rule 11a) that are mainly intended to apply a risk classification based on the significance of the provided information and the potential impact of an (incorrect) decision made using information from the MDSW. Accordingly, MDSW that is intended to provide information which is used to take decisions with diagnosis and therapeutic purposes, is at a higher risk class where such decisions, if based on incorrect information from the MDSW, are reasonably likely to have an impact that may cause:

1. death or an irreversible deterioration of a person's state of health, in which case it is in class III;
2. serious deterioration of a person's state of health or surgical intervention, in which case it is classified as class IIb.

Compare IMDRF/SaMD WG/N12FINAL:2014 which states that there are two major factors that provide adequate description of the intended use of software: A. - Significance of the information provided by the software to the healthcare decision and B. - State of the healthcare situation or patient condition.
The MDR contains several references to “serious deterioration of a person’s state of health” and “surgical intervention”, notably in the vigilance or clinical investigation context. Further horizontal guidance could be provided in the future and will be available at: https://ec.europa.eu/growth/sectors/medical-devices/new-regulations/guidance_en

Rule 11 was also introduced to mirror the regulatory guidance developed at international level and notably in the context of the International Medical Device Regulators Forum (IMDRF). The IMDRF framework for risk categorisation of software as a medical device (SaMD) (“IMDRF Risk Framework”) categorises the risk of software based on the combination of the significance of the information provided by the software to the healthcare decision and the healthcare situation or patient condition. IMDRF also developed a table for assisting operators in identifying the appropriate risk category for their own product.

Such a table could provide operators placing MDSW on the EU market with some useful indications on the risk class applicable to their products as a result of the application of Rule 11 of the MDR. For this purpose, a table is provided in Annex III to this document which lists the IMDRF risk categories and the possible corresponding MDR risk classes according to Rule 11 of the MDR. It must be noted that this table does not take into account MDSW which is Class I.

# Sub-rule 11b):

MDSW that is intended to monitor physiological processes will, under most circumstances, provide “information which is used to take decisions with diagnosis or therapeutic purposes and hence fall under sub-rule 11a. Sub-rule 11b) should therefore be considered as a specific rule for MDSW intended only for monitoring purposes. Sub-rule 11b) was introduced to ensure that MDSW which has the same intended purpose as (hardware) devices which would fall under rule 10, third indent, are in the same risk class.

However, this sub rule applies to MDSW intended to be used for monitoring any/all physiological processes and not just vital physiological processes (equivalent to rule 10, third indent). Vital physiological processes and parameters include, for example, respiration, heart rate, cerebral functions, blood gases, blood pressure and body temperature.

# Sub-rule 11c):

Sub-rule 11c) implies that all other MDSW is classified as class I.

# 4.2.2. Rule 12 – Active devices intended to administer and/or remove substances

As software devices cannot physically administer and/or remove substances, please refer to the implementation rule 3.3 of Annex VIII for MDSW covered by this rule.

# 4.2.3. Rule 13 – All other active devices

Taking into consideration all implementing and classification rules applicable to active devices, if no other rule applies, all other active devices are class I.

# 4.2.4. Rule 15 - Devices used for contraception

Rule 15 applies to devices used for contraception or prevention of the transmission of sexually transmitted diseases. Software used for contraception will be classified as class IIb.

Specific implementation or classification rules for active Annex XVI devices (which might also include software) are expected to be provided together with the relevant Common Specifications for those devices.
# 4.2.5. Rule 22 – Closed loop systems

Active therapeutic devices with an integrated or incorporated diagnostic function which significantly determines the patient management by the device, such as closed loop systems or automated external defibrillators, are classified as class III.

See also implementing rule 3.3 for MDSW covered by this rule.

Further horizontal Guidance on the application of MD classification and implementing rules can be found at https://ec.europa.eu/growth/sectors/medical-devices/new-regulations/guidance_en. This is expected to provide useful orientation in relation to the application of non-software specific classification rules.

# 5. Classification and implementing rules per IVDR 2017/746

# 5.1. Implementing Rules:

All implementing rules in Annex VIII of Regulation (EU) 2017/746 shall be considered.

Special considerations on Implementing Rule 1.4 and 1.9:

Implementing rule 1.4 is only applicable for software which drives or influences the use of an in vitro diagnostic medical device. This rule should also be considered at least as an orientation for finding the right (minimum) classification of software which is placed on the market in combination with a (hardware) medical device.

According to the second sentence of implementing rule 1.4, if the software is independent of any other device, it shall be classified in its own right.

Examples for applying this implementing rule under the in vitro diagnostic medical devices regulation:

- Software that is exclusively intended to drive or influence the use of an instrument intended by the manufacturer specifically to be used for in vitro diagnostic procedures is classified in the same class as the instrument.
- A software that is intended to operate (driving) a C-reactive protein (CRP) measuring analyser from a remote location is classified in the same class as the analyser i.e. if the analyser is classified as class A then the software operating the analyser falls into Class A.
- MDSW that integrates genotype of multiple genes to predict risk a disease or medical condition developing or recurring; this is an independent IVD MDSW and is classified on its own.

Implementing rule 1.9 states that if several classification rules apply to the same device based on the devices’ intended purpose, the rule resulting in higher classification will apply. To classify In Vitro Diagnostic Medical Device Software (IVD MDSW) which is independent of any other device, see the MDCG Guidance on Classification of IVDs when available at https://ec.europa.eu/growth/sectors/medical-devices/new-regulations/guidance_en.

# 5.2. Classification Rules:

In determining the proper classification of MDSW under the IVDR, the manufacturer shall consider all classification and implementing rules of Annex VIII of the IVD Regulation (EU) 2017/746.

As spelled out by Implementing Rule 1.1 of Annex VIII of Regulation (EU) 2017/746, the application of the classification rules shall be governed by the intended purpose of the MDSW.
Guidance on the application of the IVD classification and implementing rules can be found at https://ec.europa.eu/growth/sectors/medical-devices/new-regulations/guidance_en25

# Examples for the classification of MDSW under the IVDR:

- Software intended to be installed on a fully automated enzyme-linked immunosorbent assay (ELISA) analyser, and intended to determine the Human HbA1c concentration in serum from the results obtained with a Human HbA1c ELISA, intended to screen for and diagnose diabetes and monitor diabetic patients, should be in class C per Rule 3(k).
- Software within a PAP stain automated cervical cytology screening system, intended to classify the PAP cervical smear as either normal or suspicious, should be in class C per Rule 3(h).
- Software for the interpretation of automated readings of line immunoassay for the confirmation and determination of antibodies to HIV-1, HIV-1 group O and HIV-2 in human serum and plasma, should be in class D per Rule 1.
- Software that uses maternal parameters such as age, concentration of serum markers and information obtained through foetal ultrasound examination for evaluating the risk of trisomy 21, should be in class C per Rule 3(l).

Classification examples in Annex IV are provided for guidance purposes and aim to illustrate how a particular rule may be applied to a device. The indicated classification in the example is not a confirmation of the final classification of the device, as other rules must also be considered.

# 6. Considerations on placing on the market and conformity assessment of MDSW

The type of interconnection between the MDSW and the device (e.g. embedded systems, wires, Wi-Fi, Bluetooth) does not affect the qualification of the software as a device under the MDR and IVDR (e.g. whether the software is incorporated in a device or is at a different location). However, MDSW can be placed on the market in two different ways: as a medical device or in-vitro diagnostic medical device in its own right or as an integral component or part of a hardware device.

# 6.1. Option 1: as a medical device in its own right

MDSW may be placed on the market or put into service in its own right.

- MDSW intended to be installed on a fully automated enzyme-linked immunosorbent assay (ELISA) analyser, and intended to determine the Human HbA1c concentration in serum from the results obtained with a Human HbA1c ELISA.
- MDSW app that provides a 10-year risk of cardiovascular disease from data input by a lay user.
- MDSW app that calculates anticoagulant dosage for patients in oral anticoagulant therapy, from INR test results input by IVD instruments and other manually entered patient data.
- MDSW app that analyses digital images of stained HEp-2 cell substrates from a microscope, for detecting antinuclear antibody (ANA) patterns to guide confirmatory testing useful in elucidating a specific clinical diagnosis or prognosis.

Conformity assessment:

25 Please note that at the time of the adoption of this document, the referenced Guidance on the application of IVDR classification and implementing rules was under finalisation.
# 6.2. Option 2: as an integral component/part of a device

MDSW may be placed on the market or put into service as an integral component/part of a device.

- MDSW contained within a blood gas analyser that enables a user to run tests on the instrument.
- MDSW that is part of a handheld hardware device intended for near-patient testing (POCT: point of care testing) for the determination of the blood glucose concentration.
- A fully automated enzyme-linked immunosorbent assay (ELISA) analyser, composed of hardware and MDSW, intended to determine the Human HbA1c concentration in serum from the results obtained with a Human HbA1c ELISA.
- MDSW that is part of a pulse oximeter intended to digitally filter the noise from low perfusion performance and motion artefacts, to calculate the ratio of red light/infrared light and to use a lookup table based on Beer-Lambert law to convert the ratio into the oxygen saturation in a person’s blood (SpO2).

# Conformity assessment:

MDSW that is placed on the market or put into service solely as an integral component/part of a (hardware) device may not have to undergo its own regulatory process. In this case, the MDSW shall be assessed through the regulatory process applied to the device as a whole, as it is placed on the market.

Applying the classification rules to these hardware devices, which is de-facto a combination of the hardware device and the MDSW, requires careful consideration of the intended purpose of the MDSW. This must also be analysed when later changes to the MDSW are done.

Note: MDSW could be independent under both scenarios described in 6.1 and 6.2, despite the presentation in which it is placed on the market.

# 7. Modules

Some medical device software may be segregated into a number of applications where each of these applications is correlated with a module. Some of these modules have a medical purpose, some not.

Such modules may be intended to cover many needs, e.g.:

- Collect and maintain administrative patient data;
- Keep on file the medical history of the patient;
- Invoicing and other accounting functions;
- Provide a link to the social security system for reimbursement;
- Provide a link to drug prescription systems (with possible link to drug dispensing outlets);
- Provide expert system assistance for medical decision making (e.g. radiotherapy dose planner).

Note: MDSW that is intended specifically to replace a part or component of a device and that significantly changes the performance or safety characteristics or the intended purpose of the device shall be considered to be a device and shall meet the requirements laid down in this Regulation (see Article 23.2 (2)).
This raises the issue as to whether the whole product can be CE marked when not all applications have a medical purpose. Computer programmes used in healthcare can have applications which consist of both medical device and non-medical device modules. The modules which are subject to the Medical Devices Regulations (figure 1 and 2) must comply with the requirements of the medical device regulations and must carry the CE marking. The non-medical device modules are not subject to the requirements for medical devices. It is the obligation of the manufacturer to identify the boundaries and the interfaces of the different modules. The boundaries of the modules which are subject to the medical device regulations should be clearly identified by the manufacturer based on the intended use.

If the modules which are subject to the medical device regulations are intended for use in combination with other modules of the whole software structure, other devices or equipment, the whole combination, including the connection system, must be safe and must not impair the specified performances of the modules which are subject to the medical device regulations.27

# 8. Consideration of changes to an MDSW

Manufacturers shall evaluate the potential impact of any changes to the function, intended use, essential design, and manufacturing characteristics on the software’s qualification as MDSW and its classification (including the classification of the combination of the MDSW with another medical device).

It is to be noted that a change to or the addition of functionality to a software may lead it to be qualified as MDSW, or a revision of the classification of the MDSW. Similarly, a module that is added to a software might be qualified as a MDSW on its own.

When determining the risk class of a combination of a modified MDSW and a medical device, the intended purpose and functionality of that (new) combination must be considered.

Note: For all MDSW, the manufacturer shall ensure safety and performance throughout the lifecycle of the software, through a continuous process of clinical and/or performance evaluation and risk management.

# 9. Annex I: Illustrative examples of qualification of software used in the healthcare environment

Software for a medical purpose is rapidly evolving. Thus, the list of examples provided below is not exhaustive. The examples have been drafted in light of today’s state of the art, in order to give the reader a better understanding of the application of the principles set out in the guideline. The Manual on borderline and classification in the Community regulatory framework for medical devices contains many examples related to qualification of software and apps, under the current.

27 i.e. general safety and performance requirements 14.1 of EU MDR 2017/745 and 13.1 of EU IVDR 2017/746
# Directives

The Manual is currently under revision for adaptation to MDRs. In light of the technological progress, further examples will be regularly published in both the Manual and in this guidance.

# a) Hospital Information Systems

Hospital Information Systems mean, in this context, systems that support the process of patient management. Typically they are intended for patient admission, for scheduling patient appointments, for insurance and billing purposes.

These Hospital Information Systems are not qualified as medical devices. However, they may be used with additional modules, as described hereafter. These modules might be qualified in their own right as medical devices.

# b) Decision Support Software

In general, these are computer based tools which combine general medical information databases and algorithms with patient-specific data. They are intended to provide healthcare professionals and/or users with recommendations for diagnosis, prognosis, monitoring and treatment of individual patients. Based on Figure 1, they are qualified as medical devices.

- Radiotherapy treatment planning systems are intended to calculate the dosage of ionizing irradiation to be applied to a specific patient. They are considered to control, monitor or directly influence the source of ionizing radiation and are qualified as medical devices.
- Drug planning systems (e.g. chemotherapy) are intended to calculate the drug dosage to be administered to a specific patient and therefore are qualified as medical devices.
- Computer Aided Detection systems are intended to provide information that may suggest or exclude medical conditions are qualified as medical devices (MDSW). For example, such systems would be able to automatically analyse x-ray images or interpret ECGs.

# c) Information Systems

Information Systems that are intended only to transfer, store, convert, format, archive data are not qualified as medical devices in themselves. However, they may be used with additional modules which may be qualified in their own right as medical devices (MDSW).

# c.1.) Electronic Patient Record Systems

Electronic patient record systems are intended to store and transfer electronic patient records. They archive all kinds of documents and data related to a specific patient. The electronic patient records should not be qualified as a medical device, i.e. an electronic patient record that simply replaces a patient’s paper file does not meet the definition of a medical device. The modules used with electronic patient record system modules that might be qualified in their own right as medical devices (MDSW) are for example:

- An image viewer with functionality for diagnosis based on digital images;
- A medication module

28 http://ec.europa.eu/Docsroom/documents/12867/attachments/1/translations/en/renditions/native

29 See EN 62083 “Requirements for the safety and radiotherapy treatment planning systems”

Page 19 of 28
# c.1.1.) Clinical Information Systems – CIS / Patient Data Management Systems – PDMS

A CIS/PDMS is a software-based system primarily intended to store and transfer patient information generated in association with the patient’s intensive care treatment (e.g. intensive care units). Usually the system contains information such as patient identification, vital intensive care parameters and other documented clinical observations. These CIS/PDMS are not qualified as medical devices. Modules that are intended to provide additional information that contributes to diagnosis, therapy and follow-up (e.g. generate alarms) are qualified as medical devices.

# c.1.2.) Pre-hospital Electrocardiograph (ECG) System

A system for managing pre-hospital ECG is a software-based system intended for ambulance services to store and transfer information from patients to a doctor at remote location. Usually the system contains information about patient identification, vital parameters and other documented clinical observations. These Pre-hospital Electrocardiograph (ECG) Systems are not qualified as medical devices. Modules that create and provide new patient treatment information to the paramedics or to the doctor at a remote location to start the patient’s treatment while the patient is being transported are qualified as medical devices.

# c.1.3.) Picture Archive Communication System (PACS)

The Manual on Borderline and Classification in the Community Regulatory Framework for Medical Devices addresses the qualification of PACS. The transposition of this Directive Guidance to the Regulations is currently underway and will be published at https://ec.europa.eu/growth/sectors/medical-devices/new-regulations/guidance_en

# d) Communication Systems

The healthcare sector uses communication systems (e.g. email systems, mobile telecommunication systems, video communication systems, paging, etc.) to transfer electronic information. Different types of messages are sent such as prescription, referrals, images, patient records, etc. Most of the communication systems handle types of messages other than medical information. This communication system is intended for general purposes, and is used for transferring both medical and non-medical information. Communication systems are normally based on software for general purposes, and do not fall within the definition of a medical device. Communication system modules might be used with other modules that might be qualified in their own right as medical devices (MDSW). A software module generating alarms based on the monitoring and analysis of patient specific physiological parameters is qualified as a medical device (MDSW).

# d.1) Telemedicine systems

Telemedicine Systems are intended to allow monitoring and/or delivery of healthcare to patients at locations remote from where the healthcare professional is located.

30 https://ec.europa.eu/docsroom/documents/35582/attachments/1/translations/en/renditions/native
# d.1.1.) Telesurgery

Telesurgery is intended to conduct a surgical procedure from a remote location. Virtual reality technology may be used to support a remote surgeon to control a surgical robot performing the surgical procedure.

Telesurgery systems should be qualified as medical devices according to Figure 2 of this document. Remote control software used in combination with telesurgery robots is a software that drives or influences the use of a medical device. Communication modules themselves are not medical devices. Other modules that are intended to influence the surgery procedure are qualified as medical devices (MDSW).

# e) Web systems for monitoring of data

A web system for the monitoring of clinical data typically interacts with a medical device (e.g. implanted devices or homecare devices), and uses a transmitter to send the information over the internet, a landline telephone or a mobile network.

The information is collected and stored on a web server usually run by an external party who is generally the manufacturer of the system. The information can be reached by authorized health professionals or the patient through an internet connection.

- Monitoring of performance of medical devices:
Modules that are intended to monitor the medical performance of medical devices fall under the medical device regulations. This includes the clinical performance and failures that could affect medical performance of the device. One example of such a product is a web system for monitoring of active implants such as pacemakers or Intra Cardiac Defibrillators (ICDs).
- Monitoring of non-medical performance of medical devices:
Modules that are intended to perform administrative monitoring of non-medical performance of medical devices do not necessarily fall under the scope of the medical devices regulations.

Software for the monitoring of medical devices in hospital systems for the purpose of maintenance and repair.

# f) In vitro diagnostic medical device software

# f.1.) Laboratory Information Systems (LIS) and Work Area Managers (WAM)

Laboratory Information System (LIS) and Work Area Managers (WAM) mean, in this context, systems that support the process from patient sample to patient result. Typically, they have pre-analytical functions for ordering, sorting and distribution of test samples.

The main task is the management and validation of incoming information obtained from in vitro diagnostic medical device analysers connected to the system, such as calibration, quality control, product expiry and feedback (e.g. retesting of samples needed) through interconnections with various analytical instruments (technical and clinical validation).

Finally the post-analytical process allows communication of laboratory results, statistics and optional reporting to external databases.

The software normally supports the following functions:

- Ordering of laboratory tests, samples with labels and sorting;
- Technical and clinical validation, connection to analytic instruments;
- Laboratory results and reports on paper, fax or electronic records that can be directly returned to e.g. the ordering clinic’s patient record;
- Analytical instruments can be interfaced with Hospital Information Systems (HIS), Electronic Patient Record Systems, Infectious control databases, etc.
Note: software intended to modify the representation of available in vitro diagnostic medical device results is not considered an in vitro diagnostic medical device, e.g. basic operations of arithmetic (e.g. mean, conversion of units) and/or plotting of results in function of time, and/or a comparison of the result to the limits of acceptance set by the user.

The results are available, readable and understandable without the intervention of the software. Laboratory Information Systems (LIS) and Work Area Managers (WAM) are not qualified as medical devices in themselves. However, they may be used with additional modules. These modules might be qualified in their own right as medical devices.

A module whose intended purpose is to assess the criticality of tests required and to perform automatic reprioritisation of the order based on patient data is qualified as a MDSW.

# f.2.) Expert system

MDSW which is intended to provide information within the scope of the in vitro diagnostic medical devices definition by capturing and analysing together one or multiple results obtained for one patient by means of in vitro examination of body samples (possibly combined with information from medical devices and non-medical devices).

- MDSW that integrates genotype of multiple genes to predict risk a disease or medical condition developing or recurring;
- MDSW that uses an algorithm to characterise viral resistances to various drugs, based on a nucleotide sequence generated by genotyping assays. This software serves to generate new information (virus resistance profile) from available information on the genotype of the virus;
- MDSW intended to be used in microbiology for the identification of clinical isolates and/or the detection of antimicrobial resistances.

Refer to Figure 2 of this guidance if data is obtained from both in vitro diagnostic medical devices and medical devices.

# f.3.) Interpretation of raw data

In the case where MDSW is necessary to render raw data, readable for the user, obtained from an in vitro diagnostic medical device by means of in vitro examination of body samples, this MDSW is to be considered driving or influencing the use of the in vitro diagnostic medical device when it is specifically intended to be used together with this in vitro diagnostic medical device to enable it to be used in accordance with its intended purpose.

MDSW intended for the analysis and interpretation of enzyme-linked immunosorbent assay (ELISA) reader optical density results, line patterns or spot patterns of a blot.

# f.4.) Home care monitoring, wired or mobile

Software intended for archiving patient results or for transferring results obtained from in vitro diagnostic medical devices from the home environment to the healthcare provider is not an in vitro diagnostic medical device. The results are available, readable and understandable by the user without the intervention of the software.

# f.5.) Image Management System (IMS)

An IMS is a software-based system primarily intended to be networked with digital pathology systems, e.g., whole slide scanners, scanning microscopes, as well as LIS. It does not contain controls for the direct operation of the digital pathology systems, and is intended to access, display, annotate, manage, store, archive and share collections of digitised patient images. IMS may be configured to

Page 22 of 28
provide limited or extensive capabilities to further visualise or analyse patient images acquired from networked digital pathology systems.

An IMS only used for viewing, archiving and transmitting images are not considered medical devices in themselves. However, these IMS may be used with additional modules that might be qualified in their own right as medical devices (MDSW).

IMS that incorporate functions to support post-processing of images for diagnostics purposes, e.g., image processing functions which alter image data or complex quantitative functions to aid in diagnosis, are qualified as MDSW.

Page 23 of 28
# 10. Annex II - Qualification examples of Medical Device Software (MDSW) according to Figures 1 and 2

# Figure 1 - Example 1:

A software module which runs on an in vitro diagnostic medical device instrument and tracks how the laboratory is performing in real-time on key operational metrics such as test volumes, turnaround times, pending tests, and quality control. Its intent is to improve a laboratory’s operations by providing real-time monitoring of performance metrics that can drive change management and continuous improvement initiatives within the lab. The software is configurable so that customers can choose the metrics on which they would like to focus.

Qualification: Step 1 is concluded with a “yes” as the software is a product which uses a set of instructions (or algorithm) to process input data and create output data. Step 2 determines that the software is not an MDR Annex XVI device, nor is it an accessory for a medical device, nor a software driving or influencing the use of a medical device. Step 3 is answered “yes” since the software is doing more than storage, archival, communication or simple search of information. Step 4 is answered “no” as the software does not perform this action for the benefit of individual patients. The conclusion is that the software does not fall under the Medical Devices Regulations. This is appropriate since the software is intended to be a Laboratory Information Systems (LIS), which is not considered a medical device.

# Figure 2 - Example 2:

MDSW intended to generate a risk score in order to trigger care processes to help reduce ICU transfers, readmissions, adverse events and length of stay. The risk score by default includes respiratory rate, heart rate, blood pressure and SpO2, but a user can configure it to include other parameters, including in vitro diagnostic medical device results.

Qualification: In decision Step 1, the MDSW can be understood to meet criteria (a), (f) and (h), it is therefore answered “yes”. Step 2 is answered with a “No” as an in vitro diagnostic medical device result may be included in the calculation. Step 3 directs the significance of the medical device derived information as driving the intended purpose, resulting in the qualification of the software as an MD MDSW (as the data received from the in vitro diagnostic medical device is not deemed decisive for the overall calculation result (output) achieved by the MDSW).

# Figure 3 - Example 3:

A MDSW algorithm intended to provide information on the statistical predisposition for Down syndrome (Trisomy 21) and Edwards syndrome (Trisomy 18) in the first and second trimesters of pregnancy. The MDSW analyses input data from various in vitro diagnostic medical device assays as well as ultrasound measurements of the nasal bone or neck fold. The MDSW provides clinicians/obstetricians with a risk factor score for a foetus’s likelihood of having genetic mutations in the first or second trimester of pregnancy. The risk score suggests whether or not additional diagnostic testing is needed to confirm the genetic mutations of Trisomy 21, Trisomy 18.

Qualification: Step 1 can be answered “yes” as the software bears a medical purpose and fulfils the definition of MDSW. The MDSW meets criteria (c) as it provides information according to the in vitro.

31 The software can also detect neural tube defects (NTD) in the second trimester as well as the risk for Patau’s syndrome (Trisomy 13).

32 AFP (LKAP, L2KAP), Unconjugated Estriol (LKUE3, L2KUE3), hCG (LKCG, L2KCG), free β-hCG (LKFB, L2KFB), PAPP A (LKPC, L2KPC)

33 or neural tube defects and Trisomy 13

Page 24 of 28
# Diagnostic Medical Devices Definition

Decision step 2 is answered “no” as an imaging measurement is included in the calculation. Step 3 is answered “yes” as the intended purpose is substantially driven by in vitro diagnostic medical device data resulting in the qualification of the software as an IVD MDSW (as the data received from the in vitro diagnostic medical devices (markers) are deemed decisive for the overall calculation result (output) achieved by the MDSW).

# Figure 2 - Example 4

A bioinformatics MDSW intended to analyse digital Next Generation Sequencing (NGS) raw data coming from sequenced patient’s cancer genomes. It allows the detection and visualisation of somatic genome alterations (such as substitutions, small insertions and deletions (indels), copy number alterations, and genomic rearrangements) across a selected number of genes. Additionally, it is also capable of determining genomic signatures* (such as microsatellite instability [MSI] and/or tumour mutational burden [TMB]). The types of somatic genome alterations and genomic signatures detected depend on the test chosen. The MDSW assists the user in identifying and visualising genomic alterations and is intended to identify somatic genome alterations to support diagnosis and treatment decisions.

# Qualification

Decision step 1 is concluded with a “yes” as the MDSW is intended for analysing congenital data to provide information on the predisposition to a medical condition or disease, thus meeting criteria (b) and (c) laid out in the decision step. As the MDSW processes data coming only from in vitro diagnostic medical devices into the calculation, then the software is qualified as an IVD MDSW according to Step 2.
# 11. Annex III - Usability of the IMDRF risk classification framework in the context of the MDR

The table below, which is intended for illustrative purposes only, may provide operators placing MDSW on the EU market with some useful indicative orientation on the risk class applicable to their products as a result of the application of Rule 11 a of the MDR.

Note: MDR 2017/745 Sub-rule 11(a), point i., referring above to MDR class III, aligns with IMDRF risk category IV. Sub-rule 11(a), point ii., referring above to MDR class IIb, aligns with IMDRF risk category III products mentioned in section 7.2 of the mentioned IMDRF document. The IMDRF risk category II and IMDRF risk category I products are classified as MDR class IIa as per Rule 11.

This table does not take into account MDSW which is Class I.

|Significance of Information provided by the MDSW to a healthcare situation related to diagnosis/therapy| |High|Medium|Low|
|---|---|---|---|---|
|Treat or diagnose|Drives clinical management|Informs clinical management (everything else)| | |
|Critical situation or patient condition|Class III|Class IIb|Class IIa| |
|Serious situation or patient condition|Class IIb|Class IIa|Class IIa| |
|Non-serious patient condition situation or (everything else)|Class IIa|Class IIa|Class IIa| |

Table 1: Classification Guidance on Rule 11

Annex III and IV are not relevant for IVD MDSW. See section 4.2 in order to classify IVD MDSW. MDCG Guidance on Classification of IVDs should also be considered.

Page 26 of 28
# 12. Annex IV – Classification examples

The examples are provided for guidance purposes only, to illustrate how a particular rule may be applied to a device. The indicated classification in the example is not a confirmation of the final classification of the device, as other rules might also be considered.

Moreover, the proposed classification reflects the specific intended purpose, or the healthcare context or situation, in which the device is used as described in the example itself. Any change to the intended purpose or the healthcare context/situation in which that same device is used might result in a different risk class.

- MDSW intended to perform diagnosis by means of image analysis for making treatment decisions in patients with acute stroke should be classified as class III under Rule 11(a)
- IMDRF Risk Category IV.i as the healthcare situation (stroke) is critical and the significance of the information is “treat or diagnose”.
- Cognitive therapy MDSW that includes a diagnostic function which is intended to feed back to the software to determine follow-up therapy, e.g. software adapts treatment of depression based on diagnostic feedback, should be in class III per Rule 22. When a specialist determines the necessary cognitive therapy based on the outcome provided by the MDSW, the MDSW would be classified as class IIa per Rule 11(a).
- IMDRF Risk Category II.ii as the healthcare situation is serious and the significance of the information is to “drive clinical management”.
- Medical devices including MDSW intended to be used for continuous surveillance of vital physiological processes in anaesthesia, intensive care or emergency care should be classified as class IIb per Rule 11(b).
- Medical devices, including MDSW intended to monitor physiological processes that are not considered to be vital, and devices intended to be used to obtain readings of vital physiological signals in routine check-ups including monitoring at home should be classified as class IIa per Rule 11(b).
- A mobile app intended to analyse a user’s heartbeat, detect abnormalities and inform a physician accordingly should be classified as class IIb per Rule 11(a), if the information provided by the software is intended to guide the physician in the diagnosis.
- IMDRF Risk Category III.i as the information drives clinical management.
- Diagnostic MDSW intended for scoring depression based on inputted data on a patient’s symptoms (e.g. mood, anxiety) should be classified as class IIb under Rule 11(a),
- (IMDRF Risk Category III.ii) as the healthcare situation (depression) is serious and the significance of the information is “diagnosis”.
- Ambulatory respiratory ventilation systems MDSW intended for long-term use (e.g. at home) that alert the user/operator to any disconnection or deviation to the programmed respiratory volume should be classified as class IIb per Rule 9.
- Active devices, such as electronic thermometers and stethoscopes, which include MDSW intended for direct diagnosis may be classified as class IIa per Rule 10, third indent since body temperature and heart rate are considered decisive information for diagnosis (implementing rule 3.7), where the nature of the variations of these parameters would not result in immediate danger to the patient.
- MDSW intended to rank therapeutic suggestions for a health care professional based on patient history, imaging test results, and patient characteristics, for example, MDSW that lists and ranks all available chemotherapy options for BRCA-positive individuals, should be classified as class IIa per Rule 11(a).

Page 27 of 28
# IMDRF Risk Category II.i

as it informs clinical management for cancer, a critical disease.

# MDSW App

intended to support conception by calculating the user’s fertility status based on a validated statistical algorithm. The user inputs health data including basal body temperature (BBT) and menstruation days to track and predict ovulation. The fertility status of the current day is reflected by one of three indicator lights: red (fertile), green (infertile) or yellow (learning phase/cycle fluctuation). This MDSW app should be classified as class I per Rule 11c.

Page 28 of 28
