# MUKALMA
A knowledge-grounded, human-like coversational agent

## Overview
MUKALMA is a chatbot which specializes in incorporating knowledge from a knowledge source into its responses. A user can select a topic to discuss, and start a conversation with MUKALMA. MUKALMA can perform well across the entire spectrum of message types that are possible over the course of a knowledgable discussion. It is capable of conducting chit-chat, answering explicit questions, and everything in between.

## Run MUKALMA
1. Navigate to `src/front_end/api`
2. Run the flask app using the command `flask run`. The API serving the model should be running.
3. Navigate to the `src/front_end/chat` directory
4. Run `npm build` to build all of the required node modules
5. Run `npm start` to start the ReactJS web application

## Support
Contact us via email:
- [Farjad Ilyas](mailto:ilyasfarjad@gmail.com?subject=[GitHub]%20Source%20Han%20Sans)
- [Nabeel Danish](mailto:nabeelben@gmail.com?subject=[GitHub]%20Source%20Han%20Sans)
- [Saad Saqlain](mailto:i180694@nu.edu.pksubject=[GitHub]%20Source%20Han%20Sans)

## Roadmap
- Use topic modelling to enable dynamic fetching of knowledge sources from Wikipedia
- Introduce a controller to enable MUKALMA to have token-level control over the output sequence it generates. Currently, the retrieved knwoledge phrase is incorporated into a knowledge-grounded response as-is
