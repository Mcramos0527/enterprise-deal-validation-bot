# Enterprise Deal Validation Bot

A Python demo project that simulates an enterprise automation workflow for processing pending approval records in an ERP-style environment.

This demo retrieves pending approval records, enriches them with external portal data, evaluates rule-based decisions, applies actions such as approve / reject / hold / annotate / attach supporting evidence, and generates an audit report.

## Why this project exists

This repository is a fictionalized demonstration inspired by enterprise automation work in large-scale business environments.

It is designed to showcase:
- Python automation
- business rules processing
- ERP-style workflow orchestration
- external data reconciliation
- reporting and auditability
- clean modular project structure

## Features

- Simulated ERP queue processing
- Simulated external portal lookup
- Rule-based decision engine
- Exchange rate validation logic
- Approval / rejection / hold actions
- Comment enrichment
- Attachment simulation
- CSV audit report generation
- Execution logging

## Example scenarios covered

- Previous version rejected -> reject current record
- Deal not won -> skip processing
- FX mismatch + active prior version -> update and approve
- Comment found in external portal -> add note and hold
- Incomplete mapping restriction -> attach support file and hold
- Complex record + comment -> escalate / hold

## Project structure

```text
enterprise-deal-validation-bot/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
├── attachments/
├── output/
└── src/