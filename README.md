# Notion Conference Leads Database

Scripts for managing Notion databases for Bedrock Robotics conference lead tracking.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a Notion Integration:**
   - Go to https://www.notion.so/my-integrations
   - Click "New integration"
   - Name it (e.g., "Bedrock Conference Leads")
   - Copy the API key

3. **Connect integration to your Notion page:**
   - Open the Notion page where you want the database
   - Click "..." menu → "Add connections" → Select your integration

4. **Set environment variables:**
   ```bash
   export NOTION_API_KEY="your-api-key-here"
   export NOTION_PARENT_PAGE_ID="your-page-id-here"
   ```

   The page ID is the 32-character string in your Notion page URL:
   `https://notion.so/Your-Page-Title-abc123def456...` → `abc123def456...`

## Usage

### Create Conference Leads Database

```bash
python conference_leads_database.py
```

This will:
- Check if a "Conference Leads" database already exists
- If not, create one with all necessary properties for tracking conference leads

## Database Schema

The Conference Leads database includes:

| Property | Type | Description |
|----------|------|-------------|
| Name | Title | Lead's full name |
| Company | Text | Company name |
| Email | Email | Contact email |
| Phone | Phone | Contact phone number |
| Conference | Select | Which conference (ConExpo 2026, etc.) |
| Lead Source | Select | How they were captured (Booth Visit, Demo Request, etc.) |
| ICP Tier | Select | Tier 1 Subs / Tier 2 GCs / Tier 3 Owners |
| Status | Select | New → Contacted → Qualified → Won/Lost |
| Priority | Select | P0-P3 priority levels |
| Job Title | Text | Their role at the company |
| Fleet Size | Number | Number of machines in fleet |
| Equipment Types | Multi-select | Excavator, Dozer, Loader, etc. |
| Notes | Text | Conversation notes |
| Follow-up Date | Date | When to follow up |
| Captured Date | Date | When lead was captured |
| Captured By | People | Team member who captured the lead |
| HubSpot Synced | Checkbox | Whether synced to HubSpot CRM |
| LinkedIn URL | URL | Lead's LinkedIn profile |

## Integration with HubSpot

The database includes a "HubSpot Synced" checkbox to track which leads have been synced to HubSpot CRM. This supports the HubSpot migration workflow mentioned in TickTick tasks.
