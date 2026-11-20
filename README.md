# Alerte paniers anti-gaspi (Drive Leclerc)

Vérifie toutes les 15 minutes si la catégorie « anti-gaspi » est apparue sur le
Drive, et envoie une notification Telegram au passage absent → présent.

## Mise en place

1. **Bot Telegram** : parle à `@BotFather`, envoie `/newbot`, récupère le token.
2. **Chat ID** : envoie un message à ton bot, puis ouvre
   `https://api.telegram.org/bot<TOKEN>/getUpdates` et note `chat.id`.
3. **Dépôt GitHub** : crée un dépôt (public = minutes Actions illimitées), puis
   place-y `check.py`, `requirements.txt` et `.github/workflows/check.yml`.
4. **Secrets** : Settings → Secrets and variables → Actions →
   `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID`.
5. **Test** : onglet Actions → « Check anti-gaspi » → Run workflow.

## Points d'attention

- Le workflow tourne en UTC ; ajuste la plage horaire du `cron` si besoin.
- GitHub peut retarder ou sauter des exécutions planifiées.
- Si les logs montrent une page de blocage, les IP de GitHub sont refusées :
  il faudra faire tourner `check.py` ailleurs (Raspberry Pi, petit VPS).
- Le site interdit l'accès automatisé dans son robots.txt : garde une
  fréquence raisonnable et usage personnel.
