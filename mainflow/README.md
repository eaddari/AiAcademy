# EY Junior Accelerator

**AI-Powered Personalized Learning Plan Generator**

Un sistema multi-agente avanzato che utilizza CrewAI per creare piani di studio personalizzati basati sul background, esperienza e obiettivi di apprendimento dell'utente. Il sistema combina ricerca web, analisi di paper accademici e pianificazione intelligente per fornire un percorso di apprendimento completo e strutturato.

## 🎯 Panoramica

Il **Junior Accelerator** è un'applicazione AI che automatizza la creazione di piani di studio personalizzati attraverso un workflow orchestrato di agenti specializzati. Ogni agente ha competenze specifiche che contribuiscono alla generazione di un piano di apprendimento completo e ottimizzato.

### Caratteristiche Principali

- **🤖 Sistema Multi-Agente**: 6 agenti CrewAI specializzati che lavorano in sequenza
- **🌐 Interfaccia Web Streamlit**: Frontend intuitivo e responsive
- **📊 Monitoraggio MLflow**: Tracking completo delle performance e metriche
- **🔍 Ricerca Intelligente**: Integrazione con risorse web e paper accademici
- **📅 Pianificazione Automatica**: Generazione di calendari di studio strutturati
- **💾 Export Multi-formato**: Download di tutti i risultati in formato Markdown

## 🏗️ Architettura del Sistema

### Workflow degli Agenti

Il sistema segue un flusso sequenziale orchestrato:

1. **InputValidationCrew** - Sanitizzazione e validazione dell'input utente
2. **PlanningCrew** - Generazione del piano di studio iniziale
3. **WebCrew** - Ricerca di risorse online pertinenti
4. **PaperCrew** - Ricerca di paper accademici rilevanti
5. **CalendarCrew** - Creazione del calendario di studio
6. **FinalStudyPlanCrew** - Assemblaggio del piano finale

### Struttura del Progetto

```
mainflow/
├── streamlit_app.py              # Applicazione Streamlit principale
├── pyproject.toml               # Configurazione dipendenze e progetto
├── src/
│   └── mainflow/
│       ├── main.py             # Flow principale CrewAI
│       ├── crews/              # Agenti specializzati
│       │   ├── input_crew/     # Validazione input
│       │   ├── planner_crew/   # Pianificazione iniziale
│       │   ├── web_crew/       # Ricerca web
│       │   ├── paper_crew/     # Ricerca accademica
│       │   ├── calendar_crew/  # Pianificazione temporale
│       │   └── study_plan_crew/# Piano finale
│       ├── components/         # Componenti condivisi
│       └── utils/             # Utilità e validazioni
├── frontend/
│   ├── utils/                 # Gestione stili UI
│   ├── pics/                  # Asset grafici
│   └── styles/                # CSS personalizzati
├── docs/                      # Documentazione Sphinx
├── tests/                     # Test suite
├── output/                    # File generati
└── mlruns/                   # Dati MLflow
```

## 🚀 Installazione e Setup

### Prerequisiti

- **Python**: >=3.10, <3.14
- **UV**: Package manager raccomandato per gestione dipendenze
- **Chiavi API**: OpenAI API key configurata

### Installazione

1. **Installa UV** (se non presente):
   ```bash
   pip install uv
   ```

2. **Clona e naviga nel progetto**:
   ```bash
   cd mainflow
   ```

3. **Installa dipendenze**:
   ```bash
   uv install
   # oppure
   pip install -e .
   ```

4. **Configura variabili d'ambiente**:
   Crea un file `.env` nella root del progetto:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint  # Se usi Azure OpenAI
   AZURE_OPENAI_API_KEY=your_azure_api_key    # Se usi Azure OpenAI
   ```

### Dipendenze Principali

```toml
dependencies = [
    "arxiv>=2.2.0",                    # Accesso paper accademici
    "crewai[tools]>=0.175.0,<1.0.0",  # Framework multi-agente
    "langchain-openai>=0.2.14",       # Integrazione LLM
    "streamlit>=1.28.0",               # Frontend web
    "mlflow>=3.1",                     # Monitoraggio ML
    "plotly>=5.15.0",                  # Visualizzazioni
    "pandas>=2.0.0",                   # Gestione dati
    "numpy>=1.24.0"                    # Calcoli numerici
]
```

## 🖥️ Utilizzo

### Interfaccia Web (Raccomandato)

1. **Avvia l'applicazione Streamlit**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Apri il browser** su `http://localhost:8501`

3. **Utilizza l'interfaccia**:
   - Accetta il disclaimer AI
   - Inserisci background, esperienza e obiettivi
   - Clicca "Generate My Study Plan"
   - Monitora il progresso degli agenti
   - Scarica i risultati generati

### CLI (Comando Diretto)

Per utilizzare il sistema via command line:

```bash
crewai run
# oppure
python -m mainflow.main
```

## 📊 Monitoraggio e Analytics

Il sistema integra **MLflow** per un monitoraggio completo:

### Metriche Tracciate

- **Token Usage**: Conteggio token per ogni agente
- **Costi Stimati**: Calcolo costi GPT-4.1 in EUR
- **Tempi di Esecuzione**: Performance temporali
- **Quality Scores**: Valutazione qualità output
- **Workflow Status**: Stato completamento

### Accesso MLflow

```bash
mlflow ui
```
Apri `http://localhost:5000` per visualizzare dashboard

### Esperimenti

- **Esperimento Principale**: "EY Junior Accelerator"
- **Run Naming**: Identificazione automatica per tipo di operazione
- **Nested Runs**: Ogni crew genera un run figlio

## 🎛️ Configurazione Avanzata

### Personalizzazione Agenti

Ogni crew può essere personalizzata modificando:

```python
# Esempio: src/mainflow/crews/planner_crew/crew.py
@agent
def planner_agent(self):
    return Agent(
        config=self.agents_config['planner_agent'],
        llm=self.llm,
        verbose=True,
        # Personalizza qui role, goal, backstory
    )
```

### Configurazione UI

Modifica `frontend/styles/main.css` per personalizzare l'aspetto:

```css
/* Personalizzazioni tema */
.main-header {
    background: linear-gradient(90deg, #1f4e79, #2d5a87);
}
```

### Validazione Input

Il sistema include validazione robusta in `src/mainflow/utils/input_validation.py`:

```python
def is_valid_input(user_input: str) -> bool:
    # Logica di validazione personalizzabile
    return True  # Implementa le tue regole
```

## 📈 Risultati e Output

### File Generati

Il sistema produce 4 file principali:

1. **Study Plan** (`my_study_plan.md`): Piano completo e dettagliato
2. **Resources** (`learning_resources.md`): Risorse web curate
3. **Papers** (`academic_papers.md`): Paper accademici rilevanti
4. **Calendar** (`study_calendar.md`): Pianificazione temporale

### Formato Output

Tutti gli output sono in **Markdown** per:
- Facile lettura e modifica
- Compatibilità cross-platform
- Integrazione con sistemi di documentazione

## 🧪 Testing e Sviluppo

### Struttura Test

```bash
tests/
├── __init__.py
├── monitoring.py           # Test monitoraggio
└── output/                # Risultati test
```

### Esecuzione Test

```bash
# Test specifici
python -m pytest tests/

# Test con coverage
python -m pytest tests/ --cov=src/mainflow
```

### Sviluppo

```bash
# Modalità development
pip install -e ".[dev]"

# Linting
flake8 src/

# Formatting
black src/
```

## 📚 Documentazione

### Generazione Docs

La documentazione è gestita con **Sphinx**:

```bash
cd docs/
# Windows
.\generate-docs.ps1

# Unix
./generate-docs.sh
```

### Struttura Documentazione

```
docs/
├── index.rst              # Homepage documentazione
├── getting-started.rst    # Guida introduttiva
├── api-reference.rst      # Riferimenti API
├── crews.rst             # Documentazione agenti
└── _build/html/          # Documentazione generata
```

## 🚨 Troubleshooting

### Problemi Comuni

**1. Errore Chiavi API**
```bash
# Verifica variabili d'ambiente
echo $OPENAI_API_KEY
```

**2. Dipendenze Mancanti**
```bash
# Reinstallazione completa
uv install --force-reinstall
```

**3. Errori Streamlit**
```bash
# Cache cleanup
streamlit cache clear
```

### Debug Mode

Attiva logging dettagliato:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contribuire

### Workflow Contributi

1. Fork del repository
2. Crea feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Apri Pull Request

### Standard Coding

- **PEP 8** compliance
- **Type hints** obbligatori
- **Docstrings** per funzioni pubbliche
- **Test coverage** > 80%

## 📄 Licenza

Questo progetto è sviluppato per **EY Junior Accelerator Program**.

## 🔗 Risorse e Support

### Framework e Tecnologie

- **[CrewAI](https://crewai.com)** - Framework multi-agente
- **[Streamlit](https://streamlit.io)** - Framework web app
- **[MLflow](https://mlflow.org)** - ML lifecycle management
- **[LangChain](https://langchain.com)** - LLM orchestration

### Community e Support

- **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
- **GitHub Issues**: Per bug reports e feature requests
- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)

---

**🚀 Sviluppato con AI per accelerare l'apprendimento del futuro**
