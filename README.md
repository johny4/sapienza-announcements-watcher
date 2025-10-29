# Sapienza Announcements Watcher

This repository automatically monitors the Sapienza University of Rome – Cybersecurity course announcements page:  
[https://corsidilaurea.uniroma1.it/it/course/33516/announcements](https://corsidilaurea.uniroma1.it/it/course/33516/announcements)

Every 6 hours, a GitHub Action checks the page for new announcements.  
If new ones are found, it automatically creates a GitHub Issue with the title and link, so you receive an email notification from GitHub.

## Setup

If you fork this repository or adapt it for another course:
1. Edit the URL inside `fetch.py` to match the new page.
2. Make sure GitHub Actions are enabled under  
   **Settings → Actions → General → Allow all actions**.
3. Watch your own repository to receive email notifications when new Issues are created.

## Example

When new announcements are detected, a GitHub Issue like this will appear:

> **[AUTO] 1 new announcement(s)**  
> Detected new announcement(s) at 2025-10-29 09:00 UTC  
> - “Esame di Sicurezza Informatica”  
>   [https://corsidilaurea.uniroma1.it/it/course/33516/announcements#announcement-XXXX](https://corsidilaurea.uniroma1.it/it/course/33516/announcements#announcement-XXXX)

## Author

Created by João Trocado (johny). Made in Rome :)
