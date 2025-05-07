# AOE RAG

Eine einfache RAG-Anwendung, die auf den Inhalten der AOE-Website basiert.

Beispiel:

```bash
👤 In einem Satz. Was ist AOE?

🤖 AOE ist ein Unternehmen, das digitale Potenziale durch Plattformen, Services und Beratung erschließt, um Unternehmen bei ihrer digitalen Transformation zu unterstützen, wobei die Unternehmenskultur auf Vertrauen, Offenheit, Zusammenarbeit und nachhaltigem Impact basiert, insbesondere im Bereich Automation, Künstliche Intelligenz und Digital Experience.
```

## Installation

Das Projekt verwendet `uv` als Paketmanager.
Hier ist eine [Installationsanleitung für `uv`](https://docs.astral.sh/uv/getting-started/installation/).

Um die Abhängigkeiten zu installieren, führe den folgenden Befehl in der Konsole aus:
```bash
uv sync
```

Als Linter/Formatter verwende ich `ruff`. Hier ist eine [Installationsanleitung für `ruff`](https://docs.astral.sh/ruff/installation/).

Der Linter kann einfach mit dem folgenden Befehl ausgeführt werden:
```bash
uv run ruff check  # alle Dateien im aktuellen Verzeichnis prüfen
uv run ruff format # alle Dateien im aktuellen Verzeichnis formatieren
```

## Konfiguration

Es gibt eine Beispielkonfiguration in der Datei `.env.example`. Diese Datei enthält alle Umgebungsvariablen, die für die Anwendung benötigt werden. Du kannst die Datei einfach kopieren, um sie zu aktivieren:

```bash
cp .env.example .env
```

Es gibt aktuell nur eine Umgebungsvariable:
- `OPENAI_API_KEY`: Dein OpenAI API-Key. Du kannst ihn [hier](https://platform.openai.com/signup) erstellen.

## Starten

Die Anwendung kann einfach mit dem folgenden Befehl über die Konsole gestartet werden:

```bash
uv run main.py
```

## Tests

Die Tests sind in der Datei [test_aoe_rag.py](./test_aoe_rag.py) enthalten. Sie verwenden `pytest` und können einfach mit dem folgenden Befehl ausgeführt werden:

```bash
uv run pytest
```

In der Datei [test_aoe_rag.py](./test_aoe_rag.py) gibt es auch Tests für die Relevanz der Antworten mit dem `QueryResponseEvaluator` von `LlamaIndex`.

## Frameworks, Bibliotheken

Ich verwende [`LlamaIndex`](https://docs.llamaindex.ai/en/stable/) für den RAG-Workflow. Es bietet viele Features out of the box und ist einfach zu verwenden. Workflows und Agenten sind auch möglich.

[`Haystack`](https://docs.haystack.deepset.ai/docs/get_started) sehe ich auch als valide Option, allerdings liegen für mich die Stärken eher im Aufbau komplexerer Pipelines. Für einfache RAG-Workflows ist `LlamaIndex` meiner Meinung nach die bessere Wahl.

`LangChain` gilt als [übermäßig komplex](https://www.octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents) und veraltet, deshalb habe ich mich dagegen entschieden.

Die Stärken von neueren Frameworks wie `LangGraph` und `Pydantic AI` sehe ich eher im Bereich von Agenten und Workflows.

## Datenquellen

Diese Seiten wurden als Datenquellen verwendet:

- [Start](https://www.aoe.com/de) · Für generelle Fragen zu AOE
- [Services: Automation Ai](https://www.aoe.com/de/services/automation-ai) · Weil es in der Challenge um den Einsatz von KI geht
- [Services: Digital Experience](https://www.aoe.com/de/services/digital-experience) · Ein beispielhafter Service von AOE
- [Branche: Telecommunications](https://www.aoe.com/de/branchen/telecommunications) · Ein Beispiel für eine Branche, in der AOE tätig ist
- [Werte, Kultur](https://www.aoe.com/de/ueber-uns/values-culture) · Für Fragen zu den Werten und der Kultur von AOE

Für den Prototyp habe ich die Seiten manuell als Bilder gespeichert und sie dann mit GPT-4o in Markdown umgewandelt. Das war der einfachste Weg, um die Inhalte zu extrahieren und die Struktur zu erhalten.

Sollte großflächiger gescraped werden, würde ich die Seiten mit `playwright` oder `selenium` scrapen. Da auf der Seite Inhalte per JavaScript nachgeladen werden, müsste der virtuelle Browser Scrollen, bis keine neuen Inhalte mehr erscheinen, um sicherzustellen, dass alle Inhalte geladen sind.

Passent dazu ist gerade [MarkItDown](https://www.thoughtworks.com/en-de/radar/languages-and-frameworks/summary/markitdown) im Thoughtworks Tech Radar auf 'Trial' und könnte eine gute Option sein, um die HTML-Seiten in Markdown umzuwandeln.

Der [Web Page Reader von LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/) könnte auch eine Option sein, wird aber wahrscheinlich nicht so gut mit den dynamischen Inhalten der AOE-Seite umgehen können.

## Chunking

Für das Chunking verwende ich den `SentenceSplitter` von `LlamaIndex`. Dadurch soll die Struktur der Texte erhalten bleiben. Die Chunks sind besonders groß gewählt (2048 Tokens), da das LLM ein großes Kontextfenster hat.

Alternativ wäre der `SemanticSplitter` eine gute Wahl, allerdings funktioniert er [primär mit englischen Texten](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/).

Durch die großen Chunks landen ganze Seiten in einem Chunk. Die Qualität der Antworten ist dadurch gut, allerdings könnte es bei größeren Datenmengen Sinn machen, die Chunks kleiner zu wählen, um die Qualität der Antworten zu verbessern. Vor allem bei Fragen, die sich auf spezifische Abschnitte beziehen.

## Embeddings

Für die Embeddings verwende ich das Modell `text-embedding-3-large` von OpenAI. Mit unkomplizierten Texten wie den AOE-Seiten habe ich auch mit `text-embedding-3-small` gute Erfahrungen gemacht. Meistens sind die Kosten entscheidend - in diesem Fall ist die Menge an Tokens aber überschaubar, daher ist der Preisunterschied nicht entscheidend.

Andere Alternativen habe ich vorerst ausgeschlossen, da ich der Einfachheit halber nur Modelle von OpenAI verwenden möchte.

## Speicherung

Zum Speichern des Index verwende ich die In-Memory-Datenbank von `LlamaIndex`. Diese ist einfach zu verwenden und benötigt keine zusätzliche Konfiguration. Die Daten werden im Arbeitsspeicher gehalten und als JSON-Datei lokal gespeichert. Das ist für den Prototypen in Ordnung, müsste allerdings in einer produktiven Umgebung angepasst werden.

Wenn die Anwendung noch eine eigene Datenbank benötigen würde, wäre `Postgres` mit `pgvector` eine gute Wahl.

Eine Cloud Lösung wie `Milvus` oder `Qdrant` fände ich für diesen Prototypen etwas überdimensioniert.

## Retrieval

In LlamaIndex können mit Hilfe von [Response Modes](https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/response_modes/) verschiedene Retrieval-Strategien verwendet werden.

Mit dem Response-Mode `refine` habe ich auf Anhieb die besten Antworten erhalten. Dabei werden die Chunks nacheinander an das LLM übergeben, und das LLM verfeinert die Antwort mit jedem Chunk.

Beim Testen verwende ich `compact`, um Requests zu sparen. Dafür werden die Chunks in einem einzigen Request an das LLM übergeben. Das Ergebnis ist nicht so gut wie bei `refine`, aber immer noch akzeptabel. Bei größeren Datenmengen könnte es auch zu Problemen mit der Tokenanzahl kommen, da alle Chunks in einem Request verarbeitet werden müssen.

## Generation

Die Generierung der Antworten erfolgt mit `gpt-4.1-nano`. Das Modell ist noch neu und bietet stabile Performance bei sehr niedrigen Kosten. Das Kontextfenster ist mit etwa 1 Millionen Tokens sehr groß, dadurch können problemlos große Chunks hineingeladen werden.

## LLM

Freie Modelle wären auch möglich gewesen. Lokal habe ich mit [`Deepseek R1 Distill (Qwen 7b)`](https://huggingface.co/lmstudio-community/DeepSeek-R1-Distill-Qwen-7B-GGUF) und [`Qwen3 4B`](https://ollama.com/library/qwen3) gute Erfahrungen gemacht. Die Modelle sind schnell und bieten eine gute Leistung. Allerdings ist die Qualität der Antworten nicht so gut wie bei den OpenAI-Modellen.

Lokal ließen sich die Modelle leicht über [`Ollama`](https://ollama.com) oder [`LmStudio`](https://lmstudio.ai) einbinden. In Production wäre es am einfachsten einen Service wie Azure zu verwenden, um die Modelle zu hosten. Das Setup konnte ich mir sparen durch die API von OpenAI.

## Agent

Aktuell ist noch kein Agent implementiert - das habe ich in der Zeit leider nicht mehr geschafft.

Ich sehe zwei Ansätze für Agenten:
1. **Ein Agent, der die AOE-Website nach Bedarf abfragt und die Daten in den Index speichert.**
    - Der Agent sucht bei Bedarf z.B. über die Google API nach den Inhalten der AOE-Website und fügt sie dem Index hinzu.
    - Der Agent Prüft, ob die Daten zu eine Seite aktuell sind (z.B. neuer als ein Monat) und aktualisiert sie gegebenenfalls.

2. **Ein Agentennetzwerk mit Spezialisten zu den einzelnen Bereichen der AOE-Webseite**
    - Für jeden Bereich der AOE-Webseite gibt es einen Agenten, der sich in diesem Bereich auskennt.
    - Ein Meta-Agent koordiniert die Agenten und leitet die Anfragen an den passenden Agent weiter.
    - Der Ansatz lässt sich mit der Idee von oben kombinieren, dass die Agenten auch die AOE-Webseite abfragen können, um ihre Daten aktuell zu halten.
    - Die Unteragenten könnten auf Dauer auch um Features erweitert werden, wie z.B. Kundenanfragen anzunehmen und weiterzuleiten.

## Einschränkungen

Die Inhalte basieren auf manuell hinterlegten Daten. Das bedeutet, dass die Antworten nicht immer aktuell sind und möglicherweise nicht alle Informationen enthalten.

Momentan ist die Anwendung auf deutsche Inhalte beschränkt.

## Verbesserungsvorschläge für produktive Nutzung

- Je nach Kontext in dem die Anwendung verwendet wird entweder:
    - ein CLI-Interface z.B. mit [`typer`](https://typer.tiangolo.com/)
    - eine Webanwendung z.B. mit [`Chainlit`](https://docs.chainlit.io/)
    - eine API z.B. mit [`FastAPI`](https://fastapi.tiangolo.com/)
- Ein Docker-Container für die Anwendung, um sie einfach zu deployen
    - Die Daten sollten in einem persistent Volume gespeichert werden, damit sie nicht verloren gehen, wenn der Container neu gestartet wird
- Ein CI/CD-Workflow, der die Tests automatisch ausführt existiert
    - er sollte auch die Anwendung automatisch deployen, wenn die Tests erfolgreich sind
- Logging und Metriken zur Überwachung der Qualität der Antworten und der Stabilität der Anwendung
    - Ein Monitoring-Tool wie der ELK-Stack
- Dynamische Abfrage der AOE-Website (je nachdem wie oft die Inhalte aktualisiert werden)
- Genauer definieren, welche Anfragen beantwortet werden sollen und [evaluieren, ob die Antworten passend sind](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/usage_pattern/)
