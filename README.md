# FloraAI

FloraAI is a Streamlit web app project for floral design and bouquet cost planning.

## Apps

| App | File to run or deploy | Features |
| --- | --- | --- |
| Cost dashboard | `floraai_dashboard.py` | Plan materials, labor, and expenses; compare selling prices; download a scenario as CSV. No API key needed. |
| Floral design prototype | `app.py` | Browse arrangements and customize bouquet concepts. AI image generation requires an OpenAI API key. |

The dashboard uses editable planning assumptions, not recorded sales. Scenario edits are kept in the current session; use **Download this scenario** to save them. They are not written to the repository. The floral design app is a prototype; its shopping bag does not process payments.

## Run on your computer

Use Python 3.10 or newer (Python 3.12 is a suitable choice for cloud deployment).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run floraai_dashboard.py
```

Open the local URL printed in the terminal, usually `http://localhost:8501`. Keep the terminal running while using the app. To open the floral design prototype instead, run `python -m streamlit run app.py`.

## View the dashboard online

GitHub stores and displays the source code. GitHub Pages serves static websites and cannot run this Python/Streamlit server. Deploy the app with [Streamlit Community Cloud](https://share.streamlit.io/) to get a live website that works while your computer is off.

1. Sign in to Streamlit Community Cloud with your GitHub account and select **Create app**.
2. Choose **Yup, I have an app**.
3. Enter repository `gini-chen/flora_ai`, branch `main`, and main file path `floraai_dashboard.py`.
4. In **Advanced settings**, select Python 3.12. Leave Secrets empty for the cost dashboard.
5. Click **Deploy**. Streamlit will install `requirements.txt` and provide a URL ending in `.streamlit.app`.
6. Copy that URL to share the running dashboard. Add it to this README and the GitHub repository's **About → Website** field so visitors can open it from GitHub.

For the floral design prototype, create another app using `app.py` as the main file. Add its API key in the hosted app's Secrets settings to enable image generation.

After deployment, pushes to the selected branch update the hosted app. This repository contains deployment-ready source code; it does not yet declare a live dashboard URL.

See the official [deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## Keep local files private

The repository stays public. `.gitignore` excludes these files from normal Git commits while keeping them on your computer:

- Real credentials: `.streamlit/secrets.toml`, other `secrets*.toml` files, `.env` files, and local AWS credentials.
- Personal notes and instructions: `notes`, `notes.*`, and root-level `instructions*` files.
- Local drafts: `dashboard.py` (a duplicate dashboard) and `cost_model.py` (a scratch calculation script). The shared dashboard is `floraai_dashboard.py`.
- CSV exports, `private/`, `local/`, virtual environments, caches, logs, and editor settings.

To configure the floral design app locally, copy `.streamlit/secrets.example.toml` to `.streamlit/secrets.toml` and fill in your key. The example file contains no credentials. For cloud deployment, enter secrets in the app's settings following the [secrets management guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

`.gitignore` does not hide files already committed to Git history. Review `git status` before committing, and avoid force-adding private files. New scratch files can go in `local/`; private business files can go in `private/`.

## Project aims

- Explore the costs and contribution margins of a small floral business.
- Use bouquet previews to help communicate flower, color, and style preferences.
- Collect reliable cost and preparation-time data before exploring predictive models.
