"""API client for Tasks Todo App addon."""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Optional

import aiohttp

class TasksAppAPIClient:
    """Client for Tasks Todo App API."""

    def __init__(self, host: str, port: int, api_key: str, session: aiohttp.ClientSession, mcp_port: Optional[int] = None):
        """Initialize the API client."""
        self.host = host
        self.port = port
        self.api_key = api_key
        self.session = session
        self.mcp_port = mcp_port
        self.base_url = f"http://{host}:{port}/api"
        self.mcp_url = f"http://{host}:{mcp_port}/mcp" if mcp_port else None
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None
    ) -> dict:
        """Make an API request."""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with self.session.request(
                method,
                url,
                headers=self._headers,
                json=data,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 401:
                    raise Exception("Invalid API key")
                if response.status == 404:
                    raise Exception(f"Endpoint not found: {endpoint}")
                if response.status >= 400:
                    raise Exception(f"API error: {response.status}")
                
                return await response.json()
        except asyncio.TimeoutError:
            raise Exception("API request timeout")
        except aiohttp.ClientError as e:
            raise Exception(f"Connection error: {e}")

    async def get_current_user(self) -> dict:
        """Get current user info."""
        return await self._request("GET", "users/me")

    async def get_lists(self) -> list:
        """Get all lists."""
        return await self._request("GET", "lists")

    async def get_list(self, list_id: str) -> dict:
        """Get a specific list."""
        return await self._request("GET", f"lists/{list_id}")

    async def create_list(self, name: str, description: str = "") -> dict:
        """Create a new list."""
        data = {
            "name": name,
            "description": description
        }
        return await self._request("POST", "lists", data)

    async def get_items(self, list_id: str) -> list:
        """Get items for a list."""
        return await self._request("GET", f"lists/{list_id}/items")

    async def get_item(self, list_id: str, item_id: str) -> dict:
        """Get a specific item."""
        return await self._request("GET", f"lists/{list_id}/items/{item_id}")

    async def create_item(
        self,
        list_id: str,
        title: str,
        description: str = "",
        schedule: Optional[dict] = None,
        tags: list = None
    ) -> dict:
        """Create a new item."""
        data = {
            "title": title,
            "description": description,
            "schedule": schedule or {"type": "once"},
            "tags": tags or []
        }
        return await self._request("POST", f"lists/{list_id}/items", data)

    async def complete_item(self, list_id: str, item_id: str) -> dict:
        """Mark item as complete."""
        return await self._request("POST", f"lists/{list_id}/items/{item_id}/complete")

    async def undo_item(self, list_id: str, item_id: str) -> dict:
        """Undo item completion."""
        return await self._request("POST", f"lists/{list_id}/items/{item_id}/undo")

    async def delete_item(self, list_id: str, item_id: str) -> None:
        """Delete an item."""
        await self._request("DELETE", f"lists/{list_id}/items/{item_id}")

    async def get_health(self) -> dict:
        """Get health status."""
        try:
            return await self._request("GET", "health")
        except:
            return {"status": "error"}

    async def close(self) -> None:
        """Close the session."""
        if self.session:
            await self.session.close()
