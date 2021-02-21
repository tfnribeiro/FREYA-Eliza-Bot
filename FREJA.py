# -*- coding: utf-8 -*-
# FREJA - A Danish Inspired ELIZA

import random as r
import re
import os
import codecs

reflections = {
    "jeg":"du",
    "mig":"dig",
    "min":"din",
    "mit":"dit",
    "mine":"dine",
    "dig":"mig"
    "din":"min",
    "dit":"mit",
    "dine":"mine"
}

pychoAnalysis = [
    [r'Jeg har brug for (.*)',
    ["Hvorfor har du brug for {0}?",
    "Skulle det virkelige hjælpe dig at få {0}?",
    "Er du sikkert at du har brug for {0}?"
    ]],
    [r'Hvorfor vil du ikke ([^\?]*)\??',
    ["Er du sikkert jeg vil ikke {0}?",
    "Måske kommer jeg til at {0}.",
    "Vil du virkelig at jeg {0}?"
    ]],
    [r'Hvorfor kan jeg ikke ([^\?]*)\??',
    ["Tror du, at du skulle {0}?",
    "Hvis du kunne {0}, hvad ville du så gøre?",
    "Jeg ved ikke -- hvorfor kan du ikke {0}?",
    "Har du virkelig prøvet at {0}?"
    ]],
    [r'Jeg kan ikke (.*)',
    ["Hvordan ved du at du kan ikke {0}?",
    "Måske kan du {0}, hvis du prøve at gøre det."
    "Hvad skulle det være, så du kan {0}?"
    ]],
    [r'Jeg er (.*)',
    ["Har du kommet til mig fordi du er {0}?",
    "Hvor længe har du været {0}?",
    "Hvordan føler du om at være {0}?",
    "Hvorfor tror du at du er {0}?"
    ]],
    [r'Er du ([^\?]*)\??',
    ["Hvorfor er det vigtigt at jeg er {0}?",
    "Vil du hellere at jeg var ikke {0}?",
    "Muligvis, tror du at jeg er {0}?",
    "Jeg er måske {0} -- hvad synes du?"
    ]],
    [r'Hvad (.*)',
    ["Hvorfor spørger du det?",
    "Hvordan skullen en svar til det hjælpe dig?",
    "Hvad synes du?"
    ]],
    [r'Hvordan (.*)',[
    "Hvordan tror du?",
    "Måske kan du svar dine egne spørgsmål?",
    "Hvad er det du spørger om endelig?"
    ]],
    [r'Fordi (.*)',
    ["Er det nemlig gruden?",
    "Hvad andre grunde kan du tænke på?",
    "Passer det til noget andet?",
    "Hvis {0}, hvad kunne det være til at blive bedre?"
    ]],
    [r'(.*) udskyld (.*)',
    ["Der er ingen grund til at sige undskyld.",
    "Hvilke føler har du når du undskylde?"
    ]],
    [r'Hej(.*)?',
    ["Hej... Det glæder mig at se dig.",
    "Hej der... Hvordan har du det i dag?",
    "Hej, hvordan går det?"
    ]],
    [r'Jeg tror (.*)',
    ["Tror du virkelig {0}?",
    "Tror du virkelig det?",
    "Men er du ikke sikkert om {0}?"
    ]],
    [r'(.*) ven[n,i]?.+ (.*)',
    ["Fortæl mig mere om dine venner.",
    "Når du tænker på dine venner, hvordan føler du?",
    "Vil du ikke fortæl mig om en ven eller en veninde fra din barndom?"
    ]],
    [r'Ja',
    ["Du ser meget sikkert.",
    "OK, men kan du sige lidt mere?"
    "Kan du uddybe det?"
    ]],
    [r'(.*)computer(.*)',
    ["Snakker du om mig?",
    "Føler det mærkeligt at snakke med en computer?",
    "Hvordan føler du ift. computere?",
    "Er du bange for computere?"
    ]],
    [r'(.*)bot(.*)',
    ["Snakker du om mig?",
    "Føler det mærkelig at snakke med in computer?",
    "Hvordan føler du ift. computere?",
    "Er du bange for computere?"
    ]],
    [r'Er (.*)',
    ["Tror du virkelig at {0}?",
    "Måske {0} -- hvad synes du?",
    "Hvis det var {0}, hvad vil du gøre?",
    "Det kunne godt være {0}."]],
    [r'De[n,t]? er (.*)',
    ["Du er meget sikkert.",
    "Hvis jeg fortalt dig det er ikke {0}, hvordan skulle du så føle?"
    ]],
    [r'Kan du ([^\?]*)\??',
    ["Hvorfor tror du jeg kan ikke {0}?",
    "Hvis jeg kunne {0}, så hvad?",
    "Hvorfor spørger du efter, at jeg {0}?"
    ]],
    [r'Kan jeg ([^\?]*)\??',
    ["Måske vil du ikke {0}?",
    "Vil du være gode til {0}?",
    "Hvis du kunne {0},ville du?"
    ]],
    [r'Du er (.*)',
    ["Hvorfor siger du at jeg er {0}?",
    "Vil du at jeg er {0}?",
    "Snakker du om dig, eller mig?",
    "Måske snakker du endlig om digselv?"
    ]],
    [r'Jeg er ikke (.*)',
    ["Er du virkelig ikke {0}?",
    "Hvorfor er du ikke {0}?",
    "Vil du gerne at {0}?"
    ]],
    [r'Jeg føler (.*)',
    ["Godt, så fortæl mig mere om dine følser.",
    "Føler du tit {0}?",
    "Hvornår føler du {0}?",
    "Når du føler {0}, hvad gør du?"
    ]],
    [r'Jeg har (.*)',
    ["Hvorfor fortalt du mig at du har {0}?",
    "Har du virkelig {0}?",
    "Nu, har du {0}, hvad vil du gøre så?"
    ]],
    [r'Jeg vil (.*)',
    ["Kan du forklar hvorfor du vil {0}?",
    "Hvorfor vil du {0}?",
    "Hvad ellers vil du {0}?"
    ]],
    [r'Er der (.*)',
    ["Tror du, at der er virkelig {0}?",
    "Det er mulligivis at der er {0}.",
    "Ville du gerne at der var {0}?"
    ]],
    [r'Min (.*)',
    ["Nu forstår jeg, din {0}",
    "Hvorfor siger du din {0}",
    "Når din {0}, hvordan føler du?"
    ]],
    [r'Du (.*)',
    ["Vi skulle snakke om dig, ikke mig",
    "Hvorfor siger du det om mig?",
    "Hvorfor gider du om hvis jeg {0}?"
    ]],
    [r'Hvorfor (.*)',
    ["Hvorfor fortaller du ikke grunde at {0}?",
    "Hvorfor tror du {0}?"
    ]],
    [r'Tak(.*)',
    ["Så lidt! Håber du føler bedre.",
    "Det glæader mig at høre det."
    ]],
    [r'Jeg vil (.*)',
    ["Hvad betyder det hvis du fik {0}?",
    "Hvorfor vil du det?",
    "Hvad skulle du gøre hvis du havde {0}?"
    ]],
    [r'(.*) mor(.*)',
    ["Fortæl mig mere om din mor.",
    "Hvordan var dit forhold med din mor?",
    "Hvordan føler du om din mor?",
    "Hvordan kan du relatere det til dine føleser idag?",
    "Godt familie forholder er vigtig."
    ]],
    [r'(.*) far(.*)',
    ["Fortæl mig mere om din far.",
    "Hvordan var dit forhold med din far?",
    "Hvordan føler du om din far?",
    "Hvordan kan du relatere det til dine føleser idag?",
    "Har du problemer med at vise kærlighed med dine familie?"
    ]],
    [r'(.*) barn(.*)',
    ["Havde du tæt venner som barn?",
    "Hvad er dine undlyingshukommelse som barn?",
    "Kan du huske drømmer eller mareridter fra dine barndom?",
    "Hvordan tror du at dine barndom påvirker dine føler idag?"
    ]],
    [r'(.*)\?',
    ["Hvorfor spurgte du det?",
    "Har du måske allerede tænkte på et svar til din spørgsmål?",
    "Måske din svar er inde i digselv?",
    "Hvorfor fortaler du ikke mig om det?"
    ]],
    [r'quit',
    ["Tak for samtale",
    "Favel!",
    "Det var en god samtale.",
    "Bliv positiv!"
    ]],
    [r'(.*)',
    ["Fortæl mig mere.",
    "Skal vi skifte emne?... Fortæl mig om dine familie.",
    "Kan du uddybe dine forklaring?",
    "Hvorfor siger du at {0}?",
    "Nå, nu forstår jeg.",
    "Virkelig interessant.",
    "{0}",
    "Nå... Hvad fortæller det til dig?",
    "Hvordan føler du om det?",
    "Hvordan føler du når du siger det?",
    ]]
]

def reflect(fragment):
    tokens = fragment.lower().split()
    reflection = ""
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    for token in tokens:
        reflection = reflection + token + " "
    return reflection

def analyse(statement):
    for pattern, responses in pychoAnalysis:
        match = re.match(pattern, statement.rstrip(".!"), re.IGNORECASE)
        if match:
            response = r.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])
    return "Jeg forstår ikke hvad du mener, kan du sige noget andet?"

# def convert(s):
#    replacement = {
#        "\\xc3\\xa6":"æ",
#        "\\xc3\\xa5":"å",
#        "\\xc3\\xb8":"oe",
#    }
#
#    chars = re.findall(r'(\\\w\w\d\\\w\w\d){1,}',str(s))
#    result =""
#    for i,char in enumerate(chars):
#        if char in replacement:
#            chars[i] = replacement[char]
#    for char in chars:
#        result = result + char
#    return result

def main():
    conversation = []
    print("Velkomme til FREJA, en slags ELIZA på dansk")
    print("Dvs. at FREJA kan hjælpe dig at tænke over emne, som en psycolog.")
    #print("***Bruge o eller oe til den danske vokal***")
    while True:
        statement = input("> ")
        if statement == "quit" or statement == "slut":
            f = open("conversation.txt","w+")
            for (u,b) in conversation:
                f.write("++USER++: " + (u) + "\n")
                f.write("++BOT++: " + (b) + "\n")
            f.write("---END---")
            f.close
            break
        response = analyse(statement)
        conversation.append((statement,response))
        print("FREJA:", response)

if __name__ == "__main__":
    main()