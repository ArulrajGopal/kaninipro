# Steps to Databricks CLI auth and create/manage secrets using **Databricks Secret Scopes**.

---

## 1. Authenticate to Databricks

Use the following command to authenticate to your Databricks workspace.

```bash
databricks auth login --host <workspace_url>
```

Example:

```bash
databricks auth login --host https://adb-123456789012.3.azuredatabricks.net
```

After authentication, you can verify the configured profiles.

```bash
databricks auth profiles
```

This command lists all available authentication profiles configured in your system.

---

# Databricks Secret Scope Management

Databricks Secret Scopes allow you to securely store sensitive values such as passwords, API keys, or storage account keys.

---

## 2. Create a Secret Scope

Create a new secret scope using the following command.

```bash
databricks secrets create-scope <scope-name>
```

Example:

```bash
databricks secrets create-scope my-secret-scope
```

---

## 3. Add a Secret to the Scope

Use the following command to add a secret to the created scope.

```bash
databricks secrets put-secret <scope-name> <secret-key-name> --string-value=<secret-value>
```

Example:

```bash
databricks secrets put-secret my-secret-scope storage-key --string-value="abcd1234xyz"
```

---

## Summary

| Command                           | Purpose                                 |
| --------------------------------- | --------------------------------------- |
| `databricks auth login`           | Authenticate to Databricks workspace    |
| `databricks auth profiles`        | List configured authentication profiles |
| `databricks secrets create-scope` | Create a secret scope                   |
| `databricks secrets put-secret`   | Store a secret inside a scope           |

---

## Best Practice

Never hardcode secrets in notebooks, scripts, or source code.
Always store sensitive credentials in **Databricks Secret Scopes** or **Azure Key Vault**.

Secrets can then be accessed securely inside notebooks using:

```python
dbutils.secrets.get(scope="my-secret-scope", key="storage-key")
```
