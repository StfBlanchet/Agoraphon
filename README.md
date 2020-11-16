# Agoraphon
A Flask application for analyzing activity on an online discussion forum, using scraping, indexing, analytics, relational graph and NLP.

# Agor@phon

* [Objectives](#objectives)
* [How it works](#how-it-works)
* [Stack and Architecture](#stack-and-architecture)
* [Status](#status)
* [Contributing](#contributing)
* [Authors](#authors)
* [License](#license) 


## Objectives

The Agor@phon Project is intended at contributing to the knowledge of natural language for machine learning purposes and providing real-world materials for studying phenomena such as disinformation and hate / extremism speech.

A tool developed by a researcher-programmer for scientific research, it materializes in a web software that ensures the collection and in-depth analysis of multimodal contents published on an online discussion forum.  


### NLP / linguistic application

The content collected will make it possible to build real-world textual corpora in French, which are rare compared with English ones. This is all the more a valuable resource that, on the forum studied here, the language is of a very oral and slang style, with idioms specific to its user community. That kind of communication is a pain for natural language processing systems which algorithms are mainly trained on texts written by professionals (e.g. press articles) and / or to be read by the greatest number (e.g. Wikipedia).


### Disinformation and hate speech investigation

The obtained datasets will also allow the study of phenomena such as fake news and trolls as well as extremism / hate speech for which any online communication platform may be fertile ground. What makes the type of forums studied here a little bit different is that users can register truly anonymously - no phone number or verified professional email to provide, which facilitates opportunistic or impulsive interventions, whether to launch or to participate in a discussion. Also, the desire to build and maintain any community of followers is out of concern for most of users. Unlike other platforms where family, friends and colleagues may identify them, they can post freely without worrying about their reputation. And when social desirability is not at stake, anything goes…

It should be noted that, on this research subject too, large French corpora are few or else concentrated on easily accessible deposits (e.g. Twitter).

A preliminary exploratory study has shown that the forum is a place of convergence of different kinds of sources, whether social networks, micro-blogging and videos or images sharing platforms, information sites, or even messaging such as Telegram or Whatsapp which screenshots can be found shared by users. Thus the forum opens on a wider spectrum than itself and offers materials that enable to catch social trends.


## How it works

![alt text](Agoraphon_design/Agoraphon_search.png "Agoraphon search")
![alt text](Agoraphon_design/Agoraphon_select.png "Agoraphon select")
![alt text](Agoraphon_design/Agoraphon_analyze_topic.png "Agoraphon analyze_topic")
![alt text](Agoraphon_design/Agoraphon_nlp_annotator.png "Agoraphon nlp_annotator")
![alt text](Agoraphon_design/Agoraphon_extract_ne.png "Agoraphon extract_ne")
![alt text](Agoraphon_design/Agoraphon_source_annotator.png "Agoraphon source_annotator")
![alt text](Agoraphon_design/Agoraphon_select_bulk.png "Agoraphon select_bulk")
![alt text](Agoraphon_design/Agoraphon_analyze_bulk.png "Agoraphon analyze_bulk")
![alt text](Agoraphon_design/Agoraphon_analyze_user.png "Agoraphon analyze_user")



## Stack and Architecture

The application is built with Flask framework 1.1 and written in Python 3.8.

The whole system is based on a distributed architecture. Three servers are at play: the first one is dedicated to scraping ; the second one to data indexing and retrieving ; and the third one hosts the application where the data mining, analytics and visualization tasks are performed.

<img src="Agoraphon_design/Agoraphon_architecture.png">

 
## Status

This project is in progress.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Authors

- Initial work: Stephanie BLANCHET, R&D Cognitician. Data Pythonist.
- Contact: agoraphon@gmail.com


## License

This project is licensed under the MIT License - see [MIT](https://choosealicense.com/licenses/mit/) for details.
