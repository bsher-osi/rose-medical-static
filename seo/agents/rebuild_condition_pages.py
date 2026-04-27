#!/usr/bin/env python3
"""
Rebuild the main condition pages (/pediatric-epilepsy-phoenix/, etc.)
using the same clean template as city landing pages.

This replaces the heavy WordPress-exported HTML with a lightweight version
that has a working nav and footer.

Usage:
  python rebuild_condition_pages.py
  python rebuild_condition_pages.py --service pediatric-epilepsy-phoenix
  python rebuild_condition_pages.py --dry-run
"""

import argparse
import os
import sys
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config.yml")

SERVICE_CONTENT = {
    "pediatric-epilepsy-phoenix": {
        "intro": "Epilepsy is one of the most common neurological conditions in children, affecting approximately 1 in 150 kids. At Rose Medical Pavilion, Dr. Zach Rose MD provides comprehensive epilepsy diagnosis, management, and treatment plans tailored to each child in the Phoenix, AZ area.",
        "body": """
<h3>Signs &amp; Symptoms of Epilepsy</h3>
<p>Common signs of epilepsy in children include recurrent seizures, staring spells, sudden stiffening or jerking of the body, temporary confusion, and loss of awareness. Some children experience absence seizures that can be mistaken for daydreaming. Any unprovoked seizure warrants prompt neurological evaluation.</p>

<h3>Diagnosis</h3>
<p>Diagnosis begins with a detailed medical history and neurological examination. An EEG (electroencephalogram) is typically ordered to evaluate brain electrical activity. MRI may be recommended to look for structural causes. Dr. Zach Rose MD interprets all studies personally and discusses findings clearly with families.</p>

<h3>Treatment Options</h3>
<p>Treatment is individualized and may include anti-seizure medications, lifestyle modifications, and ongoing monitoring. Most children with epilepsy achieve good seizure control with appropriate medication. Dr. Zach Rose MD works closely with each family to balance seizure control with quality of life.</p>

<h3>Why Choose Rose Medical Pavilion?</h3>
<p>Dr. Zach Rose MD brings specialized expertise in pediatric epilepsy, using advanced diagnostic tools and evidence-based treatment protocols. Families throughout the Phoenix metro area — including Scottsdale, Chandler, Mesa, Tempe, and Gilbert — trust Rose Medical Pavilion for compassionate, expert neurological care.</p>
""",
    },
    "pediatric-seizures-phoenix": {
        "intro": "Seizures occur when abnormal electrical activity disrupts normal brain function. Dr. Zach Rose MD at Rose Medical Pavilion specializes in identifying the underlying cause of childhood seizures and creating targeted treatment plans for families throughout Phoenix, AZ.",
        "body": """
<h3>Types of Seizures in Children</h3>
<p>Seizure types include focal (partial) seizures, generalized tonic-clonic seizures, absence seizures, and febrile seizures. Accurate classification through EEG and clinical evaluation is essential for choosing the right treatment. Not all seizures are epilepsy — some are isolated events with excellent prognosis.</p>

<h3>What to Do During a Seizure</h3>
<p>Keep calm and keep your child safe. Place them on their side, clear the area of hazards, and time the seizure. Do not restrain them or put anything in their mouth. Call 911 if the seizure lasts more than 5 minutes, if another seizure follows immediately, or if your child does not recover normally.</p>

<h3>Evaluation and Diagnosis</h3>
<p>Dr. Zach Rose MD evaluates seizures through detailed history, neurological examination, EEG, and neuroimaging when indicated. Early, accurate diagnosis guides treatment and helps families understand what to expect going forward.</p>

<h3>Treatment</h3>
<p>Treatment depends on seizure type, frequency, and underlying cause. Options include anti-seizure medications, dietary therapy (ketogenic diet), and in some cases surgical evaluation. Dr. Zach Rose MD provides ongoing monitoring and adjusts treatment as your child grows.</p>
""",
    },
    "developmental-delays-phoenix": {
        "intro": "Developmental delays occur when a child does not reach expected milestones in areas such as speech, motor skills, social skills, or cognition. Early neurological evaluation can identify treatable causes and guide effective intervention for children throughout Phoenix, AZ.",
        "body": """
<h3>Types of Developmental Delays</h3>
<p>Delays can affect a single developmental domain (speech only, motor skills only) or multiple areas simultaneously. Global developmental delay involves significant delays across two or more domains. Identifying the pattern of delay guides the diagnostic workup and treatment plan.</p>

<h3>When to See a Neurologist</h3>
<p>Consider a pediatric neurology evaluation if your child is significantly behind peers on milestones, shows regression (losing previously acquired skills), or if your pediatrician recommends further evaluation. Earlier referral generally leads to better outcomes.</p>

<h3>Diagnostic Approach</h3>
<p>Evaluation includes detailed history, neurological examination, developmental screening tools, and targeted testing (genetic testing, metabolic studies, MRI, EEG) based on clinical findings. Dr. Zach Rose MD coordinates with therapists, schools, and other specialists as needed.</p>

<h3>Support and Resources in Arizona</h3>
<p>Arizona Early Intervention Program (AzEIP) provides free early intervention services for children under 3. The Arizona Division of Developmental Disabilities (DDD) supports older children. Dr. Zach Rose MD helps families navigate these resources and connect with the right support services.</p>
""",
    },
    "pediatric-headaches-phoenix": {
        "intro": "Pediatric headaches and migraines are more common than many parents realize, affecting up to 10% of school-age children. Dr. Zach Rose MD at Rose Medical Pavilion provides comprehensive headache evaluation and management for children throughout Phoenix, AZ.",
        "body": """
<h3>Migraines vs. Tension Headaches</h3>
<p>Migraines in children often present differently than in adults — episodes may be shorter, more commonly bilateral, and accompanied by nausea, vomiting, and sensitivity to light and sound. Tension-type headaches are typically bilateral, pressing/tightening, and not aggravated by activity.</p>

<h3>Headache Red Flags</h3>
<p>Seek prompt evaluation for headaches that are sudden and severe ("thunderclap"), worsen with position changes, awaken your child from sleep, are accompanied by fever, stiff neck, or rash, or come with neurological symptoms such as weakness, vision changes, or altered consciousness.</p>

<h3>Diagnosis and Workup</h3>
<p>Most childhood headaches do not require neuroimaging. Dr. Zach Rose MD performs a thorough headache history and neurological examination. Brain MRI is ordered when red flags are present or the headache pattern is atypical.</p>

<h3>Treatment and Prevention</h3>
<p>Treatment includes acute medications for relief, preventive medications for frequent migraines, and lifestyle modifications (consistent sleep, hydration, regular meals, stress management). Arizona's heat can be a trigger — hydration strategies are specifically addressed for Phoenix families.</p>
""",
    },
    "cerebral-palsy-muscle-disease-phoenix": {
        "intro": "Cerebral palsy (CP) and muscle diseases (myopathies) affect a child's movement, muscle tone, and overall physical function. Dr. Zach Rose MD at Rose Medical Pavilion provides expert evaluation, therapy coordination, and long-term management for affected children in Phoenix, AZ.",
        "body": """
<h3>Understanding Cerebral Palsy</h3>
<p>Cerebral palsy is caused by injury to the developing brain, most often occurring before or during birth. It is the most common physical disability in childhood. CP affects muscle tone, movement, and motor skills. It is non-progressive, meaning the brain injury itself does not worsen over time.</p>

<h3>Types of CP</h3>
<p>Spastic CP (most common) involves stiff, tight muscles. Dyskinetic CP involves uncontrolled movements. Ataxic CP affects balance and coordination. Many children have mixed types. Early classification guides therapy and treatment decisions.</p>

<h3>Muscle Diseases in Children</h3>
<p>Myopathies and muscular dystrophies affect the muscles directly, causing weakness, reduced muscle tone, and delayed motor milestones. Early genetic testing and multidisciplinary management improve outcomes significantly.</p>

<h3>Our Approach</h3>
<p>Management is individualized and coordinated. Dr. Zach Rose MD works with physical therapists, occupational therapists, speech therapists, orthopedic specialists, and school teams. Treatment may include medications for spasticity, botulinum toxin injections, and coordination of adaptive equipment and school accommodations.</p>
""",
    },
    "movement-disorders-phoenix": {
        "intro": "Pediatric movement disorders — including tremors, dystonia, chorea, ataxia, and tics — can significantly impact a child's daily functioning and quality of life. Dr. Zach Rose MD at Rose Medical Pavilion provides expert evaluation and individualized treatment for children throughout Phoenix, AZ.",
        "body": """
<h3>Types of Movement Disorders</h3>
<p>Movement disorders are classified by the type of abnormal movement. Tremors are rhythmic, involuntary oscillations. Dystonia involves sustained or repetitive muscle contractions causing twisting postures. Chorea consists of brief, irregular, unpredictable movements. Ataxia refers to incoordination of voluntary movements.</p>

<h3>Causes</h3>
<p>Causes vary widely and include genetic conditions, autoimmune disorders, metabolic diseases, medications, and structural brain abnormalities. Accurate diagnosis requires a systematic approach — a thorough history, examination, and targeted testing.</p>

<h3>Diagnosis</h3>
<p>Dr. Zach Rose MD evaluates movement disorders through detailed neurological examination, video documentation of abnormal movements, and targeted laboratory and imaging studies. Genetic testing is frequently informative for childhood-onset movement disorders.</p>

<h3>Treatment</h3>
<p>Treatment is condition-specific and may include medications to reduce abnormal movements, physical and occupational therapy, and — for select conditions — deep brain stimulation (coordinated with neurosurgery). Dr. Zach Rose MD provides ongoing follow-up and adjusts treatment as the child grows.</p>
""",
    },
    "tic-disorders-phoenix": {
        "intro": "Tic disorders, including Tourette syndrome, are among the most common neurological conditions in school-age children. Dr. Zach Rose MD at Rose Medical Pavilion provides compassionate, evidence-based evaluation and treatment for children with tic disorders throughout Phoenix, AZ.",
        "body": """
<h3>What Are Tics?</h3>
<p>Tics are sudden, repetitive, non-rhythmic movements or sounds. Motor tics involve body movements (eye blinking, head jerking, shoulder shrugging). Vocal tics involve sounds (throat clearing, sniffing, words). Most children with tics have a provisional tic disorder that resolves within a year.</p>

<h3>Tourette Syndrome</h3>
<p>Tourette syndrome is diagnosed when a child has had both motor and vocal tics for more than one year, with onset before age 18. It is frequently associated with ADHD and OCD. With proper management, most children with Tourette syndrome lead full, productive lives.</p>

<h3>When to Seek Treatment</h3>
<p>Many children with mild tics do not require medication. Treatment is indicated when tics cause pain, interfere with daily activities, affect school performance, or cause significant social distress. The goal is improved quality of life, not necessarily elimination of all tics.</p>

<h3>Treatment Options</h3>
<p>Behavioral therapy (Comprehensive Behavioral Intervention for Tics — CBIT) is the first-line treatment for tics and is effective for many children. Medications are available for more severe cases. Dr. Zach Rose MD creates individualized plans and provides school advocacy letters when needed.</p>
""",
    },
    "sleep-disorders-children-phoenix": {
        "intro": "Sleep disorders in children affect brain development, behavior, learning, and emotional health. Dr. Zach Rose MD at Rose Medical Pavilion provides expert evaluation and treatment for childhood sleep disorders throughout Phoenix, AZ.",
        "body": """
<h3>Common Sleep Disorders in Children</h3>
<p>Neurologically relevant sleep disorders include restless leg syndrome (RLS), sleep-related epilepsy (seizures occurring during sleep), narcolepsy, and parasomnias such as sleepwalking and night terrors. Behavioral insomnia is also very common and can have neurological contributors.</p>

<h3>Signs Your Child May Have a Sleep Disorder</h3>
<p>Watch for: difficulty falling asleep, frequent night wakings, snoring or breathing pauses, leg discomfort at night, excessive daytime sleepiness, sudden muscle weakness with laughter or strong emotions (cataplexy), or unusual behaviors during sleep.</p>

<h3>Evaluation</h3>
<p>Dr. Zach Rose MD conducts thorough sleep evaluations including review of sleep diaries, targeted laboratory testing, and EEG when seizure activity is suspected. Polysomnography (overnight sleep study) is arranged when warranted.</p>

<h3>Treatment</h3>
<p>Treatment is tailored to the specific diagnosis. Sleep hygiene education is foundational for all patients. Medical treatment for RLS, narcolepsy, and sleep-related epilepsy is highly effective when the correct diagnosis is established.</p>
""",
    },
    "dizziness-vertigo-children-phoenix": {
        "intro": "Dizziness and vertigo in children are more common than often recognized and can arise from vestibular, neurological, or cardiovascular causes. Dr. Zach Rose MD at Rose Medical Pavilion provides systematic evaluation and targeted treatment for affected children in Phoenix, AZ.",
        "body": """
<h3>Types of Dizziness in Children</h3>
<p>Dizziness may be described as a spinning sensation (vertigo), lightheadedness, imbalance, or a general sense of unsteadiness. Vertigo in children is most commonly caused by benign paroxysmal vertigo of childhood (a migraine variant), vestibular migraine, or middle ear problems.</p>

<h3>Neurological Causes</h3>
<p>Central causes of dizziness require careful evaluation. These include posterior fossa tumors, demyelinating disease, and vascular conditions. Red flags include persistent vertigo, ataxia, double vision, headache, or hearing loss — all warrant prompt neurological evaluation.</p>

<h3>Evaluation</h3>
<p>Dr. Zach Rose MD performs a thorough history and neurological examination with specific focus on vestibular function, ocular movements, gait, and coordination. Targeted imaging and laboratory studies are ordered when indicated.</p>

<h3>Treatment</h3>
<p>Most causes of childhood dizziness respond well to treatment. Vestibular migraine is managed similarly to migraine. Benign paroxysmal vertigo typically resolves with age. Physical therapy with a vestibular specialist can be helpful for ongoing balance problems.</p>
""",
    },
    "traumatic-brain-injury-phoenix": {
        "intro": "Traumatic brain injury (TBI) in children ranges from mild concussion to severe injury requiring intensive care. Neurological follow-up is essential for monitoring recovery and guiding return to school and activities. Dr. Zach Rose MD at Rose Medical Pavilion serves TBI patients throughout Phoenix, AZ.",
        "body": """
<h3>Spectrum of TBI</h3>
<p>TBI severity is classified as mild (GCS 13–15), moderate (GCS 9–12), or severe (GCS ≤8). Most pediatric TBIs are mild (concussion). Even mild TBI can cause persistent symptoms requiring careful management. Moderate and severe TBI require coordinated multidisciplinary care.</p>

<h3>Common Symptoms</h3>
<p>Post-TBI symptoms include headache, dizziness, cognitive difficulties (memory, concentration, processing speed), emotional changes (irritability, anxiety, depression), sleep disturbances, and sensitivity to light and noise. Symptom profiles vary by injury severity and individual factors.</p>

<h3>Recovery and Rehabilitation</h3>
<p>Dr. Zach Rose MD provides ongoing TBI management including headache treatment, cognitive rehabilitation coordination, mood support, and management of post-traumatic epilepsy when it develops. Academic accommodations are arranged through school liaison letters.</p>

<h3>Arizona Resources</h3>
<p>Arizona has strong TBI rehabilitation resources. Dr. Zach Rose MD coordinates referrals to neuropsychology, physical medicine and rehabilitation, and school-based support services to optimize recovery for Phoenix area children and families.</p>
""",
    },
    "pediatric-concussion-phoenix": {
        "intro": "Concussion is a mild traumatic brain injury caused by a bump, blow, or jolt to the head. Proper evaluation and management by a pediatric neurologist helps ensure safe recovery and return to school and sports. Dr. Zach Rose MD serves concussion patients throughout Phoenix, AZ.",
        "body": """
<h3>Recognizing Concussion</h3>
<p>Symptoms include headache, dizziness, confusion, memory problems ("foggy" feeling), nausea, light and noise sensitivity, emotional changes, and sleep disturbances. Symptoms may appear immediately or develop over hours. Any suspected concussion in a child warrants prompt evaluation.</p>

<h3>Why Proper Management Matters</h3>
<p>Premature return to contact sports before full recovery increases the risk of second-impact syndrome — a potentially life-threatening condition. Evidence-based, graduated return-to-learn and return-to-play protocols significantly reduce this risk.</p>

<h3>Return-to-Learn and Return-to-Play</h3>
<p>Dr. Zach Rose MD follows current evidence-based protocols for academic accommodations and safe return to sports. Communication with school staff and coaches is facilitated through detailed letters outlining specific recommendations.</p>

<h3>When Symptoms Persist</h3>
<p>Post-concussion syndrome occurs when symptoms last beyond 4 weeks. Contributing factors include sleep dysfunction, anxiety, vestibular dysfunction, and cervicogenic pain. A multidisciplinary approach targeting each contributor achieves the best outcomes.</p>
""",
    },
    "nerve-injury-phoenix": {
        "intro": "Peripheral nerve injuries in children can result from birth trauma, accidents, compression, or underlying medical conditions. Early evaluation and appropriate management optimize recovery. Dr. Zach Rose MD at Rose Medical Pavilion provides expert nerve injury care in Phoenix, AZ.",
        "body": """
<h3>Types of Nerve Injuries</h3>
<p>Nerve injuries range from neuropraxia (temporary conduction block, fully reversible) to axonotmesis (axon damage with intact sheath) to neurotmesis (complete nerve division). Brachial plexus injuries from birth trauma are among the most common peripheral nerve injuries in children.</p>

<h3>Symptoms</h3>
<p>Symptoms depend on which nerve is affected and include weakness, paralysis, numbness, tingling, pain, and changes in reflexes in the affected area. Accurate localization guides targeted treatment and rehabilitation.</p>

<h3>Diagnosis</h3>
<p>Electrodiagnostic testing — electromyography (EMG) and nerve conduction studies (NCS) — is the gold standard for evaluating nerve injury severity and monitoring recovery. Dr. Zach Rose MD performs and interprets these studies in the context of the full clinical picture.</p>

<h3>Treatment and Recovery</h3>
<p>Treatment depends on injury type and severity. Most neuropraxias recover fully without intervention. Axonal injuries require physical and occupational therapy to maintain joint mobility and strengthen recovering muscles. Surgical evaluation is considered for complete nerve injuries that fail to show recovery.</p>
""",
    },
    "insomnia-children-phoenix": {
        "intro": "Childhood insomnia affects sleep initiation and maintenance, leading to daytime fatigue, behavioral problems, and academic difficulties. Dr. Zach Rose MD at Rose Medical Pavilion evaluates neurological contributors to insomnia and coordinates comprehensive care for children in Phoenix, AZ.",
        "body": """
<h3>Types of Insomnia in Children</h3>
<p>Behavioral insomnia of childhood is the most common type and includes sleep-onset association disorder (needing a parent present to fall asleep) and limit-setting disorder (resisting bedtime). Medical and neurological conditions — including ADHD, anxiety, RLS, and seizures — frequently contribute to insomnia.</p>

<h3>Impact of Poor Sleep</h3>
<p>Sleep is essential for brain development, memory consolidation, emotional regulation, and immune function. Chronic insomnia in children is associated with ADHD-like symptoms, learning difficulties, mood disorders, and behavioral problems. Treating insomnia often produces dramatic improvements across multiple domains.</p>

<h3>Evaluation</h3>
<p>Dr. Zach Rose MD evaluates neurological contributors through detailed sleep history, review of sleep logs, and targeted testing. EEG is ordered when nocturnal seizures are suspected. Referral to behavioral sleep medicine is coordinated when indicated.</p>

<h3>Treatment</h3>
<p>Behavioral interventions (CBT-I adapted for children) are first-line treatment for behavioral insomnia. Medical treatment addresses underlying conditions (RLS, seizures, ADHD). Sleep hygiene recommendations are tailored to Arizona's hot climate, which can disrupt sleep if bedrooms are not adequately cooled.</p>
""",
    },
    "syncope-loss-of-consciousness-phoenix": {
        "intro": "Syncope (fainting) and loss of consciousness in children require careful evaluation to distinguish benign causes from serious cardiac or neurological conditions. Dr. Zach Rose MD at Rose Medical Pavilion provides systematic evaluation for children throughout Phoenix, AZ.",
        "body": """
<h3>Common Causes of Syncope in Children</h3>
<p>The most common cause of childhood syncope is vasovagal syncope — a benign reflex response to triggers such as prolonged standing, heat, dehydration, pain, or emotional stress. Arizona's extreme heat significantly increases syncope risk, particularly during summer months when children are active outdoors.</p>

<h3>When to Be Concerned</h3>
<p>Red flags requiring urgent evaluation include syncope during exercise, syncope without warning, syncope with family history of sudden cardiac death, chest pain or palpitations before loss of consciousness, and syncope associated with neurological symptoms such as prolonged confusion, focal weakness, or abnormal movements.</p>

<h3>Distinguishing Syncope from Seizure</h3>
<p>This distinction is clinically important and can be challenging. Syncope typically involves a brief period of pallor, sweating, and lightheadedness before loss of consciousness. Brief convulsive movements can occur with syncope and do not always indicate a seizure. Dr. Zach Rose MD performs EEG and detailed history to clarify the diagnosis when needed.</p>

<h3>Evaluation and Management</h3>
<p>Evaluation includes neurological examination, EEG when seizure is suspected, ECG, and coordination with cardiology for exercise-triggered or high-risk syncope. Most children with vasovagal syncope respond well to increased salt and fluid intake, positional maneuvers, and avoidance of triggers.</p>
""",
    },
    "visual-disturbances-children-phoenix": {
        "intro": "Visual disturbances in children can arise from migraines, seizures, increased intracranial pressure, or other neurological conditions. Timely evaluation is essential. Dr. Zach Rose MD at Rose Medical Pavilion serves children with visual symptoms throughout Phoenix, AZ.",
        "body": """
<h3>Neurological Causes of Visual Symptoms</h3>
<p>Neurological causes of visual disturbances in children include visual aura of migraine (the most common cause), occipital lobe seizures, idiopathic intracranial hypertension (pseudotumor cerebri), optic neuritis, and — less commonly — tumors or vascular malformations.</p>

<h3>Visual Aura of Migraine</h3>
<p>Visual aura typically consists of zigzag lines, flickering lights, or scotomas (blind spots) that spread across the visual field over 20–30 minutes, followed by headache. Recognizing this pattern can be reassuring, though the first episode always warrants evaluation.</p>

<h3>Red Flags</h3>
<p>Seek prompt evaluation for sudden vision loss, persistent visual field defects, double vision (diplopia), vision changes with headache and nausea/vomiting (especially on waking), or visual symptoms accompanied by weakness, numbness, or altered consciousness.</p>

<h3>Evaluation and Treatment</h3>
<p>Dr. Zach Rose MD evaluates visual disturbances through detailed history, neurological and fundoscopic examination, and targeted imaging. Visual field testing and ophthalmology consultation are coordinated as needed. Treatment is directed at the underlying cause.</p>
""",
    },
    "brain-mri-children-phoenix": {
        "intro": "Pediatric brain MRI is the gold-standard imaging study for evaluating neurological conditions in children. Dr. Zach Rose MD at Rose Medical Pavilion orders, interprets, and discusses brain MRI results with families throughout Phoenix, AZ.",
        "body": """
<h3>When Is a Brain MRI Needed?</h3>
<p>Brain MRI is indicated for new or unexplained seizures, abnormal neurological findings on examination, suspected structural brain abnormalities, certain developmental delay patterns, unexplained headaches with red flags, and monitoring of known neurological conditions. Dr. Zach Rose MD provides clear guidance on when imaging adds value.</p>

<h3>What Brain MRI Can Show</h3>
<p>MRI provides detailed images of brain structure including gray and white matter, cortical organization, ventricles, blood vessels, and the brainstem and cerebellum. It can identify tumors, cortical dysplasia, malformations, demyelination, ischemia, and many metabolic conditions.</p>

<h3>What to Expect</h3>
<p>MRI is painless and does not use radiation. The study typically takes 30–60 minutes. Children must remain still — for young children or those with anxiety, sedation can be arranged. Dr. Zach Rose MD reviews results personally and explains findings in language families can understand.</p>

<h3>MRI vs. CT Scan</h3>
<p>MRI is generally preferred over CT for children because it provides superior brain detail without radiation exposure. CT may be used in emergencies when rapid evaluation is needed. Dr. Zach Rose MD orders the most appropriate study for each clinical situation.</p>
""",
    },
    "pediatric-eeg-phoenix": {
        "intro": "An EEG (electroencephalogram) is a non-invasive test that measures electrical activity in the brain. It is essential for diagnosing epilepsy and evaluating other neurological conditions. Dr. Zach Rose MD at Rose Medical Pavilion performs and interprets pediatric EEGs for children throughout Phoenix, AZ.",
        "body": """
<h3>What Is an EEG?</h3>
<p>An EEG records electrical brain activity through small electrodes placed on the scalp with conductive gel. The procedure is painless and takes approximately 30–60 minutes. Hair washing before the test helps ensure good electrode contact. No needles or electricity are used.</p>

<h3>What EEG Can Diagnose</h3>
<p>EEG is the primary tool for diagnosing epilepsy and classifying seizure types. It can also evaluate unexplained spells, assess brain function after brain injury, and detect abnormal electrical patterns that may guide treatment decisions.</p>

<h3>Preparing Your Child</h3>
<p>Wash hair the night before without using conditioner or styling products. For routine EEG, sleep deprivation the night before may be requested to increase the chance of capturing abnormal activity. Bring a favorite toy or book to help your child relax.</p>

<h3>Understanding Results</h3>
<p>A normal EEG does not rule out epilepsy — seizure activity may not occur during the recording window. Abnormal patterns help confirm epilepsy, classify seizure type, and guide treatment selection. Dr. Zach Rose MD reviews all EEGs personally and discusses results with families at the follow-up visit.</p>
""",
    },
    "tourette-syndrome-phoenix": {
        "intro": "Tourette syndrome is a neurological disorder characterized by repetitive, involuntary movements and vocalizations called tics. Dr. Zach Rose MD at Rose Medical Pavilion provides expert, compassionate care for children with Tourette syndrome throughout Phoenix, AZ.",
        "body": """
<h3>Understanding Tourette Syndrome</h3>
<p>Tourette syndrome (TS) is diagnosed when a child has had both multiple motor tics and at least one vocal tic for more than one year, with onset before age 18. TS is more common than often recognized, affecting approximately 1 in 160 school-age children. Boys are affected 3–4 times more often than girls.</p>

<h3>Associated Conditions</h3>
<p>Most children with TS have at least one co-occurring condition. ADHD occurs in approximately 60% of children with TS. OCD, anxiety, learning disabilities, and sleep problems are also common. Addressing these associated conditions is often as important as treating the tics themselves.</p>

<h3>Treatment</h3>
<p>Many children with mild tics do not require medication. Comprehensive Behavioral Intervention for Tics (CBIT) is an effective behavioral therapy and is the preferred first-line treatment for most children. Medications are available for more disabling tics. Dr. Zach Rose MD tailors treatment to each child's specific needs and goals.</p>

<h3>School and Social Support</h3>
<p>Dr. Zach Rose MD provides school advocacy letters explaining Tourette syndrome and requesting appropriate accommodations. Education of teachers, classmates, and family members reduces stigma and improves outcomes. Arizona has active TS support networks that Dr. Zach Rose MD can connect families with.</p>
""",
    },
}

PAGE_TEMPLATE = '''<!DOCTYPE html>
<html dir="ltr" lang="en-US" prefix="og: https://ogp.me/ns#">
<head><meta charset="UTF-8">
<link rel="profile" href="http://gmpg.org/xfn/11">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes">
<title>{title} | Rose Medical Pavilion</title>
<meta name="description" content="{description}">
<meta name="robots" content="max-image-preview:large">
<link rel="canonical" href="https://rosemedicalpavilion.com/{slug}/">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Rose Medical Pavilion">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} | Rose Medical Pavilion">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://rosemedicalpavilion.com/{slug}/">
<meta property="og:image" content="/wp-content/uploads/2026/04/IMG_0045.jpg">
<meta property="og:image:width" content="2400">
<meta property="og:image:height" content="2400">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
  {{"@type":"MedicalWebPage",
   "name":"{title} | Rose Medical Pavilion",
   "url":"https://rosemedicalpavilion.com/{slug}/",
   "description":"{description}",
   "about":{{"@type":"MedicalCondition","name":"{service_name}"}},
   "audience":{{"@type":"Patient"}},
   "specialty":"Pediatric Neurology",
   "dateModified":"{today}"}},
  {{"@type":"Physician","name":"Dr. Zach Rose MD",
   "url":"https://rosemedicalpavilion.com/about-us/",
   "telephone":"+16028927467",
   "medicalSpecialty":"Neurology",
   "worksFor":{{"@type":"MedicalClinic","name":"Rose Medical Pavilion",
     "address":{{"@type":"PostalAddress","streetAddress":"4045 E Bell Rd, Suite 131",
       "addressLocality":"Phoenix","addressRegion":"AZ","postalCode":"85032",
       "addressCountry":"US"}}}}}},
  {{"@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"Home","item":"https://rosemedicalpavilion.com/"}},
    {{"@type":"ListItem","position":2,"name":"{service_name} in Phoenix, AZ"}}
  ]}}
]}}
</script>
<link rel="dns-prefetch" href="//fonts.googleapis.com">
<link rel="dns-prefetch" href="//www.googletagmanager.com">
<link rel="stylesheet" href="/wp-includes/css/dist/block-library/style.min.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/plugins/contact-form-7/includes/css/styles.css?ver=6.1.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/framework/admin/assets/css/select2.min.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/style.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/modules.min.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/font-awesome/css/font-awesome.min.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/elegant-icons/style.min.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/ion-icons/css/ionicons.min.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/style_dynamic.css?ver=1704067333" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/modules-responsive.min.css?ver=6.9.4" type="text/css" media="all">
<link rel="stylesheet" href="/wp-content/themes/mediclinic/assets/css/style_dynamic_responsive.css?ver=1704067333" type="text/css" media="all">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Poppins%3A300%2C400%2C500%7COpen+Sans%3A300%2C400%2C500&subset=latin-ext&ver=1.0.0" type="text/css" media="all">
<script type="text/javascript" src="/wp-includes/js/jquery/jquery.min.js?ver=3.7.1"></script>
<script type="text/javascript" src="/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1"></script>
<script type="text/javascript" src="https://www.googletagmanager.com/gtag/js?id=GT-TX5XVLK" async></script>
<script type="text/javascript">
window.dataLayer = window.dataLayer || [];function gtag(){{dataLayer.push(arguments);}}
gtag("js", new Date());
gtag("config", "GT-TX5XVLK");
</script>
<link rel="stylesheet" href="/refresh.css">
</head>
<body class="page-template-default page wp-theme-mediclinic mkdf-core-2.0 mediclinic-ver-2.0 mkdf-grid-1200 mkdf-sticky-header-on-scroll-down-up mkdf-dropdown-animate-height mkdf-header-standard mkdf-menu-area-in-grid-shadow-disable mkdf-menu-area-border-disable mkdf-menu-area-in-grid-border-disable mkdf-logo-area-border-disable mkdf-logo-area-in-grid-border-disable mkdf-header-vertical-shadow-disable mkdf-header-vertical-border-disable mkdf-default-mobile-header mkdf-sticky-up-mobile-header wpb-js-composer js-comp-ver-6.7.0 vc_responsive" itemscope itemtype="http://schema.org/WebPage">
<div class="mkdf-wrapper">
<div class="mkdf-wrapper-inner">

<div class="mkdf-top-bar">
  <div class="mkdf-grid">
    <div class="mkdf-vertical-align-containers">
      <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
        <div class="widget widget_text mkdf-top-bar-widget"><div class="textwidget"><span style="font-weight:400;">Dr. Zach Rose MD</span></div></div>
      </div></div>
      <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
        <div class="widget mkdf-icon-info-widget"><div class="mkdf-info-icon clearfix mkdf-icon-info-icon-medium">
          <div class="mkdf-icon-info-icon"><a href="tel:+16028927467"><span class="mkdf-icon-shortcode mkdf-normal"><i class="mkdf-icon-ion-icon ion-android-call mkdf-icon-element" style="color:#005da8;font-size:15px"></i></span></a></div>
          <div class="mkdf-info-icon-content"><a href="tel:+16028927467"><span class="mkdf-info-icon-title-text" style="color:#6b6b6b;font-size:13px;font-weight:400">(602) 892-7467</span></a></div>
        </div></div>
        <div class="widget mkdf-icon-info-widget"><div class="mkdf-info-icon clearfix mkdf-icon-info-icon-medium">
          <div class="mkdf-icon-info-icon"><span class="mkdf-icon-shortcode mkdf-normal"><i class="mkdf-icon-ion-icon ion-ios-clock mkdf-icon-element" style="color:#005da8;font-size:15px"></i></span></div>
          <div class="mkdf-info-icon-content"><span class="mkdf-info-icon-title-text" style="color:#6b6b6b;font-size:13px;font-weight:400">Mon - Fri: 8:00AM - 4:00PM</span></div>
        </div></div>
        <div class="widget mkdf-icon-info-widget"><div class="mkdf-info-icon clearfix mkdf-icon-info-icon-medium">
          <div class="mkdf-icon-info-icon"><a href="mailto:info@rosemedicalpavilion.com"><span class="mkdf-icon-shortcode mkdf-normal"><i class="mkdf-icon-ion-icon ion-ios-email mkdf-icon-element" style="color:#005da8;font-size:20px"></i></span></a></div>
          <div class="mkdf-info-icon-content"><a href="mailto:info@rosemedicalpavilion.com"><span class="mkdf-info-icon-title-text" style="color:#6b6b6b;font-size:13px;font-weight:400">info@rosemedicalpavilion.com</span></a></div>
        </div></div>
      </div></div>
    </div>
  </div>
</div>

<header class="mkdf-page-header">
<div class="mkdf-menu-area mkdf-menu-right">
<div class="mkdf-grid">
<div class="mkdf-vertical-align-containers">
  <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
    <div class="mkdf-logo-wrapper">
      <a itemprop="url" href="/" style="height:auto;display:flex;align-items:center;">
        <img fetchpriority="high" itemprop="image" class="mkdf-normal-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="logo">
        <img itemprop="image" class="mkdf-dark-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="dark logo">
        <img itemprop="image" class="mkdf-light-logo" src="/wp-content/uploads/2017/04/logo-light.png" alt="light logo">
      </a>
    </div>
  </div></div>
  <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
    <nav class="mkdf-main-menu mkdf-drop-down mkdf-default-nav">
      <ul class="clearfix">
        <li class="menu-item narrow"><a href="/"><span class="item_outer"><span class="item_text">Home</span></span></a></li>
        <li class="menu-item menu-item-has-children has_sub narrow"><a href="/about-us/"><span class="item_outer"><span class="item_text">About Us</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
          <div class="second"><div class="inner"><ul>
            <li class="menu-item"><a href="/about-us/announcements/"><span class="item_outer"><span class="item_text">Announcements</span></span></a></li>
          </ul></div></div>
        </li>
        <li class="menu-item menu-item-has-children mkdf-active-item has_sub narrow"><a href="#"><span class="item_outer"><span class="item_text">Conditions We Treat</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
          <div class="second"><div class="inner"><ul>
            <li class="menu-item"><a href="/pediatric-epilepsy-phoenix/"><span class="item_outer"><span class="item_text">Epilepsy</span></span></a></li>
            <li class="menu-item"><a href="/pediatric-seizures-phoenix/"><span class="item_outer"><span class="item_text">Seizures</span></span></a></li>
            <li class="menu-item"><a href="/pediatric-headaches-phoenix/"><span class="item_outer"><span class="item_text">Headaches &amp; Migraines</span></span></a></li>
            <li class="menu-item"><a href="/developmental-delays-phoenix/"><span class="item_outer"><span class="item_text">Developmental Delays</span></span></a></li>
            <li class="menu-item"><a href="/tourette-syndrome-phoenix/"><span class="item_outer"><span class="item_text">Tourette Syndrome</span></span></a></li>
            <li class="menu-item"><a href="/cerebral-palsy-muscle-disease-phoenix/"><span class="item_outer"><span class="item_text">Cerebral Palsy &amp; Muscle Disease</span></span></a></li>
            <li class="menu-item"><a href="/movement-disorders-phoenix/"><span class="item_outer"><span class="item_text">Movement Disorders</span></span></a></li>
            <li class="menu-item"><a href="/tic-disorders-phoenix/"><span class="item_outer"><span class="item_text">Tic Disorders</span></span></a></li>
            <li class="menu-item"><a href="/pediatric-concussion-phoenix/"><span class="item_outer"><span class="item_text">Concussion</span></span></a></li>
            <li class="menu-item"><a href="/traumatic-brain-injury-phoenix/"><span class="item_outer"><span class="item_text">Traumatic Brain Injury</span></span></a></li>
            <li class="menu-item"><a href="/nerve-injury-phoenix/"><span class="item_outer"><span class="item_text">Nerve Injury</span></span></a></li>
            <li class="menu-item"><a href="/brain-mri-children-phoenix/"><span class="item_outer"><span class="item_text">Brain MRI</span></span></a></li>
            <li class="menu-item"><a href="/pediatric-eeg-phoenix/"><span class="item_outer"><span class="item_text">EEG Testing</span></span></a></li>
            <li class="menu-item"><a href="/visual-disturbances-children-phoenix/"><span class="item_outer"><span class="item_text">Visual Disturbances</span></span></a></li>
            <li class="menu-item"><a href="/dizziness-vertigo-children-phoenix/"><span class="item_outer"><span class="item_text">Dizziness &amp; Vertigo</span></span></a></li>
            <li class="menu-item"><a href="/syncope-loss-of-consciousness-phoenix/"><span class="item_outer"><span class="item_text">Syncope / Loss of Consciousness</span></span></a></li>
            <li class="menu-item"><a href="/insomnia-children-phoenix/"><span class="item_outer"><span class="item_text">Insomnia</span></span></a></li>
            <li class="menu-item"><a href="/sleep-disorders-children-phoenix/"><span class="item_outer"><span class="item_text">Sleep Disorders</span></span></a></li>
          </ul></div></div>
        </li>
        <li class="menu-item narrow"><a href="/blogs/"><span class="item_outer"><span class="item_text">Blog</span></span></a></li>
        <li class="menu-item narrow"><a href="/refer-a-patient/"><span class="item_outer"><span class="item_text">Refer a patient</span></span></a></li>
        <li class="menu-item narrow"><a href="/careers/"><span class="item_outer"><span class="item_text">Careers</span></span></a></li>
        <li class="menu-item menu-item-has-children has_sub narrow"><a href="https://www.onpatient.com/login/"><span class="item_outer"><span class="item_text">Patient Portal</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
          <div class="second"><div class="inner"><ul>
            <li class="menu-item"><a href="/wp-content/uploads/2025/03/Onpatient-portal-sign-up-directions.pdf"><span class="item_outer"><span class="item_text">Portal Sign-Up Instructions</span></span></a></li>
          </ul></div></div>
        </li>
        <li class="menu-item menu-item-has-children has_sub narrow"><a href="/contact-us/"><span class="item_outer"><span class="item_text">Contact Us</span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
          <div class="second"><div class="inner"><ul>
            <li class="menu-item"><a href="/schedule-online/"><span class="item_outer"><span class="item_text">Schedule Online</span></span></a></li>
          </ul></div></div>
        </li>
      </ul>
    </nav>
  </div></div>
</div>
</div>
</div>
<div class="mkdf-sticky-header">
  <div class="mkdf-sticky-holder">
    <div class="mkdf-vertical-align-containers">
      <div class="mkdf-position-left"><div class="mkdf-position-left-inner">
        <div class="mkdf-logo-wrapper">
          <a itemprop="url" href="/" style="height:auto;display:flex;align-items:center;">
            <img fetchpriority="high" itemprop="image" class="mkdf-normal-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="logo">
            <img itemprop="image" class="mkdf-dark-logo" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="dark logo">
            <img itemprop="image" class="mkdf-light-logo" src="/wp-content/uploads/2017/04/logo-light.png" alt="light logo">
          </a>
        </div>
      </div></div>
      <div class="mkdf-position-right"><div class="mkdf-position-right-inner">
        <nav class="mkdf-main-menu mkdf-drop-down mkdf-sticky-nav">
          <ul class="clearfix">
            <li class="menu-item narrow"><a href="/"><span class="item_outer"><span class="item_text">Home</span><span class="plus"></span></span></a></li>
            <li class="menu-item menu-item-has-children has_sub narrow"><a href="/about-us/"><span class="item_outer"><span class="item_text">About Us</span><span class="plus"></span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
              <div class="second"><div class="inner"><ul>
                <li class="menu-item"><a href="/about-us/announcements/"><span class="item_outer"><span class="item_text">Announcements</span><span class="plus"></span></span></a></li>
              </ul></div></div>
            </li>
            <li class="menu-item menu-item-has-children mkdf-active-item has_sub narrow"><a href="#"><span class="item_outer"><span class="item_text">Conditions We Treat</span><span class="plus"></span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
              <div class="second"><div class="inner"><ul>
                <li class="menu-item"><a href="/pediatric-epilepsy-phoenix/"><span class="item_outer"><span class="item_text">Epilepsy</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/pediatric-seizures-phoenix/"><span class="item_outer"><span class="item_text">Seizures</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/pediatric-headaches-phoenix/"><span class="item_outer"><span class="item_text">Headaches &amp; Migraines</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/developmental-delays-phoenix/"><span class="item_outer"><span class="item_text">Developmental Delays</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/tourette-syndrome-phoenix/"><span class="item_outer"><span class="item_text">Tourette Syndrome</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/cerebral-palsy-muscle-disease-phoenix/"><span class="item_outer"><span class="item_text">Cerebral Palsy &amp; Muscle Disease</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/movement-disorders-phoenix/"><span class="item_outer"><span class="item_text">Movement Disorders</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/tic-disorders-phoenix/"><span class="item_outer"><span class="item_text">Tic Disorders</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/pediatric-concussion-phoenix/"><span class="item_outer"><span class="item_text">Concussion</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/traumatic-brain-injury-phoenix/"><span class="item_outer"><span class="item_text">Traumatic Brain Injury</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/nerve-injury-phoenix/"><span class="item_outer"><span class="item_text">Nerve Injury</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/brain-mri-children-phoenix/"><span class="item_outer"><span class="item_text">Brain MRI</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/pediatric-eeg-phoenix/"><span class="item_outer"><span class="item_text">EEG Testing</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/visual-disturbances-children-phoenix/"><span class="item_outer"><span class="item_text">Visual Disturbances</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/dizziness-vertigo-children-phoenix/"><span class="item_outer"><span class="item_text">Dizziness &amp; Vertigo</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/syncope-loss-of-consciousness-phoenix/"><span class="item_outer"><span class="item_text">Syncope / Loss of Consciousness</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/insomnia-children-phoenix/"><span class="item_outer"><span class="item_text">Insomnia</span><span class="plus"></span></span></a></li>
                <li class="menu-item"><a href="/sleep-disorders-children-phoenix/"><span class="item_outer"><span class="item_text">Sleep Disorders</span><span class="plus"></span></span></a></li>
              </ul></div></div>
            </li>
            <li class="menu-item narrow"><a href="/blogs/"><span class="item_outer"><span class="item_text">Blog</span><span class="plus"></span></span></a></li>
            <li class="menu-item narrow"><a href="/refer-a-patient/"><span class="item_outer"><span class="item_text">Refer a patient</span><span class="plus"></span></span></a></li>
            <li class="menu-item narrow"><a href="/careers/"><span class="item_outer"><span class="item_text">Careers</span><span class="plus"></span></span></a></li>
            <li class="menu-item menu-item-has-children has_sub narrow"><a href="https://www.onpatient.com/login/"><span class="item_outer"><span class="item_text">Patient Portal</span><span class="plus"></span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
              <div class="second"><div class="inner"><ul>
                <li class="menu-item"><a href="/wp-content/uploads/2025/03/Onpatient-portal-sign-up-directions.pdf"><span class="item_outer"><span class="item_text">Portal Sign-Up Instructions</span><span class="plus"></span></span></a></li>
              </ul></div></div>
            </li>
            <li class="menu-item menu-item-has-children has_sub narrow"><a href="/contact-us/"><span class="item_outer"><span class="item_text">Contact Us</span><span class="plus"></span><i class="mkdf-menu-arrow fa fa-angle-down"></i></span></a>
              <div class="second"><div class="inner"><ul>
                <li class="menu-item"><a href="/schedule-online/"><span class="item_outer"><span class="item_text">Schedule Online</span><span class="plus"></span></span></a></li>
              </ul></div></div>
            </li>
          </ul>
        </nav>
      </div></div>
    </div>
  </div>
</div>
</header>

<header class="mkdf-mobile-header">
<div class="mkdf-mobile-header-inner">
  <div class="mkdf-mobile-header-holder">
    <div class="mkdf-grid">
      <div class="mkdf-vertical-align-containers">
        <div class="mkdf-mobile-menu-opener">
          <a href="javascript:void(0)"><span class="mkdf-mobile-menu-icon"><i class="fa fa-bars" aria-hidden="true"></i></span></a>
        </div>
        <div class="mkdf-position-center"><div class="mkdf-position-center-inner">
          <div class="mkdf-mobile-logo-wrapper">
            <a itemprop="url" href="/"><img itemprop="image" src="/wp-content/uploads/2023/11/Rose-Logo_ROSE-2.png" width="1201" height="1200" alt="Mobile Logo"></a>
          </div>
        </div></div>
      </div>
    </div>
  </div>
  <nav class="mkdf-mobile-nav" role="navigation" aria-label="Mobile Menu">
    <div class="mkdf-grid"><ul>
      <li class="menu-item"><a href="/"><span>Home</span></a></li>
      <li class="menu-item menu-item-has-children has_sub"><a href="/about-us/" class="mkdf-mobile-no-link"><span>About Us</span></a><span class="mobile_arrow"><i class="mkdf-sub-arrow fa fa-angle-right"></i><i class="fa fa-angle-down"></i></span>
        <ul class="sub_menu"><li><a href="/about-us/announcements/"><span>Announcements</span></a></li></ul>
      </li>
      <li class="menu-item menu-item-has-children has_sub"><a href="#" class="mkdf-mobile-no-link"><span>Conditions We Treat</span></a><span class="mobile_arrow"><i class="mkdf-sub-arrow fa fa-angle-right"></i><i class="fa fa-angle-down"></i></span>
        <ul class="sub_menu">
          <li><a href="/pediatric-epilepsy-phoenix/"><span>Epilepsy</span></a></li>
          <li><a href="/pediatric-seizures-phoenix/"><span>Seizures</span></a></li>
          <li><a href="/pediatric-headaches-phoenix/"><span>Headaches &amp; Migraines</span></a></li>
          <li><a href="/developmental-delays-phoenix/"><span>Developmental Delays</span></a></li>
          <li><a href="/tourette-syndrome-phoenix/"><span>Tourette Syndrome</span></a></li>
          <li><a href="/cerebral-palsy-muscle-disease-phoenix/"><span>Cerebral Palsy &amp; Muscle Disease</span></a></li>
          <li><a href="/movement-disorders-phoenix/"><span>Movement Disorders</span></a></li>
          <li><a href="/tic-disorders-phoenix/"><span>Tic Disorders</span></a></li>
          <li><a href="/pediatric-concussion-phoenix/"><span>Concussion</span></a></li>
          <li><a href="/traumatic-brain-injury-phoenix/"><span>Traumatic Brain Injury</span></a></li>
          <li><a href="/nerve-injury-phoenix/"><span>Nerve Injury</span></a></li>
          <li><a href="/brain-mri-children-phoenix/"><span>Brain MRI</span></a></li>
          <li><a href="/pediatric-eeg-phoenix/"><span>EEG Testing</span></a></li>
          <li><a href="/visual-disturbances-children-phoenix/"><span>Visual Disturbances</span></a></li>
          <li><a href="/dizziness-vertigo-children-phoenix/"><span>Dizziness &amp; Vertigo</span></a></li>
          <li><a href="/syncope-loss-of-consciousness-phoenix/"><span>Syncope / Loss of Consciousness</span></a></li>
          <li><a href="/insomnia-children-phoenix/"><span>Insomnia</span></a></li>
          <li><a href="/sleep-disorders-children-phoenix/"><span>Sleep Disorders</span></a></li>
        </ul>
      </li>
      <li class="menu-item"><a href="/blogs/"><span>Blog</span></a></li>
      <li class="menu-item"><a href="/refer-a-patient/"><span>Refer a patient</span></a></li>
      <li class="menu-item"><a href="/careers/"><span>Careers</span></a></li>
      <li class="menu-item"><a href="https://www.onpatient.com/login/"><span>Patient Portal</span></a></li>
      <li class="menu-item"><a href="/contact-us/"><span>Contact Us</span></a></li>
      <li class="menu-item"><a href="/schedule-online/"><span>Schedule Online</span></a></li>
    </ul></div>
  </nav>
</div>
</header>

<a id="mkdf-back-to-top" href="#"><span class="mkdf-icon-stack"><i class="mkdf-icon-ion-icon ion-chevron-up"></i></span></a>

<div class="mkdf-content">
  <div class="mkdf-content-inner">
    <div class="mkdf-title mkdf-standard-type mkdf-content-left-alignment mkdf-preload-background mkdf-has-background mkdf-title-image-not-responsive" style="height:200px;background-image:url(/wp-content/uploads/2017/04/blog-parallax-1.jpg);" data-height="200" data-background-width="&quot;1920&quot;">
      <div class="mkdf-title-image">
        <img itemprop="image" src="/wp-content/uploads/2017/04/blog-parallax-1.jpg" alt="Title Image">
      </div>
      <div class="mkdf-title-holder" style="height:200px;">
        <div class="mkdf-container clearfix">
          <div class="mkdf-container-inner">
            <div class="mkdf-title-subtitle-holder">
              <div class="mkdf-title-subtitle-holder-inner">
                <h1 class="mkdf-page-title entry-title"><span>{title}</span></h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mkdf-container mkdf-default-page-template">
      <div class="mkdf-container-inner clearfix">
        <div class="mkdf-grid-row">
          <div class="mkdf-page-content-holder mkdf-grid-col-12">

            <h2>{title}</h2>
            <p>{intro}</p>

            {body}

            <h3>Schedule a Consultation</h3>
            <p>If your child is experiencing symptoms of {service_name_lower}, early evaluation is key. Dr. Zach Rose MD provides compassionate, expert pediatric neurology care at Rose Medical Pavilion in Phoenix, AZ. Call <strong><a href="tel:+16028927467">(602) 892-7467</a></strong> or <a href="/schedule-online/">schedule online</a> today.</p>

          </div>
        </div>
      </div>
    </div>
  </div>
</div>

</div><!-- mkdf-wrapper-inner -->
</div><!-- mkdf-wrapper -->

<footer class="rose-footer">
  <div class="rose-footer-inner">
    <div class="rose-footer-col">
      <i class="ion-android-call rose-footer-icon"></i>
      <h4>Call</h4>
      <p>(602) 892-7467</p>
    </div>
    <div class="rose-footer-col">
      <i class="ion-location rose-footer-icon"></i>
      <h4>Location</h4>
      <p>4045 E Bell Rd, Suite 131<br>Phoenix, AZ 85032</p>
    </div>
    <div class="rose-footer-col">
      <i class="ion-calendar rose-footer-icon"></i>
      <h4>Request an appointment</h4>
      <p>info@rosemedicalpavilion.com</p>
      <a href="/schedule-online/" class="rose-footer-btn rose-footer-btn-coral">Schedule Online</a>
      <a href="/refer-a-patient/" class="rose-footer-btn rose-footer-btn-blue">Refer Patient</a>
    </div>
  </div>
  <div class="rose-footer-bottom">
    <p>&copy; 2026 Rose Medical Pavilion All Rights Reserved</p>
  </div>
</footer>

<script>
var mkdfPerPageVars = {{"vars":{{"mkdfStickyScrollAmount":0,"mkdfHeaderTransparencyHeight":0}}}};
if(typeof window.fluidvids === 'undefined') window.fluidvids = {{init:function(){{}}}};
(function($){{
  if($ && !$.fn.mediaelementplayer) $.fn.mediaelementplayer = function(){{return this;}};
  if($ && !$.fn.perfectScrollbar) $.fn.perfectScrollbar = function(){{return this;}};
}})(window.jQuery);
</script>
<script type="text/javascript" src="/wp-content/themes/mediclinic/assets/js/modules.min.js?ver=6.9.4"></script>
<script>
(function(){{
  var header = document.querySelector('.mkdf-page-header');
  var sticky = document.querySelector('.mkdf-sticky-header');
  if(!header || !sticky) return;
  var lastScroll = 0;
  var threshold = header.offsetHeight || 80;
  window.addEventListener('scroll', function(){{
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if(y > threshold){{
      if(y < lastScroll){{
        sticky.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:1000;display:block !important;transform:translateY(0);transition:transform .3s ease;box-shadow:0 2px 8px rgba(0,0,0,0.15);background:#fff;';
      }} else {{
        sticky.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:1000;display:none !important;';
      }}
    }} else {{
      sticky.style.cssText = 'display:none !important;';
    }}
    lastScroll = y;
  }}, {{passive:true}});
}})();
</script>
<script>
(function fixGap(){{
  function fix(){{
    var btt = document.getElementById("mkdf-back-to-top");
    if(btt) btt.parentNode.removeChild(btt);
    document.body.style.removeProperty("padding-bottom");
    document.body.style.removeProperty("margin-bottom");
    [".mkdf-wrapper",".mkdf-wrapper-inner",".mkdf-content",".mkdf-content-inner"].forEach(function(s){{
      var el = document.querySelector(s);
      if(el){{ el.style.removeProperty("height"); el.style.removeProperty("min-height"); }}
    }});
  }}
  document.addEventListener("DOMContentLoaded", fix);
  window.addEventListener("load", fix);
  [100,300,600,1000].forEach(function(ms){{ setTimeout(fix,ms); }});
}})();
</script>
</body>
</html>
'''


def service_display_name(slug):
    names = {
        "pediatric-epilepsy-phoenix": "Pediatric Epilepsy Treatment in Phoenix, AZ",
        "pediatric-seizures-phoenix": "Pediatric Seizures Treatment in Phoenix, AZ",
        "developmental-delays-phoenix": "Developmental Delays — Pediatric Neurology in Phoenix, AZ",
        "pediatric-headaches-phoenix": "Pediatric Headaches & Migraines in Phoenix, AZ",
        "cerebral-palsy-muscle-disease-phoenix": "Cerebral Palsy & Muscle Disease Treatment in Phoenix, AZ",
        "movement-disorders-phoenix": "Movement Disorders in Children — Phoenix, AZ",
        "tic-disorders-phoenix": "Tic Disorders in Children — Phoenix, AZ",
        "sleep-disorders-children-phoenix": "Sleep Disorders in Children — Phoenix, AZ",
        "dizziness-vertigo-children-phoenix": "Dizziness & Vertigo in Children — Phoenix, AZ",
        "traumatic-brain-injury-phoenix": "Traumatic Brain Injury in Children — Phoenix, AZ",
        "pediatric-concussion-phoenix": "Pediatric Concussion Management in Phoenix, AZ",
        "nerve-injury-phoenix": "Nerve Injury in Children — Phoenix, AZ",
        "insomnia-children-phoenix": "Insomnia in Children — Phoenix, AZ",
        "syncope-loss-of-consciousness-phoenix": "Syncope & Loss of Consciousness in Children — Phoenix, AZ",
        "visual-disturbances-children-phoenix": "Visual Disturbances in Children — Phoenix, AZ",
        "brain-mri-children-phoenix": "Pediatric Brain MRI in Phoenix, AZ",
        "pediatric-eeg-phoenix": "Pediatric EEG Testing in Phoenix, AZ",
        "tourette-syndrome-phoenix": "Tourette Syndrome Treatment in Phoenix, AZ",
    }
    return names.get(slug, slug.replace("-", " ").replace(" phoenix", " in Phoenix, AZ").title())


def service_short_name(slug):
    shorts = {
        "pediatric-epilepsy-phoenix": "pediatric epilepsy",
        "pediatric-seizures-phoenix": "pediatric seizures",
        "developmental-delays-phoenix": "developmental delays",
        "pediatric-headaches-phoenix": "pediatric headaches and migraines",
        "cerebral-palsy-muscle-disease-phoenix": "cerebral palsy and muscle disease",
        "movement-disorders-phoenix": "movement disorders",
        "tic-disorders-phoenix": "tic disorders",
        "sleep-disorders-children-phoenix": "sleep disorders",
        "dizziness-vertigo-children-phoenix": "dizziness and vertigo",
        "traumatic-brain-injury-phoenix": "traumatic brain injury",
        "pediatric-concussion-phoenix": "pediatric concussion",
        "nerve-injury-phoenix": "nerve injury",
        "insomnia-children-phoenix": "childhood insomnia",
        "syncope-loss-of-consciousness-phoenix": "syncope and loss of consciousness",
        "visual-disturbances-children-phoenix": "visual disturbances",
        "brain-mri-children-phoenix": "pediatric brain MRI",
        "pediatric-eeg-phoenix": "pediatric EEG",
        "tourette-syndrome-phoenix": "Tourette syndrome",
    }
    return shorts.get(slug, slug.replace("-phoenix", "").replace("-", " "))


def main():
    from datetime import date
    parser = argparse.ArgumentParser(description="Rebuild condition pages with clean template")
    parser.add_argument("--service", help="Single service slug to rebuild")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    today = date.today().isoformat()
    slugs = list(SERVICE_CONTENT.keys())
    if args.service:
        slugs = [s for s in slugs if s == args.service]
        if not slugs:
            print(f"Service not found: {args.service}")
            sys.exit(1)

    for slug in slugs:
        content = SERVICE_CONTENT[slug]
        title = service_display_name(slug)
        service_name = title.split(" in Phoenix")[0].split(" —")[0]
        short = service_short_name(slug)
        description = f"Expert {short} diagnosis and treatment in Phoenix, AZ. Dr. Zach Rose MD at Rose Medical Pavilion. Call (602) 892-7467."

        html = PAGE_TEMPLATE.format(
            title=title,
            description=description,
            slug=slug,
            service_name=service_name,
            service_name_lower=short,
            intro=content["intro"],
            body=content["body"],
            today=today,
        )

        out_path = os.path.join(REPO_ROOT, slug, "index.html")
        if args.dry_run:
            print(f"  [dry-run] /{slug}/index.html")
            continue

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  wrote: /{slug}/index.html")

    print(f"\nDone. Rebuilt {len(slugs)} condition pages.")


if __name__ == "__main__":
    main()
