# FloraAI

FloraAI is a Streamlit web app project for floral design and bouquet cost planning.

## Apps

| App | File to run or deploy | Features |
| --- | --- | --- |
| Cost dashboard | `floraai_dashboard.py` | Plan materials, labor, and expenses; compare selling prices; download a scenario as CSV. No API key needed. |
| Floral design prototype | `app.py` | Browse arrangements and customize bouquet concepts. AI image generation requires an OpenAI API key. |

The dashboard uses editable planning assumptions, not recorded sales. Scenario edits are kept in the current session; use **Download this scenario** to save them. They are not written to the repository. The floral design app is a prototype; its shopping bag does not process payments.

## Project aims

- Explore the costs and contribution margins of a small floral business.
- Use bouquet previews to help communicate flower, color, and style preferences.
- Collect reliable cost and preparation-time data before exploring predictive models.
