from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
from ...models.ukbm.ukbm import ukbm

app = Flask(__name__)
CORS(app)


knowledge_source = ['''Multan is a city and capital of Multan Division located in Punjab, Pakistan. Situated on the bank of the Chenab River, Multan is Pakistan's 7th largest city and is the major cultural and economic centre of Southern Punjab. Multan's history stretches deep into antiquity. The ancient city was site of the renowned Hindu Multan Sun Temple, and was besieged by Alexander the Great during the Mallian Campaign. Multan was one of the most important trading centres of medieval Islamic India, and attracted a multitude of Sufi mystics in the 11th and 12th centuries, earning the city the sobriquet "City of Saints". 
                The city, along with the nearby city of Uch, is renowned for its large number of Sufi shrines dating from that era.''', 
                '''The immune system is a system of many biological structures and processes within an organism that protects against disease. 
                To function properly, an immune system must detect a wide variety of agents, known as pathogens, from viruses to parasitic worms, and distinguish them from the organism's own healthy tissue. 
                In many species, the immune system can be classified into subsystems, such as the innate immune system versus the adaptive immune system, or humoral immunity versus cell-mediated immunity. 
                In humans, the blood–brain barrier, blood–cerebrospinal fluid barrier, and similar fluid–brain barriers separate the peripheral immune system from the neuroimmune system which protects the brain. 
                Disorders of the immune system can result in autoimmune diseases, inflammatory diseases and cancer. 
                Immunodeficiency occurs when the immune system is less active than normal, resulting in recurring and life-threatening infections. 
                In humans, immunodeficiency can either be the result of a genetic disease such as severe combined immunodeficiency, acquired conditions such as HIV/AIDS, or the use of immunosuppressive medication. 
                In contrast, autoimmunity results from a hyperactive immune system attacking normal tissues as if they were foreign organisms. 
                Common autoimmune diseases include Hashimoto's thyroiditis, rheumatoid arthritis, diabetes mellitus type 1, and systemic lupus erythematosus. 
                Immunology covers the study of all aspects of the immune system.
                ''',
                '''The ICC Men's T20 World Cup (earlier known as ICC World Twenty20)[4] is the international championship of Twenty20 International cricket. Organised by cricket's governing body, the International Cricket Council (ICC), the tournament currently consists of 16 teams, comprising the top ten teams from the rankings at the given deadline and six other teams chosen through the T20 World Cup Qualifier. All matches are played as Twenty20 Internationals.
                The event has generally been held every two years. However, the next edition of the tournament was scheduled to take place in 2020 in Australia, but due to COVID-19, the tournament has been postponed to 2021, with the host changed to India, five years after the conclusion of the 2016 edition. However, due to the COVID-19 pandemic in India, the matches were relocated to the United Arab Emirates and Oman.[5] In May 2016, the ICC put forward the idea of having a tournament in 2018, with South Africa being the possible host.[6] But at the conclusion of the 2017 ICC Champions Trophy, the ICC dropped the idea of 2018 edition.
                Six tournaments have so far been played, and only the West Indies, who currently hold the title, has won the tournament on multiple occasions. The inaugural 2007 World Twenty20, was staged in South Africa, and won by India, who defeated Pakistan in the final at the Wanderers Stadium in Johannesburg. The 2009 tournament took place in England, and was won by the previous runner-up, Pakistan, who defeated Sri Lanka in the final at Lord's. The third tournament was held in 2010, hosted by the countries making up the West Indies cricket team.
                ''',
                '''Cryptography, or cryptology (from Ancient Greek: κρυπτός, romanized: kryptós "hidden, secret"; and γράφειν graphein, "to write", or -λογία -logia, "study", respectively), is the practice and study of techniques for secure communication in the presence of adversarial behavior. 
                More generally, cryptography is about constructing and analyzing protocols that prevent third parties or the public from reading private messages; various aspects in information security such as data confidentiality, data integrity, authentication, and non-repudiation are central to modern cryptography. Modern cryptography exists at the intersection of the disciplines of mathematics, computer science, electrical engineering, communication science, and physics. Applications of cryptography include electronic commerce, chip-based payment cards, digital currencies, computer passwords, and military communications.
                Cryptography prior to the modern age was effectively synonymous with encryption, converting information from a readable state to unintelligible nonsense. 
                The sender of an encrypted message shares the decoding technique only with intended recipients to preclude access from adversaries. The cryptography literature often uses the names Alice ("A") for the sender, Bob ("B") for the intended recipient, and Eve ("eavesdropper") for the adversary. Since the development of rotor cipher machines in World War I and the advent of computers in World War II, cryptography methods have become increasingly complex and its applications more varied.
                Modern cryptography is heavily based on mathematical theory and computer science practice; 
                cryptographic algorithms are designed around computational hardness assumptions, 
                making such algorithms hard to break in actual practice by any adversary.''']


topics = ["Multan", "The Immune System", "T20 World Cup", "Cryptography"]

class APImodel:
    def __init__(self):
        self.selected_id = 2
        self.model = ukbm(knowledge_source[self.selected_id])

    def changeTopic(self, id):
        self.selected_id = id 
        self.model = ukbm(knowledge_source[self.selected_id])

    def reply(self, message):
        return self.model.getResponse(message)


test_model = APImodel()

@app.route('/reply', methods=['POST'])
def get_reply():
    _json = request.json
    _message = _json['message']
    response = {"response": test_model.reply(_message)}
    return jsonify(response), 200

@app.route('/source', methods=['GET'])
def get_source():
    response = { "response" : knowledge_source[test_model.selected_id] }
    return jsonify(response), 200

@app.route('/topics', methods=['GET'])
def get_topics():
    response = { "topics" : topics, "current_topic": topics[test_model.selected_id]}
    return jsonify(response), 200

@app.route('/topics/select', methods=['POST'])
def select_topics():
    _json = request.json 
    _topic = _json['topic']
    print (_topic)
    for i, topic in enumerate(topics):
        if topic == _topic:
            test_model.changeTopic(i)
            break

    return jsonify({"response": "OK"}), 200