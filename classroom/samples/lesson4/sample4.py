import json

import requests


REST_PROXY_URL = "http://localhost:8082"


def get_topics():
    """Gets topics from REST Proxy"""
    # TODO: See: https://docs.confluent.io/current/kafka-rest/api.html#get--topics
    resp = requests.get(f"{REST_PROXY_URL}/topics")

    try:
        resp.raise_for_status()
    except:
        print("Failed to get topics {json.dumps(resp.json(), indent=2)})")
        return []

    print("Fetched topics from Kafka:")
    print(json.dumps(resp.json(), indent=2))
    return resp.json()



def get_topic(topic_name):
    """Get specific details on a topic"""
    # TODO: See: https://docs.confluent.io/current/kafka-rest/api.html#get--topics
    resp = requests.get(f"{REST_PROXY_URL}/topics/{topic_name}")

    try:
        resp.raise_for_status()
    except:
        print("Failed to get topics {json.dumps(resp.json(), indent=2)})")

    print("Fetched topics from Kafka:")
    print(json.dumps(resp.json(), indent=2))


def get_brokers():
    """Gets broker information"""
    # TODO See: https://docs.confluent.io/current/kafka-rest/api.html#get--brokers
    resp = requests.get(f"{REST_PROXY_URL}/brokers")

    try:
        resp.raise_for_status()
    except:
        print("Failed to get brokers {json.dumps(resp.json(), indent=2)})")

    print("Fetched brokers from Kafka:")
    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    topics = get_topics()
    get_topic(topics[0])
    get_brokers()
