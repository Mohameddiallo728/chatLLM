# RAG Mistral

RAG Mistral est une application Streamlit qui utilise LangChain et différents modèles d'apprentissage automatique pour offrir une expérience de chat interactive. Les utilisateurs peuvent télécharger des documents PDF que l'application traite pour générer des embeddings et répondre aux requêtes des utilisateurs en fonction du contenu des documents.

![Architecture Simple](https://raw.githubusercontent.com/Mohameddiallo728/chatLLM/main/app-architecture.png)

![Architecture](https://raw.githubusercontent.com/Mohameddiallo728/chatLLM/main/architecture.png)

## Fonctionnalités

- Téléchargement de documents PDF pour traitement.
- Génération d'embeddings pour le contenu des documents.
- Interface de chat interactive pour interroger les informations des documents.
- Utilise des modèles de langage de pointe pour générer des réponses.

## Installation

### Prérequis

Assurez-vous d'avoir installé Python sur votre machine, Ollama et mistral en local.

Cet article médium vous permettra de faire l'installation complète si ce n'est pas le cas: 

[Local LLM Installation Guide: Install Llama3 using Ollama](https://medium.com/@sealteamsecs/local-llm-installation-guide-install-llama3-using-ollama-ef8cf68bb461)


1. Clonez le dépôt :

```bash
    git clone git@github.com:Mohameddiallo728/chatLLM.git
    cd chatLLM
```
2. Créez un environnement virtuel (optionnel mais recommandé) :

```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`
```
3. Installez les packages requis :

```bash
    pip install -r requirements.txt
```

## Utilisation

1. Démarrez l'application Streamlit :

 ```bash
    streamlit run app.py
 ```

2. Ouvrez votre navigateur web et accédez à http://localhost:8501.

3. Utilisez la barre latérale pour télécharger un fichier PDF. L'application traitera le document et le préparera pour l'interrogation.

4. Entrez vos questions dans l'interface de chat pour recevoir des réponses basées sur le document téléchargé.


## Contributions

Les contributions sont les bienvenues ! Si vous avez des idées d'améliorations, veuillez ouvrir une issue ou soumettre
une demande de fusion.

## Auteurs

    Nom : Mohamed DIALLO
    email : mohameddiallo728@gmail.com

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](https://opensource.org/licenses/MIT) pour plus de détails.
