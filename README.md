# 📚 Livres KDP — Sacha

Archive automatisée de la collection de livres jeunesse publiés sur Amazon KDP par **Apolline Verger** (nom de plume).

Collection : **« Au seuil des merveilles »**
Tranche d'âge : 6-8 ans
Format : Album carré 22,8 × 22,8 cm
Pipeline : Higgsfield (Nano Banana Pro 2K) → Python (PIL) → PDF KDP

---

## 📖 Tomes publiés

| # | Titre | Statut | Lien |
|---|---|---|---|
| 1 | Lila et la clé du grenier | 🔵 Prêt à publier | [📁 Tome 1](./Tome-1_Lila-et-la-cle-du-grenier/) |
| 2 | Lila et le grenier des autres | 🔵 Prêt à publier | [📁 Tome 2](./Tome-2_Lila-et-le-grenier-des-autres/) |

---

## 🗂️ Structure d'un tome

```
Tome-N_titre/
├── README.md            ← présentation du tome
├── PDFs/                ← fichiers prêts à uploader sur KDP
│   ├── INTERIEUR_KDP.pdf
│   └── COUVERTURE_KDP.pdf
├── Sources/
│   ├── scripts/         ← scripts Python d'assemblage
│   └── images/          ← illustrations 2048×2048
├── Previews/            ← previews HTML pour validation visuelle
└── Metadata/            ← description Amazon, mots-clés, checklist
```

---

## 🔄 Workflow de génération

1. **Génération images** : Higgsfield (Nano Banana Pro 2K) avec images de référence des personnages
2. **Assemblage PDFs** : scripts Python natifs (Pillow + ReportLab)
3. **Validation** : previews HTML générées avec textes overlay
4. **Archive** : push automatique vers ce repo
5. **Publication** : upload manuel sur KDP (description et métadonnées dans `Metadata/`)

---

## 📓 Cerveau du projet

La database Notion **📚 Bibliothèque KDP** centralise les métadonnées vivantes (statut, prix, ISBN, date de publication, etc.) et les fichiers KDP : 
→ https://www.notion.so/b0ba4f22190f496fb62881a42ebd5d23
