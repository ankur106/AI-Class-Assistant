# AI-Class-Assistant

The AI Class Assistant is an innovative tool designed to revolutionize how you interact with your documents. By combining cutting-edge technologies like FastAPI, React, OpenAI, ElasticSearch, and Docker, this project allows you to effortlessly converse with your documents in real time. Whether you’re navigating complex reports, lengthy articles, or detailed papers, the assistant provides precise, context-aware answers to your questions, making information retrieval intuitive and engaging.

This system leverages custom system prompts to deliver accurate and tailored responses, ensuring that every interaction feels personalized and relevant. With its robust backend, sleek and dynamic frontend, blazing-fast search capabilities, and scalable Docker-based architecture, the AI class Assistant is built for efficiency and adaptability. Say goodbye to static documents and experience the future of document interaction as your information becomes a conversational partner. 🚀

![React_UI](/File/UI.png)

## Requirements
To set up the project it will require Docker, Python3 and Node.js.


## Installation and steps to run
1. Clone the repository from github.
2. UI is made with the React and here are the steps to run it locally(Node is prerequisite).
```
cd /Chat_UI
npm install
npm run dev
```
3. Elastic Search and Kibana in Docker
After  starting the docker via desktop or comand line utility run below code in terminal.
```
# Create network and pull elasticsearch and kibana images.

docker network create elastic

docker pull docker.elastic.co/elasticsearch/elasticsearch:8.16.0

docker pull docker.elastic.co/kibana/kibana:8.16.0


# Run Elaticsearch
docker run --name es_512 \
--net elastic \
-p 9200:9200 \
-it \
-m 1GB \
-e "xpack.security.enabled=false" \
-e "xpack.security.transport.ssl.enabled=false" \
-e "network.host=0.0.0.0" \
-e "discovery.type=single-node" \
docker.elastic.co/elasticsearch/elasticsearch:8.16.0


# Run Kibana
docker run --name kib_512 \
--net elastic \
-p 5601:5601 \
-it \
-e "SERVER_HOST=0.0.0.0" \
-e "ELASTICSEARCH_HOSTS=http://es_512:9200" \
-e "xpack.security.enabled=false" \
-e "xpack.monitoring.enabled=false" \
-e "xpack.graph.enabled=false" \
-e "xpack.ml.enabled=false" \
docker.elastic.co/kibana/kibana:8.16.0



```

4. Install virtual environment and RUN FAST API backend

```
# Open a new terminal and go into backend folder
cd /RAG-elasticsearch

# Create virtual environment first with below command
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate #(for Mac/Linux)
venv\Scripts\activate #(for Windows)

# Make an .env file and set OpenAI api key
OPENAI_API_KEY = your_api_key

# Install python libraries
pip install -r requirements.txt

# Run ingestion pipeline to add vectors in elasticsearch
cd ingestion_pipeline 
python elastic.ingestion.py
cd  ..


# run the FAST API backend
uvicorn app:app --reload


```

5. Open Below link in browser
```
http://localhost:5173/
```

##### Demo Video

Demo Video is /file/Demo.mov

