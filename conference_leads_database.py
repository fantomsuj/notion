#!/usr/bin/env python3
"""
Conference Leads Database for Notion

This script creates a Conference Leads database in Notion if it doesn't already exist.
Designed for tracking leads from conferences like ConExpo.

Usage:
    1. Set NOTION_API_KEY environment variable with your Notion integration token
    2. Set NOTION_PARENT_PAGE_ID environment variable with the parent page ID
    3. Run: python conference_leads_database.py

Requirements:
    pip install notion-client
"""

import os
import sys
from notion_client import Client

# Database configuration
DATABASE_NAME = "Conference Leads"
DATABASE_ICON = "🎪"

# Database schema with properties for conference lead tracking
DATABASE_PROPERTIES = {
    "Name": {
        "title": {}
    },
    "Company": {
        "rich_text": {}
    },
    "Email": {
        "email": {}
    },
    "Phone": {
        "phone_number": {}
    },
    "Conference": {
        "select": {
            "options": [
                {"name": "ConExpo 2026", "color": "blue"},
                {"name": "World of Concrete", "color": "gray"},
                {"name": "CONEXPO-CON/AGG", "color": "orange"},
                {"name": "Bauma", "color": "yellow"},
                {"name": "Other", "color": "default"}
            ]
        }
    },
    "Lead Source": {
        "select": {
            "options": [
                {"name": "Booth Visit", "color": "green"},
                {"name": "Demo Request", "color": "blue"},
                {"name": "Referral", "color": "purple"},
                {"name": "Badge Scan", "color": "orange"},
                {"name": "Networking Event", "color": "pink"},
                {"name": "Speaking Session", "color": "red"},
                {"name": "Other", "color": "default"}
            ]
        }
    },
    "ICP Tier": {
        "select": {
            "options": [
                {"name": "Tier 1 - Subcontractors", "color": "green"},
                {"name": "Tier 2 - General Contractors", "color": "blue"},
                {"name": "Tier 3 - Owner Groups", "color": "purple"},
                {"name": "Unqualified", "color": "gray"}
            ]
        }
    },
    "Status": {
        "select": {
            "options": [
                {"name": "New", "color": "blue"},
                {"name": "Contacted", "color": "yellow"},
                {"name": "Qualified", "color": "green"},
                {"name": "Meeting Scheduled", "color": "purple"},
                {"name": "Proposal Sent", "color": "orange"},
                {"name": "Won", "color": "green"},
                {"name": "Lost", "color": "red"},
                {"name": "Nurture", "color": "gray"}
            ]
        }
    },
    "Priority": {
        "select": {
            "options": [
                {"name": "P0 - Hot", "color": "red"},
                {"name": "P1 - High", "color": "orange"},
                {"name": "P2 - Medium", "color": "yellow"},
                {"name": "P3 - Low", "color": "gray"}
            ]
        }
    },
    "Job Title": {
        "rich_text": {}
    },
    "Fleet Size": {
        "number": {
            "format": "number"
        }
    },
    "Equipment Types": {
        "multi_select": {
            "options": [
                {"name": "Excavator", "color": "orange"},
                {"name": "Dozer", "color": "yellow"},
                {"name": "Loader", "color": "green"},
                {"name": "Grader", "color": "blue"},
                {"name": "Compactor", "color": "purple"},
                {"name": "Scraper", "color": "pink"},
                {"name": "Other", "color": "gray"}
            ]
        }
    },
    "Notes": {
        "rich_text": {}
    },
    "Follow-up Date": {
        "date": {}
    },
    "Captured Date": {
        "date": {}
    },
    "Captured By": {
        "people": {}
    },
    "HubSpot Synced": {
        "checkbox": {}
    },
    "LinkedIn URL": {
        "url": {}
    }
}


def get_notion_client():
    """Initialize Notion client with API key from environment."""
    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("Error: NOTION_API_KEY environment variable not set")
        print("Get your API key from: https://www.notion.so/my-integrations")
        sys.exit(1)
    return Client(auth=api_key)


def get_parent_page_id():
    """Get parent page ID from environment."""
    page_id = os.environ.get("NOTION_PARENT_PAGE_ID")
    if not page_id:
        print("Error: NOTION_PARENT_PAGE_ID environment variable not set")
        print("Find your page ID in the Notion page URL (32 character string)")
        sys.exit(1)
    return page_id


def search_existing_database(notion, database_name):
    """Search for an existing database with the given name."""
    try:
        response = notion.search(
            query=database_name,
            filter={"property": "object", "value": "database"}
        )

        for result in response.get("results", []):
            title_list = result.get("title", [])
            if title_list:
                title = title_list[0].get("plain_text", "")
                if title.lower() == database_name.lower():
                    return result
        return None
    except Exception as e:
        print(f"Error searching for database: {e}")
        return None


def create_conference_leads_database(notion, parent_page_id):
    """Create the Conference Leads database in Notion."""
    try:
        database = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[
                {
                    "type": "text",
                    "text": {"content": DATABASE_NAME}
                }
            ],
            icon={"type": "emoji", "emoji": DATABASE_ICON},
            properties=DATABASE_PROPERTIES
        )
        return database
    except Exception as e:
        print(f"Error creating database: {e}")
        return None


def main():
    """Main function to check for and create Conference Leads database."""
    print(f"Checking for existing '{DATABASE_NAME}' database...")

    notion = get_notion_client()
    parent_page_id = get_parent_page_id()

    # Check if database already exists
    existing_db = search_existing_database(notion, DATABASE_NAME)

    if existing_db:
        db_id = existing_db.get("id", "unknown")
        print(f"\n✓ Database '{DATABASE_NAME}' already exists!")
        print(f"  Database ID: {db_id}")
        print(f"  URL: https://notion.so/{db_id.replace('-', '')}")
        return existing_db

    # Create new database
    print(f"\nDatabase not found. Creating '{DATABASE_NAME}'...")
    new_db = create_conference_leads_database(notion, parent_page_id)

    if new_db:
        db_id = new_db.get("id", "unknown")
        print(f"\n✓ Successfully created '{DATABASE_NAME}' database!")
        print(f"  Database ID: {db_id}")
        print(f"  URL: https://notion.so/{db_id.replace('-', '')}")
        print("\nDatabase properties created:")
        for prop_name in DATABASE_PROPERTIES.keys():
            print(f"  - {prop_name}")
        return new_db
    else:
        print("\n✗ Failed to create database")
        sys.exit(1)


if __name__ == "__main__":
    main()
