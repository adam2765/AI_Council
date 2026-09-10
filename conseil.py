import os
import json
from openai import OpenAI
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=os.environ["OPENROUTER_API_KEY"])

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

CONSEIL = ["openai/gpt-5-mini",        # le débatteur américain
           "deepseek/deepseek-r1",
           "qwen/qwen3-235b-a22b",
           "moonshotai/kimi-k2.5"]

# juge = "anthropic/claude-sonnet-4.6"

OUTILS = [{
    "type": "function",
    "function": {
        "name": "recherche_web",
        "description": ("Cherche une information à jour sur le web. "
                        "À utiliser quand la réponse dépend de faits "
                        "récents ou vérifiables."),
        "parameters": {
            "type": "object",
            "properties": {
                "requete": {
                    "type": "string",
                    "description": "Les mots-clés de la recherche"
                }
            },
            "required": ["requete"]
        }
    }
}]


def recherche_web(requete):
    if requete == "":
        return "Requête vide."
    try:
        resultats = tavily.search(requete)["results"][:3]
        bloc = ""
        for r in resultats:
            bloc += f"--- {r['title']} ---\n{r['content']}\n\n"
        return bloc
    except Exception as e:
        return f"Erreur de recherche : {e}"


def demander(texte, model, max_tokens=1000, temperature=0.3):
    if texte == "":
        return None

    messages = [{"role": "user", "content": texte}]

    try:
        reponse = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            tools=OUTILS,
            messages=messages)
        message = reponse.choices[0].message

        # Pas d'outil demandé : réponse directe
        if not message.tool_calls:
            return message.content

        # Outil demandé : on garde sa demande dans l'historique
        messages.append(message)

        appel = message.tool_calls[0]
        arguments = json.loads(appel.function.arguments)
        resultat = recherche_web(arguments["requete"])

        messages.append({
            "role": "tool",
            "tool_call_id": appel.id,
            "content": resultat})

        # 2e appel : il lit le résultat et rédige
        reponse2 = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages)
        return reponse2.choices[0].message.content

    except Exception as e:
        print(f"[{model}] erreur : {e}")
        return None


def formater(avis):
    bloc = ""
    for i in range(len(avis)):
        if avis[i] is None:
            continue
        bloc += f"--- Membre {i+1} ---\n{avis[i]}\n\n"
    return bloc


def tour1(question):
    avis = []
    for m in CONSEIL:
        avis.append(demander(question, m, temperature=0.8))
    return avis


def tour2(question, avis):
    bloc = formater(avis)
    avis2 = []
    for i in range(len(CONSEIL)):
        prompt = (f"Question :\n{question}\n\n"
                  f"Voici les avis de tous les membres :\n{bloc}"
                  f"Tu es le Membre {i+1}. Identifie les faiblesses des "
                  "autres avis. Ne change de position que si un argument "
                  "précis te fait changer d'avis.")
        avis2.append(demander(prompt, CONSEIL[i]))
    return avis2


def synthetiser(question, avis, juge="anthropic/claude-sonnet-4.6"):
    prompt = (f"Question :\n{question}\n\n{formater(avis)}"
              "Tu présides le conseil. Indique d'abord sur quoi les membres "
              "divergent réellement, puis donne la réponse finale.")
    return demander(prompt, juge, max_tokens=1500)


def conseil(question):
    avis = tour1(question)
    avis = tour2(question, avis)
    return synthetiser(question, avis)


print(conseil(input("Question : ")))
