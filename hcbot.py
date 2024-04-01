import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from nltk.chat.util import Chat, reflections
from PyQt5.QtGui import QIcon 
import speech_recognition as sr
import pyttsx3
import threading
import PyQt5


rules = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!']),
    (r'(.*) (symptoms)', ['I can provide general information about symptoms. Please describe your symptoms.']),
    (r'(.*) (appointment)', ['You can schedule an appointment by calling the hospital directly.']),
    (r'(.*) (disease|condition)', ['I can provide information about diseases and conditions. Please specify the disease or condition you want to know more about.']),
    (r'(.*) (solutions|treatment) (for|to) (.*)', ['Here are some general treatment options for $3: [Treatment 1, Treatment 2, Treatment 3].']),
    (r'(.*) (identify|diagnose) (a|an|the) disease (based|from|on) symptoms', ['To identify a disease based on symptoms, please provide a list of symptoms, separated by commas.']),
    (r'(.*) (fever|headache|cough)', ['It could be a common cold. Rest, drink fluids, and consider over-the-counter medication.']),
    (r'(.*) (sore throat|runny nose|congestion)', ['It may be a respiratory infection. Rest, stay hydrated, and consider over-the-counter cold remedies. If it persists, consult a doctor.']),
    (r'(.*) (stomach ache|nausea|vomiting)', ['These symptoms could be related to various gastrointestinal issues. Avoid spicy foods and dairy, and consult a doctor if symptoms persist.']),
    (r'(.*) (fatigue|weakness)', ['Fatigue can be due to various reasons. Ensure you get enough sleep, maintain a healthy diet, and consult a healthcare professional for a proper evaluation.']),
    (r'(.*) (rash|itchy skin)', ['It could be a skin allergy or dermatological condition. Avoid scratching, keep the area clean, and consult a dermatologist if it worsens.']),
    (r'(.*) (shortness of breath|chest pain)', ['These symptoms can be serious. Seek immediate medical attention or call 911.']),
    (r'(.*) (dizziness|vertigo)', ['Dizziness may have multiple causes. Sit down, keep still, and consult a doctor if it persists.']),
    (r'(.*) (back pain|muscle pain)', ['Back pain and muscle pain can result from strain. Rest, apply ice or heat, and consider over-the-counter pain relief.']),
    (r'(.*) (joint pain|swelling)', ['It may be arthritis or an injury. Rest, apply ice, and consult a rheumatologist or orthopedic specialist.']),
    (r'(.*) (frequent urination|painful urination)', ['These symptoms can be related to a urinary tract infection. Drink plenty of water and consult a healthcare professional.']),
    (r'(.*) (insomnia|sleep problems)', ['Maintain a regular sleep schedule, create a relaxing bedtime routine, and avoid caffeine before bedtime.']),
    (r'(.*) (anxiety|stress|panic attack)', ['Practice relaxation techniques, mindfulness, and consider speaking to a therapist.']),
    (r'(.*) (diabetes|blood sugar)', ['High or low blood sugar can cause symptoms. Monitor your levels, consult a doctor, and follow a prescribed treatment plan.']),
    (r'(.*) (allergies|allergic reaction)', ['If you suspect an allergy, avoid the allergen and consult an allergist for testing.']),
    (r'(.*) (migraine|severe headache)', ['It may be a migraine. Find a quiet, dark place, rest, and consider over-the-counter pain relief.']),
    (r'(.*) (flu|influenza)', ['These symptoms could be the flu. Rest, stay hydrated, and consult a doctor if symptoms worsen.']),
    (r'(.*) (COVID-19|coronavirus)', ['If you suspect COVID-19, self-isolate and get tested. Follow local health guidelines.']),
    (r'(.*) (earache|ear pain)', ['It may be an ear infection. Avoid inserting objects in the ear, keep it dry, and consult an ENT specialist.']),
    (r'(.*) (toothache|dental pain)', ['Toothache could be due to dental issues. Rinse with warm water, floss, and see a dentist.']),
    (r'(.*) (skin rash|hives|redness)', ['It could be an allergic reaction or skin condition. Avoid irritants and consult a dermatologist.']),
    (r'(.*) (covid test|coronavirus test)', ['If you have COVID-19 symptoms or exposure, get tested at a local testing center.']),
    (r'(.*) (broken bone|fracture)', ['If you suspect a broken bone, immobilize the area and seek immediate medical attention.']),
    (r'(.*) (insect bite|sting)', ['Clean the area, apply an antiseptic, and monitor for allergic reactions.']),
    (r'(.*) (nausea|vomiting|diarrhea)', ['Stay hydrated, avoid solid food, and consult a doctor if it persists.']),
    (r'(.*) (insulin|diabetic|blood sugar)', ['If you have diabetes, ensure you monitor blood sugar levels and follow your treatment plan.']),
    (r'(.*) (sunburn|sunscreen)', ['For sunburn, apply aloe vera or a moisturizer. Use sunscreen to prevent future sunburn.']),
    (r'(.*) (depression|mental health)', ['Mental health is important. Seek help from a mental health professional if you\'re experiencing depression.']),
    (r'(.*) (allergic reaction|anaphylaxis)', ['If you suspect anaphylaxis, use an EpiPen if available and seek immediate medical attention.']),
    (r'(.*) (menstrual cramps|PMS)', ['For menstrual cramps, consider over-the-counter pain relief or consult a gynecologist for solutions.']),
    (r'(.*) (asthma|difficulty breathing)', ['If you have asthma, use your inhaler. If breathing difficulties persist, seek medical assistance.']),
    (r'(.*) (chest congestion|phlegm)', ['Stay hydrated, use a humidifier, and consider over-the-counter decongestants.']),
    (r'(.*) (food poisoning|stomach upset)', ['If you suspect food poisoning, stay hydrated and consult a doctor if symptoms worsen.']),
    (r'(.*) (hair loss|baldness)', ['Hair loss can have multiple causes. Consult a dermatologist for a proper evaluation and treatment.']),
    (r'(.*) (mood swings|bipolar disorder)', ['If you experience extreme mood swings, consult a mental health professional for diagnosis and treatment.']),
    (r'(.*) (hiccups|persistent hiccups)', ['Hiccups are usually harmless and go away on their own. If persistent, consult a doctor.']),
    (r'(.*) (sore eyes|conjunctivitis)', ['It may be conjunctivitis (pink eye). Avoid touching your eyes and consult an eye specialist.']),
    (r'(.*) (toenail fungus|nail infection)', ['For nail infections, consult a podiatrist for diagnosis and treatment.']),
    (r'(.*) (sprained ankle|injury)', ['RICE (Rest, Ice, Compression, Elevation) can help with a sprained ankle. Seek medical attention if severe.']),
    (r'(.*) (blurred vision|vision problems)', ['Blurred vision can result from eye strain or eye conditions. Rest your eyes and consult an ophthalmologist if needed.']),
    (r'(.*) (hair fall|hair thinning)', ['Hair fall can have multiple causes. Maintain a healthy diet, consider hair care products, and consult a dermatologist if it persists.']),
    (r'(.*) (burns|burned skin)', ['For burns, cool the affected area with cold water and apply a sterile dressing. Seek medical attention for severe burns.']),
    (r'(.*) (bruises|ecchymosis)', ['Bruises are usually harmless. Apply ice to reduce swelling and consult a doctor if they appear without injury.']),
    (r'(.*) (seizures|epilepsy)', ['If you experience seizures, protect your head, lie down, and seek immediate medical evaluation. Consult a neurologist for epilepsy management.']),
    (r'(.*) (swollen glands|lymph nodes)', ['Swollen glands can be due to infections. Rest, stay hydrated, and consult a doctor if they persist.']),
    (r'(.*) (blister|fluid-filled bump)', ['For blisters, avoid popping them, keep them clean, and consider over-the-counter ointments.']),
    (r'(.*) (urinary tract infection|UTI)', ['UTIs require antibiotics. Stay hydrated, avoid irritants, and consult a doctor for diagnosis and treatment.']),
    (r'(.*) (irregular menstruation|period problems)', ['For irregular menstruation, consult a gynecologist to identify the underlying cause and potential treatments.']),
    (r'(.*) (tinnitus|ringing in ears)', ['Tinnitus may have various causes. Avoid loud noises, and consult an audiologist for evaluation.']),
    (r'(.*) (irritable bowel syndrome|IBS)', ['Manage IBS with dietary changes and stress reduction techniques. Consult a gastroenterologist for guidance.']),
    (r'(.*) (chronic pain|persistent pain)', ['Chronic pain may require ongoing pain management. Consult a pain specialist or pain clinic for options.']),
    (r'(.*) (heart disease|cardiovascular issues)', ['For heart disease concerns, consult a cardiologist for diagnostic tests and personalized recommendations.']),
    (r'(.*) (joint inflammation|arthritis)', ['Arthritis can cause joint inflammation. Rest, use ice or heat, and consult a rheumatologist for evaluation.']),
    (r'(.*) (memory loss|cognitive decline)', ['If you experience memory loss, consult a neurologist for cognitive assessments and potential interventions.']),
    (r'(.*) (cancer symptoms|cancer concerns)', ['If you have cancer-related concerns, consult an oncologist for appropriate screenings and evaluation.']),
    (r'(.*) (weight gain|unexplained weight changes)', ['Unexplained weight changes may have underlying causes. Consult a healthcare professional for evaluation and guidance.']),
    (r'(.*) (urinary retention|difficulty urinating)', ['Urinary retention may require immediate medical attention. Consult a urologist for diagnosis and treatment.']),
    (r'(.*) (thyroid symptoms|thyroid concerns)', ['Thyroid symptoms can indicate thyroid disorders. Consult an endocrinologist for evaluation and treatment.']),
    (r'(.*) (pneumonia)', ['Pneumonia is an inflammatory lung infection that can cause cough, fever, and difficulty breathing. Treatment depends on the cause and severity and may involve antibiotics or hospitalization. Consult a pulmonologist for more details.']),
    (r'(.*) (diarrhea|gastroenteritis)', ['Diarrhea is characterized by frequent, loose bowel movements. It can result from infections or dietary issues. Stay hydrated and consult a doctor if it persists.']),
    (r'(.*) (malaria)', ['Malaria is a mosquito-borne infectious disease. It causes symptoms like fever, chills, and fatigue. Treatment involves anti-malarial medications. Consult an infectious disease specialist for more information.']),
    (r'(.*) (depression)', ['Depression is a mood disorder that affects feelings of sadness and hopelessness. Treatment includes therapy and sometimes medication. Consult a mental health professional or psychiatrist for more information.']),
    (r'(.*) (anxiety)', ['Anxiety is a common mental health condition characterized by excessive worry and fear. Treatment may involve therapy, lifestyle changes, or medication. Consult a psychologist or psychiatrist for more details.']),
    (r'(.*) (arthritis)', ['Arthritis is inflammation of one or more joints, leading to pain and stiffness. Treatment varies depending on the type of arthritis and may include medication or physical therapy. Consult a rheumatologist for specific information.']),
    (r'(.*) (osteoporosis)', ['Osteoporosis is a bone disease that weakens bones, making them more likely to break. Prevention includes diet, exercise, and sometimes medication. Consult an orthopedic specialist for more details.']),
    (r'(.*) (migraine)', ['Migraine is a type of headache often accompanied by nausea and sensitivity to light and sound. Management may involve medication and lifestyle changes. Consult a neurologist for more information.']),
    (r'(.*) (liver disease)', ['Liver diseases can have various causes. Treatment depends on the specific liver condition and may include medication or lifestyle modifications. Consult a hepatologist for more information.']),
    (r'(.*) (kidney disease)', ['Kidney disease can result from various factors. Management may include dietary changes, medication, or dialysis. Consult a nephrologist for specific details.']),
    (r'(.*) (rheumatoid arthritis)', ['Rheumatoid arthritis is an autoimmune disease that affects the joints. Treatment aims to reduce inflammation and may include medication or physical therapy. Consult a rheumatologist for more information.']),
    (r'(.*) (multiple sclerosis)', ['Multiple sclerosis is a chronic autoimmune disease that affects the central nervous system. Treatment may involve disease-modifying drugs and symptom management. Consult a neurologist for specific information.']),
    (r'(.*) (eczema|dermatitis)', ['Eczema is a skin condition characterized by itching and inflammation. Management includes moisturizers and topical medications. Consult a dermatologist for more details.']),
    (r'(.*) (glaucoma)', ['Glaucoma is an eye condition that can lead to vision loss. Treatment aims to lower eye pressure and may involve eye drops or surgery. Consult an ophthalmologist for more information.']),
    (r'(.*) (urinary tract infection|UTI)', ['A urinary tract infection (UTI) is a bacterial infection that affects the urinary system. It causes symptoms like frequent urination and pain during urination. Treatment involves antibiotics. Consult a urologist or general practitioner for more information.']),
    (r'(.*) (gastroesophageal reflux disease|GERD)', ['GERD is a chronic condition where stomach acid flows back into the esophagus, causing heartburn and irritation. Management includes lifestyle changes and medication. Consult a gastroenterologist for specific details.']),
    (r'(.*) (obesity|weight management)', ['Obesity is a condition characterized by excess body fat. Management involves diet, exercise, and sometimes surgery. Consult a nutritionist or bariatric specialist for more information.']),
    (r'(.*) (sleep apnea)', ['Sleep apnea is a sleep disorder characterized by interrupted breathing during sleep. Treatment may include lifestyle changes, continuous positive airway pressure (CPAP) therapy, or surgery. Consult a sleep specialist or pulmonologist for specific details.']),
    (r'(.*) (gout)', ['Gout is a type of arthritis that causes painful joint inflammation. Treatment includes medication and dietary changes. Consult a rheumatologist for more information.']),
    (r'(.*) (lupus)', ['Lupus is an autoimmune disease that can affect various body systems. Treatment depends on the specific symptoms and may involve medication and lifestyle changes. Consult a rheumatologist or immunologist for more details.']),
    (r'(.*) (chronic obstructive pulmonary disease|COPD)', ['COPD is a progressive lung disease that includes chronic bronchitis and emphysema. Treatment aims to relieve symptoms and may involve inhalers or oxygen therapy. Consult a pulmonologist for specific information.']),
    (r'(.*) (irritable bowel syndrome|IBS)', ['IBS is a gastrointestinal disorder that can cause abdominal pain and changes in bowel habits. Management includes dietary changes and symptom relief. Consult a gastroenterologist for more details.']),
    (r'(.*) (parkinson\'s disease)', ['Parkinson\'s disease is a neurodegenerative disorder that affects movement. Treatment may involve medication and physical therapy. Consult a neurologist for specific information.']),
    (r'(.*) (endometriosis)', ['Endometriosis is a painful condition where tissue similar to the uterine lining grows outside the uterus. Treatment depends on the severity and may involve medication or surgery. Consult a gynecologist for more details.']),
    (r'(.*) (hypothyroidism|underactive thyroid)', ['Hypothyroidism is a condition where the thyroid gland doesn\'t produce enough thyroid hormones. Treatment involves thyroid hormone replacement therapy. Consult an endocrinologist for specific information.']),
    (r'(.*) (hyperthyroidism|overactive thyroid)', ['Hyperthyroidism is a condition where the thyroid gland produces too much thyroid hormone. Treatment may include medication, radioactive iodine therapy, or surgery. Consult an endocrinologist for more details.']),
    (r'(.*) (anemia)', ['Anemia is a condition characterized by a lack of red blood cells or a low hemoglobin level. Treatment depends on the underlying cause and may involve dietary changes or iron supplements. Consult a hematologist for more information.']),
    (r'(.*) (fibromyalgia)', ['Fibromyalgia is a chronic pain disorder. Treatment aims to manage symptoms and may include medication, physical therapy, and lifestyle changes. Consult a rheumatologist for specific details.']),
    (r'(.*) (bipolar disorder)', ['Bipolar disorder is a mental health condition characterized by mood swings between mania and depression. Treatment includes mood stabilizers and therapy. Consult a psychiatrist or mental health professional for more information.']),
    (r'(.*) (diabetes|diabetic)', ['Diabetes is a chronic condition that affects how your body processes glucose (sugar). There are two main types, Type 1 and Type 2. Management includes monitoring blood sugar levels, lifestyle changes, and medication. Consult a doctor for more information.']),
    (r'(.*) (hypertension|high blood pressure)', ['Hypertension is a condition where the force of blood against the artery walls is consistently too high. It can lead to serious health problems. Lifestyle changes and medication can help control it. Consult a cardiologist for more details.']),
    (r'(.*) (asthma|breathing difficulties)', ['Asthma is a chronic respiratory condition that causes airway inflammation and bronchoconstriction. It can be managed with inhalers and avoiding triggers. Consult a pulmonologist for more information.']),
    (r'(.*) (cancer|oncology)', ['Cancer is a group of diseases characterized by uncontrolled cell growth. Treatment depends on the type and stage of cancer and may include surgery, chemotherapy, radiation therapy, or immunotherapy. Consult an oncologist for specific details.']),
    (r'(.*) (Alzheimer\'s disease|dementia)', ['Alzheimer\'s disease is a progressive neurodegenerative disorder that affects memory, thinking, and behavior. It has no cure, but there are treatments to manage symptoms. Consult a neurologist or geriatric specialist for more information.']),
    (r'(.*) (stroke|cerebrovascular accident)', ['A stroke occurs when blood flow to the brain is interrupted, leading to brain damage. There are different types of strokes, and treatment may involve medication or surgery. Seek immediate medical attention if you suspect a stroke.']),
    (r'thank you|thanks', ['You\'re welcome!', 'No problem, happy to help!', 'Anytime! If you have more questions, feel free to ask.']),
    (r'(.*) (concussion|head injury)', ['If you suspect a concussion or head injury, rest in a quiet place, apply ice, and seek medical attention.']),
    (r'(.*) (allergic reactions)', ['Allergic reactions can vary in severity. If you experience a severe allergic reaction (anaphylaxis), use an EpiPen if available and seek immediate medical attention. For milder reactions, consult an allergist for evaluation and guidance.'])
]

chatbot = Chat(rules, reflections)

class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Corrected the super() call
        self.init_ui()
        self.recognizer = sr.Recognizer()
        self.speech_engine = pyttsx3.init()
        self.listening = False
        self.conversation_state = 0

    def init_ui(self):

        self.setWindowTitle('Healthcare Chatbot')
        self.setGeometry(387, 165, 1149, 748)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.chat_display = QTextBrowser()
        layout.addWidget(self.chat_display)

        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.get_response)
        layout.addWidget(self.user_input)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.get_response)
        layout.addWidget(self.send_button)

        central_widget.setLayout(layout)

        font = self.chat_display.font()
        font.setPointSize(12)
        self.chat_display.setFont(font)

        font = self.user_input.font()
        font.setPointSize(12)
        self.user_input.setFont(font)
        icon = QIcon("consultant.png")
        self.setWindowIcon(icon)
        self.voice_input_label = QLabel()
        layout.addWidget(self.voice_input_label)

        self.voice_input_button = QPushButton('Voice Input')
        self.voice_input_button.clicked.connect(self.process_voice_input)
        layout.addWidget(self.voice_input_button)

        self.stop_button = QPushButton('Stop Listening')
        self.stop_button.clicked.connect(self.stop_listening)
        layout.addWidget(self.stop_button)

        self.exit_button = QPushButton('Exit to Conversation')
        self.exit_button.clicked.connect(self.Exit_conv)
        layout.addWidget(self.exit_button)

    def Exit_conv(self):
        quit()
        # exit()
    def get_response(self):
        user_input = self.user_input.text()
        response = ""

        if self.conversation_state == 0:
            response = "Hello! May I know your name, please?"
            self.conversation_state = 1

        elif self.conversation_state == 1:
            user_name = user_input.strip()
            if user_name:
                self.user_name = user_name
                response = f"Nice to meet you, {user_name}! What is your age?"
                self.conversation_state = 2
            else:
                response = "I didn't catch your name. Please enter your name."

        elif self.conversation_state == 2:
            user_age = user_input.strip()
            if user_age.isdigit():
                self.user_age = user_age
                response = "What is your gender (e.g., Male, Female, Other)?"
                self.conversation_state = 3
            else:
                response = "Please provide a valid age."

        elif self.conversation_state == 3:
            user_gender = user_input.strip()
            if user_gender.lower() in ["male", "female", "other"]:
                self.user_gender = user_gender
                response = "Do you have any symptoms you'd like to discuss? If so, please describe them. If you're done, you can simply say 'No' to end the conversation."
                self.conversation_state = 4
            else:
                response = "Please provide a valid gender (e.g., Male, Female, Other)."

        elif self.conversation_state == 4:
            if user_input.strip().lower() in ["no", "nope"]:
                response = f"Alright, {self.user_name}! If you ever need assistance in the future, feel free to ask. Have a great day!"
            else:
                response = chatbot.respond(user_input)
                self.conversation_state = 5
        elif self.conversation_state == 5:        
            response = "Alright! Is there anything else I can assist you with today?"
            self.conversation_state = 4
        self.chat_display.append(f'You: {user_input}')
        self.chat_display.append(f'Chatbot: {response}')
        self.user_input.clear()
        threading.Thread(target=self.speak, args=(response,)).start()

    def start_listening(self):
        self.listening = True
        self.voice_input_label.setText("Listening for voice input...")
        self.voice_input_label.repaint()

        def voice_input_thread():
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source)
                    if self.listening:
                        voice_input = self.recognizer.recognize_google(audio)
                        print("Voice Input:", voice_input)
                        self.voice_input_label.setText(f"Voice Input: {voice_input}")
                        self.voice_input_label.repaint()
                        self.user_input.setText(voice_input)
                        self.get_response()
                    else:
                        print("Listening stopped.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

        threading.Thread(target=voice_input_thread).start()

    def process_voice_input(self):
        self.start_listening()

    def stop_listening(self):
        self.listening = False
        self.voice_input_label.setText("Voice input listening stopped.")

    def speak(self, text):
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec_())
