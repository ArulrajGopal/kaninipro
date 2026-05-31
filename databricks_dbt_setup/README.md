# zero_to_one_dbt

A step-by-step guide to setting up dbt with Databricks from scratch.

---

## Initial Setup

### 1. Create and enter a new project folder

```bash
mkdir dbt_project
cd dbt_project
```

### 2. Update system packages

```bash
sudo apt-get update
```

### 3. Install Python pip

```bash
sudo apt install python3-pip
```

### 4. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install dbt for Databricks

```bash
pip install dbt-databricks
```

### 6. Initialize a new dbt project

```bash
dbt init
```

> Follow the prompts to configure your project name and Databricks connection details.

### 7. Verify the connection

```bash
dbt debug
```

> A successful `dbt debug` confirms your Databricks credentials and connection are configured correctly.
