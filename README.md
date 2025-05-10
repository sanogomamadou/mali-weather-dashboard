# ⛅️ Dashboard Météo Temps Réel (Mali) avec Kafka, Elasticsearch et Kibana

Un projet full-stack Data Engineering qui permet de **surveiller en temps réel la météo dans les différentes villes du Mali** 🌍,
à partir de données injectées via Apache Kafka, stockées dans Elasticsearch, et visualisées dans un **dashboard Kibana interactif**.

---

## 🎯 Objectif

Concevoir un système qui permet de :

- Collecter les données météo en temps réel (Kafka)
- Les stocker efficacement dans Elasticsearch
- Les visualiser dynamiquement dans Kibana
- Identifier rapidement des **anomalies climatiques** (vents forts, pluie, températures extrêmes, humidité)

---

## 🧰 Stack Technique

| 🧩 Composant        | Description                                  |
|--------------------|----------------------------------------------|
| **Apache Kafka**    | Ingestion temps réel des données météo       |
| **Python**          | Transformation et insertion dans Elasticsearch |
| **Elasticsearch**   | Stockage et indexation optimisés             |
| **Kibana**          | Visualisation et dashboard interactif        |


---

## 🌐 Visualisations dans le Dashboard

Voici un aperçu des visualisations présentes dans Kibana :

### 🌡️ Température en temps réel
- **📈 Ligne de température** par ville du Mali en temps réel
- **📊 Indicateurs :**
  - Température maximale 🔥
  - Température minimale ❄️
  - Température moyenne 🌡️

### 🌬️ Carte Alerte Vents Forts
- **Carte géographique** avec signalement des zones où les vents dépassent un seuil critique
- **Icône + Couleur personnalisée** pour visualiser l'intensité

### 🌧️ Carte Alerte Pluie
- Affichage en temps réel des zones pluvieuses dans tout le pays

### ☁️ Carte de Couverture Nuageuse
- Visualisation des conditions : `ciel dégagé`, `peu nuageux`, `nuageux`, `couvert`

### 💧 Graphique d’évolution de l’humidité moyenne
- Suivi de la variation de l’humidité dans les principales villes

---

## 🎯 Cas d’usage possible

* Suivi climatique pour agriculture intelligente 🌽
* Alerte précoce pour services d’urgence 🚨
* Intégration avec IoT météo local 🛰️

---

## 📸 Capture d'écran du Dashboard

*Ajoute ici un screenshot de ton dashboard Kibana*

---

## 👨‍💻 Auteur

**Mamadou**
🎓 Étudiant en Ingénierie Informatique - Big Data & AI
🚀 Créateur de solutions smart pour l’Afrique

---

## 🪪 Licence

MIT – Projet libre d’utilisation et d’amélioration ✨

---

## ✨ Si tu kiffes le projet

* ⭐ Laisse un star sur GitHub
* 💬 Ouvre une issue ou une PR si tu veux contribuer
* 🤝 Contacte-moi si tu veux bosser sur des projets data !

---

> *"Les données sont le nouveau pétrole. Ce dashboard te montre comment les raffiner."* 🛢️📊

