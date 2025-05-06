# AOE RAG

Eine einfache RAG-Anwendung, die auf den Inhalten der AOE-Website basiert.

## Installation

```bash
uv sync
```

## Konfiguration

.env.example kopieren und in .env umbenennen. Die Umgebungsvariablen anpassen.

```bash
cp .env.example .env
```

## Starten

```bash
uv run main.py
```

## Frameworks, Bibliotheken

Ich verwende `LlamaIndex` für den RAG-Workflow. Es bietet viele Features out of the box und ist einfach zu verwenden. Workflows und Agenten sind auch möglich.

`Haystack` wäre auch eine valide Option gewesen, aber ich habe mich für dagegen entschieden, weil LlamaIndex populärer ist und ich mehr Erfahrung damit habe.

`LangGraph` ist stark im Abbilden komplexer Agents und Workflows. In diesem Fall liegt der Fokus aber auf der RAG-Architektur, deshalb habe ich es nicht verwendet. Die Features von `LlamaIndex` sollten dafür ausreichen.

`LangChain` ist aus der Mode gekommen durch die Komplexität, dehsalb habe ich es nicht verwendet.

## Datenquellen

Diese Seiten wurden als Datenquellen verwendet:

- [Start](https://www.aoe.com/de)
- [Services: Automation Ai](https://www.aoe.com/de/services/automation-ai)
- [Services: Digital Experience](https://www.aoe.com/de/services/digital-experience)
- [Branche: Telecommunications](https://www.aoe.com/de/branchen/telecommunications)
- [Werte, Kultur](https://www.aoe.com/de/ueber-uns/values-culture)

## Chunking

Für das Chunking verwende ich den `SentenceSplitter` von `LlamaIndex`. Dadurch wird sichergestellt, dass die Chunks nicht zu lang sind und die Struktur der Sätze erhalten bleibt.

Alternativ wäre der `SentenceSplitter` eine gute Wahl, allerdings funktioniert er [primär mit englischen Texten](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/).

Die Chunks sind möglichst groß, da das verwendete LLM ein großes Kontextfenster hat.

## Embeddings

Ich verwende die `text-embedding-3-large` von OpenAI. Mit unkomplizierten Texten wie den AOE-Seiten habe ich auch mit `text-embedding-3-small` gute Erfahrungen gemacht. Meistens sind die Kosten entscheident - in diesem Fall ist die Menge an Tokens aber überschaubar, daher ist der Preisunterschied nicht entscheidend.

Andere Alternativen habe ich vorerst ausgeschlossen, da ich der Einfachheit halber nur Modelle von OpenAI verwenden möchte.

## Speicherung

Zum Speichern des Index verwende ich die In-Memory-Datenbank von `LlamaIndex`. Diese ist einfach zu verwenden und benötigt keine zusätzliche Konfiguration.

`Postgres` mit `pgvector` wäre eine gute Alternative für einen separaten Speicher. Sie passt besonders gut, wenn die Postgres-Datenbank auch für andere Zwecke in der Anwendung verwendet wird.

Speziallisierte Vektordatenbanken wie `Milvus` oder `Qdrant` wären bei größeren Datenmengen sinnvoll. Sie bieten eine bessere Leistung und Skalierbarkeit, sind aber auch komplexer in der Einrichtung und Verwaltung. In diesem Fall wären sie etwas überdimensioniert.

## Retrieval

Mit dem Response-Mode `refine` habe ich auf Anhieb die besten Antworten erhalten. Dabei werden die Chunks nacheinander an das LLM übergeben, und das LLM verfeinert die Antwort mit jedem Chunk - dadurch ist die Antwort präziser und relevanter.

Beim testen verwende ich `compact`, um Requests zu sparen. Dafür werden die Chunks in einem einzigen Request an das LLM übergeben. Das Ergebnis ist nicht so gut wie bei `refine`, aber immer noch akzeptabel. Bei größeren Datenmengen kann es auch zu Problemen mit der Tokenanzahl kommen, da alle Chunks in einem Request verarbeitet werden müssen.

## Generation

Die Generierung der Antworten erfolgt mit `gpt-4.1-nano`. Das Modell ist noch neu und soll stabile performance bieten bei sehr niedrigen Kosten. Das Kontextfenster ist mit etwa 1 Millionen Tokens sehr groß, dadurch können problemlos große Chunks verarbeiten.

## LLM

Freie Modelle wären auch möglich gewesen. Lokal habe ich mit `Deepseek` und `Qwen6B` sehr gute Erfahrungen gemacht. Die Modelle sind schnell und bieten eine gute Leistung. Allerdings ist die Qualität der Antworten nicht so gut wie bei den OpenAI-Modellen.

Lokal ließen sich die Modelle leicht über `Ollama` oder `LmStudio` einbinden. In Production wäre es am einfachsten einen Service wie Azure zu verwenden, um die Modelle zu hosten. Das Setup konnte ich mir sparen durch die API von OpenAI.

## Einschränkungen

- Die Inhalte basieren auf manuell hinterlegten Daten. Das bedeutet, dass die Antworten nicht immer aktuell sind und möglicherweise nicht alle Informationen enthalten.
- Es gibt noch kein Interface, um zu chatten

## Verbesserungsvorschläge für produktive Nutzung

- Dynamische Abfrage der AOE-Website
- Agent, der nach bedarft die Website abfragt und den Index aktualisiert
- Je nach Kontext in dem die Anwendung verwendet wird entweder:
    - ein CLI-Interface
    - eine Webanwendung
    - eine API
- Daten, die den State repräsentieren, sollten separat gespeichert werden, damit sie nicht verloren gehen, wenn die Anwendung neu gestartet wird
- Containerisierung der Anwendung, um sie einfach zu deployen
- Inhaltliche Tests und Metriken, um die RAG-Qualität zu gewährleisten
