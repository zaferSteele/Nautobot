# Zafer Steele's Nautobot API Automation Toolkit

![Nautobot logo](https://docs.nautobot.com/projects/core/en/v2.1.0-beta.1/assets/nautobot_logo.svg)


A collection of Python and Ansible tools to interact with the Nautobot API for network automation and data management. Simplify your network inventory tasks, retrieve and update data, and automate workflows using these handy API tools.

---

## 🚀 Features

### 🐍 Python Scripts

* `pynautobot/`

  * Query Nautobot API directly using `pynautobot`.
  * Examples: Generate available IP reports, list devices by location, get device IDs.

* `graphQL/`

  * Use GraphQL queries to retrieve device data by location.

* `nornir_with_nautobot/`

  * Example script to integrate Nornir with Nautobot data.

### 🔧 Ansible Integration

* `ansible_with_nautobot/`

  * Dynamic inventories based on Nautobot data.
  * Playbooks to retrieve and push data.
  * Secure and variant inventory options.

---

## 📁 Directory Structure

```bash
Nautobot-main/
├── create_nautobot_device_with_loopback.py
├── custom_devices_report_template.j2
├── inventory_loader.py
├── list_devices_ips_by_location.py
├── nornir_show_ip_from_nautobot.py
├── run_nautobot_job_template.py
├── pynautobot/
├── graphQL/
├── nornir_with_nautobot/
├── ansible_with_nautobot/
│   ├── dynamic_inventory/
│   ├── inventory/
│   ├── playbooks/
│   │   └── write_operations/
│   └── playbooks_using_dynamic_inventory/
```

---

## 🛠️ Getting Started

### Prerequisites

```bash
python3 -m venv venv
source venv/bin/activate

```

You may need environment variables or a `.env` file for Nautobot credentials (API Token, URL).

### Install Tools

```bash
pip install pynautobot nornir ansible nornir-nautobot python-dotenv 
```

---

## 💡 Usage Examples

### Python

```bash
python3 pynautobot/get_devices_with_location.py
python3 graphQL/retrieve_devices_by_location.py
```

### Ansible

```bash
ansible-playbook ansible_with_nautobot/playbooks/retrieve_devices_data.yml
ansible-playbook ansible_with_nautobot/playbooks/write_operations/create_devices.yml
```

---

## 📦 Requirements

* `pynautobot`
* `nornir`
* 'nornir-nautobot'
* `ansible`
* `python-dotenv`

---

## 👤 Author

**Zafer Steele**
GitHub: [@zaferSteele](https://github.com/zaferSteele)

---

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
