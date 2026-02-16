# 🩺 OCI INFRASTRUCTURE AUDIT HANDOVER: ACCOUNT 3

**To the Auditor Agent:**
You have been dispatched to perform a meticulous security and infrastructure audit of **OCI Account 3** (Prototype/Empty Tenancy). Your goal is to verify the live environment against the proposed inventory PR and identify any "invisible" custom settings.

---

## 🎯 MISSION SCOPE

Compare live OCI data against:

- **Repo:** `oracle-cloud-vps`
- **Branch:** `inventory/account3`
- **Baseline:** `BASELINE.md`

You are looking for **Discrepancies**, **Hallucinations**, and **Gaps** (undocumented settings).

---

## 🔑 AUTHENTICATION & LOGIN

1. Ask the User for the **ROOT_OCID** and **Region** of Account 3.
2. Log into the **OCI Cloud Shell**.
3. Verify you are in the correct compartment/account by running:
   `oci iam compartment get --compartment-id [ROOT_OCID]`

---

## 📋 DATA COLLECTION COMMANDS (DEEP SCAN)

### 1. The Basics (Resource Inventory)

```bash
# Instances (Check Shapes, OCID, State)
oci compute instance list --all

# VCNs & Networking (Check CIDRs, Subnets, DNS)
oci network vcn list --all
oci network subnet list --all
oci network security-list list --all
```

### 2. Custom Governance (Non-Standard Settings)

The user has set **Custom Budget Alerts**. You MUST check these:

```bash
# Budget & Alerts (Financial Guardrails)
oci budget budget list --compartment-id [ROOT_OCID]
# For each budget ID found:
oci budget alert-rule list --budget-id [BUDGET_ID]
```

### 3. Identity & Metadata

```bash
# Resource Tags (Look for project IDs, automation tags)
# oci resources tag-summary get ... (Or check list output)

# Groups & Policies (Access control)
oci iam policy list --compartment-id [ROOT_OCID]
```

### 4. Terraform Presence

Check if this account was initialized via Terraform/OpenTofu:

```bash
oci resourcemanager stack list --all
```

---

## 🧐 COMPARISON PROTOCOL (TRUST NO ONE)

- **Wait/Check CIDRs**: If `vcns.json` says `10.0.0.0/16` but OCI says `10.1.0.0/16`, flag it.
- **Instance Shapes**: If the PR says `VM.Standard.E2.1.Micro` but OCI has an **A1.Flex**, flag it.
- **Invisible Resources**: If OCI has a Volume or a Bucket not in the `raw/` directory, flag it.
- **Budget Alerts**: Any alert discovered that isn't in `ACCOUNT3-SUMMARY.md` is a **Gap**.

---

## 🤖 RECOMMENDED MODEL SETTINGS

- **Model**: Claude 3.7 Sonnet (Thinking) or Claude 3.5 Sonnet.
- **Mode**: **Planning Mode** (Thinking enabled).
- **Attitude**: Skeptical, Meticulous, Auditor-first.
