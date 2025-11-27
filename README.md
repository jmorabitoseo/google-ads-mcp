### Quick start instructions

If you want to start testing this MCP server from your own machine, follow
these simplified steps:

1. **Prerequisites on your laptop**
   - Install Python 3.10+ from `python.org` and make sure "Add Python to PATH"
     is checked.
   - Install `pipx`:

     ```shell
     python -m pip install --user pipx
     python -m pipx ensurepath
     ```

   - Install either:
     - [Gemini Code Assist](https://marketplace.visualstudio.com/items?itemName=Google.geminicodeassist), or
     - [Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/index.md).

2. **Make sure you have these values**
   - `GOOGLE_ADS_DEVELOPER_TOKEN` (Basic or higher access)
   - `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (your manager account ID, digits only)
   - `GOOGLE_PROJECT_ID`
   - `GOOGLE_APPLICATION_CREDENTIALS` (path to the ADC / service account JSON)

3. **Create `~/.gemini/settings.json` on your machine**

   ```json
   {
     "mcpServers": {
       "google-ads-mcp": {
         "command": "pipx",
         "args": [
           "run",
           "--spec",
           "git+https://github.com/googleads/google-ads-mcp.git",
           "google-ads-mcp"
         ],
         "env": {
           "GOOGLE_APPLICATION_CREDENTIALS": "PATH_TO_CREDENTIALS_JSON",
           "GOOGLE_PROJECT_ID": "YOUR_PROJECT_ID",
           "GOOGLE_ADS_DEVELOPER_TOKEN": "YOUR_DEVELOPER_TOKEN",
           "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "YOUR_MANAGER_CUSTOMER_ID"
         }
       }
     }
   }
   ```

4. **Test from Gemini**
   - Launch Gemini Code Assist or Gemini CLI.
   - Type `/mcp` and verify that `google-ads-mcp` appears and is enabled.
   - Ask natural language questions, for example:
     - `what can the ads-mcp server do?`
     - `what customers do I have access to?`
     - `For customer id 1234567890, how many active campaigns did I have in the last 7 days?`


## Try it out

Launch Gemini Code Assist or Gemini CLI and type `/mcp`. You should see
`google-ads-mcp` listed in the results.

Here are some sample prompts to get you started:

- Ask what the server can do:

  ```
  what can the ads-mcp server do?
  ```

- Ask about customers:

  ```
  what customers do I have access to?
  ```

- Ask about campaigns 

  ```
  How many active campaigns do I have?
  ```

  ```
  How is my campaign performance this week?
  ```

### Note about Customer ID

Your agent will need and ask for a customer id for most prompts. If you are 
moving between multiple customers, including the customer ID in the prompt may
be simpler.

```
How many active campaigns do I have for customer id 1234567890
```


## Contributing

Contributions welcome! See the [Contributing Guide](CONTRIBUTING.md).