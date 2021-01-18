import json
import config
import requests
import sys

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import EmotionOptions, Features, SentimentOptions


class Colors:
    OK = "\u001b[38;2;0;255;0m"
    UNCERTAIN = "\u001b[38;2;252;161;3m"
    BAD = "\u001b[38;2;255;0;0m"
    END = "\u001b[0m"


def nluAnalyzer(url):
    authenticator = IAMAuthenticator(config.NLU_APIKEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2020-08-01", authenticator=authenticator
    )
    natural_language_understanding.set_service_url(config.NLU_URL)
    nlp_response = natural_language_understanding.analyze(
        url=url,
        features=Features(
            metadata={},
            sentiment=SentimentOptions(),
            emotion=EmotionOptions(),
        ),
    ).get_result()

    return processData(nlp_response)


def processData(nlp_response):
    title = ""
    authors = []
    sentiment_score = ""
    sentiment_label = ""
    emotions = []
    for key, value in nlp_response.items():
        if key == "metadata":
            title = value["title"]
            authors = value["authors"]
            if(title == "") or authors == []:
                sys.exit()
        elif key == "sentiment":
            for key, value in value.items():
                if(key == "document"):
                    for key, value in value.items():
                        if(key == "score"):
                            sentiment_score = value
                        elif(key == "label"):
                            sentiment_label = value
        elif key == "emotion":
            for key, value in value["document"]["emotion"].items():
                emotions.append(str(key) + ": " + str(value))
    
    return (title, authors, sentiment_score, sentiment_label, emotions)


if __name__ == "__main__":
    args = sys.argv
    url = args[1]
    content = ""
    nlp_response = nluAnalyzer(
        url=url,
    )
    if(len(args) > 2):
        content = args[2]
        nlp_response = nluAnalyzer(
            url=url,
        )

        response = requests.post("http://localhost:8080/fakebox/check", data={
            "url": url,
            "title": nlp_response[0],
            "content": content,
        })
    else:
        nlp_response = nluAnalyzer(
            url=url,
        )
        response = requests.post("http://localhost:8080/fakebox/check", data={
            "url": url,
            "title": nlp_response[0],
        })
    authors = ""
    for author in nlp_response[1]:
        for key, value in author.items():
            value.replace("  ", " ")
            authors = (authors + value + ", ")

    print(f"[Article Title] - {nlp_response[0]}")
    print(f"[Authors] - {authors}")
    temp = response.json()
    decision = temp["title"]["decision"]
    score = temp['title']['score']
    score = round(score, ndigits=4)
    if(decision == "bias"):
        print(f"{Colors.BAD}[Decision] - Biased{Colors.END}")
        print(f"[Confidence] - {score*100}%")
        if(score > 0.7):
            print(
                "[Analysis] - There is a high chance this article is biased and not safe to read")
        elif(score > 0.4):
            print("[Analysis] - There is a decent chance that this article is biased")
        else:
            print("[Analysis] - There is a low possibility that this article is biased")
    elif(decision == "impartial"):
        print(f"{Colors.OK}[Decision] - Impartial{Colors.END}")
        print(f"[Confidence] - {score*100}%")
        if(score > 0.7):
            print(
                "[Analysis] - There is a high chance this article is not biased and safe to read")
        elif(score > 0.4):
            print(
                "[Analysis] - There is a decent chance that this article is not biased")
        else:
            print(
                "[Analysis] - There is a low possibility that this article is not biased")
    else:
        print(f"[{Colors.UNCERTAIN}Decision] - Uncertain{Colors.END}")
        print(f"[Confidence] - {score*100}%")
        print("[Analysis] - We are unsure about this article... take what you are reading with a grain of salt")
    if(content != ""):
        content_decision = temp["content"]["decision"]
        content_score = temp["content"]["score"]
        print(f"[Content Decision] - {str(content_decision).capitalize()}")
        print(f"[Content Score] - {content_score}")
    domain_category = temp["domain"]["category"]
    print(f"[Domain Category] - {domain_category}")
    print(f"[Document Level Sentiment] - {nlp_response[3]}")
    print(f"[Document Level Score] - {nlp_response[2]}")
    print(f"[Document Level Emotions] - {str(nlp_response[4])}")
