#! /usr/bin/env python3
# coding: utf-8

"""
Agor@aphon constant values
"""

# Mapping to be implemented when
# a new index is created to store
# a post dataset in Elasticsearch
POST_ = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        },
        "mappings": {
            "properties": {
                "topic": {"type": "text"},
                "date": {"type": "date"},
                "user": {"type": "text"},
                "post": {"type": "text"},
                "post_tone": {"type": "text"},
                "post_img": {"type": "text"},
                "post_vid": {"type": "text"},
                "post_sources": {"type": "text"},
                "quotes": {"type": "text"}
            }
        }
    }

# Word list to isolate a video content
# from a set of urls
VID_ = ['youtu', 'dailymotion', 'vimeo']

TONES_ = {
    'doute': ['2', '34', '43'],
    'approbation': ['23', '36', '37', '69'],
    'désapprobation': ['25', '30', '45', '56', '63', '35'],
    'déception': ['33', '14'],
    'surprise': ['22', '57'],
    'colère': ['15', '19'],
    'peur': ['8'],
    'joie': ['40', '55', '66'],
    'malice': ['61', '67', '11'],
    'tristesse': ['13', '20'],
    'prière': ['59', '60'],
    'rire': ['32', '39', '62', '12'],
    'sourire': ['1', '18', '53', '46'],
    'félicitations': ['29', '42'],
    'ridicule': ['47'],
    'séduction': ['7', '31', '71']
}

# Thematics that have their own lexicons
# to automate broad plain text search
THEMATIC_ = ['politique', 'religion', 'santé', 'science', 'environnement']

LEXICON_ = {
    "politique": "(assemblée nationale) OR (néo nazi) OR (extrême droite) "
                 "OR (extrême gauche) OR (la gauche) OR "
                 "(la droite) OR (rassemblement national) OR "
                 "(front national) OR (marine le pen) OR (le pen) "
                 "OR (debout la france) OR (nicolas dupont-aignan) "
                 "OR (les patriotes) OR (florian philippot) OR "
                 "(comités jeanne) OR (jean-marie le pen) OR "
                 "(ligue du sud) OR (jacques bompard) OR "
                 "(identité et libertés) OR (paul-marie coûteaux) "
                 "OR (karim ouchikh) OR (parti de l'in-nocence) OR "
                 "(renaud camus) OR (dissidence française) OR "
                 "(vincent vauclin) OR (les identitaires) OR "
                 "(bloc identitaire) OR (fabrice robert) OR "
                 "(génération identitaire) OR (clément gandelin) OR "
                 "(parti national-libéral) OR (henry de lesquen) "
                 "OR (alain escada) OR (dies irae) OR "
                 "(parti de la france) OR (carl lang) OR (thomas joly) "
                 "OR (mouvement national républicain) OR "
                 "(bruno mégret) OR (action française) OR "
                 "(parti nationaliste français) OR (jean-françois simon) "
                 "OR (terre et peuple) OR (pierre vial) OR "
                 "(renouveau français) OR (thibaut de chassey) OR "
                 "(les républicains) OR (union pour un mouvement populaire) "
                 "OR (christian jacob) OR (le mouvement de la ruralité) "
                 "OR (nature et traditions) OR (les républicains) OR "
                 "(centre national des indépendants et paysans) OR "
                 "(bruno north) OR (parti chrétien-démocrate) OR "
                 "(christine boutin) OR (jean-frédéric poisson) OR "
                 "(alliance royale) OR (yves-marie adeline) OR "
                 "(le trèfle - les nouveaux écologistes) OR "
                 "(bernard manovelli) OR (albert lapeyre) OR "
                 "(emmanuel macron) OR (nicolas sarkozy) OR (soyons libres) "
                 "OR (valérie pécresse) OR (territoires en mouvement) OR "
                 "(jean-christophe fromantin) OR (république solidaire) OR "
                 "(dominique de villepin) OR (union populaire républicaine) "
                 "OR (françois asselineau) OR "
                 "(rassemblement des contribuables français) OR "
                 "(nicolas miguet) OR (la république en marche) OR "
                 "(stanislas guerini) OR (mouvement démocrate) OR "
                 "(union pour la démocratie française) OR "
                 "(françois bayrou) OR (union des démocrates et indépendants) "
                 "OR (jean-christophe lagarde) OR "
                 "(force européenne démocrate) OR (hervé marseille) OR "
                 "(mouvement radical) OR (parti radical) OR "
                 "(parti radical de gauche) OR (la gauche moderne) OR "
                 "(jean-marie bockel) OR "
                 "(nouvelle écologie démocrate) OR (nathalie tortrat) OR "
                 "(alliance centriste) OR (jean arthuis) OR "
                 "(philippe folliot) OR (parti écologiste) OR (écologistes !) "
                 "OR (françois de rugy) OR "
                 "(mouvement démocrate) OR (jean lassalle) OR "
                 "(les centristes) OR (nouveau centre) OR (hervé morin) OR "
                 "(nous citoyens) OR (denis payre) OR (alexia germont) OR "
                 "(génération citoyens) OR (jean-marie cavada) "
                 "OR (alliance écologiste indépendante) OR "
                 "(jean-marc governatori) OR "
                 "(mouvement écologiste indépendant) OR (antoine waechter) "
                 "OR (mouvement hommes animaux nature) OR "
                 "(jacques leboucher) OR (parti animaliste) OR "
                 "(parti fédéraliste européen) OR (yves gernigon) OR "
                 "(allons enfants) OR (pierre cazeneuve) OR "
                 "(force européenne démocrate) OR (jean-christophe lagarde) "
                 "OR (hervé marseille) OR (europe écologie les verts) OR "
                 "(les verts) OR (julien bayou) OR (parti socialiste) OR "
                 "(place publique) OR (raphaël glucksmann) OR "
                 "(thomas porcher) OR (claire nouvian) OR (jo spiegel) OR "
                 "(nouvelle donne) OR (parti socialiste) OR "
                 "(pierre larrouturou) OR (parti radical de gauche) OR "
                 "(guillaume lacroix) OR (gauche républicaine et socialiste) "
                 "OR (emmanuel maurel) OR (marie-noëlle lienemann) OR "
                 "(la france insoumise) OR (mouvement républicain et citoyen) "
                 "OR (jean-pierre chevènement) OR (benoît hamon) OR "
                 "(génération écologie) OR (delphine batho) OR "
                 "(union des démocrates et des écologistes) OR "
                 "(le rassemblement citoyen) OR (corinne lepage) OR "
                 "(rassemblement des écologistes pour le vivant) OR "
                 "(aymeric caron) OR (benjamin joyeux) OR (malena azzam) "
                 "OR (la force du 13) OR (jean-noël guérini) OR "
                 "(mouvement des progressistes) OR (robert hue) OR "
                 "(mouvement des citoyens) OR (les radicaux de gauche) OR "
                 "(virginie rozière) OR (stéphane saint-andré) OR "
                 "(union des démocrates musulmans français) OR "
                 "(nagib azergui) OR (nouvelle action royaliste) OR "
                 "(jacques cheminade) OR (parti pirate) OR "
                 "(mouvement républicain et citoyen) OR "
                 "(jean-pierre chevènement) OR (la france insoumise) OR "
                 "(jean-luc mélenchon) OR (parti de gauche) OR "
                 "(ensemble !) OR (parti communiste français) OR "
                 "(fabien roussel) OR (république et socialisme) OR "
                 "(nouveau parti anticapitaliste) OR "
                 "(olivier besancenot) OR (lutte ouvrière) OR "
                 "(parti pour la décroissance) OR (vincent cheynet) OR "
                 "(parti ouvrier indépendant) OR "
                 "(parti communiste des ouvriers de france) OR "
                 "(pôle de renaissance communiste en france) OR "
                 "(union communiste libertaire) OR "
                 "(coordination des groupes anarchistes et "
                 "alternative libertaire) OR (fédération anarchiste) OR "
                 "(indigènes de la république) OR (parti des indigènes "
                 "de la république) OR (houria bouteldja) OR "
                 "politique OR politicien OR politicienne OR gouvernement "
                 "OR sénat OR élysée OR ministre OR sénateur "
                 "OR maire OR député OR président OR féministe OR "
                 "républicain OR démocrate OR nazi OR trump "
                 "OR fachiste OR politique OR politicien OR fachos OR rn "
                 "OR fn OR dlf OR dupont-aignan OR lp OR "
                 "philippot OR cj OR ls OR bompard OR souveraineté OR siel "
                 "OR ouchikh OR pi OR df OR vauclin OR li OR "
                 "bi OR gi OR civitas OR di OR pdf OR mnr OR af OR pnf OR "
                 "rf OR lr OR ump OR lmr OR chasse OR pêche "
                 "OR cpnt OR cnip OR pcd OR ar OR lt-ne OR agir OR macron "
                 "OR sarkozy OR sl OR libres OR tem OR rs OR "
                 "upr OR rcf OR lrem OR larem OR rem OR lrm OR modem OR udf "
                 "OR udi OR fed OR mr OR lgm OR ned OR "
                 "cap21 OR ac OR résistons OR lc OR nc OR nc OR gc OR aei "
                 "OR mei OR mhan OR pa OR pfe OR ae OR fed OR eelv OR ps "
                 "OR pp OR nd OR prg OR grs OR mrc OR générations OR g·s "
                 "OR ge OR ude OR cap21 OR lrc-cap21 OR rev OR lfd13 OR mdp "
                 "OR mdc OR rdg OR lrdg OR udmf OR nar OR pp OR mrc OR fi OR "
                 "lfi OR pg OR pcf OR npa OR lo OR ppld OR poi OR pcof OR "
                 "prcf OR ucl OR fa OR ir",
    "religion": "religions OR croyant OR mécréant OR catholique OR catho OR "
                "chrétien OR feuj OR juif OR juive OR judaïsme OR islam OR "
                "islamique OR islamiste OR intégriste OR orthodoxe OR "
                "christianisme OR musulman OR muslim OR bible OR coran OR "
                "chariah OR boudhisme OR boudhiste OR religieux OR religieuse "
                "OR culte OR église OR temple OR mosquée OR synagogue "
                "OR fondamentaliste",
    "santé": "santé OR coronavirus OR sida OR grippe OR fièvre OR varicelle "
             "OR hépatite OR herpès OR listériose OR listeria OR peste OR "
             "rage OR maladie OR malade OR virus OR bactérie OR microbe OR "
             "OMS OR contagion OR infection OR infecter OR infectés OR "
             "quarantaine OR épidémie OR pandémie OR contaminer OR contaminé",
    "science": "(intelligence artificielle) OR science OR biologie OR "
               "technologie OR physique OR quantique OR psychologie OR "
               "sociologie OR économie OR mathématiques OR génétique OR "
               "astronomie OR astrophysique OR (machine learning) OR "
               "(deep learning) OR (reconnaissance faciale) OR cognitif "
               "OR satellite OR ovni OR 5G OR fibre optique OR microbiologie",
    "environnement": "(catastrophe naturelle) OR environnement OR écologie "
                     "OR écologique OR nature OR climat OR pollution OR "
                     "(économie circulaire) OR éco-responsable OR recyclage "
                     "OR (changement climatique) OR climato-sceptique OR "
                     "climatosceptique OR (réchauffement climatique) OR "
                     "permafrost OR (déchets plastiques) OR "
                     "(déchets industriels) OR biodiversité OR écosystème "
                     "OR faune OR flore"
}

# Special stop words ("oralised")
# to be discarded from the corpus
STOP_ = ['ben', 'bin', 'bé', 'béh', 'bah', 'oki', 'ouep', 'ouais', 'ouaip',
         'yes', 'yep', 'ah', 'ha', 'oh', 'ho', 'ptin', 'ptain', 'tain',
         'putain', 'ptn', 'kheys', 'khey', 'kheyou', 'ça', 'ca', 'aya',
         'ayaa', 'ayaaa', 'ayaaaa', 'ayaaaaa', 'ayaaaaaa', 'nan', 'http',
         'https', 'spoilaffichermasquer', 'wtf', 'jyfu', 'gg', 'qqun',
         'hmm', 'hum', 'euh', 'heu', 'lol', 'ya', 'cest', 'fr', 'aaah',
         'aha', 'ahahah', 'eugeuh', 'haha', 'ptete',
         'peutetre', 'ptet', 'voila', 'putaiiiiiiin']

# Set of colors to be used
# for dataviz charts
COLORS_ = ['#154360', '#1a5276', '#1f618d', '#512e5f', '#633974', '#76448a',
           '#884ea0', '#a569bd', '#2471a3', '#2980b9', '#5499c7', '#7fb3d5',
           '#a9cce3', '#154360', '#1a5276', '#1f618d', '#512e5f', '#633974',
           '#76448a', '#884ea0', '#a569bd', '#2471a3', '#2980b9', '#5499c7',
           '#7fb3d5', '#a9cce3', '#154360', '#1a5276', '#1f618d', '#512e5f',
           '#633974', '#76448a', '#884ea0', '#a569bd', '#2471a3']
