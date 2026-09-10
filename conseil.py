import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from ddgs import DDGS
load_dotenv()


client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=os.environ["OPENROUTER_API_KEY"])

CONSEIL = ["openai/gpt-5-mini",        # le débatteur américain
           "deepseek/deepseek-r1",
           "qwen/qwen3-235b-a22b",
           "moonshotai/kimi-k2.5"]

# juge = "anthropic/claude-sonnet-4.6"

outils = [
    {
        "type": "function",
        "function": {
            "name": "recherche_web",
            "description": "Cherche des informations récentes ou factuelles sur le web.",
            "parameters": {
                "type": "object",
                "properties": {
                    "requete": {
                        "type": "string",
                        "description": "Les mots-clés à rechercher.",
                    }
                },
                "required": ["requete"],
            },
        },
    }
]


def recherche_web(requete, nb_resultats=5):
    try:
        resultats = DDGS().text(requete, max_results=nb_resultats)
        if not resultats:
            return "Aucun résultat trouvé."
        return "\n".join(
            f"- {r['title']} : {r['body']} ({r['href']})" for r in resultats
        )
    except Exception as e:
        return f"Erreur de recherche web : {e}"


def demander(texte, model, max_tokens=1000, temperature=0.3):
    if texte == "":
        return None

    messages = [{"role": "user", "content": texte}]

    try:
        reponse = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            tools=outils,
            messages=messages,
        )
        message = reponse.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        appel = message.tool_calls[0]
        arguments = json.loads(appel.function.arguments)
        resultat = recherche_web(arguments["requete"])

        messages.append({
            "role": "tool",
            "tool_call_id": appel.id,
            "content": resultat,
        })

        reponse2 = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
        )
        return reponse2.choices[0].message.content

    except Exception as e:
        print(f"[{model}] erreur : {e}")
        return None


def formater(avis):
    bloc = ""
    for i in range(len(avis)):
        bloc += f"--- Membre {i+1} ---\n{avis[i]}\n\n"
    return bloc


def tour1(question):
    avis = []
    for m in CONSEIL:
        avis.append(demander(question, m))
    return avis


def tour2(question, avis):
    bloc = formater(avis)
    avis2 = []
    for i in range(len(CONSEIL)):
        prompt = (f"Question :\n{question}\n\n"
                  f"Voici les avis de tous les membres :\n{bloc}"
                  f"Tu es le Membre {i+1}. Corrige-toi si tu t'es trompé, "
                  "ou maintiens ta position en expliquant pourquoi.")
        avis2.append(demander(prompt, CONSEIL[i]))
    return avis2


def synthetiser(question, avis, juge = "anthropic/claude-sonnet-4.6"):
    prompt = (f"Question :\n{question}\n\n{formater(avis)}"
              "Tu présides le conseil. Indique d'abord sur quoi les membres "
              "divergent réellement, puis donne la réponse finale.")
    return demander(prompt, juge, max_tokens=1500)


def conseil(question):
    avis = tour1(question)
    avis = tour2(question, avis)
    return synthetiser(question, avis)


print(demander("Dis bonjour.", "deepseek/deepseek-chat"))   # test rapide
print(conseil(input("Question : ")))
